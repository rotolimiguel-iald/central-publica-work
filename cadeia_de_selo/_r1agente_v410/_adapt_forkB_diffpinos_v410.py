# -*- coding: utf-8 -*-
"""_adapt_forkB_diffpinos_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) adapta a v410 o diff_e_pinos_v410.py. O CORPO da subida mecanica foi conferido linha a linha no diff contra o
original da v409 e esta' certo para a v410 (le tudo do delta e do CANDIDATO_v410.json: N_BUNDLE = 1, BUNDLE_RELS, a raiz; a base e' v410\\base_v409; os pinos herdados do B(n) vem de v409\\PINOS_BN_v409.json,
que existe, recalculados do arquivo; o B(n) seguinte e' DL.B_N_SEGUINTE = B19 e a Bancada pina DL.BANCADA_PINA_HOJE). So' a docstring e as marcas mudam: o modulo novo e' o IALD2 (DESENHO_v410), e o molde passa a dizer
que os 2 modulos da v409, os 4 da v408, os 9 da v407 e os 301 da v406 ficam no kernel como registro. A marca [A ADAPTAR v410] e a marca antiga subida saem. Trocas de contagem exata; backup de bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_forkB_util_v410 import adaptar, linha, NOTA_FORKB  # noqa: E402

rel = "diff_e_pinos_v410.py"
l3 = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410]")
adaptar(rel, [
    (l3 + "\n", "", 1),
    ("(o modulo do bundle da v410, em TGLExt/: 1 pelo DESENHO_v409, TraducaoTuring; o numero e' o de CANDIDATO_v410.json)",
     "(o modulo do bundle da v410, em TGLExt/: 1 pelo DESENHO_v410, IALD2; o numero e' o de CANDIDATO_v410.json)", 1),
    ("Molde: diff_e_pinos_v409.py (adaptado em 05/11/2026 ao bundle de UM modulo, TraducaoTuring; os 4 da v409, os 9 da v407 e os 301 da v406 ficam no kernel como registro).",
     "Molde: diff_e_pinos_v409.py (adaptado em 06/11/2026 ao bundle de UM modulo, IALD2; os 2 da v409, os 4 da v408, os 9 da v407 e os 301 da v406 ficam no kernel como registro).", 1),
], "o corpo le tudo do delta e do CANDIDATO (1 modulo, IALD2; a raiz; o Audit nao muda); pinos herdados de v409\\PINOS_BN_v409.json (recalculados do arquivo); B19; so' a docstring mudou; " + NOTA_FORKB)
print("diff_e_pinos: ok")
