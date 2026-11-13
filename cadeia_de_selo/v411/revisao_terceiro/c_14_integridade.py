import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
M = json.load(open(V + r"\MANIFESTO_INSUMOS_v411.json", encoding="utf-8"))
def walk(o, acc):
    if isinstance(o, dict):
        if "sha256" in o and any(isinstance(o.get(k), str) and (":\\" in o.get(k) or ":/" in o.get(k)) for k in o):
            p = [o[k] for k in o if isinstance(o.get(k), str) and (":\\" in o[k] or ":/" in o[k])][0]
            acc.append((p, o["sha256"]))
        for v in o.values(): walk(v, acc)
    elif isinstance(o, list):
        for v in o: walk(v, acc)
acc = []; walk(M, acc)
ok = 0; ruins = []
seen = set()
for p, s in acc:
    if (p, s) in seen: continue
    seen.add((p, s))
    if "kimi" in p.lower().split("\\"): ruins.append(("KIMI?", p)); continue
    if not os.path.exists(p): ruins.append(("AUSENTE", p)); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == s: ok += 1
    else: ruins.append(("SHA_DIFERE", p))
print("entradas do manifesto com caminho+sha256:", len(seen), "ok:", ok, "problemas:", ruins[:5])
# VERBATIM_CONGELADO
Vb = json.load(open(V + r"\VERBATIM_CONGELADO_v411.json", encoding="utf-8"))
acc2 = []; walk(Vb, acc2); ok2 = 0; r2 = []
for p, s in set(acc2):
    if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == s: ok2 += 1
    else: r2.append(p)
print("VERBATIM_CONGELADO:", len(set(acc2)), "ok", ok2, "problemas", r2[:3])
