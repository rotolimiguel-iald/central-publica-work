"""Apply the user's explicit own-account exemption; never alter global caps."""
from datetime import datetime
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
receipt = WORK / 'deployment.json'
if receipt.exists():
    raise RuntimeError('Deployment already recorded')
baseline = json.loads((WORK / 'baseline.json').read_text())
prepared = []
for name, expected in baseline.items():
    path = ROOT / name
    before, after = path.read_bytes(), (WORK / 'stage' / name).read_bytes()
    if hashlib.sha256(before).hexdigest() != expected:
        raise RuntimeError('Concurrent modification: ' + name)
    if name.endswith('.py'):
        compile(after, str(path), 'exec')
    prepared.append((path, before, after))

sys.dont_write_bytecode = True
sys.path.insert(0, str(WORK / 'stage'))
import iald_motores as mt
from dotenv import dotenv_values
env_before = (ROOT / '.env').read_bytes()
env = dotenv_values(ROOT / '.env')
global_cap = float(env['IALD_OPENAI_COTA_GLOBAL_USD_DIA'])
users_path = ROOT / 'iald_users.json'
users_before = users_path.read_bytes()
users = json.loads(users_before)
owner = users.get('luiz')
if not isinstance(owner, dict) or owner.get('admin') is not True or mt.plano_de(owner) != mt.OPERADOR:
    raise RuntimeError('Account luiz is not a verified operator administrator')
changed = copy.deepcopy(users)
changed['luiz']['somente_limite_global'] = True
assert {k:v for k,v in users.items() if k != 'luiz'} == {k:v for k,v in changed.items() if k != 'luiz'}
assert {k:v for k,v in changed['luiz'].items() if k != 'somente_limite_global'} == {k:v for k,v in owner.items() if k != 'somente_limite_global'}
users_after = json.dumps(changed, ensure_ascii=False, indent=2).encode('utf-8')
prepared.append((users_path, users_before, users_after))

def create(path, data, sensitive=False):
    if sensitive:
        # Protect the empty file before any account data reaches it.
        with path.open('xb'):
            pass
        principal = os.environ['USERNAME']
        subprocess.run(['icacls.exe', str(path), '/inheritance:r', '/grant:r',
                        principal + ':(F)', 'SYSTEM:(F)'], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with path.open('r+b') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    else:
        with path.open('xb') as handle:
            handle.write(data)
    if path.read_bytes() != data:
        raise RuntimeError('Byte verification failed: ' + path.name)

rows = []
for path, before, after in prepared:
    if path.read_bytes() != before:
        raise RuntimeError('Concurrent change before backup: ' + path.name)
    sensitive = path == users_path
    backup = path.with_name(path.name + '.bak_' + stamp)
    create(backup, before, sensitive)
    temp = path.with_name(path.name + '.tmp_' + stamp)
    create(temp, after, sensitive)
    if path.read_bytes() != before:
        raise RuntimeError('Concurrent change before replace: ' + path.name)
    os.replace(temp, path)
    assert path.read_bytes() == after
    row = {'path': str(path), 'backup': str(backup)}
    if not sensitive:
        row['sha256'] = hashlib.sha256(after).hexdigest()
    rows.append(row)

assert (ROOT / '.env').read_bytes() == env_before
assert json.loads(users_path.read_bytes()) == changed
report = {'recorded_at': datetime.now().astimezone().isoformat(),
          'status':'INSTALLED_RESTART_PENDING', 'account':'luiz',
          'somente_limite_global':True, 'global_usd_per_day':global_cap,
          'global_cap_changed':False, 'other_accounts_changed':False,
          'tests':{'global_only':8,'motor_regression':218,'budget_regression':67,'retry':7,'ui':7},
          'files':rows}
create(receipt, json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in report.items() if k != 'files'}, ensure_ascii=True))
