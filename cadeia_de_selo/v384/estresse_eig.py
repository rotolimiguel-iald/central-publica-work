# -*- coding: utf-8 -*-
"""Estresse do autovalor nao Hermitiano na GPU (so hardware: matrizes ALEATORIAS). Cada caso roda num SUBPROCESSO (uma queda nativa nao derruba o teste).
Casos: funcao (eig com vetores | eigvals) x biblioteca preferida (padrao | cusolver | magma) x n (64, 256, 1024). Mede quedas e tempo."""
import json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
if len(sys.argv) > 1 and sys.argv[1] == "filho":
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ.setdefault(k, "4")
    import numpy as np, torch
    fn, lib, n, reps = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    torch.use_deterministic_algorithms(True); torch.set_num_threads(4)
    if lib != "padrao":
        torch.backends.cuda.preferred_linalg_library(lib)
    rg = np.random.default_rng(n)
    t0 = time.time()
    for i in range(reps):
        A = torch.as_tensor(rg.standard_normal((n, n)) + 1j * rg.standard_normal((n, n)), dtype=torch.complex128, device="cuda")
        if fn == "eig":
            lam, V = torch.linalg.eig(A)
        else:
            lam = torch.linalg.eigvals(A)
        torch.cuda.synchronize()
    print(json.dumps({"ok": True, "s_por_chamada": (time.time() - t0) / reps, "lib_efetiva": str(torch.backends.cuda.preferred_linalg_library())}))
    sys.exit(0)
res = {}
for fn in ("eig", "eigvals"):
    for lib in ("padrao", "cusolver", "magma"):
        for n, reps in ((64, 1500), (256, 150), (1024, 8)):
            k = "%s_%s_%d" % (fn, lib, n)
            t0 = time.time()
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "filho", fn, lib, str(n), str(reps)], capture_output=True, text=True, timeout=1800)
            out = (r.stdout.strip().splitlines() or [""])[-1]
            res[k] = {"rc": r.returncode, "reps": reps, "s": round(time.time() - t0, 1), "saida": out[:200], "erro": r.stderr.strip()[-300:] if r.returncode else ""}
            print(k, res[k]["rc"], res[k]["saida"][:120], flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "estresse_eig.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
