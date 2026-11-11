# -*- coding: utf-8 -*-
"""Revisor v410: despeja os textos/contratos literais da secao v410 do CANDIDATO (por ast.literal_eval; nada executa) em arquivos legiveis desta pasta."""
import ast, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
sec = open(R + "revisao_terceiro/cand_v410_secao.py", encoding="utf-8").read()
tr = ast.parse(sec)
out = {}
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id.startswith("_V410_"):
        nm = n.targets[0].id
        try:
            out[nm] = ast.literal_eval(n.value)
        except Exception as e:
            out[nm] = "NAO_LITERAL: " + repr(e)[:100]
json.dump(out, open(R + "revisao_terceiro/literais_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
for k, v in out.items():
    print(k, type(v).__name__, len(json.dumps(v, ensure_ascii=False, default=str)))
for nm in ("_V410_AESCALA_TEXT", "_V410_H0DN_TEXT", "_V410_HMS13_TEXT", "_V410_IALD2_TEXT"):
    open(R + "revisao_terceiro/txt_%s.json" % nm, "w", encoding="utf-8").write(json.dumps(out[nm], ensure_ascii=False, indent=1))
