import ast, sys, json
sys.stdout.reconfigure(encoding="utf-8")
s = open("_nodes/_V409_TRADUCAO_CONTRACT.txt", encoding="utf-8").read()
C = ast.literal_eval(s.split("=", 1)[1].strip())
for k, v in C.items():
    j = json.dumps(v, ensure_ascii=False, default=str)
    print(k, type(v).__name__, (len(v) if hasattr(v, "__len__") else ""), j[:260])
