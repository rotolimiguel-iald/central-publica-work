from b_lib import *
import re
def paras(tx):
    tx = tx.replace("\r\n", "\n")
    return [p for p in re.split(r"\n\s*\n", tx) if p.strip()]
def ungroup(s):
    # remove '(' right after '^' and its matching ')'
    out = []; i = 0; stack = []
    while i < len(s):
        if s[i] == "^" and i + 1 < len(s) and s[i+1] == "(":
            # find matching paren
            depth = 0; j = i + 1
            while j < len(s):
                if s[j] == "(": depth += 1
                elif s[j] == ")":
                    depth -= 1
                    if depth == 0: break
                j += 1
            out.append("^" + ungroup(s[i+2:j])); i = j + 1; continue
        out.append(s[i]); i += 1
    return "".join(out)
for lang, fn in (("pt", "um_absoluto_pt.txt"), ("en", "um_absoluto_en.txt")):
    po = paras(rd(NOS + "\\" + fn)); pn = paras(rd(F + "\\" + fn))
    sn = set(re.sub(r"\s+", " ", p) for p in pn)
    n_raw_diff = 0; n_after_ungroup = 0; bad = []
    pn_ung = set(re.sub(r"\s+", " ", ungroup(p)) for p in pn)
    for p in po:
        k = re.sub(r"\s+", " ", p)
        if k in sn: continue
        n_raw_diff += 1
        if k in pn_ung: n_after_ungroup += 1
        else: bad.append(p[:100])
    print(lang, "old paragraphs not present verbatim in new:", n_raw_diff, "of which equal after removing exponent grouping:", n_after_ungroup, "remaining:", len(bad))
    for b in bad: print("   ", b.replace("\n", " "))
