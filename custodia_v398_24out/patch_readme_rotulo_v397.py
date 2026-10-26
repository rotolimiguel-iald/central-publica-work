# -*- coding: utf-8 -*-
"""Errata do rótulo (achado L03 do auditor do G1, 24/10/2026): o item do Teste da Única Palavra na frente do README dizia «(v398, 2026-10-24 …)»
porque usava a versão/data do SELO corrente; o registro é o da v397. Agora o rótulo lê a versão do NOME do registro e a data da assinatura
do próprio registro (extras.assinatura), e diz em que selo foi lido. Troca contada; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path("C:/IALD/Artigo/the_boundary/tools/gerar_readme_frente.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "read in the current seal" in s:
    raise SystemExit("já aplicado")
A = ("    F.append('\\n> **The Unique Word Test (%s, %s) `[REAL: read from registry %s]`:** z_disc = %.2f (calibrated; one-sided p %.1e), '\n")
B = ("    _mv = re.search(r'_v(\\d{3,})$', _k); _vreg = ('v' + _mv.group(1)) if _mv else '?'          # a versão do REGISTRO, não a do selo corrente (errata 24/10)\n"
     "    _md = re.search(r'\\d{2}/\\d{2}/\\d{4}', str((_v.get('extras') or {}).get('assinatura') or '')); _dreg = _md.group(0) if _md else '?'\n"
     "    F.append('\\n> **The Unique Word Test (%s, %s; read in the current seal %s) `[REAL: read from registry %s]`:** z_disc = %.2f (calibrated; one-sided p %.1e), '\n")
C = "             % (versao, data, _k, _l['z_disc_calibrado'], _l['p_disc_unilateral'], _l['z_disc_calibrado'], _l['z_delta_calibrado'],\n"
D = "             % (_vreg, _dreg, versao, _k, _l['z_disc_calibrado'], _l['p_disc_unilateral'], _l['z_disc_calibrado'], _l['z_delta_calibrado'],\n"
for a, b in ((A, B), (C, D)):
    n = s.count(a)
    assert n == 1, (a[:60], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("gerar_readme_frente.py: rótulo do Teste da Única Palavra pela versão/data do registro | %d -> %d bytes" % (len(raw), P.stat().st_size))
