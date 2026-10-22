"""sha256 dos bytes de cada caminho dado (somente leitura). Uso: python -I sha.py <p1> <p2> ..."""
import hashlib
import os
import sys

LONG = "\\\\?\\"  # prefixo de caminho longo do Windows: \\?\

for p in sys.argv[1:]:
    ap = os.path.abspath(p)
    lp = ap if len(ap) < 250 else LONG + ap
    try:
        with open(lp, "rb") as fh:
            b = fh.read()
        print(f"{hashlib.sha256(b).hexdigest()}\t{len(b)}\t{p}")
    except Exception as e:  # falha visivel, nunca ok falso
        print(f"ERRO\t{type(e).__name__}: {e}\t{p}")
