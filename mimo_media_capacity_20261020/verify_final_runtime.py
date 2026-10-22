"""Pin the effective release lineage without reapplying earlier plans."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
plans=[W/'install_plan.json',
 W/'client_stage/bootstrap_hotfix_R7/install_plan.json',
 W/'host_followup/capability_R2/install_plan.json',
 W/'host_followup/availability_deploy_R1/install_plan.json']
def pin(p):
    raw=Path(p).read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
files={};lineage=[]
for path in plans:
    report=json.loads((path.parent/'deployment.json').read_bytes())
    restart=json.loads((path.parent/'restart.json').read_bytes())
    assert restart['status']=='PASS'
    assert report['plan_sha256']==pin(path)['sha256']
    lineage.append(dict(plan=pin(path),deployment=pin(path.parent/'deployment.json'),
                        restart=pin(path.parent/'restart.json')))
    for item in json.loads(path.read_bytes())['files']:
        files[item['destination']]=dict(path=item['destination'],sha256=item['sha256'])
for item in files.values():assert pin(item['path'])['sha256']==item['sha256']
science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
for item in science['files']:assert pin(item['path'])['sha256']==item['sha256']
assert len(files)==19
value=dict(status='PASS_EFFECTIVE_RUNTIME_NOT_INSTALLABLE',files=list(files.values()),
           unique_files=len(files),lineage=lineage,science_preserved=True,
           science_baseline=pin(W/'SCIENCE_BASELINE.json'),live_validation_complete=False,
           client_native_versions=dict(ios='4.1(35)',android='4.1(30)'),
           physical_installation_verified=False)
with (W/'FINAL_RUNTIME_PINS.json').open('xb') as f:
    f.write(json.dumps(value,ensure_ascii=False,indent=2).encode())
print('Effective runtime:19 files verified; full scientific baseline preserved')
