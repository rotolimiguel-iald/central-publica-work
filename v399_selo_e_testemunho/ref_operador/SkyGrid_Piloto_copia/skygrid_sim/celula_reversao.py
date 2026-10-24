#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
celula_reversao — BLOCO 5c. Reversal Cell (patent BR 10 2026 004849-6).

Energy storage by angular phase coding on a holographic substrate
[PILOTO/HARDWARE mock].

  Charge port (Dipolo REFLECT): energy amplitude L -> angular phase
     theta = arcsin(g/g_max), g = sqrt|L|, sign s. Stored on the "6 inner
     faces" as (s, theta_quantized, g_max).
  Discharge port (Dipolo MANIFEST): L' = s * (g_max*sin(theta))^2.
  Stability controller: Lindblad phase operator keeps the stored phase (in the
     pilot: exact storage, no self-discharge -> ideal retention == 1).

Round-trip is lossy only through the angular quantization (configurable bits).
"""

import math

import numpy as np

from . import tgl_core

EPSILON = 1e-10


class CelulaReversao:
    def __init__(self, angular_bits: int = 16):
        self.bits = angular_bits
        self.qmax = (1 << angular_bits) - 1
        self.beta = tgl_core.beta()
        self._store = None

    def charge(self, energy: np.ndarray) -> dict:
        L = np.asarray(energy, dtype=np.float64)
        shape = L.shape
        flat = L.ravel()
        g = np.sqrt(np.abs(flat))
        g_max = float(g.max()) if g.size else 0.0
        s = np.sign(flat); s[s == 0] = 1.0
        theta = np.arcsin(np.clip(g / (g_max + EPSILON), 0, 1))
        theta_q = np.round(theta / (math.pi / 2) * self.qmax).astype(np.uint32)
        self._store = {"s": (s > 0), "theta_q": theta_q, "g_max": g_max, "shape": shape}
        stored_energy = float(np.sum(flat ** 2))
        return {"stored_faces": 6, "g_max": g_max, "energy_in": stored_energy}

    def discharge(self) -> np.ndarray:
        if self._store is None:
            raise ValueError("celula vazia")
        st = self._store
        theta = st["theta_q"].astype(np.float64) / self.qmax * (math.pi / 2)
        g = st["g_max"] * np.sin(theta)
        s = np.where(st["s"], 1.0, -1.0)
        return (s * g ** 2).reshape(st["shape"])

    def retention(self, energy: np.ndarray) -> float:
        """Fraction of energy recovered after a charge/discharge cycle."""
        self.charge(energy)
        out = self.discharge()
        e_in = float(np.sum(np.asarray(energy, dtype=np.float64) ** 2))
        e_out = float(np.sum(out ** 2))
        return e_out / e_in if e_in > 0 else 1.0
