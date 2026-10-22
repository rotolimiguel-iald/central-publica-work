"""One authorized independent M3 acceptance, fresh CAS and durable receipts."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
B=Path(__file__).resolve().parent;REF=B.parent/'FECHO_MISSION_REFERENCE.json'
ACTOR={'id':'codex-fock-r6-review','kind':'agent'}
def pin(p):return {'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,v):
 raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode();tmp=p.with_suffix('.tmp')
 with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==raw;os.rename(tmp,p)
def call(payload):
 proc=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(payload),capture_output=True,text=True,encoding='utf-8',timeout=60)
 result=json.loads(proc.stdout) if proc.stdout.strip() else None
 return {'request':payload,'exit_code':proc.returncode,'result':result,'stderr':proc.stderr}
assert not (B/'ACCEPT_E3_REQUEST.json').exists(),'Prior attempt exists: recover its outcome; never blind-repeat.'
r=call({'operation':'project','reference':str(REF),'max_chars':200000});new(B/'ACCEPT_E3_PREFLIGHT_PROJECT.json',r)
assert r['exit_code']==0 and r['result']['ok'];p=r['result']['result']
task=next(t for t in p['projection']['active'] if t['id']=='M3_TERMINAL_RECORDS')
assert task['status']=='review_pending' and task['submitted_by']!=ACTOR['id'] and not p['projection']['hold']
review=B/'REVIEW_INSTALLED_E3.json';report=json.loads(review.read_bytes())
assert report['verdict']=='PASS_WITH_SCOPE' and report['reviewer']['id']==ACTOR['id'] and report['reference']==pin(REF)
for row in report['installed_files']:
 assert pin(Path(row['target']['path']))==row['target']
 assert pin(Path(row['backup']['path']))==row['backup']
for e in task['evidence']:assert pin(Path(e['path']))==e
request={'operation':'accept','reference':str(REF),'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'memory-e3-independent-accept-r1','task_id':'M3_TERMINAL_RECORDS','review_evidence':[pin(review)]}
new(B/'ACCEPT_E3_REQUEST.json',request)
response=call(request);new(B/'ACCEPT_E3_RECEIPT.json',response)
assert response['exit_code']==0 and response['result']['ok'],response
accepted=response['result']['result'];assert accepted['task']['status']=='satisfied' and accepted['task']['reviewed_by']==ACTOR['id']
final=call({'operation':'project','reference':str(REF),'max_chars':200000});new(B/'ACCEPT_E3_FINAL_PROJECT.json',final)
assert final['exit_code']==0 and final['result']['ok']
f=final['result']['result'];settled=next(t for t in f['projection']['settled'] if t['id']=='M3_TERMINAL_RECORDS')
assert settled['status']=='satisfied' and settled['reviewed_by']==ACTOR['id']
old={t['id']:t for t in p['projection']['active']+p['projection']['settled'] if t['id']!='M3_TERMINAL_RECORDS'}
current={t['id']:t for t in f['projection']['active']+f['projection']['settled'] if t['id']!='M3_TERMINAL_RECORDS'}
assert old==current,'Other requirement changed: inspect concurrent event, do not attribute it to acceptance.'
print(json.dumps({'accepted':True,'actor':ACTOR['id'],'revision':accepted['receipt']['revision'],'final_revision':f['receipt']['revision'],'review':pin(review),'acceptance':pin(B/'ACCEPT_E3_RECEIPT.json'),'other_requirements_unchanged':True,'tetelestai':f['projection']['tetelestai']}))
