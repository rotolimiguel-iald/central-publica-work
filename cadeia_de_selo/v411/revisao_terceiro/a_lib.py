"""biblioteca do revisor A: indice de topo do candidato (por AST, uma vez) e carregador por NOME, resolvendo NameError so' entre nomes de topo do proprio candidato."""
import ast, json, os, re, math, hashlib, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
OUT = r"C:\t\k411c\revisao_A"
CAND = os.path.join(V, "um_v411_candidato.py")
BASE = os.path.join(V, "base_v410", "um.py")
_IDXF = os.path.join(OUT, "idx_%s.json")

def indice(path, tag):
    f = _IDXF % tag
    st = os.stat(path)
    if os.path.exists(f):
        d = json.load(open(f, encoding="utf-8"))
        if d["size"] == st.st_size and d["mtime"] == st.st_mtime:
            return d["idx"]
    src = open(path, "rb").read().decode("utf-8")
    t = ast.parse(src)
    idx = {}
    for n in t.body:
        names = []
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            names = [n.name]
        elif isinstance(n, ast.Assign):
            names = [x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name)]
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            names = [n.target.id]
        for nm in names:
            idx.setdefault(nm, []).append((n.lineno, n.end_lineno))
    json.dump({"size": st.st_size, "mtime": st.st_mtime, "idx": idx}, open(f, "w", encoding="utf-8"))
    return idx

class Fonte:
    def __init__(self, path, tag):
        self.path = path
        self.idx = indice(path, tag)
        self.lines = open(path, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")
    def trecho(self, nome, k=-1):
        a, b = self.idx[nome][k]
        return "\n".join(self.lines[a - 1:b]) + "\n"
    def bloco(self, a, b):
        return "\n".join(self.lines[a - 1:b]) + "\n"
    def carregar(self, nomes, ns=None):
        ns = ns if ns is not None else {"re": re, "os": os, "math": math, "json": json, "hashlib": hashlib, "__name__": "revA_cand", "__file__": self.path}
        for n in nomes:
            exec(compile(self.trecho(n), "<cand:%s>" % n, "exec"), ns)
        return ns
    def chamar(self, ns, fn, *a, **k):
        for _ in range(120):
            try:
                return ns[fn](*a, **k)
            except NameError as e:
                m = re.search(r"name '([A-Za-z_0-9]+)' is not defined", str(e))
                if not (m and m.group(1) in self.idx):
                    raise
                self.carregar([m.group(1)], ns)
        raise RuntimeError("dependencias demais")
