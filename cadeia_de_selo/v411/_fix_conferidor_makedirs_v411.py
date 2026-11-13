# -*- coding: utf-8 -*-
"""_fix_conferidor_makedirs_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
conferir_rito_v411.py --controle-negativo (Nos na v410 selada, 5d9497a721c3589e): FileNotFoundError ao gravar a copia de import do um.py em
C:\\t\\k411c\\conferidor_import_<sha16>\\. A causa: na adaptacao (D135) o `os.makedirs(_cp, exist_ok=True)` ficou DENTRO do comentario da linha
(o mesmo padrao do comentario que engole o resto da linha que a frente H achou na leitura): a pasta so' existia quando uma rodada anterior a
tinha criado. O conserto: o makedirs sai do comentario, antes do uso. Backup de BYTES antes; ancora unica; ast.parse.
uso: python -B -X utf8 _fix_conferidor_makedirs_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = '_cp = os.path.join(DL.RODADA_PAI, "conferidor_import_" + umsha)   # (D135: a copia de import do um.py por rodada fica FORA de work\\); os.makedirs(_cp, exist_ok=True)\n'
n = ('_cp = os.path.join(DL.RODADA_PAI, "conferidor_import_" + umsha)   # (D135: a copia de import do um.py por rodada fica FORA de work\\)\n'
     'os.makedirs(_cp, exist_ok=True)   # (fork C, 12/11: estava dentro do comentario acima; a pasta so\' existia se uma rodada anterior a tivesse criado)\n')
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_makedirs"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
