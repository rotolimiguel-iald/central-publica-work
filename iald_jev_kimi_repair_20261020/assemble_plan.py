from pathlib import Path
import ast,json,hashlib
import task
W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
task.project();task.check('repair')
admission=json.loads((W/'admission_R3/INSTALL_PLAN.json').read_bytes())
files=[{'source':r['install_from']['path'],'destination':r['destination'],'sha256':r['install_sha256'],'baseline':r['expected_destination_sha256']} for r in admission['files']]
kimi_plan=W/'stage_kimi_R3/install_plan_R3.json'
files+=json.loads(kimi_plan.read_bytes())['files']
files.append(json.loads((W/'jobs_patch_plan.json').read_bytes()))
assert len(files)==10 and len({r['destination'] for r in files})==10
for item in files:
 source=Path(item['source']);dest=Path(item['destination'])
 assert sha(source)==item['sha256']
 assert (sha(dest) if dest.exists() else None)==item['baseline']
 assert source.resolve().is_relative_to(W)
 if source.suffix=='.py':ast.parse(source.read_bytes())
plan={'schema':'iald.transaction.plan.v1','purpose':'App repair and Kimi JEV v2 integration; no client/scientific/account changes','files':files}
task.new('install_plan.json',plan)
validation=W/'validation';validation.mkdir(exist_ok=True)
evidence=['admission_R3/DELIVERY_R3.json','stage_kimi_R3/TEST_RESULTS_R3.json','jobs_tests.json']
for f in evidence:
 value=json.loads((W/f).read_bytes())
 assert value.get('status') not in ('FAIL','FAILED')
checks={'passed':True,'plan_sha256':sha(W/'install_plan.json'),'files_verified':len(files),'client_changes':False,'evidence':[{'path':str(W/f),'sha256':sha(W/f)} for f in evidence]}
with (validation/'final_checks.json').open('x',encoding='utf-8') as out:json.dump(checks,out,ensure_ascii=False,indent=2)
project=task.project();lease=next(t['lease']['id'] for t in project['projection']['active'] if t['id']=='repair')
pins=[{'path':str(W/f),'sha256':sha(W/f)} for f in ['install_plan.json','validation/final_checks.json']+evidence]
task.new('repair_submission.json',task.act('submit',task_id='repair',lease_id=lease,evidence=pins,event_id='jev-kimi-repair-submit'))
print(json.dumps({'status':'READY_FOR_REVIEW','files':len(files),'plan_sha256':checks['plan_sha256']}))
