# -*- coding: utf-8 -*-
"""DURABILIDADE do pipeline do trabalhador (so hardware: operadores ALEATORIOS densos, nenhum da teoria), com os autovalores nao Hermitianos no MAGMA em TODO
tamanho: milhares de instancias seguidas cobrindo o que o rito chama em massa (eigvals, solve, matrix_exp, eigvalsh em lote, Choi, inv, eig + inv do T1).
Cada bloco num SUBPROCESSO que imprime o contador; uma queda nativa aparece como rc != 0 com o ultimo contador."""
import json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) > 1 and sys.argv[1] == "filho":
    import importlib.util
    sp = importlib.util.spec_from_file_location("w", os.path.join(HERE, "pilar_quantico_worker.py")); w = importlib.util.module_from_spec(sp); sp.loader.exec_module(w)
    import numpy as np, torch
    torch.use_deterministic_algorithms(True); torch.backends.cuda.matmul.allow_tf32 = False; torch.set_num_threads(4)
    E = w.Engine(torch, torch.device("cuda"), magma_up_to_n=10 ** 9)
    kind, d, reps = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    tol = {"tol0_rel": 1e-10, "gap_rel": 1e-8, "spohn_abs": 1e-10, "spohn_rel": 1e-9}
    rg = np.random.default_rng([77, d])
    for i in range(reps):
        A = rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d)); H = (A + A.conj().T) / 2
        Ls = [(rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d))) / d for _ in range(5)]
        if kind == "pipeline":
            Pi = np.zeros((d, d)); Pi[:2, :2] = np.eye(2)
            w.pipeline(E, H, Ls, d, Pi, tol, 0.05, 64, rg, want_nonreturn=(i % 10 == 0))
        else:
            S = E.superop(E.T(H), [E.T(L) for L in Ls]); Phi = E.propagator(S, 0.05); del S
            E.generator_from_propagator(Phi, 0.05, d); del Phi
        torch.cuda.synchronize()
        print(i + 1, flush=True)
    sys.exit(0)
res = {}
for kind, d, reps in (("pipeline", 8, 4000), ("pipeline", 16, 1500), ("t1", 8, 1500), ("t1", 16, 500), ("pipeline", 32, 150), ("t1", 32, 60)):
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "filho", kind, str(d), str(reps)], capture_output=True, text=True, timeout=7200)
    lines = r.stdout.strip().splitlines(); last = int(lines[-1]) if lines and lines[-1].strip().isdigit() else 0
    res["%s_d%d" % (kind, d)] = {"rc": r.returncode, "reps": reps, "ate": last, "s": round(time.time() - t0, 1), "erro": r.stderr.strip()[-400:] if r.returncode else ""}
    print(kind, d, res["%s_d%d" % (kind, d)], flush=True)
json.dump(res, open(os.path.join(HERE, "durabilidade_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
