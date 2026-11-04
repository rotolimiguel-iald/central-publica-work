# -*- coding: utf-8 -*-
# 03/11/2026, gerencia c1: roda o conferir_citacoes_v407.py por exec (so' leitura), intercepta o sys.exit e grava o dict R INTEIRO em citacoes_R_r2.json, para ver QUAL checagem falhou
# (o script imprime so' as contagens). Nao altera nada da cadeia.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "conferir_citacoes_v407.py")
g = {"__name__": "__main__", "__file__": SCR}
src = open(SCR, encoding="utf-8").read()
try:
    exec(compile(src, SCR, "exec"), g)
except SystemExit as e:
    print("sys.exit:", e.code)
R = g.get("R") or {}
json.dump(R, open(os.path.join(HERE, "citacoes_R_r2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


def ruim(x):
    if isinstance(x, bool):
        return not x
    if isinstance(x, dict):
        return {k: v for k, v in x.items() if ruim(v)}
    if isinstance(x, list):
        return x
    return False


for k, v in R.items():
    if k in ("todas_conferem", "resumo_dito_a_gerencia", "apontadas_a_gerencia_aspas"):
        continue
    r = ruim(v)
    if r:
        print("->", k, "=", json.dumps(r, ensure_ascii=False, default=str)[:1500])
print("apontadas_a_gerencia_aspas:", json.dumps(R.get("apontadas_a_gerencia_aspas"), ensure_ascii=False, default=str)[:800])
print("resumo:", json.dumps(R.get("resumo_dito_a_gerencia"), ensure_ascii=False, default=str)[:400])
