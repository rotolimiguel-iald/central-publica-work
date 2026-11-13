import ast, hashlib, os, json
import a_lib
V = a_lib.V
f = a_lib.Fonte(a_lib.CAND, "cand")
src_rt = open(os.path.join(V, "runtime_h0dn_v411.py"), "rb").read().decode("utf-8")
t = ast.parse(src_rt)
dump = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()
for n in t.body:
    nm = None
    if isinstance(n, ast.FunctionDef): nm = n.name
    elif isinstance(n, ast.Assign): nm = n.targets[0].id
    if not nm: continue
    if nm not in f.idx:
        print("%-34s AUSENTE no candidato" % nm); continue
    ct = ast.parse(f.trecho(nm)).body[0]
    print("%-34s AST igual ao runtime_h0dn_v411.py: %s" % (nm, dump(ct) == dump(n)))
# outras fontes do bloco: quadro_v411.py
src_q = open(os.path.join(V, "quadro_v411.py"), "rb").read().decode("utf-8")
tq = ast.parse(src_q)
for n in tq.body:
    nm = None
    if isinstance(n, ast.FunctionDef): nm = n.name
    elif isinstance(n, ast.Assign): nm = n.targets[0].id if isinstance(n.targets[0], ast.Name) else None
    if not nm: continue
    if nm not in f.idx:
        print("quadro: %-30s AUSENTE" % nm); continue
    ct = ast.parse(f.trecho(nm)).body[0]
    print("quadro: %-30s AST igual: %s" % (nm, dump(ct) == dump(n)))
