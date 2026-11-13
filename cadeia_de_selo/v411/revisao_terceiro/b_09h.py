from b_lib import *
co = json.loads(rd(NOS + r"\um_absoluto.json"))["core"]; cn = core()["core"]
def dd(a, b, path, out):
    if type(a) != type(b): out.append((path, str(a)[:100], str(b)[:100])); return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a: out.append((path + "." + k, "<ausente>", "novo")); continue
            if k not in b: out.append((path + "." + k, "antigo", "<ausente>")); continue
            dd(a[k], b[k], path + "." + k, out)
    elif isinstance(a, list):
        if len(a) != len(b): out.append((path, "len %d" % len(a), "len %d" % len(b))); return
        for i, (x, y) in enumerate(zip(a, b)): dd(x, y, path + "[%d]" % i, out)
    else:
        if a != b: out.append((path, str(a)[:100], str(b)[:100]))
out = []
dd(co["interface_is_light"], cn["interface_is_light"], "interface_is_light", out)
print(len(out))
for o in out[:12]: print(o)
# where does 'INTERFACE_IS_LIGHT_' verdict live
def find(o, pat, path, hits):
    if isinstance(o, dict):
        for k, v in o.items(): find(v, pat, path + "." + k, hits)
    elif isinstance(o, str) and pat in o: hits.append((path, o[:80]))
for nm, c in (("old", co), ("new", cn)):
    h = []; find(c, "INTERFACE_IS_LIGHT_", "", h); print(nm, h[:4])
