# -*- coding: utf-8 -*-
"""Consulta SÓ DE LEITURA ao inventário da bancada (INVENTARIO_BANCADA_CHATGPT.json): busca textual por termos.
Uso: python -I consultar_inventario.py <saida.json>"""
import hashlib, json, sys
INV = r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json"
TERMOS = ["identity_flow_not_kms", "theSpecificAQFTWitness", "omega_not_tracial", "FockCertificate",
          "TheTimeHasNoRank", "absoluteRho", "gibbs_kms", "KMSAt"]
b = open(INV, "rb").read()
inv = json.loads(b)
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[" + str(i) + "]")
    else:
        yield path, o
res = {"inventario": INV, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "termos": {}}
folhas = list(walk(inv))
for t in TERMOS:
    hits = [(p, str(v)[:160]) for p, v in folhas if isinstance(v, str) and t in v]
    res["termos"][t] = {"n": len(hits), "exemplos": hits[:6]}
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.reconfigure(encoding="utf-8")
print(res["sha256"][:16], {t: v["n"] for t, v in res["termos"].items()})
for t, v in res["termos"].items():
    for p, s in v["exemplos"][:3]:
        print(" ", t, "|", p[:90], "|", s[:120])
