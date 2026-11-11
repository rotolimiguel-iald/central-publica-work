# -*- coding: utf-8 -*-
"""
ACOM — DISPOSITIVO (o dispositivo funcionando: a interface de compressão)
=========================================================================
Patente BR102025026951-1 — "Método e Sistema de Compressão Ontológica de Memória
baseado em Transformação Luminodinâmica" (TGL).

Este é o **dispositivo dentro do dispositivo**: o ACOM efetivamente *funcionando*
como um compressor de arquivos. Você entrega bytes, ele devolve um contêiner `.acom`;
você entrega o `.acom`, ele devolve os bytes originais — bit a bit idênticos.

DOIS MODOS — e a honestidade entre eles é a régua (o número corrige a frase):

  (1) MODO ARQUIVO  — universal, **SEM PERDAS** (lossless).
      Funciona em QUALQUER arquivo (pdf, docx, zip, imagem, texto, binário).
      Round-trip bit-exato, garantido por SHA-256 no cabeçalho.
      A redução de bytes de arquivos arbitrários é feita por um **backend de
      entropia real** (LZMA, da biblioteca padrão). A camada ACOM contribui com:
        - classificação de REGIME ontológico (TETELESTAI/CONDENSED/VACUUM/VAPOR),
          usando os MESMOS limiares TGL do algoritmo (β, e/2, 3e/2), medidos sobre
          a entropia de Shannon do fluxo de bytes;
        - um estágio ontológico REVERSÍVEL de paleta para o regime TETELESTAI
          (dados de baixa entropia: poucos valores distintos) que pode reduzir
          antes do backend;
        - proveniência TGL (β, θ_Miguel) e integridade (SHA-256).
      Dados incompressíveis são guardados crus (backend="stored"); nesse caso o contêiner
      fica ~algumas centenas de bytes MAIOR que o original (overhead do cabeçalho de
      proveniência) e o relatório informa isso honestamente (ratio < 1, sem compressão).

  (2) MODO TENSOR  — o algoritmo **nativo da patente** (g=√|L|), **COM PERDA** controlada.
      É a invenção de fato: extrai a componente gravitacional g=√|L| e a fase s=sign(L),
      quantiza e reconstrói por L = s·g². Aplica-se a arrays de ponto flutuante
      (embeddings, KV-cache, sinais). Atinge 3:1–10:1 com PSNR alto / correlação>0,999
      (reivindicação 18). É COM PERDA por construção — reportamos PSNR e correlação
      honestamente. Requer numpy (roda quando disponível).

β NUNCA é literal: BETA_TGL = ALPHA_FINE_CODATA_2018 · √e, calculado em runtime.
"""
from __future__ import annotations

import bz2
import hashlib
import io
import json
import lzma
import math
import struct
import zlib
from dataclasses import dataclass, asdict
from typing import Any

# ─── CONSTANTES TGL (β/θ derivados em runtime — jamais hardcoded) ───────────────
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3          # α (CODATA 2018) — [INPUT]
SQRT_E = math.sqrt(math.e)                         # √e
BETA_TGL = ALPHA_FINE_CODATA_2018 * SQRT_E         # β = α·√e  ≈ 0.012031... [DERIVED]
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))      # θ_M = arcsin(√β)        [DERIVED]
THETA_MIGUEL_DEG = math.degrees(THETA_MIGUEL)

# Limiares de regime — os mesmos do ACOM (v19), em nats:
TTS_THRESH = BETA_TGL          # < β        → TETELESTAI (permanência: baixíssima entropia)
COND_THRESH = 0.5 * math.e     # < e/2      → CONDENSED
VAP_THRESH = 1.5 * math.e      # < 3e/2     → VACUUM ; senão VAPOR

MAGIC = b"ACOM1\x00"
CODEC_VERSION = "1.0"
PATENT_ID = "BR102025026951-1"

# limites de segurança (o dispositivo roda num backend exposto por túnel)
MAX_INPUT_BYTES = 64 * 1024 * 1024          # 64 MB de entrada
MAX_DECOMP_BYTES = 512 * 1024 * 1024        # teto anti-bomba de descompressão
MAX_HEADER_BYTES = 1 * 1024 * 1024          # cabeçalho JSON sanidade


def beta_provenance() -> dict:
    """β/θ calculados agora (para auditoria: nada literal)."""
    return {
        "alpha_fine_codata_2018": ALPHA_FINE_CODATA_2018,
        "sqrt_e": SQRT_E,
        "beta_tgl": BETA_TGL,
        "theta_miguel_deg": THETA_MIGUEL_DEG,
        "formula": "beta = alpha_fine_codata_2018 * sqrt(e)",
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  REGIME ONTOLÓGICO — classificação por entropia de Shannon (nats)
# ═══════════════════════════════════════════════════════════════════════════════

def _byte_histogram(data: bytes) -> list[int]:
    h = [0] * 256
    for b in data:
        h[b] += 1
    return h


def shannon_entropy_nats(data: bytes, hist: list[int] | None = None) -> float:
    """Entropia de Shannon do fluxo de bytes, em NATS (base e — a base do TGL)."""
    n = len(data)
    if n == 0:
        return 0.0
    hist = hist if hist is not None else _byte_histogram(data)
    s = 0.0
    for c in hist:
        if c:
            p = c / n
            s -= p * math.log(p)          # log natural → nats
    return s


def classify_regime(entropy_nats: float) -> str:
    if entropy_nats < TTS_THRESH:
        return "TETELESTAI"
    if entropy_nats < COND_THRESH:
        return "CONDENSED"
    if entropy_nats < VAP_THRESH:
        return "VACUUM"
    return "VAPOR"


# ═══════════════════════════════════════════════════════════════════════════════
#  ESTÁGIO ONTOLÓGICO REVERSÍVEL — paleta (só ajuda no regime de baixa entropia)
# ═══════════════════════════════════════════════════════════════════════════════
# Para dados com poucos valores distintos de byte (TETELESTAI/CONDENSED), reindexar
# para uma paleta compacta pode reduzir o material antes do backend de entropia.
# É REVERSÍVEL exatamente. Só é aplicado quando reduz o nº de símbolos de forma útil.

def _palette_encode(data: bytes) -> tuple[bytes, dict] | None:
    uniq = sorted(set(data))
    k = len(uniq)
    if k == 0 or k > 16:
        return None                        # só vale para pouquíssimos símbolos
    # mapeia cada byte para um nibble (4 bits) — 2 símbolos por byte
    idx = {v: i for i, v in enumerate(uniq)}
    packed = bytearray((len(data) + 1) // 2)
    for i, b in enumerate(data):
        v = idx[b]
        if i & 1:
            packed[i >> 1] |= v
        else:
            packed[i >> 1] |= (v << 4)
    meta = {"palette": uniq, "n": len(data)}
    return bytes(packed), meta


def _palette_decode(packed: bytes, meta: dict) -> bytes:
    palette = meta.get("palette")
    n = meta.get("n")
    # ANTI-BOMBA: nada de alocar bytearray(n) com n do atacante sem validar (n vem do header).
    if not isinstance(n, int) or n < 0 or n > MAX_DECOMP_BYTES:
        raise ValueError("paleta: n inválido ou acima do teto")
    if n > 2 * len(packed):                 # packed tem ceil(n/2) bytes ⇒ n ≤ 2·len(packed)
        raise ValueError("paleta: n incompatível com o payload")
    if not isinstance(palette, list) or not (1 <= len(palette) <= 16):
        raise ValueError("paleta: tamanho inválido")
    if any((not isinstance(v, int) or not (0 <= v <= 255)) for v in palette):
        raise ValueError("paleta: valores inválidos")
    out = bytearray(n)
    for i in range(n):
        byte = packed[i >> 1]
        v = (byte >> 4) if not (i & 1) else (byte & 0x0F)
        if v >= len(palette):
            raise ValueError("paleta: índice fora do intervalo")
        out[i] = palette[v]
    return bytes(out)


# ═══════════════════════════════════════════════════════════════════════════════
#  BACKEND DE ENTROPIA — real, da biblioteca padrão
# ═══════════════════════════════════════════════════════════════════════════════

def _backend_compress(name: str, data: bytes) -> bytes:
    if name == "lzma":
        return lzma.compress(data, preset=9 | lzma.PRESET_EXTREME)
    if name == "bz2":
        return bz2.compress(data, 9)
    if name == "zlib":
        return zlib.compress(data, 9)
    if name == "stored":
        return data
    raise ValueError(f"backend desconhecido: {name}")


def _backend_decompress(name: str, data: bytes) -> bytes:
    if name == "lzma":
        dec = lzma.LZMADecompressor()
        out = dec.decompress(data, max_length=MAX_DECOMP_BYTES)
        if not dec.eof:
            raise ValueError("descompressão excedeu o teto (possível bomba)")
        return out
    if name == "bz2":
        dec = bz2.BZ2Decompressor()
        out = dec.decompress(data, max_length=MAX_DECOMP_BYTES)
        if not dec.eof:
            raise ValueError("descompressão excedeu o teto (possível bomba)")
        return out
    if name == "zlib":
        dobj = zlib.decompressobj()
        out = dobj.decompress(data, MAX_DECOMP_BYTES)
        if dobj.unconsumed_tail:
            raise ValueError("descompressão excedeu o teto (possível bomba)")
        return out
    if name == "stored":
        return data
    raise ValueError(f"backend desconhecido: {name}")


# ═══════════════════════════════════════════════════════════════════════════════
#  RELATÓRIO
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CompressReport:
    mode: str
    orig_name: str
    orig_size: int
    compressed_size: int
    ratio: float                 # orig/compressed (quanto maior, melhor)
    saved_pct: float
    backend: str
    regime: str
    entropy_nats: float
    entropy_bits_per_byte: float
    ontological_stage: str
    orig_sha256: str
    beta_tgl: float
    theta_miguel_deg: float
    lossless: bool
    note: str
    # campos do modo tensor (opcionais)
    psnr_db: float | None = None
    correlation: float | None = None
    # campos da PORTA ÚNICA (acom_auto) — a decisão que o SINAL tomou, não o operador.
    # Opcionais: quando o codec é chamado direto (sem o auto), saem do relatório.
    signal_type: str | None = None       # o que a leitura tipou (cadeia de sinal)
    signal_evidence: str | None = None   # a evidência que sustenta a tipagem
    route: str | None = None             # a rota efetivamente tomada
    decision_why: str | None = None      # a lei: por que esta rota, dado (sinal, regime)
    decided_by: str | None = None        # o que desempatou (portão de fidelidade medido, etc.)
    alternatives: list | None = None     # as rotas MEDIDAS e descartadas (auditoria)
    auto_version: str | None = None
    seal_probe: dict | None = None       # a sondagem que conferiu (ou rejeitou) o selo do contêiner

    def as_dict(self) -> dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


# ═══════════════════════════════════════════════════════════════════════════════
#  MODO ARQUIVO — compressão universal SEM PERDAS
# ═══════════════════════════════════════════════════════════════════════════════

def compress_file(data: bytes, name: str = "arquivo",
                  backends: tuple[str, ...] | None = None) -> tuple[bytes, CompressReport]:
    """Comprime QUALQUER arquivo, sem perdas, para um contêiner .acom. Bit-exato.

    `backends`: quais backends de entropia vale a pena MEDIR (o `acom_auto` os escolhe pelo
    tipo de sinal + regime, para não queimar LZMA-extremo onde ele não teria ganho).
    None = os três de sempre. "stored" cru continua sempre concorrendo — nunca expande."""
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError(f"arquivo grande demais (> {MAX_INPUT_BYTES // (1024*1024)} MB)")

    name = _safe_name(name)
    orig_size = len(data)
    sha = hashlib.sha256(data).hexdigest()
    hist = _byte_histogram(data)
    ent = shannon_entropy_nats(data, hist)
    regime = classify_regime(ent)

    # estágio ontológico reversível (paleta) — só no regime de baixíssima entropia
    onto = "identity"
    staged = data
    pal_meta: dict | None = None
    if regime in ("TETELESTAI", "CONDENSED"):
        pe = _palette_encode(data)
        if pe is not None:
            staged, pal_meta = pe
            onto = "palette"

    # escolhe o menor entre backends reais + "stored" (nunca expande)
    bk_list = tuple(backends) if backends else ("lzma", "bz2", "zlib")
    for bk in bk_list:
        if bk not in ("lzma", "bz2", "zlib"):
            raise ValueError(f"backend inválido: {bk!r}")
    candidates: list[tuple[str, bytes]] = []
    for bk in bk_list:
        try:
            candidates.append((bk, _backend_compress(bk, staged)))
        except Exception:
            pass
    # "stored" mede sobre o dado ORIGINAL (paleta+stored não faria sentido)
    candidates.append(("stored_raw", data))
    best_name, best_payload = min(candidates, key=lambda c: len(c[1]))

    if best_name == "stored_raw":
        onto, best_backend, payload = "identity", "stored", data
        pal_meta = None
    else:
        best_backend, payload = best_name, best_payload

    header = {
        "codec": "ACOM-LOSSLESS",
        "version": CODEC_VERSION,
        "patent": PATENT_ID,
        "mode": "file",
        "orig_name": name,
        "orig_size": orig_size,
        "orig_sha256": sha,
        "backend": best_backend,
        "regime": regime,
        "entropy_nats": ent,
        "ontological_stage": onto,
        "beta": beta_provenance(),
    }
    if pal_meta is not None:
        header["palette_meta"] = pal_meta

    container = _pack(header, payload)
    comp_size = len(container)
    ratio = orig_size / comp_size if comp_size else 1.0
    report = CompressReport(
        mode="file",
        orig_name=name, orig_size=orig_size, compressed_size=comp_size,
        ratio=ratio, saved_pct=(1 - comp_size / orig_size) * 100 if orig_size else 0.0,
        backend=best_backend, regime=regime, entropy_nats=ent,
        entropy_bits_per_byte=ent / math.log(2),
        ontological_stage=onto, orig_sha256=sha,
        beta_tgl=BETA_TGL, theta_miguel_deg=THETA_MIGUEL_DEG, lossless=True,
        note=(f"Sem perdas (bit-exato, verificado por SHA-256). Dados INCOMPRESSÍVEIS "
              f"(regime {regime}): guardados crus — o contêiner acrescenta ~{comp_size - orig_size} B "
              f"de cabeçalho de proveniência (ratio < 1, sem compressão)."
              if best_backend == "stored" else
              f"Sem perdas (bit-exato, verificado por SHA-256). Redução de entropia pelo "
              f"backend {best_backend.upper()}; camada ACOM: regime {regime} + estágio {onto}."),
    )
    return container, report


def decompress_any(container: bytes) -> tuple[bytes, str, dict]:
    """Despacha pelo codec do contêiner: ACOM-LOSSLESS (sem perdas) ou ACOM-TENSOR (com perda)."""
    header, _ = _unpack(container)                 # só espia o cabeçalho
    codec = header.get("codec")
    if codec == "ACOM-LOSSLESS":
        return decompress_file(container)
    if codec == "ACOM-TENSOR":
        if not tensor_available():
            raise ValueError("contêiner tensor requer numpy (indisponível neste backend)")
        return decompress_tensor(container)
    raise ValueError(f"contêiner de codec desconhecido: {codec!r}")


def decompress_file(container: bytes) -> tuple[bytes, str, dict]:
    """Restaura os bytes originais de um contêiner .acom (sem perdas). Verifica SHA-256."""
    header, payload = _unpack(container)
    if header.get("codec") != "ACOM-LOSSLESS":
        raise ValueError("contêiner não é ACOM-LOSSLESS")
    # valida o tamanho declarado ANTES de qualquer alocação (anti-bomba)
    orig_size = header.get("orig_size")
    if not isinstance(orig_size, int) or orig_size < 0 or orig_size > MAX_DECOMP_BYTES:
        raise ValueError("tamanho declarado inválido ou acima do teto")
    backend = header["backend"]
    staged = _backend_decompress(backend, payload)      # já limitado a MAX_DECOMP_BYTES
    onto = header.get("ontological_stage", "identity")
    if onto == "palette":
        pm = header.get("palette_meta") or {}
        if pm.get("n") != orig_size:
            raise ValueError("paleta: n inconsistente com orig_size")
        data = _palette_decode(staged, pm)              # valida n/paleta internamente
    else:
        data = staged
    # integridade — a régua: bit-exato ou erro honesto
    sha = hashlib.sha256(data).hexdigest()
    if sha != header.get("orig_sha256"):
        raise ValueError("FALHA DE INTEGRIDADE: SHA-256 não confere (contêiner corrompido)")
    if len(data) != orig_size:
        raise ValueError("FALHA DE INTEGRIDADE: tamanho não confere")
    return data, _safe_name(header.get("orig_name", "arquivo")), {
        "verified": True, "orig_sha256": sha, "regime": header.get("regime"),
        "backend": backend, "beta": header.get("beta"), "lossy": False,
    }


# ─── contêiner .acom ────────────────────────────────────────────────────────────

def _pack(header: dict, payload: bytes) -> bytes:
    hb = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(hb) > MAX_HEADER_BYTES:
        raise ValueError("cabeçalho grande demais")
    return MAGIC + struct.pack(">I", len(hb)) + hb + payload


def _unpack(container: bytes) -> tuple[dict, bytes]:
    if len(container) < len(MAGIC) + 4 or container[:len(MAGIC)] != MAGIC:
        raise ValueError("arquivo .acom inválido (magic ausente)")
    off = len(MAGIC)
    (hlen,) = struct.unpack(">I", container[off:off + 4])
    off += 4
    if hlen > MAX_HEADER_BYTES or off + hlen > len(container):
        raise ValueError("arquivo .acom inválido (cabeçalho)")
    header = json.loads(container[off:off + hlen].decode("utf-8"))
    payload = container[off + hlen:]
    return header, payload


def _safe_name(name: str) -> str:
    """Só o basename, sem separadores de caminho (defesa contra path traversal no download)."""
    name = (name or "arquivo").replace("\\", "/").split("/")[-1].strip()
    name = "".join(c for c in name if c.isprintable() and c not in '<>:"|?*')
    return name[:200] or "arquivo"


# ═══════════════════════════════════════════════════════════════════════════════
#  MODO TENSOR — o algoritmo NATIVO da patente (g=√|L|), COM PERDA. Requer numpy.
# ═══════════════════════════════════════════════════════════════════════════════

def tensor_available() -> bool:
    import importlib.util
    return importlib.util.find_spec("numpy") is not None


def compress_tensor(npy_bytes: bytes, name: str = "tensor.npy") -> tuple[bytes, CompressReport]:
    """Reflexão holográfica ACOM sobre um array .npy: g=√|L|, s=sign(L), L=s·g².
    COM PERDA (reporta PSNR e correlação). O domínio nativo e patenteado do ACOM."""
    import numpy as np  # lazy

    if len(npy_bytes) > MAX_INPUT_BYTES:
        raise ValueError(f"arquivo grande demais (> {MAX_INPUT_BYTES // (1024*1024)} MB)")
    name = _safe_name(name)
    arr = np.load(io.BytesIO(npy_bytes), allow_pickle=False)
    orig = np.asarray(arr).astype(np.float64)
    orig_size = len(npy_bytes)
    shape, dtype = list(orig.shape), str(arr.dtype)

    flat = orig.flatten()
    # transformada luminodinâmica: componente gravitacional g=√|L| e fase s=sign(L)
    g = np.sqrt(np.abs(flat))
    s = np.sign(flat).astype(np.int8)
    # quantização configurável do gravitacional (reivindicação 6: 10 bits preferencial)
    bits = 10
    gmax = float(g.max()) if g.size and g.max() > 0 else 1.0
    levels = (1 << bits) - 1
    gq = np.clip(np.round(g / gmax * levels), 0, levels).astype("<u2")  # little-endian fixo

    # empacota g quantizado (uint16) + sinais (bit-packed) + header, e comprime com backend real
    sign_bits = np.packbits((s > 0).astype(np.uint8))
    thead = {"shape": shape, "dtype": dtype, "bits": bits, "gmax": gmax, "n": int(flat.size)}
    thb = json.dumps(thead).encode("utf-8")
    raw = struct.pack(">I", len(thb)) + thb + gq.tobytes() + struct.pack(">I", len(sign_bits)) + sign_bits.tobytes()
    payload = _backend_compress("lzma", raw)

    # reconstrução para medir a perda honestamente
    g_rec = gq.astype(np.float64) / levels * gmax
    rec = (g_rec ** 2) * s.astype(np.float64)
    psnr, corr = _tensor_metrics(flat, rec)

    header = {
        "codec": "ACOM-TENSOR", "version": CODEC_VERSION, "patent": PATENT_ID,
        "mode": "tensor", "orig_name": name, "orig_size": orig_size,
        "orig_sha256": hashlib.sha256(npy_bytes).hexdigest(),
        "backend": "lzma", "tensor": thead, "beta": beta_provenance(),
    }
    container = _pack(header, payload)
    comp_size = len(container)
    ratio = orig_size / comp_size if comp_size else 1.0
    ent = shannon_entropy_nats(npy_bytes)
    report = CompressReport(
        mode="tensor", orig_name=name, orig_size=orig_size, compressed_size=comp_size,
        ratio=ratio, saved_pct=(1 - comp_size / orig_size) * 100 if orig_size else 0.0,
        backend="lzma", regime=classify_regime(ent), entropy_nats=ent,
        entropy_bits_per_byte=ent / math.log(2), ontological_stage="graviton_reflect_q%d" % bits,
        orig_sha256=header["orig_sha256"], beta_tgl=BETA_TGL, theta_miguel_deg=THETA_MIGUEL_DEG,
        lossless=False,
        note=("COM PERDA (domínio nativo da patente). Transformada g=√|L|, fase s=sign(L), "
              "quantização de %d bits, reconstrução L=s·g². Fidelidade medida abaixo." % bits),
        psnr_db=(None if math.isinf(psnr) else psnr), correlation=corr,
    )
    return container, report


def decompress_tensor(container: bytes) -> tuple[bytes, str, dict]:
    """Reconstrói o array .npy de um contêiner ACOM-TENSOR: L = s·g² (COM PERDA — a
    reconstrução não é idêntica bit a bit; é o comportamento honesto de um codec lossy)."""
    import numpy as np  # lazy

    header, payload = _unpack(container)
    if header.get("codec") != "ACOM-TENSOR":
        raise ValueError("contêiner não é ACOM-TENSOR")
    thead = header.get("tensor") or {}
    n = thead.get("n")
    if not isinstance(n, int) or n < 0 or n > MAX_DECOMP_BYTES:
        raise ValueError("tensor: n inválido ou acima do teto")
    raw = _backend_decompress(header["backend"], payload)   # limitado a MAX_DECOMP_BYTES
    off = 0
    (tlen,) = struct.unpack(">I", raw[off:off + 4]); off += 4
    off += tlen                                             # o thead interno é redundante com o header
    need = 2 * n
    if off + need + 4 > len(raw):
        raise ValueError("tensor: payload truncado")
    gq = np.frombuffer(raw[off:off + need], dtype="<u2").astype(np.float64); off += need
    (slen,) = struct.unpack(">I", raw[off:off + 4]); off += 4
    if off + slen > len(raw):
        raise ValueError("tensor: bits de sinal truncados")
    sign_bits = np.frombuffer(raw[off:off + slen], dtype=np.uint8)

    bits = int(thead["bits"]); gmax = float(thead["gmax"])
    shape = tuple(thead["shape"]); dtype = np.dtype(thead["dtype"])
    levels = (1 << bits) - 1
    s = np.where(np.unpackbits(sign_bits)[:n] > 0, 1.0, -1.0)
    g_rec = gq / levels * gmax
    L = (g_rec ** 2) * s
    arr = L.reshape(shape).astype(dtype)
    buf = io.BytesIO(); np.save(buf, arr); npy = buf.getvalue()
    return npy, _safe_name(header.get("orig_name", "tensor.npy")), {
        "verified": False, "lossy": True, "regime": None,
        "note": "Reconstrução COM PERDA (L=s·g²) — não idêntica bit a bit ao original (codec lossy).",
        "beta": header.get("beta"),
    }


def _tensor_metrics(orig, rec):
    import numpy as np
    o = np.asarray(orig, dtype=np.float64).flatten()
    r = np.asarray(rec, dtype=np.float64).flatten()
    n = min(len(o), len(r)); o, r = o[:n], r[:n]
    mse = float(np.mean((o - r) ** 2)); sig = float(np.mean(o ** 2))
    psnr = float("inf") if mse < 1e-20 else (0.0 if sig < 1e-20 else float(10 * np.log10(sig / mse)))
    if o.std() < 1e-12 or r.std() < 1e-12:
        corr = 1.0 if np.allclose(o, r, rtol=1e-4, atol=1e-8) else 0.0
    else:
        c = float(np.corrcoef(o, r)[0, 1]); corr = c if math.isfinite(c) else 0.0
    return psnr, corr


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTODEMONSTRAÇÃO (forma = conteúdo): roda standalone e prova o round-trip
# ═══════════════════════════════════════════════════════════════════════════════

def _selftest() -> dict:
    import os
    results = {"beta": beta_provenance(), "cases": []}
    samples = {
        "texto_repetitivo": ("Haja luz. " * 5000).encode("utf-8"),
        "binario_aleatorio": os.urandom(200_000),
        "baixa_entropia": bytes([0, 1, 0, 1, 2, 0] * 40_000),
        "vazio_quase": b"A" * 100_000,
    }
    for nm, data in samples.items():
        cont, rep = compress_file(data, nm)
        back, oname, meta = decompress_file(cont)
        ok = back == data and meta["verified"]
        results["cases"].append({
            "name": nm, "orig": rep.orig_size, "comp": rep.compressed_size,
            "ratio": round(rep.ratio, 3), "regime": rep.regime, "backend": rep.backend,
            "stage": rep.ontological_stage, "lossless_roundtrip": ok,
        })
    results["all_lossless"] = all(c["lossless_roundtrip"] for c in results["cases"])
    return results


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # console Windows (cp1252) → utf-8
    except Exception:
        pass
    r = _selftest()
    print(json.dumps(r, indent=2, ensure_ascii=False))
    print("\nβ = α·√e =", BETA_TGL, "| θ_Miguel =", THETA_MIGUEL_DEG, "°")
    print("ROUND-TRIP SEM PERDAS:", "OK ✓" if r["all_lossless"] else "FALHOU ✗")
    sys.exit(0 if r["all_lossless"] else 1)
