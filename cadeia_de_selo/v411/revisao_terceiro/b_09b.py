from b_lib import *
import re, difflib, collections
d = json.load(open(SC + r"\b09_diff.json", encoding="utf-8"))
def toks(s): return re.findall(r"\S+", s)
for lang in ("pt",):
    on, oo = d[lang]["only_new"], d[lang]["only_old"]
    cnt = collections.Counter(); where = collections.defaultdict(list)
    for (i, j, r) in d[lang]["pairs"]:
        a, b = toks(oo[j]), toks(on[i])
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        for o, a1, a2, b1, b2 in sm.get_opcodes():
            if o == "equal": continue
            key = (" ".join(a[a1:a2])[:80], " ".join(b[b1:b2])[:120], o)
            cnt[key] += 1; where[key].append(i)
    print(lang, "distinct ops", len(cnt))
    for (a, b, o), n in cnt.most_common(70):
        print(n, o, "|", repr(a), "=>", repr(b))
