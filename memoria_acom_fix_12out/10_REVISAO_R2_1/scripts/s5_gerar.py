# -*- coding: utf-8 -*-
"""Gera scripts/s5_ensaio_rev.py: o ensaio do construtor (9_R2_1/scripts/s5_ensaio_r2_1.py, que adapta o do revisor R2
8_REVISAO_R2/scripts/s5_ensaio.py; diff conferido) com as ENTRADAS lidas de 9_R2_1 e as SAIDAS em 10_REVISAO_R2_1,
mais os cenarios novos de s5_extra.py. Nada fora de 10_REVISAO_R2_1 e escrito."""
import hashlib
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
SRC = ME.parent / '9_R2_1' / 'scripts' / 's5_ensaio_r2_1.py'
s = SRC.read_text(encoding='utf-8')
subs = [
    ("R21 = Path(__file__).resolve().parents[1]\n", "R21 = Path(__file__).resolve().parents[1]\nSRC21 = R21.parent / '9_R2_1'\n"),
    ("cpb(R21 / n, TOOLS / n)", "cpb(SRC21 / n, TOOLS / n)"),
    ("assert log[n] == sha(R21 / n)[:16]", "assert log[n] == sha(SRC21 / n)[:16]"),
    ("cpb(R21 / n, TOOLS_K3 / n)", "cpb(SRC21 / n, TOOLS_K3 / n)"),
    ("k3 = (R21 / 'implantacao_lib.py')", "k3 = (SRC21 / 'implantacao_lib.py')"),
    ("R21 / 'candidato_r2_1'", "SRC21 / 'candidato_r2_1'"),
    ("R21 / 'CANDIDATO_MANIFESTO_R2_1.json'", "SRC21 / 'CANDIDATO_MANIFESTO_R2_1.json'"),
    ("R21 / 'copia'", "R21 / 'suite_r21' / 'copia'"),
]
for a, b in subs:
    assert a in s, a
    s = s.replace(a, b)
main_at = s.index("\nif __name__ == '__main__':")
s = s[:main_at] + (ME / 'scripts' / 's5_extra.py').read_text(encoding='utf-8') + "\n\nif __name__ == '__main__':\n    main_rev(sys.argv[1:])\n"
out = ME / 'scripts' / 's5_ensaio_rev.py'
out.write_text(s, encoding='utf-8')
print(out.name, hashlib.sha256(out.read_bytes()).hexdigest()[:16], 'fonte', hashlib.sha256(SRC.read_bytes()).hexdigest()[:16])
for i, line in enumerate(s.splitlines(), 1):
    if 'R21' in line and 'SRC21' not in line and "'suite_r21'" not in line:
        print(i, line.strip()[:110])
