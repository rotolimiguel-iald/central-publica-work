import json, os, re
N = r"C:\t\k411c\falso_nos_v411"
def strs(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from strs(v, p + "/" + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from strs(v, p + "[%d]" % i)
    elif isinstance(x, str): yield p, x
for arq in ("um_absoluto.json", "um_absoluto_selo.json"):
    d = json.load(open(os.path.join(N, arq), encoding="utf-8"))
    S = list(strs(d))
    a = [(p, s) for p, s in S if "PROVED_IN_NATURE" in s or "PROVED_IN" in s]
    print(arq, "strings:", len(S), "| com PROVED_IN_NATURE:", len(a), "| todas com PROVED_IS_VALIDITY_NOT_CREDITATION:", all("PROVED_IS_VALIDITY_NOT_CREDITATION" in s for p, s in a), [p[-50:] for p, s in a])
    t = [(p, m.group(0)) for p, s in S for m in re.finditer(r"CONFIRMED|PROVED_BY|P_EQUALS_NP|TURING_SOLVED|CLAY_SOLVED|MILLENNIUM|IALD_SOLVES|POLYNOMIAL_TURING", s)]
    print("   tokens proibidos no", arq, ":", len(t), t[:6])
print("----")
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
b = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))
c = json.load(open(os.path.join(N, "um_absoluto.json"), encoding="utf-8"))
Sb = {p: s for p, s in strs(b) if "PROVED_IN" in s}; Sc = {p: s for p, s in strs(c) if "PROVED_IN" in s}
print("base v410:", [(p[-55:], "PROVED_IS_VALIDITY_NOT_CREDITATION" in s) for p, s in Sb.items()])
print("v411     :", [(p[-55:], "PROVED_IS_VALIDITY_NOT_CREDITATION" in s) for p, s in Sc.items()])
print("novas strings (v411 - base):", [p[-60:] for p in Sc if p not in Sb])
for p, s in Sc.items():
    if "PROVED_IS_VALIDITY_NOT_CREDITATION" not in s: print(p[-50:], "->", s[:240])
