# -*- coding: utf-8 -*-
"""_dois_modulos_pos_build_v409.py -- (claude-construtor-v409, 05/11/2026) pos_build_kernel_v409.py: o bundle passa a DOIS modulos (TraducaoTuring, ParNaFaceDeFock); a conferencia da lista dos modulos novos
compara com o delta (2), nao com UM. O resto do pos-build ja' e' generico no numero de modulos."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_build_kernel_v409.py")
a.troca('''    chk("a lista dos modulos novos (kernel_modulos_novos_v409.json) == o UM do delta (TraducaoTuring), sem repeticao",
        N_NOVOS == 1 and len(NEWMODS) == 1 and''', '''    chk("a lista dos modulos novos (kernel_modulos_novos_v409.json) == os DOIS do delta (TraducaoTuring, ParNaFaceDeFock), sem repeticao",
        N_NOVOS == DL.N_BUNDLE == 2 and len(NEWMODS) == 2 and''')
a.grava()
