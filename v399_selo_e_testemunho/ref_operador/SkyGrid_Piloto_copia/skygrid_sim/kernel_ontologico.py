#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kernel_ontologico — BLOCO 3c. Ontological kernel (patent BR 10 2026 006129-8).

Two-layer REFLECT/MANIFEST processing with the VERB FILTER by beta_TGL.

Pilot reading [PILOTO — the patent speaks of LLM attention; here the node
version]: a node's attention/weight vector w is passed through
  layer 1 (REFLECT) : dimensional reflection of w (acom_mirror);
  layer 2 (MANIFEST): re-emergence, then the VERB FILTER — components below
                      the beta floor (beta * max(w)) are cut and the vector
                      is renormalized. beta comes from tgl_core at runtime.
The cosmogenesis initial condition of the patent maps, in the pilot, to the
uniform state as layer-zero attention (no component privileged before the
first inscription).
"""

import numpy as np

from . import tgl_core
from .acom_mirror import DimensionalMirror


def initial_attention(n: int) -> np.ndarray:
    """Layer zero: uniform (no name privileged before the first act)."""
    return np.full(n, 1.0 / n)


def verb_filter(w: np.ndarray) -> tuple:
    """Cut components below beta*max(w); renormalize. Returns (w_f, stats)."""
    w = np.asarray(w, dtype=np.float64)
    if np.any(w < 0):
        raise ValueError("attention weights must be non-negative")
    beta = tgl_core.beta()
    floor = beta * float(w.max()) if w.size else 0.0
    mask = w >= floor
    if not mask.any():
        mask = w == w.max()
    w_f = np.where(mask, w, 0.0)
    total = w_f.sum()
    if total > 0:
        w_f = w_f / total
    stats = {"floor": floor, "kept": int(mask.sum()), "cut": int((~mask).sum()),
             "beta_runtime": beta}
    return w_f, stats


def two_layer(w: np.ndarray, angular_bits: int = 10) -> tuple:
    """REFLECT -> MANIFEST -> VERB FILTER (the kernel's two layers)."""
    mirror = DimensionalMirror(angular_bits=angular_bits)
    r = mirror.reflect(np.asarray(w, dtype=np.float64))
    w_back = np.abs(mirror.manifest(r))        # attention is non-negative
    return verb_filter(w_back)
