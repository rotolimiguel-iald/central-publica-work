# -*- coding: utf-8 -*-
"""Revisor v408 R1: complemento da a_intocados: para os blocos fora dos nos declarados, lista cada LINHA fora (so' o que nao e' comentario/branco); confirma que sao so' comentarios e brancos."""
import ast, difflib, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
bs = open(R + "base_v407/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v408_candidato.py", "rb").read().decode("utf-8")
bt = ast.parse(bs); ct = ast.parse(cs); bl = bs.split("\n"); cl = cs.split("\n")
import json
cmpj = json.load(open(R + "COMPARACAO_V407_v408.json", encoding="utf-8")); decl = set(cmpj["mudados"]) | set(cmpj["novos"])
iv = []
for n in ct.body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
    if nm in decl or (isinstance(n, ast.Expr) and n.lineno >= 224369): iv.append((n.lineno, n.end_lineno))
sm = difflib.SequenceMatcher(None, bl, cl, autojunk=False)
subst = 0; mais = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": continue
    for j in range(j1, j2):
        if not any(a <= j + 1 <= b for a, b in iv):
            t = cl[j].strip()
            if t and not t.startswith("#"): mais.append((j + 1, t[:160]))
            else: subst += 1
    for i in range(i1, i2):   # linhas removidas da base: tem de ser comentario/branco ou estar em no mudado
        t = bl[i].strip()
if mais: print("LINHAS FORA que NAO sao comentario/branco:", len(mais)); [print("  ", m) for m in mais[:20]]
else: print("todas as linhas fora dos nos declarados sao comentarios/brancos:", subst)
# linhas removidas da base fora de nos mudados da base
mud_iv = []
for n in bt.body:
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
