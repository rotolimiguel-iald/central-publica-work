# -*- coding: utf-8 -*-
"""grava o resultado da 9a afericao (o campo result do arquivo de saida do workflow wytu2a2s6), temporario -> conferir -> substituir; nunca sobrescreve"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "..", "tasks", "wytu2a2s6.output")
SRC = os.path.normpath(SRC)
j = json.load(open(SRC, encoding="utf-8"))["result"]
OUT = os.path.join(HERE, "afericao9_resultado.json")
b = json.dumps(j, ensure_ascii=False, indent=1).encode("utf-8")
assert not os.path.exists(OUT) or open(OUT, "rb").read() == b, "ja existe com outro conteudo"
open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b); os.replace(OUT + ".tmp", OUT)
print("afericao9_resultado.json", hashlib.sha256(b).hexdigest()[:16], len(b), "| fonte", hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:16])
