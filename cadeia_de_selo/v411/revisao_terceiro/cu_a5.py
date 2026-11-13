"""CU-A5: linhas ACRESCENTADAS (nos mudados/novos): numeros do teste ou beta digitados?"""
import ast, os, re, difflib, json, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053"); NEW = os.path.join(V, "um_v411_candidato.py")
def load(p): return open(p, "rb").read().decode("utf-8")
def nodes(src):
    t = ast.parse(src); d = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): k = n.name
        elif isinstance(n, ast.Assign): k = ",".join(x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name))
        else: continue
        d[k] = n
    return d
so, sn = load(OLD), load(NEW); ol, nl = so.split("\n"), sn.split("\n"); od, nd = nodes(so), nodes(sn)
CH = [k for k in nd if k not in od or ast.dump(od[k]) != ast.dump(nd[k])]
print(len(CH), CH)
alvo = ["0.0318", "0,0318", "6.10", "6,10", "6,11", "6.11", "4.37", "4,37", "4.38", "4,38", "0.605", "0,605", "0.812", "0,812", "6.7101", "5.1913", "0.0294", "0.1887", "0.0578"]
pat_num = re.compile(r"\b\d+[.,]\d{3,}\b")
tot = 0
for k in CH:
    A = ol[od[k].lineno-1:od[k].end_lineno] if k in od else []
    B = nl[nd[k].lineno-1:nd[k].end_lineno]
    add = [l[1:] for l in difflib.unified_diff(A, B, lineterm="", n=0) if l.startswith("+") and not l.startswith("+++")]
    tot += len(add)
    hits = [(a, l[:90]) for l in add for a in alvo if a in l]
    nums = [m.group(0) for l in add for m in pat_num.finditer(l)]
    print(k, "linhas acrescentadas:", len(add), "numeros-do-teste:", hits[:3], "decimais (>=3 casas):", nums[:5])
# estatuto_tex completo (as duas linhas)
n = nd["_v411_estatuto_tex"]; print("\n".join(nl[n.lineno-1:n.end_lineno])[:2500])
