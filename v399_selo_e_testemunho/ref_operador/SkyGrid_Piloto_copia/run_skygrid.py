#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_skygrid.py — executa uma rodada do grafo SkyGrid-Sim e grava o manifesto+selo.

Uso:  python run_skygrid.py [n_sats] [n_bases]
Ex.:  python run_skygrid.py 12 12
      python run_skygrid.py 144 48     (topologia da reivindicacao 2 — mais lento)

NAO e' alegacao de energia. Simula a arquitetura da patente SkyGrid como grafo
distribuido de software; valida cada transferencia por duplo trilho + placebo.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from skygrid_sim import skygrid  # noqa: E402


def main():
    n_sats = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    n_bases = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    sim = skygrid.SkyGridSim(n_sats=n_sats, n_bases=n_bases, seed=11)
    rep = sim.run()
    out = os.path.join(os.path.dirname(__file__), "SKYGRID_RUN_MANIFEST.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"report": rep, "transfers": sim.transfers}, f,
                  indent=2, ensure_ascii=False)
    print("SkyGrid-Sim  %d satelites x %d bases" % (n_sats, n_bases))
    print("  transferencias aceitas : %d/%d" % (rep["transfers_accepted"], rep["transfers_total"]))
    print("  placebo rejeitado      : %s" % rep["placebo_rejected"])
    print("  cadeia de fase (blocos): %d" % rep["chain_length"])
    print("  veredito estrutural    : %s" % rep["verdict"])
    print("  veredito fisico        : PROIBIDO (physical_verdict_allowed=%s)"
          % rep["physical_verdict_allowed"])
    print("  selo sha256            : %s" % rep["seal_sha256"])
    print("  manifesto              : %s" % out)


if __name__ == "__main__":
    main()
