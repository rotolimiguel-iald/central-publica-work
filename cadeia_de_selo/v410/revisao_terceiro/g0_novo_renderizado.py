# -*- coding: utf-8 -*-
"""Revisor v410 R1: extrai o que e' NOVO nos textos renderizados do ensaio a seco (v410 contra v409): as linhas acrescentadas/alteradas (difflib por linhas) -> novo_*.txt nesta pasta."""
import difflib, sys
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/IALD/Central de Patentes/work/cadeia_de_selo/"
R = W + "v410/revisao_terceiro/"
pares = {"pt": ("v409/dry_v409/dry_v409_pt.txt", "v410/dry_v410/dry_v410_pt.txt"), "en": ("v409/dry_v409/dry_v409_en.txt", "v410/dry_v410/dry_v410_en.txt"),
         "md": ("v409/dry_v409/um_absoluto_forma_canonica.md", "v410/dry_v410/um_absoluto_forma_canonica.md")}
for k, (a, b) in pares.items():
    al = open(W + a, "rb").read().decode("utf-8", "replace").split("\n"); bl = open(W + b, "rb").read().decode("utf-8", "replace").split("\n")
    sm = difflib.SequenceMatcher(None, al, bl, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("insert", "replace"): out += ["[L%d]" % (j1 + 1)] + bl[j1:j2]
    open(R + "novo_%s.txt" % k, "w", encoding="utf-8").write("\n".join(out))
    print(k, "linhas novas/alteradas:", sum(1 for x in out if not x.startswith("[L")), "chars", sum(len(x) for x in out))
