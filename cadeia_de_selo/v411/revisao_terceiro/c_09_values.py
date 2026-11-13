import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
rf = E["registros_funcao_v411"]
print(list(rf))
h = rf.get("h0dn") or {}
print(list(h))
vals = h["values"]
for k, v in vals.items():
    s = json.dumps(v, ensure_ascii=False)
    print(k, type(v).__name__, s[:160])
print("cunhagens ESP keys:", list(E["cunhagens"])[:3], list(next(iter(E["cunhagens"].values()))))
