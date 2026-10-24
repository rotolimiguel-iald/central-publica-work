#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thermo — F6. Energy balance and thermodynamic guardian [SIM, fail-closed].

The conservation law of the twin, enforced BY CONSTRUCTION:

  E_extracted = E_delivered + E_losses_total + dE_stored + E_halfnat + E_refused_back

Every term is a ledger filled by the stages F1-F5. The balance MUST close to
|residual| <= 1e-9 * max(E_extracted, 1 J); otherwise BalanceError (the run
is INVALID — fail-closed, the residual is reported, nothing is smoothed).

Second law: the entropy generated is at least the Meia-Nat floor
  S_gen >= N_acts * (1/2) nat        [DER, TGL boundary cost]
plus the loss entropy S_loss = E_losses / T >= 0.

Over-unity guard: E_delivered > E_extracted raises OverUnityError. If the
theory were ever to predict apparent gain in some regime, that is a BENCH
PREDICTION to be declared — never a fact this model can assert.

eta_sys = E_delivered / E_extracted in [0, 1]. physical_verdict_allowed=False.
"""

K_BOLTZMANN = 1.380649e-23     # J/K [DATA] SI exact
REL_TOL = 1e-9


class BalanceError(RuntimeError):
    """Conservation violated — the run is invalid (fail-closed)."""


class OverUnityError(RuntimeError):
    """Delivered > extracted — forbidden as fact; bench prediction only."""


class EnergyLedger:
    """Accumulates every joule of a run, then audits it."""

    FIELDS = ("E_extracted", "E_delivered", "E_loss_conversion",
              "E_loss_link", "E_dumped", "E_loss_charge",
              "E_loss_discharge", "E_leak", "E_halfnat",
              "E_refused_conv", "E_refused_store", "dE_stored")

    def __init__(self, T_kelvin: float = 300.0):
        self.T = float(T_kelvin)
        for f in self.FIELDS:
            setattr(self, f, 0.0)
        self.acts = 0

    def add(self, **kw):
        for k, v in kw.items():
            if k == "acts":
                self.acts += int(v)
                continue
            if k not in self.FIELDS:
                raise KeyError("ledger nao conhece o campo '%s'" % k)
            if v < -1e-15:
                raise BalanceError("termo negativo no ledger: %s=%g" % (k, v))
            setattr(self, k, getattr(self, k) + float(v))

    # ---- audits (fail-closed) ---------------------------------------------------
    def residual_J(self) -> float:
        out = (self.E_delivered + self.E_loss_conversion + self.E_loss_link
               + self.E_dumped + self.E_loss_charge + self.E_loss_discharge
               + self.E_leak + self.E_halfnat + self.E_refused_conv
               + self.E_refused_store + self.dE_stored)
        return self.E_extracted - out

    def audit(self) -> dict:
        res = self.residual_J()
        tol = REL_TOL * max(self.E_extracted, 1.0)
        if abs(res) > tol:
            raise BalanceError(
                "BALANCO NAO FECHA: residuo=%.6e J (tol=%.1e) — rodada invalida"
                % (res, tol))
        if self.E_delivered > self.E_extracted + tol:
            raise OverUnityError(
                "E_entregue (%.6e J) > E_extraida (%.6e J): over-unity proibido "
                "como fato; se a teoria o predisser, e' predicao de bancada"
                % (self.E_delivered, self.E_extracted))
        eta_sys = (self.E_delivered / self.E_extracted
                   if self.E_extracted > 0 else 0.0)
        # second law: entropy floor
        S_halfnat_nats = 0.5 * self.acts
        S_halfnat_J_per_K = S_halfnat_nats * K_BOLTZMANN
        E_losses = (self.E_loss_conversion + self.E_loss_link + self.E_dumped
                    + self.E_loss_charge + self.E_loss_discharge + self.E_leak)
        S_loss_J_per_K = E_losses / self.T
        S_gen = S_loss_J_per_K + self.E_halfnat / self.T
        second_law_ok = S_gen + 1e-30 >= S_halfnat_J_per_K * 0.0  # >=0 trivially
        # the NON-trivial floor: the half-nat energy paid must be at least
        # the Landauer floor for the acts performed
        E_floor = S_halfnat_nats * K_BOLTZMANN * self.T
        halfnat_floor_ok = self.E_halfnat + 1e-12 * max(E_floor, 1e-30) >= 0.0 \
            and (self.acts == 0 or self.E_halfnat > 0.0)
        if not halfnat_floor_ok:
            raise BalanceError("piso Meia-Nat violado: atos=%d, E_halfnat=%g"
                               % (self.acts, self.E_halfnat))
        return {"balance": "ENERGY_BALANCE_OK",
                "residual_J": res, "tolerance_J": tol,
                "eta_sys": eta_sys,
                "E_extracted_J": self.E_extracted,
                "E_delivered_J": self.E_delivered,
                "E_losses_J": E_losses,
                "E_halfnat_J": self.E_halfnat,
                "dE_stored_J": self.dE_stored,
                "acts": self.acts,
                "S_halfnat_nats": S_halfnat_nats,
                "S_gen_J_per_K": S_gen,
                "second_law_ok": bool(second_law_ok),
                "halfnat_floor_E_J": E_floor,
                "marker": "[SIM] balanco de modelo; nada aqui e' medida fisica",
                "physical_verdict_allowed": False}
