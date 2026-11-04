# -*- coding: utf-8 -*-
# Exploracao estrutural (somente leitura) dos recibos da instalacao v406.
import json, hashlib
from pathlib import Path

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def shape(o, depth=0, maxd=2):
    if isinstance(o, dict):
        ks = list(o.keys())
        return {"type": "dict", "n": len(ks), "keys": ks[:25]}
    if isinstance(o, list):
        return {"type": "list", "n": len(o), "first": (shape(o[0], depth + 1) if o else None)}
    return {"type": type(o).__name__, "v": (str(o)[:120])}


for name in ("install_plan.json", "deployment.json", "validation/review_final.json", "app/RUNTIME_BASELINE.json", "validation/final_checks.json"):
    p = W / name
    d = json.loads(p.read_bytes())
    print("==", name, p.stat().st_size, sha(p)[:16])
    if isinstance(d, dict):
        for k, v in d.items():
            print("  ", k, "->", json.dumps(shape(v), ensure_ascii=False)[:400])
    else:
        print(json.dumps(shape(d), ensure_ascii=False))

plan = json.loads((W / "install_plan.json").read_bytes())
print("plan first item:", json.dumps(plan["files"][0], ensure_ascii=False)[:600])
nb = [f for f in plan["files"] if f.get("baseline")]
print("plan items with baseline:", len(nb))
for f in nb:
    print("  BASE", f["destination"], f["baseline"][:16], f["sha256"][:16])
print("plan last item:", json.dumps(plan["files"][-1], ensure_ascii=False)[:600])
print("plan keys:", [k for k in plan.keys()])
for k in plan.keys():
    if k != "files":
        print("  plan[", k, "] =", json.dumps(plan[k], ensure_ascii=False)[:500])

rf = json.loads((W / "validation/review_final.json").read_bytes())
for k, v in rf.items():
    if isinstance(v, (str, int, float, bool)) or v is None:
        print("review_final.", k, "=", str(v)[:200])
