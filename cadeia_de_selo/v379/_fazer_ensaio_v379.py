# -*- coding: utf-8 -*-
# gera ensaio_a_seco_v379.py a partir do ensaio v378 (edicoes pontuais, count == 1) -- molde _fazer_ensaio_v378.py
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__))
V8 = os.path.join(os.path.dirname(HERE), "v378")
src = open(os.path.join(V8, "ensaio_a_seco_v378.py"), encoding="utf-8", newline="").read()
K379 = ("the_elementary_reason_v379",)
R = [
    ('TAG = "v378"', 'TAG = "v379"'),
    ('    if k.startswith(("ext_dlc_",)):', '    if k.startswith(("ext_ter_",)):'),
    ('c["bancada_fase4_v378"] = um.prove_bancada_fase4_v378(1.0, c)\n',
     'c["bancada_fase4_v378"] = um.prove_bancada_fase4_v378(1.0, c)\n' + "".join('c["%s"] = um.prove_%s(1.0, c)\n' % (k, k) for k in K379)),
    ('DEVE = {"pt": ["Ao lado (v378) --- O que faltou",',
     'DEVE = {"pt": ["Ao lado (v379) --- A Razão Elementar", "TheElementaryReason", "limite assintótico em tempo finito", "colisão dita por termo", "Ao lado (v378) --- O que faltou",'),
    ('        "en": ["Beside (v378) --- What was missed",',
     '        "en": ["Beside (v379) --- The Elementary Reason", "TheElementaryReason", "asymptotic limit in finite time", "a collision stated by term", "Beside (v378) --- What was missed",'),
    ('    nome = "dry_v378_%s" % lang', '    nome = "dry_v379_%s" % lang'),
    ('rep["markdown_v376"] = {"v376": md.count("v378"), "carimbo": "**Versão v378**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v379"), "carimbo": "**Versão v379**" in md,'),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v378**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v379**" in open(mani, encoding="utf-8").read()}'),
]
NL = chr(13) + chr(10) if src.count(chr(13) + chr(10)) > src.count(chr(10)) // 2 else chr(10)
R = [(x.replace(chr(10), NL), y.replace(chr(10), NL)) for x, y in R]
for a, b in R:
    assert src.count(a) == 1, (a[:100], src.count(a))
    src = src.replace(a, b)
a1 = '"what_was_missed_v378", "bancada_fase4_v378")}'
n1 = src.count(a1); assert n1 == 2, n1
src = src.replace(a1, '"what_was_missed_v378", "bancada_fase4_v378", ' + ", ".join('"%s"' % k for k in K379) + ')}')
a2 = '"what_was_missed_v378", "bancada_fase4_v378") if c[k].get("all_verified")'
n2 = src.count(a2); assert n2 == 1, n2
src = src.replace(a2, '"what_was_missed_v378", "bancada_fase4_v378", ' + ", ".join('"%s"' % k for k in K379) + ') if c[k].get("all_verified")')
out = os.path.join(HERE, "ensaio_a_seco_v379.py")
open(out, "w", encoding="utf-8", newline="").write(src)
ast.parse(src)
print("ok", out, "| listas ampliadas:", n1, n2)
