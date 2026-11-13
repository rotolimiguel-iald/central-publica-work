import json, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
p = os.path.join(V, "kernel", "POS_BUILD_v411.json")
PB = json.load(open(p, encoding="utf-8"))
print("POS_BUILD_v411.json chaves:", list(PB.keys())[:14])
print("ok:", PB.get("ok"), "| n_modulos_compilados:", PB.get("n_modulos_compilados"), "| criterios:", PB.get("criterios"))
print("escada:", PB.get("escada"))
PR = json.load(open(os.path.join(V, "PREPARACAO_v411_PRONTA.json"), encoding="utf-8"))
print("PREPARACAO chaves:", list(PR.keys())[:12])
pt = PR.get("portoes")
print("portoes:", type(pt).__name__, (len(pt) if pt else None))
if isinstance(pt, dict):
    print("kernel:", pt.get("kernel"))
elif isinstance(pt, list):
    print([x for x in pt if "kernel" in json.dumps(x)][:2])
