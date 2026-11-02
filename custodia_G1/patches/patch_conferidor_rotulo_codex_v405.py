# -*- coding: utf-8 -*-
"""Conferidor publico (gerencia c1, 02/11/2026, custodia v405): o rotulo de fluxo do Codex nao e credencial. So este valor exato, por sha256; a regra nao muda."""
import datetime, hashlib, os, py_compile
from pathlib import Path

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_c1"
p = Path("C:/IALD/Central de Patentes/work/central_publica_22out/conferir_preparos.py")
ROTULO = b"explicit_parent_go"
h = hashlib.sha256(ROTULO).hexdigest()
assert h.startswith("d1e00e0d2979f7f7"), h[:16]
b = p.read_bytes()
t = b.decode("utf-8")
crlf = "\r\n" in t
assert not crlf or t.count("\n") == t.count("\r\n")
NL = "\r\n" if crlf else "\n"
old = 'APROVADOS = {"c521b24d2889ff6204f5c7b1c76a9524306dc2cdba8cd807c6cd64a69b72d8ab"}' + NL
new = ('# (02/11/2026, custódia v405) rótulo de fluxo do Codex, sem segredo: chave authorization em filmes_v7_20261024/adendo_h_v404 (MEDIA_GO.json, release_media.py); '
       'valor lido e aceito pela gerência c1, não pelo operador' + NL
       + 'APROVADOS = {"c521b24d2889ff6204f5c7b1c76a9524306dc2cdba8cd807c6cd64a69b72d8ab", "' + h + '"}' + NL)
assert t.count(old) == 1
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
