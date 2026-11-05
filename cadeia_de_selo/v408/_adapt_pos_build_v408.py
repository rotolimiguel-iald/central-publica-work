# -*- coding: utf-8 -*-
"""_adapt_pos_build_v408.py -- adapta pos_build_kernel_v408.py (subida mecanica do molde v407) ao bundle de 4 modulos de TGLExt/ da v408 (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; 41 ancoras; bandeiras ext_tt408_*).
Substituicoes de contagem EXATA; backup de bytes; retira a marca [A ADAPTAR v408]. Molde: v407/_adapt_pos_build_v407.py. Escrito pela ferramenta Write (o heredoc do Bash colapsa barras invertidas)."""
import ast
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pos_build_kernel_v408.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8")
assert "\r\n" not in t
BS = "\\"   # uma barra invertida (o texto do arquivo traz duas seguidas dentro das docstrings: C:\\t\\k408c\\final)


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:90], t.count(old), n)
    t = t.replace(old, new)


t = re.sub(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n", "# [ADAPTADO v408, 04/11/2026] o bundle e' de 4 modulos de TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP); ancoras = os #print axioms das fontes normalizadas (41); bandeiras ext_tt408_*\n", t, count=1)
sub("# [ADAPTADO v408] o bundle e' de 9 modulos de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11); ancoras = os #print axioms das candidatas; bandeiras ext_psi407_*\n", "")   # (a nota da v407, ja' rotulada pelo bump: sai; a nota nova entrou acima)
sub('"delta_vs_v406": {"decl": j1[0], "thm": j1[1]}', '"delta_vs_v407": {"decl": j1[0], "thm": j1[1]}')   # (delta_vs_v406 e' chave do um.py v407 e por isso o bump a protegeu; aqui e' a medida desta geracao: contra a v407)
sub('"| delta_vs_v406:", j1[:2]', '"| delta_vs_v407:", j1[:2]')
sub("(build a FRIO dos 9 modulos novos de TGLExt/ no sandbox C:" + BS * 2 + "t" + BS * 2 + "k408c" + BS * 2 + "final)", "(build a FRIO dos 4 modulos novos de TGLExt/ no sandbox C:" + BS * 2 + "t" + BS * 2 + "k408c" + BS * 2 + "final)")
sub("linha BUILT (nao Replayed) de CADA um dos 9 modulos", "linha BUILT (nao Replayed) de CADA um dos 4 modulos")
sub("confere as ANCORAS das 9 pedras (delta_v408.ANCORAS) e deriva FLAGS_v408.json (as declaracoes\nNOMEADAS publicas dos 9 modulos, politica da v394: UMA serie ext_psi408_NNNN",
    "confere as ANCORAS das 4 pedras (delta_v408.ANCORAS) e deriva FLAGS_v408.json (as declaracoes\nNOMEADAS publicas dos 4 modulos, politica da v394: UMA serie ext_tt408_NNNN")
sub('chk("a lista dos modulos novos (kernel_modulos_novos_v408.json) == os 9 do delta (PsionCanto, Par e as sete pedras de 02/11), sem repeticao",\n        N_NOVOS == 9 and len(NEWMODS) == 9 and',
    'chk("a lista dos modulos novos (kernel_modulos_novos_v408.json) == os 4 do delta (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), sem repeticao",\n        N_NOVOS == 4 and len(NEWMODS) == 4 and')
sub("a raiz do sandbox == a raiz do Nos (v407 selada) + os NOVE imports do delta (ROOT_SUFFIX), em bytes", "a raiz do sandbox == a raiz do Nos (v407 selada) + os QUATRO imports do delta (ROOT_SUFFIX), em bytes")
sub("# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v407 selado + os nove imports", "# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v407 selado + os quatro imports")
sub("# ------------------------------------------------------------------ as ANCORAS das 9 pedras (os #print axioms das candidatas)", "# ------------------------------------------------------------------ as ANCORAS das 4 pedras (os #print axioms das fontes normalizadas)")
sub('chk("as %d ANCORAS das 9 pedras (delta_v408.ANCORAS) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo esperado" % len(DL.ANCORAS), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) > 0, anc_bad[:3])',
    'chk("as %d ANCORAS das 4 pedras (delta_v408.ANCORAS) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo esperado" % len(DL.ANCORAS), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS, anc_bad[:3])')
sub("# (os 9 modulos do bundle moram em TGLExt/ (nao ha subpasta nova): o invariante e' que os 9 NAO existiam no Nos v407", "# (os 4 modulos do bundle moram em TGLExt/ (nao ha subpasta nova): o invariante e' que os 4 NAO existiam no Nos v407")
sub("UMA serie ext_psi408_NNNN ordenada por (modulo, nome)", "UMA serie ext_tt408_NNNN ordenada por (modulo, nome)")
sub('chk("o lema das duas faces (the_psion_is_the_corner_on_both_faces) e o par (o_par_de_psions_e_o_graviton) tem bandeira", all(bandeira_testemunha.values()), bandeira_testemunha)',
    'chk("a ancora principal (tetelestai) e a do tempo (o_tempo_e_a_moeda) tem bandeira; as quatro ancoras principais (uma por modulo) tem bandeira", all(bandeira_testemunha.values()) and all(chave_de.get(n_) for n_ in DL.ANCORAS_PRINCIPAIS), bandeira_testemunha)')
sub("(informativo) duracao do `lake build` a frio dos 9 modulos < 2400 s", "(informativo) duracao do `lake build` a frio dos 4 modulos < 2400 s")
sub("(copia do kernel do NOS v407 compilado pelo rito de 03/11) e A FRIO nos \" + str(N_NOVOS) + \" modulos novos (PsionCanto, Par e as sete pedras de 02/11; linha Built em cada um)",
    "(copia do kernel do NOS v407 compilado pelo rito de 04/11) e A FRIO nos \" + str(N_NOVOS) + \" modulos novos (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; linha Built em cada um)")
sub("o recibo v408 lista os \" + str(N_NOVOS) + \" modulos NOVOS de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11) e a \"", "o recibo v408 lista os \" + str(N_NOVOS) + \" modulos NOVOS de TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP) e a \"")
sub("(preparacao, 03/11/2026)", "(preparacao, 04/11/2026)")
sub("como na v393, v394, v396, v404 e v407", "como na v393, v394, v396, v404, v406 e v407")
assert "[A ADAPTAR" not in t and "PsionCanto" not in t and "ext_psi" not in t, [l_ for l_ in t.split("\n") if "PsionCanto" in l_ or "ext_psi" in l_][:3]
ast.parse(t)
open(P, "wb").write(t.encode("utf-8"))
print("ok", len(t))
