# -*- coding: utf-8 -*-
"""Uso: python -I _inspeciona_fonte.py <arquivo> <regex> [pagina_pdf]. Imprime trechos do texto normalizado que casam (dado nao confiavel)."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runner"))
import f9v2_text as T  # noqa: E402

p, rx = sys.argv[1], sys.argv[2]
raw = open(p, "rb").read()
if p.lower().endswith(".pdf"):
    pages = T.pdf_pages_text(raw)
    for i, tx in enumerate(pages):
        for m in re.finditer(rx, tx):
            print("p%d:" % (i + 1), tx[max(0, m.start() - 160): m.end() + 160])
            print("---")
else:
    tx = T.html_to_text(raw)
    for m in re.finditer(rx, tx):
        print(tx[max(0, m.start() - 200): m.end() + 250])
        print("---")
