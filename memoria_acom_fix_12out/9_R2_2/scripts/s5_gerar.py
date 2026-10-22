# -*- coding: utf-8 -*-
"""R2.2: gera scripts/s5_ensaio_r2_2.py a partir do ensaio do revisor R2.1 (10_REVISAO_R2_1/scripts/s5_ensaio_rev.py,
que é o ensaio do construtor R2.1 + os cenários novos do revisor), trocando SÓ as entradas e saídas:
  ferramentas, candidato e manifesto  -> os da R2.2 (9_R2_2; web server REDIGIDO na cópia do ensaio, como antes)
  cópia da suíte (guarda, store v1, superfícies) -> 9_R2_2/copia
  saídas, guarda (ACOM_AUDIT_ROOT) e ensaio -> 9_R2_2
e acrescenta `main_r22`, que roda TODOS os cenários (K1a, K1b2, K1c, K1d, K2, K3, K4, K5, K6, P8 e K2b, K2c, K2d, K3b,
K3r, K4b, K4c, K6b, K6c, P8b, CFG) e um resumo por cenário com o que a R2.2 promete. Nada fora de 9_R2_2 é escrito."""
import hashlib
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
SRC = ME.parent / '10_REVISAO_R2_1' / 'scripts' / 's5_ensaio_rev.py'
s = SRC.read_text(encoding='utf-8')
subs = [
    ("R21 = Path(__file__).resolve().parents[1]\nSRC21 = R21.parent / '9_R2_1'\n",
     "R21 = Path(__file__).resolve().parents[1]\nSRC21 = R21                      # R2.2: ferramentas, candidato e manifesto da R2.2\n"),
    ("SRC21 / 'candidato_r2_1'", "SRC21 / 'candidato_r2_2'"),
    ("SRC21 / 'CANDIDATO_MANIFESTO_R2_1.json'", "SRC21 / 'CANDIDATO_MANIFESTO_R2_2.json'"),
    ("R21 / 'suite_r21' / 'copia'", "R21 / 'copia'"),
    ("MAN = ENS / 'CANDIDATO_MANIFESTO_R2_1_redigido.json'", "MAN = ENS / 'CANDIDATO_MANIFESTO_R2_2_redigido.json'"),
    ("nome = 's5_ensaio_r2_1%s.json'", "nome = 's5_ensaio_r2_2_base%s.json'"),
    ("nome = 's5_ensaio_rev%s.json'", "nome = 's5_ensaio_r2_2_rev%s.json'"),
]
for a, b in subs:
    assert a in s, a
    s = s.replace(a, b)
assert "'9_R2_1'" not in s and 'suite_r21' not in s
main_at = s.rindex("\nif __name__ == '__main__':")
s = s[:main_at] + (ME / 'scripts' / 's5_r22_main.py').read_text(encoding='utf-8') + \
    "\n\nif __name__ == '__main__':\n    main_r22(sys.argv[1:])\n"
out = ME / 'scripts' / 's5_ensaio_r2_2.py'
out.write_text(s, encoding='utf-8')
print(out.name, hashlib.sha256(out.read_bytes()).hexdigest()[:16], 'fonte', hashlib.sha256(SRC.read_bytes()).hexdigest()[:16])
