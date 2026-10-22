"""Assemble a new immutable installation plan from accepted deliveries."""
import json
from pathlib import Path
from mission_io import WORK, pin, save, check

check('D')
out=WORK/'deployment_r2'
out.mkdir(exist_ok=False)
for name in ('transaction.py','controlled.py','maintenance.py','legacy_app_checks.py',
             'queue_lock.py','test_transaction.py','test_controlled.py'):
    (out/name).write_bytes((WORK/'deployment'/name).read_bytes())

def read(p): return json.loads((WORK/p).read_bytes())
files={}
def add(source,target,sha,baseline,**extra):
    assert pin(source)['sha256']==sha
    dest=Path(target)
    assert (pin(dest)['sha256'] if dest.exists() else None)==baseline, str(dest)
    files[str(dest)]={'source':str(source),'destination':str(dest),'sha256':sha,
                      'baseline':baseline,**extra}
core=Path(r'C:\IALD\MEMORIA_IALD')
baselines={r['path']:r['sha256'] for r in read('CORE_BASELINE.json')}
for row in read('CORE_C2_DELIVERY_R1.json')['files']:
    s=Path(row['path']); dest=core/'lib/iald_memory'/s.name
    if s.name in {'activity.py','mission.py','store.py'}:
        add(s,dest,row['sha256'],baselines.get(str(dest)))
for row in read('APP_DELIVERY_R1.json')['files']:
    add(row['source']['path'],row['target'],row['source']['sha256'],row['baseline_sha256'])
for row in read('tests_jev/J_DELIVERY_R1.json')['files']:
    add(row['source'],row['destination'],row['sha256'],row['baseline'])
app=Path(r'C:\IALD\projetos_pyhton\IALD')
baselines={r['path']:r['sha256'] for r in read('NATIVE_BASELINE_R1.json')['sources']}
for row in read('NATIVE_DELIVERY_R1.json')['implementation']:
    s=Path(row['path']); dest=app/s.name
    add(s,dest,row['sha256'],baselines.get(str(dest)))
for f in ('tests_queue/QUEUE_INSTALL_PLAN_R2.json','tests_queue/Q2_INSTALL_PLAN_R1.json'):
    for row in read(f)['files']:
        add(row['source']['path'],row['destination'],row['source']['sha256'],row['baseline']['sha256'])
for row in read('tests_app/MOBILE_EXACT_RESOURCE_PLAN_R1.json')['files']:
    add(**{'source':row['source'],'target':row['destination'],'sha':row['sha256'],
           'baseline':row['baseline'],'backup_directory':str(WORK/'mobile_backups')})
assert len(files)==31
save(out/'INSTALL_PLAN_R1.json',{'schema':'organism-install-plan/v2','author':'codex-gerente-tgl',
    'reference':str(WORK/'SESSION_REFERENCE.json'),'files':list(files.values()),
    'final_integration':pin(WORK/'validation_final/V_ROOT_REVIEW_R1.json'),
    'scope':'Only reviewed implementation files and three shared client resources. No state/schema/science/account changes or provider dispatch.'})
print(json.dumps({'plan':pin(out/'INSTALL_PLAN_R1.json'),'files':len(files)}))
