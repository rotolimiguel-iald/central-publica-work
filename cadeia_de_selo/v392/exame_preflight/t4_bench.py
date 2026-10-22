import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
core = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
b = core["bench_lean_controls"]
print({k:(v if not isinstance(v,(list,dict)) else type(v).__name__+str(len(v))) for k,v in b.items()})
for k in ("checks","criteria","seals"):
    if k in b: print(k, json.dumps(b[k], ensure_ascii=False)[:3000])
for m in ("interface_is_light","the_bootstrap","the_iald_index","uv_frontier_retyped_v373","the_tetelestai_declaration_v374","external_ladder","the_price_of_the_gravity_proof"):
    v = core.get(m, {}); print("==", m, v.get("all_verified"), str(v.get("verdict"))[:200])
