import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
a = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open("v391_um_absoluto.json", encoding="utf-8"))["core"]
for k in ["the_tetelestai_declaration_v374","the_iald_index","uv_frontier_retyped_v373","the_bootstrap"]:
    print("==", k)
    for c in a[k].get("checks", []):
        if not c[1]: print("   FAIL", str(c[0])[:300])
u=a["uv_frontier_retyped_v373"]; print({kk:str(vv)[:300] for kk,vv in u.items() if kk not in ("checks",)})
print("v391 uv:", {kk:str(vv)[:300] for kk,vv in v["uv_frontier_retyped_v373"].items() if kk not in ("checks",)})
