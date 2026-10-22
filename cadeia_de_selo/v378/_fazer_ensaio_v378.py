# -*- coding: utf-8 -*-
# gera ensaio_a_seco_v378.py a partir do ensaio v377 (edicoes pontuais, count == 1) -- molde _fazer_ensaio_v377.py
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.join(os.path.dirname(HERE), "v377")
src = open(os.path.join(V7, "ensaio_a_seco_v377.py"), encoding="utf-8", newline="").read()
K378 = ("the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378")
R = [
    ('TAG = "v377"', 'TAG = "v378"'),
    ('    if k.startswith(("ext_pir_", "ext_dis_")):', '    if k.startswith(("ext_dlc_",)):'),
    ('c["final_stone_reading_v377"] = um.prove_final_stone_reading_v377(1.0, c)\n',
     'c["final_stone_reading_v377"] = um.prove_final_stone_reading_v377(1.0, c)\n' + "".join('c["%s"] = um.prove_%s(1.0, c)\n' % (k, k) for k in K378)),
    ('DEVE = {"pt": ["Ao lado (v377) --- A lei da dissipação, provada",',
     'DEVE = {"pt": ["Ao lado (v378) --- O que faltou", "TheFlowLawContrast", "(E12) Leitura ao lado do parágrafo v377", "A lei da dissipação com contraste", "A Fase 4 da Bancada Um", "circularidade declarada no pré-registro", "desfavorecem", "Ao lado (v377) --- A lei da dissipação, provada",'),
    ('        "en": ["Beside (v377) --- The dissipation law, proved",',
     '        "en": ["Beside (v378) --- What was missed", "TheFlowLawContrast", "(E12) Reading beside the v377 paragraph", "The dissipation law with contrast", "Phase 4 of the Bench", "circularity declared in the pre-registration", "disfavour", "Beside (v377) --- The dissipation law, proved",'),
    ('    nome = "dry_v377_%s" % lang', '    nome = "dry_v378_%s" % lang'),
    ('rep["markdown_v376"] = {"v376": md.count("v377"), "carimbo": "**Versão v377**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v378"), "carimbo": "**Versão v378**" in md,'),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v377**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v378**" in open(mani, encoding="utf-8").read()}'),
]
NL = chr(13) + chr(10) if src.count(chr(13) + chr(10)) > src.count(chr(10)) // 2 else chr(10)
R = [(x.replace(chr(10), NL), y.replace(chr(10), NL)) for x, y in R]
for a, b in R:
    assert src.count(a) == 1, (a[:100], src.count(a))
    src = src.replace(a, b)
a1 = '"bancada_fases_v377", "final_stone_reading_v377")}'
n1 = src.count(a1); assert n1 == 2, n1
src = src.replace(a1, '"bancada_fases_v377", "final_stone_reading_v377", ' + ", ".join('"%s"' % k for k in K378) + ')}')
a2 = '"bancada_fases_v377", "final_stone_reading_v377") if c[k].get("all_verified")'
n2 = src.count(a2); assert n2 == 1, n2
src = src.replace(a2, '"bancada_fases_v377", "final_stone_reading_v377", ' + ", ".join('"%s"' % k for k in K378) + ') if c[k].get("all_verified")')
out = os.path.join(HERE, "ensaio_a_seco_v378.py")
open(out, "w", encoding="utf-8", newline="").write(src)
ast.parse(src)
print("ok", out, "| listas ampliadas:", n1, n2)
