# -*- coding: utf-8 -*-
# Auditor de estatuto (r2): sandbox Lean PROPRIO. Copia (so leitura na origem) bin/ e lib/lean/{Init,Std,Lean,Lake} do
# toolchain v4.31.0 do elan para r2\toolchain_v4.31.0; compila com LEAN_PATH so-leitura ao .lake do tgl_kernel do Nos
# (+ r2\sandbox\build). Nada e escrito fora de r2. Uso: copiar | compilar <alvo rel. ao sandbox> <tag> [--root R] [--olean O] | apagar
import os, sys, shutil, json, time, hashlib, subprocess, datetime
R2 = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(os.path.expanduser("~"), ".elan", "toolchains", "leanprover--lean4---v4.31.0")
TC = os.path.join(R2, "toolchain_v4.31.0")
SB = os.path.join(R2, "sandbox")
BUILD = os.path.join(SB, "build")
LOGS = os.path.join(R2, "logs")
K = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N" + chr(0xf3) + "s", "tgl_kernel", ".lake")
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
MODS = ("Init", "Std", "Lean", "Lake")
PFX = chr(92) * 2 + "?" + chr(92)
def L(p): return p if p.startswith(PFX) else PFX + p
def sha(b): return hashlib.sha256(b).hexdigest()
def copiar():
    t0 = time.time()
    if os.path.exists(L(TC)): print("ja existe"); return
    shutil.copytree(L(os.path.join(ORIG, "bin")), L(os.path.join(TC, "bin")))
    lo = L(os.path.join(ORIG, "lib", "lean")); ld = L(os.path.join(TC, "lib", "lean")); os.makedirs(ld, exist_ok=True)
    for fn in os.listdir(lo):
        if fn.split(".")[0] not in MODS: continue
        p = os.path.join(lo, fn)
        if os.path.isdir(p): shutil.copytree(p, os.path.join(ld, fn))
        else: shutil.copy2(p, os.path.join(ld, fn))
    n = sum(len(f) for _, _, f in os.walk(L(TC)))
    print(json.dumps({"copiado_para": TC, "arquivos": n, "segundos": round(time.time() - t0, 1)}))
def compilar(alvo, tag):
    paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
    paths = [p for p in paths if os.path.isdir(p) or p == BUILD]
    os.makedirs(BUILD, exist_ok=True); os.makedirs(LOGS, exist_ok=True)
    rec_path = os.path.join(LOGS, tag + "_RECIBO.json")
    if os.path.exists(rec_path): raise SystemExit("FALHA VISIVEL: recibo ja existe: " + rec_path)
    env = dict(os.environ); env["LEAN_PATH"] = ";".join(paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"): env.pop(k, None)
    cmd = [os.path.join(TC, "bin", "lean.exe")]
    if "--root" in sys.argv: cmd += ["--root=" + sys.argv[sys.argv.index("--root") + 1]]
    olean = None
    if "--olean" in sys.argv:
        olean = os.path.join(BUILD, sys.argv[sys.argv.index("--olean") + 1]); cmd += ["-o", olean]
    cmd += [alvo]
    src = open(os.path.join(SB, alvo), "rb").read()
    t0 = time.time(); st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
    txt = saida.decode("utf-8", "replace")
    rec = {"alvo": alvo, "tag": tag, "source_sha256": sha(src), "inicio_utc": st, "segundos": round(time.time() - t0, 2),
           "exit_code": r.returncode, "saida_sha256": sha(saida), "n_erros": txt.count(": error"), "n_avisos": txt.count(": warning"),
           "sorryAx": txt.count("sorryAx"), "comando": cmd, "LEAN_PATH": env["LEAN_PATH"]}
    if olean and os.path.exists(olean):
        ob = open(olean, "rb").read(); rec["olean_sha256"] = sha(ob); rec["olean_bytes"] = len(ob)
    open(rec_path, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "sorryAx", "olean_sha256")}))
    print(txt[:15000])
def apagar():
    out = {}
    for a in (TC, BUILD):
        if os.path.exists(L(a)): shutil.rmtree(L(a))
        out[a] = {"existe_depois": os.path.exists(L(a))}
    for dp, dns, fns in os.walk(L(R2)):
        for d in list(dns):
            if d == ".lake": shutil.rmtree(os.path.join(dp, d)); out.setdefault("lake_apagados", []).append(os.path.join(dp, d))
    print(json.dumps(out, ensure_ascii=False, indent=1))
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "copiar": copiar()
    elif c == "compilar": compilar(sys.argv[2], sys.argv[3])
    elif c == "apagar": apagar()
