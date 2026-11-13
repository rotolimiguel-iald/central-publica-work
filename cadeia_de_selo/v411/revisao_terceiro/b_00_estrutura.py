from b_lib import *
c = core()["core"]
h = c["h0dn_bg1_v411"]
print(list(h.keys()))
v = h.get("values")
print(json.dumps(v, ensure_ascii=False)[:2500])
for k in h:
    if k not in ("values","insumos"): 
        s = json.dumps(h[k], ensure_ascii=False)
        print(k, '=>', s[:300])
