import json, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
N = r"C:\t\k411c\falso_nos_v411"
s = json.load(open(os.path.join(N, "um_absoluto_selo.json"), encoding="utf-8"))
b = json.load(open(os.path.join(V, "base_v410", "um_absoluto_selo.json"), encoding="utf-8"))
print("qg_closure_verdict igual:", s["qg_closure_verdict"] == b["qg_closure_verdict"], "|", s["qg_closure_verdict"][:60])
dif = [k for k in b if k in s and json.dumps(b[k], sort_keys=True) != json.dumps(s[k], sort_keys=True)]
print("chaves do selo com valor diferente (base v410 -> emulado v411):", dif)
for k in ("um_version", "n_theorems", "escada", "kernel"):
    if k in s: print(k, "|", str(b.get(k))[:90], "->", str(s.get(k))[:90])
fl = [k for k in s if "flag" in k.lower() or "bandeira" in k.lower()]
print("chaves de bandeiras:", fl)
for k in fl: print(k, b.get(k) == s.get(k))
print("registros_v410 igual:", b.get("registros_v410") == s.get("registros_v410") if "registros_v410" in b else "n/a")
