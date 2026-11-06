# -*- coding: utf-8 -*-
"""_conserta_continuacao_r2_v409.py -- (claude-construtor-v409) as duas linhas do gf.troca da continuacao da R2 ficaram com aspas triplas mal fechadas (o texto comeca e termina com aspa simples): passam a aspas
triplas DUPLAS. So' o adaptador muda."""
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_adapt_revisao_r2_continuacao_v409.py")
t = open(p, encoding="utf-8").read()
L = t.split("\n")
FR = "'a pedra Par (v407) deixou a face de Fock «[OPEN]: o FockCertificate não tem operadores de criação como termo»; a E21 da v408 corrigiu ao lado'"
i = next(i_ for i_, l_ in enumerate(L) if l_.startswith("gf.troca(''''a pedra Par"))
assert L[i + 1].lstrip().startswith("''''a pedra Par"), L[i + 1][:40]
L[i] = 'gf.troca("""' + FR + '""",'
L[i + 1] = '         """' + FR + ', """ + ", ".join(repr(s_) for s_ in CERTAS))'
open(p + ".tmp", "w", encoding="utf-8", newline="\n").write("\n".join(L)); os.replace(p + ".tmp", p)
import ast; ast.parse(open(p, encoding="utf-8").read()); print("ok")
