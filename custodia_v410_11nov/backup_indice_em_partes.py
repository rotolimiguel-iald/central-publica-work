# -*- coding: utf-8 -*-
r"""Backup de BYTES (11/11/2026, custodia v410, claude-site-custodia) dos arquivos que a errata do indice em partes toca, na mesma pasta de cada um.
O llms.txt mora dentro do preparo do central-publica-work, que e uma arvore git cujos nao-rastreados a conferencia do delta varre: o backup ao lado
dele so fica na mesma pasta com a exclusao LOCAL e estreita `/llms.txt.bak_*` em .git/info/exclude (nunca vai ao git; a conferencia nao o ve)."""
import os
import shutil
import subprocess
import time

TS = time.strftime("%Y%m%d_%H%M%S")
W = r"C:\IALD\Central de Patentes\work\central_publica_22out"
PREP = r"C:\IALD\Central_publica\central-publica-work"
EXC = PREP + r"\.git\info\exclude"
LINHA = "/llms.txt.bak_*   # 11/11/2026 (custodia v410): backup de bytes do llms.txt ao lado dele, so local\n"
t = open(EXC, "rb").read().decode("utf-8")
if "/llms.txt.bak_*" not in t:
    nb = (t if t.endswith("\n") else t + "\n") + LINHA
    tmp = EXC + ".tmp"
    open(tmp, "wb").write(nb.encode("utf-8"))
    os.replace(tmp, EXC)
ALVOS = [W + "\\conferir_preparos.py", W + "\\atualizar_repo_publico.py", W + "\\gerar_readmes_publicos.py", W + "\\atualizar_central_publica.py",
         PREP + "\\llms.txt", r"C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_llms_site.py"]
for p in ALVOS:
    b = p + ".bak_" + TS + "_indice_em_partes"
    shutil.copy2(p, b)
    assert open(p, "rb").read() == open(b, "rb").read()
    print(os.path.getsize(b), b)
r = subprocess.run(["git", "-C", PREP, "check-ignore", "-q", "llms.txt.bak_" + TS + "_indice_em_partes"])
assert r.returncode == 0, "o backup do llms.txt nao esta excluido do git"
print("backup do llms.txt excluido do git (local)")
