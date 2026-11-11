# -*- coding: utf-8 -*-
"""_fix_leitura_d76_v410.py -- a leitura o_selo_diz_beta_tgl_provado citava «H0DN» sem a frase obrigatoria da D72 (achado do controle negativo). Backup; troca exata; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_fix2"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
v = "[INPUT; a 15a fala, inteira, 09/11; D76]: a cabeca do ramo (4) da funcao de veredito congelada do H0DN diz beta_TGL provado na natureza"
n = "[INPUT; a 15a fala, inteira, 09/11; D76]: a cabeca do ramo (4) da funcao de veredito congelada do H0DN (pré-registrado; nenhum dado observado lido) diz beta_TGL provado na natureza"
assert t.count(v) == 1; t = t.replace(v, n)
nb = t.encode("utf-8"); ast.parse(nb); tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("delta_v410.py (fix2):", len(b0), "->", len(nb), hashlib.sha256(nb).hexdigest()[:16])
