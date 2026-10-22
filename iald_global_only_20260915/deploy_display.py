from datetime import datetime
from pathlib import Path
import hashlib
import json
import os

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
receipt = WORK / 'display_deployment.json'
assert not receipt.exists()
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
initial = []
for name, expected in json.loads((WORK / 'display_baseline.json').read_text()).items():
    path = ROOT / name
    before, after = path.read_bytes(), (WORK / 'stage' / name).read_bytes()
    assert hashlib.sha256(before).hexdigest() == expected, 'Concurrent edit: ' + name
    if name.endswith('.py'): compile(after, str(path), 'exec')
    initial.append((path, before, after))

def create(path, data):
    with path.open('xb') as f: f.write(data)
    assert path.read_bytes() == data

rows = []
for path, before, after in initial:
    assert path.read_bytes() == before, 'Concurrent edit: ' + path.name
    backup = path.with_name(path.name + '.bak_' + stamp)
    create(backup, before)
    temp = path.with_name(path.name + '.tmp_' + stamp)
    create(temp, after)
    assert path.read_bytes() == before
    os.replace(temp, path)
    assert path.read_bytes() == after
    rows.append({'path':str(path), 'backup':str(backup), 'sha256':hashlib.sha256(after).hexdigest()})
report = {'status':'INSTALLED_RESTART_PENDING', 'recorded_at':datetime.now().astimezone().isoformat(),
          'change':'Global usage display uses the same ledger as the reservation guard',
          'quotas_changed':False, 'accounts_changed':False, 'files':rows}
create(receipt, json.dumps(report, ensure_ascii=False, indent=2).encode())
print(json.dumps({'status':report['status'], 'files':len(rows)}))
