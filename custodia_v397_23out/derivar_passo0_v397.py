# -*- coding: utf-8 -*-
"""Deriva custodia_v397_passo0_backup.py do da v396 por trocas CONTADAS: o backup da v396, que ESTÁ no espelho, antes de sobrescrever."""
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")
s = (T / "custodia_v396_passo0_backup.py").read_text(encoding="utf-8")
for a, b, n in [
    ('r"""CUSTÓDIA v396 (22/10, handoff v396; molde v395: backup da v395).',
     'r"""CUSTÓDIA v397 (23/10, handoff v397; molde v396: backup da v396; regra do operador de 23/10: custodiar quando o handoff aparecer). '
     'Do molde: CUSTÓDIA v396 (22/10, handoff v396; molde v395: backup da v395).', 1),
    ('for v in SEMENTES + ("v395",):', 'for v in SEMENTES + ("v396",):', 1),
    ('assert pin_esp == PIN["v395"], "o espelho não está na v395 (pin %s; diário v395 = %s) — PARAR" % (pin_esp, PIN["v395"])',
     'assert pin_esp == PIN["v396"], "o espelho não está na v396 (pin %s; diário v396 = %s) — PARAR" % (pin_esp, PIN["v396"])', 1),
    ('dest = BK / ("um_v395_" + pin_esp)', 'dest = BK / ("um_v396_" + pin_esp)', 1),
    ('man = {"versao": "v395", "um_py_sha16": pin_esp,', 'man = {"versao": "v396", "um_py_sha16": pin_esp,', 1),
    ('(custódia v396; molde da custódia v395)', '(custódia v397; molde da custódia v396)', 1),
    ('"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v396_passo0_backup.py",', '"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v397_passo0_backup.py",', 1),
    ('assert ok == len(SEMENTES)  # v395: nenhuma semente', 'assert ok == len(SEMENTES)  # v396: nenhuma semente', 1),
]:
    c = s.count(a)
    assert c == n, (a[:90], c, n)
    s = s.replace(a, b)
d = T / "custodia_v397_passo0_backup.py"
assert not d.exists(), "já existe — PARAR"
compile(s, str(d), "exec")
d.write_text(s, encoding="utf-8")
print("ok", d.name, len(s))
