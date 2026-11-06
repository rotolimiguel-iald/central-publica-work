# -*- coding: utf-8 -*-
"""_adapt_rito_tempo_v409.py -- (claude-construtor-v409, 05/11/2026 ~19h40) o kernel foi reconstruido (build incremental + Audit) depois da revisao dos insumos pela gerencia: o cabecalho do rito_v409.sh traz o
TEMPO MEDIDO, e o conferidor do instalar/rito exige no rito os numeros de kernel/construir_marcas.txt. Os tempos sao LIDOS de kernel/POS_BUILD_v409.json (nunca digitados) e trocados por expressao regular no texto
do cabecalho (contagem exata: 1 e 1); o Audit desta rodada rodou inteiro logo depois do build, e a nota da queda de energia sai."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq, HERE
PB = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v409.json"), encoding="utf-8"))
B, A, SOMA, MAX = PB["duracao_build_s"], PB["duracao_audit_s"], PB["build_modulos_s_soma"], PB["build_modulos_s_max"]
r = Arq("rito_v409.sh")
r.troca_re(r"= \d+ s e 1 Audit = \d+ s \(a soma dos tempos por modulo e' [\d.]+ s, o maximo de um modulo [\d.]+ s; o Audit foi refeito sozinho depois da queda de energia de ~17:10\);",
           "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %.1f s, o maximo de um modulo %.1f s; medidos de novo depois da revisao dos insumos de ~19h30);" % (B, A, SOMA, MAX))
r.troca_re(r"\(a ordem de grandeza e' a medida do sandbox, \d+ s \+ \d+ s\) e as outras duas passagens so' reconferem \(build ja' pronto \+ Audit de \d+ s\)",
           "(a ordem de grandeza e' a medida do sandbox, %d s + %d s) e as outras duas passagens so' reconferem (build ja' pronto + Audit de %d s)" % (B, A, A))
r.grava()
