#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
energy_twin — ESTAGIO G. The SkyGrid energy digital twin [SIM].

Integrates F1-F6 into an end-to-end power flow COUPLED to the v2 data plane:

  reservoir -> OH coupling -> dipole conversion -> Psi link (double rail)
            -> reversal-cell storage -> load dispatch (demand profile)

TWO PLANES, ONE VERDICT: each satellite's energy windows are gated by the
DATA plane of the v2 orchestrator (ACOM crypto + double rail + Proof-of-Phase
quorum). A satellite whose data transfer is rejected has its energy windows
DUMPED (accounted loss) until it re-seals. The PLACEBO satellite (claim 3,
no beta coupling) extracts and delivers exactly 0 W by construction.

Load model: deterministic daily-like demand profile per base + dispatch
priority (direct power first, then storage discharge).

Verdict: MODEL_CLOSES iff the global energy balance audits (thermo.py,
fail-closed), placebo == 0, every fault is detected, eta_sys in [0,1] and
the data plane closes. physical_verdict_allowed = False, always: this is a
predictive model under [CONJ] hypotheses — the bench remains.
"""

import hashlib
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skygrid_sim import tgl_core                                  # noqa: E402
from skygrid_sim.orchestrator import SkyGridOrchestrator          # noqa: E402
from skygrid_physics.field_reservoir import FieldReservoir        # noqa: E402
from skygrid_physics.coupling import ResonantCoupler              # noqa: E402
from skygrid_physics.conversion import DipoloConverter            # noqa: E402
from skygrid_physics.transmission import PsiPowerLink             # noqa: E402
from skygrid_physics.storage import ReversalCellStore             # noqa: E402
from skygrid_physics.thermo import EnergyLedger                   # noqa: E402


class LoadProfile:
    """Deterministic demand P_load(t) [W] per base (daily-like, seeded)."""

    def __init__(self, base_index: int, P_peak_W: float = 900.0,
                 period_s: float = 3600.0):
        self.P_peak = float(P_peak_W)
        self.period = float(period_s)
        self.phase = 2 * math.pi * (base_index % 7) / 7.0

    def demand(self, t: float) -> float:
        s = 0.55 + 0.45 * math.sin(2 * math.pi * t / self.period + self.phase)
        return self.P_peak * max(0.05, s)


class EnergyTwin:
    """The integrated digital twin (data plane v2 + energy plane v3)."""

    def __init__(self, n_sats: int = 12, n_bases: int = 12, seed: int = 11,
                 duration_s: float = 120.0, dt_s: float = 1.0,
                 data_reseal_every: int = 10,
                 S_field_W_m2: float = 100.0, A_cap_m2: float = 10.0,
                 Q: float = 1.0e4, eta_geo: float = 0.80,
                 eta_conv: float = 0.92, eta_hop: float = 0.985,
                 eta_rt: float = 0.95, T_kelvin: float = 300.0,
                 f_drive_MHz: float = None,
                 faults=(), state_path: str = None):
        self.params = dict(n_sats=n_sats, n_bases=n_bases, seed=seed,
                           duration_s=duration_s, dt_s=dt_s,
                           S_field_W_m2=S_field_W_m2, A_cap_m2=A_cap_m2,
                           Q=Q, eta_geo=eta_geo, eta_conv=eta_conv,
                           eta_hop=eta_hop, eta_rt=eta_rt, T_kelvin=T_kelvin,
                           f_drive_MHz=f_drive_MHz, faults=list(faults))
        self.beta = tgl_core.beta()
        self.dt = float(dt_s)
        self.n_steps = int(round(duration_s / dt_s))
        self.data_reseal_every = int(data_reseal_every)
        self.faults = tuple(sorted(set(faults)))

        # data plane: the FULL v2 orchestrator (crypto+rail+quorum+kernel+memory)
        self.orch = SkyGridOrchestrator(
            n_sats=n_sats, n_bases=n_bases, seed=seed, faults=self.faults,
            state_path=state_path)

        # energy plane per satellite
        f_dr = f_drive_MHz
        self.reservoirs = [FieldReservoir(S_field_W_m2, A_cap_m2,
                                          seed=seed * 100 + i)
                           for i in range(n_sats)]
        self.couplers = [ResonantCoupler(Q=Q, eta_geo=eta_geo,
                                         T_kelvin=T_kelvin,
                                         **({"f_drive_MHz": f_dr} if f_dr else {}))
                         for _ in range(n_sats)]
        self.converters = [DipoloConverter(eta_conv=eta_conv, seed=seed * 7 + i)
                           for i in range(n_sats)]
        self.link = PsiPowerLink(eta_hop=eta_hop)
        self.stores = [ReversalCellStore(eta_rt=eta_rt)
                       for _ in range(n_bases)]
        self.loads = [LoadProfile(i) for i in range(n_bases)]
        # placebo energy chain (claim 3): coupler with NO beta coupling
        self.placebo_reservoir = FieldReservoir(S_field_W_m2, A_cap_m2,
                                                seed=seed ^ 0xC0FFEE)
        self.placebo_coupler = ResonantCoupler(Q=Q, eta_geo=eta_geo,
                                               T_kelvin=T_kelvin)

        self.ledger = EnergyLedger(T_kelvin=T_kelvin)
        self.series = {k: [] for k in
                       ("t", "P_avail", "P_in", "P_conv", "P_rx",
                        "P_demand", "P_delivered", "soc_total",
                        "placebo_P")}
        self.data_rounds = []
        self.hops = {}

    # ---- data plane gate --------------------------------------------------------
    def _run_data_round(self) -> dict:
        """One full v2 data round; returns accepted flag per satellite id."""
        self.orch.transfers = []
        self.orch.fault_events = []
        rep = None
        accepted = {}
        results = []
        for i, sat in enumerate(self.orch.sats):
            base = self.orch.bases[i % len(self.orch.bases)]
            if not sat.alive:
                accepted[i] = False
                continue
            inject = None
            if "tamper" in self.faults and i == 2:
                inject = "tamper"
            elif "noise" in self.faults and i == 3:
                inject = "noise"
            r = self.orch.transfer_full(sat, base, inject=inject)
            accepted[i] = bool(r["accepted"])
            results.append(r)
            self.hops[i] = r.get("hops", 1)
        placebo = self.orch.placebo_transfer(
            next(s for s in self.orch.sats if s.alive), self.orch.bases[0])
        self.data_rounds.append({
            "accepted": accepted, "placebo_rejected": not placebo["accepted"]})
        return accepted

    # ---- main run ------------------------------------------------------------------
    def run(self) -> dict:
        t_start = time.perf_counter()
        if "dead" in self.faults and len(self.orch.sats) > 1:
            self.orch.sats[1].alive = False
        gate = self._run_data_round()
        n_b = len(self.stores)

        for step in range(self.n_steps):
            t = step * self.dt
            if step > 0 and step % self.data_reseal_every == 0:
                gate = self._run_data_round()

            P_avail_sum = P_in_sum = P_conv_sum = P_rx_sum = 0.0
            E_rx_by_base = [0.0] * n_b

            for i in range(len(self.orch.sats)):
                res, cpl, cnv = self.reservoirs[i], self.couplers[i], self.converters[i]
                alive = self.orch.sats[i].alive
                P_avail_sum += res.power_available() if alive else 0.0
                if not alive:
                    res.idle(self.dt)
                    continue
                w = cpl.couple(res, self.dt)
                self.ledger.add(E_extracted=w["E_in_J"] + w["E_halfnat_J"],
                                E_halfnat=w["E_halfnat_J"], acts=w["acts"])
                c = cnv.convert(w["E_in_J"])
                self.ledger.add(E_loss_conversion=c["E_loss_conv_J"],
                                E_refused_conv=c["E_refused_J"])
                data_ok = gate.get(i, False)
                dist = 0.0
                if "meter" in self.faults and i == 4:
                    dist = 0.01          # meter divergence fault (window dumped)
                tx = self.link.transmit(c["E_out_J"], self.hops.get(i, 1),
                                        rail_data_accepted=data_ok,
                                        meter_disturbance=dist)
                self.ledger.add(E_loss_link=tx["E_loss_link_J"],
                                E_dumped=tx["E_dumped_J"])
                bi = i % n_b
                E_rx_by_base[bi] += tx["E_rx_J"]
                P_in_sum += w["E_in_J"] / self.dt
                P_conv_sum += c["E_out_J"] / self.dt
                P_rx_sum += tx["E_rx_J"] / self.dt

            # placebo chain: MUST stay at exactly zero
            wp = self.placebo_coupler.couple(self.placebo_reservoir, self.dt,
                                             placebo=True)
            placebo_P = wp["E_in_J"] / self.dt

            # bases: charge then dispatch against demand
            P_del_sum = P_dem_sum = 0.0
            for b in range(n_b):
                st, ld = self.stores[b], self.loads[b]
                E_rx = E_rx_by_base[b]
                P_dem = ld.demand(t)
                E_dem = P_dem * self.dt
                # direct dispatch first, then storage
                E_direct = min(E_rx, E_dem)
                E_to_store = E_rx - E_direct
                ch = st.charge(E_to_store)
                self.ledger.add(E_loss_charge=ch["E_loss_charge_J"],
                                E_refused_store=ch["E_refused_J"])
                E_need = E_dem - E_direct
                dis = st.discharge(E_need)
                self.ledger.add(E_loss_discharge=dis["E_loss_discharge_J"])
                E_del = E_direct + dis["E_delivered_J"]
                self.ledger.add(E_delivered=E_del)
                st.step(self.dt)
                P_del_sum += E_del / self.dt
                P_dem_sum += P_dem

            s = self.series
            s["t"].append(t)
            s["P_avail"].append(P_avail_sum)
            s["P_in"].append(P_in_sum)
            s["P_conv"].append(P_conv_sum)
            s["P_rx"].append(P_rx_sum)
            s["P_demand"].append(P_dem_sum)
            s["P_delivered"].append(P_del_sum)
            s["soc_total"].append(sum(st.soc_J for st in self.stores))
            s["placebo_P"].append(placebo_P)

        # close the books: leakage + stored delta enter the balance
        for st in self.stores:
            self.ledger.add(E_leak=st.E_leak_J, dE_stored=st.soc_J)
        audit = self.ledger.audit()               # fail-closed (raises on break)

        placebo_zero = all(p == 0.0 for p in self.series["placebo_P"]) \
            and self.placebo_reservoir.energy_debited_J == 0.0
        data_ok_frac = (np.mean([all(r["accepted"].get(i, False)
                                     for i in r["accepted"]
                                     if self.orch.sats[i].alive
                                     and not self._is_faulted_sat(i))
                                 for r in self.data_rounds])
                        if self.data_rounds else 0.0)
        placebo_data_ok = all(r["placebo_rejected"] for r in self.data_rounds)
        faults_detected = all(ev["detected"] for ev in self.orch.fault_events) \
            if self.orch.fault_events else True

        verdict_ok = (audit["balance"] == "ENERGY_BALANCE_OK"
                      and placebo_zero and placebo_data_ok
                      and 0.0 <= audit["eta_sys"] <= 1.0
                      and faults_detected and data_ok_frac == 1.0)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "marker": "[SIM] gemeo digital sob hipoteses [CONJ]; resta a bancada",
            "beta_runtime": self.beta,
            "params": self.params,
            "coupler_spec": self.couplers[0].spec(),
            "audit": audit,
            "energy": {
                "E_extracted_J": audit["E_extracted_J"],
                "E_delivered_J": audit["E_delivered_J"],
                "E_losses_J": audit["E_losses_J"],
                "E_halfnat_J": audit["E_halfnat_J"],
                "E_stored_final_J": audit["dE_stored_J"],
                "eta_sys": audit["eta_sys"],
                "P_delivered_mean_W": float(np.mean(self.series["P_delivered"])),
                "P_demand_mean_W": float(np.mean(self.series["P_demand"])),
                "demand_coverage": float(
                    sum(self.series["P_delivered"]) /
                    max(sum(self.series["P_demand"]), 1e-30)),
            },
            "controls": {
                "placebo_energy_zero": bool(placebo_zero),
                "placebo_data_rejected_all_rounds": bool(placebo_data_ok),
                "data_rounds": len(self.data_rounds),
                "data_plane_healthy_accept_frac": float(data_ok_frac),
                "faults_injected": list(self.faults),
                "faults_all_detected": bool(faults_detected),
            },
            "physical_verdict_allowed": False,
            "verdict": "MODEL_CLOSES" if verdict_ok else "OPEN",
            "elapsed_s": time.perf_counter() - t_start,
        }
        report["seal_sha256"] = hashlib.sha256(
            json.dumps(report, sort_keys=True, default=str).encode()).hexdigest()
        self.report = report
        return report

    def _is_faulted_sat(self, i: int) -> bool:
        return (("tamper" in self.faults and i == 2)
                or ("noise" in self.faults and i == 3))
