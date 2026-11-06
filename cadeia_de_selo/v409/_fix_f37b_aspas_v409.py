# -*- coding: utf-8 -*-
"""_fix_f37b_aspas_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA do citacoes rc 1 no ensaio: o comentario da F37b (escrito pelo construtor) punha entre « » uma PARAFRASE da D56 («onde P = nP e Turing aparecem JUNTOS»),
que nao e' verbatim de fala nenhuma; a regra do conferidor de citacoes (« » so' para o verbatim ou rotulo declarado) a pega com razao. Sai a aspa: a D56 e' citada por nome, sem « »."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("runtime_v409.py")
a.troca("# F37b (a OBRIGACAO LOCAL, D56: «onde P = nP e Turing aparecem JUNTOS»): o proprio trecho", "# F37b (a OBRIGACAO LOCAL da D56, onde P = nP e Turing aparecem juntos): o proprio trecho")
a.grava()
