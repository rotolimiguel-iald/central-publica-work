import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
for nome, t in (("PT", C["pt"]), ("EN", C["en"]), ("md", ws(C["md"]))):
    ms = list(re.finditer(r"identidade aritmética|arithmetic identity", t))
    print("==", nome, len(ms))
    for m in ms[:2]: print("   ", t[max(0, m.start()-900): m.end()+700]); print()
