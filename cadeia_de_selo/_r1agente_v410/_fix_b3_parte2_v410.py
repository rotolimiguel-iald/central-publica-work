# -*- coding: utf-8 -*-
"""_fix_b3_parte2_v410.py -- B3 (o arquivo e' CRLF; o backup de bytes .bak_*_pre_b123 ja' foi gravado pelo _fix_b1_b2_b3): alias a_escala em registros_funcao_v410 do gerar_esperados_v410.py."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(HERE, "gerar_esperados_v410.py")
b0 = open(p, "rb").read(); CR = bytes([13, 10])
assert [f for f in os.listdir(HERE) if f.startswith("gerar_esperados_v410.py.bak_") and f.endswith("_pre_b123")], "backup ausente"
a = b'_rf10a = esp["registros_funcao_v410"]["aescala"]' + CR
b = a + 'esp["registros_funcao_v410"]["a_escala"] = esp["registros_funcao_v410"]["aescala"]   # (parte 2: a leitura do pos-rito le a chave curta a_escala; o conferir_rito le aescala; o MESMO registro nas duas chaves)'.encode("utf-8") + CR
assert b0.count(a) == 1, b0.count(a)
nb = b0.replace(a, b); ast.parse(nb)
open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
print("gerar_esperados_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| CRLF", nb.count(CR), "LF", nb.count(bytes([10])))
