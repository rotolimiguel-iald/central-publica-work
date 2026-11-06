import ast, sys, json
sys.stdout.reconfigure(encoding="utf-8")
s = open("_nodes/_V409_SPECS.txt", encoding="utf-8").read()
S = ast.literal_eval(s.split("=", 1)[1].strip())
print(type(S).__name__, len(S))
for sp in S:
    print("==", sp.get("nome") or sp.get("name"), list(sp.keys()))
    for k, v in sp.items():
        if k in ("checks", "erratas"): continue
        print("   ", k, ":", json.dumps(v, ensure_ascii=False)[:180])
    chs = sp.get("checks", [])
    print("   n_checks", len(chs))
    for c in chs:
        print("     ", c.get("id"), "|", c.get("op"), "|", json.dumps(c.get("caminho"), ensure_ascii=False)[:90], "|", (c.get("descricao") or "")[:110])
