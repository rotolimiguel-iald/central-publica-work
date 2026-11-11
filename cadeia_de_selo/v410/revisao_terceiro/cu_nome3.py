import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
RX = re.compile(r"leitura do operador|leitura dele|operator[’']s reading|reading of the operator|his reading|\[ONTO[^\]]*\]|\[INPUT/ONTO\]", re.I)
for k in ("md", "en"):
    t = ws(rd("novo_%s.txt" % k))
    ms = list(RX.finditer(t)); print("==", k, len(ms))
    for m in ms: print("   >", ctx(t, m, 150))
