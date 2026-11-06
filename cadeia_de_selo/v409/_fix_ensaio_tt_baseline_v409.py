# -*- coding: utf-8 -*-
"""_fix_ensaio_tt_baseline_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA da unidade tetelestai_terminal_v408_os_numeros_foram_recalculados_aqui = False: o bloco herdado (copia do bloco da v408)
comparava o baseline do contrato do terminal com o um.py da BASE desta cadeia (agora a v408 selada); o baseline do terminal e' a v407 (a base da v408). Faz-se como o bloco herdado do psion ja' faz
(_CP7 baseline contra _CM7 base_v406_sha16): o baseline do terminal contra o base_v407_sha16 do CANDIDATO_v408.json. Nada relaxado: a mesma igualdade, contra a base certa."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("ensaio_a_seco_v409.py")
a.troca('and _CP8["baseline"]["ladder"] == _CM8["escada"][0] and _CP8["baseline"]["sha256"] == hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()',
        'and _CP8["baseline"]["ladder"] == _CM8["escada"][0] and _CP8["baseline"]["sha256"][:16] == _CM8["base_v407_sha16"]   # (v409: o baseline do terminal e\' a v407, a base da v408)')
a.grava()
