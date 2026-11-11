# -*- coding: utf-8 -*-
"""Revisor v410 R2: (1) literais _V410_* do candidato ATUAL (ast.literal_eval; nada executa) -> literais_v410.json; (2) texto renderizado NOVO (dry_v410 x dry_v409) -> novo_pt/en/md.txt."""
import ast, difflib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/IALD/Central de Patentes/work/cadeia_de_selo/"
R = W + "v410/"
s = open(R + "um_v410_candidato.py", "rb").read().decode("utf-8")
tr = ast.parse(s)
out = {}
for n in tr.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id.startswith("_V410_"):
        nm = n.targets[0].id
        try: out[nm] = ast.literal_eval(n.value)
        except Exception as e: out[nm] = "NAO_LITERAL: " + repr(e)[:100]
json.dump(out, open(R + "revisao_terceiro/literais_v410.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print({k: len(json.dumps(v, ensure_ascii=False, default=str)) for k, v in out.items()})
pares = {"pt": ("v409/dry_v409/dry_v409_pt.txt", "v410/dry_v410/dry_v410_pt.txt"), "en": ("v409/dry_v409/dry_v409_en.txt", "v410/dry_v410/dry_v410_en.txt"),
         "md": ("v409/dry_v409/um_absoluto_forma_canonica.md", "v410/dry_v410/um_absoluto_forma_canonica.md")}
for k, (a, b) in pares.items():
    al = open(W + a, "rb").read().decode("utf-8", "replace").split("\n"); bl = open(W + b, "rb").read().decode("utf-8", "replace").split("\n")
    sm = difflib.SequenceMatcher(None, al, bl, autojunk=False); o = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("insert", "replace"): o += ["[L%d]" % (j1 + 1)] + bl[j1:j2]
    open(R + "revisao_terceiro/novo_%s.txt" % k, "w", encoding="utf-8").write("\n".join(o))
    print(k, "linhas novas/alteradas:", sum(1 for x in o if not x.startswith("[L")), "chars", sum(len(x) for x in o))
