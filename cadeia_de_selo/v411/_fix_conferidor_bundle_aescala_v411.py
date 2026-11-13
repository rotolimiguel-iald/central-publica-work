# -*- coding: utf-8 -*-
"""_fix_conferidor_bundle_aescala_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
conferir_rito_v411.py --controle-negativo: KeyError 'TGLExt/AEscala.lean' em _aescala_ok. A causa: a checagem HERDADA da v410 compara a pedra
embutida da AEscala com ESP["bundle_sha256"][MODULO_AESCALA]; na v410 o modulo era NOVO (estava no bundle da versao); na v411 nao ha' modulo
novo (bundle_sha256 == {}, conferido em bundle_ok) e a AEscala e' HERANCA: o pino dela e' ESP["bundle_v410_sha256"] (o mesmo que bundle_v410_ok
confere no kernel do Nos e no hash formal). O conserto: a referencia passa ao bundle da v410. Backup de BYTES antes; ancora unica; ast.parse.
uso: python -B -X utf8 _fix_conferidor_bundle_aescala_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = '(vv_.get("pedra_sha256_embutida") == vv_.get("pedra_sha256_formal") == ESP["bundle_sha256"][DL.D10.MODULO_AESCALA])'
n = '(vv_.get("pedra_sha256_embutida") == vv_.get("pedra_sha256_formal") == ESP["bundle_v410_sha256"][DL.D10.MODULO_AESCALA])'
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_bundle_aescala"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
