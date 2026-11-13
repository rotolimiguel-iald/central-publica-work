"""CU-D2: terceiros (nao stdlib, nao locais) importados pelos scripts da cadeia que rodam com python -I (sem user-site), transitivamente pelos modulos locais."""
import ast, importlib.util, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
TOOLS = r"C:\IALD\Central de Patentes\work\cadeia_de_selo"
SEL = os.path.join(V, "pos_rito")
sys.dont_write_bytecode = True
std = set(sys.stdlib_module_names)
rd = lambda p: open(p, "rb").read().decode("utf-8")
chain = rd(os.path.join(SEL, "chain_pos_rito_v411.sh"))
# linhas que rodam com $PY (-I) vs $PY_B
comI = set(re.findall(r"\$PY \"\$(?:SEL|PK)/([A-Za-z0-9_.\-]+\.py)\"", chain)) | set(re.findall(r"\$PY \"\$FILA\"", chain) and ["fila_memoria_v411.py"])
comB = set(re.findall(r"\$PY_B ([A-Za-z0-9_.\-]+\.py)", chain)) | set(re.findall(r"\$PY_B \"\$(?:SEL|PK)/([A-Za-z0-9_.\-]+\.py)\"", chain))
print("rodam com -I:", sorted(comI))
print("rodam com -B (sem -I):", sorted(comB))


def local(m, d):
    for b in (d, V, SEL, TOOLS):
        p = os.path.join(b, m + ".py")
        if os.path.isfile(p):
            return p
    return None


def terceiros(p, vis=None, acc=None):
    vis = set() if vis is None else vis
    acc = {} if acc is None else acc
    if p in vis:
        return acc
    vis.add(p)
    t = ast.parse(rd(p))
    for x in ast.walk(t):
        nomes = []
        if isinstance(x, ast.Import):
            nomes = [a.name.split(".")[0] for a in x.names]
        elif isinstance(x, ast.ImportFrom) and x.level == 0 and x.module:
            nomes = [x.module.split(".")[0]]
        for m in nomes:
            if m in std:
                continue
            lp = local(m, os.path.dirname(p))
            if lp:
                terceiros(lp, vis, acc)
            else:
                acc.setdefault(m, set()).add(os.path.basename(p))
    return acc


for n in sorted(comI | {"conferir_rito_v411.py"}):
    p = None
    for b in (SEL, V, TOOLS):
        if os.path.isfile(os.path.join(b, n)):
            p = os.path.join(b, n)
            break
    if not p:
        print("nao achado:", n)
        continue
    a = terceiros(p)
    print("%-28s terceiros: %s" % (n, {k: sorted(v)[:3] for k, v in a.items()}))
