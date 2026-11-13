from b_lib import *
import re
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
rx = re.compile(r"\bsela\b|\bselar\b|\bselou\b|\bselad[oa]s?\b|\bselo\b|\bseal(?:s|ed|ing)?\b", re.I)
for lang in ("pt", "en"):
    for blk in d[lang]:
        for p in blk["new"]:
            for m in rx.finditer(p):
                s = p[max(0, m.start()-90): m.end()+70].replace("\n", " ")
                print(lang, "|", s)
# md new lines
m1 = md(); old = set(l.rstrip("\r") for l in rd(NOS + r"\um_absoluto_forma_canonica.md").split("\n"))
for l in m1.split("\n"):
    l = l.rstrip("\r")
    if l not in old and l.strip():
        for m in rx.finditer(l): print("md |", l[max(0, m.start()-90): m.end()+70])
