"""A1 (revisor A): AST de topo, base_v410\\um.py contra o candidato. Saida curta."""
import ast, hashlib, json, sys, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OUT = r"C:\t\k411c\revisao_A"
os.makedirs(OUT, exist_ok=True)

def load(p):
    return open(p, "rb").read().decode("utf-8")

def key(n, i):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return (type(n).__name__, n.name)
    if isinstance(n, ast.Assign):
        names = []
        for t in n.targets:
            for x in ast.walk(t):
                if isinstance(x, ast.Name):
                    names.append(x.id)
        return ("Assign", ",".join(names))
    if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
        return ("AnnAssign", n.target.id)
    if isinstance(n, (ast.Import, ast.ImportFrom)):
        return ("Import", ast.dump(n)[:200] + "|" + hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12])
    return ("Anon", ast.dump(n)[:110] + "|" + hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12])

def index(src):
    t = ast.parse(src)
    d = {}
    order = []
    for i, n in enumerate(t.body):
        k = key(n, i)
        h = hashlib.sha256(ast.dump(n).encode()).hexdigest()
        seg = None
        kk = k
        j = 2
        while kk in d:
            kk = (k[0], k[1] + "#%d" % j); j += 1
        d[kk] = (h, n.end_lineno - n.lineno, n.lineno, n.end_lineno)
        order.append(kk)
    return d, order, t

bsrc = load(os.path.join(V, "base_v410", "um.py"))
csrc = load(os.path.join(V, "um_v411_candidato.py"))
bd, bo, bt = index(bsrc)
cd, co, ct = index(csrc)
res = {"n_base": len(bd), "n_cand": len(cd)}
res["removidos"] = [k for k in bd if k not in cd]
res["novos"] = [k for k in cd if k not in bd]
res["mudados"] = [k for k in bd if k in cd and bd[k][0] != cd[k][0]]
res["iguais"] = sum(1 for k in bd if k in cd and bd[k][0] == cd[k][0])
# ordem relativa dos comuns
comuns_b = [k for k in bo if k in cd]
comuns_c = [k for k in co if k in bd]
res["ordem_relativa_dos_comuns_igual"] = comuns_b == comuns_c
res["novos_nomes"] = sorted(k[1] for k in res["novos"])
res["mudados_nomes"] = [k[1] for k in res["mudados"]]
res["removidos_nomes"] = [k[1] for k in res["removidos"]]
# onde os novos entram (posicao relativa)
pos = {}
for k in res["novos"]:
    i = co.index(k)
    prev = co[i-1][1] if i else None
    pos[k[1]] = prev
res["novos_depois_de"] = sorted(set(v for v in pos.values() if v))
res["novos"] = [list(k) for k in res["novos"]]
res["removidos"] = [list(k) for k in res["removidos"]]
res["mudados"] = [list(k) for k in res["mudados"]]
print(json.dumps({k: v for k, v in res.items() if k not in ("novos", "removidos", "mudados", "novos_nomes")}, ensure_ascii=False, indent=1))
print("novos_nomes", res["novos_nomes"])
json.dump(res, open(os.path.join(OUT, "a1_ast.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
