"""CU-A2: mostra o diff por no, SEM gravar arquivo; o no _V411_VERBATINS2 e' so' resumido (guarda de nao-transcricao)."""
import ast, hashlib, os, sys, difflib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")
NEW = os.path.join(V, "um_v411_candidato.py")
want = sys.argv[1:]
def load(p): return open(p, "rb").read().decode("utf-8")
def nodes(src):
    t = ast.parse(src); d = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): k = n.name
        elif isinstance(n, ast.Assign): k = ",".join(x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name))
        else: continue
        d[k] = n
    return d
so, sn = load(OLD), load(NEW)
ol, nl = so.split("\n"), sn.split("\n")
od, nd = nodes(so), nodes(sn)
def abr(x, lim=260):
    r = []
    for l in x:
        r.append(l if len(l) <= lim else l[:lim//2] + "...[%d ch sha16=%s]..." % (len(l), hashlib.sha256(l.encode()).hexdigest()[:16]) + l[-60:])
    return r
for w in want:
    a = od.get(w); b = nd.get(w)
    print("=====", w, "old" if a else "-", "new" if b else "-")
    if w == "_V411_VERBATINS2":
        for tag, n, L in (("old", a, ol), ("new", b, nl)):
            if n: 
                seg = "\n".join(L[n.lineno-1:n.end_lineno])
                print(tag, "linhas", n.end_lineno-n.lineno+1, "chars", len(seg), "sha16", hashlib.sha256(seg.encode()).hexdigest()[:16], "head:", seg[:60].replace("\n"," "))
        continue
    A = ol[a.lineno-1:a.end_lineno] if a else []
    B = nl[b.lineno-1:b.end_lineno] if b else []
    if not a: print("\n".join(abr(B))); continue
    for ln in difflib.unified_diff(abr(A), abr(B), lineterm="", n=0):
        print(ln)
