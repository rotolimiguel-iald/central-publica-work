"""Read installed bytes and controlled restart receipts; no remote model calls."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
plan=json.loads((W/'install_plan.json').read_bytes())
rows=[]
for item in plan['files']:
    actual=digest(item['destination'])
    assert actual==item['sha256'],item['destination']
    rows.append(dict(path=item['destination'],sha256=actual,match=True))
science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
for item in science['files']:
    assert digest(item['path'])==item['sha256']
restart=json.loads((W/'restart.json').read_bytes())
assert restart['status']=='PASS' and restart['http_status']==200
result=dict(status='PASS',plan_sha256=digest(W/'install_plan.json'),files=rows,
            science_preserved=True,science_release=science.get('release'),
            restart=restart,model_calls=0,physical_installation_verified=False)
with (W/'INSTALLED_VERIFICATION.json').open('xb') as f:
    f.write(json.dumps(result,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(status='PASS',files=len(rows),science_preserved=True)))
