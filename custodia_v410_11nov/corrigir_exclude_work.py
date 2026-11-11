# -*- coding: utf-8 -*-
r"""O .git/info/exclude nao aceita comentario no fim da linha (o padrao virava o texto inteiro): comentario na linha de cima, padrao sozinho."""
import os
import subprocess

PREP = r"C:\IALD\Central_publica\central-publica-work"
EXC = PREP + r"\.git\info\exclude"
t = open(EXC, "rb").read().decode("utf-8")
velha = "/llms.txt.bak_*   # 11/11/2026 (custodia v410): backup de bytes do llms.txt ao lado dele, so local\n"
nova = "# 11/11/2026 (custodia v410, claude-site-custodia): backup de bytes do llms.txt ao lado dele, so local\n/llms.txt.bak_*\n"
assert t.count(velha) == 1
nb = t.replace(velha, nova)
tmp = EXC + ".tmp"
open(tmp, "wb").write(nb.encode("utf-8"))
os.replace(tmp, EXC)
r = subprocess.run(["git", "-C", PREP, "check-ignore", "-q", "llms.txt.bak_20261111_051506_indice_em_partes"])
assert r.returncode == 0, "ainda nao excluido"
s = subprocess.run(["git", "-C", PREP, "status", "--porcelain", "--untracked-files=all", "--", "llms.txt.bak_20261111_051506_indice_em_partes"], capture_output=True, text=True)
assert s.stdout.strip() == "", s.stdout
print("ok: o backup do llms.txt esta excluido do git (local) e fora do status")
