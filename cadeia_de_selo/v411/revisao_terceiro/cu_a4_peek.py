import json
c = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))
print(list(c.keys())[:8])
core = c["core"] if "core" in c else c
print(len(core))
r = core["h0dn_bg1_v411"]
print(list(r.keys()))
m = r.get("mechanics", {})
print(list(m.keys()))
ck = m.get("checks", [])
print(len(ck), [ (x["id"], x["ok"]) for x in ck])
print(r["verdict"][:300], r["all_verified"])
a = json.load(open(r"C:\t\k411c\revisao_A\a2_blobs.json", encoding="utf-8"))
for k, v in a.items(): print(k, v.get("rel"))
for k in r:
    if isinstance(r[k], (dict, list)): print(k, type(r[k]).__name__, len(r[k]), str(r[k])[:200])
    else: print(k, str(r[k])[:200])
