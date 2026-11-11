import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
RX = re.compile(r"leitura do operador|leitura dele|operator[’']s reading|reading of the operator|his reading|\[ONTO\]|\[INPUT/ONTO\]|\[ONTO[^\]]*\]|\[INPUT/dicionário", re.I)
novo = {k: rd("novo_%s.txt" % k) for k in ("pt", "en", "md")}
def sentencas(t):
    return [s for s in re.split(r"(?<=[.;])\s+(?=[A-ZÀ-Ú\[«“\*#-])", ws(t)) if s]
tot = {}
for k, t in novo.items():
    hits = [(m, t) for m in RX.finditer(ws(t))]
    tot[k] = len(hits)
print("hits nos trechos novos/alterados do artigo/md:", tot)
t = ws(novo["pt"])
sec = {}
for m in RX.finditer(t):
    c = ctx(t, m, 200)
    key = m.group(0).lower()
    sec.setdefault(key, []).append(c)
for k, v in sec.items():
    print("== PT novo:", repr(k), len(v))
    for c in v[:3]: print("     ", c.replace("\n", " "))
# registros (v410)
REG = todos_registros(C)
cont = {}
for p, tx in REG:
    for m in RX.finditer(tx):
        cont.setdefault(p.split(".")[0] + ":" + m.group(0).lower(), []).append((p, ctx(tx, m, 150)))
print()
for k, v in sorted(cont.items()): print("REG", k, len(v))
