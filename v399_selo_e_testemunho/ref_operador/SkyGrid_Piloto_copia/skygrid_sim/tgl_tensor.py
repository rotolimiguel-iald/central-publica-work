#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tgl_tensor — BLOCO 2. Tensor compression (patent BR 10 2026 003441-0).

Two modes, ported from tgl_tensor_v4.py (v4.3, numpy path) [REAL]:

  DIRECT  : TGL quantization of the root. L -> (s, g=sqrt|L|) ; g min-max
            normalized and quantized to `bits`; signs packed 1 bit each.
            Reconstruction L' = s * g^2.
  SPECTRAL: per-matrix SVD; keep the smallest rank k whose cumulated spectral
            energy reaches the retention threshold; factors then compressed
            with DIRECT.

TGL grounding (runtime, never literal):
  * VERB FLOOR [DER-reading]: default spectral retention = 1 - beta().
    beta is the paid cost of inscription (the dephasing fraction); the pilot
    retains 1-beta of the spectral energy and lets the beta fraction go.
    Fully configurable; the default is the TGL-derived one.
  * TETELESTAI flag: relative dispersion of g below beta() marks a tensor
    whose root is already quiet (variance paid). The legacy carried this
    threshold as a truncated numeric literal; here it comes from tgl_core.beta().
"""

import struct
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np

from . import tgl_core
from .acom import reflect as acom_reflect

EPSILON = 1e-10
MAGIC = b"TGS1"


# --------------------------------------------------------------------- bitpacker
def pack_bits(values: np.ndarray, bits: int) -> bytes:
    """Vectorized N-bit packer (port of BitPackerNumPy v4.2)."""
    values = np.clip(np.asarray(values).ravel().astype(np.uint64), 0, (1 << bits) - 1)
    if bits == 8:
        return values.astype(np.uint8).tobytes()
    if bits == 16:
        return values.astype(np.uint16).tobytes()
    n = len(values)
    all_bits = ((values[:, None] >> np.arange(bits, dtype=np.uint64)) & 1).astype(np.uint8)
    stream = all_bits.ravel()
    pad = (8 - len(stream) % 8) % 8
    if pad:
        stream = np.concatenate([stream, np.zeros(pad, dtype=np.uint8)])
    powers = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
    out = (stream.reshape(-1, 8) * powers).sum(axis=1).astype(np.uint8)
    return out[: (n * bits + 7) // 8].tobytes()


def unpack_bits(data: bytes, bits: int, count: int) -> np.ndarray:
    if bits == 8:
        return np.frombuffer(data[:count], dtype=np.uint8).astype(np.uint32)
    if bits == 16:
        return np.frombuffer(data[: count * 2], dtype=np.uint16).astype(np.uint32)
    b = np.frombuffer(data, dtype=np.uint8)
    powers8 = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)
    stream = ((b[:, None] & powers8) > 0).astype(np.uint8).ravel()[: count * bits]
    vals = (stream.reshape(count, bits).astype(np.uint64)
            * (1 << np.arange(bits, dtype=np.uint64))).sum(axis=1)
    return vals.astype(np.uint32)


# --------------------------------------------------------------------- container
@dataclass
class CompressedTensor:
    packed: bytes
    mode: str
    shape: tuple
    bits: int
    variance: float
    tetelestai: bool
    ranks: Optional[Tuple[int, ...]] = None

    @property
    def original_bytes(self) -> int:
        return int(np.prod(self.shape)) * 8

    @property
    def compression_ratio(self) -> float:
        return self.original_bytes / max(len(self.packed), 1)


# --------------------------------------------------------------------- engine
class TGLTensor:
    def __init__(self, bits: int = 10, energy_threshold: Optional[float] = None):
        """energy_threshold=None -> VERB FLOOR default 1 - beta() (runtime)."""
        self.bits = bits
        self.levels = 1 << bits
        self.beta = tgl_core.beta()
        self.energy_threshold = (1.0 - self.beta) if energy_threshold is None else energy_threshold

    # ---- DIRECT --------------------------------------------------------------
    def compress_direct(self, arr: np.ndarray) -> CompressedTensor:
        arr = np.asarray(arr, dtype=np.float64)
        flat = arr.ravel()
        g, s = acom_reflect(flat)                      # root of the trilho (BLOCO 1a)
        s_bit = (s > 0).astype(np.uint8)
        g_min, g_max = float(g.min()), float(g.max())
        rng = g_max - g_min
        g_norm = (g - g_min) / rng if rng > EPSILON else np.zeros_like(g)
        g_q = np.round(g_norm * (self.levels - 1)).astype(np.uint32)

        g_nz = g[g > EPSILON]
        variance = float(np.std(g_nz) / (np.mean(g_nz) + EPSILON)) if g_nz.size else 0.0

        header = MAGIC + struct.pack("<BB", self.bits, arr.ndim)
        for d in arr.shape:
            header += struct.pack("<I", d)
        header += struct.pack("<ddQ", g_min, g_max, flat.size)
        g_packed = pack_bits(g_q, self.bits)
        header += struct.pack("<I", len(g_packed))
        payload = header + g_packed + np.packbits(s_bit).tobytes()

        return CompressedTensor(payload, "direct", tuple(arr.shape), self.bits,
                                variance, bool(variance < self.beta))

    def decompress_direct(self, comp: CompressedTensor) -> np.ndarray:
        data = comp.packed
        if data[:4] != MAGIC:
            raise ValueError("Magic invalido")
        bits, ndim = struct.unpack("<BB", data[4:6])
        off = 6
        shape = []
        for _ in range(ndim):
            shape.append(struct.unpack("<I", data[off:off + 4])[0]); off += 4
        g_min, g_max, n = struct.unpack("<ddQ", data[off:off + 24]); off += 24
        glen = struct.unpack("<I", data[off:off + 4])[0]; off += 4
        g_q = unpack_bits(data[off:off + glen], bits, n); off += glen
        s = np.unpackbits(np.frombuffer(data[off:off + (n + 7) // 8], dtype=np.uint8))[:n]
        g = g_q.astype(np.float64) / ((1 << bits) - 1) * (g_max - g_min) + g_min
        return ((s.astype(np.float64) * 2 - 1) * g ** 2).reshape(shape)

    # ---- SPECTRAL ------------------------------------------------------------
    def _split(self, arr: np.ndarray):
        if arr.ndim == 1:
            return [arr.reshape(-1, 1)]
        if arr.ndim == 2:
            return [arr]
        if arr.ndim == 3:
            return [arr[i] for i in range(arr.shape[0])]
        if arr.ndim == 4:
            return [arr[b, h] for b in range(arr.shape[0]) for h in range(arr.shape[1])]
        raise ValueError("Tensor %dD nao suportado" % arr.ndim)

    def compress_spectral(self, arr: np.ndarray) -> CompressedTensor:
        arr = np.asarray(arr, dtype=np.float64)
        factors, ranks = [], []
        for mat in self._split(arr):
            U, S, Vt = np.linalg.svd(mat, full_matrices=False)
            energy = S ** 2
            cum = np.cumsum(energy) / (energy.sum() + EPSILON)
            k = max(1, min(int((cum < self.energy_threshold).sum()) + 1, len(S)))
            ranks.append(k)
            factors.append((U[:, :k], S[:k], Vt[:k, :]))
        blobs = []
        for U, S, Vt in factors:
            for f in (U, S, Vt):
                c = self.compress_direct(f)
                blobs.append(struct.pack("<I", len(c.packed)) + c.packed)
        payload = MAGIC + b"S" + struct.pack("<BI", arr.ndim, len(factors))
        for d in arr.shape:
            payload += struct.pack("<I", d)
        for k in ranks:
            payload += struct.pack("<I", k)
        payload += b"".join(blobs)
        var = float(np.mean([np.std(S) / (np.mean(S) + EPSILON) for _, S, _ in factors]))
        return CompressedTensor(payload, "spectral", tuple(arr.shape), self.bits,
                                var, bool(var < self.beta), tuple(ranks))

    def decompress_spectral(self, comp: CompressedTensor) -> np.ndarray:
        data = comp.packed
        if data[:5] != MAGIC + b"S":
            raise ValueError("Magic espectral invalido")
        ndim, n_mats = struct.unpack("<BI", data[5:10])
        off = 10
        shape = []
        for _ in range(ndim):
            shape.append(struct.unpack("<I", data[off:off + 4])[0]); off += 4
        ranks = []
        for _ in range(n_mats):
            ranks.append(struct.unpack("<I", data[off:off + 4])[0]); off += 4
        mats = []
        for _ in range(n_mats):
            fs = []
            for _ in range(3):
                ln = struct.unpack("<I", data[off:off + 4])[0]; off += 4
                sub = CompressedTensor(data[off:off + ln], "direct", (), self.bits, 0.0, False)
                off += ln
                fs.append(self.decompress_direct(sub))
            U, S, Vt = fs
            mats.append(U @ np.diag(S) @ Vt)
        if ndim <= 2:
            return mats[0].reshape(shape)
        return np.stack(mats).reshape(shape)


# --------------------------------------------------------------------- GPU path
# ESTAGIO A2 [PILOTO]: optional torch/CUDA acceleration ported from
# tgl_tensor_v4.py (BitPackerTorch idea). SEMANTICS ARE IDENTICAL to the
# numpy path: the radicalization g=sqrt|L| and the round-half-to-even
# quantization happen on the GPU; the quantized integers make a single
# transfer to the CPU and reuse the SAME pack_bits/header code, so the
# packed bytes are bit-for-bit equal to the numpy path. If torch or CUDA
# is absent (e.g. sandbox), TGLTensorAccel degrades transparently to the
# numpy engine — fail-open on acceleration, never on correctness.
try:                                    # guarded import: torch is OPTIONAL
    import torch as _torch
    _HAS_TORCH = True
except ImportError:                     # pragma: no cover - env dependent
    _torch = None
    _HAS_TORCH = False


def gpu_available() -> bool:
    """True only if torch is importable AND a CUDA device is present."""
    return bool(_HAS_TORCH and _torch.cuda.is_available())


class TGLTensorAccel(TGLTensor):
    """GPU-ready TGL tensor engine (RTX-class), numpy fallback guaranteed.

    device=None -> auto ('cuda' if available else numpy path).
    The `gpu_active` flag is recorded so manifests state which path ran.
    """

    def __init__(self, bits: int = 10, energy_threshold=None, device=None):
        super().__init__(bits, energy_threshold)
        if device is None:
            device = "cuda" if gpu_available() else "cpu"
        self.device = device
        self.gpu_active = bool(_HAS_TORCH and device == "cuda"
                               and _torch.cuda.is_available())

    def compress_direct(self, arr: np.ndarray) -> CompressedTensor:
        if not self.gpu_active:
            return super().compress_direct(arr)      # numpy fallback [REAL]
        arr = np.asarray(arr, dtype=np.float64)
        t = _torch.from_numpy(arr.ravel()).to(self.device)
        g_t = _torch.sqrt(_torch.abs(t))              # root of the trilho
        s_t = _torch.sign(t)
        s_t[s_t == 0] = 1.0
        g_min = float(g_t.min().item())
        g_max = float(g_t.max().item())
        rng = g_max - g_min
        if rng > EPSILON:
            g_norm = (g_t - g_min) / rng
        else:
            g_norm = _torch.zeros_like(g_t)
        # torch.round == round-half-to-even == np.round (same quantization)
        g_q = _torch.round(g_norm * (self.levels - 1)).to(_torch.int64)
        g_q_np = g_q.cpu().numpy().astype(np.uint32)  # single CPU transfer
        s_bit = (s_t > 0).to(_torch.uint8).cpu().numpy()

        g_np = g_t.cpu().numpy()
        g_nz = g_np[g_np > EPSILON]
        variance = float(np.std(g_nz) / (np.mean(g_nz) + EPSILON)) if g_nz.size else 0.0

        header = MAGIC + struct.pack("<BB", self.bits, arr.ndim)
        for d in arr.shape:
            header += struct.pack("<I", d)
        header += struct.pack("<ddQ", g_min, g_max, arr.size)
        g_packed = pack_bits(g_q_np, self.bits)
        header += struct.pack("<I", len(g_packed))
        payload = header + g_packed + np.packbits(s_bit).tobytes()
        return CompressedTensor(payload, "direct", tuple(arr.shape), self.bits,
                                variance, bool(variance < self.beta))
