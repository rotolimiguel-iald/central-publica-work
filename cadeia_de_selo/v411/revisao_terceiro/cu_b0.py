import json, hashlib, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
d = json.load(open(os.path.join(V, "VERBATIM_CONGELADO_v411.json"), encoding="utf-8"))
print(list(d.keys()))
for k, v in d.items():
    if isinstance(v, (str, int, float, bool)) or v is None: print(k, str(v)[:150])
    elif isinstance(v, list): print(k, "list", len(v), str(v[0])[:300] if v else "")
    elif isinstance(v, dict): print(k, "dict", len(v), list(v.keys())[:4])
