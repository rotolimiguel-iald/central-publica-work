# -*- coding: utf-8 -*-
"""Compila UM .lean do sandbox com o binario lean v4.31.0 do elan (chamado DIRETAMENTE, sem lake, sem copiar toolchain),
LEAN_PATH SOMENTE LEITURA ao .lake do tgl_kernel do Nos; nenhum -o (nenhum .olean gravado).
Grava logs/<tag>_SAIDA.txt e logs/<tag>_RECIBO.json. Uso: rodar_lean.py <arquivo em sandbox> <tag>"""
import os, sys, subprocess, hashlib, json, time, datetime
AQUI = os.path.dirname(os.path.abspath(__file__))
SB = os.path.join(AQUI, "sandbox")
LOGS = os.path.join(AQUI, "logs")
LEAN = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe")
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
paths = [os.path.join(K, "build", "lib", "lean")] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
paths = [p.replace("/", "\\") for p in paths if os.path.isdir(p)]
alvo, tag = sys.argv[1], sys.argv[2]
src = os.path.join(SB, alvo)
sb = open(src, "rb").read()
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(paths)
for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
    env.pop(k, None)
cmd = [LEAN, alvo]
t0 = time.time()
st = datetime.datetime.now(datetime.timezone.utc).isoformat()
r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
dt = time.time() - t0
saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
os.makedirs(LOGS, exist_ok=True)
open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
txt = saida.decode("utf-8", errors="replace")
rec = {"alvo": alvo, "tag": tag, "source_sha256": hashlib.sha256(sb).hexdigest(), "source_bytes": len(sb),
       "inicio_utc": st, "segundos": round(dt, 2), "exit_code": r.returncode,
       "saida_sha256": hashlib.sha256(saida).hexdigest(), "n_erros": txt.count(": error"),
       "n_avisos": txt.count(": warning"), "declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
       "lean": LEAN, "LEAN_PATH_n": len(paths), "olean_gravado": False, "comando": cmd}
json.dump(rec, open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: rec[k] for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "declaration_uses_sorry")}))
print(txt[:12000])
