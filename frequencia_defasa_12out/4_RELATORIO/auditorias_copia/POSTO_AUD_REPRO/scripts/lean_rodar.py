# -*- coding: utf-8 -*-
# Auditor REPRO: compila UM arquivo .lean do sandbox do auditor com o toolchain COPIADO e LEAN_PATH (so leitura) para
# o .lake do tgl_kernel do Nos (+ lean_sb\build, onde ficam os .olean gerados aqui). Nada e escrito fora da pasta do auditor.
# Uso: lean_rodar.py <arquivo relativo a lean_sb> <tag> [--olean <nome relativo a lean_sb\build>] [--root <dir>]
import os, sys, subprocess, hashlib, json, time, datetime
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(AUD, "L")
LEAN = os.path.join(SB, "tc", "bin", "lean.exe")
BUILD = os.path.join(SB, "build")
LOGS = os.path.join(AUD, "saidas", "lean_logs")
K = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\.lake"
pk = sorted(os.listdir(os.path.join(K, "packages")))
paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in pk]
paths = [p for p in paths if os.path.isdir(p) or p == BUILD]
LEAN_PATH = ";".join(paths)


def sha(b):
    return hashlib.sha256(b).hexdigest()


alvo, tag = sys.argv[1], sys.argv[2]
olean = None
if "--olean" in sys.argv:
    olean = os.path.join(BUILD, sys.argv[sys.argv.index("--olean") + 1])
os.makedirs(BUILD, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)
src = open(os.path.join(SB, alvo), "rb").read()
env = dict(os.environ)
env["LEAN_PATH"] = LEAN_PATH
for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH", "LAKE", "LAKE_HOME"):
    env.pop(k, None)
cmd = [LEAN]
if "--root" in sys.argv:
    cmd += ["--root=" + sys.argv[sys.argv.index("--root") + 1]]
if olean:
    cmd += ["-o", olean]
cmd += [alvo]
t0 = time.time()
st = datetime.datetime.now(datetime.timezone.utc).isoformat()
r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
dt = time.time() - t0
saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
txt = saida.decode("utf-8", errors="replace")
rec = {"alvo": alvo, "tag": tag, "source_sha256": sha(src), "source_bytes": len(src), "inicio_utc": st, "segundos": round(dt, 2),
       "exit_code": r.returncode, "saida_sha256": sha(saida), "n_erros": txt.count(": error"), "n_avisos": txt.count(": warning"),
       "ocorrencias_sorryAx": txt.count("sorryAx"), "declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
       "comando": cmd, "cwd": SB, "LEAN_PATH": LEAN_PATH}
if olean and os.path.exists(olean):
    ob = open(olean, "rb").read()
    rec["olean_bytes"] = len(ob)
    rec["olean_sha256"] = sha(ob)
open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "ocorrencias_sorryAx", "olean_bytes", "olean_sha256")}, ensure_ascii=False))
print(txt[:30000])
