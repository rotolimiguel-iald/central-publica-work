# -*- coding: utf-8 -*-
"""_r1_a6_orquestrador_v410.py -- R1, A6 (BAIXO 12 da revisao de terceiro; fora do candidato): a docstring e o log do S4 do orquestrador diziam um modulo novo a frio; sao DOIS (IALD2 e AEscala). So' texto. Backup de BYTES; temporario -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "orquestrador", "pos_treino_v410.py")
b0 = open(P, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
for a, b in (("Só 1 módulo novo compila a frio (", "São 2 módulos novos a compilar a frio, IALD2 e AEscala ("), ("1 módulo novo a frio: no sandbox k410c", "2 módulos novos a frio, IALD2 e AEscala: no sandbox k410c")):
    c = t.count(a); assert c == 1, (c, a); t = t.replace(a, b)
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_r1_a6", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("orquestrador/pos_treino_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])
