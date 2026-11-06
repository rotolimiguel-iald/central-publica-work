# -*- coding: utf-8 -*-
"""_adapt_pos_build_v409.py -- (claude-construtor-v409, 05/11/2026) adapta pos_build_kernel_v409.py (subida mecanica da v408) ao bundle de UM modulo (TraducaoTuring): contagens, textos das checagens e notas;
a chave delta_vs_v407 do KH_N1 vira delta_vs_v408 (a v409 mede contra a v408). Trocas com contagem exata (_adapt_util_v409)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("pos_build_kernel_v409.py")
a.troca("# [ADAPTADO v409, 04/11/2026] o bundle e' de 4 modulos de TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP); ancoras = os #print axioms das fontes normalizadas (41); bandeiras ext_tt408_*\n",
        "# (v409: o bundle e' de UM modulo de TGLExt/ (TraducaoTuring); ancoras = os 62 #print axioms da fonte normalizada; bandeiras ext_tu409_*; a origem do sandbox e' C:\\t\\k408c\\final)\n")
a.troca("(build a FRIO dos 4 modulos novos de TGLExt/ no sandbox", "(build a FRIO do modulo novo de TGLExt/ no sandbox")
a.troca("linha BUILT (nao Replayed) de CADA um dos 4 modulos, da raiz", "linha BUILT (nao Replayed) do modulo novo, da raiz")
a.troca("confere as ANCORAS das 4 pedras (delta_v409.ANCORAS)", "confere as ANCORAS da pedra (delta_v409.ANCORAS)")
a.troca("NOMEADAS publicas dos 4 modulos, politica da v394: UMA serie ext_tt409_NNNN", "NOMEADAS publicas do modulo, politica da v394: UMA serie ext_tu409_NNNN")
a.troca('    chk("a lista dos modulos novos (kernel_modulos_novos_v409.json) == os 4 do delta (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), sem repeticao",\n        N_NOVOS == 4 and len(NEWMODS) == 4 and',
        '    chk("a lista dos modulos novos (kernel_modulos_novos_v409.json) == o UM do delta (TraducaoTuring), sem repeticao",\n        N_NOVOS == 1 and len(NEWMODS) == 1 and')
a.troca("# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v408 selado + os quatro imports", "# ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v408 selado + o import")
a.troca('"a raiz do sandbox == a raiz do Nos (v408 selada) + os QUATRO imports do delta (ROOT_SUFFIX), em bytes"', '"a raiz do sandbox == a raiz do Nos (v408 selada) + o import do delta (ROOT_SUFFIX), em bytes"')
a.troca("# ------------------------------------------------------------------ as ANCORAS das 4 pedras (os #print axioms das fontes normalizadas)", "# ------------------------------------------------------------------ as ANCORAS da pedra (os #print axioms da fonte normalizada)")
a.troca('"as %d ANCORAS das 4 pedras (delta_v409.ANCORAS) existem no Audit', '"as %d ANCORAS da pedra (delta_v409.ANCORAS) existem no Audit')
a.troca("ordenada por (modulo, nome)\n    por_rel = {}", "ordenada por (modulo, nome)\n    por_rel = {}", 1)
a.troca("# (os 4 modulos do bundle moram em TGLExt/ (nao ha subpasta nova): o invariante e' que os 4 NAO existiam no Nos v408", "# (o modulo do bundle mora em TGLExt/ (nao ha subpasta nova): o invariante e' que ele NAO existia no Nos v408")
a.troca('chk("a ancora principal (tetelestai) e a do tempo (o_tempo_e_a_moeda) tem bandeira; as quatro ancoras principais (uma por modulo) tem bandeira"',
        'chk("a ancora principal (p_igual_np_no_modo_selecao) e a da traducao (a_traducao) tem bandeira; as %d ancoras principais (a principal e as de secao) tem bandeira" % len(DL.ANCORAS_PRINCIPAIS)')
a.troca("para os %d modulos do bundle de TGLExt/ (decisao da gerencia c1, v409: bundle como a v408;", "para o(s) %d modulo(s) do bundle de TGLExt/ (decisao da gerencia c1, v409: bundle como a v408, de UM modulo;")
a.troca('chk("(informativo) duracao do `lake build` a frio dos 4 modulos < 2400 s"', 'chk("(informativo) duracao do `lake build` a frio do modulo novo < 2400 s"')
a.troca('"delta_vs_v407": {"decl": j1[0], "thm": j1[1]}', '"delta_vs_v408": {"decl": j1[0], "thm": j1[1]}')
a.troca('"| delta_vs_v407:", j1[:2]', '"| delta_vs_v408:", j1[:2]')
a.troca('"gerado por pos_build_kernel_v409.py (preparacao, 04/11/2026);', '"gerado por pos_build_kernel_v409.py (preparacao, 05/11/2026);')
a.troca("(copia do kernel do NOS v408 compilado pelo rito de 04/11) e A FRIO nos \" + str(N_NOVOS) + \" modulos novos (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; linha Built em cada um)",
        "(copia de C:/t/k408c/final, o kernel da v408 compilado, com as fontes conferidas por sha256 contra o Nos v408) e A FRIO no(s) \" + str(N_NOVOS) + \" modulo(s) novo(s) (TraducaoTuring; linha Built)")
a.troca("lista os \" + str(N_NOVOS) + \" modulos NOVOS de TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP) e a ", "lista o(s) \" + str(N_NOVOS) + \" modulo(s) NOVO(s) de TGLExt/ (TraducaoTuring) e a ")
a.marca("pos_build do bundle de UM modulo (TraducaoTuring): contagens e textos das checagens; KH_N1 com delta_vs_v408")
a.grava()
