# -*- coding: utf-8 -*-
"""_fix_ordem_assert_h0dn_v410.py -- o assert dos tokens no veredito do H0DN ficou ANTES da definicao de TOKENS_PROIBIDOS_V410 no delta: move-o para depois de TOKENS_PROIBIDOS_H0DN. Backup; trocas exatas; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_fix3"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
A = "assert not any(t_ in VEREDITO_H0DN_OK + VEREDITO_H0DN_RECUSA for t_ in TOKENS_PROIBIDOS_V410 + TOKENS_PROIBIDOS_H0DN)\n"
assert t.count(A) == 1; t = t.replace(A, "")
B = 'TOKENS_PROIBIDOS_H0DN = ("FIVE_SIGMA_" + "OBSERVED", "DETEC" + "TED", "H0DN_" + "CONFIRMS")   # D72: tokens proibidos no veredito e no texto do registro H0DN (montados por concatenacao: a guarda varre este texto)\n'
assert t.count(B) == 1; t = t.replace(B, B + A)
nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("delta_v410.py (fix3):", len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16])
