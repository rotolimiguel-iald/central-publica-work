# -*- coding: utf-8 -*-
"""_adapt_lote1_v409.py -- (claude-construtor-v409, 05/11/2026) adapta copiar_base_v409.py (so' a docstring: o sha16 da v408 selada e' o do DESENHO_v409; o corpo ja' le tudo do delta)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("copiar_base_v409.py")
a.troca("# [ADAPTADO v409, 04/11/2026] copia de bytes do Nos v408 SELADO (833121339e649f71) para base_v408; so' o sha16 da docstring e esta linha mudaram sobre a subida de rotulo\n",
        "# (v408: a linha [ADAPTADO] anterior era da v408 sobre a v407)\n")
a.troca("(833121339e649f71; o arquivo manda; o 0030242565cc13f6 que o molde trazia era o da v405, herdado por subida de rotulo)", "(o sha16 do DESENHO_v409, lido de delta_v409.BASE_SHA16_DA_ORDEM; o arquivo manda)")
a.marca("copia de bytes do Nos v408 SELADO para base_v408; so' a docstring mudou sobre a subida de rotulo (o sha16 da base vem do delta)")
a.grava()
