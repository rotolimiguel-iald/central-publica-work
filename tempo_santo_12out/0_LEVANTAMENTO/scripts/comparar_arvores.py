"""Compara duas arvores (contagem de arquivos e bytes) — somente leitura. Uso: python -I comparar_arvores.py <origem> <copia>"""
import json
import os
import sys

LONG = "\\\\?\\"


def tot(root):
    n = 0
    b = 0
    for dp, dn, fn in os.walk(LONG + os.path.abspath(root)):
        for f in fn:
            b += os.path.getsize(os.path.join(dp, f))
            n += 1
    return n, b


a = tot(sys.argv[1])
c = tot(sys.argv[2])
print(json.dumps(dict(origem=sys.argv[1], copia=sys.argv[2], origem_arquivos=a[0], origem_bytes=a[1],
                      copia_arquivos=c[0], copia_bytes=c[1], iguais=(a == c))))
