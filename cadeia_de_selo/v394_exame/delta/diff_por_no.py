# -*- coding: utf-8 -*-
"""diff_por_no.py -- exame do delta v394: atribui cada bloco do diff A -> B (diff de bytes) ao no de topo (AST) que o contem, nos dois lados;
compara os nos de topo por AST (iguais / mudados / novos / removidos) e lista os anonimos novos. So' le; escreve so' em v394_exame\\delta.
uso: python -I -B -X utf8 diff_por_no.py <A.py> <B.py> <diff.txt> <saida.json>"""
import ast, hashlib, json, re, sys, collections
A_, B_, D_, S_ = sys.argv[1:5]
sa, sb = open(A_, "rb").read().decode("utf-8"), open(B_, "rb").read().decode("utf-8")
TA, TB = ast.parse(sa), ast.parse(sb)
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): return n.targets[0].id
    if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name): return n.target.id
    return None
def spans(T):
    out = []
    for n in T.body:
        out.append((n.lineno, n.end_lineno, nm(n) or ("<anon:%s@%d>" % (type(n).__name__, n.lineno))))
    return out
spA, spB = spans(TA), spans(TB)
def owner(sp, ln):
    for a, z, k in sp:
        if a <= ln <= z: return k
    return "<entre_nos>"
hdr = re.compile(r"^(\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?$")
por = collections.defaultdict(lambda: {"rem": 0, "add": 0})
for l in open(D_, encoding="utf-8", errors="replace"):
    m = hdr.match(l.rstrip("\n"))
    if m:
        a1 = int(m.group(1)); a2 = int(m.group(2) or a1); b1 = int(m.group(4)); b2 = int(m.group(5) or b1); t = m.group(3)
        if t in "cd":
            for ln in range(a1, a2 + 1): por["A:" + owner(spA, ln)]["rem"] += 1
        if t in "ca":
            for ln in range(b1, b2 + 1): por["B:" + owner(spB, ln)]["add"] += 1
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
da = {}; db = {}
for n in TA.body:
    k = nm(n)
    if k: da.setdefault(k, []).append(n)
for n in TB.body:
    k = nm(n)
    if k: db.setdefault(k, []).append(n)
mud = sorted(k for k in da if k in db and [h(x) for x in da[k]] != [h(x) for x in db[k]])
nov = sorted(k for k in db if k not in da); rem = sorted(k for k in da if k not in db)
anA = collections.Counter(h(n) for n in TA.body if not nm(n)); anB = collections.Counter(h(n) for n in TB.body if not nm(n))
anon_novos = [ast.unparse(n)[:300] for n in TB.body if not nm(n) and anB[h(n)] > anA.get(h(n), 0)]
anon_rem = [ast.unparse(n)[:300] for n in TA.body if not nm(n) and anA[h(n)] > anB.get(h(n), 0)]
R = {"A_sha16": hashlib.sha256(sa.encode()).hexdigest()[:16], "B_sha16": hashlib.sha256(sb.encode()).hexdigest()[:16],
     "nos_mudados": mud, "nos_novos": nov, "nos_removidos": rem, "anonimos_novos": anon_novos, "anonimos_removidos": anon_rem,
     "linhas_por_no": dict(sorted(por.items(), key=lambda kv: -(kv[1]["rem"] + kv[1]["add"])))}
json.dump(R, open(S_, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("A_sha16", "B_sha16", "nos_mudados", "nos_novos", "nos_removidos")}, ensure_ascii=False, indent=0))
print("ANON novos:", json.dumps(anon_novos, ensure_ascii=False)[:1500]); print("ANON removidos:", json.dumps(anon_rem, ensure_ascii=False)[:800])
for k, v in list(R["linhas_por_no"].items())[:60]: print(" ", k, v)
