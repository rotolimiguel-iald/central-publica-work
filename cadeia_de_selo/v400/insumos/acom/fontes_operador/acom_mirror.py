#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acom_mirror — BLOCO 1b. Dimensional reflection (patent BR 10 2026 003428-2).

    REFLECT : L -> (psi, theta)   psi in H4 named from (sign L, sign dL);
                                  theta = arcsin(g / g_max), angular return info.
    MANIFEST: (psi, theta) -> L' = s * (g_max * sin(theta))^2   (the FOLD, x2)

[REAL] Ported from Acom_v17_mirror.py (torch) to pure numpy.
Reconciliation note (operator decision, 02/07/2026): the legacy file carried the
coupling as a numeric literal ("mirror imperfection"). Here the coupling is
imported from tgl_core.beta() — the standard algebraic form alpha*sqrt(e),
computed at runtime. No numeric beta literal exists in this module.

H4 psionic states (2 bits): 0 |COLLAPSE+> (+,-)  1 |ASCEND+> (+,+)
                            2 |EMERGE->  (-,+)  3 |FALL->   (-,-)
Parity: states 0,3 inverse (F_exp active); 1,2 normal.
F_exp = mean parity; S_psi = -sum p_k log2 p_k (state entropy).
"""

import math
import zlib
from dataclasses import dataclass
from typing import Dict, Any, Tuple

import numpy as np

from . import tgl_core

EPSILON = 1e-10          # normalization guard only (never enters the root transform)
PARITY = np.array([-1.0, +1.0, +1.0, -1.0])   # per state 0..3
SIGN_L_OF_STATE = np.array([+1.0, +1.0, -1.0, -1.0])


@dataclass
class MirrorReflection:
    psi_packed: bytes        # H4 states, 2 bits each, zlib-compressed
    theta_packed: bytes      # quantized angles, zlib-compressed
    metadata: Dict[str, Any]


def _nominate(sign_L: np.ndarray, sign_dL: np.ndarray) -> np.ndarray:
    """Name psi states in H4 from the two signs (NOMINATION, not encoding)."""
    return ((sign_L < 0).astype(np.uint8) * 2 + (sign_dL > 0).astype(np.uint8))


def _pack2bits(states: np.ndarray) -> bytes:
    n = len(states)
    padded = np.zeros(((n + 3) // 4) * 4, dtype=np.uint8)
    padded[:n] = states
    b = (padded[0::4] << 6) | (padded[1::4] << 4) | (padded[2::4] << 2) | padded[3::4]
    return b.astype(np.uint8).tobytes()


def _unpack2bits(packed: bytes, n: int) -> np.ndarray:
    b = np.frombuffer(packed, dtype=np.uint8)
    out = np.empty(len(b) * 4, dtype=np.uint8)
    out[0::4] = (b >> 6) & 0x03
    out[1::4] = (b >> 4) & 0x03
    out[2::4] = (b >> 2) & 0x03
    out[3::4] = b & 0x03
    return out[:n]


class DimensionalMirror:
    """Numpy port of the v17 mirror. angular_bits <= 16."""

    def __init__(self, angular_bits: int = 8):
        if not (1 <= angular_bits <= 16):
            raise ValueError("angular_bits must be in [1,16]")
        self.angular_bits = angular_bits
        self.n_angles = 1 << angular_bits
        self.beta = tgl_core.beta()            # runtime, never literal
        self.theta_miguel = tgl_core.theta_m()

    # -- forward -------------------------------------------------------------
    def reflect(self, L: np.ndarray) -> MirrorReflection:
        L = np.asarray(L, dtype=np.float64)
        shape = L.shape
        flat = L.ravel()
        n = flat.size

        g = np.sqrt(np.abs(flat))
        g_max = float(g.max()) if n else 0.0

        dL = np.zeros_like(flat)
        if n > 1:
            dL[1:] = flat[1:] - flat[:-1]
            dL[0] = dL[1]
        sign_L = np.sign(flat); sign_L[sign_L == 0] = 1.0
        sign_dL = np.sign(dL); sign_dL[sign_dL == 0] = 1.0

        psi = _nominate(sign_L, sign_dL)

        theta = np.arcsin(np.clip(g / (g_max + EPSILON), 0.0, 1.0))
        qmax = self.n_angles - 1
        theta_q = np.clip(np.round(theta / (math.pi / 2) * qmax), 0, qmax)
        theta_q = theta_q.astype(np.uint8 if self.angular_bits <= 8 else np.uint16)

        parities = PARITY[psi]
        f_exp = float(parities.mean()) if n else 0.0
        counts = np.bincount(psi, minlength=4).astype(np.float64)
        probs = counts[counts > 0] / max(n, 1)
        s_psi = float(-(probs * np.log2(probs)).sum()) if n else 0.0

        psi_packed = zlib.compress(_pack2bits(psi), 9)
        theta_packed = zlib.compress(theta_q.tobytes(), 9)

        original_size = n * 8
        compressed_size = len(psi_packed) + len(theta_packed)
        meta = {
            "version": "skygrid_sim.acom_mirror v1 (port of ACOM v17 MIRROR)",
            "shape": tuple(shape), "n_elements": n,
            "angular_bits": self.angular_bits, "g_max": g_max,
            "f_exp": f_exp, "state_entropy": s_psi,
            "state_counts": {int(k): int(v) for k, v in enumerate(counts)},
            "original_size": original_size, "compressed_size": compressed_size,
            "compression_ratio": (original_size / compressed_size) if compressed_size else float("inf"),
            "beta_runtime": self.beta, "theta_miguel_rad": self.theta_miguel,
        }
        return MirrorReflection(psi_packed, theta_packed, meta)

    # -- backward ------------------------------------------------------------
    def manifest(self, r: MirrorReflection) -> np.ndarray:
        meta = r.metadata
        n = meta["n_elements"]
        psi = _unpack2bits(zlib.decompress(r.psi_packed), n)
        dt = np.uint8 if meta["angular_bits"] <= 8 else np.uint16
        theta_q = np.frombuffer(zlib.decompress(r.theta_packed), dtype=dt)[:n]

        qmax = (1 << meta["angular_bits"]) - 1
        theta = theta_q.astype(np.float64) / qmax * (math.pi / 2)
        g = meta["g_max"] * np.sin(theta)
        s = SIGN_L_OF_STATE[psi]
        return (s * g ** 2).reshape(meta["shape"])


def roundtrip_correlation(L: np.ndarray, angular_bits: int = 8) -> Tuple[float, MirrorReflection]:
    """Pearson correlation between original and manifested data (lossy: quantized theta)."""
    m = DimensionalMirror(angular_bits=angular_bits)
    r = m.reflect(L)
    L2 = m.manifest(r)
    a = np.asarray(L, dtype=np.float64).ravel()
    b = L2.ravel()
    if a.std() == 0 or b.std() == 0:
        return (1.0 if np.allclose(a, b) else 0.0), r
    return float(np.corrcoef(a, b)[0, 1]), r
