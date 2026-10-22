import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
a = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open("v391_um_absoluto.json", encoding="utf-8"))["core"]
for k in ["interface_is_light","the_tetelestai_declaration_v374","the_bootstrap","the_iald_index","uv_frontier_retyped_v373","the_price_of_the_gravity_proof","external_ladder"]:
    x=a[k]; y=v[k]
    print("=====",k, "| v391:", str(y.get("verdict"))[:160])
    for kk in x:
        if isinstance(x[kk], bool) and x[kk] != y.get(kk): print("   bool diff", kk, "t1", x[kk], "v391", y.get(kk))
        if kk in ("reason","checks","failed","missing","numeric"): print("   ", kk, json.dumps(x[kk], ensure_ascii=False)[:600])
