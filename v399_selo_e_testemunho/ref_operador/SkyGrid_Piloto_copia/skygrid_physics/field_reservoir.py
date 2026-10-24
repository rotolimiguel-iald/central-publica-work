#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
field_reservoir — F1. The psionic field RESERVOIR as an energy source [SIM].

[CONJ] the physical existence of the field; [SIM] this model. The reservoir is
modeled like any honest source (a solar panel's Sun, a turbine's gradient):

  * flux density S_field [W/m^2]  — design parameter, sweepable;
  * capture area A_cap [m^2] per extractor;
  * deterministic availability alpha_avail(t) in [0,1] (field 'weather', seeded);
  * LOCAL DEPLETION: the local patch has finite energy E_local and replenishes
    with time constant tau_rep. Extracting faster than replenishment depresses
    availability:   dD/dt = P_ext/E_local - D/tau_rep,  D in [0, 0.95].

Conservation: every joule extracted is an explicit DEBIT (energy_debited_J).
Nothing is created: the twin's delivered energy can never exceed this debit.
No physical verdict: the numbers are model predictions under the hypotheses.
"""

import math

import numpy as np


class FieldReservoir:
    """Local reservoir patch seen by one extractor node."""

    def __init__(self, S_field_W_m2: float = 100.0, A_cap_m2: float = 10.0,
                 E_local_J: float = 5.0e6, tau_rep_s: float = 600.0,
                 seed: int = 11):
        if S_field_W_m2 < 0 or A_cap_m2 <= 0 or E_local_J <= 0 or tau_rep_s <= 0:
            raise ValueError("parametros do reservatorio devem ser positivos")
        self.S_field = float(S_field_W_m2)      # [CONJ] design parameter
        self.A_cap = float(A_cap_m2)
        self.E_local = float(E_local_J)
        self.tau_rep = float(tau_rep_s)
        self.rng = np.random.default_rng(seed)
        # deterministic availability profile: slow seeded modulation in [0.6, 1]
        self._phase = float(self.rng.uniform(0, 2 * math.pi))
        self._period = float(self.rng.uniform(1800.0, 5400.0))   # 30-90 min
        self.depletion = 0.0                     # D in [0, 0.95]
        self.energy_debited_J = 0.0              # conservation ledger (out)
        self.t = 0.0

    # ---- availability ---------------------------------------------------------
    def availability(self, t: float) -> float:
        """Deterministic field availability in [0.6, 1.0] (no randomness at
        call time; the profile was fixed at construction)."""
        return 0.8 + 0.2 * math.sin(2 * math.pi * t / self._period + self._phase)

    def power_available(self) -> float:
        """P_avail = S_field * A_cap * alpha_avail(t) * (1 - D)   [W]."""
        return (self.S_field * self.A_cap * self.availability(self.t)
                * (1.0 - self.depletion))

    # ---- extraction (the only way energy leaves the reservoir) -----------------
    def extract(self, P_request_W: float, dt_s: float) -> float:
        """Withdraw up to P_request for dt seconds. Returns the energy actually
        granted [J], debits the ledger and advances depletion. Fail-closed on
        negative requests."""
        if P_request_W < 0 or dt_s <= 0:
            raise ValueError("extracao invalida (P<0 ou dt<=0)")
        P_grant = min(P_request_W, self.power_available())
        E = P_grant * dt_s
        self.energy_debited_J += E
        # depletion dynamics (explicit Euler, dt small vs tau_rep)
        dD = (P_grant * dt_s) / self.E_local - self.depletion * dt_s / self.tau_rep
        self.depletion = float(min(0.95, max(0.0, self.depletion + dD)))
        self.t += dt_s
        return E

    def idle(self, dt_s: float):
        """Time passes without extraction: replenishment only."""
        self.depletion = float(max(
            0.0, self.depletion * (1.0 - dt_s / self.tau_rep)))
        self.t += dt_s

    def state(self) -> dict:
        return {"S_field_W_m2": self.S_field, "A_cap_m2": self.A_cap,
                "availability": self.availability(self.t),
                "depletion": self.depletion,
                "power_available_W": self.power_available(),
                "energy_debited_J": self.energy_debited_J,
                "marker": "[SIM] fonte modelada; existencia fisica [CONJ]",
                "physical_verdict_allowed": False}
