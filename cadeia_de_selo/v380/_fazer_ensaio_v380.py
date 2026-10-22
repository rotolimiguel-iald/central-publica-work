# -*- coding: utf-8 -*-
# gera ensaio_a_seco_v380.py a partir do ensaio v379 (edicoes pontuais, count == 1) -- molde _fazer_ensaio_v379.py. A v380 NAO tem kernel novo:
# o relatorio de axiomas do sandbox e o da v379 (kernel identico), copiado sob o nome do candidato v380.
import os, ast, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
V9 = os.path.join(os.path.dirname(HERE), "v379")
src = open(os.path.join(V9, "ensaio_a_seco_v379.py"), encoding="utf-8", newline="").read()
K380 = ("bancada_fases_5_6_7_v380",)
R = [
    ('TAG = "v379"', 'TAG = "v380"'),
    ('c["the_elementary_reason_v379"] = um.prove_the_elementary_reason_v379(1.0, c)\n',
     'c["the_elementary_reason_v379"] = um.prove_the_elementary_reason_v379(1.0, c)\n' + "".join('c["%s"] = um.prove_%s(1.0, c)\n' % (k, k) for k in K380)),
    ('DEVE = {"pt": ["Ao lado (v379) --- A Razão Elementar",',
     'DEVE = {"pt": ["Ao lado (v380) --- As Fases 5, 6 e 7 da Bancada Um", "a transformada radical", "FALSIFIED\\\\_AT\\\\_DELAY\\\\_LAW", "Moresco+2020", "Seis erratas ao lado", "Ao lado (v379) --- A Razão Elementar",'),
    ('        "en": ["Beside (v379) --- The Elementary Reason",',
     '        "en": ["Beside (v380) --- Phases 5, 6 and 7 of the Bench", "the radical transform", "FALSIFIED\\\\_AT\\\\_DELAY\\\\_LAW", "Moresco+2020", "Six errata beside", "Beside (v379) --- The Elementary Reason",'),
    ('    nome = "dry_v379_%s" % lang', '    nome = "dry_v380_%s" % lang'),
    ('rep["markdown_v376"] = {"v376": md.count("v379"), "carimbo": "**Versão v379**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v380"), "carimbo": "**Versão v380**" in md,'),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v379**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v380**" in open(mani, encoding="utf-8").read()}'),
]
NL = chr(13) + chr(10) if src.count(chr(13) + chr(10)) > src.count(chr(10)) // 2 else chr(10)
R = [(x.replace(chr(10), NL), y.replace(chr(10), NL)) for x, y in R]
for a, b in R:
    assert src.count(a) == 1, (a[:100], src.count(a))
    src = src.replace(a, b)
a1 = '"the_elementary_reason_v379")}'
n1 = src.count(a1); assert n1 == 2, n1
src = src.replace(a1, '"the_elementary_reason_v379", ' + ", ".join('"%s"' % k for k in K380) + ')}')
a2 = '"the_elementary_reason_v379") if c[k].get("all_verified")'
n2 = src.count(a2); assert n2 == 1, n2
src = src.replace(a2, '"the_elementary_reason_v379", ' + ", ".join('"%s"' % k for k in K380) + ') if c[k].get("all_verified")')
out = os.path.join(HERE, "ensaio_a_seco_v380.py")
open(out, "w", encoding="utf-8", newline="").write(src)
ast.parse(src)
# o relatorio de axiomas do sandbox: o da v379 (kernel identico), sob o nome do candidato v380
shutil.copyfile(os.path.join(V9, "sandbox_axiom_report__um_v379_candidato.json"), os.path.join(HERE, "sandbox_axiom_report__um_v380_candidato.json"))
shutil.copyfile(os.path.join(V9, "carregar_embutido.py"), os.path.join(HERE, "carregar_embutido.py"))
print("ok", out, "| listas ampliadas:", n1, n2, "| axiom report do sandbox copiado da v379 (kernel identico)")
