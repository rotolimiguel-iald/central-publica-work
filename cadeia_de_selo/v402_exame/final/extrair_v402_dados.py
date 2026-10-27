# -*- coding: utf-8 -*-
"""extrair_v402_dados.py -- exame final v402, SO LEITURA: extrai por AST/literal_eval os dados novos da v402 do candidato
(_V402_SPECS, _V402_TEXTS, _V402_VERBATINS2, _V402_FONTES, _V402_RECUSA, _V402_CONTRACTS, _V402_NOMES_REGISTROS) e o codigo-fonte das 10 funcoes novas.
Grava V402_DADOS.json e v402_funcoes_novas.py.txt (para leitura)."""
import ast, json, os
C_ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v402\um_v402_candidato.py"
H = os.path.dirname(os.path.abspath(__file__))
src = open(C_, encoding="utf-8").read(); T = ast.parse(src)
D = {}; F = []
for n in T.body:
    nm = n.targets[0].id if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) else getattr(n, "name", None)
    if nm and nm.startswith("_V402_"):
        try: D[nm] = ast.literal_eval(n.value)
        except Exception as e: D[nm] = "NAO_LITERAL: " + ast.unparse(n.value)[:3000]
        D[nm + "__linhas"] = [n.lineno, n.end_lineno]
    if isinstance(n, ast.FunctionDef) and ("v402" in n.name):
        F.append("# ---- %s (l.%d-%d)\n%s\n" % (n.name, n.lineno, n.end_lineno, ast.get_source_segment(src, n)))
json.dump(D, open(os.path.join(H, "V402_DADOS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
open(os.path.join(H, "v402_funcoes_novas.py.txt"), "w", encoding="utf-8").write("\n".join(F))
print({k: (type(v).__name__, len(v) if hasattr(v, "__len__") else v) for k, v in D.items()})
