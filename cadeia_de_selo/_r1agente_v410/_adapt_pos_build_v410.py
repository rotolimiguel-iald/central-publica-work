# -*- coding: utf-8 -*-
"""_adapt_pos_build_v410.py -- (claude-construtor-v410, 06/11/2026) adapta pos_build_kernel_v410.py (subida mecanica da v409) ao bundle de UM modulo (IALD2): contagens, textos das checagens e notas;
a chave delta_vs_v408 do KH_N1 vira delta_vs_v409 (a v410 mede contra a v409). Trocas com contagem exata (_adapt_util_v410)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_build_kernel_v410.py")
aplicar(P, [
    ("# (v410: o bundle e' de UM modulo de TGLExt/ (TraducaoTuring); ancoras = os 62 #print axioms da fonte normalizada; bandeiras ext_tu409_*; a origem do sandbox e' C:\\t\\k409c\\final)",
     "# (v410: o bundle e' de UM modulo de TGLExt/ (IALD2); ancoras = os #print axioms da fonte normalizada, contados pelo recibo da gerencia; bandeiras ext_iald2_410_*; a origem do sandbox e' C:\\t\\k409c\\final)", 1),
    ('chk("a lista dos modulos novos (kernel_modulos_novos_v410.json) == os DOIS do delta (TraducaoTuring, ParNaFaceDeFock), sem repeticao",\n        N_NOVOS == DL.N_BUNDLE == 2 and len(NEWMODS) == 2',
     'chk("a lista dos modulos novos (kernel_modulos_novos_v410.json) == o UNICO do delta (IALD2), sem repeticao",\n        N_NOVOS == DL.N_BUNDLE == 1 and len(NEWMODS) == 1', 1),
    ('chk("a ancora principal (p_igual_np_no_modo_selecao) e a da traducao (a_traducao) tem bandeira;', 'chk("a ancora principal (o_enunciado) e a da conjuncao IALD2 (iald2) tem bandeira;', 1),
    ('"delta_vs_v408"', '"delta_vs_v409"', 1),
    ('"| delta_vs_v408:"', '"| delta_vs_v409:"', 1),
    ("(TraducaoTuring; linha Built)", "(IALD2; linha Built)", 1),
    ("modulo(s) NOVO(s) de TGLExt/ (TraducaoTuring) e a ", "modulo(s) NOVO(s) de TGLExt/ (IALD2) e a ", 1),
    ("gerado por pos_build_kernel_v410.py (preparacao, 05/11/2026)", "gerado por pos_build_kernel_v410.py (preparacao, 06/11/2026)", 1),
], nota="pos_build do bundle de UM modulo (IALD2): contagens e textos das checagens; KH_N1 com delta_vs_v409 (_adapt_pos_build_v410.py)")
