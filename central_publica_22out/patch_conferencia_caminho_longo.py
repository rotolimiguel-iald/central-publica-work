# -*- coding: utf-8 -*-
"""A conferência percorre o preparo com o prefixo de caminho longo do Windows (\\\\?\\): o rglob não enumerava caminhos acima de 260
caracteres e 343 arquivos do work ficaram sem varrer (achado de 22/10/2026). Também: rótulos que não são valor de segredo (nome de
arquivo, constante em maiúsculas, «…_only», «DO_NOT_…») saem da leitura de credencial. Backup de BYTES; trocas conferidas por contagem."""
import os, time
from pathlib import Path

p = Path(__file__).with_name("conferir_preparos.py")
raw = p.read_bytes()
s = raw.decode("utf-8")
pares = [
    ('for p in D.rglob("*"):\n    if not p.is_file():\n        continue\n    rel = p.relative_to(D).as_posix()\n',
     '_RAIZ = "\\\\\\\\?\\\\" + str(D.resolve())\n'
     'def _todos():\n'
     '    for dp, dns, fns in os.walk(_RAIZ):\n'
     '        dns[:] = [x for x in dns if x != ".git"]\n'
     '        for f in fns:\n'
     '            yield Path(os.path.join(dp, f))\n'
     'for p in _todos():\n'
     '    rel = os.path.relpath(str(p), _RAIZ).replace(os.sep, "/")\n'),
    ('    if rel not in vistos and not (D / rel).is_file():\n',
     '    if rel not in vistos and not os.path.isfile("\\\\\\\\?\\\\" + str((D / rel).resolve())):\n'),
    ('r"dado pessoal removido|redacted|test|teste|__Host-|__Secure-|_session\\b)")',
     'r"dado pessoal removido|redacted|test|teste|__Host-|__Secure-|_session\\b|\\.(?:txt|json|md|py|yaml)$|^[A-Z0-9_]+$|_only$|DO_NOT)")'),
]
for a, b in pares:
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
if "import os" not in s.split("\n", 30)[0:30].__str__():
    s = s.replace("import base64, binascii, hashlib, io, json, re, sys, zipfile", "import base64, binascii, hashlib, io, json, os, re, sys, zipfile", 1)
compile(s, str(p), "exec")
p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = p.with_name(p.name + ".tmp_cl")
t.write_bytes(s.encode("utf-8"))
os.replace(t, p)
print("ok conferir_preparos.py", len(raw), "->", p.stat().st_size)
