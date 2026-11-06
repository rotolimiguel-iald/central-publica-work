# -*- coding: utf-8 -*-
"""_fix_e25_g1_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA de a E25 ainda reprovar no portao de textos do G1 (provada sem estatuto na mesma frase): o portao corta a frase em «;», e o estatuto
estava depois de um «;» dentro do parentese («(a_trava_no_nome; validade no kernel, nao creditacao)»). O estatuto passa para a MESMA frase, sem «;» no meio: «provada no kernel, validade no kernel e nao creditacao (a_trava_no_nome)»."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
d = Arq("delta_v409.py")
d.troca("a trava esta' provada no kernel (a_trava_no_nome; validade no kernel, nao creditacao)", "a trava esta' provada no kernel, validade no kernel e nao creditacao (a_trava_no_nome)")
d.grava()
r = Arq("registros_v409.py")
r.troca("o operador corrigiu e a trava esta' provada no kernel (a_trava_no_nome; validade no kernel, nao creditacao)", "o operador corrigiu e a trava esta' provada no kernel, validade no kernel e nao creditacao (a_trava_no_nome)")
r.grava()
