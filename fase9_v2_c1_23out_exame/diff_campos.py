# -*- coding: utf-8 -*-
"""diff_campos.py -- auditoria c1: diff campo a campo (folhas) das secoes ALTERADAS da spec R5.2-E1 -> V2-c1; lista as folhas numericas que mudaram."""
import json, sys
A = json.load(open(sys.argv[1], encoding="utf-8"))["spec"]; B = json.load(open(sys.argv[2], encoding="utf-8"))["spec"]
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, p + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, p + "[%d]" % i)
    else: yield p, o
out = {}
for sec in sorted(set(A) & set(B)):
    if json.dumps(A[sec], sort_keys=True) == json.dumps(B[sec], sort_keys=True): continue
    la, lb = dict(leaves(A[sec])), dict(leaves(B[sec]))
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    out[sec] = {"folhas_so_R52": len(set(la) - set(lb)), "folhas_so_V2": len(set(lb) - set(la)), "folhas_mudadas": len([k for k in la if k in lb and la[k] != lb[k]]),
                "numericas_mudadas": {k: [la[k], lb[k]] for k in la if k in lb and la[k] != lb[k] and (num(la[k]) or num(lb[k]))},
                "numericas_novas": {k: lb[k] for k in set(lb) - set(la) if num(lb[k])}, "numericas_removidas": {k: la[k] for k in set(la) - set(lb) if num(la[k])}}
print(json.dumps(out, ensure_ascii=False, indent=1)[:9000])
json.dump(out, open("DIFF_CAMPOS_R52_V2C1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
