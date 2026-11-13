from b_lib import *
import re
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
RX = {
 "D59": re.compile(r"mil[eê]nio|millennium|navier|lind[ãa]o|\bkimi\b", re.I),
 "nome": re.compile(r"leitura\s+do\s+operador|leitura\s+dele|\[ONTO\]|ontol[óo]gic|operator'?s\s+reading|his\s+reading|reading\s+of\s+the\s+operator|INPUT/dicion[áa]rio|INPUT/ONTO|identifica[çc][ãa]o\s+do\s+operador", re.I),
}
def scan(label, texts):
    for pk, rx in RX.items():
        for p in texts:
            for m in rx.finditer(p):
                print(label, pk, "|", p[max(0, m.start()-80): m.end()+80].replace("\n", " "))
for lang in ("pt", "en"):
    ps = [p for blk in d[lang] for p in blk["new"]]
    scan(lang, ps)
old = set(l.rstrip("\r") for l in rd(NOS + r"\um_absoluto_forma_canonica.md").split("\n"))
scan("md", [l for l in md().split("\n") if l.rstrip("\r") not in old and l.strip()])
for nm, pn, po in (("man", F + r"\um_absoluto_manifest.md", NOS + r"\um_absoluto_manifest.md"), ("out", F + r"\rodada_v411_stdout.txt", NOS + r"\rodada_v410_stdout.txt")):
    o = set(l.rstrip("\r") for l in rd(po).split("\n"))
    scan(nm, [l for l in rd(pn).split("\n") if l.rstrip("\r") not in o and l.strip()])
print("fim")
