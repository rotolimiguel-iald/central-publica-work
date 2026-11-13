import a_lib, json
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_H0DN_CONTRACT"]); C = ns["_V411_H0DN_CONTRACT"]
for k, v in C.items():
    if k in ("insumos", "citados", "checagens", "mecanica"): continue
    s = json.dumps(v, ensure_ascii=False)
    print("%-28s %s" % (k, s[:330]))
print("checagens:", {k: v[:70] for k, v in C["checagens"].items()})
print("mecanica:", str(C["mecanica"])[:300])
