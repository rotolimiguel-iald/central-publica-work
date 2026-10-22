# -*- coding: utf-8 -*-
"""comparar_v393_v394.py -- NADA DA v393 PERDIDO: compara, no=a=no (AST), a v393 SELADA (base_v393\\um.py) com o candidato v394: todo no nomeado da v393 existe no candidato, ou foi mudado/removido por um PATCH declarado
(CANDIDATO_v394.json). Escreve COMPARACAO_V393_v394.json. uso: python -I -B -X utf8 comparar_v393_v394.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, "base_v393", "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


da = {nm(n): n for n in A.body if nm(n)}; db = {nm(n): n for n in B.body if nm(n)}
ig = [k for k in da if k in db and h(da[k]) == h(db[k])]
mud = [k for k in da if k in db and h(da[k]) != h(db[k])]; rem = [k for k in da if k not in db]; nov = [k for k in db if k not in da]
anon_a = sorted(h(n) for n in A.body if not nm(n)); anon_b = sorted(h(n) for n in B.body if not nm(n))
sa = {}
for x in anon_a:
    sa[x] = sa.get(x, 0) + 1
sb = {}
for x in anon_b:
    sb[x] = sb.get(x, 0) + 1
anon_perdidos = [k for k, v in sa.items() if sb.get(k, 0) < v]
res = {"nos_nomeados_v393": len(da), "iguais": len(ig), "mudados": mud, "removidos": rem, "novos": len(nov), "anonimos_da_v393_ausentes": len(anon_perdidos)}
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V393_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
