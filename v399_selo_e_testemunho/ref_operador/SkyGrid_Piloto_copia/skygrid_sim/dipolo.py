#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dipolo — BLOCO 5b. Luminodynamic Dipole Transistor (patent BR 10 2026 004688-4).

Switching by ontological radicalization + psionic condensate, modeled as a
finite state machine [PILOTO/HARDWARE mock].

States: REFLECT (input, L->(g,s)) and MANIFEST (output, (g,s)->L').
The gate opens when the input's ontological "radical" g exceeds a threshold
set by the Verb floor beta*g_max (below it the signal is dephased noise and
the transistor stays closed). This is the same beta filter as the kernel.
"""

import numpy as np

from . import tgl_core


class DipoloTransistor:
    REFLECT = "REFLECT"
    MANIFEST = "MANIFEST"

    def __init__(self):
        self.state = self.REFLECT
        self.beta = tgl_core.beta()
        self._latched = None

    def gate(self, signal: np.ndarray) -> dict:
        """Switch: open (MANIFEST) if max radical g exceeds beta*g_max_seen."""
        L = np.asarray(signal, dtype=np.float64).ravel()
        g = np.sqrt(np.abs(L))
        s = np.sign(L); s[s == 0] = 1.0
        g_max = float(g.max()) if g.size else 0.0
        threshold = self.beta * g_max
        active = float(g.max()) > threshold if g.size else False
        if active:
            self.state = self.MANIFEST
            self._latched = (g, s)
            out = s * g ** 2
        else:
            self.state = self.REFLECT
            out = np.zeros_like(L)
        return {"state": self.state, "open": bool(active),
                "threshold": threshold, "output": out}
