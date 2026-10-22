from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK.joinpath('tests').mkdir(exist_ok=True)
baselines = {}
for name in ('test_gratuito_rotas.py', 'test_motor_rotas.py'):
    source = WORK.parent / 'iald_group_beta_20260915/tests' / name
    raw = source.read_bytes()
    text = raw.decode('utf-8')
    if name == 'test_gratuito_rotas.py':
        old = 'FERRAMENTAS_KERNEL | {"iald_public_read"}'
        assert text.count(old) == 2, text.count(old)
        text = text.replace(old, 'FERRAMENTAS_KERNEL | {"iald_public_read", "search_tgl", "fetch_tgl"}')
    path = WORK / 'tests' / name
    with path.open('xb') as handle:
        handle.write(text.encode('utf-8'))
    baselines[name] = hashlib.sha256((ROOT / 'tests' / name).read_bytes()).hexdigest()

with (WORK / 'test_baseline.json').open('x', encoding='utf-8') as handle:
    json.dump(baselines, handle, indent=2)
script = WORK / 'run_staged_routes.ps1'
before = script.read_bytes()
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
with script.with_name(script.name+'.bak_'+stamp).open('xb') as handle:
    handle.write(before)
after = before.replace(b'work\\iald_group_beta_20260915\\tests', b'work\\iald_core_indexed_20260915\\tests')
after = after.replace(b"'free_staged.log'", b"'free_staged_updated_expectations.log'")
tmp = script.with_name(script.name+'.tmp_'+stamp)
with tmp.open('xb') as handle:
    handle.write(after)
assert tmp.read_bytes() == after and before != after
os.replace(tmp, script)
print('Prepared test fixtures: same assertions, explicit addition of the two published corpus tools.')
