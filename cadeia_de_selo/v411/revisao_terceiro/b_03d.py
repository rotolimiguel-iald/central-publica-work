from b_lib import *
import re
exec(open("b_03c.py", encoding="utf-8").read().split("d = json.load")[0])
pairs = {"md": (NOS + r"\um_absoluto_forma_canonica.md", F + r"\um_absoluto_forma_canonica.md"),
         "man": (NOS + r"\um_absoluto_manifest.md", F + r"\um_absoluto_manifest.md"),
         "out": (NOS + r"\rodada_v410_stdout.txt", F + r"\rodada_v411_stdout.txt")}
for nm, (po, pn) in pairs.items():
    old = set(l.rstrip("\r") for l in rd(po).split("\n")); newl = [l.rstrip("\r") for l in rd(pn).split("\n")]
    only = [l for l in newl if l not in old and l.strip()]
    print("=====", nm, "linhas novas/alteradas:", len(only), "de", len(newl))
    for l in only[:3]: print("   ex:", l[:110])
    for pk, rx in RX.items():
        for l in only:
            for m in rx.finditer(l):
                if pk in ("cego", "evid_indep") and re.search(r"n[ãa]o|not|never|nunca", l[max(0, m.start()-40):m.start()], re.I): continue
                print("  %-10s | %s" % (pk, l[max(0, m.start()-70): m.end()+70]))
