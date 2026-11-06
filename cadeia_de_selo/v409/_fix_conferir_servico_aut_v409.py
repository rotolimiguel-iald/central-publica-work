# -*- coding: utf-8 -*-
"""_fix_conferir_servico_aut_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA do Traceback no servico estatico (conferir_exigencias_servico_v409.py, linha do AUT): o AUT do orquestrador da v409
(orquestrador/pos_treino_v409.py) e' MONTADO do delta (o prefixo de sha16 da ordem e a frase, lidos de delta_v409, nada digitado) e nao e' mais um literal; o conferidor so' sabia ler literal (ast.literal_eval).
Agora: literal, como antes; se nao for, a EXPRESSAO do AUT (o no' do AST, sem executar o resto do orquestrador) e' avaliada com o delta_v409 desta pasta e a frase dele, sem builtins. A checagem que vem depois e' a mesma
(o sha16 CALCULADO do arquivo da fala esta' no AUT, a frase, a data, nenhum texto de 01/11): nada e' relaxado."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("bancada_B3_servico/conferir_exigencias_servico_v409.py")
a.troca('''        aut_orq = ast.literal_eval(n_.value)
''', '''        try:
            aut_orq = ast.literal_eval(n_.value)
        except ValueError:   # (v409) o AUT e' MONTADO do delta (sha16 e frase lidos de delta_v409): avalia-se SO' a expressao do AUT, com o delta desta pasta e a frase dele, sem builtins
            import importlib.util as _ilu9
            _sp9 = _ilu9.spec_from_file_location("delta_v409_conferir_servico", os.path.join(V, "delta_v409.py")); _dl9 = _ilu9.module_from_spec(_sp9); _sp9.loader.exec_module(_dl9)
            aut_orq = eval(compile(ast.Expression(n_.value), "AUT_do_orquestrador", "eval"), {"__builtins__": {}}, {"_DL": _dl9, "AUT_FRASE": _dl9.FRASE_ORDEM_V409})
''')
a.grava()
