"""Install the verified availability fix; collect metadata, never credentials."""
from pathlib import Path
from datetime import datetime
import ast, hashlib, json, os, sqlite3

W = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
receipt_path = W / 'jev_router_health_fix.json'
assert not receipt_path.exists(), 'Already installed; inspect receipt instead of repeating'
prior = json.loads((W/'installed_reviewed.json').read_bytes())
target = ROOT/'iald_auto_router.py'
old = target.read_bytes()
assert hashlib.sha256(old).hexdigest() == prior['files'][target.name]['sha256']
new = (W/'stage'/target.name).read_bytes()
ast.parse(new)
dbpath = ROOT/'.iald_runtime/app_evaluation/metrics.sqlite3'
db = sqlite3.connect('file:' + str(dbpath) + '?mode=ro', uri=True)
records = [json.loads(row[0]) for row in db.execute('SELECT data FROM turns ORDER BY rowid DESC')]
db.close()
assert not [r for r in records if r.get('status') == 'started'], 'Generation still running'
latest = records[0]
assert latest['provider'] == 'mimo' and latest['status'] == 'completed'
selector = json.loads((W/'jev_rotated_key_selector.json').read_bytes())['receipt']
routing = [json.loads(p.read_bytes()) for p in (ROOT/'.iald_runtime/app_routing').glob('*.json')]
routing.sort(key=lambda r:r['utc'],reverse=True)
assert routing[0]['utc'] > selector['utc'] and routing[0]['selected'] == 'mimo'
assert latest['utc'] >= routing[0]['utc']

def create(path, raw):
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert path.read_bytes() == raw

backup = Path(str(target)+'.bak_'+stamp)
create(backup, old)
temp = Path(str(target)+'.tmp_'+stamp)
create(temp, new)
assert target.read_bytes() == old, 'Concurrent edit'
os.replace(temp,target)
assert target.read_bytes() == new
report = dict(at=datetime.now().astimezone().isoformat(),
    installed_file=str(target), backup=str(backup),
    old_sha256=hashlib.sha256(old).hexdigest(), sha256=hashlib.sha256(new).hexdigest(),
    routing=routing[0], generation=latest,
    browser_test='Author and beta formula received and visually rendered; automatic mode preserved',
    user='luiz', restart='pending', client_changed=False, scientific_memory_changed=False)
create(receipt_path,json.dumps(report,ensure_ascii=False,indent=2).encode())
print(json.dumps(report,ensure_ascii=False,indent=2))
