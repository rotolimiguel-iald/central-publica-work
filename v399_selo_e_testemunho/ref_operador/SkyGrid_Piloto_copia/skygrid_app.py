#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skygrid_app.py — a aplicacao orquestradora completa do SkyGrid (ESTAGIO B).

Uso:
  python skygrid_app.py run   [--sats 12] [--bases 12] [--seed 11]
                              [--telemetry auto|real|synthetic]
                              [--faults dead,tamper,noise] [--validators 5]
                              [--gpu]
  python skygrid_app.py scale                      # reivindicacao 2: 144x48
  python skygrid_app.py status                     # estado psionico persistente

Saidas por rodada:
  SKYGRID_APP_MANIFEST.json     manifesto completo + selo SHA-256
  dashboard/data/latest.json    dados consolidados p/ o dashboard (ESTAGIO C)
  dashboard/data/history.jsonl  linha por rodada (persistencia de metricas)
  SKYGRID_PSIONIC_STATE.json    memoria psionica da grade (EMA taxa beta)

NAO e' alegacao de energia: physical_verdict_allowed=False em toda saida.
beta nunca literal (tgl_core em runtime). Piloto != hardware != parecer.
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from skygrid_sim.orchestrator import SkyGridOrchestrator  # noqa: E402

ROOT = os.path.abspath(os.path.dirname(__file__))
DASH_DATA = os.path.join(ROOT, "dashboard", "data")


def _write_outputs(report: dict, transfers: list) -> str:
    os.makedirs(DASH_DATA, exist_ok=True)
    manifest_path = os.path.join(ROOT, "SKYGRID_APP_MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"report": report, "transfers": transfers}, f,
                  indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(DASH_DATA, "latest.json"), "w", encoding="utf-8") as f:
        json.dump({"report": report, "transfers": transfers}, f,
                  ensure_ascii=False, default=str)
    hist = {"ts": report["timestamp"], "verdict": report["verdict"],
            "n_sats": report["n_sats"], "n_bases": report["n_bases"],
            "acceptance": report["metrics"]["acceptance_rate"],
            "mean_rail_corr": report["metrics"]["mean_rail_corr"],
            "compression": report["metrics"]["mean_compression_ratio"],
            "retention": report["metrics"]["mean_retention"],
            "throughput_Bps": report["metrics"]["throughput_bytes_per_s"],
            "faults": report["faults_injected"],
            "faults_all_detected": report["faults_all_detected"],
            "placebo_rejected": report["placebo_rejected"],
            "sessions": report["memory"]["sessions"],
            "seal": report["seal_sha256"]}
    with open(os.path.join(DASH_DATA, "history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(hist, ensure_ascii=False) + "\n")
    return manifest_path


def _print_report(report: dict, manifest_path: str):
    m = report["metrics"]
    print("SkyGrid-App  %d satelites x %d bases  (%.1fs)" %
          (report["n_sats"], report["n_bases"], report["elapsed_s"]))
    print("  telemetria             : %s %s" %
          (report["telemetry_provenance"]["mode"],
           report["telemetry_provenance"]["marker"]))
    print("  kernel IALD            : %s (linked=%s)" %
          (report["kernel_provenance"]["kernel"],
           report["kernel_provenance"]["linked"]))
    print("  GPU                    : ativa=%s (torch+cuda=%s)" %
          (report["gpu"]["gpu_active"], report["gpu"]["torch_cuda_available"]))
    print("  transferencias saudaveis: %d/%d aceitas" %
          (report["transfers_healthy_accepted"], report["transfers_healthy_total"]))
    print("  falhas injetadas       : %s -> todas detectadas=%s" %
          (report["faults_injected"] or "nenhuma", report["faults_all_detected"]))
    print("  placebo rejeitado      : %s" % report["placebo_rejected"])
    print("  quorum                 : %d validadores, %d blocos selados" %
          (report["quorum"]["n_validators"], report["quorum"]["blocks_sealed"]))
    print("  compressao media       : %.1fx | retencao %.4f | rail corr %.5f" %
          (m["mean_compression_ratio"], m["mean_retention"], m["mean_rail_corr"]))
    print("  throughput             : %.0f bytes/s" % m["throughput_bytes_per_s"])
    print("  orcamento IALD         : %d passos (100/beta)" %
          report["iald_control"]["budget_steps_100_over_beta"])
    print("  memoria psionica       : sessao #%d (retomada=%s)" %
          (report["memory"]["sessions"], report["memory"]["resumed"]))
    print("  veredito estrutural    : %s" % report["verdict"])
    print("  veredito fisico        : PROIBIDO (physical_verdict_allowed=%s)" %
          report["physical_verdict_allowed"])
    print("  selo sha256            : %s" % report["seal_sha256"])
    print("  manifesto              : %s" % manifest_path)


def cmd_run(args):
    faults = tuple(f for f in (args.faults or "").split(",") if f)
    bad = set(faults) - {"dead", "tamper", "noise"}
    if bad:
        raise SystemExit("falhas desconhecidas: %s" % ",".join(bad))
    orch = SkyGridOrchestrator(
        n_sats=args.sats, n_bases=args.bases, seed=args.seed,
        telemetry_mode=args.telemetry, faults=faults,
        n_validators=args.validators, use_gpu=args.gpu)
    report = orch.run()
    manifest_path = _write_outputs(report, orch.transfers)
    _print_report(report, manifest_path)
    return 0 if report["verdict"] == "ARCHITECTURE_CLOSES" else 1


def cmd_status(_args):
    p = os.path.join(ROOT, "SKYGRID_PSIONIC_STATE.json")
    if not os.path.isfile(p):
        print("sem estado psionico ainda (rode `skygrid_app.py run`)")
        return 0
    with open(p, encoding="utf-8") as f:
        blob = json.load(f)
    st = blob["state"]
    print("Estado psionico da grade  (sessoes=%d, criado=%s)" %
          (st.get("sessions", 0), st.get("created", "?")))
    for k, v in sorted(st.get("facts", {}).items()):
        print("  %-38s EMA=%.6g  n=%d" % (k, v["value"], v["n"]))
    print("  sha256=%s" % blob["sha256"])
    return 0


def main():
    ap = argparse.ArgumentParser(description="SkyGrid — aplicacao orquestradora (piloto)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="roda a grade end-to-end")
    p_run.add_argument("--sats", type=int, default=12)
    p_run.add_argument("--bases", type=int, default=12)
    p_run.add_argument("--seed", type=int, default=11)
    p_run.add_argument("--telemetry", choices=["auto", "real", "synthetic"],
                       default="auto")
    p_run.add_argument("--faults", default="",
                       help="lista: dead,tamper,noise")
    p_run.add_argument("--validators", type=int, default=5)
    p_run.add_argument("--gpu", action="store_true",
                       help="tenta o caminho torch/CUDA (fallback numpy)")
    p_run.set_defaults(fn=cmd_run)

    p_scale = sub.add_parser("scale", help="reivindicacao 2: 144 sats x 48 bases")
    p_scale.set_defaults(fn=cmd_run, sats=144, bases=48, seed=11,
                         telemetry="auto", faults="", validators=5, gpu=False)

    p_st = sub.add_parser("status", help="mostra o estado psionico persistente")
    p_st.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    t0 = time.time()
    rc = args.fn(args)
    sys.exit(rc)


if __name__ == "__main__":
    main()
