# -*- coding: utf-8 -*-
"""_alinha_bloco_ensaio_v409.py -- (claude-construtor-v409) no ensaio montado, o elo novo (c18 a c20 refeitos aqui) caiu DEPOIS do comentario «# NENHUMA chave antiga muda...» do bloco v409 (no bloco-fonte, antes):
reordena para que o montado traga o bloco-fonte tal qual (o comentario fica junto do codigo que ele descreve). Confere no fim que o bloco-fonte inteiro esta' contido no montado."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
b = Arq("_ensaio_bloco_v409.pysnip").t
a = Arq("ensaio_a_seco_v409.py")
i0 = a.t.index("# c18 a c20 REFEITOS AQUI por outro caminho")
i1 = a.t.index('_cc10 = _rapido9(); _cc10.pop("traducao_turing_v409", None);', i0)
novo = a.t[i0:i1]
j1 = a.t.rindex("\n", 0, i0 - 1) + 1   # inicio da linha anterior (o comentario)
com = a.t[j1:i0]
assert com.startswith("# NENHUMA chave antiga muda: o core ANTES e DEPOIS do registro sao iguais em tudo menos a propria chave; o gate nao se move; a chave do lema (v407)"), com[:120]
a.troca(com + novo, novo + com)
a.grava()
assert b.strip() in Arq("ensaio_a_seco_v409.py").t, "o bloco-fonte nao esta' contido no montado"
print("o bloco-fonte esta' contido no montado")
