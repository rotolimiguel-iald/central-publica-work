# -*- coding: utf-8 -*-
"""Revisor v409: extrai do candidato o texto-fonte dos nos v409 (para leitura) em _nodes/<nome>.txt. So le o candidato."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
cs = open(R + "um_v409_candidato.py", "rb").read().decode("utf-8")
tr = ast.parse(cs); L = cs.split("\n")
os.makedirs(R + "revisao_terceiro/_nodes", exist_ok=True)
NOMES = ["_V409_FONTES", "_V409_NOMES_REGISTROS", "_V409_RECUSA", "_V409_REGISTROS_FUNCAO", "_V409_SPECS", "_V409_TRADUCAO_CONTRACT", "_V409_TRADUCAO_TEXT", "_V409_VERBATINS2",
         "_v409_formal", "_v409_guarda_frases", "_v409_rodar_specs", "_v409_sat", "traducao_turing_v409", "v409_traducao_mechanics"]
for n in tr.body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)): nm = n.name
    elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): nm = n.targets[0].id
    if nm in NOMES:
        t = "\n".join(L[n.lineno - 1:n.end_lineno])
        open(R + "revisao_terceiro/_nodes/%s.txt" % nm, "w", encoding="utf-8").write(t)
        print(nm, n.lineno, n.end_lineno, len(t))
