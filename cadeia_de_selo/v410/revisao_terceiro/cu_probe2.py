import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
novo = {k: ws(rd("novo_%s.txt" % k)) for k in ("pt", "en")}
v409 = {k: ws(rd(R + "../v409/dry_v409/dry_v409_%s.txt" % k)) for k in ("pt", "en")} if os.path.exists(R + "../v409/dry_v409/dry_v409_pt.txt") else {}
for k in ("pt", "en"):
    t = C[k]
    ms = list(re.finditer(r"e\^-[a-z]", t))
    print("==", k, "todas:", len(ms), "| no texto novo/alterado vs v409:", len(re.findall(r"e\^-[a-z]", novo[k])), "| na v409:", len(re.findall(r"e\^-[a-z]", v409.get(k, ""))) if v409 else "n/d")
    for m in ms:
        print("   ", ctx(t, m, 60).replace("\n", " "))
    # decimais com ponto no PT
print()
for k in ("pt",):
    t = C[k]
    ms = list(re.finditer(r"\b\d+\.\d+\b", t))
    print("decimais com ponto no PT (todo):", len(ms), "| nos novos:", len(re.findall(r"\b\d+\.\d+\b", novo["pt"])))
    for m in ms[:12]: print("   ", ctx(t, m, 50))
