from b_lib import *
import re, collections
C = core()["core"]
L = C.get("the_ledger_of_charges_v383")
print(type(L).__name__, list(L.keys())[:30])
def find_lists(o, p, out):
    if isinstance(o, list) and o and isinstance(o[0], dict) and any(k in o[0] for k in ("outcome", "status", "veredito")):
        out.append((p, len(o)))
    if isinstance(o, dict):
        for k, v in o.items(): find_lists(v, p + "." + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o[:2]): find_lists(v, p + "[%d]" % i, out)
out = []; find_lists(L, "L", out); print(out[:12])
