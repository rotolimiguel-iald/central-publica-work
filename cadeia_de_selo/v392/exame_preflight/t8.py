import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
a = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]["the_iald_index"]
v = json.load(open("v391_um_absoluto.json", encoding="utf-8"))["core"]["the_iald_index"]
for (ca, oa), (cv, ov) in zip(a["checks"], v["checks"]):
    if ca != cv or oa != ov:
        print("t1  :", oa, ca[:900]); print("v391:", ov, cv[:900]); print()
print([k for k in a if k not in ("checks",)])
