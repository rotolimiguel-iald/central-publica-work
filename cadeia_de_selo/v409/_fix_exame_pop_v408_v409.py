# -*- coding: utf-8 -*-
"""_fix_exame_pop_v408_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA de «bloco_mexeu_em_chaves_existentes» no exame_pontos_v409 (chaves mexidas: cunhagens_v408, kh_n1_cobertura_v408, tetelestai_terminal_v408):
o exame retira do core da base, ANTES de executar o bloco do main, as chaves que o fluxo RECRIA (as da v393 a v407); faltavam as da v408 (tetelestai_terminal_v408 e os specs da v408), que na v409 sao HERDADAS e recriadas
pelo mesmo bloco (a escada do contrato subida pela C12; a errata E26 e os pisos da C13 ao lado). Acrescentam-se as da v408 a lista, como a v408 fez com as da v407; a comparacao delas com o core0 continua nos pontos herdados."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("exame_pontos_v409.py")
a.troca('+ list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS):\n    core.pop(n_, None)',
        '+ list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS):   # (v409: + os da v408, HERDADOS e recriados pelo bloco)\n    core.pop(n_, None)')
a.grava()
