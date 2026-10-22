# -*- coding: utf-8 -*-
# Exame final v394: nos de topo NOVOS (nomeados e anonimos) do candidato contra a v393 selada; nomes definidos 2x;
# atribuicoes/mutacoes de topo sobre nomes que JA existiam (monkeypatch de objeto da v393). So' LE; escreve so' em v394_exame.
import ast, hashlib, json, os, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v394"
H = os.path.dirname(os.path.abspath(__file__))
A = ast.parse(open(os.path.join(V, "base_v393", "um.py"), "rb").read().decode("utf-8"))
B = ast.parse(open(os.path.join(V, "um_v394_candidato.py"), "rb").read().decode("utf-8"))
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
        return n.target.id
    return None
def defs(T):
    d = {}
    for n in T.body:
        k = nm(n)
        if k:
            d.setdefault(k, []).append(n)
    return d
da, db = defs(A), defs(B)
dup_a = {k: [x.lineno for x in v] for k, v in da.items() if len(v) > 1}
dup_b = {k: [x.lineno for x in v] for k, v in db.items() if len(v) > 1}
novos_nomeados = sorted(((v[0].lineno, k, type(v[0]).__name__) for k, v in db.items() if k not in da))
# anonimos novos
sa = {}
for n in A.body:
    if not nm(n):
        sa[h(n)] = sa.get(h(n), 0) + 1
anon_novos = []
for n in B.body:
    if not nm(n):
        k = h(n)
        if sa.get(k, 0) > 0:
            sa[k] -= 1
        else:
            try:
                s = ast.unparse(n)
            except Exception:
                s = "?"
            anon_novos.append({"linha": n.lineno, "tipo": type(n).__name__, "src": s[:600]})
# mutacoes de topo (no bloco novo) sobre nomes da v393: Assign a Subscript/Attribute, chamadas de metodo .update/.append/.extend/.setdefault/.pop
nomes_v393 = set(da)
mut = []
for n in B.body:
    tgt_names = []
    if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
        tg = n.targets if isinstance(n, ast.Assign) else [n.target]
        for t in tg:
            base = t
            while isinstance(base, (ast.Subscript, ast.Attribute)):
                base = base.value
            if isinstance(base, ast.Name) and base is not t:
                tgt_names.append(base.id)
            if isinstance(n, ast.AugAssign) and isinstance(t, ast.Name):
                tgt_names.append(t.id)
    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute):
        base = n.value.func.value
        while isinstance(base, (ast.Subscript, ast.Attribute)):
            base = base.value
        if isinstance(base, ast.Name):
            tgt_names.append(base.id)
    for t in tgt_names:
        if t in nomes_v393 or t in ("globals",):
            mut.append({"linha": n.lineno, "alvo": t, "src": ast.unparse(n)[:300]})
# redefinicoes no candidato de nomes da v393 depois da linha onde a v393 os definiu (sombra)
sombra = []
for k, v in db.items():
    if k in da and len(v) > len(da[k]):
        sombra.append({"nome": k, "linhas_v394": [x.lineno for x in v], "linhas_v393": [x.lineno for x in da[k]]})
R = {"n_topo_v393": len(A.body), "n_topo_v394": len(B.body), "novos_nomeados": novos_nomeados, "n_novos_nomeados": len(novos_nomeados),
     "anonimos_novos": anon_novos, "dup_v393": dup_a, "dup_v394": dup_b, "mutacoes_de_topo_sobre_nomes_v393": mut, "redefinicoes_novas": sombra}
json.dump(R, open(os.path.join(H, "AST_NOVOS_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("n_topo_v393", "n_topo_v394", "n_novos_nomeados")}, ensure_ascii=False))
print("NOVOS NOMEADOS:"); [print("  ", x) for x in novos_nomeados]
print("ANONIMOS NOVOS:"); [print("  ", x["linha"], x["tipo"], x["src"][:300].replace("\n", " | ")) for x in anon_novos]
print("DUP v393:", dup_a); print("DUP v394:", dup_b)
print("MUTACOES:"); [print("  ", x) for x in mut]
print("REDEFINICOES NOVAS:", sombra)
