# -*- coding: utf-8 -*-
"""Revisor v410 R1: classifica as citacoes NAO casadas de e_citacoes_v410_out.json: (i) HERDADA (a mesma citacao existe no texto rendido da v409 selada: dry_v409) -> fora do escopo da v410;
(ii) FRAGMENTO de concatenacao de codigo (contem ' + ' ou aspas de codigo); (iii) restante = NOVA a classificar a mao."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/"
j = json.load(open(R + "v410/revisao_terceiro/e_citacoes_v410_out.json", encoding="utf-8"))
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "").replace("\\%", "%").replace("\\_", "_")).strip()
base = ""
for p in glob.glob(R + "v409/dry_v409/*.txt") + glob.glob(R + "v409/dry_v409/*.md") + glob.glob(R + "v409/pedra/*.lean"):
    base += " || " + norm(open(p, "rb").read().decode("utf-8", "replace"))
bs = norm(open(R + "v410/base_v409/um.py", "rb").read().decode("utf-8", "replace"))
print("base chars", len(base), len(bs))
novas = {}
herd = 0; frag = 0
for q, ks in j["nao_casadas"].items():
    if len(q) < 12: continue
    if " + " in q or q.startswith('"') or "DL." in q or '"]' in q:
        frag += 1; continue
    if q in base or q in bs:
        herd += 1; continue
    novas[q] = ks
print("herdadas", herd, "fragmentos de codigo", frag, "NOVAS", len(novas))
for q, ks in sorted(novas.items(), key=lambda x: -len(x[0])):
    print(len(q), repr(q[:260]), "<-", sorted({k.split(":")[-1][-34:] for k in ks})[:5])
