# -*- coding: utf-8 -*-
# gera ensaio_a_seco_v377.py a partir do ensaio v376 (edicoes pontuais, count == 1) -- molde _fazer_ensaio_v376.py
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(os.path.dirname(HERE), "v376")
src = open(os.path.join(V6, "ensaio_a_seco_v376.py"), encoding="utf-8", newline="").read()
K377 = ("physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377")
K376 = ("light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376",
        "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376")
R = [
    ('TAG = "v376"', 'TAG = "v377"'),
    ('    if k.startswith(("ext_lrs_", "ext_kir_", "ext_wio_")):', '    if k.startswith(("ext_pir_", "ext_dis_")):'),
    ('c["tetelestai_conference_v376"] = um.prove_tetelestai_conference_v376(1.0, c)\n',
     'c["tetelestai_conference_v376"] = um.prove_tetelestai_conference_v376(1.0, c)\n'
     + "".join('c["%s"] = um.prove_%s(1.0, c)\n' % (k, k) for k in K377)),
    ('DEVE = {"pt": ["Ao lado (v376) --- O todo é um",',
     'DEVE = {"pt": ["Ao lado (v377) --- A lei da dissipação, provada", "TheFlowLawD1a", "PhysicsIsTheReading", "(E10) Errata ao lado do módulo de Coma", "(E11) errata ao lado do D1 V3", "O desvio de", "Ao lado (v376) --- O todo é um",'),
    ('        "en": ["Beside (v376) --- The whole is one",',
     '        "en": ["Beside (v377) --- The dissipation law, proved", "TheFlowLawD1a", "PhysicsIsTheReading", "(E10) Erratum beside the Coma module", "(E11) erratum beside the D1 V3", "The deviation from", "Beside (v376) --- The whole is one",'),
    ('    nome = "dry_v376_%s" % lang', '    nome = "dry_v377_%s" % lang'),
    ('rep["markdown_v376"] = {"v376": md.count("v376"), "carimbo": "**Versão v376**" in md,', 'rep["markdown_v376"] = {"v376": md.count("v377"), "carimbo": "**Versão v377**" in md,'),
    ('rep["manifest_v376"] = {"carimbo": "**Versão v376**" in open(mani, encoding="utf-8").read()}', 'rep["manifest_v376"] = {"carimbo": "**Versão v377**" in open(mani, encoding="utf-8").read()}'),
]
NL = chr(13) + chr(10) if src.count(chr(13) + chr(10)) > src.count(chr(10)) // 2 else chr(10)
R = [(x.replace(chr(10), NL), y.replace(chr(10), NL)) for x, y in R]
for a, b in R:
    assert src.count(a) == 1, (a[:100], src.count(a))
    src = src.replace(a, b)
# as duas listas de "falhas" e de "nao selados" tambem ganham as chaves v377 (ocorrencias multiplas: todas as que fecham com tetelestai_conference_v376")}" ou ') if c[k]')
a1 = '"coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376")}'
n1 = src.count(a1)
src = src.replace(a1, '"coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376", ' + ", ".join('"%s"' % k for k in K377) + ')}')
a2 = '"coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376") if c[k].get("all_verified")'
n2 = src.count(a2)
src = src.replace(a2, '"coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376", ' + ", ".join('"%s"' % k for k in K377) + ') if c[k].get("all_verified")')
out = os.path.join(HERE, "ensaio_a_seco_v377.py")
open(out, "w", encoding="utf-8", newline="").write(src)
ast.parse(src)
print("ok", out, "| listas ampliadas:", n1, n2)
