import json
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
c = json.load(open(T+"um_absoluto.json", encoding="utf-8"))["core"]
v = json.load(open("v391_um_absoluto.json", encoding="utf-8"))["core"]
kf=c["kernel_formalization"]; kv=v["kernel_formalization"]
print("t1 apagadas:", sorted(k for k,x in kf.items() if x is False))
print("v391 apagadas:", sorted(k for k,x in kv.items() if x is False))
ix=c["the_iald_index"]; print(json.dumps(ix["statuses"], ensure_ascii=False)[:3000])
print("amb new:", sorted(set(ix["ambiguos"]) - set(v["the_iald_index"]["ambiguos"])))
