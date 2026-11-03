# -*- coding: utf-8 -*-
"""Revisor terceiro v406: as tres funcoes que mudaram so' no literal (rede_fock_v394, psibit_v395, testemunha_estatica_v396), diff de fonte base x candidato;
mais o nivel superior completo (qualquer no do corpo do modulo, nao so' os nomeados) e os quatro blocos de specs."""
import ast, difflib, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
bs = open(R + "base_v405/um.py", "rb").read().decode("utf-8"); cs = open(R + "um_v406_candidato.py", "rb").read().decode("utf-8")
bt = ast.parse(bs); ct = ast.parse(cs)
bl = bs.split("\n"); cl = cs.split("\n")


def fn(tr, lines, nome):
    for n in tr.body:
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return "\n".join(lines[n.lineno - 1:n.end_lineno])
    return None


for nome in ["rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"]:
    a = fn(bt, bl, nome); b = fn(ct, cl, nome)
    print("=" * 30, nome, len(a), len(b))
    for l in difflib.unified_diff(a.split("\n"), b.split("\n"), "base", "cand", lineterm="", n=0):
        print(l[:1500])

# corpo do modulo: tudo que nao e' no nomeado
def sig(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): k = ("def", n.name)
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): k = ("asg", n.targets[0].id)
    else: k = (type(n).__name__, "")
    return k, hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]


from collections import Counter
cb = Counter(sig(n) for n in bt.body); cc = Counter(sig(n) for n in ct.body)
so_base = cb - cc; so_cand = cc - cb
print("nos do corpo so na base:", len(so_base)); print("nos do corpo so no cand:", len(so_cand))
nomes_b = sorted({k[0] for k in so_base}); nomes_c = sorted({k[0] for k in so_cand})
print("so base (tipo,nome):", [x for x in nomes_b if x[0] not in ("def", "asg")] or "so' nomeados")
print("so cand nao-nomeados:", [x for x in nomes_c if x[0] not in ("def", "asg")])
print("so cand nomeados:", len([x for x in nomes_c if x[0] in ("def", "asg")]))
print([x for x in nomes_b if x not in nomes_c][:50])
