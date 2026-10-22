# -*- coding: utf-8 -*-
"""02_secoes.py -- lista as secoes (chapter/section/subsection) dos .tex PT e EN da v375, com numero de linha."""
import re, os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
rx = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\{(.*)$")
res = {}
for lang in ("pt", "en"):
    p = os.path.join(NOS, "um_absoluto_%s.tex" % lang)
    lines = open(p, encoding="utf-8").read().splitlines()
    secs = []
    for i, l in enumerate(lines, 1):
        m = rx.match(l)
        if m:
            secs.append((i, m.group(1), m.group(2).rstrip("}").strip()))
    res[lang] = secs
    print("=====", lang, "n_linhas", len(lines), "n_secs", len(secs))
    for i, k, t in secs:
        print("%6d %-13s %s" % (i, k, t[:160]))
json.dump(res, open(os.path.join(OUT, "02_secoes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
