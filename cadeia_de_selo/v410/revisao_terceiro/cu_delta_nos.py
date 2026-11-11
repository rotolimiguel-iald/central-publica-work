# -*- coding: utf-8 -*-
"""Revisor v410 conferencia unica D109, item A: delta de AST pre_r6fix (o que revisei na R3) x candidato atual,
por no de nivel superior. Funcoes: diff -/+ ; literais: tamanho e numero de linhas mudadas.
Tambem: funcoes do gate e veredito_h0dn identicas ao pre_r6fix E a base v409."""
import ast, difflib, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
a = open(R + "um_v410_candidato.pre_r6fix.py", "rb").read().decode("utf-8")
b = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
c = open(R + "base_v409/um.py", "rb").read().decode("utf-8")
al = a.split("\n"); bl = b.split("\n"); cl = c.split("\n")
ta = ast.parse(a); tb = ast.parse(b); tc = ast.parse(c)


def top(tr, L):
    d = {}
    for n in tr.body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
        if nm: d[nm] = (hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12], "\n".join(L[n.lineno - 1:n.end_lineno]), isinstance(n, ast.FunctionDef))
    return d


A = top(ta, al); B = top(tb, bl); C = top(tc, cl)
mud = sorted(k for k in A if k in B and A[k][0] != B[k][0]); nov = sorted(k for k in B if k not in A); rem = sorted(k for k in A if k not in B)
print("nos de nivel superior: pre_r6fix", len(A), "| atual", len(B), "| base v409", len(C))
print("mudados", len(mud), "novos", nov, "removidos", rem)
res = {"mudados": mud, "novos": nov, "removidos": rem, "funcoes": {}, "literais": {}}
for k in mud:
    fa, fb = A[k][1], B[k][1]
    if B[k][2]:
        d = [l for l in difflib.unified_diff(fa.split("\n"), fb.split("\n"), "pre", "novo", lineterm="", n=0) if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
        print("== FUNCAO", k, "linhas -/+:", len(d))
        for l in d[:60]: print("    ", l[:260])
        res["funcoes"][k] = len(d)
    else:
        d = [l for l in difflib.unified_diff(fa.split("\n"), fb.split("\n"), "pre", "novo", lineterm="", n=0) if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
        print("== LITERAL/ASSIGN", k, len(fa), "->", len(fb), "bytes; linhas mudadas -/+:", len(d))
        res["literais"][k] = [len(fa), len(fb), len(d)]
for k in nov:
    print("== NOVO", k, "(funcao)" if B[k][2] else "(literal)", len(B[k][1]), "chars")
print()
for nm in ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "veredito_h0dn", "_v410_h0dn_decode"):
    if nm in B:
        print("  %-36s atual==pre_r6fix: %s | atual==base_v409: %s" % (nm, (A.get(nm, (None,))[0] == B[nm][0]), (C.get(nm, (None,))[0] == B[nm][0]) if nm in C else "n/a (nao existe na v409)"))
    else:
        print("  %-36s ausente no atual" % nm)
print("veredito_h0dn texto-fonte identico (atual x pre_r6fix):", A["veredito_h0dn"][1] == B["veredito_h0dn"][1], "| sha16 do texto:", hashlib.sha256(B["veredito_h0dn"][1].encode("utf-8")).hexdigest()[:16])
res["veredito_h0dn_identico"] = A["veredito_h0dn"][1] == B["veredito_h0dn"][1]
# funcoes herdadas da v409 que mudaram em relacao a v409 e que NAO mudaram desde a R3 (apenas informativo): contagem
herd_mud_v409 = sorted(k for k in C if k in B and C[k][0] != B[k][0])
print("herdados da v409 que diferem da v409 no atual:", len(herd_mud_v409), "| destes, os que tambem diferem do pre_r6fix:", len([k for k in herd_mud_v409 if k in mud]))
res["herdados_mudados_v409"] = herd_mud_v409
res["herdados_mudados_v409_e_desde_r3"] = [k for k in herd_mud_v409 if k in mud]
json.dump(res, open(R + "revisao_terceiro/cu_delta_nos_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
