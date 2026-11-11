import sys, collections
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import central
CS = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo")
def contar(v):
    src = CS / v; cnt = collections.Counter(); byt = collections.Counter()
    for p in src.rglob("*"):
        if not p.is_file(): continue
        rel = p.relative_to(src)
        top = rel.parts[0] if len(rel.parts) > 1 else None
        if top and central.FORA_RE.match(top): continue
        if any(x in ("raiz", "temp", "__pycache__", ".lake") for x in rel.parts[:-1]): continue
        if ".bak_" in rel.name: continue
        if p.stat().st_size > central.LIM: continue
        k = top or "(primeiro nivel)"
        cnt[k] += 1; byt[k] += p.stat().st_size
    return cnt, byt
a, ab = contar("v409"); b, bb = contar("v410")
print("v409 total", sum(a.values()), "| v410 total", sum(b.values()))
for k in sorted(set(a) | set(b), key=lambda k: -(b[k] - a[k])):
    print("%-48s v409 %5d  v410 %5d  (%+d)  %8.1f MB" % (k[:48], a[k], b[k], b[k] - a[k], bb[k] / 1e6))
print("FORA_RE:", central.FORA_RE.pattern)
