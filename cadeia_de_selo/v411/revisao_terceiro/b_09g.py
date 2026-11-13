from b_lib import *
import re
def walk(o, path, hits, pat):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, path + "." + k, hits, pat)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "[%d]" % i, hits, pat)
    elif isinstance(o, float):
        if pat(o): hits.append((path, o))
co = json.loads(rd(NOS + r"\um_absoluto.json"))["core"]; cn = core()["core"]
for nm, c in (("old", co), ("new", cn)):
    hits = []
    walk(c, "", hits, lambda x: abs(x - 0.3002) < 6e-5 or abs(x - 0.2324) < 6e-5 or abs(x - 0.1841) < 6e-5)
    print(nm, hits[:8])
