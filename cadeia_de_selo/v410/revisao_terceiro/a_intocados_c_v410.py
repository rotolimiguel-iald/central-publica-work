# -*- coding: utf-8 -*-
"""Revisor v410 R1 (complemento): segmentacao por no de nivel superior (comentarios/brancos que precedem o no ficam no segmento dele). Para todo no NAO declarado
(mudado ou novo), o segmento (texto, byte a byte) tem de ser IGUAL ao da base. Tambem: as linhas fora de nos declarados no diff por linhas sao so' comentario/branco."""
import ast, difflib, hashlib, json, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
bs = open(R + "base_v409/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
cmpj = json.load(open(R + "COMPARACAO_V409_v410.json", encoding="utf-8")); decl = set(cmpj["mudados"]) | set(cmpj["novos"])


def segs(s):
    tr = ast.parse(s); L = s.split("\n"); out = []; prev = 0
    for n in tr.body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
        out.append((nm, type(n).__name__, "\n".join(L[prev:n.end_lineno]), n.lineno)); prev = n.end_lineno
    tail = "\n".join(L[prev:])
    return out, tail


sb, tb = segs(bs); sc, tc = segs(cs)
print("segmentos base", len(sb), "cand", len(sc), "| cauda igual:", tb == tc, len(tb), len(tc))
cb = Counter((nm, ty, hashlib.sha256(t.encode()).hexdigest()[:12]) for nm, ty, t, _ in sb if nm not in decl)
cc = Counter((nm, ty, hashlib.sha256(t.encode()).hexdigest()[:12]) for nm, ty, t, _ in sc if nm not in decl and not (nm is None and ty == "Expr" and "_V410_" in t))
so_b = cb - cc; so_c = cc - cb
print("nos NAO declarados: segmentos so na base:", sum(so_b.values()), "so no cand:", sum(so_c.values()))
for k in list(so_b)[:20]: print("   so base:", k)
for k in list(so_c)[:20]: print("   so cand:", k)
if so_b or so_c:
    bm = {(nm, ty): t for nm, ty, t, _ in sb if nm not in decl}; cm = {(nm, ty): t for nm, ty, t, _ in sc if nm not in decl}
    for (nm, ty) in list(bm)[:4000]:
        if (nm, ty) in cm and bm[(nm, ty)] != cm[(nm, ty)] and nm:
            print("DIF em", nm)
            for l in list(difflib.unified_diff(bm[(nm, ty)].split("\n"), cm[(nm, ty)].split("\n"), "b", "c", lineterm="", n=0))[:10]: print("    ", l[:200])
# linhas de nivel superior inseridas que nao sao comentario/branco e estao fora de qualquer no declarado
ct = ast.parse(cs); cl = cs.split("\n"); bl = bs.split("\n")
iv = []
for n in ct.body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
    if nm in decl or (nm is None and isinstance(n, ast.Expr) and "_V410_" in "\n".join(cl[n.lineno-1:n.end_lineno])): iv.append((n.lineno, n.end_lineno))
sm = difflib.SequenceMatcher(None, bl, cl, autojunk=False)
mais = []; subst = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": continue
    for j in range(j1, j2):
        if not any(a <= j + 1 <= b for a, b in iv):
            t = cl[j].strip()
            if t and not t.startswith("#"): mais.append((j + 1, t[:160]))
            else: subst += 1
print("linhas fora dos nos declarados que NAO sao comentario/branco:", len(mais), "| so comentario/branco:", subst)
for m in mais[:20]: print("  ", m)
mud_iv = []
for n in ast.parse(bs).body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
    if nm in cmpj["mudados"]: mud_iv.append((n.lineno, n.end_lineno))
rem = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ("delete", "replace"):
        for i in range(i1, i2):
            if not any(a <= i + 1 <= b for a, b in mud_iv):
                t = bl[i].strip()
                if t and not t.startswith("#"): rem.append((i + 1, t[:160]))
print("linhas da base REMOVIDAS/alteradas fora dos nos mudados e nao-comentario:", len(rem))
for r in rem[:20]: print("  ", r)
