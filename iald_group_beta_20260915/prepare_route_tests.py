from pathlib import Path
import json
import hashlib
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
tests = WORK / 'tests'
tests.mkdir(exist_ok=True)
rows = []
for name in ['test_gratuito_rotas.py', 'test_motor_rotas.py']:
    source = (ROOT / 'tests' / name).read_bytes()
    old = b'def prompt(self, legado, catalogo):'
    assert source.count(old) == 1
    new = source.replace(old, b'def prompt(self, legado, catalogo, public=False):')
    with (tests / name).open('xb') as handle:
        handle.write(new)
    rows.append({'path': 'tests/' + name, 'baseline': hashlib.sha256(source).hexdigest()})
with (WORK / 'test_baseline.json').open('x', encoding='utf-8') as handle:
    json.dump(rows, handle, indent=2)
