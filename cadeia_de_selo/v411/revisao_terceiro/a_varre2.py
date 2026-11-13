import re, os
D = r"C:\t\k411c\falso_nos_v411"
NEG = re.compile(r"n[ãa]o|nunca|nem\b|sem\b|\bnot\b|\bnever\b|\bno\b|\bnor\b|\bwithout\b|recus|proib|refus|forbid|creditaç|credita|accredit|creditation|observador|observer|juízo|judg|\bato\b|\bact\b|NOT_|_NOT|de fora|from outside|ninguém|nobody|CONFIRMADA é|CONFIRMED is|\[sic\]|``", re.I)
for f in ("um_absoluto_pt.txt", "um_absoluto_en.txt", "um_absoluto_forma_canonica.md"):
    t = open(os.path.join(D, f), encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r"\bconfirm\w*|\bconfirmad[oa]s?\b|\bconfirma(?:ção|cao|ções|coes)\b", t, re.I):
        w = t[max(0, m.start() - 110):m.end() + 110]
        if not NEG.search(w):
            out.append(t[max(0, m.start() - 100):m.end() + 70].replace("\n", " "))
    print("==", f, "| sem negacao/creditacao por perto:", len(out))
    for c in out[:40]: print("    ", c[:200])
