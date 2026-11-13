from b_lib import *
import re
PRO = {
 "confirm": r"confirm\w*|confirmaç\w*|confirmad\w*",
 "certificad": r"certificad\w*|certified|certificate",
 "montagem": r"montagem|assembly",
 "cego": r"\bceg[oa]s?\b|\bblind\w*",
 "evid_indep": r"evid[êe]ncia\s+independente|independent\s+evidence",
 "descoberta": r"descobert\w*|descobr\w*|discover\w*",
 "posdicao": r"p[óo]s-?\s?di[çc]\w*|post-?diction|n[ãa]o\s+provou|did\s+not\s+prove|has\s+not\s+proven|not\s+proven",
 "beta_lit": r"0[.,]0120\d*|1[.,]2031\d*|12\.031",
 "clay": r"\bClay\b",
 "provou": r"\bprovou\b|\bproved\b|\bprovad[oa]s?\b|\bproven\b",
 "resolvid": r"resolvid[oa]|resolved|solved",
 "descobr_n": r"supremo|supreme",
}
RX = {k: re.compile(v, re.I) for k, v in PRO.items()}
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
def new_text(lang):
    blks = d[lang]; out = []
    for blk in blks:
        for p in blk["new"]:
            # skip registry list lines, hash/version-only replaced paragraphs: keep all new paragraphs but flag
            out.append(p)
    return out
res = {}
for lang in ("pt", "en"):
    paras_ = new_text(lang)
    print("=====", lang, "novos/alterados:", len(paras_))
    for pk, rx in RX.items():
        for p in paras_:
            for m in rx.finditer(p):
                if pk in ("provou", "resolvid", "clay", "descobr_n") : pass
                s = p[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")
                print("  %-10s | %s" % (pk, s))
