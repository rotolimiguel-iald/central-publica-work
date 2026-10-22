"""Roda o dump de collectAxioms (axioms_dump.lean) no sandbox C:\\t\\k396\\final e grava as linhas DECL|... em axioms_dump_raw.txt.

Processo criado e esperado por este script (nenhum processo é morto por nome). Só escreve em C:\\t\\k396 e na pasta de trabalho.
Uso: python -I -X utf8 run_axioms_dump.py
"""
import os
import shutil
import subprocess

W = r"C:\IALD\Central de Patentes\work\testemunha_estatica_v396"
SB = r"C:\t\k396\final"
SRC = W + r"\scripts\axioms_dump.lean"
DST = SB + r"\probe\axioms_dump.lean"
RAW_SB = r"C:\t\k396\axioms_dump_raw.txt"

os.makedirs(SB + r"\probe", exist_ok=True)
shutil.copyfile(SRC, DST)

env = dict(os.environ)
env["PATH"] = r"C:\Users\rotol\.elan\bin;" + env.get("PATH", "")
r = subprocess.run(["lake", "env", "lean", "probe/axioms_dump.lean"], capture_output=True, text=True, cwd=SB, env=env, encoding="utf-8")
saida = r.stdout + r.stderr
linhas = []
for ln in saida.split("\n"):
    i = ln.find("DECL|")
    if i >= 0:
        linhas.append(ln[i:].rstrip("\r"))
open(RAW_SB, "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
shutil.copyfile(RAW_SB, W + r"\axioms_dump_raw.txt")
print("returncode:", r.returncode, "| linhas DECL:", len(linhas))
if r.returncode != 0 or not linhas:
    print(saida[:3000])
