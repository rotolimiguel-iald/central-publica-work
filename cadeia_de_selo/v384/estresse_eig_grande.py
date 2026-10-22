import json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estresse_eig.py")
res = {}
for fn, lib, n, reps in (("eigvals", "magma", 4096, 3), ("eig", "magma", 4096, 2), ("eigvals", "cusolver", 1024, 300), ("eig", "cusolver", 1024, 150),
                         ("eigvals", "cusolver", 4096, 40), ("eig", "cusolver", 4096, 12), ("eigvals", "magma", 1024, 300)):
    k = "%s_%s_%d" % (fn, lib, n); t0 = time.time()
    r = subprocess.run([sys.executable, F, "filho", fn, lib, str(n), str(reps)], capture_output=True, text=True, timeout=7200)
    out = (r.stdout.strip().splitlines() or [""])[-1]
    res[k] = {"rc": r.returncode, "reps": reps, "s": round(time.time() - t0, 1), "saida": out[:200]}
    print(k, r.returncode, out[:140], flush=True)
json.dump(res, open(os.path.join(os.path.dirname(F), "estresse_eig_grande.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
