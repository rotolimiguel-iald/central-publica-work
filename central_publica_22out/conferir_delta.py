# -*- coding: utf-8 -*-
"""CONFERÊNCIA INDEPENDENTE DO DELTA de um preparo público já publicado (22/10/2026, custódia v396): roda o PRÓPRIO código de
conferir_preparos.py (não importa a guarda nem a máscara), com UMA troca — a lista de arquivos varridos passa a ser o que difere do HEAD do
repositório do preparo (novo ou alterado, segundo o git) — e grava o relatório ao lado, varredura_conferencia_delta_<preparo>.json, com a
lista do que foi conferido. O resto do conferidor vale inteiro (inclusive «índice sem arquivo» sobre o índice todo). Os arquivos que não
mudaram já foram aprovados pela conferência completa de 22/10 e são os mesmos bytes do HEAD publicado.
Uso: conferir_delta.py <pasta_do_preparo> [regiao]   (exit 1 se achar algo)"""
import os, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
D = Path(sys.argv[1])
REG = len(sys.argv) > 2 and sys.argv[2] == "regiao"
st = subprocess.run(["git", "-C", str(D), "status", "--porcelain", "-z", "--untracked-files=all"], capture_output=True,
                    env=dict(os.environ, GIT_LITERAL_PATHSPECS="1")).stdout.decode("utf-8", "replace").split("\0")
delta = []
for e in st:
    if not e:
        continue
    cod, rel = e[:2], e[3:]
    if "D" in cod:
        continue                       # apagado: nada a varrer (o índice já não o traz)
    delta.append(rel)
src = (W / "conferir_preparos.py").read_text(encoding="utf-8")
assert src.count("for p in _todos():") == 1 and src.count('"varredura_conferencia_%s.json"') == 1
antes, depois = src.split("for p in _todos():")
depois = "for p in _todos():" + depois.replace('"varredura_conferencia_%s.json"', '"varredura_conferencia_delta_%s.json"')
ns = {"__file__": str(W / "conferir_preparos.py")}
sys.argv = [sys.argv[0], str(D)] + (["regiao"] if REG else [])
exec(compile(antes, "conferir_preparos.py (definições)", "exec"), ns)
_raiz = ns["_RAIZ"]


def _so_o_delta():
    for rel in delta:
        yield Path(_raiz + "\\" + rel.replace("/", "\\"))


ns["_todos"] = _so_o_delta
cod = 0
try:
    exec(compile(depois, "conferir_preparos.py (varredura)", "exec"), ns)
except SystemExit as e:
    cod = e.code or 0
rp = W / ("varredura_conferencia_delta_%s.json" % D.name)
import json  # noqa: E402
r = json.loads(rp.read_text(encoding="utf-8"))
r["delta_conferido"] = sorted(delta)
r["n_delta"] = len(delta)
rp.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
print("delta de %s: %d arquivos conferidos (o resto é o HEAD já aprovado) | %s" % (D.name, len(delta), "APROVADO" if r["aprovado"] else "REPROVADO"))
sys.exit(cod)
