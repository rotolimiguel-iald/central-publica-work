from b_lib import *
import re, difflib, hashlib
def paras(tx):
    tx = tx.replace("\r\n", "\n")
    return [p.strip("\n") for p in re.split(r"\n\s*\n", tx) if p.strip()]
res = {}
for lang, fn in (("pt", "um_absoluto_pt.txt"), ("en", "um_absoluto_en.txt")):
    old = rd(NOS + "\\" + fn); new = rd(F + "\\" + fn)
    po, pn = paras(old), paras(new)
    so, sn = set(po), set(pn)
    only_old = [p for p in po if p not in sn]
    only_new = [p for p in pn if p not in so]
    print("=====", lang, "paras old", len(po), "new", len(pn), "only_old", len(only_old), "only_new", len(only_new))
    res[lang] = {"only_old": only_old, "only_new": only_new}
    # pairing by similarity
    used = set()
    pairs = []
    for i, p in enumerate(only_new):
        best = None; bs = 0
        for j, q in enumerate(only_old):
            if j in used: continue
            r = difflib.SequenceMatcher(None, p[:400], q[:400], autojunk=False).quick_ratio()
            if r > bs: bs, best = r, j
        if best is not None and bs > 0.6:
            used.add(best); pairs.append((i, best, bs))
    print("pairs (changed paragraphs):", len(pairs), " new-only unpaired:", len(only_new) - len(pairs), " old-only unpaired:", len(only_old) - len(used))
    res[lang]["pairs"] = pairs
json.dump(res, open(SC + r"\b09_diff.json", "w", encoding="utf-8"), ensure_ascii=False)
