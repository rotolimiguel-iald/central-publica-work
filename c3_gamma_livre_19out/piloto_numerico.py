#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piloto NUMERICO (antes do pre-registro): so a qualidade do nucleo do liouvilliano em sementes que NAO
estao na grade (7 e 8). Imprime apenas diagnosticos numericos (valores singulares, erros, tempo).
NAO imprime O, nem pesos, nem autovalores do estado: nenhum resultado da pergunta e olhado aqui.
"""
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rodar  # noqa: E402


def main():
    print("seed d nc gamma | s1_rel s2_rel herm trace_err tp_err_rel psd_min lu_diff | ok reason | t_s")
    for (d, nc) in ((8, 2), (16, 3), (32, 4)):
        for seed in (7, 8):
            base = rodar.build_system(d, nc, 5.0, seed)
            for g in (1e-4, 3e-3, 1.0):
                t0 = time.time()
                ss = rodar.steady_state_kernel(base, g)
                print("%d %d %d %.0e | %.2e %.2e %.2e %.2e %.2e %+.2e %.2e | %s %s | %.2f" %
                      (seed, d, nc, g, ss["s1_rel"], ss["s2_rel"], ss["herm"], ss["trace_err"],
                       ss["tp_err_rel"], ss["psd_min"], ss["lu_diff"], ss["ok"], ss["reason"] or "-",
                       time.time() - t0))
    print("\nN2 (saltos aleatorios), mesma checagem numerica, semente 7:")
    for (d, nc) in ((8, 2), (32, 4)):
        base = rodar.build_system(d, nc, 5.0, 7)
        rnd = rodar.make_random_jump_system(base, 7)
        for g in (1e-4, 1.0):
            t0 = time.time()
            ss = rodar.steady_state_kernel(rnd, g)
            print("7 %d %d %.0e | %.2e %.2e %.2e %.2e %.2e %+.2e %.2e | %s %s | %.2f" %
                  (d, nc, g, ss["s1_rel"], ss["s2_rel"], ss["herm"], ss["trace_err"],
                   ss["tp_err_rel"], ss["psd_min"], ss["lu_diff"], ss["ok"], ss["reason"] or "-",
                   time.time() - t0))


if __name__ == "__main__":
    main()
