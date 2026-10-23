# -*- coding: utf-8 -*-
"""Deriva snapshot_chatgpt_v396.py do da v395 por trocas CONTADAS: a base passa a ser o snapshot da v395."""
from pathlib import Path
W5 = Path(r"C:/IALD/Central de Patentes/work/custodia_v395_21out")
W6 = Path(r"C:/IALD/Central de Patentes/work/custodia_v396_22out")
s = (W5 / "snapshot_chatgpt_v395.py").read_text(encoding="utf-8")
for a, b, n in [
    ("custódia v395 (21/10/2026, sessão a7)", "custódia v396 (22/10/2026, sessão a7)", 1),
    ('assert base.name == "Chatgpt_20261019_190704_delta_de_20261007_195426", base.name',
     'assert base.name == "Chatgpt_20261021_175747_delta_de_20261019_190704", base.name', 1),
    ("v2 (custodia v395, 21/10; exclusoes iguais as de 15/09)", "v2 (custodia v396, 22/10; exclusoes iguais as de 15/09)", 1),
]:
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)
d = W6 / "snapshot_chatgpt_v396.py"
assert not d.exists()
compile(s, str(d), "exec")
d.write_text(s, encoding="utf-8")
print("ok", d.name, len(s))
