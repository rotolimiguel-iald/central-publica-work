# -*- coding: utf-8 -*-
"""_adapt_harness_v407_irma_v409.py -- (claude-construtor-v409) o harness do fechar copia ao sandbox as pastas IRMAS que os deltas e as conferencias importam por caminho; a lista (fork B) tinha v408, v406..v399
e deixou de fora a v407 -- mas acom_conferencias_v408.py importa acom_conferencias_v407.py (e o delta_v408 le a v407): o conferidor no sandbox caia em FileNotFoundError, e o fechar_v409 saia rc 1 sem recusar.
A causa (a irma ausente) e' corrigida: a v407 entra nas duas listas (os arquivos pequenos do topo e a pedra). Nenhuma conferencia muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_rito/harness_fechar_sandbox_v409.py")
a.troca('''for _vv in ("v408", "v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):''', '''for _vv in ("v408", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):   # (v409: a v407 entra -- acom_conferencias_v408 importa acom_conferencias_v407)''')
a.troca('''for _vp in ("v408", "v406", "v405", "v404", "v403", "v402", "v401", "v399"):''', '''for _vp in ("v408", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v399"):''')
a.grava()
