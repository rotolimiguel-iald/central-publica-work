# -*- coding: utf-8 -*-
"""Conferencia unica, item F2: renderiza SO' as constantes de texto do README (README_FRENTE, README_O_QUE_SAI, README_PONTEIRO_ABSTRACT) do modulo
pos_rito/textos_custodia_handoff_v410.py, SEM importar o modulo (ele le o Nos de producao): AST, so' as atribuicoes das constantes necessarias (e as assertivas das linhas >= 211), com delta_v410 como DL.
Grava cu_saidas/readme_render.json."""
import ast, json, re, sys, os, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
sys.path.insert(0, R)
import delta_v410 as DL  # noqa: E402

src = open(R + "pos_rito/textos_custodia_handoff_v410.py", "rb").read().decode("utf-8")
tr = ast.parse(src)
NEED = {"OBR_EN", "OBR_PT", "CLAY_PT", "CLAY_EN", "D83_PT", "D83_EN", "D81_PT", "D81_EN", "UMH_PT", "UMH_EN", "PAREDE_PT", "PAREDE_EN", "PODER_PT", "PODER_EN", "README_FRENTE_TETO_B", "_ESC_EN", "_ESC_PT", "_H0_EN", "_H0_PT", "README_FRENTE", "README_PONTEIRO_ABSTRACT", "README_O_QUE_SAI", "BLOCOS_README", "_RF_NOMES"}
ns = {"DL": DL, "re": re, "unicodedata": unicodedata, "sys": sys}
feitas = []
for n in tr.body:
    if isinstance(n, ast.Assign):
        nomes = set()
        for t in n.targets:
            if isinstance(t, ast.Name): nomes.add(t.id)
            elif isinstance(t, ast.Tuple): nomes |= {e.id for e in t.elts if isinstance(e, ast.Name)}
        if nomes & NEED:
            exec(compile(ast.Module([n], []), "tch", "exec"), ns); feitas.append(sorted(nomes))
    elif isinstance(n, ast.Assert) and 211 <= n.lineno <= 252:
        exec(compile(ast.Module([n], []), "tch", "exec"), ns); feitas.append("assert@%d" % n.lineno)
out = {k: ns[k] for k in sorted(NEED) if k in ns and k != "BLOCOS_README"}
out["_tamanho_README_FRENTE_B"] = len(ns["README_FRENTE"].encode("utf-8"))
json.dump(out, open(R + "revisao_terceiro/cu_saidas/readme_render.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("atribuicoes executadas:", len(feitas), "| faltam:", sorted(NEED - set(ns) - {"BLOCOS_README"}), "| assertivas executadas (todas passaram):", [f for f in feitas if isinstance(f, str)])
print("README_FRENTE (B):", out["_tamanho_README_FRENTE_B"], "| teto:", ns["README_FRENTE_TETO_B"])
