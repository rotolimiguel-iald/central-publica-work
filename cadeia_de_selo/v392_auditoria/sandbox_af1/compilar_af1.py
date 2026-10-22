# -*- coding: utf-8 -*-
"""Auditor cetico c1 (v392): compila Posto.lean e PostoAdendo.lean e as sondas num sandbox curto (C:/t/af1).
LEAN_PATH so-leitura ao .lake do Nos; saidas so em C:/t/af1/out. Nao toca o Nos."""
import hashlib, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
AF = "C:/t/af1"
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel"
LEAN = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe")
libs = [AF + "/out", K + "/.lake/build/lib/lean"]
for p in sorted(os.listdir(K + "/.lake/packages")):
    d = K + "/.lake/packages/" + p + "/.lake/build/lib/lean"
    if os.path.isdir(d):
        libs.append(d)
env = dict(os.environ); env["LEAN_PATH"] = ";".join(libs)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
res = {"lean": LEAN, "lean_path": libs, "passos": []}


def run(src, olean=None):
    cmd = [LEAN]
    if olean:
        os.makedirs(os.path.dirname(olean), exist_ok=True)
        cmd += ["-o", olean, "-i", olean[:-6] + ".ilean"]
    cmd.append(src)
    t0 = time.time()
    pr = subprocess.run(cmd, env=env, capture_output=True, timeout=3000, cwd=AF)
    out = (pr.stdout + pr.stderr).decode("utf-8", "replace")
    logp = AF + "/" + os.path.basename(src) + ".log"
    open(logp, "w", encoding="utf-8").write(out)
    r = {"src": src, "src_sha256": sha(src), "rc": pr.returncode, "segundos": round(time.time() - t0, 1), "log": logp, "log_sha256": sha(logp),
         "n_error": out.count("error:"), "n_warning": out.count("warning:"),
         "sorry_crase": "declaration uses `sorry`" in out, "sorry_aspas": "declaration uses 'sorry'" in out, "sorryAx": "sorryAx" in out}
    if olean and os.path.exists(olean):
        r["olean_sha256"] = sha(olean)
    res["passos"].append(r); print(json.dumps(r, ensure_ascii=False)); sys.stdout.flush()
    return r, out


which = sys.argv[1:] or ["posto", "adendo", "sondas"]
if "posto" in which:
    run(AF + "/src/TGLExt/Posto.lean", AF + "/out/TGLExt/Posto.olean")
if "adendo" in which:
    run(AF + "/src/TGLExt/PostoAdendo.lean", AF + "/out/TGLExt/PostoAdendo.olean")
if "sondas" in which:
    for s in ("Sonda_axiomas.lean", "Sonda_enunciados.lean", "Sonda_negativo.lean"):
        if os.path.exists(AF + "/" + s):
            run(AF + "/" + s)
json.dump(res, open(AF + "/RESULTADO_%s.json" % "_".join(which), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
