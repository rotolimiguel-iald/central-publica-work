# -*- coding: utf-8 -*-
"""_adapt_citacoes_remove_apontadas_v409.py -- (claude-construtor-v409) a gerencia corrigiu nos insumos as tres citacoes que eu tinha APONTADO (a fala sem a virgula a mais; as duas frases que nao sao do operador
passaram de « » a “ ”): as tres entradas saem de _APONTADAS_PEDRAS, para que a varredura volte a REPROVAR se elas reaparecerem entre « » (nada fica abonado sem necessidade)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("conferir_citacoes_v409.py")
i0 = a.t.index('''escrita entre « » na docstring de p_igual_np_no_modo_selecao",\n    "com ele a igualdade vale relativa a ele": ''')
i1 = a.t.index('''    "eu quero que entre tudo na versão 409, não deixar nada para a v410": ''', i0)
j1 = a.t.index("\n", i1)
bloco = a.t[i0:j1]
assert bloco.endswith('"}'), bloco[-60:]
a.troca(bloco, '''escrita entre « » na docstring de p_igual_np_no_modo_selecao"}''')
a.grava()
