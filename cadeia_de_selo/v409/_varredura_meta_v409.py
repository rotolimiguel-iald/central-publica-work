# -*- coding: utf-8 -*-
"""_varredura_meta_v409.py -- (claude-construtor-v409) a varredura trata como META (a definicao da guarda, nao texto que sai): guarda_frases_v409.py inteiro (as listas PROIBIDAS e LIMPAS sao testadas pelo controle
negativo dela) e os comentarios da propria guarda em runtime_v409.py (os que descrevem o que ela reprova: «dito em aberto», «no MESMO trecho»)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("varredura_fock_omega_v409.py")
a.troca('''    if b_ == "guarda_frases_v409.py":   # as listas de PROIBIDAS/sondas sao a definicao da guarda
        i_p_ = next((i_ for i_ in range(len(linhas_)) if linhas_[i_].startswith("PROIBIDAS = ")), 0)
        idx_ = [i_ for i_ in idx_ if i_ > i_p_]''', '''    if b_ == "guarda_frases_v409.py":   # META: as listas PROIBIDAS e LIMPAS sao a definicao da guarda (o controle negativo dela as testa)
        idx_ = []''')
a.troca('''"f41", "f40", "f42",''', '''"f41", "f40", "f42", "dito em aberto", "no mesmo trecho",''')
a.grava()
