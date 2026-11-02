# -*- coding: utf-8 -*-
"""Patch da guarda do arco no site (gerencia c1, 02/11/2026, custodia v405): a guarda aceitava a frase da regua so em ingles; a forma portuguesa e a redacao literal da regua."""
import datetime, os, py_compile
from pathlib import Path

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_c1"
p = Path("C:/IALD/Site/tgl/v3.0_bancada/tools/atualizar_dados_selo_site.py")
old = ".replace('NOT_FALSIFIED is not CONFIRMED', '')"
new = ".replace('NOT_FALSIFIED is not CONFIRMED', '').replace('NOT_FALSIFIED nunca é CONFIRMED', '')"
b = p.read_bytes()
t = b.decode("utf-8")
assert t.count(old) == 1, t.count(old)
nb = t.replace(old, new).encode("utf-8")
bak = p.with_name(p.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(b)
assert bak.read_bytes() == b
tmp = p.with_name(p.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(nb)
py_compile.compile(str(tmp), cfile=str(tmp) + ".pyc", doraise=True)
os.remove(str(tmp) + ".pyc")
os.replace(tmp, p)
print("ok", len(b), "->", len(nb))
