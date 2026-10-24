#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coupling — F2. Resonant OH extraction through the modular boundary [SIM].

Extends FusaoFrioMock (BR 10 2026 003456-8) from interface-only to a resonant
coupling MODEL. Three multiplicative factors, each declared:

  eta_res(f)   Lorentzian resonance at the hydroxyl line f0 = 1667.359 MHz
               [DATA, quoted in the patents]: 1/(1+(2Q (f-f0)/f0)^2), Q [CONJ].
  (1 - beta)   the MODULAR BOUNDARY APERTURE [DER]: TGL S-boundary theorem
               gives |R|^2 = beta = sin^2(theta_M) reflected and
               |T|^2 = 1 - beta transmitted — the same Pi_boundary = 1-beta
               ceiling as the pilot's Verb Floor. beta at RUNTIME from tgl_core.
  eta_geo      geometric/impedance-matching efficiency of the device [CONJ].

MEIA-NAT FLOOR [DER, quantitative]: every inscription act dissipates at least
S_boundary = 1/2 nat  =>  E_act >= (1/2) k_B T  (generalized Landauer, nats).
Act rate = the coherence bandwidth f0/Q (one inscription per coherence time).
This floor is ALWAYS debited in the energy balance — negligible at macro
scale, but never zero: the boundary charges for every act of distinction.

No physical verdict: eta values are design hypotheses for the bench.
"""

import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skygrid_sim import tgl_core                     # noqa: E402

K_BOLTZMANN = 1.380649e-23      # J/K  [DATA] SI exact
OMEGA_OH_MHZ = 1667.359         # [DATA] hydroxyl line quoted in the patents


class ResonantCoupler:
    """OH-resonance coupler of one ExtractorSat [SIM]."""

    def __init__(self, Q: float = 1.0e4, eta_geo: float = 0.80,
                 T_kelvin: float = 300.0, f_drive_MHz: float = OMEGA_OH_MHZ):
        if Q <= 0 or not (0.0 <= eta_geo <= 1.0) or T_kelvin <= 0:
            raise ValueError("parametros de acoplamento invalidos")
        self.Q = float(Q)
        self.eta_geo = float(eta_geo)
        self.T = float(T_kelvin)
        self.f_drive = float(f_drive_MHz)
        self.beta = tgl_core.beta()              # runtime, never literal
        self.aperture = 1.0 - self.beta          # [DER] boundary transmission
        self.f0 = OMEGA_OH_MHZ
        self.acts = 0                            # inscription ledger
        self.energy_halfnat_J = 0.0              # Meia-Nat cost ledger

    # ---- resonance ------------------------------------------------------------
    def eta_res(self, f_MHz: float = None) -> float:
        f = self.f_drive if f_MHz is None else float(f_MHz)
        delta = (f - self.f0) / self.f0
        return 1.0 / (1.0 + (2.0 * self.Q * delta) ** 2)

    @property
    def bandwidth_Hz(self) -> float:
        return self.f0 * 1e6 / self.Q

    def eta_couple(self, f_MHz: float = None) -> float:
        """Total coupling efficiency = (1-beta) * eta_res * eta_geo, in [0,1)."""
        return self.aperture * self.eta_res(f_MHz) * self.eta_geo

    # ---- Meia-Nat entropic floor -----------------------------------------------
    def halfnat_power_W(self) -> float:
        """P_halfnat = (1/2) k_B T * (acts/s), acts/s = coherence bandwidth."""
        return 0.5 * K_BOLTZMANN * self.T * self.bandwidth_Hz

    # ---- extraction step --------------------------------------------------------
    def couple(self, reservoir, dt_s: float, placebo: bool = False) -> dict:
        """One coupling window: draws from the reservoir the couplable power
        plus the Meia-Nat overhead. PLACEBO (claim 3): no beta coupling —
        eta_couple = 0, extracts NOTHING, delivers 0 W by construction.
        Returns the energy ledger of the window [SIM]."""
        if placebo:
            reservoir.idle(dt_s)
            return {"E_in_J": 0.0, "E_halfnat_J": 0.0, "E_loss_coupling_J": 0.0,
                    "eta_couple": 0.0, "acts": 0, "placebo": True,
                    "physical_verdict_allowed": False}
        eta = self.eta_couple()
        P_avail = reservoir.power_available()
        P_couple = eta * P_avail                      # what crosses the boundary
        P_over = self.halfnat_power_W()               # entropic floor (always)
        # withdraw coupled power + the half-nat overhead from the source
        E_gross = reservoir.extract(P_couple + P_over, dt_s)
        # the overhead is paid first (it is the cost of the act itself)
        E_halfnat = min(E_gross, P_over * dt_s)
        E_in = E_gross - E_halfnat                    # usable coupled energy
        n_acts = max(1, int(round(self.bandwidth_Hz * dt_s)))
        self.acts += n_acts
        self.energy_halfnat_J += E_halfnat
        return {"E_in_J": E_in, "E_halfnat_J": E_halfnat,
                "E_loss_coupling_J": 0.0,   # sub-unity eta = not-extracted (stays in field)
                "eta_couple": eta, "acts": n_acts, "placebo": False,
                "physical_verdict_allowed": False}

    def spec(self) -> dict:
        return {"f0_MHz": self.f0, "f_drive_MHz": self.f_drive, "Q": self.Q,
                "bandwidth_Hz": self.bandwidth_Hz, "eta_geo": self.eta_geo,
                "boundary_aperture_1_minus_beta": self.aperture,
                "beta_runtime": self.beta,
                "theta_M_deg": math.degrees(tgl_core.theta_m()),
                "halfnat_power_W": self.halfnat_power_W(),
                "T_K": self.T,
                "marker": "[SIM] acoplamento modelado; fisica do campo [CONJ]",
                "physical_verdict_allowed": False}
