import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
for rx in (r"os 44 nomes das declaracoes RATIFICADOS", r"44 nomes", r"os 44 nomes"):
    n, on = achar_em_folhas(REG, rx, 0, 260); print(rx, "reg:", n)
    for p, c in on[:3]: print("    ", p, "::", c[:520])
    for nm in ("pt", "en", "md", "custodia_ws"):
        k, c = achar(C[nm] if nm != "md" else ws(C["md"]), rx, 0, 200)
        if k: print("    ", nm, k, c[:420])
