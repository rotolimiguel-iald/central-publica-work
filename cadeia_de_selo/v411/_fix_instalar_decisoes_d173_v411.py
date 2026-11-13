# -*- coding: utf-8 -*-
"""_fix_instalar_decisoes_d173_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
conferir_instalar_rito_v411.py sobre o candidato real 21e87eb3df5098f8: o pino da lista de decisoes dizia D159 a D170; a lista cresceu por ordem
da gerencia (12/11, D172 e D173: D159 a D173, DL.DECISOES_V411 com 9 ids). A causa: o fim da faixa digitado antes da ordem. O conserto: o pino
passa a D173 (a faixa da ordem; o primeiro, o ultimo e as erratas seguem pinados). As marcas exigidas nos arquivos ja' saem do delta (_DEC[0], _DEC[-1]). Backup de BYTES antes; ancora unica; ast.parse.
uso: python -B -X utf8 _fix_instalar_decisoes_d173_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_instalar_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = 'assert _DEC[0] == "D159" and _DEC[-1] == "D170" and _ERR == ["E41", "E42", "E43"], (_DEC, _ERR)\n'
n = ('assert _DEC[0] == "D159" and _DEC[-1] == "D173" and _ERR == ["E41", "E42", "E43"], (_DEC, _ERR)   # (ordem da gerencia c1 de 12/11, D172 e D173: a faixa vai de D159 a D173; antes, D170)\n')
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_d173"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
