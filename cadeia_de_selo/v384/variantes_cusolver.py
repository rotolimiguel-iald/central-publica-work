# -*- coding: utf-8 -*-
"""A queda do cuSOLVER (eigvals, n = 36, onde cai em ~200 chamadas) some com alguma condicao simples? So hardware: matrizes ALEATORIAS. Cada variante num subprocesso,
3 repeticoes de 3000 chamadas; registra em que chamada caiu. Variantes: base (deterministico, como no trabalhador); sem determinismo; CUDA_LAUNCH_BLOCKING=1;
empty_cache + synchronize antes de cada chamada; uma copia contigua nova a cada chamada; a matriz criada na CPU e copiada (sem as_tensor direto)."""
import json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
if len(sys.argv) > 1 and sys.argv[1] == "filho":
    var, n, reps, seed = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    import numpy as np, torch
    if var != "sem_determinismo":
        torch.use_deterministic_algorithms(True)
    torch.set_num_threads(4)
    torch.backends.cuda.preferred_linalg_library("cusolver")
    rg = np.random.default_rng(seed)
    for i in range(reps):
        A = torch.as_tensor(rg.standard_normal((n, n)) + 1j * rg.standard_normal((n, n)), dtype=torch.complex128, device="cuda")
        if var == "empty_cache_sync":
            torch.cuda.synchronize(); torch.cuda.empty_cache()
        if var == "copia_contigua":
            A = A.clone().contiguous()
        torch.linalg.eigvals(A); torch.cuda.synchronize()
        print(i + 1, flush=True)
    sys.exit(0)
res = {}
for var in ("base", "sem_determinismo", "launch_blocking", "empty_cache_sync", "copia_contigua"):
    out = []
    for seed in (1, 2, 3):
        env = dict(os.environ)
        if var == "launch_blocking":
            env["CUDA_LAUNCH_BLOCKING"] = "1"
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "filho", var, "36", "3000", str(seed)], capture_output=True, text=True, timeout=1800, env=env)
        lines = r.stdout.strip().splitlines(); last = int(lines[-1]) if lines and lines[-1].strip().isdigit() else 0
        out.append({"seed": seed, "rc": r.returncode, "ate": last})
    res[var] = out
    print(var, out, flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "variantes_cusolver.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
