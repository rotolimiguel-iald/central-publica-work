# -*- coding: utf-8 -*-
"""SÓ LEITURA: antes da mescla incremental, o que cada índice público tem que NÃO existe na origem (no núcleo: que o git da Central não
rastreia) e o que cada preparo tem em disco na raiz fora do índice (os gerados depois do construtor: README, PATENTES, índices)."""
import json, os, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes")
RAIZ = Path(r"C:\IALD\Central_publica")


def longo(base, rel):
    return "\\\\?\\" + str(base) + "\\" + rel.replace("/", "\\")


tr = set(x for x in subprocess.run(["git", "-C", str(CEN), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0") if x)
for nome, tipo in (("central-publica", "nucleo"), ("central-publica-work", "work"), ("central-publica-bancada", "Chatgpt")):
    D = RAIZ / nome
    idx = json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))
    rels = [a["caminho"] for a in idx["arquivos"]]
    src = CEN if tipo == "nucleo" else CEN / tipo
    if tipo == "nucleo":
        sem = [r for r in rels if r not in tr or not os.path.exists(longo(src, r))]
    else:
        sem = [r for r in rels if not os.path.exists(longo(src, r))]
    raiz_fora = sorted(p.name for p in D.iterdir() if p.is_file() and p.name not in set(rels))
    print("%s: índice %d | sem origem %d %s" % (nome, len(rels), len(sem), sem[:12]))
    print("   na raiz e fora do índice:", raiz_fora)
