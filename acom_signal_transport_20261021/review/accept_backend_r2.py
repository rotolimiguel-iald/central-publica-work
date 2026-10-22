from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parent.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(W))
import task
ACTOR='codex-readability-reviewer'
receipt=W/'review/BACKEND_ACCEPTED_R2.json'
if receipt.exists():raise RuntimeError('Existing acceptance receipt: inspect instead of duplicating')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=W/'review/BACKEND_REVIEW_R2.json';review=json.loads(p.read_bytes())
assert review['status']=='PASS' and review['reviewer']==ACTOR and review['task_id']=='backend_integration'
for e in [review['manifest'],review['delivery'],*review['files'],*review['evidence']]:assert sha(Path(e['path']))==e['sha256']
stage=W/'integration/backend_R2'
for e in json.loads((stage/'FROZEN_MANIFEST.json').read_bytes())['files']:assert sha(stage/e['path'])==e['sha256']
before=task.project();current=next(t for t in before['projection']['active'] if t['id']=='backend_integration')
assert current['status']=='review_pending' and current['submitted_by']!=ACTOR
for e in current['evidence']:assert sha(Path(e['path']))==e['sha256']
result=task.act('accept',actor=ACTOR,task_id='backend_integration',event_id='signal-independent-backend-integration-accept-r2',review_evidence=[{'path':str(p),'sha256':sha(p)}])
out={'status':'ACCEPT_RECORDED','actor':ACTOR,'task_id':'backend_integration','scope':'Backend staging R2 only; no client/engineering/deployment acceptance.','result':result,'review_evidence':{'path':str(p),'sha256':sha(p)}}
with receipt.open('xb') as f:f.write((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode())
after=task.project()
print(json.dumps({'receipt_path':str(receipt),'receipt_sha256':sha(receipt),'current_receipt':after['receipt'],'active_tasks':[{k:t.get(k) for k in ['id','status','reviewed_by','lease']} for t in after['projection']['active']]},ensure_ascii=False))
