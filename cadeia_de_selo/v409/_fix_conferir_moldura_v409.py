# -*- coding: utf-8 -*-
"""_fix_conferir_moldura_v409.py -- (claude-construtor-v409, 05/11/2026) duas CAUSAS no conferidor (achadas contra o TXT do ensaio, antes do caminho positivo):
(1) o fim da secao v409 e' o titulo da secao da v408, que traz $\beta$ (LaTeX) e o TXT rende β: o find sem _tt nunca achava o fim e a secao saia vazia; usa-se _tt, como no inicio;
(2) a frase certa conferida era a da v408 («Validade no kernel...» com maiuscula; «Kernel validity is not creditation», que na v409 so' esta' num comentario do snippet EN): passa a ser a moldura da v409,
em pedacos que o TXT rende inteiros (PT: relativo ao leitor; a maquina sem leitor e' a fita sem escala; validade no kernel nao e' creditacao; o gate nao se move. EN: relative to the reader; (kernel validity, not creditation);
the machine without a reader is the tape without scale; the gate does not move). Mais estrita que a da v408 (quatro pedacos por lingua em vez de dois)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("conferir_rito_v409.py")
a.troca('_fim409 = {l: txt[l].find(ESP["titulo_secao_v408"][l], max(_ini409[l], 0)) for l in ("pt", "en")}', '_fim409 = {l: txt[l].find(_tt(ESP["titulo_secao_v408"][l]), max(_ini409[l], 0)) for l in ("pt", "en")}   # (v409: o titulo da v408 traz $\beta$; o TXT rende β)')
a.troca('_frase_no_artigo = bool("Validade no kernel não é creditação" in _sec409["pt"] and "o gate não se move" in _sec409["pt"] and "Kernel validity is not creditation" in _sec409["en"] and "the gate does not move" in _sec409["en"]',
        '_frase_no_artigo = bool(all(p_ in _sec409["pt"] for p_ in ("relativo ao leitor", "a máquina sem leitor é a fita sem escala", "validade no kernel não é creditação", "o gate não se move")) and all(p_ in _sec409["en"] for p_ in ("relative to the reader", "(kernel validity, not creditation)", "the machine without a reader is the tape without scale", "the gate does not move"))')
a.grava()
