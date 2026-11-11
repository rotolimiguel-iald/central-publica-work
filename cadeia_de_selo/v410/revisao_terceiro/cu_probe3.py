import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
novo = {k: ws(rd("novo_%s.txt" % k)) for k in ("pt", "en", "md")}
print("decimais com ponto no PT NOVO:")
for m in re.finditer(r"\b\d+\.\d+\b", novo["pt"]): print("   ", ctx(novo["pt"], m, 70))
for k in ("pt", "en"):
    t = C[k]
    for rx in (r"Π\^\(k\+1\)=Π", r"Π\^k\+1", r"P\^\(k\+1\)=P", r"P\^k\+1", r"nln 2", r"n ?[·]? ?ln ?2", r"ln\(\(1-β\)/β\)", r"ln ?\(1-β\)", r"√\(\(?b/\(1-b\)\)?\)", r"√b/\(1-b\)", r"√\(b/\(1-b\)\)"):
        ms = list(re.finditer(rx, t))
        print("[%s] /%s/ -> %d" % (k, rx, len(ms)), ("| " + ctx(t, ms[0], 40)) if ms else "")
t = C["pt"]
ms = list(re.finditer(r"2[\.,]867", t)); print("Phi(-5) PT:", [ctx(t, m, 30) for m in ms])
ms = list(re.finditer(r"2[\.,]867", C["en"])); print("Phi(-5) EN:", [ctx(C["en"], m, 30) for m in ms])
