# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): citacoes entre « » nos textos RENDIDOS pelo harness do pos-rito (/c/t/h407/harness_saida_v407/textos) contra o corpus das falas do operador. Lista as NAO-substring."""
import glob, hashlib, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/IALD/Central de Patentes/work/"
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "")).strip()
noacc = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
corp = []
for pat in (W + "cadeia_de_selo/v407/insumos/cunhagens/*.txt", W + "cunhagens_13out/*.txt", W + "cadeia_de_selo/v406/insumos/cunhagens/*.txt"):
    for p in glob.glob(pat): corp.append(norm(open(p, "rb").read().decode("utf-8", "replace")))
C = " || ".join(corp); CN = noacc(C)
# + o texto das ressalvas/limites/diz/nao_diz do registro (a excecao do verificar_paragrafo)
import json, ast
cs = open(W + "cadeia_de_selo/v407/delta_v407.py", encoding="utf-8").read()
q = re.compile(r"«([^»]+)»")
tot = 0; nao = {}
for f in sorted(glob.glob("C:/t/h407/harness_saida_v407/textos/*.txt")):
    t = open(f, encoding="utf-8").read()
    for m in q.finditer(t):
        tot += 1; s = norm(m.group(1)).strip(" .,;:\u201c\u201d\"")
        segs = [x.strip(" .,;:\u201c\u201d\"") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", s) if len(x.strip(" .,;:\u201c\u201d\"")) >= 4]
        ok = (s in C) or (segs and all(x in C for x in segs)) or (segs and all(noacc(x) in CN for x in segs))
        if not ok: nao.setdefault(s, set()).add(os.path.basename(f))
print("total de citacoes « » nos textos rendidos:", tot, "| distintas nao-substring:", len(nao))
for s, fs in sorted(nao.items()): print("  ?", repr(s[:200]), sorted(fs)[:4])
