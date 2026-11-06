# -*- coding: utf-8 -*-
"""_f43_numa_leitura_v409.py -- (claude-construtor-v409, 05/11/2026) a marca 1 da F43 (NP numa leitura) nao aceitava «NP numa leitura» nem «NP holds in one reading» (so' «com uma leitura» e «NP in one reading»);
a regra fica a mesma (a E28 tem de estar no texto), o reconhecimento da marca e' que passa a aceitar as duas formas comuns. Nenhuma proibicao relaxada: o controle negativo da guarda roda de novo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("runtime_v409.py")
a.troca(r'''NP[^.;]{0,40}?(?:com|numa|em)\s+(?:uma|1)\s+(?:s[oó]'?\s+)?leitura|uma\s+leitura\s+decide|NP\s+in\s+one\s+reading''', r'''NP[^.;]{0,40}?(?:com\s+(?:uma|1)|numa|em\s+uma)\s+(?:s[oó]'?\s+)?leitura|uma\s+leitura\s+decide|NP[^.;]{0,40}?in\s+one\s+reading''')
a.grava()
