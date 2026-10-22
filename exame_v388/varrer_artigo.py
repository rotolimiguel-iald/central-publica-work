# -*- coding: utf-8 -*-
"""varrer_artigo.py <lingua> <regex> [largura] -- imprime cada ocorrencia (linha do txt + janela) no um_absoluto_<l>.txt do Nos (so leitura)."""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
l, rx = sys.argv[1], sys.argv[2]; w = int(sys.argv[3]) if len(sys.argv) > 3 else 120
L = open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read().split("\n")
P = re.compile(rx); n = 0
for i, s in enumerate(L, 1):
    for m in P.finditer(s):
        n += 1
        print("%5d | %s" % (i, s[max(0, m.start() - w): m.end() + w].replace("\n", " ")))
print("TOTAL", n)
