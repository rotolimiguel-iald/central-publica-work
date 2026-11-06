# -*- coding: utf-8 -*-
"""_adapt_d62_en_sem_aspas_v409.py -- (claude-construtor-v409) a conferencia das citacoes exige que o snippet EN nao traga « » (o EN so' traz a TRADUCAO da gerencia, marcada como nao-citacao; a fala verbatim fica no PT).
Eu pus «Ratifico os nomes» no EN (a causa): passa a traducao marcada, no padrao do proprio snippet («our translation: ...»)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
e = Arq("artigo_en_v409.pysnip")
e.troca("those added in R9 too, on 05/11, by the saying «Ratifico os nomes») and", "those added in R9 too, on 05/11, D62, by the operator's saying, our translation: I ratify the names) and")
e.grava()
