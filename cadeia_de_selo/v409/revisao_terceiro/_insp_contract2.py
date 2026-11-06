import ast, sys, json
sys.stdout.reconfigure(encoding="utf-8")
s = open("_nodes/_V409_TRADUCAO_CONTRACT.txt", encoding="utf-8").read()
C = ast.literal_eval(s.split("=", 1)[1].strip())
for k in ("fica_aberto", "fechado_nesta_versao", "alcance"):
    print("##", k)
    for kk, v in C[k].items(): print("  *", kk, ":", v)
