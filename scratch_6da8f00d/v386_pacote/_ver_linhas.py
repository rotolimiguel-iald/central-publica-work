# -*- coding: utf-8 -*-
"""_ver_linhas.py -- SO LEITURA: imprime faixas de linhas do um.py v385 do Nos (CRLF), truncadas. uso: python _ver_linhas.py A-B [A-B ...] [--max N]"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
T = open(os.path.join(NOS, "um.py"), "rb").read().decode("utf-8")
lines = T.split("\r\n")
MAX = 400
args = []
for a in sys.argv[1:]:
    if a.startswith("--max="):
        MAX = int(a.split("=", 1)[1])
    else:
        args.append(a)
for a in args:
    lo, hi = [int(x) for x in a.split("-")]
    print("\n===== L%d-L%d =====" % (lo, hi))
    for n in range(lo, hi + 1):
        l = lines[n - 1]
        print("L%d: %s" % (n, l[:MAX] + (" ...[%d]" % len(l) if len(l) > MAX else "")))
