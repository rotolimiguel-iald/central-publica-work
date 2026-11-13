# -*- coding: utf-8 -*-
"""_fix_esperados_onze_falas_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
gerar_esperados_v411.py sobre o candidato real 21e87eb3df5098f8: o assert pinava as falas da v411 no LITERAL 9, e a lista cresceu por ordem da
gerencia (12/11, D172 e D173: 11 falas, D159 a D173; DL.FALAS_V411). A causa: o numero digitado. O conserto: o numero vem da lista do delta e
tem de ser o do manifesto do candidato (verbatins_embutidos) -- nada digitado, e mais estrito que o literal. Docstring e comentario dizem 11 e
D159 a D173 (lidos do delta no assert). Backup de BYTES antes; ancoras unicas; ast.parse. uso: python -B -X utf8 _fix_esperados_onze_falas_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_esperados_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
PARES = [
    ('assert len(_vd) == DL.N_FALAS_V411 == 9 and all(',
     'assert len(_vd) == DL.N_FALAS_V411 == len(DL.FALAS_V411) == CM["verbatins_embutidos"] and all('),
    ('# ---- as falas (9, por sha256), as decisoes (D159 a D170) e as erratas (E41, E42, E43): o candidato == o delta == os registros\n',
     '# ---- as falas (as de DL.FALAS_V411, 11 desde a ordem da gerencia de 12/11, por sha256; o numero == o do manifesto), as decisoes (DL.DECISOES_V411, D159 a D173) e as erratas (E41, E42, E43): o candidato == o delta == os registros\n'),
    ('(as 9 falas de 11 e 12/11 por sha256; D159 a D170;', '(as 11 falas de 11 e 12/11 por sha256, lidas de DL.FALAS_V411; D159 a D173, DL.DECISOES_V411;'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_onze_falas"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
