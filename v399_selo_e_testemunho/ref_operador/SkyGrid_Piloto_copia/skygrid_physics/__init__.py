# -*- coding: utf-8 -*-
"""
skygrid_physics — ESTAGIO F (v3). Energy-physics core of the SkyGrid digital twin.

EPISTEMIC CONTRACT (the ruler, applied to energy):
  * Everything here is [SIM] — a PREDICTIVE MODEL under declared hypotheses.
    The physical existence of the psionic field reservoir and its couplings is
    [CONJ]: a bench question, never settled by this code.
  * Energy is CONSERVED by construction: every joule delivered is an explicit
    debit from the reservoir; every inefficiency is an accounted loss; the
    balance MUST close (fail-closed) — see thermo.py.
  * The Meia-Nat (S_boundary = 1/2 nat per inscription act) enters as the
    minimum entropic cost of coupling (generalized Landauer), never zero.
  * beta_TGL is NEVER a literal: runtime alpha*sqrt(e) from skygrid_sim.tgl_core.
  * physical_verdict_allowed = False in every output. Max verdict:
    ENERGY_BALANCE_OK / MODEL_CLOSES (the model closes) — never "generates
    energy" as physical fact. What remains after this package is the bench.
"""

PHYSICAL_VERDICT_ALLOWED = False
