# -*- coding: utf-8 -*-
"""_fix_topo_recuo_variantes_ensaio_v411.py -- (claude-construtor-v411, fork C, 12/11/2026; CONDICAO 3(a) da gerencia c1, segunda metade)
os dois ARTIGOS DE RECUO que o ensaio compila de verdade -- a variante sem o registro teste_de_veracidade_fase9_v397 (o topo diz que nao da' o
resultado porque a fonte de um marcador falta) e a variante sem os registros da v411 (o topo diz que o registro do H0DN v411 nao selou) --
NUNCA passam como selo: a conferencia independente (topo_com_resultado_v411.confere) os REPROVA, tanto com o core da variante quanto com o core
completo do ensaio, e a frase de recuo propria de cada um esta' la'. Entram como chaves novas de rep["variante"] e rep["variante_v411"] e no
mau_var / mau_var11 (o ensaio FALHA se um artigo de recuo passar). Backup de BYTES antes; ancoras unicas; ast.parse.
uso: python -B -X utf8 _fix_topo_recuo_variantes_ensaio_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
_REP = '_TR11.confere(%s, lang, %s, "txt", um._V411_TOPO, um._v411_tex_misto, um._tex_to_txt)["ok"] is False'
PARES = [
    ('    rep["variante"][lang] = {"rc": _r2, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),\n',
     '    rep["variante"][lang] = {"rc": _r2, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),\n'
     '                             "topo_de_recuo_sem_a_v397_nao_passa_como_selo": bool(_TR11.RECUO[lang][0] in fl and ' + (_REP % ("cv", "_x")) + ' and ' + (_REP % ("c", "_x")) + '),   # (condicao 3(a) da gerencia c1)\n'),
    ('           or v["rc_hms13_v410"] != [0] or not v["frase_guarda_hms13_v410"] or not v["so_a_guarda_do_hms13_quando_so_ele_falta"]]   # (parte 2) as duas variantes novas e as guardas especificas\n',
     '           or v["rc_hms13_v410"] != [0] or not v["frase_guarda_hms13_v410"] or not v["so_a_guarda_do_hms13_quando_so_ele_falta"]   # (parte 2) as duas variantes novas e as guardas especificas\n'
     '           or not v["topo_de_recuo_sem_a_v397_nao_passa_como_selo"]]   # (condicao 3(a) da gerencia c1, 12/11) o artigo de recuo nunca passa como selo\n'),
    ('    rep["variante_v411"][lang] = {"rc": _r211v, "frases_de_guarda_na_variante": {g_: g_ in fl11 for g_ in _g11}, "frases_de_guarda_ausentes_no_texto_completo": {g_: g_ not in flc11 for g_ in _g11}}\n'
     'mau_var11 = [l for l, v in rep["variante_v411"].items() if v["rc"] != [0] or not all(v["frases_de_guarda_na_variante"].values()) or not all(v["frases_de_guarda_ausentes_no_texto_completo"].values())]\n',
     '    rep["variante_v411"][lang] = {"rc": _r211v, "frases_de_guarda_na_variante": {g_: g_ in fl11 for g_ in _g11}, "frases_de_guarda_ausentes_no_texto_completo": {g_: g_ not in flc11 for g_ in _g11},\n'
     '                                  "topo_de_recuo_sem_o_registro_nao_passa_como_selo": bool(_TR11.RECUO[lang][1] in fl11 and ' + (_REP % ("cv11", "_x11v")) + ' and ' + (_REP % ("c", "_x11v")) + ')}   # (condicao 3(a) da gerencia c1)\n'
     'mau_var11 = [l for l, v in rep["variante_v411"].items() if v["rc"] != [0] or not all(v["frases_de_guarda_na_variante"].values()) or not all(v["frases_de_guarda_ausentes_no_texto_completo"].values()) or not v["topo_de_recuo_sem_o_registro_nao_passa_como_selo"]]\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_topo_recuo_variantes"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
