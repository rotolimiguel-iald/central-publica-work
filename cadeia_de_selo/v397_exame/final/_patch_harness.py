# -*- coding: utf-8 -*-
"""_patch_harness.py -- copia do harness do fechar com o SANDBOX num caminho curto desta pasta de exame (MAX_PATH); nada mais muda."""
import os
P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame\sf\work\cadeia_de_selo\v397\pos_rito"
t = open(os.path.join(P, "harness_fechar_sandbox_v397.py"), encoding="utf-8").read()
a = 'OUT = os.path.join(HERE, "harness_saida_v397"); SB = os.path.join(OUT, "fechar_sandbox")'
assert t.count(a) == 1
b = 'OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v397_exame/hs"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v397_exame/sb"   # EXAME: caminho curto (MAX_PATH)'
t = t.replace(a, b)
open(os.path.join(P, "harness_fechar_sandbox_v397_EXAME.py"), "w", encoding="utf-8", newline="\n").write(t)
print("patched", b)
