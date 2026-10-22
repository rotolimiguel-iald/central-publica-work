"""Preserve parallel model-selector work; change only the staged renderer block."""
import hashlib
import json
from pathlib import Path
from datetime import datetime

w = Path(__file__).parent
n = Path(r'C:\IALD\projetos_pyhton\IALD')
target = w / 'app/iald.js'
before = target.read_bytes()
prepared = before.decode('utf-8')
production_raw = (n / 'app/iald.js').read_bytes()
production = production_raw.decode('utf-8')
marker = '// ── SANEAMENTO (início) ──'
new_renderer = prepared[prepared.index('function protectMath('):prepared.index(marker)]
start, end = production.index('function renderMarkdown('), production.index(marker)
after = (production[:start] + new_renderer + production[end:]).encode('utf-8')
assert 'function modelosTrocaveis()' in after.decode('utf-8')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup = target.with_name(target.name + '.bak_' + stamp)
backup.write_bytes(before)
assert backup.read_bytes() == before
temp = target.with_name(target.name + '.tmp_' + stamp)
temp.write_bytes(after)
assert temp.read_bytes() == after and target.read_bytes() == before
temp.replace(target)
baseline = json.loads((w / 'baseline.json').read_bytes())
for row in baseline:
    if row['relative'] in ('app\\iald.js', 'app\\index.html', 'app\\iald.css'):
        source = n / row['relative']
        row['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
for name in ('index.html', 'iald.css'):
    source, dest = n / 'app' / name, w / 'app' / name
    old = dest.read_bytes()
    dest.with_name(dest.name + '.bak_' + stamp).write_bytes(old)
    tmp = dest.with_name(dest.name + '.tmp_' + stamp)
    new = source.read_bytes()
    tmp.write_bytes(new)
    assert tmp.read_bytes() == new
    tmp.replace(dest)
receipt = w / 'baseline_reconciled.json'
assert not receipt.exists()
receipt.write_bytes(json.dumps(baseline, indent=2).encode('utf-8'))
print('STAGE_ONLY_RECONCILED; PARALLEL_MODEL_SELECTOR_PRESERVED; PRODUCTION_UNCHANGED')
