# -*- coding: utf-8 -*-
"""_adapt_r2_ficava_v409.py -- (claude-construtor-v409) a F41b estendida reprovou o «dizia» da nota ao lado da E21 («que a ligacao do par na face de Fock ficava por fazer (fiacao), nao que faltasse»): e' o texto
HISTORICO que a errata cita (no passado). A excecao historica da F41b ganha «ficava» (o imperfeito do que a E21 dizia), ao lado de e21/v407/deixou/dizia. As sondas novas seguem reprovando (conferido no controle)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("runtime_v409.py")
a.troca('''and not any(x_ in _sl for x_ in ("e21", "v407", "deixou", "dizia")):''', '''and not any(x_ in _sl for x_ in ("e21", "v407", "deixou", "dizia", "ficava")):''')
a.grava()
