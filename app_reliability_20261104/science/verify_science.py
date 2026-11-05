"""Read-only scientific deployment audit; writes only beside this script."""
from pathlib import Path
import ast
import hashlib
import json
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
W = OUT.parent.parent / 'iald_v407_20261104'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
N = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
E = Path(r'C:\IALD\Artigo\the_boundary')
pins = []
def read(p):
    p = Path(p)
    before = p.stat()
    b = p.read_bytes()
    after = p.stat()
    pin = dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b),
               mtime_ns=after.st_mtime_ns, stable_during_read=(before.st_mtime_ns == after.st_mtime_ns and before.st_size == after.st_size))
    pins.append(pin)
    return b, pin
def obj(p):
    b, _ = read(p)
    return json.loads(b)

report = dict(schema='iald.science.sidecar-status.v1', observed_at=datetime.now(timezone.utc).isoformat(),
    statute='REAL: bytes and documents observed; receipt claims retain their scope',
    mission_reference=str(OUT.parent/'SESSION_REFERENCE.json'), requirement='science', owner='codex-app-01a094df',
    project_observed=dict(ok=True,revision=5,context_id='b9db5389-0ba8-5c6d-b5db-ee46f6440a44',lease_id='aa0eaae8-ec59-44dc-a118-1bb22acba312'),
    restrictions=dict(writes='science subfolder only',acom_modified=False,claim_modified=False,source_modified=False,
                      runtime_modified=False,science_executed=False,provider_calls=0,private_data_read=False))
receipts={}
for name in ['INSTALLED_VERIFICATION.json','app/RELEASE.json','sources_verified.json','restart.json','deployment.json']:
    d=obj(W/name)
    receipts[name]={k:d[k] for k in ['status','release','identity','JEV_release','files_verified','scope','published','source_sha256','espelho_commit','um_py_sha256','http_status','restart_scope'] if k in d}
report['prior_receipts']=receipts
plan=obj(W/'install_plan.json')
checks=[]
for row in plan['files']:
    try:
        _,pin=read(row['destination'])
        checks.append(dict(path=row['destination'],expected_sha256=row['sha256'],actual_sha256=pin['sha256'],match=pin['sha256']==row['sha256'],stable=pin['stable_during_read']))
    except OSError as exc:
        checks.append(dict(path=row['destination'],match=False,error=type(exc).__name__))
report['installed_files']={'total':len(checks),'matched':sum(x['match'] for x in checks),'mismatches':[x for x in checks if not x['match']],'checks':checks}
manifest=obj(R/'iald_nucleo_fixo.json')
contract=obj(manifest['jev_control']['path'])
report['active_science']={k:manifest[k] for k in ['active_cluster','jev_control','operational_core']}
report['contract']={k:contract[k] for k in ['schema','release','source_sha256','result_sha256','proof_manifest_sha256'] if k in contract}
packages={}
for name in ['haiku55','haiku']:
    d=obj(R/'.iald_runtime'/name/'manifest.json')
    packages[name]={k:d[k] for k in ['model','deployment','coverage','prefix_sha256','budget'] if k in d}
report['provider_packages']=packages
policy,_=read(R/'iald_task_policy.py')
tree=ast.parse(policy.decode('utf-8-sig'))
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='AUTOMATIC_ORDER' for t in node.targets):
        report['configured_automatic_order']=ast.literal_eval(node.value)
jev,_=read(R/'iald_jev_control.py')
for node in ast.parse(jev.decode('utf-8-sig')).body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODEL' for t in node.targets):
        report['configured_jev_model']=ast.literal_eval(node.value)
report['loading_scope']='Current manifests, packages and static loader/provider configuration checked; prior fresh-process loader PASS reused. No current live provider selection/response or resident process memory inspected.'
seal=obj(N/'um_absoluto_selo.json')
_,program=read(N/'um.py')
seal_checks=[]
for name,expected in seal['sha256'].items():
    try:
        _,pin=read(N/name)
        seal_checks.append(dict(name=name,expected_sha256=expected,actual_sha256=pin['sha256'],match=expected==pin['sha256']))
    except OSError as exc:
        seal_checks.append(dict(name=name,match=False,error=type(exc).__name__))
_,handoff=read(N/'HANDOFF_v407_CUSTODIA.md')
report['nos']={'program_pin':program,'seal_timestamp':seal.get('timestamp'),'program_matches_seal':program['sha256']==seal['sha256']['um.py'],'program_matches_active_release':program['sha256']==manifest['active_cluster']['release_source_sha256'],'seal_artifact_checks':seal_checks,'selftest_declared':seal.get('fail_closed_selftest'),'not_sealed_this_run':seal.get('not_sealed_this_run'),'handoff':handoff,'v408_handoffs_found':[str(p) for p in N.glob('HANDOFF*v408*')]}
report['mirror']={'local_head_observed':'bf9017157406afa6b4dc05c6a9d566129e6a6ee4','remote_main_observed':'bf9017157406afa6b4dc05c6a9d566129e6a6ee4','method':'read-only git log, ls-files and ls-remote origin refs/heads/main in this audit','version':'v407','v408_tracked_files_found':False}
report['v408']={'status':'NOT_OBSERVED_AS_FINAL_SEALED_OR_PUBLISHED','running':'DECLARADO_BY_PARENT_NOT_INDEPENDENTLY_VERIFIED','incorporate_now':False,'reason':'Current canonical program/seal/handoff and public main remain v407; no v408 completion evidence located in the inspected canonical paths. Absence does not prove execution elsewhere stopped.', 'when_ready':['Receive existing Claude updater handoff; do not start a parallel update.','Verify v408 program/seal/proof/custody hashes and final-run receipt with matching version.','Verify immutable public commit and source bytes; retain source statuses and limitations.','Reuse updater deployment: verify active manifest, JEV contract, provider packages and installed pins, then current-process loading evidence.','Parent integrates evidence under current mission revision/lease; this sidecar makes no ACOM transition.']}
report['gaps']=['No independent observation of running v408 process or its work directory.','No current live model response/provider loading probe; historical loader receipt is explicitly scoped.','Inspection is a point-in-time view; another Claude updater may change state afterwards.']
# Recheck the active pointer after the full read to detect a concurrent switch.
end=obj(R/'iald_nucleo_fixo.json')
report['active_manifest_unchanged_during_audit']=(end==manifest)
report['pins']=pins
report['status']='V407_VERIFIED_V408_NOT_READY_IN_OBSERVED_CANONICAL_STATE' if all(c['match'] for c in checks) and end==manifest else 'GAPS_OR_CONCURRENT_CHANGE'
dest=OUT/'SCIENCE_STATUS.json'
if dest.exists():
    raise FileExistsError('Existing evidence preserved; do not overwrite')
tmp=OUT/'SCIENCE_STATUS.json.tmp'
payload=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
with tmp.open('xb') as f: f.write(payload)
assert tmp.stat().st_size==len(payload)
json.loads(tmp.read_bytes())
tmp.replace(dest)
print(json.dumps({'status':report['status'],'installed_total':len(checks),'installed_matched':sum(x['match'] for x in checks),'seal_checks':len(seal_checks),'seal_matched':sum(x['match'] for x in seal_checks),'active_version':manifest['active_cluster']['release'],'report':str(dest),'sha256':hashlib.sha256(payload).hexdigest()},ensure_ascii=False))
