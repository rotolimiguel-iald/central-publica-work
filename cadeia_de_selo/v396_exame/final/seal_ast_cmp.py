# -*- coding: utf-8 -*-
"""seal_ast_cmp.py -- compara por AST o literal `seal = {...}` do main da v395 instalada (A) e do candidato (B): chaves e expressoes de valor."""
import ast, sys
def seal(p):
    T = ast.parse(open(p, encoding="utf-8").read())
    m = [n for n in T.body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
    st = [n for n in ast.walk(m) if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "seal"]
    assert len(st) == 1 and isinstance(st[0].value, ast.Dict)
    return {ast.literal_eval(k): ast.dump(v) for k, v in zip(st[0].value.keys, st[0].value.values)}, m
(a, ma), (b, mb) = seal(sys.argv[1]), seal(sys.argv[2])
print("chaves A", len(a), "B", len(b), "| so_B", sorted(set(b) - set(a)), "| so_A", sorted(set(a) - set(b)), "| valor mudado:", sorted(k for k in a if k in b and a[k] != b[k]))
# as instrucoes do main: quais mudaram (por AST), fora as novas
la = [ast.dump(s) for s in ma.body]; lb = [ast.dump(s) for s in mb.body]
import difflib
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        print(tag, "A[%d:%d]" % (i1, i2), "B[%d:%d]" % (j1, j2), [ast.unparse(mb.body[j])[:110].replace("\n", " | ") for j in range(j1, j2)][:3])
