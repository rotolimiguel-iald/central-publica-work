# -*- coding: utf-8 -*-
"""privacidade_v402.py -- exame final v402, SO LEITURA: conta os arquivos que contem a palavra de abertura da integra privada
(grafia da fala e grafia padrao) e o prefixo do hash da integra, em v402\, C:\t\k402c, cunhagens_13out e nesta pasta de exame.
Padroes montados por concatenacao (este arquivo nao os contem). Grava PRIVACIDADE_v402.json (contagens e caminhos, sem os padroes)."""
import json, os, re, sys, time
H = os.path.dirname(os.path.abspath(__file__))
W = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work")
PATS = {"A_grafia_da_fala": ("entuasi" + "asm").encode(), "A2_grafia_padrao": ("entusi" + "asm").encode(), "B_hash": ("484ad9" + "82").encode()}
raizes = [os.path.join(W, "cadeia_de_selo", "v402"), os.path.join("C:" + os.sep, "t", "k402c"), os.path.join(W, "cunhagens_13out"), H]
res = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "raizes": {}}
for r in raizes:
    ach = {k: [] for k in PATS}; n = 0
    for d, ds, fs in os.walk(r):
        for f in fs:
            p = os.path.join(d, f)
            if os.path.abspath(p) in (os.path.abspath(__file__), os.path.join(H, "PRIVACIDADE_v402.json")):
                continue
            n += 1
            try:
                with open(p, "rb") as fh:
                    prev = b""
                    while True:
                        b = fh.read(8 << 20)
                        if not b: break
                        chunk = (prev + b).lower()
                        for k, pat in PATS.items():
                            if pat in chunk and p not in ach[k]: ach[k].append(p)
                        prev = b[-64:]
            except OSError as e:
                ach.setdefault("erro_leitura", []).append(p + " " + str(e))
    res["raizes"][r] = {"arquivos_varridos": n, **{k: {"n": len(v), "lista": v[:50]} for k, v in ach.items()}}
json.dump(res, open(os.path.join(H, "PRIVACIDADE_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r, v in res["raizes"].items():
    print(r, v["arquivos_varridos"], {k: v[k]["n"] for k in PATS})
