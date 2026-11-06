# -*- coding: utf-8 -*-
"""_adapt_forkB_v409_d.py -- (claude-construtor-v409, fork B, 05/11/2026) quarta passada: a nota herdada dos dois recibos do servico citava a data da ordem anterior (o conferidor do servico proibe qualquer data de autorizacao anterior no texto). Troca de contagem exata; backup de bytes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
for rel in ("bancada_B3_servico/recibo_parada_v409.py", "bancada_B3_servico/recibo_religamento_v409.py"):
    a = Arq(rel)
    a.troca("(nota herdada da adaptacao da v408 [fork C, 04/11/2026], com os rotulos subidos;", "(nota herdada da adaptacao da v408 [fork C da cadeia v408], com os rotulos subidos;")
    a.grava()
