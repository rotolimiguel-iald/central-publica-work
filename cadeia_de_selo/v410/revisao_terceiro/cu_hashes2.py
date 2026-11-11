import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
for tkn in ("589ac6a38849381d", "a6c4912afc6f0dc4", "cd80fed6fea1ea5d"):
    print("==", tkn)
    n, on = achar_em_folhas(REG, tkn, 0, 230); print("  reg:", n)
    for p, c in on[:2]: print("     ", p, "::", c)
    n, c = achar(ws(C["md"]), tkn, 0, 230); print("  md:", n, c[:460])
    for nm in ("pt", "en", "custodia_ws"):
        n, c = achar(C[nm], tkn, 0, 200); 
        if n: print("  ", nm, n, c[:400])
