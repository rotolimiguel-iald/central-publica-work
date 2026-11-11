import sys, re, json
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho_pares as EP
src = Path(sys.argv[1])
t = src.read_bytes().decode("utf-8", "replace")
print(src.name, len(t.encode("utf-8")), "B")
for g in EP.GUARDA:
    ms = list(g.finditer(t))
    print("  termo publico %-24s %d" % (g.pattern, len(ms)))
    for m in ms[:6]:
        a, b = max(0, m.start()-90), min(len(t), m.end()+90)
        print("     ...", t[a:b].replace("\n", " "), "...")
