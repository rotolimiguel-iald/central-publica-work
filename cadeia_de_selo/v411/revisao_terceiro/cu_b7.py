"""CU-B7: (i) nomes OPERADOR_1xnov no candidato: algum com contagem maior que na base v410? (ii) nos mudados/novos: leitura de arquivo da casa?"""
import ast, os, re, collections
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")
c = rd(os.path.join(V, "um_v411_candidato.py"))
b = rd(os.path.join(NOS, "um.py"))
pat = re.compile(r"(?:OPERADOR|GERENCIA)_1[0-2]nov[A-Za-z0-9_\u00c0-\u00ff]*")
cc = collections.Counter(pat.findall(c))
bb = collections.Counter(pat.findall(b))
print("nomes distintos candidato:", len(cc), "base:", len(bb))
mais = [(k[:70], cc[k], bb.get(k, 0)) for k in cc if cc[k] > bb.get(k, 0)]
print("nomes com contagem MAIOR que na base:", len(mais), mais[:10])
novos = [k[:70] for k in cc if k not in bb]
print("nomes que a base nao tem:", len(novos), novos[:10])
print("nomes que SUMIRAM do candidato:", len([k for k in bb if k not in cc]))
# (ii)
OLD = os.path.join(V, "um_v411_candidato.py.bak_20261112_195053")
so, sn = rd(OLD), c
t = ast.parse(sn)
OLDT = ast.parse(so)
od = {}
for n in OLDT.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        od[n.name] = ast.dump(n)
    elif isinstance(n, ast.Assign):
        od[",".join(x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name))] = ast.dump(n)
mud = []
for n in t.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        k = n.name
    elif isinstance(n, ast.Assign):
        k = ",".join(x.id for tg in n.targets for x in ast.walk(tg) if isinstance(x, ast.Name))
    else:
        continue
    if od.get(k) != ast.dump(n):
        mud.append((k, n))
for k, n in mud:
    seg = ast.get_source_segment(sn, n) or ""
    hits = [w for w in ("open(", "os.path", "cunhagens_13out", "VERBATIM", "work\\\\", "listdir", "glob", "subprocess", "read_text") if w in seg]
    if hits:
        print("no", k, "contem:", hits)
print("nos mudados/novos examinados:", len(mud))
