from b_lib import *
pairs = {"md": (NOS + r"\um_absoluto_forma_canonica.md", F + r"\um_absoluto_forma_canonica.md"),
         "man": (NOS + r"\um_absoluto_manifest.md", F + r"\um_absoluto_manifest.md"),
         "out": (NOS + r"\rodada_v410_stdout.txt", F + r"\rodada_v411_stdout.txt")}
for nm, (po, pn) in pairs.items():
    o = [l.rstrip("\r") for l in rd(po).split("\n")]; n = [l.rstrip("\r") for l in rd(pn).split("\n")]
    so, sn = set(o), set(n)
    oo = [l for l in o if l not in sn and l.strip()]; nn = [l for l in n if l not in so and l.strip()]
    print("=====", nm, "linhas old-only:", len(oo), " new-only:", len(nn), " (tam old %d new %d)" % (len(o), len(n)))
    for l in oo[:14]: print("  OLD:", l[:190])
    if nm != "md":
        for l in nn[:10]: print("  NEW:", l[:190])
