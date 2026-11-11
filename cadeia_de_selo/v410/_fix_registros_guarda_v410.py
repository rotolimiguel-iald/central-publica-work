# -*- coding: utf-8 -*-
"""_fix_registros_guarda_v410.py -- (claude-construtor-v410, 06/11/2026) a CAUSA de duas reprovacoes da guarda das frases no texto novo (nenhuma regra relaxada): (1) a F35 da v409 lia «a do Clay) seja decidida» como afirmacao (a negacao vinha
depois); o item do «nao diz» passa a dizer que a pergunta nao tem resposta aqui; (2) a F47b da v410 pegava, no papel da pedra, o trecho «o algoritmo IALD (a forma da luz que satisfaz P = nP» sem o qualificador no mesmo trecho; o qualificador passa para o
mesmo trecho. Trocas com contagem exata."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
aplicar(os.path.join(os.path.dirname(os.path.abspath(__file__)), "registros_v410.py"), [
    ("\"que a pergunta da maquina de Turing padrao sem o leitor (no Mathlib, Turing.TM2ComputableInPolyTime; a do Clay) seja decidida aqui: nao e'; o que o kernel prova e' isto: \"",
     "\"que a pergunta da maquina de Turing padrao sem o leitor (no Mathlib, Turing.TM2ComputableInPolyTime; a pergunta do Clay) tenha resposta aqui: nao tem; o que o kernel prova e' isto: \"", 1),
    ("o algoritmo IALD (a forma da luz que satisfaz P = nP; resolver = verificar; uma leitura decide SAT), relativo ao leitor (a maquina com o leitor), com a maquina de Turing padrao sem o leitor fora; ",
     "o algoritmo IALD -- a forma da luz que satisfaz P = nP relativo ao leitor (a maquina com o leitor), em que resolver = verificar e uma leitura decide SAT --, com a maquina de Turing padrao sem o leitor fora; ", 1),
])
