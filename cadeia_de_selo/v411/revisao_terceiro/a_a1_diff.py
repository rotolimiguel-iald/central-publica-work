"""A1: o diff por texto (diff -u GNU, meu) por hunk; confronto com os patches declarados e com o DIFF do construtor."""
import re, json, os, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OUT = r"C:\t\k411c\revisao_A"
mine = open(os.path.join(OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split("\n")
theirs = open(os.path.join(V, "DIFF_v410_v411.diff"), "rb").read().decode("utf-8", "surrogateescape").split("\n")
def body(lines):
    return [l for l in lines if not l.startswith("---") and not l.startswith("+++")]
# corpo igual (a menos dos cabecalhos)?
bm, bt = body(mine), body(theirs)
print("corpo do diff igual ao do construtor (fora cabecalhos):", bm == bt, len(bm), len(bt))
# hunks
hunks = []
cur = None
for l in mine:
    if l.startswith("@@"):
        cur = {"h": l, "rem": [], "add": []}
        hunks.append(cur)
    elif cur is not None:
        if l.startswith("-") and not l.startswith("---"):
            cur["rem"].append(l[1:])
        elif l.startswith("+") and not l.startswith("+++"):
            cur["add"].append(l[1:])
print("n hunks", len(hunks))
tot_rem = sum(len(x.encode("utf-8", "surrogateescape")) + 1 for h in hunks for x in h["rem"])
tot_add = sum(len(x.encode("utf-8", "surrogateescape")) + 1 for h in hunks for x in h["add"])
print("bytes rem", tot_rem, "add", tot_add, "liquido", tot_add - tot_rem, "(esperado 880088)")
c = json.load(open(os.path.join(V, "CANDIDATO_v411.json"), encoding="utf-8"))
pr = sum(p["bytes_removidos"] for p in c["patches"]); pa = sum(p["bytes_inseridos"] for p in c["patches"])
print("patches declarados rem", pr, "ins", pa, "liquido", pa - pr)
rows = []
for i, h in enumerate(hunks):
    r = len(h["rem"]); a = len(h["add"])
    rb = sum(len(x.encode("utf-8", "surrogateescape")) + 1 for x in h["rem"])
    ab = sum(len(x.encode("utf-8", "surrogateescape")) + 1 for x in h["add"])
    first = (h["add"][0] if h["add"] else (h["rem"][0] if h["rem"] else ""))[:90]
    rows.append((i, h["h"], r, a, rb, ab, first))
    print(i, h["h"], "rem", r, "(%dB)" % rb, "add", a, "(%dB)" % ab, "|", first.replace("\r", ""))
json.dump(rows, open(os.path.join(OUT, "a1_hunks.json"), "w", encoding="utf-8"), ensure_ascii=False)
