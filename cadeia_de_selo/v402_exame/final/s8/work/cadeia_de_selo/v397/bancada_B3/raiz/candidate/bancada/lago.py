# -*- coding: utf-8 -*-
"""lago.py -- o LAGO RESIDENTE da Bancada Um: os arquivos de dados da TGL carregados INTEIROS na RAM e mantidos carregados.

* FITS por leitor próprio em numpy puro (sem dependência nova): cabeçalhos de 2880 bytes, HDUs IMAGE e BINTABLE (formatos L X B I J K A
  E D C M P Q, com repetição); a tabela binária fica na RAM como UM buffer e é vista sem cópia por um dtype estruturado big-endian;
  TSCAL/TZERO e BSCALE/BZERO aplicados na leitura da coluna. NPY/NPZ por numpy; CSV/DAT/TXT tabulares por pandas.
* sha256 calculado NA MESMA PASSADA da leitura (a proveniência não custa uma segunda leitura).
* cópias idênticas (mesmo nome e tamanho em casas diferentes) carregadas UMA vez; a outra vira apelido, conferida pelo hash.
* orçamento: nunca passa de uma fração da RAM livre (padrão 60%); o que não cabe fica listado como não carregado, com o motivo.
* colunas sobem para a GPU SOB DEMANDA (histograma, mapa 2D) e voltam como números; os originais em disco nunca são escritos.
"""
import hashlib
import math
import os
import threading
import time

import numpy as np

BLOCO = 2880
TFORM = {"L": ("u1", 1), "B": ("u1", 1), "I": (">i2", 2), "J": (">i4", 4), "K": (">i8", 8), "E": (">f4", 4), "D": (">f8", 8),
         "C": (">c8", 8), "M": (">c16", 16)}
BITPIX = {8: "u1", 16: ">i2", 32: ">i4", 64: ">i8", -32: ">f4", -64: ">f8"}
TABULARES = (".csv", ".dat", ".txt")
SUPORTADOS = (".fits", ".fit", ".npy", ".npz") + TABULARES


def _cartas(buf, off):
    """Lê um cabeçalho FITS a partir de off; devolve (dict, off_dos_dados)."""
    h, i = {}, off
    while True:
        bloco = bytes(buf[i:i + BLOCO])
        if len(bloco) < BLOCO:
            raise ValueError("cabeçalho FITS truncado")
        i += BLOCO
        fim = False
        for k in range(0, BLOCO, 80):
            c = bloco[k:k + 80].decode("ascii", "replace")
            chave = c[:8].strip()
            if chave == "END":
                fim = True
                break
            if c[8:10] == "= ":
                v = c[10:].split("/")[0].strip() if not c[10:].strip().startswith("'") else c[10:].strip()
                if v.startswith("'"):
                    v = v[1:v.rfind("'")].strip() if v.rfind("'") > 0 else v.strip("'")
                else:
                    try:
                        v = int(v)
                    except ValueError:
                        try:
                            v = float(v.replace("D", "E"))
                        except ValueError:
                            v = {"T": True, "F": False}.get(v, v)
                h[chave] = v
        if fim:
            return h, i


def _dtype_bintable(h):
    campos, nomes = [], set()
    for n in range(1, int(h.get("TFIELDS", 0)) + 1):
        f = str(h["TFORM%d" % n]).strip()
        j = 0
        while j < len(f) and f[j].isdigit():
            j += 1
        r = int(f[:j]) if j else 1
        t = f[j]
        nome = str(h.get("TTYPE%d" % n, "col%d" % n)).strip() or "col%d" % n
        base = nome; k = 2
        while nome.lower() in nomes:
            nome = "%s_%d" % (base, k); k += 1
        nomes.add(nome.lower())
        if t == "A":
            campos.append((nome, "S%d" % max(r, 1)))
        elif t == "X":
            campos.append((nome, "u1", (int(math.ceil(r / 8.0)),)))
        elif t in ("P", "Q"):
            campos.append((nome, ">i4" if t == "P" else ">i8", (2,)))
        elif r == 0:
            continue
        else:
            dt = TFORM[t][0]
            campos.append((nome, dt) if r == 1 else (nome, dt, (r,)))
    return np.dtype(campos)


class Tabela:
    """Uma HDU (ou arquivo tabular) residente."""

    def __init__(self, arquivo, hdu, tipo, dados, cab=None, escalas=None):
        self.arquivo, self.hdu, self.tipo, self.dados, self.cab, self.escalas = arquivo, hdu, tipo, dados, cab or {}, escalas or {}

    @property
    def n_linhas(self):
        if self.tipo == "tabela":
            return int(len(self.dados))
        return int(self.dados.shape[0]) if self.dados.ndim else 1

    def colunas(self):
        if self.tipo == "tabela":
            return [dict(nome=n, dtype=str(self.dados.dtype.fields[n][0]), forma=list(self.dados.dtype.fields[n][0].shape)) for n in self.dados.dtype.names]
        return [dict(nome="(imagem)", dtype=str(self.dados.dtype), forma=list(self.dados.shape))]

    def coluna(self, nome):
        if self.tipo != "tabela":
            return np.asarray(self.dados, dtype=np.float64).ravel()
        v = self.dados[nome]
        esc, zero = self.escalas.get(nome, (1.0, 0.0))
        if v.dtype.kind in "iuf":
            v = v.astype(v.dtype.newbyteorder("=")) if v.dtype.byteorder == ">" else v
            if esc != 1.0 or zero != 0.0:
                v = v * esc + zero
        return v


class Lago:
    def __init__(self, raizes, fracao_ram=0.60):
        self.raizes = raizes
        self.fracao_ram = fracao_ram
        self.arquivos = {}          # chave -> dict(caminho, bytes, sha256, tabelas, estado, motivo, segundos)
        self.buffers = {}
        self.estado = dict(estado="parado", progresso=0.0, carregados=0, bytes_residentes=0)
        self.lock = threading.Lock()

    @staticmethod
    def _ram_livre():
        try:
            import ctypes

            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("c", ctypes.c_ulong), ("t", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong),
                            ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
            m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return int(m.a)
        except Exception:
            return 0

    def inventario(self):
        itens = []
        for r in self.raizes:
            if not os.path.isdir(r):
                continue
            for dp, dn, fn in os.walk(r):
                for f in fn:
                    p = os.path.join(dp, f)
                    e = os.path.splitext(f)[1].lower()
                    if e in SUPORTADOS:
                        try:
                            itens.append((os.path.getsize(p), p))
                        except OSError:
                            pass
        return sorted(itens)                          # pequenos primeiro: o painel enche logo

    def _le(self, p, tamanho):
        buf = bytearray(tamanho)
        mv = memoryview(buf)
        h = hashlib.sha256()
        with open(p, "rb", buffering=0) as f:
            i = 0
            while i < tamanho:
                n = f.readinto(mv[i:i + (64 << 20)])
                if not n:
                    break
                h.update(mv[i:i + n]); i += n
        if i != tamanho:
            raise IOError("leitura curta: %d de %d bytes" % (i, tamanho))
        return buf, h.hexdigest()

    def _fits(self, chave, buf):
        tabelas, off, n = [], 0, 0
        while off + BLOCO <= len(buf):
            try:
                h, doff = _cartas(buf, off)
            except ValueError:
                break
            naxis = int(h.get("NAXIS", 0))
            dims = [int(h.get("NAXIS%d" % k, 0)) for k in range(1, naxis + 1)]
            bitpix = int(h.get("BITPIX", 8))
            tam = abs(bitpix) // 8 * int(h.get("GCOUNT", 1)) * (int(h.get("PCOUNT", 0)) + (int(np.prod(dims)) if dims else 0))
            xt = str(h.get("XTENSION", "PRIMARY")).strip()
            if xt == "BINTABLE" and dims:
                dt = _dtype_bintable(h)
                linhas = dims[1]
                if dt.itemsize != dims[0]:
                    raise ValueError("BINTABLE: largura do dtype %d != NAXIS1 %d" % (dt.itemsize, dims[0]))
                arr = np.frombuffer(buf, dtype=dt, count=linhas, offset=doff)
                esc = {}
                for k in range(1, int(h.get("TFIELDS", 0)) + 1):
                    nome = str(h.get("TTYPE%d" % k, "col%d" % k)).strip()
                    s, z = float(h.get("TSCAL%d" % k, 1.0)), float(h.get("TZERO%d" % k, 0.0))
                    if (s, z) != (1.0, 0.0):
                        esc[nome] = (s, z)
                tabelas.append(Tabela(chave, n, "tabela", arr, {k: h[k] for k in list(h)[:60]}, esc))
            elif dims and bitpix in BITPIX:
                arr = np.frombuffer(buf, dtype=BITPIX[bitpix], count=int(np.prod(dims)), offset=doff).reshape(dims[::-1])
                tabelas.append(Tabela(chave, n, "imagem", arr, {k: h[k] for k in list(h)[:60]}))
            off = doff + int(math.ceil(tam / BLOCO)) * BLOCO
            n += 1
        return tabelas

    @staticmethod
    def _so_hash(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(64 << 20), b""):
                h.update(b)
        return h.hexdigest()

    def _tabular(self, chave, p):
        import pandas as pd
        primeira = ""
        with open(p, encoding="utf-8", errors="replace") as f:
            for ln in f:
                if ln.strip() and not ln.lstrip().startswith("#"):
                    primeira = ln
                    break
        sep = "," if primeira.count(",") >= 2 else r"\s+"
        df = pd.read_csv(p, sep=sep, engine="python" if sep != "," else "c", comment="#")
        return [Tabela(chave, 0, "tabela", df.to_records(index=False))]

    @staticmethod
    def _npy_do_buffer(buf):
        import io
        fp = io.BytesIO(bytes(buf[:4096]))
        versao = np.lib.format.read_magic(fp)
        leitor = np.lib.format.read_array_header_1_0 if versao == (1, 0) else np.lib.format.read_array_header_2_0
        forma, fortran, dt = leitor(fp)
        if dt.hasobject:
            raise ValueError("npy com objetos (pickle) recusado")
        arr = np.frombuffer(buf, dtype=dt, count=int(np.prod(forma)) if forma else 1, offset=fp.tell())
        return arr.reshape(forma, order="F" if fortran else "C")

    def carregar_tudo(self):
        with self.lock:
            if self.estado["estado"] == "carregando":
                return
            self.estado = dict(estado="carregando", progresso=0.0, carregados=0, bytes_residentes=0, inicio=time.time())
        itens = self.inventario()
        total = sum(s for s, _ in itens) or 1
        feito = 0
        vistos = {}
        orcamento = self.fracao_ram * self._ram_livre()
        for tamanho, p in itens:
            chave = p
            rec = dict(caminho=p, bytes=tamanho, estado="na_fila")
            self.arquivos[chave] = rec
            ident = (os.path.basename(p).lower(), tamanho)
            try:
                if ident in vistos:
                    ori = self.arquivos[vistos[ident]]
                    sha_c = self._so_hash(p)                     # a cópia é LIDA e conferida: apelido só com bytes idênticos
                    if sha_c == ori.get("sha256"):
                        rec.update(estado="apelido", apelido_de=vistos[ident], sha256=sha_c, tabelas=ori.get("tabelas"))
                        feito += tamanho
                        continue
                if self.estado["bytes_residentes"] + tamanho > orcamento:
                    rec.update(estado="nao_carregado", motivo="orçamento de RAM (%.0f%% da livre) seria excedido" % (100 * self.fracao_ram))
                    feito += tamanho
                    continue
                t0 = time.time()
                e = os.path.splitext(p)[1].lower()
                buf, sha = self._le(p, tamanho)
                if e in (".fits", ".fit"):
                    tabs = self._fits(chave, buf)
                    self.buffers[chave] = buf
                elif e == ".npy":
                    arr = self._npy_do_buffer(buf)
                    tabs = [Tabela(chave, 0, "tabela" if arr.dtype.names else "imagem", arr)]
                    self.buffers[chave] = buf
                elif e == ".npz":
                    import io
                    z = np.load(io.BytesIO(bytes(buf)), allow_pickle=False)
                    tabs = [Tabela(chave, i, "tabela" if z[k].dtype.names else "imagem", z[k], {"nome": k}) for i, k in enumerate(z.files)]
                    del buf
                else:
                    tabs = self._tabular(chave, p)
                    del buf
                rec.update(estado="residente", sha256=sha, tabelas=tabs, segundos=round(time.time() - t0, 2))
                vistos[ident] = chave
                self.estado["bytes_residentes"] += tamanho
                self.estado["carregados"] += 1
            except Exception as ex:                    # falha visível, nunca «ok» falso
                rec.update(estado="falhou", motivo=repr(ex)[:300])
            feito += tamanho
            self.estado["progresso"] = feito / total
        self.estado.update(estado="residente", progresso=1.0, segundos=round(time.time() - self.estado["inicio"], 1))

    def resumo(self):
        out = []
        for chave, r in self.arquivos.items():
            tabs = r.get("tabelas") or []
            out.append(dict(caminho=chave, bytes=r["bytes"], estado=r["estado"], sha256=(r.get("sha256") or "")[:16], motivo=r.get("motivo"),
                            apelido_de=r.get("apelido_de"), segundos=r.get("segundos"),
                            tabelas=[dict(hdu=t.hdu, tipo=t.tipo, linhas=t.n_linhas, n_colunas=len(t.colunas()) if t.tipo == "tabela" else None,
                                          forma=list(t.dados.shape) if t.tipo == "imagem" else None) for t in tabs]))
        return dict(estado=self.estado, arquivos=out)

    def tabela(self, caminho, hdu):
        r = self.arquivos.get(caminho)
        if not r or r["estado"] not in ("residente", "apelido"):
            raise KeyError("arquivo não residente: %s" % caminho)
        for t in r["tabelas"]:
            if int(t.hdu) == int(hdu):
                return t
        raise KeyError("HDU %s ausente" % hdu)


# ---------------- operações de GPU sobre o lago residente ----------------
_CACHE_GPU = {}            # (arquivo, hdu, coluna) -> tensor float64 na GPU (colunas usadas FICAM na VRAM)
_CACHE_ORDEM = []
_CACHE_TETO_BYTES = 8 * 2 ** 30


def _coluna_gpu(tab, nome, dev):
    """A coluna na GPU, com cache LRU: a segunda consulta não recopia nem reenvia. Teto: mín(8 GiB, 40% da VRAM livre)."""
    import torch
    chave = (tab.arquivo, int(tab.hdu), nome, str(dev))
    if chave in _CACHE_GPU:
        _CACHE_ORDEM.remove(chave); _CACHE_ORDEM.append(chave)
        return _CACHE_GPU[chave]
    v = np.asarray(tab.coluna(nome)).ravel()
    if v.dtype.kind not in "iuf":
        raise ValueError("coluna não numérica")
    t = torch.from_numpy(np.ascontiguousarray(v.astype(np.float64, copy=False))).to(dev)
    teto = _CACHE_TETO_BYTES
    if str(dev).startswith("cuda"):
        livre, _ = torch.cuda.mem_get_info()
        teto = min(teto, int(0.4 * livre))
    usado = sum(x.numel() * 8 for x in _CACHE_GPU.values())
    while _CACHE_ORDEM and usado + t.numel() * 8 > teto:
        velho = _CACHE_ORDEM.pop(0); usado -= _CACHE_GPU[velho].numel() * 8; del _CACHE_GPU[velho]
    if t.numel() * 8 <= teto:
        _CACHE_GPU[chave] = t; _CACHE_ORDEM.append(chave)
    return t


def cache_gpu_resumo():
    return dict(colunas=len(_CACHE_GPU), bytes=int(sum(x.numel() * 8 for x in _CACHE_GPU.values())),
                itens=[dict(arquivo=k[0].split("\\")[-1], hdu=k[1], coluna=k[2]) for k in _CACHE_ORDEM[-20:]])


def _gpu(tab, nome, dev):
    import torch
    t = _coluna_gpu(tab, nome, dev)
    return t[torch.isfinite(t)]


def histograma(tab, coluna, bins=120, faixa=None, log=False, dev="cuda"):
    import torch
    t0 = time.time()
    t = _gpu(tab, coluna, dev)
    n_total = int(t.numel())
    if log:
        t = torch.log10(t[t > 0])
    if faixa:
        lo, hi = float(faixa[0]), float(faixa[1])
    else:
        amostra = t if t.numel() <= 8_000_000 else t[torch.randint(0, t.numel(), (8_000_000,), device=t.device)]
        q = torch.quantile(amostra, torch.tensor([0.001, 0.999], device=t.device, dtype=t.dtype))
        lo, hi = float(q[0]), float(q[1])
        if hi <= lo:
            lo, hi = float(t.min()), float(t.max()) + 1e-12
    h = torch.histc(t, bins=int(bins), min=lo, max=hi)
    if dev != "cpu":
        torch.cuda.synchronize()
    return dict(coluna=coluna, n=n_total, n_finito=int(t.numel()), media=float(t.mean()), desvio=float(t.std()), minimo=float(t.min()), maximo=float(t.max()),
                faixa=[lo, hi], log10=bool(log), contagens=h.cpu().numpy().tolist(), segundos=round(time.time() - t0, 4), dispositivo=str(dev))


def mapa2d(tab, cx, cy, bins=(360, 180), faixa=None, dev="cuda"):
    import torch
    t0 = time.time()
    X = _coluna_gpu(tab, cx, dev)
    Y = _coluna_gpu(tab, cy, dev)
    ok = torch.isfinite(X) & torch.isfinite(Y)
    X, Y = X[ok], Y[ok]
    if faixa:
        (x0, x1), (y0, y1) = faixa
    else:
        x0, x1, y0, y1 = float(X.min()), float(X.max()), float(Y.min()), float(Y.max())
    nx, ny = int(bins[0]), int(bins[1])
    ix = torch.clamp(((X - x0) / (x1 - x0 + 1e-300) * nx).long(), 0, nx - 1)
    iy = torch.clamp(((Y - y0) / (y1 - y0 + 1e-300) * ny).long(), 0, ny - 1)
    H = torch.bincount(ix * ny + iy, minlength=nx * ny).reshape(nx, ny)
    if dev != "cpu":
        torch.cuda.synchronize()
    return dict(x=cx, y=cy, n=int(X.numel()), faixa=[[x0, x1], [y0, y1]], bins=[nx, ny], contagens=H.cpu().numpy().tolist(),
                segundos=round(time.time() - t0, 4), dispositivo=str(dev))
