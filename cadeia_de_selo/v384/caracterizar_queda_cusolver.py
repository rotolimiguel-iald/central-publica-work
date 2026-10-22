# -*- coding: utf-8 -*-
"""Caracteriza a queda do cuSOLVER (so hardware: matrizes ALEATORIAS): para cada n, ate quantas chamadas de eigvals o processo sobrevive. Cada n num subprocesso que
imprime o contador a cada chamada (flush); a ultima linha impressa antes da queda diz em que chamada caiu. Faixa: os tamanhos de superoperador d^2 de d = 4 a 32."""
import json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
if len(sys.argv) > 1 and sys.argv[1] == "filho":
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    import numpy as np, torch
    n, reps, lib = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    torch.use_deterministic_algorithms(True); torch.set_num_threads(4)
    torch.backends.cuda.preferred_linalg_library(lib)
    rg = np.random.default_rng(1000 + n)
    for i in range(reps):
        A = torch.as_tensor(rg.standard_normal((n, n)) + 1j * rg.standard_normal((n, n)), dtype=torch.complex128, device="cuda")
        torch.linalg.eigvals(A); torch.cuda.synchronize()
        print(i + 1, flush=True)
    sys.exit(0)
res = {}
for lib in ("cusolver", "magma"):
    for n, reps in ((16, 3000), (36, 3000), (64, 3000), (100, 2000), (144, 2000), (196, 1500), (256, 1000), (400, 600), (576, 400)):
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "filho", str(n), str(reps), lib], capture_output=True, text=True, timeout=3600)
        lines = r.stdout.strip().splitlines()
        last = int(lines[-1]) if lines and lines[-1].strip().isdigit() else 0
        res["%s_%d" % (lib, n)] = {"rc": r.returncode, "reps": reps, "sobreviveu_ate": last, "caiu": r.returncode != 0, "s": round(time.time() - t0, 1)}
        print(lib, n, res["%s_%d" % (lib, n)], flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "caracterizar_queda_cusolver.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
