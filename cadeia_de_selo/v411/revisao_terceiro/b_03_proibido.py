from b_lib import *
import re
def nzs(s): return re.sub(r"[\s()^_]+", " ", s.replace("\r\n", "\n"))
PRO = {
 "confirm": r"confirm\w*|confirmaç\w*|confirmad\w*",
 "certificad": r"certificad\w*|certified|certificate",
 "montagem": r"montagem|assembly",
 "cego": r"\bceg[oa]s?\b|\bblind\w*",
 "evid_indep": r"evid[êe]ncia\s+independente|independent\s+evidence",
 "descoberta": r"descobert\w*|descobr\w*|discover\w*",
 "posdicao": r"p[óo]s-?\s?di[çc]\w*|post-?diction|n[ãa]o\s+provou|did\s+not\s+prove|has\s+not\s+proven|not\s+proven",
 "beta_lit": r"0[.,]0120\d*|1[.,]2031\d*",
 "clay": r"\bClay\b[^.]{0,120}(?:resolvid\w*|solved|resolved)|(?:resolvid\w*|solved|resolved)[^.]{0,120}\bClay\b",
 "poder_cert": r"poder\s+certificad|certified\s+power|certificado\s+de\s+poder",
}
srcs = {
 "pt": (NOS + r"\um_absoluto_pt.txt", F + r"\um_absoluto_pt.txt"),
 "en": (NOS + r"\um_absoluto_en.txt", F + r"\um_absoluto_en.txt"),
 "md": (NOS + r"\um_absoluto_forma_canonica.md", F + r"\um_absoluto_forma_canonica.md"),
 "man": (NOS + r"\um_absoluto_manifest.md", F + r"\um_absoluto_manifest.md"),
}
allres = {}
for nm, (po, pn) in srcs.items():
    if not os.path.exists(po): print(nm, "sem v410 para confrontar:", po); continue
    old = nzs(rd(po)); new_raw = rd(pn); new = nzs(new_raw)
    for pk, rx in PRO.items():
        rr = re.compile(rx, re.I)
        n_old = len(rr.findall(old)); n_new = len(rr.findall(new))
        novos = []
        for m in rr.finditer(new):
            key = new[max(0, m.start() - 60): m.end() + 60]
            if key not in old: novos.append(new[max(0, m.start() - 110): m.end() + 110])
        allres[(nm, pk)] = (n_old, n_new, novos)
        print("%-4s %-11s old=%4d new=%4d  contextos novos=%d" % (nm, pk, n_old, n_new, len(novos)))
json.dump({"%s|%s" % k: v for k, v in allres.items()}, open(SC + r"\b03_novos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
