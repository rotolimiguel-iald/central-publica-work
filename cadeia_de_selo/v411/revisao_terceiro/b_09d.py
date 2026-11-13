from b_lib import *
import re, difflib
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
def toks(s): return re.findall(r"\S+", s)
def show(old, new, lbl):
    a, b = toks(old), toks(new)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    print("#####", lbl, "old len", len(a), "new len", len(b))
    for o, a1, a2, b1, b2 in sm.get_opcodes():
        if o == "equal": continue
        A = " ".join(a[a1:a2]); B = " ".join(b[b1:b2])
        print("  [%s] OLD(%d): %s\n       NEW(%d): %s" % (o, a2-a1, A[:700], b2-b1, B[:900]))
for lang in ("pt", "en"):
    blks = d[lang]
    # block 0: abstract: compare old[0] tail with new[0] after the new text
    old0 = blks[0]["old"][0]; new0 = blks[0]["new"][0]
    show(old0, new0, lang + " abstract")
    for k, blk in enumerate(blks[1:], 1):
        if blk["op"] == "replace" and len(blk["old"]) == len(blk["new"]):
            for o, n in zip(blk["old"], blk["new"]):
                show(o, n, "%s blk%d %s" % (lang, k, o[:40]))
