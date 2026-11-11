from pathlib import Path
import json,hashlib,subprocess
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106');R=W/'review';reviewer='codex-scroll-independent-reviewer'
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(p,value):
 with p.open('xb') as f:f.write((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())
def call(q):
 p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(q).encode(),capture_output=True)
 d=json.loads(p.stdout)
 if p.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
ref=str(W/'SESSION_REFERENCE.json');pr=call({'operation':'project','reference':ref});task=next(t for t in pr['projection']['active'] if t['id']=='fix')
assert task['status']=='review_pending' and task['submitted_by']!=reviewer
for p in task['evidence']:assert pin(p['path'])['sha256']==p['sha256']
files=['baseline/iald.js','baseline/owner_office.js','stage/iald.js','stage/owner_office.js','prepare_fix.py','test_scroll.mjs','TEST_SCROLL.json','test_full_client.mjs','TEST_FULL_CLIENT.json','mobile/PLAN.json','mobile/prepare_mobile.py','mobile/build_android42.py','mobile/release_controls.py','mobile/android42.init.gradle','mobile/build_log.py','INSTALL_PLAN.json','install_static.py','review/reproduce_public.mjs','review/REPRODUCED_PUBLIC.json','review/private_regression.mjs','review/PRIVATE_REGRESSION.json','review/public_auth.mjs','review/PUBLIC_AUTH_REGRESSION.json','review/review_static.py','review/STATIC_AND_INSTALLER.json']
for f in ['REPRODUCED_PUBLIC.json','PRIVATE_REGRESSION.json','PUBLIC_AUTH_REGRESSION.json','STATIC_AND_INSTALLER.json']:assert json.loads((R/f).read_bytes())['status']=='PASS'
r={'status':'PASS','reviewer':reviewer,'unit':'F9.APP_SCROLL_20261106','task_id':'fix','submission_revision':pr['receipt']['revision'],'plan_sha256':pin(W/'mobile/PLAN.json')['sha256'],'install_plan_sha256':pin(W/'INSTALL_PLAN.json')['sha256'],'pins':[pin(W/f) for f in files],
 'tests':{'public_reproduced':11,'real_private_mount_added':9,'public_auth_added':4,'synthetic_installer_cases':5,'static_plan_checks':32,'full_client_parent_receipt':'PASS; source and receipt reviewed, not independently rerun','protected_pins_verified':1797},
 'findings':[],
 'reviewed_behaviors':['Small upward intent pauses following before subsequent content','Touch/scroll, touchcancel, keyboard and explicit end button','Stale RAF guarded by view/render/gesture revisions','Same-account identity recovery preserves DOM and reading position','New-account filter retained; delayed success from old token/epoch rejected','Real mountOwnerMainChat uses shared scroll callback and preserves selection','Private stale poll/history and auth loss cannot resurrect cleared content','Mobile eight rows, exact two asset copies across three surfaces, version-only iOS47/Android42 changes','Installer ten destinations, source/destination hashes, byte backups, temporary verification, no restart, rollback on injected failures','Build reviewed statically: no execution, offline Gradle, isolated output, no-repeat attempt, signed APK/AAB and certificate/resource audits'],
 'limits':['Chromium DOM and synthetic touch/API fixtures, no physical iPhone/WebKit inspection','No real conversation, case, credentials, provider request or authenticated browser','No build, runtime installation, restart or publication executed','Static installer uses assertions; execute Python without -O/PYTHONOPTIMIZE, as reviewed','No process-wide lock: parent must maintain exclusive release window; multi-file replacement is not globally atomic','Fix acceptance is distinct from deployment/mobile completion']}
save(R/'REVIEW_R1.json',r)
# Current projection and all submitted pins verified immediately above; actual distinct reviewer accepts fix only.
a=call({'operation':'accept','reference':ref,'task_id':'fix','actor':{'id':reviewer,'kind':'agent'},'expected_revision':pr['receipt']['revision'],'projection_sha256':pr['projection_sha256'],'event_id':'scroll-fix-independent-accept-r1','review_evidence':[pin(R/'REVIEW_R1.json'),pin(R/'PRIVATE_REGRESSION.json'),pin(R/'REPRODUCED_PUBLIC.json'),pin(R/'PUBLIC_AUTH_REGRESSION.json')],'note':'Independent review PASS; 24 browser/identity cases and 5 synthetic installer cases. Fix only; deployment/mobile remain separate.'})
save(R/'FIX_ACCEPT_R1.json',a)
print(json.dumps({'status':'PASS','reviewer':reviewer,'review':str(R/'REVIEW_R1.json'),'accept_revision':a['receipt']['revision'],'plan_sha256':r['plan_sha256'],'install_plan_sha256':r['install_plan_sha256']}))
