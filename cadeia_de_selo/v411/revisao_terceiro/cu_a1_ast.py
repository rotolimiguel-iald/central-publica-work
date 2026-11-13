"""CU-A1: delta por AST de topo entre o candidato revisado na R1 (bak) e o final. Saida curta; detalhe em C:\t\k411c\revisao_CU."""
import ast, hashlib, json, os, difflib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OUT = r"C:\t\k411c\revisao_CU"
os.makedirs(OUT, exist_ok=True)
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")
NEW = os.path.join(V, "um_v411_candidato.py")

def load(p):
    return open(p, "rb").read().decode("utf-8")

def key(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return (type(n).__name__, n.name)
    if isinstance(n, ast.Assign):
        names = [x.id for t in n.targets for x in ast.walk(t) if isinstance(x, ast.Name)]
        return ("Assign", ",".join(names))
    if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
        return ("AnnAssign", n.target.id)
    d = ast.dump(n)
    return (type(n).__name__, hashlib.sha256(d.encode()).hexdigest()[:12])

def index(src):
    t = ast.parse(src)
    d = {}; order = []
    for n in t.body:
        k = key(n); kk = k; j = 2
        while kk in d:
            kk = (k[0], k[1] + "#%d" % j); j += 1
        d[kk] = (hashlib.sha256(ast.dump(n).encode()).hexdigest(), n.lineno, n.end_lineno)
        order.append(kk)
    return d, order

so, sn = load(OLD), load(NEW)
od, oo = index(so); nd, no = index(sn)
res = {"n_old": len(od), "n_new": len(nd)}
res["removidos"] = [k[1] for k in od if k not in nd]
res["novos"] = [k[1] for k in nd if k not in od]
res["mudados"] = [k[1] for k in od if k in nd and od[k][0] != nd[k][0]]
res["iguais"] = sum(1 for k in od if k in nd and od[k][0] == nd[k][0])
res["ordem_relativa_dos_comuns_igual"] = [k for k in oo if k in nd] == [k for k in no if k in od]
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(os.path.join(OUT, "a1_ast.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

ol = so.split("\n"); nl = sn.split("\n")
# diff por no mudado
def seg(lines, a, b):
    return lines[a-1:b]
with open(os.path.join(OUT, "a1_diff_nos.txt"), "w", encoding="utf-8") as f:
    for k in od:
        if k in nd and od[k][0] != nd[k][0]:
            a = seg(ol, od[k][1], od[k][2]); b = seg(nl, nd[k][1], nd[k][2])
            def abr(x):
                return [(l if len(l) <= 400 else l[:200] + "...[%d chars sha16=%s]..." % (len(l), hashlib.sha256(l.encode()).hexdigest()[:16]) + l[-100:]) for l in x]
            f.write("=== MUDADO %s (old %d-%d, new %d-%d)\n" % (k[1], od[k][1], od[k][2], nd[k][1], nd[k][2]))
            for ln in difflib.unified_diff(abr(a), abr(b), lineterm="", n=0):
                f.write(ln + "\n")
    for k in nd:
        if k not in od:
            b = seg(nl, nd[k][1], nd[k][2])
            f.write("=== NOVO %s (new %d-%d, %d linhas, %d chars)\n" % (k[1], nd[k][1], nd[k][2], len(b), sum(len(x) for x in b)))
    for k in od:
        if k not in nd:
            a = seg(ol, od[k][1], od[k][2])
            f.write("=== REMOVIDO %s (old %d-%d, %d linhas)\n" % (k[1], od[k][1], od[k][2], len(a)))
print("ok")
