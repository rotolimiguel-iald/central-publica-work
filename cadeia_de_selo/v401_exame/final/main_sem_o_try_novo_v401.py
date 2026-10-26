# -*- coding: utf-8 -*-
"""main_sem_o_try_novo_v401.py -- exame final v401: o `main` do candidato, SEM o `try` novo da falsidade, difere do `main` da v400 instalada em QUE instrucoes?
Esperado: so' o literal `seal = {...}` (duas chaves novas: falsidade_da_inercia_v401 e registros_v401). Tambem: o try novo e' um `try` com AVISO (fail-closed, nao derruba o rito)."""
import ast, json, os, difflib
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "um.py")
CAND = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v401\um_v401_candidato.py"
mainA = [n for n in ast.parse(open(NOS, encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
mainB = [n for n in ast.parse(open(CAND, encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
i_fal = [i for i, st in enumerate(mainB.body) if isinstance(st, ast.Try) and "falsidade_da_inercia_v401(core)" in ast.unparse(st)]
i_v401 = [i for i, st in enumerate(mainB.body) if isinstance(st, ast.Try) and ("falsidade_da_inercia_v401(core)" in ast.unparse(st) or "_v401_rodar_specs(core)" in ast.unparse(st))]
R0 = {"instrucoes_novas_v401": [(i, type(mainB.body[i]).__name__, ast.unparse(mainB.body[i])[:120]) for i in i_v401]}
bodyB = [st for i, st in enumerate(mainB.body) if i not in i_v401]
R = {**R0, "n_A": len(mainA.body), "n_B": len(mainB.body), "i_try_falsidade": i_fal, "args_iguais": ast.dump(mainA.args) == ast.dump(mainB.args), "mesmo_numero_sem_o_try": len(bodyB) == len(mainA.body)}
dif = []
for i, (a, b) in enumerate(zip(mainA.body, bodyB)):
    if ast.dump(a) != ast.dump(b):
        da, db = ast.unparse(a).splitlines(), ast.unparse(b).splitlines()
        dd = [l for l in difflib.unified_diff(da, db, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        dif.append({"i": i, "tipo": type(a).__name__, "inicio": ast.unparse(a)[:60], "diff": [l[:300] for l in dd][:12]})
R["instrucoes_diferentes_fora_do_try_novo"] = dif
if i_fal:
    t = mainB.body[i_fal[0]]
    R["try_novo"] = {"linha": t.lineno, "handlers": [ast.unparse(h.type) if h.type else None for h in t.handlers], "handler_tem_AVISO": any("AVISO" in ast.unparse(h) for h in t.handlers), "handler_relanca": any(isinstance(x, ast.Raise) for h in t.handlers for x in ast.walk(h)),
                    "texto_do_handler": [ast.unparse(h)[:400] for h in t.handlers]}
# o literal seal: chaves novas
def seal_keys(fn):
    for st in fn.body:
        if isinstance(st, ast.Assign) and ast.unparse(st).startswith("seal = {"):
            return [ast.unparse(k) for k in st.value.keys]
ka, kb = seal_keys(mainA), seal_keys(mainB)
R["seal_literal"] = {"chaves_A": len(ka), "chaves_B": len(kb), "novas": [k for k in kb if k not in ka], "removidas": [k for k in ka if k not in kb]}
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MAIN_SEM_O_TRY_NOVO_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:4000])
