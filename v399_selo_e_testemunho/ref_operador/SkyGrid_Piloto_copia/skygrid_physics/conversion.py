#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conversion — F3. Dipolo Transistor as power converter/rectifier [SIM].

Extends the state machine of skygrid_sim/dipolo.py (BR 10 2026 004688-4) to
an ENERGY conversion model: the resonant carrier is rectified through the
ontological radicalization g = sqrt|L| (the pilot's data rail made power).

  eta_conv    rectification efficiency [CONJ] design parameter (0.85-0.98);
  eta_quant   quantization loss of the angular rail: the pilot MEASURED
              fidelity F_q ~ 0.9999 on the 10-bit rail [REAL in-model], so
              eta_quant = F_q^2 (power goes as amplitude squared);
  gate        the dipole switch: closed => nothing is drawn (no phantom loss).

Every joule in = joule out + accounted conversion loss. [SIM] throughout;
no physical rectifier is validated here.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skygrid_sim.dipolo import DipoloTransistor        # noqa: E402
from skygrid_sim.tgl_tensor import TGLTensor           # noqa: E402


class DipoloConverter:
    """Power conversion stage of one ExtractorSat [SIM]."""

    def __init__(self, eta_conv: float = 0.92, bits: int = 10, seed: int = 11):
        if not (0.0 < eta_conv <= 1.0):
            raise ValueError("eta_conv fora de (0,1]")
        self.eta_conv = float(eta_conv)
        self.dipolo = DipoloTransistor()
        self.rng = np.random.default_rng(seed)
        # measure the quantization fidelity of the angular rail ONCE, live
        # (the same 10-bit rail the data pilot uses) — [REAL in-model]
        probe = self.rng.normal(size=512) * 3.0
        eng = TGLTensor(bits=bits)
        rt = eng.decompress_direct(eng.compress_direct(probe))
        F_q = float(np.corrcoef(probe, rt)[0, 1])
        self.eta_quant = float(np.clip(F_q, 0.0, 1.0)) ** 2
        self.gate_open_history = []

    def convert(self, E_in_J: float, carrier: np.ndarray = None) -> dict:
        """One conversion window. Returns converted energy + accounted loss."""
        if E_in_J < 0:
            raise ValueError("energia negativa na conversao")
        if carrier is None:
            carrier = self.rng.normal(size=64)
        g = self.dipolo.gate(np.asarray(carrier, dtype=np.float64))
        gate_open = bool(g["open"])
        self.gate_open_history.append(gate_open)
        if not gate_open or E_in_J == 0.0:
            # gate closed: energy was NOT drawn downstream in this window;
            # it returns to the ledger as pass-through-refused (no loss).
            return {"E_out_J": 0.0, "E_loss_conv_J": 0.0,
                    "E_refused_J": E_in_J, "gate_open": gate_open,
                    "eta_stage": 0.0, "physical_verdict_allowed": False}
        eta = self.eta_conv * self.eta_quant
        E_out = eta * E_in_J
        return {"E_out_J": E_out, "E_loss_conv_J": E_in_J - E_out,
                "E_refused_J": 0.0, "gate_open": True,
                "eta_stage": eta, "physical_verdict_allowed": False}

    def spec(self) -> dict:
        return {"eta_conv": self.eta_conv, "eta_quant": self.eta_quant,
                "eta_total": self.eta_conv * self.eta_quant,
                "marker": "[SIM] conversao modelada; retificador fisico [HARDWARE]",
                "physical_verdict_allowed": False}
