# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  ACOM ARCHIVE v1  —  o empacotador multi-arquivo do dispositivo   ║
║  Muitos arquivos / pastas inteiras -> UM contêiner .acom selado.  ║
║  IALD LTDA — beta_TGL = alpha_fine * sqrt(e) — Zero Free Params.  ║
║  Patente INPI: BR 10 2025 026951-1 (ACOM)                         ║
╚══════════════════════════════════════════════════════════════════╝

Extensão do dispositivo ACOM (acom_codec.py) para ARQUIVO MÚLTIPLO — a base do backup
com a própria criptografia da casa e, no futuro, da leitura direta de .acom pela IALD Nativa.

FORMATO (.acom archive v1) — auto-descritível, streamável, restaurável bit-a-bit:

    [MAGIC 10B]
    [u32 header_len][header_json]         # v, ferramenta, beta, enc?, kdf{salt,n,r,p}, count
    [record_0][record_1]...[record_N-1]   # cada record = blob do arquivo (comprimido; se cifrado, AES-GCM)
    [manifest_bytes]                       # entradas {path, size, sha256, method, off, len, i} + meta_cadeia
    [MAGIC_END 10B][u64 manifest_off][u32 manifest_len]   # rodapé: o leitor busca o fim -> manifesto

MODOS:
  * PLANO   — empacota + comprime (regime ontológico do ACOM) + integridade SHA-256.
              STDLIB PURO (lzma/bz2/zlib/hashlib) — a Nativa lê sem dependência extra.
  * CIFRADO — + AES-256-GCM por-arquivo, chave = scrypt(senha, salt+beta) -> HKDF por-índice.
              O manifesto também é cifrado (a lista de arquivos só abre com a senha).

REGRA (a régua): beta NUNCA literal (via acom_codec.beta_provenance); restauração bit-exata
verificada por SHA-256; proteção anti-zip-slip na extração; tetos anti-bomba na entrada
não-confiável (web) e relaxados/streamed para os próprios arquivos (CLI). Simulação não
valida física — este é o dispositivo de ENGENHARIA da patente, e ele roda de verdade.
"""
from __future__ import annotations

import hashlib
import io
import json
import lzma
import os
import struct
import zlib
from pathlib import Path
from typing import Callable, Iterable, Iterator, Optional, Union

# o codec do próprio dispositivo (mesma pasta) — reuso do regime ontológico + proveniência β
try:
    from . import acom_codec as _codec          # quando importado como pacote
except Exception:                                # pragma: no cover - execução standalone
    import importlib.util as _ilu
    import sys as _sys
    _spec = _ilu.spec_from_file_location("acom_codec", str(Path(__file__).with_name("acom_codec.py")))
    _codec = _ilu.module_from_spec(_spec)
    _sys.modules["acom_codec"] = _codec          # registrar ANTES do exec (o @dataclass se procura aqui)
    _spec.loader.exec_module(_codec)             # type: ignore

# a PORTA ÚNICA (acom_auto): o sinal escolhe o codec. O empacotador a usa com fidelity="exata"
# — ela decide a ROTA (e poupa o LZMA-extremo nos contêineres já selados), nunca a integridade.
# Opcional por construção: se o arquivo não estiver presente, o empacotador segue no codec.
try:
    from . import acom_auto as _auto             # quando importado como pacote
except Exception:                                # pragma: no cover - execução standalone
    try:
        import importlib.util as _ilu2
        import sys as _sys2
        if "acom_auto" in _sys2.modules:
            _auto = _sys2.modules["acom_auto"]
        else:
            _p = Path(__file__).with_name("acom_auto.py")
            if _p.is_file():
                _spec2 = _ilu2.spec_from_file_location("acom_auto", str(_p))
                _auto = _ilu2.module_from_spec(_spec2)
                _sys2.modules["acom_auto"] = _auto
                _spec2.loader.exec_module(_auto)  # type: ignore
            else:
                _auto = None
    except Exception:
        _auto = None

MAGIC = b"ACOMARCH1\x00"
MAGIC_END = b"ACOMAEND1\x00"
FMT_VERSION = 1
FOOTER_LEN = len(MAGIC_END) + 8 + 4              # MAGIC_END + u64 offset + u32 len

# limites (a web passa untrusted=True; o CLI passa untrusted=False para os próprios arquivos)
ACOM_FILE_CAP = _codec.MAX_INPUT_BYTES           # 64 MB → passa pelo codec do dispositivo (regime+paleta)
BIG_FILE_STREAM_CHUNK = 8 * 1024 * 1024          # 8 MB por chunk no streaming de arquivos grandes
MAX_FILES = 500_000                              # backstop de nº de arquivos
WEB_MAX_TOTAL_INPUT = 512 * 1024 * 1024          # teto agregado da entrada na WEB (memória do navegador)
WEB_MAX_DECOMP_TOTAL = 512 * 1024 * 1024         # teto anti-bomba agregado na WEB (coerente c/ RAM da nuvem)
CIFRADO_STREAM_CAP = 2 * 1024 * 1024 * 1024      # teto do arquivo grande+cifrado (AES-GCM numa passada; bufferiza)
_ZERO_NONCE = b"\x00" * 12                        # seguro: chave ÚNICA por arquivo (HKDF por índice)
MIN_PASSWORD = 8

# métodos de record
M_STORE = "store"    # bruto (incompressível)
M_ZLIB = "zlib"
M_XZ = "xz"          # lzma stream (arquivos grandes)
M_ACOM = "acom"      # contêiner do próprio acom_codec (arquivos ≤ ACOM_FILE_CAP: regime+paleta da casa)
# ALLOWLIST de decodificação: o empacotador só PRODUZ estes; recusar qualquer outro método vindo
# de um manifesto forjado (o bz2, por ex., nunca é gerado — não abrir bomba de bz2 sem teto).
_DECODE_ALLOWED = frozenset((M_STORE, M_ACOM, M_XZ, M_ZLIB))


# ───────────────────────────────────────────────────────── β (nunca literal)
def beta_provenance() -> dict:
    return _codec.beta_provenance()


def _beta_bytes() -> bytes:
    """β como assinatura de domínio da KDF (derivado, jamais 0.012 literal)."""
    return ("%.18e" % _codec.BETA_TGL).encode("ascii")


# ───────────────────────────────────────────────────────── criptografia (cifrado)
def _crypto():
    """Importa cryptography só quando o modo cifrado é usado (plano é stdlib puro)."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    return AESGCM, HKDF, hashes


def crypto_available() -> bool:
    try:
        _crypto(); return True
    except Exception:
        return False


def _derive_master(password: str, salt: bytes) -> bytes:
    if not isinstance(password, str) or len(password) < MIN_PASSWORD:
        raise ValueError(f"senha muito curta (mín {MIN_PASSWORD}).")
    pw = password.encode("utf-8")
    # scrypt memory-hard sobre os BYTES da senha + salt + β (domínio da casa). Nada literal.
    return hashlib.scrypt(pw, salt=salt + _beta_bytes(), n=2 ** 14, r=8, p=1,
                          maxmem=132 * 1024 * 1024, dklen=32)


def _subkey(master: bytes, info: bytes) -> bytes:
    AESGCM, HKDF, hashes = _crypto()
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=info).derive(master)


def _enc_blob(master: bytes, index: int, blob: bytes) -> bytes:
    AESGCM, _HKDF, _h = _crypto()
    key = _subkey(master, b"acom-archive/file/%d" % index)
    return AESGCM(key).encrypt(_ZERO_NONCE, blob, None)      # ct || tag(16)


def _dec_blob(master: bytes, index: int, enc: bytes) -> bytes:
    AESGCM, _HKDF, _h = _crypto()
    key = _subkey(master, b"acom-archive/file/%d" % index)
    return AESGCM(key).decrypt(_ZERO_NONCE, enc, None)


def _enc_manifest(master: bytes, raw: bytes) -> bytes:
    AESGCM, _HKDF, _h = _crypto()
    key = _subkey(master, b"acom-archive/manifest")
    return AESGCM(key).encrypt(_ZERO_NONCE, raw, None)


def _dec_manifest(master: bytes, enc: bytes) -> bytes:
    AESGCM, _HKDF, _h = _crypto()
    key = _subkey(master, b"acom-archive/manifest")
    return AESGCM(key).decrypt(_ZERO_NONCE, enc, None)


# ───────────────────────────────────────────────────────── compressão por arquivo
def _try_small(data: bytes) -> tuple[str, bytes]:
    """Arquivos pequenos: passa pela PORTA ÚNICA do dispositivo (`acom_auto`), que tipa o
    sinal e escolhe a rota — com `fidelity="exata"`.

    Por que isto importa AQUI, e muito: um backup de máquina real é majoritariamente feito de
    contêineres JÁ selados (jpg, mp4, zip, pdf, docx…). Antes, cada um deles queimava
    LZMA-PRESET_EXTREME + BZ2 + ZLIB para ganhar ~nada — a redundância já tinha sido extraída
    por quem os criou. A leitura reconhece o selo e faz UMA sondagem barata em vez de supor.

    `fidelity="exata"` é obrigatório e não é um detalhe: proíbe de forma DURA a rota com perda
    (g=√|L|). Backup que perde dado não é backup. Um .npy dentro da sua pasta continua saindo
    bit-exato daqui — a rota nativa da patente é para o dispositivo de arquivo único, não para
    a restauração de máquina.

    Degrada sem quebrar: se a porta única não estiver presente, cai no codec de sempre."""
    if _auto is not None:
        container, _rep = _auto.compress_auto(data, "f", "exata")
    else:                                            # pragma: no cover - fallback
        container, _rep = _codec.compress_file(data, "f")
    best_m, best = M_ACOM, container
    # se o contêiner do dispositivo não ajudou, ainda tentamos os básicos (nunca expandir)
    for m, fn in ((M_XZ, lambda d: lzma.compress(d, preset=6)),
                  (M_ZLIB, lambda d: zlib.compress(d, 6))):
        try:
            c = fn(data)
            if len(c) < len(best):
                best_m, best = m, c
        except Exception:
            pass
    if len(data) <= len(best):
        return M_STORE, data
    return best_m, best


def _compress_stream_to(src, dst, size_hint: int) -> tuple[str, int, int, str]:
    """Arquivos grandes (> cap): lzma em streaming (não carrega tudo na RAM).
    Retorna (método, sha256_hex, bytes_gravados, ...). Faz stored se lzma expandir."""
    h = hashlib.sha256()
    comp = lzma.LZMACompressor(preset=4)
    written = 0
    orig = 0
    # 1ª passada não é possível em stream; comprimimos direto e, se ficar maior, o método fica xz mesmo
    while True:
        chunk = src.read(BIG_FILE_STREAM_CHUNK)
        if not chunk:
            break
        orig += len(chunk)
        h.update(chunk)
        out = comp.compress(chunk)
        if out:
            dst.write(out); written += len(out)
    tail = comp.flush()
    if tail:
        dst.write(tail); written += len(tail)
    return M_XZ, h.hexdigest(), written, "stream"


# ───────────────────────────────────────────────────────── descompressão por arquivo
def _decompress(method: str, blob: bytes, orig_size: int, decomp_cap: Optional[int]) -> bytes:
    if method not in _DECODE_ALLOWED:               # recusa método forjado (ex.: bomba de bz2)
        raise ValueError(f"método não permitido: {method!r}")
    cap = decomp_cap if (decomp_cap and decomp_cap > 0) else None
    over = "estouro do teto de descompressão"
    if method == M_STORE:
        out = blob
        if cap is not None and len(out) > cap:
            raise ValueError(over)
    elif method == M_ACOM:
        out, _name, _meta = _codec.decompress_file(blob)   # acom_codec já limita a MAX_DECOMP_BYTES
        if cap is not None and len(out) > cap:
            raise ValueError(over)
    elif method == M_XZ:
        d = lzma.LZMADecompressor()
        out = d.decompress(blob, max_length=(cap if cap is not None else (1 << 62)))
        if cap is not None and not d.eof:            # não terminou dentro do teto ⇒ bomba
            raise ValueError(over)
    elif method == M_ZLIB:
        dobj = zlib.decompressobj()
        out = dobj.decompress(blob, cap if cap is not None else 0)
        if cap is not None and dobj.unconsumed_tail:  # sobrou entrada além do teto ⇒ bomba
            raise ValueError(over)
        out += dobj.flush()
        if cap is not None and len(out) > cap:
            raise ValueError(over)
    else:                                            # inalcançável (allowlist), mas fail-closed
        raise ValueError(f"método desconhecido: {method!r}")
    if orig_size is not None and len(out) != orig_size:
        raise ValueError("tamanho restaurado difere do original")
    return out


# ───────────────────────────────────────────────────────── segurança de caminho
def _sanitize_relpath(p: str) -> str:
    """Normaliza para POSIX e recusa absoluto / drive / '..' (anti zip-slip). Retorna o rel seguro."""
    if not isinstance(p, str) or not p.strip():
        raise ValueError("caminho vazio")
    q = p.replace("\\", "/")
    # remove drive do Windows (C:) e barra inicial
    if len(q) >= 2 and q[1] == ":":
        q = q[2:]
    q = q.lstrip("/")
    parts = [seg for seg in q.split("/") if seg not in ("", ".")]
    if not parts or any(seg == ".." for seg in parts):
        raise ValueError(f"caminho inseguro: {p!r}")
    return "/".join(parts)


def _target_under(dest: Path, relpath: str) -> Path:
    dest = dest.resolve()
    tgt = (dest / relpath).resolve()
    if dest != tgt and dest not in tgt.parents:
        raise ValueError(f"caminho escapa do destino: {relpath!r}")
    return tgt


# ═══════════════════════════════════════════════════════════════════════════════
#  PACK — escreve records em streaming, manifesto no fim, rodapé apontando
# ═══════════════════════════════════════════════════════════════════════════════
def pack_stream(entries: Iterable[tuple], out: io.BufferedIOBase, *, password: Optional[str] = None,
                meta: Optional[dict] = None, untrusted: bool = False,
                progress: Optional[Callable[[str, int, int], None]] = None) -> dict:
    """Empacota `entries` (iterável de (relpath, data_bytes) OU (relpath, open_callable, size))
    em `out` (binário seekável). Retorna o relatório. Se `password`, cifra (AES-GCM por arquivo)."""
    enc = password is not None
    master = None
    salt = b""
    if enc:
        if not crypto_available():
            raise RuntimeError("modo cifrado requer o pacote 'cryptography'.")
        salt = os.urandom(16)
        master = _derive_master(password, salt)

    header = {
        "v": FMT_VERSION, "tool": "acom_archive", "format": "ACOM_ARCHIVE",
        "beta": beta_provenance(), "enc": enc,
        "kdf": ({"algo": "scrypt", "salt": salt.hex(), "n": 2 ** 14, "r": 8, "p": 1,
                 "then": "hkdf-sha256/aes-256-gcm"} if enc else None),
        "meta": meta or {},
    }
    hb = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    out.write(MAGIC)
    out.write(struct.pack(">I", len(hb)))
    out.write(hb)

    entries_meta = []
    all_hashes = hashlib.sha256()
    total_in = 0
    total_stored = 0
    count = 0
    for item in entries:
        if count >= MAX_FILES:
            raise ValueError(f"arquivos demais (> {MAX_FILES})")
        relpath = _sanitize_relpath(item[0])
        off = out.tell()
        if callable(item[1]):                          # streaming de arquivo grande do disco
            size = item[2] if len(item) > 2 else None
            with item[1]() as src:
                if size is not None and size <= ACOM_FILE_CAP:
                    data = src.read()
                    method, blob = _pack_small_blob(data, master, count)
                    sha = hashlib.sha256(data).hexdigest(); osize = len(data)
                    out.write(blob); stored = len(blob)
                else:
                    if enc:
                        # grande + cifrado: comprime p/ buffer e cifra o todo (AES-GCM numa passada).
                        # Bufferiza o COMPRIMIDO — cap explícito e honesto (chunked-AEAD fica p/ v2).
                        buf = io.BytesIO()
                        method, sha, _w, _ = _compress_stream_to(src, buf, size or 0)
                        comp = buf.getvalue()
                        if len(comp) > CIFRADO_STREAM_CAP:
                            raise ValueError(f"arquivo grande demais p/ cifrar numa passada "
                                             f"(> {CIFRADO_STREAM_CAP // (1024*1024)} MB comprimido): {relpath}")
                        try:
                            blob = _enc_blob(master, count, comp)
                        except OverflowError:
                            raise ValueError(f"arquivo grande demais p/ o AES-GCM numa passada: {relpath}")
                        out.write(blob); stored = len(blob)
                        osize = None
                    else:
                        method, sha, stored, _ = _compress_stream_to(src, out, size or 0)
                        osize = None
        else:                                          # bytes em memória (web / arquivos pequenos)
            data = item[1]
            total_in += len(data)
            if untrusted and total_in > WEB_MAX_TOTAL_INPUT:
                raise ValueError("entrada agregada grande demais para a web (use o CLI para backups)")
            method, blob = _pack_small_blob(data, master, count)
            sha = hashlib.sha256(data).hexdigest(); osize = len(data)
            out.write(blob); stored = len(blob)

        total_stored += stored
        all_hashes.update(sha.encode())
        entries_meta.append({"path": relpath, "size": osize, "sha256": sha,
                             "method": method, "off": off, "len": stored, "i": count,
                             "enc": bool(enc)})
        if progress:
            progress(relpath, count + 1, stored)
        count += 1

    manifest = {"meta_chain": all_hashes.hexdigest(), "count": count,
                "total_size": total_in if total_in else None, "entries": entries_meta}
    mb = json.dumps(manifest, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if enc:
        mb = _enc_manifest(master, mb)
    man_off = out.tell()
    out.write(mb)
    out.write(MAGIC_END)
    out.write(struct.pack(">Q", man_off))
    out.write(struct.pack(">I", len(mb)))

    return {"format": "ACOM_ARCHIVE", "version": FMT_VERSION, "encrypted": enc,
            "files": count, "total_input_bytes": total_in or None,
            "container_bytes": out.tell(), "stored_bytes": total_stored,
            "meta_chain": manifest["meta_chain"], "beta": beta_provenance()}


def _pack_small_blob(data: bytes, master, index: int) -> tuple[str, bytes]:
    method, blob = _try_small(data)
    if master is not None:
        blob = _enc_blob(master, index, blob)
    return method, blob


def pack_files(files: list[tuple], *, password: Optional[str] = None, meta: Optional[dict] = None,
               untrusted: bool = True) -> tuple[bytes, dict]:
    """Web / memória: files = lista de (relpath, bytes) → contêiner .acom em bytes."""
    buf = io.BytesIO()
    report = pack_stream(iter(files), buf, password=password, meta=meta, untrusted=untrusted)
    return buf.getvalue(), report


def pack_paths(paths: list[Union[str, Path]], out_path: Union[str, Path], *,
               password: Optional[str] = None, base: Optional[Union[str, Path]] = None,
               progress: Optional[Callable[[str, int, int], None]] = None) -> dict:
    """CLI / disco: empacota arquivos e PASTAS INTEIRAS de `paths` em `out_path` (streaming, sem
    limite de navegador). `base` define a raiz dos caminhos relativos (default: pai comum)."""
    files = _walk_paths([Path(p) for p in paths], Path(base) if base else None)

    def _entries() -> Iterator[tuple]:
        for rel, full, size in files:
            yield (rel, (lambda f=full: open(f, "rb")), size)

    # o header vai em CLARO (mesmo no cifrado); NÃO expor os caminhos-raiz de origem quando cifrado.
    meta = {"source": "cli"} if password else {"source": "cli", "roots": [str(p) for p in paths]}
    with open(out_path, "wb") as out:
        return pack_stream(_entries(), out, password=password, meta=meta,
                           untrusted=False, progress=progress)


def _walk_paths(paths: list[Path], base: Optional[Path]) -> list[tuple]:
    """Resolve arquivos + pastas → [(relpath, fullpath, size)]. Ignora symlinks (segurança)."""
    resolved = [p.resolve() for p in paths]
    if base is None:
        # base = pai comum dos ALVOS (dir ou arquivo) → o nome da pasta de topo é preservado
        # (ex.: empacotar "src" gera "src/..."; restaurar dá dest/src/... — intuitivo p/ backup)
        parents = [p.parent for p in resolved]
        try:
            base = Path(os.path.commonpath([str(p) for p in parents]))
        except ValueError:
            base = parents[0]
    base = base.resolve()
    out = []
    for orig, p in zip(paths, resolved):
        if orig.is_symlink():            # checa o ORIGINAL — .resolve() já teria seguido o link
            continue
        if p.is_file():
            rel = _rel_or_name(p, base)
            out.append((rel, p, p.stat().st_size))
        elif p.is_dir():
            for root, dirs, fnames in os.walk(p):
                dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
                for fn in fnames:
                    full = Path(root) / fn
                    if full.is_symlink():
                        continue
                    try:
                        size = full.stat().st_size
                    except OSError:
                        continue
                    out.append((_rel_or_name(full, base), full, size))
    return out


def _rel_or_name(full: Path, base: Path) -> str:
    try:
        return full.relative_to(base).as_posix()
    except ValueError:
        return full.name


# ═══════════════════════════════════════════════════════════════════════════════
#  INSPECT / UNPACK / READ
# ═══════════════════════════════════════════════════════════════════════════════
def _read_footer(fp: io.BufferedIOBase) -> tuple[int, int]:
    fp.seek(0, io.SEEK_END)
    total = fp.tell()
    if total < len(MAGIC) + FOOTER_LEN:
        raise ValueError("não é um contêiner ACOM archive (curto demais)")
    fp.seek(-FOOTER_LEN, io.SEEK_END)
    foot = fp.read(FOOTER_LEN)
    if foot[:len(MAGIC_END)] != MAGIC_END:
        raise ValueError("rodapé ACOM archive ausente/corrompido")
    man_off = struct.unpack(">Q", foot[len(MAGIC_END):len(MAGIC_END) + 8])[0]
    man_len = struct.unpack(">I", foot[len(MAGIC_END) + 8:])[0]
    if man_off < len(MAGIC) or man_off + man_len > total - FOOTER_LEN:
        raise ValueError("offset do manifesto inválido")
    return man_off, man_len


def _read_header(fp: io.BufferedIOBase) -> dict:
    fp.seek(0)
    if fp.read(len(MAGIC)) != MAGIC:
        raise ValueError("MAGIC ACOM archive ausente")
    (hl,) = struct.unpack(">I", fp.read(4))
    if hl > 4 * 1024 * 1024:
        raise ValueError("header grande demais")
    return json.loads(fp.read(hl).decode("utf-8"))


def _open(container: Union[bytes, str, Path, io.BufferedIOBase]) -> tuple[io.BufferedIOBase, bool]:
    if isinstance(container, (bytes, bytearray)):
        return io.BytesIO(bytes(container)), True
    if isinstance(container, (str, Path)):
        return open(container, "rb"), True
    return container, False


def inspect(container, *, password: Optional[str] = None) -> dict:
    """Lê o header (sempre) e, se possível, o manifesto (lista de arquivos). Não extrai payload."""
    fp, close = _open(container)
    try:
        header = _read_header(fp)
        man_off, man_len = _read_footer(fp)
        fp.seek(man_off)
        mb = fp.read(man_len)
        manifest = None
        listing_locked = False
        if header.get("enc"):
            if password is not None:
                master = _derive_master(password, bytes.fromhex(header["kdf"]["salt"]))
                try:
                    manifest = json.loads(_dec_manifest(master, mb).decode("utf-8"))
                except Exception:
                    raise ValueError("senha incorreta ou contêiner corrompido")
            else:
                listing_locked = True
        else:
            manifest = json.loads(mb.decode("utf-8"))
        out = {"format": header.get("format"), "version": header.get("v"),
               "encrypted": bool(header.get("enc")), "beta": header.get("beta"),
               "meta": header.get("meta", {}), "listing_locked": listing_locked}
        if manifest is not None:
            out["files"] = manifest.get("count")
            out["meta_chain"] = manifest.get("meta_chain")
            out["entries"] = [{"path": e["path"], "size": e["size"], "method": e["method"],
                               "sha256": e["sha256"]} for e in manifest.get("entries", [])]
        return out
    finally:
        if close:
            fp.close()


def _load_manifest(fp: io.BufferedIOBase, header: dict, password: Optional[str]):
    man_off, man_len = _read_footer(fp)
    fp.seek(man_off)
    mb = fp.read(man_len)
    if header.get("enc"):
        if password is None:
            raise ValueError("contêiner cifrado — informe a senha")
        master = _derive_master(password, bytes.fromhex(header["kdf"]["salt"]))
        try:
            manifest = json.loads(_dec_manifest(master, mb).decode("utf-8"))
        except Exception:
            raise ValueError("senha incorreta ou contêiner corrompido")
        return manifest, master
    return json.loads(mb.decode("utf-8")), None


def _extract_one(fp: io.BufferedIOBase, entry: dict, master, decomp_cap: Optional[int]) -> bytes:
    fp.seek(entry["off"])
    blob = fp.read(entry["len"])
    if entry.get("enc"):
        if master is None:
            raise ValueError("record cifrado sem chave")
        blob = _dec_blob(master, entry["i"], blob)
    data = _decompress(entry["method"], blob, entry.get("size"), decomp_cap)
    got = hashlib.sha256(data).hexdigest()
    if got != entry["sha256"]:
        raise ValueError(f"SHA-256 não confere: {entry['path']}")
    return data


def unpack_stream(container, dest_dir: Union[str, Path], *, password: Optional[str] = None,
                  untrusted: bool = False,
                  progress: Optional[Callable[[str, int, int], None]] = None) -> dict:
    """Restaura a árvore em `dest_dir` (bit-exato, verificando cada SHA-256; anti zip-slip)."""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    fp, close = _open(container)
    try:
        header = _read_header(fp)
        manifest, master = _load_manifest(fp, header, password)
        entries = manifest.get("entries", [])
        remaining = WEB_MAX_DECOMP_TOTAL if untrusted else None
        restored = 0
        total_bytes = 0
        for k, e in enumerate(entries):
            if remaining is not None and remaining <= 0:
                raise ValueError("estouro do teto agregado de descompressão")
            data = _extract_one(fp, e, master, remaining)   # teto = orçamento RESTANTE
            if remaining is not None:
                remaining -= len(data)
            tgt = _target_under(dest, e["path"])            # _target_under contém (anti zip-slip)
            tgt.parent.mkdir(parents=True, exist_ok=True)
            with open(tgt, "wb") as w:
                w.write(data)
            restored += 1
            total_bytes += len(data)
            if progress:
                progress(e["path"], k + 1, len(data))
        return {"restored": restored, "bytes": total_bytes, "dest": str(dest.resolve()),
                "meta_chain": manifest.get("meta_chain"), "verified": True}
    finally:
        if close:
            fp.close()


def unpack_to_memory(container, *, password: Optional[str] = None, untrusted: bool = True) -> list[tuple]:
    """Web / memória: retorna [(relpath, bytes)] com cada SHA-256 verificado (bounded)."""
    return [(p, d) for p, d in open_and_extract(container, password=password, untrusted=untrusted)["files"] or []]


def open_and_extract(container, *, password: Optional[str] = None, untrusted: bool = True) -> dict:
    """UMA passada: header + manifesto (1 só derivação de chave) + extração verificada, com
    orçamento de descompressão por-record. Para o backend (evita derivar scrypt duas vezes)."""
    fp, close = _open(container)
    try:
        header = _read_header(fp)
        if header.get("enc") and password is None:
            return {"listing_locked": True, "encrypted": True, "files": None, "entries": []}
        manifest, master = _load_manifest(fp, header, password)
        remaining = WEB_MAX_DECOMP_TOTAL if untrusted else None
        files, entries = [], []
        for e in manifest.get("entries", []):
            if remaining is not None and remaining <= 0:
                raise ValueError("estouro do teto agregado de descompressão")
            data = _extract_one(fp, e, master, remaining)   # teto = orçamento RESTANTE
            if remaining is not None:
                remaining -= len(data)
            path = _sanitize_relpath(e["path"])             # sanitiza na SAÍDA (Nativa/def-in-depth)
            files.append((path, data))
            entries.append({"path": path, "size": e.get("size"), "method": e["method"], "sha256": e["sha256"]})
        return {"listing_locked": False, "encrypted": bool(header.get("enc")),
                "meta_chain": manifest.get("meta_chain"), "entries": entries,
                "files": files, "total_bytes": sum(len(d) for _p, d in files)}
    finally:
        if close:
            fp.close()


def read_file(container, path: str, *, password: Optional[str] = None) -> bytes:
    """Acesso aleatório: extrai UM arquivo pelo caminho (a base para a IALD Nativa ler .acom)."""
    want = _sanitize_relpath(path)
    fp, close = _open(container)
    try:
        header = _read_header(fp)
        manifest, master = _load_manifest(fp, header, password)
        for e in manifest.get("entries", []):
            if e["path"] == want:
                return _extract_one(fp, e, master, None)
        raise KeyError(f"arquivo não encontrado no contêiner: {path}")
    finally:
        if close:
            fp.close()


def read_acom(path: Union[str, Path], *, password: Optional[str] = None) -> dict:
    """Conveniência p/ a Nativa: abre um .acom e devolve {header/manifest + função de leitura}."""
    info = inspect(path, password=password)
    return {"info": info, "read": (lambda p, _pw=password, _pt=str(path): read_file(_pt, p, password=_pw))}


# ═══════════════════════════════════════════════════════════════════════════════
def selftest() -> dict:
    """Round-trip em memória (plano e, se disponível, cifrado) — prova bit-exata + integridade."""
    import random
    rnd = random.Random(1)
    files = [
        ("docs/a.txt", b"haja luz " * 5000),
        ("docs/sub/b.bin", bytes(rnd.getrandbits(8) for _ in range(40000))),
        ("c.json", json.dumps({"beta": beta_provenance()}).encode()),
        ("vazio.dat", b""),
    ]
    res = {"beta": beta_provenance(), "plano": {}, "cifrado": {}}
    # PLANO
    cont, rep = pack_files([(p, d) for p, d in files])
    got = dict(unpack_to_memory(cont))
    ok = all(got.get(p) == d for p, d in files)
    res["plano"] = {"files": rep["files"], "container_bytes": rep["container_bytes"],
                    "bit_exact": ok, "meta_chain": rep["meta_chain"][:16]}
    # zip-slip deve falhar
    try:
        pack_files([("../evil.txt", b"x")]); res["zip_slip_blocked"] = False
    except ValueError:
        res["zip_slip_blocked"] = True
    # CIFRADO
    if crypto_available():
        pw = "senha-de-teste-123"
        cont2, rep2 = pack_files([(p, d) for p, d in files], password=pw)
        # sem senha: manifesto trancado
        locked = inspect(cont2).get("listing_locked", False)
        got2 = dict(unpack_to_memory(cont2, password=pw))
        ok2 = all(got2.get(p) == d for p, d in files)
        wrong = False
        try:
            unpack_to_memory(cont2, password="senha-errada-999")
        except Exception:
            wrong = True
        res["cifrado"] = {"files": rep2["files"], "listing_locked_sem_senha": locked,
                          "bit_exact": ok2, "senha_errada_rejeitada": wrong}
    else:
        res["cifrado"] = {"skipped": "cryptography indisponível"}
    res["pass"] = bool(res["plano"]["bit_exact"] and res["zip_slip_blocked"]
                       and (res["cifrado"].get("bit_exact", True)))
    return res


if __name__ == "__main__":
    print(json.dumps(selftest(), ensure_ascii=False, indent=1))
