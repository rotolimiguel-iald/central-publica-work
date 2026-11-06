import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
def get(p):
    s = open(p, "rb").read().decode("utf-8"); tr = ast.parse(s)
    for n in tr.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V407_FONTES": return ast.literal_eval(n.value)
a = get(R + "base_v408/um.py"); b = get(R + "um_v409_candidato.py")
k = "psion_no_acervo_do_imac_03nov"
print("BASE :", a[k]["papel"]); print("CAND :", b[k]["papel"]); print({x: (a[k][x] == b[k][x]) for x in a[k]}); print([x for x in a if x != k and a[x] != b.get(x)], "demais chaves iguais:", all(a[x] == b[x] for x in a if x != k), len(a), len(b))
