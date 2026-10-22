"""Apply tested retry/authorship fix without overwriting concurrent changes."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import os

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
targets = {
    'iald_motores.py': '651a92da9f001df03a2a80672844f62009a486449879c4f7be1f52512273d77c',
    'iald_memoria_canonica.py': '6ac874428548927c5dbd45af8edb66674416b84243873e4fcb937dfc3181cc4c',
    'tests/test_provider_retry.py': None,
}
receipt = WORK / 'retry_deployment.json'
if receipt.exists():
    raise RuntimeError('Already deployed; review receipt.')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
prepared = []
for relative, expected in targets.items():
    path = ROOT / relative
    before = path.read_bytes() if path.exists() else None
    actual = hashlib.sha256(before).hexdigest() if before is not None else None
    if actual != expected:
        raise RuntimeError('Concurrent modification: ' + relative)
    prepared.append((path, before, (WORK / relative).read_bytes()))

def create(path, data):
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data

rows = []
for path, before, after in prepared:
    backup = path.with_name(path.name + '.bak_' + stamp) if before is not None else None
    if backup:
        create(backup, before)
    temp = path.with_name(path.name + '.tmp_' + stamp)
    create(temp, after)
    if (path.read_bytes() if path.exists() else None) != before:
        raise RuntimeError('Concurrent modification before replace: ' + path.name)
    os.replace(temp, path)
    assert path.read_bytes() == after
    rows.append({'path':str(path), 'backup':str(backup) if backup else None,
                 'sha256':hashlib.sha256(after).hexdigest()})
report = {'recorded_at':datetime.now().astimezone().isoformat(),
          'status':'INSTALLED_RESTART_PENDING','files':rows,
          'credentials_or_quotas_changed':False,'tests':{'retry':7,'motor_regression':218,'nucleus':3}}
temp = receipt.with_suffix('.tmp')
create(temp, json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
os.replace(temp, receipt)
print(json.dumps(report, ensure_ascii=True))
