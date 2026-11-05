# -*- coding: utf-8 -*-
"""Revisor v408 R1 (complemento): segmentacao por no de nivel superior (comentarios/brancos que precedem o no ficam no segmento dele). Para todo no NAO declarado
(mudado ou novo), o segmento (texto, byte a byte) tem de ser IGUAL ao da base. Substitui o diff por linhas (que desalinha onde a v408 insere um bloco grande)."""
import ast, hashlib, json, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
bs = open(R + "base_v407/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v408_candidato.py", "rb").read().decode("utf-8")
cmpj = json.load(open(R + "COMPARACAO_V407_v408.json", encoding="utf-8")); decl = set(cmpj["mudados"]) | set(cmpj["novos"])


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
cc = Counter((nm, ty, hashlib.sha256(t.encode()).hexdigest()[:12]) for nm, ty, t, _ in sc if nm not in decl and not (nm is None and ty == "Expr" and "_V408_" in t))
so_b = cb - cc; so_c = cc - cb
print("nos NAO declarados: segmentos so na base:", sum(so_b.values()), "so no cand:", sum(so_c.values()))
for k in list(so_b)[:20]: print("   so base:", k)
for k in list(so_c)[:20]: print("   so cand:", k)
# onde os diferentes: mostrar a diferenca textual do 1o
if so_b or so_c:
    import difflib
    bm = {(nm, ty): t for nm, ty, t, _ in sb if nm not in decl}; cm = {(nm, ty): t for nm, ty, t, _ in sc if nm not in decl}
    for (nm, ty) in list(bm)[:4000]:
        if (nm, ty) in cm and bm[(nm, ty)] != cm[(nm, ty)] and nm:
            print("DIF em", nm)
            for l in list(difflib.unified_diff(bm[(nm, ty)].split("\n"), cm[(nm, ty)].split("\n"), "b", "c", lineterm="", n=0))[:10]: print("    ", l[:200])
