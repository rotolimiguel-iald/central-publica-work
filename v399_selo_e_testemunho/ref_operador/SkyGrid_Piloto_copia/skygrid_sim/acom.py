#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acom — BLOCO 1a. Root transform of the ecosystem (patent BR 10 2025 026951-1).

    REFLECT:  L -> (g, s)   with  g = sqrt(|L|),  s = sign(L)
    MANIFEST: (g, s) -> L' = s * g^2   (exact reconstruction up to fp roundoff)

[REAL] Ported from ACOMV13/14 (torch) to pure numpy. No epsilon bias inside the
root: reconstruction is exact (the legacy +1e-10 was a normalization guard and
is NOT part of the canonical transform).
"""

import numpy as np


def reflect(L: np.ndarray):
    """L -> (g, s). g = sqrt(|L|) [gravitational root], s = sign(L) (0 -> +1)."""
    L = np.asarray(L, dtype=np.float64)
    g = np.sqrt(np.abs(L))
    s = np.sign(L)
    s[s == 0] = 1.0
    return g, s


def manifest(g: np.ndarray, s: np.ndarray) -> np.ndarray:
    """(g, s) -> L' = s * g^2."""
    return np.asarray(s, dtype=np.float64) * np.asarray(g, dtype=np.float64) ** 2


def roundtrip_residual(L: np.ndarray) -> float:
    """Max absolute reconstruction error of REFLECT->MANIFEST (should be ~fp eps)."""
    g, s = reflect(L)
    L2 = manifest(g, s)
    denom = max(1.0, float(np.max(np.abs(L))))
    return float(np.max(np.abs(np.asarray(L, dtype=np.float64) - L2))) / denom
