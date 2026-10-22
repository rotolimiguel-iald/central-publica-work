from pathlib import Path
import hashlib
import json
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
for path in (WORK/'stage').rglob('iald.css'):
    data = path.read_bytes().replace(b'var(--texto-2)',b'var(--txt-suave)')
    temp = path.with_suffix('.css.tmp')
    with temp.open('xb') as f: f.write(data)
    temp.replace(path)
baseline = json.loads((WORK/'baseline.json').read_text())
name = 'tests/test_seguranca_rotas.py'
before = (ROOT/name).read_bytes()
old = b"connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
new = b"connect-src 'self'; frame-ancestors http://localhost:8900; base-uri 'none'; form-action 'self'"
assert before.count(old) == 1
target = WORK/'stage'/name
target.parent.mkdir(parents=True,exist_ok=True)
with target.open('xb') as f:
    f.write(before.replace(old,new))
baseline[name] = hashlib.sha256(before).hexdigest()
for name in ['test_two_models.py','quota_values.json']:
    target = WORK/'stage/tests'/name
    assert not (ROOT/'tests'/name).exists()
    with target.open('xb') as f: f.write((WORK/name).read_bytes())
    baseline['tests/'+name] = None
with (WORK/'deployment_baseline.json').open('x') as f: json.dump(baseline,f,indent=2)
print('CSS uses existing theme token; stale CSP test updated to exactly localhost:8900.')
