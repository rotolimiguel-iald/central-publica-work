"""Install sourced Hamiltonian references with an immediate byte backup."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import os

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
target = ROOT / 'iald_memoria_canonica.py'
receipt = WORK / 'hamiltonian_deployment.json'
if receipt.exists():
    raise RuntimeError('Receipt already exists')
rows = json.loads((WORK / 'retry_deployment.json').read_bytes())['files']
expected = next(row['sha256'] for row in rows if Path(row['path']) == target)
before = target.read_bytes()
assert hashlib.sha256(before).hexdigest() == expected, 'Concurrent memory-module edit'
after = (WORK / target.name).read_bytes()
assert len(after) > len(before)
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def create(path, data):
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data

backup = target.with_name(target.name + '.bak_' + stamp)
create(backup, before)
temp = target.with_name(target.name + '.tmp_' + stamp)
create(temp, after)
assert target.read_bytes() == before, 'Concurrent edit before replace'
os.replace(temp, target)
assert target.read_bytes() == after
report = {'recorded_at':datetime.now().astimezone().isoformat(), 'status':'INSTALLED_RESTART_PENDING',
          'path':str(target),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest(),
          'basis':'um_grande_atrator_forma_canonica.md v22 / Three Locks / continuous_modular_zero.resistencia_beta',
          'new_formal_proof_claimed':False}
temp = receipt.with_suffix('.tmp')
create(temp, json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
os.replace(temp,receipt)
print(json.dumps(report,ensure_ascii=True))
