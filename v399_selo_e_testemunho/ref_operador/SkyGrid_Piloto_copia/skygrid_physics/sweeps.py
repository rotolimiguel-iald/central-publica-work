#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweeps — ESTAGIO G2. Design-parameter sweeps of the energy twin [SIM].

Sweeps every declared design parameter and records the performance curve
(delivered power, eta_sys, balance residual) — no single magic number: the
model's predictions are FAMILIES of curves under [CONJ] hypotheses.

Also finds the OPERATING POINT (max delivered power at default demand) and
the LIMITS (where delivery degrades: off-resonance, low Q, depleted field).
Every sweep point re-audits conservation (fail-closed) — a sweep that breaks
the balance would abort the run.

Output: JSON (dashboard/data/energy_sweeps.json) consumed by visuals/dash.
"""

import json
import os
import sys
import tempfile
import time

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skygrid_physics.energy_twin import EnergyTwin       # noqa: E402
from skygrid_physics.coupling import OMEGA_OH_MHZ        # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "dashboard", "data")


def _run_point(**kw) -> dict:
    """One twin run in a throwaway state dir; returns the compact record."""
    defaults = dict(n_sats=6, n_bases=6, duration_s=40.0, dt_s=1.0,
                    data_reseal_every=20)
    defaults.update(kw)
    with tempfile.TemporaryDirectory() as td:
        tw = EnergyTwin(state_path=os.path.join(td, "s.json"), **defaults)
        rep = tw.run()                       # fail-closed audit inside
    e = rep["energy"]
    return {"P_delivered_W": e["P_delivered_mean_W"],
            "eta_sys": e["eta_sys"],
            "demand_coverage": e["demand_coverage"],
            "E_extracted_J": e["E_extracted_J"],
            "residual_J": rep["audit"]["residual_J"],
            "verdict": rep["verdict"]}


def sweep(param: str, values, **fixed) -> dict:
    pts = []
    for v in values:
        rec = _run_point(**{param: v}, **fixed)
        rec[param] = float(v)
        pts.append(rec)
    return {"param": param, "points": pts,
            "marker": "[SIM] curva de projeto sob hipoteses [CONJ]"}


def run_all(fast: bool = False) -> dict:
    n = 5 if fast else 9
    t0 = time.time()
    sweeps = {
        "Q": sweep("Q", np.logspace(2, 6, n)),
        "eta_geo": sweep("eta_geo", np.linspace(0.3, 0.95, n)),
        "S_field_W_m2": sweep("S_field_W_m2", np.logspace(0, 4, n)),
        "eta_rt": sweep("eta_rt", np.linspace(0.85, 0.99, n)),
        "f_drive_MHz": sweep("f_drive_MHz",
                             OMEGA_OH_MHZ * (1 + np.linspace(-3e-4, 3e-4, n))),
        "n_sats": sweep("n_sats", [3, 6, 12, 24, 48] if fast
                        else [3, 6, 12, 24, 48, 96, 144]),
    }
    # operating point: the best delivered power seen across sweeps
    best = max((p for s in sweeps.values() for p in s["points"]),
               key=lambda p: p["P_delivered_W"])
    # limits: where delivery collapses below 5% of best
    limits = {}
    for k, s in sweeps.items():
        dead = [p[k] for p in s["points"]
                if p["P_delivered_W"] < 0.05 * best["P_delivered_W"]]
        limits[k] = {"collapse_values": dead,
                     "note": "entrega <5% do melhor ponto"}
    out = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
           "sweeps": sweeps, "operating_point": best, "limits": limits,
           "all_points_balanced": all(
               p["verdict"] == "MODEL_CLOSES"
               for s in sweeps.values() for p in s["points"]),
           "elapsed_s": time.time() - t0,
           "marker": "[SIM] familia de curvas; hipoteses [CONJ]; resta a bancada",
           "physical_verdict_allowed": False}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "energy_sweeps.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=float)
    return out


if __name__ == "__main__":
    fast = "--fast" in sys.argv
    r = run_all(fast=fast)
    print("sweeps: %d familias | todos os pontos balancados: %s | %.1fs" %
          (len(r["sweeps"]), r["all_points_balanced"], r["elapsed_s"]))
    op = r["operating_point"]
    print("ponto de operacao: P=%.0f W (eta_sys=%.3f)" %
          (op["P_delivered_W"], op["eta_sys"]))
