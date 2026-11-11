# -*- coding: utf-8 -*-
"""Acha as duas portas depositadas no Zenodo da v409 (PORTA.md 27435 B md5 44e55e8a...; PORTA.json 41354 B md5 cc1e4d27...): varre todos os PORTA.* do
espelho e do No's no disco e, para a raiz do espelho, todos os commits desde a v407. Somente leitura."""
import hashlib
import subprocess
from pathlib import Path

TB = Path(r"C:\IALD\Artigo\the_boundary")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
ALVO = {"PORTA.md": ("44e55e8a4a3b36e97be8fad269c15a4e", 27435), "PORTA.json": ("cc1e4d27453db82f6978f7c2e1a32aac", 41354)}


def md5(b):
    return hashlib.md5(b).hexdigest()


for nome, (h, tam) in ALVO.items():
    print("==", nome, tam, "B")
    for raiz in (TB, NOS, Path(r"C:\IALD\Central_publica")):
        for p in raiz.rglob(nome):
            try:
                if p.stat().st_size == tam:
                    print("   tamanho igual:", p, "| md5 bate:", md5(p.read_bytes()) == h)
            except OSError:
                pass
    # historico completo da raiz do espelho
    commits = subprocess.run(["git", "-C", str(TB), "log", "--format=%h", "--", nome], capture_output=True, text=True).stdout.split()
    for c in commits[:60]:
        r = subprocess.run(["git", "-C", str(TB), "show", "%s:%s" % (c, nome)], capture_output=True)
        if r.returncode == 0 and md5(r.stdout) == h:
            print("   BATE no commit", c)
            break
    else:
        print("   nenhum dos", min(60, len(commits)), "commits da raiz tem este md5")
    atual = TB / nome
    print("   raiz hoje:", atual.stat().st_size, "B")
