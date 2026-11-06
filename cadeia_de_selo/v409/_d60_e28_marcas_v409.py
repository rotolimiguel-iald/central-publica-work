# -*- coding: utf-8 -*-
"""_d60_e28_marcas_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA de a D60 revista reprovar na F43: ela fala da maquina de Turing com oraculo e nao trazia a E28 inteira (faltava «a igualdade completa so' para o
leitor que se le»). A frase da E28 entra na propria D60; a regra nao muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
d = Arq("delta_v409.py")
d.troca('''entra a maquina com o leitor no problema completo (SAT: uma leitura decide), com Cook-Levin citado [KNOWN]; "
            "nenhum teste com a natureza''', '''entra a maquina com o leitor no problema completo (SAT: uma leitura decide), com Cook-Levin citado [KNOWN]; com o leitor que so' conta vale NP numa so' leitura "
            "e a igualdade completa so' para o leitor que se le (E28); nenhum teste com a natureza''')
d.grava()
