import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
a = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open("v391_um_absoluto.json", encoding="utf-8"))["core"]
for k in sorted(set(a)|set(v)):
    x, y = a.get(k), v.get(k)
    ax = x.get("all_verified") if isinstance(x, dict) else None
    vy = y.get("all_verified") if isinstance(y, dict) else None
    if ax != vy:
        print(k, "v391:", vy, "| t1:", ax, "|", str((x or {}).get("verdict") if isinstance(x,dict) else "")[:150])
