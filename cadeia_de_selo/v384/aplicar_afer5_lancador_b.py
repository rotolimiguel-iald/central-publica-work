# -*- coding: utf-8 -*-
"""O filtro do mata_um com a MESMA classe do vigia da linha 28 ([\\\\ \"] no texto do sh: barra invertida, espaco ou aspas antes de um.py)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "rito_v384.sh")
s = open(P, "rb").read().decode("utf-8")
old = r"""-and \$_.CommandLine -match '(^|[\\ \"])um\.py\"?(\s|\$)' } | ForEach"""
new = r"""-and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach"""
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
vig = r"""-match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' }"""
assert s.count(vig) == 2, s.count(vig)   # o vigia (linha 28) e o mata_um, agora iguais
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok")
