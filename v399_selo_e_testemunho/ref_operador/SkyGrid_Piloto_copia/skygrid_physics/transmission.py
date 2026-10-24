#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transmission — F4. Psi-channel power link with the DOUBLE RAIL [SIM].

The v2 pilot validates DATA by two independent rails; here the same discipline
is applied to POWER:

  * the Psi rail (holographic carrier — physically [HARDWARE], via the
    Supercondutor/Motor de Dobra channels) TRANSPORTS the window's energy;
  * the E rail (conventional measurement) independently measures it; if the
    two measurements diverge beyond tolerance, the window is REJECTED and its
    energy is DUMPED — accounted as loss, never silently vanished.

Link efficiency: eta_link = eta_hop ^ n_hops, with n_hops taken from the REAL
Psi-NET angular addressing (hop quantum = theta_M). eta_hop [CONJ] design
parameter. Classical microwave beaming is kept in the engineering dossier as
the reference baseline [REAL engineering], not here.
"""

RAIL_POWER_TOLERANCE = 1e-3      # relative divergence Psi vs E measurement


class PsiPowerLink:
    """Point-to-point power link sat->base over n_hops [SIM]."""

    def __init__(self, eta_hop: float = 0.985):
        if not (0.0 < eta_hop <= 1.0):
            raise ValueError("eta_hop fora de (0,1]")
        self.eta_hop = float(eta_hop)

    def eta_link(self, n_hops: int) -> float:
        return self.eta_hop ** max(1, int(n_hops))

    def transmit(self, E_in_J: float, n_hops: int,
                 rail_data_accepted: bool = True,
                 meter_disturbance: float = 0.0) -> dict:
        """One transmission window.

        rail_data_accepted: the verdict of the DATA double rail + quorum for
        this window (from the v2 orchestrator). Power inherits the data
        verdict: no sealed data block => the window's energy is dumped.
        meter_disturbance: injected divergence between the two power meters
        (fault-injection hook); beyond tolerance => rejected => dumped.
        """
        if E_in_J < 0:
            raise ValueError("energia negativa na transmissao")
        eta = self.eta_link(n_hops)
        E_arrive = eta * E_in_J
        E_loss_link = E_in_J - E_arrive

        # double rail on power: Psi meter vs E meter
        P_psi_meter = E_arrive
        P_e_meter = E_arrive * (1.0 + float(meter_disturbance))
        div = abs(P_psi_meter - P_e_meter) / max(P_psi_meter, 1e-30)
        rails_agree = div <= RAIL_POWER_TOLERANCE

        accepted = bool(rail_data_accepted and rails_agree)
        if accepted:
            E_rx, E_dump = E_arrive, 0.0
        else:
            E_rx, E_dump = 0.0, E_arrive     # dumped: accounted, not vanished
        return {"E_rx_J": E_rx, "E_loss_link_J": E_loss_link,
                "E_dumped_J": E_dump, "eta_link": eta,
                "rails_agree": rails_agree, "rail_divergence": div,
                "accepted": accepted, "n_hops": int(n_hops),
                "physical_verdict_allowed": False}

    def spec(self) -> dict:
        return {"eta_hop": self.eta_hop,
                "rail_power_tolerance": RAIL_POWER_TOLERANCE,
                "marker": "[SIM] canal modelado; canal fisico [HARDWARE]",
                "physical_verdict_allowed": False}
