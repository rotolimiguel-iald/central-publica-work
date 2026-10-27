# -*- coding: utf-8 -*-
"""main_sem_os_try_novos_v402.py -- exame final v402: o `main` do candidato, SEM os `try` novos da v402, difere do `main` da v401 selada em QUE instrucoes?
Esperado: so' o literal `seal = {...}`. Tambem: cada try novo tem handler com AVISO e nao relanca."""
import ast, json, os, difflib
B = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v402"
A_ = os.path.join(B, "base_v401", "um.py"); C_ = os.path.join(B, "um_v402_candidato.py")
mainA = [n for n in ast.parse(open(A_, encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
mainB = [n for n in ast.parse(open(C_, encoding="utf-8").read()).body if isinstance(n, ast.FunctionDef) and n.name == "main"][-1]
MARCAS = ("ponte_da_escala_dual_v402(", "queda_sem_geometria_v402(", "esperanca_condicional_v402(", "_v402_rodar_specs(", "_v402_")
i_new = [i for i, st in enumerate(mainB.body) if any(m in ast.unparse(st) for m in MARCAS) and not ast.unparse(st).startswith("seal = {")]
R = {"instrucoes_novas_v402": [(i, type(mainB.body[i]).__name__, mainB.body[i].lineno, ast.unparse(mainB.body[i])[:160]) for i in i_new]}
bodyB = [st for i, st in enumerate(mainB.body) if i not in i_new]
R.update({"n_A": len(mainA.body), "n_B": len(mainB.body), "args_iguais": ast.dump(mainA.args) == ast.dump(mainB.args), "mesmo_numero_sem_os_try": len(bodyB) == len(mainA.body),
          "todas_as_novas_sao_try": all(isinstance(mainB.body[i], ast.Try) for i in i_new)})
dif = []
for i, (a, b) in enumerate(zip(mainA.body, bodyB)):
    if ast.dump(a) != ast.dump(b):
        da, db = ast.unparse(a).splitlines(), ast.unparse(b).splitlines()
        dd = [l for l in difflib.unified_diff(da, db, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        dif.append({"i": i, "tipo": type(a).__name__, "inicio": ast.unparse(a)[:60], "n_linhas_diff": len(dd)})
R["instrucoes_diferentes_fora_dos_try_novos"] = dif
R["try_novos"] = []
for i in i_new:
    t = mainB.body[i]
    if isinstance(t, ast.Try):
        R["try_novos"].append({"linha": t.lineno, "handlers": [ast.unparse(h.type) if h.type else None for h in t.handlers], "handler_tem_AVISO": any("AVISO" in ast.unparse(h) for h in t.handlers),
                               "handler_relanca": any(isinstance(x, ast.Raise) for h in t.handlers for x in ast.walk(h)), "texto_do_handler": [ast.unparse(h)[:300] for h in t.handlers]})
def seal_keys(fn):
    for st in fn.body:
        if isinstance(st, ast.Assign) and ast.unparse(st).startswith("seal = {"):
            return [ast.unparse(k) for k in st.value.keys], [ast.unparse(v) for v in st.value.values]
(ka, va), (kb, vb) = seal_keys(mainA), seal_keys(mainB)
R["seal_literal"] = {"chaves_A": len(ka), "chaves_B": len(kb), "novas": [k for k in kb if k not in ka], "removidas": [k for k in ka if k not in kb],
                     "valores_das_antigas_iguais": all(dict(zip(ka, va))[k] == dict(zip(kb, vb))[k] for k in ka if k in kb),
                     "valores_das_novas": {k: dict(zip(kb, vb))[k][:200] for k in kb if k not in ka}}
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MAIN_SEM_OS_TRY_NOVOS_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:6000])
