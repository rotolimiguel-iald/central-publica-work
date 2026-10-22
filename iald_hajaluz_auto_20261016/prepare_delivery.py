"""Prepare hash-pinned four-file deployment using previously audited maintenance."""
from pathlib import Path
import ast,hashlib,json
W=Path(__file__).resolve().parent; R=Path(r'C:\IALD\projetos_pyhton\IALD'); P=W.parent/'iald_app_stack_20261014'
digest=lambda b:hashlib.sha256(b).hexdigest()
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    raw=(P/name).read_bytes(); p=W/name
    if not p.exists():
        with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
rows=[]
for p in sorted((W/'staging').glob('*.py')):
    raw=p.read_bytes();ast.parse(raw)
    base=W/'baseline'/p.name;dest=R/p.name
    previous=base.read_bytes() if base.exists() else None
    assert (dest.read_bytes() if dest.exists() else None)==previous, 'Concurrent change '+p.name
    rows.append({'source':str(p),'destination':str(dest),'sha256':digest(raw),'baseline':digest(previous) if previous else None})
plan={'unit':'F9.APP_HAJALUZ_AUTO_20261016','files':rows,'scientific_sources_unchanged':True,'client_files_changed':False}
blob=json.dumps(plan,ensure_ascii=False,indent=2).encode();out=W/'install_plan.json'
if out.exists():assert out.read_bytes()==blob
else:
    with out.open('xb') as f:f.write(blob)
print(json.dumps({'files':len(rows),'plan_sha256':digest(blob),'transaction_sha256':digest((W/'transaction.py').read_bytes()),'maintenance_sha256':digest((W/'maintenance.py').read_bytes())}))
