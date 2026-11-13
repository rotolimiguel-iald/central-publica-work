import json, os, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
b = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))
print("topo base:", list(b.keys())[:10], "| topo cand:", list(c.keys())[:10])
cb, cc = b["core"], c["core"]
print("n chaves core base", len(cb), "cand", len(cc))
novas = [k for k in cc if k not in cb]; sumidas = [k for k in cb if k not in cc]
print("novas:", novas); print("sumidas:", sumidas)
def canon(x): return json.dumps(x, sort_keys=True, ensure_ascii=False)
dif = [k for k in cb if k in cc and canon(cb[k]) != canon(cc[k])]
print("chaves antigas com valor diferente:", len(dif)); 
for k in dif:
    print("  ", k, len(canon(cb[k])), len(canon(cc[k])))
# top-level non-core
for k in b:
    if k != "core":
        print("topo", k, canon(b[k]) == canon(c.get(k)) if k in c else "ausente")
