# -*- coding: utf-8 -*-
"""_fix_comparar_p2_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) o comparar_v410_v411.py (do fork A) foi escrito ANTES do aditivo da gerencia de 12/11 (o P2 ao lado da v387: o patch W13_p2_v387_pt/en, uma
instrucao NOVA em build_pt e build_en, antes da linha do veredito da v387). A causa da reprovacao: o mapa dos patches nao conhecia W13 e a contagem das instrucoes novas era +5. O conserto: o W13 no mapa (build_pt / build_en),
+6 instrucoes, e uma checagem propria (a frase ao lado do P2 uma vez, logo ANTES da linha do veredito selado da v387, que fica). Backup de BYTES antes; ancoras unicas; ast.parse. uso: python -B -X utf8 _fix_comparar_p2_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "comparar_v410_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
PARES = [
    ('    for _p in ("W06_topo_", "W07_troca1_", "W03_quadro_", "W03b_remissao_", "W10_estatuto_", "W08_troca2_", "W08_troca2_metodo_", "W11_coracao_"):',
     '    for _p in ("W06_topo_", "W07_troca1_", "W03_quadro_", "W03b_remissao_", "W10_estatuto_", "W08_troca2_", "W08_troca2_metodo_", "W11_coracao_", "W13_p2_v387_"):   # (v411, aditivo da gerencia de 12/11: W13, o P2 ao lado da v387)'),
    ('    s_ = acha("_v411_secao_tex(core, \'%s\'" % lg); t_ = acha("_v411_topo_texto(core, \'%s\')" % lg)\n',
     '    s_ = acha("_v411_secao_tex(core, \'%s\'" % lg); t_ = acha("_v411_topo_texto(core, \'%s\')" % lg)\n    p2_ = acha("_v411_p2_ao_lado_tex(core, \'%s\')" % lg)   # (v411, aditivo de 12/11) o P2 ao lado da v387\n'),
    ('    return {"nada_removido_so_insercao_ou_troca": all(op[0] in ("insert", "replace") for op in ops) and len(b) == len(a) + 5,\n',
     '    return {"nada_removido_so_insercao_ou_troca": all(op[0] in ("insert", "replace") for op in ops) and len(b) == len(a) + 6,   # (v411: +6 -- o quadro, a remissao, o estatuto, o coracao, a secao e o P2 ao lado da v387)\n'
     '            "o_p2_ao_lado_uma_vez_logo_antes_da_linha_do_veredito_da_v387": len(p2_) == 1 and "three_stress_tests_v387" in vizinho(p2_[0], 1) and "_sec3s.append" in tb[p2_[0]],\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
