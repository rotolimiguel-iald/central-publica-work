# -*- coding: utf-8 -*-
"""Teste da errata do G1 (fatos.contratos_de_registro, 11/11/2026): o um.py real e tres controles negativos sinteticos."""
import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import fatos
um = open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py", encoding="utf-8").read()
c = fatos.contratos_expected_ladder(um)
r = fatos.contratos_de_registro(um, c)
assert r == ["_V410_H0DN_CONTRACT", "_V410_HMS13_CONTRACT"], r
resto = {k: x for k, x in c.items() if k not in r}
assert len(resto) == 14 and set(resto.values()) == {12308}, resto
sint = (
    "_V999_KERNEL_CONTRACT = {'theorems': ['a'], 'baseline': 'x'}\n"          # kernel sem escada: NAO sai
    "_V999_NAOLIT_CONTRACT = {'registro': 'r', 'f': len('x')}\n"              # nao literal: NAO sai
    "_V999_ERRADO_CONTRACT = {'expected_ladder': 7, 'registro': 'r'}\n"       # escada errada: fica e diverge
    "_V999_REG_CONTRACT = {'registro': 'r', 'n_checks': 3}\n"                 # registro: sai
    "x = 1\n")
cs = fatos.contratos_expected_ladder(sint)
rs = fatos.contratos_de_registro(sint, cs)
assert rs == ["_V999_REG_CONTRACT"], rs
assert cs["_V999_KERNEL_CONTRACT"] is None and cs["_V999_NAOLIT_CONTRACT"] is None and cs["_V999_ERRADO_CONTRACT"] == 7
print("OK: registro = %s; 14 contratos de escada = 12308; controles negativos: kernel sem escada, nao literal e escada errada ficam na conferencia" % r)
