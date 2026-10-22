#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fidelidade a FONTE (somente leitura): rodar.py repete a logica de TGL_C3_validator_v52.py?
Compara a fonte importada (sem gravar bytecode) com as copias de rodar.py em:
  1. build_system (H, Pi, saltos) nas 9 configs x 5 sementes: igualdade exata dos bytes;
  2. lindblad_superoperator em alguns gamma: igualdade exata;
  3. observable_O contra test_M7_dimensional_folds['d_folds_c3'] em estados SINTETICOS (aleatorios e de posto baixo);
  4. nucleo por SVD contra o autovetor nulo da fonte (get_steady_state) em sistemas FORA da grade
     (sementes 7 e 8, gamma fora da grade): so as DIFERENCAS sao impressas, nunca O.
Nada aqui olha a pergunta (O na grade pre-registrada).
"""
import os
import sys
import hashlib
import importlib.util

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402
import rodar  # noqa: E402

SRC = r"C:\IALD\projetos_pyhton\acom\TGL_C3_validator_v52.py"
SHA_ESPERADO = "c3a53ef00dd4548d3b9315409acccea46a6e309080b26c8c556302eb00c70083"


def main():
    with open(SRC, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    print("fonte:", SRC)
    print("sha256 da fonte:", sha, "| confere com o mapa:", sha == SHA_ESPERADO)
    assert sha == SHA_ESPERADO

    spec = importlib.util.spec_from_file_location("fonte_v52", SRC)
    fonte = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fonte)

    # 1. sistema
    n = 0
    for (d, nc, eps) in rodar.CONFIGS:
        for seed in rodar.SEEDS:
            a = fonte.build_system(d, nc, eps, seed)
            b = rodar.build_system(d, nc, eps, seed)
            assert np.array_equal(a["H"], b["H"]) and np.array_equal(a["Pi"], b["Pi"])
            assert all(np.array_equal(x, y) for x, y in zip(a["L_ops"], b["L_ops"]))
            assert a["d"] == b["d"] and a["nc"] == b["nc"] and a["E_sc"] == b["E_sc"]
            n += 1
    print("1. build_system: %d sistemas identicos byte a byte (H, Pi, 4 saltos)" % n)

    # 2. superoperador
    n = 0
    for (d, nc, eps) in rodar.CONFIGS:
        sysd = rodar.build_system(d, nc, eps, 42)
        for g in (1.37e-3, 0.5):
            assert np.array_equal(fonte.lindblad_superoperator(sysd, g), rodar.lindblad_superoperator(sysd, g))
            n += 1
    print("2. lindblad_superoperator: %d casos identicos byte a byte" % n)

    # 3. observavel em estados sinteticos
    rng = np.random.default_rng(12345)
    pior = 0.0
    n = 0
    for d in (8, 10, 16, 24, 32):
        sysd = rodar.build_system(d, 2, 5.0, 42)
        for k in range(40):
            if k < 20:      # Hilbert-Schmidt
                G = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
                rho = G @ G.conj().T
            else:           # posto baixo
                r = int(rng.integers(1, d))
                G = rng.standard_normal((d, r)) + 1j * rng.standard_normal((d, r))
                rho = G @ G.conj().T
            rho = rho / np.real(np.trace(rho))
            rho = (rho + rho.conj().T) / 2
            ref = fonte.test_M7_dimensional_folds(rho, sysd)["d_folds_c3"]
            meu, _ = rodar.observable_O(rho)
            pior = max(pior, abs(ref - meu))
            n += 1
    print("3. observavel: %d estados sinteticos; maior |diferenca| = %.3e" % (n, pior))
    assert pior < 1e-12

    # 4. nucleo por SVD contra o autovetor nulo da fonte, fora da grade
    pior_rho = 0.0
    pior_O = 0.0
    n = 0
    for (d, nc) in ((8, 2), (16, 3), (24, 3)):
        for seed in (7, 8):
            sysd = rodar.build_system(d, nc, 5.0, seed)
            for g in (4.1e-4, 7.7e-3, 0.31):
                rho_f, _, _ = fonte.get_steady_state(sysd, g)
                ss = rodar.steady_state_kernel(sysd, g)
                assert ss["ok"]
                pior_rho = max(pior_rho, float(np.linalg.norm(rho_f - ss["rho"])))
                Of = fonte.test_M7_dimensional_folds(rho_f, sysd)["d_folds_c3"]
                Om, _ = rodar.observable_O(ss["rho"])
                pior_O = max(pior_O, abs(Of - Om))
                n += 1
    print("4. nucleo SVD vs autovetor nulo da fonte (fora da grade): %d casos; max ||drho||_F = %.3e; max |dO| = %.3e"
          % (n, pior_rho, pior_O))
    assert pior_rho < 1e-8 and pior_O < 1e-6

    print("\nFIDELIDADE OK")


if __name__ == "__main__":
    main()
