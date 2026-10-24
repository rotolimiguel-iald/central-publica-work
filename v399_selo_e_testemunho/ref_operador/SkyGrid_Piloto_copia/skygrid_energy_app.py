#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skygrid_energy_app.py — CLI do gemeo digital fisico-energetico (v3, ESTAGIO G).

Uso:
  python skygrid_energy_app.py twin  [--sats 12] [--bases 12] [--duration 120]
                                     [--faults dead,tamper,noise,meter]
                                     [--Q 1e4] [--eta-geo 0.8] [--sfield 100]
                                     [--f-drive MHZ] [--seed 11]
  python skygrid_energy_app.py scale                 # 144 x 48 (reivindicacao 2)
  python skygrid_energy_app.py sweeps [--fast]       # familias de curvas de projeto

Saidas: SKYGRID_ENERGY_MANIFEST.json + dashboard/data/energy_latest.json
        (+ energy_history.jsonl) e dashboard/data/energy_sweeps.json.

TUDO [SIM] sob hipoteses [CONJ]: o veredito maximo e' MODEL_CLOSES /
ENERGY_BALANCE_OK (o balanco fecha NO MODELO). physical_verdict_allowed=False.
Nao e' alegacao de energia fisica — o que resta e' a bancada.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from skygrid_physics.energy_twin import EnergyTwin      # noqa: E402
from skygrid_physics import sweeps as sweeps_mod        # noqa: E402

ROOT = os.path.abspath(os.path.dirname(__file__))
DASH = os.path.join(ROOT, "dashboard", "data")


def _series_thin(series, max_pts=600):
    n = len(series["t"])
    step = max(1, n // max_pts)
    return {k: v[::step] for k, v in series.items()}


def cmd_twin(args):
    faults = tuple(f for f in (args.faults or "").split(",") if f)
    bad = set(faults) - {"dead", "tamper", "noise", "meter"}
    if bad:
        raise SystemExit("falhas desconhecidas: %s" % ",".join(bad))
    kw = {}
    if args.f_drive:
        kw["f_drive_MHz"] = args.f_drive
    tw = EnergyTwin(n_sats=args.sats, n_bases=args.bases, seed=args.seed,
                    duration_s=args.duration, Q=args.Q, eta_geo=args.eta_geo,
                    S_field_W_m2=args.sfield, faults=faults, **kw)
    rep = tw.run()

    os.makedirs(DASH, exist_ok=True)
    blob = {"report": rep, "series": _series_thin(tw.series)}
    with open(os.path.join(ROOT, "SKYGRID_ENERGY_MANIFEST.json"), "w",
              encoding="utf-8") as f:
        json.dump(blob, f, indent=1, ensure_ascii=False, default=float)
    with open(os.path.join(DASH, "energy_latest.json"), "w",
              encoding="utf-8") as f:
        json.dump(blob, f, ensure_ascii=False, default=float)
    e, c, a = rep["energy"], rep["controls"], rep["audit"]
    hist = {"ts": rep["timestamp"], "verdict": rep["verdict"],
            "n_sats": rep["params"]["n_sats"],
            "P_delivered_W": e["P_delivered_mean_W"],
            "eta_sys": e["eta_sys"], "coverage": e["demand_coverage"],
            "residual_J": a["residual_J"], "seal": rep["seal_sha256"]}
    with open(os.path.join(DASH, "energy_history.jsonl"), "a",
              encoding="utf-8") as f:
        f.write(json.dumps(hist, ensure_ascii=False, default=float) + "\n")

    print("SkyGrid ENERGY TWIN  %d sats x %d bases  (%.0f s simulados, %.1f s wall)"
          % (rep["params"]["n_sats"], rep["params"]["n_bases"],
             rep["params"]["duration_s"], rep["elapsed_s"]))
    print("  [SIM sob hipoteses CONJ] — nada aqui e' medida fisica")
    print("  extraida  : %10.1f kJ   (debito explicito do reservatorio)"
          % (e["E_extracted_J"] / 1e3))
    print("  entregue  : %10.1f kJ   (P media %.1f kW; cobertura %.1f%%)"
          % (e["E_delivered_J"] / 1e3, e["P_delivered_mean_W"] / 1e3,
             100 * e["demand_coverage"]))
    print("  perdas    : %10.1f kJ   armazenada: %.1f kJ   meia-nat: %.2e J"
          % (e["E_losses_J"] / 1e3, e["E_stored_final_J"] / 1e3,
             e["E_halfnat_J"]))
    print("  eta_sys   : %10.4f     residuo do balanco: %.2e J (tol %.1e)"
          % (e["eta_sys"], a["residual_J"], a["tolerance_J"]))
    print("  placebo   : 0 W = %s     dados: %d rodadas, placebo rejeitado = %s"
          % (c["placebo_energy_zero"], c["data_rounds"],
             c["placebo_data_rejected_all_rounds"]))
    print("  falhas    : %s -> todas detectadas = %s"
          % (c["faults_injected"] or "nenhuma", c["faults_all_detected"]))
    print("  veredito  : %s   (fisico: PROIBIDO, physical_verdict_allowed=False)"
          % rep["verdict"])
    print("  selo      : %s" % rep["seal_sha256"])
    return 0 if rep["verdict"] == "MODEL_CLOSES" else 1


def cmd_sweeps(args):
    r = sweeps_mod.run_all(fast=args.fast)
    print("sweeps: %d familias | todos os pontos balancados: %s | %.1fs"
          % (len(r["sweeps"]), r["all_points_balanced"], r["elapsed_s"]))
    op = r["operating_point"]
    print("ponto de operacao: P=%.0f W (eta_sys=%.3f) [SIM]"
          % (op["P_delivered_W"], op["eta_sys"]))
    print("saida: dashboard/data/energy_sweeps.json")
    return 0 if r["all_points_balanced"] else 1


def main():
    ap = argparse.ArgumentParser(description="SkyGrid v3 — gemeo digital de energia [SIM]")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("twin", help="roda o gemeo digital end-to-end")
    p.add_argument("--sats", type=int, default=12)
    p.add_argument("--bases", type=int, default=12)
    p.add_argument("--duration", type=float, default=120.0)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--faults", default="")
    p.add_argument("--Q", type=float, default=1.0e4)
    p.add_argument("--eta-geo", dest="eta_geo", type=float, default=0.80)
    p.add_argument("--sfield", type=float, default=100.0)
    p.add_argument("--f-drive", dest="f_drive", type=float, default=None)
    p.set_defaults(fn=cmd_twin)

    p2 = sub.add_parser("scale", help="reivindicacao 2: 144 sats x 48 bases")
    p2.set_defaults(fn=cmd_twin, sats=144, bases=48, duration=60.0, seed=11,
                    faults="", Q=1.0e4, eta_geo=0.80, sfield=100.0,
                    f_drive=None)

    p3 = sub.add_parser("sweeps", help="familias de curvas de projeto")
    p3.add_argument("--fast", action="store_true")
    p3.set_defaults(fn=cmd_sweeps)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
