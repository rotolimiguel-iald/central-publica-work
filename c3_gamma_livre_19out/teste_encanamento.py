#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do ENCANAMENTO (leitura/escrita) de rodar.py e veredito.py num sistema de brinquedo (d = 6, nc = 2,
sementes 1 e 2, 3 gammas) em subpasta propria. NAO e a grade pre-registrada e nao informa a pergunta:
so confere que run_grid, run_N1, run_N3 escrevem e que veredito.load_rows/load_n1 leem o que foi escrito.
"""
import os
import sys
import json

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import rodar  # noqa: E402
import veredito  # noqa: E402


def main():
    out = os.path.join(HERE, "encanamento_teste")
    os.makedirs(out, exist_ok=True)
    rodar.CONFIGS = [(6, 2, 5.0), (8, 2, 5.0)]
    rodar.SEEDS = [1, 2]
    rodar.GAMMAS = np.logspace(-4.0, 0.0, 3)
    rodar.N1_STATES = 7

    logs = []
    n, bad = rodar.run_grid("main", lambda base, seed: base, os.path.join(out, "main.csv"), os.path.join(out, "main.npz"),
                            logs.append)
    n2, bad2 = rodar.run_grid("N2", rodar.make_random_jump_system, os.path.join(out, "N2.csv"),
                              os.path.join(out, "N2.npz"), logs.append)
    rodar.run_N1(os.path.join(out, "N1.csv"))
    n3 = rodar.run_N3()
    with open(os.path.join(out, "N3.json"), "w", encoding="utf-8") as f:
        json.dump(n3, f)

    assert n == 2 * 2 * 3 and n2 == n
    rows = veredito.load_rows(os.path.join(out, "main.csv"))
    rows2 = veredito.load_rows(os.path.join(out, "N2.csv"))
    n1 = veredito.load_n1(os.path.join(out, "N1.csv"))
    assert len(rows) == n and len(rows2) == n and len(n1) == 7 * 2
    z = np.load(os.path.join(out, "main.npz"))
    assert len(z.files) == n - bad
    print("encanamento OK: %d pontos principais (%d sem convergir), %d de N2 (%d), %d estados N1, %d casos N3"
          % (n, bad, n2, bad2, len(n1), len(n3["casos"])))
    print("log:", logs[-1])


if __name__ == "__main__":
    main()
