from pathlib import Path
import json,hashlib,subprocess,datetime
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106');R=W/'review';actor='codex-scroll-independent-reviewer'
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(p,v):
 with p.open('xb') as f:f.write((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def call(q):
 p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(q).encode(),capture_output=True)
 d=json.loads(p.stdout)
 if p.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
ref=str(W/'SESSION_REFERENCE.json');pr=call({'operation':'project','reference':ref});t=next(t for t in pr['projection']['active'] if t['id']=='deploy')
assert t['status']=='review_pending' and t['submitted_by']!=actor
for item in t['evidence']:assert pin(item['path'])['sha256']==item['sha256']
prior=json.loads((R/'REVIEW_R1.json').read_bytes());plan=json.loads((W/'INSTALL_PLAN.json').read_bytes());installed=json.loads((W/'INSTALLED.json').read_bytes())
assert prior['install_plan_sha256']==pin(W/'INSTALL_PLAN.json')['sha256']
assert prior['plan_sha256']==pin(W/'mobile/PLAN.json')['sha256']
assert installed['status']=='PASS' and installed['restart'] is False and plan['restart'] is False
rows=plan['rows'];assert len(rows)==len(installed['files'])==10 and len({r['target'] for r in rows})==10
verified=[]
for a,b in zip(rows,installed['files']):
 assert all(a[k]==b[k] for k in ('source','target','old','new'))
 assert pin(a['target'])['sha256']==a['new']==pin(a['source'])['sha256']
 assert Path(b['backup']).parent==Path(a['target']).parent and pin(b['backup'])['sha256']==a['old']
 verified.append({'target':pin(a['target']),'source':pin(a['source']),'backup':pin(b['backup'])})
assert len(plan['preserve'])==installed['protected_count']==1797
for p in plan['preserve']:assert pin(p['path'])['sha256']==p['sha256']
for p in prior['pins']:assert pin(p['path'])['sha256']==p['sha256'],p['path']
report={'status':'PASS','reviewer':actor,'task_id':'deploy','submission_revision':pr['receipt']['revision'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'install_plan_sha256':prior['install_plan_sha256'],'plan_sha256':prior['plan_sha256'],'tests':{'installed_destinations':10,'sources_equal_installed':10,'byte_backups_equal_baseline':10,'protected_pins_unchanged':1797,'all_prior_review_pins_unchanged':True},'installed':verified,'pins':[pin(W/'INSTALLED.json'),pin(W/'INSTALL_PLAN.json'),pin(W/'DEPLOY_SUBMIT_R1.json'),pin(R/'REVIEW_R1.json'),pin(W/'TEST_FULL_CLIENT.json')],'findings':[],'scope':'Independent byte verification of installed static clients and reviewed backups/preservation. No runtime mutation, restart, browser, provider, build or publication executed. No-restart is supported by installer review and receipt; process uptime was not independently instrumented. Mobile release remains separate.'}
save(R/'DEPLOY_REVIEW_R1.json',report)
a=call({'operation':'accept','reference':ref,'task_id':'deploy','actor':{'id':actor,'kind':'agent'},'expected_revision':pr['receipt']['revision'],'projection_sha256':pr['projection_sha256'],'event_id':'scroll-deploy-independent-accept-r1','review_evidence':[pin(R/'DEPLOY_REVIEW_R1.json')],'note':'Independent installed-byte verification PASS: 10 destinations/sources/backups and 1797 protected pins; deploy only.'})
save(R/'DEPLOY_ACCEPT_R1.json',a)
post=call({'operation':'project','reference':ref});m=next(t for t in post['projection']['active'] if t['id']=='mobile')
print(json.dumps({'status':'PASS','accept_revision':a['receipt']['revision'],'mobile_ready':m['ready'],'review':str(R/'DEPLOY_REVIEW_R1.json')}))
