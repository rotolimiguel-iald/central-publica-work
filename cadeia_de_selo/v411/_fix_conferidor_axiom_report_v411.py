# -*- coding: utf-8 -*-
"""_fix_conferidor_axiom_report_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado da varredura
das chaves de ESPERADOS que o conferir_rito_v411.py le (feita por script depois do KeyError da AEscala, para nao descobrir uma por rodada): o item
«o axiom_report da v410 segue no trio e so' cresceu» le ESP["axiom_report_v409_n"], que o gerar_esperados_v411.py NAO grava (grava
axiom_report_v410_n: o tamanho do axiom_report do core da v410 selada). A causa: o nome da v410 (que comparava com a v409) ficou na porta. O
conserto: le axiom_report_v410_n, o que o rotulo do item diz. Backup de BYTES antes; ancora unica; ast.parse.
uso: python -B -X utf8 _fix_conferidor_axiom_report_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = '"o axiom_report da v410 segue no trio e so\' cresceu": len(axr) >= ESP["axiom_report_v409_n"]'
n = '"o axiom_report da v410 segue no trio e so\' cresceu": len(axr) >= ESP["axiom_report_v410_n"]'
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_axiom_report"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
