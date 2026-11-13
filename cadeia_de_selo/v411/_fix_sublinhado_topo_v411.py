# -*- coding: utf-8 -*-
"""_fix_sublinhado_topo_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do ensaio a seco do candidato real (652eaa4f201682bc): o pdflatex PARA em «Missing $ inserted»
no topo ratificado (l.31: «... veredito NOT_FALSIFIED_POWERED; ...»): o texto ratificado traz um veredito de maquina com sublinhado FORA do modo matematico. A causa: o _v411_tex_misto convertia as letras gregas e os simbolos
mas nao escapava o sublinhado do modo texto. O conserto (contido no conversor): fora do modo matematico, "_" vira "\\_" (dentro, como $β_{TGL}$ e $z_*$, fica). Backup de BYTES antes; ancora unica; ast.parse.
uso: python -B -X utf8 _fix_sublinhado_topo_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "quadro_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = '"×": r"$\\times$", "−": r"$-$", "%": r"\\%"}   # (v411: o Λ do ΛCDM, achado do ensaio a seco)\n'
n = '"×": r"$\\times$", "−": r"$-$", "%": r"\\%", "_": r"\\_"}   # (v411: o Λ do ΛCDM e o sublinhado de veredito de maquina no modo texto, achados do ensaio a seco)\n'
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc_real2"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
