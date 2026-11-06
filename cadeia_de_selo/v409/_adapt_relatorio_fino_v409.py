# -*- coding: utf-8 -*-
"""_adapt_relatorio_fino_v409.py -- (claude-construtor-v409) dois avisos do relatorio diziam o estado anterior: as erratas (E24, E25 e E26 -> E24 a E28 e a E21 ao lado) e a origem das falas novas (as tres ultimas,
nao as duas, vieram dos AO LADO do fim do DESENHO: a 11a, a 12a e a 13a, a ordem de tudo entrar na v409). So' texto; os portoes nao mudam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_relatorio_v409.py")
a.troca('"as erratas E24, E25 e E26 sao da gerencia c1, em nome proprio:', '"as erratas E24 a E28 e a E21 ao lado sao da gerencia c1, em nome proprio:')
a.troca("as duas ultimas vieram dos AO LADO do fim do DESENHO", "as tres ultimas vieram dos AO LADO do fim do DESENHO: a 11a, a 12a e a 13a, a ordem de tudo entrar na v409")
a.grava()
