# -*- coding: utf-8 -*-
"""_adapt_tudo_sem_aspas_v409.py -- (claude-construtor-v409) a varredura das aspas (conferir_citacoes_v409.py) reprovou «tudo na v409» entre « » em delta_v409.py e pos_rito/registrar_mapa_v409.py: e' um ROTULO da
gerencia/do construtor para a ordem, nao fala verbatim (a fala, sha16 fb3dc69e3c9b5516, diz «eu quero que entre tudo na versão 409 não deixar nada para a v410»). A CAUSA e' minha (escrevi o rotulo entre « »):
o rotulo perde as aspas angulares (vira: a ordem de tudo entrar na v409), aqui e no p00. O teste nao muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
for rel, n in (("delta_v409.py", 2), ("p00_precondicoes_v409.py", 2), ("pos_rito/registrar_mapa_v409.py", 1)):
    a = Arq(rel)
    a.troca("a ordem «tudo na v409»", "a ordem de tudo entrar na v409", n) if a.t.count("a ordem «tudo na v409»") == n else a.troca("ordem «tudo na v409»", "ordem de tudo entrar na v409", n)
    a.grava()
