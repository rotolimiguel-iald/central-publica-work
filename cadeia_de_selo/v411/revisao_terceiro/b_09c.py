from b_lib import *
import re, difflib
def paras(tx):
    tx = tx.replace("\r\n", "\n")
    return [p.strip("\n") for p in re.split(r"\n\s*\n", tx) if p.strip()]
def nz(s):  # format-only normalization (A2 grouping, underscores, spaces)
    return re.sub(r"[\s()^_]", "", s)
out = {}
for lang, fn in (("pt", "um_absoluto_pt.txt"), ("en", "um_absoluto_en.txt")):
    po = paras(rd(NOS + "\\" + fn)); pn = paras(rd(F + "\\" + fn))
    no = [nz(p) for p in po]; nn = [nz(p) for p in pn]
    sm = difflib.SequenceMatcher(a=no, b=nn, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    print("=====", lang, "non-equal blocks:", len(ops))
    out[lang] = []
    for o, a1, a2, b1, b2 in ops:
        print("--", o, "old[%d:%d] new[%d:%d]" % (a1, a2, b1, b2))
        for p in po[a1:a2]: print("   OLD:", p[:130].replace("\n", " "))
        for p in pn[b1:b2]: print("   NEW:", p[:130].replace("\n", " "))
        out[lang].append({"op": o, "old": po[a1:a2], "new": pn[b1:b2]})
json.dump(out, open(SC + r"\b09c_blocos.json", "w", encoding="utf-8"), ensure_ascii=False)
