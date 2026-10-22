# -*- coding: utf-8 -*-
"""Move o toolchain copiado para um caminho curto (<r2>/T): o lean.exe nao abre caminhos > 259 caracteres."""
import os

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFX = "\\\\?\\"
src = PFX + os.path.join(R2, "lean", "toolchain_v4.31.0")
dst = PFX + os.path.join(R2, "T")
print(repr(src[:8]))
os.rename(src, dst)
mx, arq = 0, ""
for dp, dn, fn in os.walk(dst):
    for f in fn:
        p = os.path.join(dp, f)[len(PFX):]
        if len(p) > mx:
            mx, arq = len(p), p
print("movido para", dst[len(PFX):], "| maior caminho:", mx, arq[-90:])
