# -*- coding: utf-8 -*-
"""G1 (25/10/2026): o ACOM recusa registro sem fonte explícita («Records require at least one explicit source»). Os registros d1_gatilho
(a regra do operador) e p1_do_operador (as pendências do handoff) iam com sources = []. Agora: d1 aponta para a ordem verbatim do operador
e para o handoff; p1 aponta para o handoff. Trocas contadas; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\memorias.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
CR, LF = chr(13), chr(10)
NL = CR + LF if (CR + LF) in s else LF
BS = chr(92)
ORDEM = "C:" + BS + "IALD" + BS + "Central de Patentes" + BS + "work" + BS + "php_e_v396_22out" + BS + "OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt"
pares = [
    ('conferidas por tools/custodiar.py vigiar.", "sources": []}]',
     'conferidas por tools/custodiar.py vigiar.", "sources": _art(Path(r"' + ORDEM + '"), ctx.handoff.caminho)}]'),
    ('[:1500], "sources": []})',
     '[:1500], "sources": _art(ctx.handoff.caminho)})'),
]
for a, b in pares:
    n = s.count(a)
    assert n == 1, (a[:60], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("memorias.py: d1_gatilho e p1_do_operador com fonte explícita")
