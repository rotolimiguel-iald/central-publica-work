#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storage — F5. Celula de Reversao as energy storage [SIM].

Extends skygrid_sim/celula_reversao.py (BR 10 2026 004849-6): the pilot showed
the ANGULAR PHASE retains the stored pattern with corr ~1.0000 [REAL in-model].
The ENERGY losses of a physical cell are design hypotheses [CONJ]:

  eta_rt      round-trip efficiency (charge*discharge), split symmetrically:
              eta_ch = eta_dis = sqrt(eta_rt);
  lambda_sd   self-discharge rate [1/s] (leakage to heat, accounted);
  E_cap       capacity [J]; overflow is refused at the door (not lost).

State of charge SoC(t) is explicit; every joule in = stored + charge-loss;
every joule out = delivered + discharge-loss; leakage is accounted per step.
"""


class ReversalCellStore:
    """Energy store of one GroundBase [SIM]."""

    def __init__(self, E_cap_J: float = 2.0e6, eta_rt: float = 0.95,
                 lambda_sd_per_s: float = 1.0e-6):
        if E_cap_J <= 0 or not (0.0 < eta_rt <= 1.0) or lambda_sd_per_s < 0:
            raise ValueError("parametros da celula invalidos")
        self.E_cap = float(E_cap_J)
        self.eta_rt = float(eta_rt)
        self.eta_ch = eta_rt ** 0.5
        self.eta_dis = eta_rt ** 0.5
        self.lam = float(lambda_sd_per_s)
        self.soc_J = 0.0
        # ledgers
        self.E_charged_J = 0.0        # gross energy pushed at the door
        self.E_refused_J = 0.0        # refused at the door (full cell)
        self.E_loss_charge_J = 0.0
        self.E_loss_discharge_J = 0.0
        self.E_leak_J = 0.0
        self.E_delivered_J = 0.0

    def charge(self, E_in_J: float) -> dict:
        if E_in_J < 0:
            raise ValueError("carga negativa")
        headroom = max(0.0, (self.E_cap - self.soc_J) / self.eta_ch)
        E_take = min(E_in_J, headroom)
        E_refused = E_in_J - E_take
        stored = E_take * self.eta_ch
        self.soc_J += stored
        self.E_charged_J += E_take
        self.E_refused_J += E_refused
        self.E_loss_charge_J += E_take - stored
        return {"E_stored_J": stored, "E_refused_J": E_refused,
                "E_loss_charge_J": E_take - stored,
                "physical_verdict_allowed": False}

    def discharge(self, E_request_J: float) -> dict:
        if E_request_J < 0:
            raise ValueError("descarga negativa")
        E_from_soc = min(self.soc_J, E_request_J / self.eta_dis
                         if self.eta_dis > 0 else 0.0)
        delivered = E_from_soc * self.eta_dis
        self.soc_J -= E_from_soc
        self.E_loss_discharge_J += E_from_soc - delivered
        self.E_delivered_J += delivered
        return {"E_delivered_J": delivered,
                "E_loss_discharge_J": E_from_soc - delivered,
                "physical_verdict_allowed": False}

    def step(self, dt_s: float):
        """Self-discharge leakage for dt seconds (accounted as heat)."""
        leak = self.soc_J * (1.0 - pow(2.718281828459045, -self.lam * dt_s))
        self.soc_J -= leak
        self.E_leak_J += leak

    def state(self) -> dict:
        return {"soc_J": self.soc_J, "soc_frac": self.soc_J / self.E_cap,
                "E_cap_J": self.E_cap, "eta_rt": self.eta_rt,
                "ledgers": {"charged": self.E_charged_J,
                            "refused": self.E_refused_J,
                            "loss_charge": self.E_loss_charge_J,
                            "loss_discharge": self.E_loss_discharge_J,
                            "leak": self.E_leak_J,
                            "delivered": self.E_delivered_J},
                "marker": "[SIM] perdas de projeto [CONJ]; fase angular [REAL no piloto]",
                "physical_verdict_allowed": False}
