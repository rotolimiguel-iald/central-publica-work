# -*- coding: utf-8 -*-
"""Varredura das palavras que a regua veda como veredito, nos tres artefatos do redator R2."""
import json, os, re, sys
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARQ = ["RELATORIO_FINAL.md", "registro_rota_F1.TEMPO.json", "registro_mapa_F1.TEMPO.json"]
PADROES = {"palavra_vedada_maiuscula": "CONF" + "IRMED", "confirm_qualquer_caixa": "conf" + "irm",
           "nao_provou": r"n[aã]o prov" + "ou", "pos_dicao": r"p[oó]s-di[cç]+[aã]o", "medido_aqui_para_beta": r"\[REAL\s*[—-]\s*medido aqui"}
out = {}
for a in ARQ:
    t = open(os.path.join(BASE, a), encoding="utf-8").read()
    out[a] = {}
    for k, p in PADROES.items():
        hits = [m.start() for m in re.finditer(p, t, re.I if k != "palavra_vedada_maiuscula" else 0)]
        ctx = [t[max(0, h - 60):h + 60].replace("\n", " ") for h in hits[:5]]
        out[a][k] = {"n": len(hits), "contexto": ctx}
outp = os.path.join(BASE, "R2", "saidas", "VARREDURA_PALAVRAS_R2.json")
with open(outp + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(outp + ".tmp", outp)
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
