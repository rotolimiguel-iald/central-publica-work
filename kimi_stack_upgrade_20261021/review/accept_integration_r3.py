from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(W))
import task
actor='codex-readability-reviewer';review=W/'review/INTEGRATION_REVIEW_R3.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify(e):assert sha(e['path'])==e['sha256'],e['path']
r=json.loads(review.read_bytes());assert r['status']=='PASS' and r['reviewer']==actor
for e in r['evidence']+r['code']:verify(e)
for tid in ('integration_prepare','integration_real'):
    out=W/'review'/(tid.upper()+'_ACCEPTED_R3.json')
    assert not out.exists(),'Existing receipt: reconcile, never repeat'
    p=task.project();t=next(t for t in p['projection']['active'] if t['id']==tid)
    assert t['status']=='review_pending' and t['submitted_by']!=actor
    for e in t['evidence']:verify(e)
    result=task.act('accept',actor=actor,task_id=tid,event_id='kimi-stack-independent-'+tid+'-accept-r3',review_evidence=[{'path':str(review),'sha256':sha(review)}])
    with out.open('xb') as f:f.write((json.dumps({'status':'ACCEPT_RECORDED','actor':actor,'task_id':tid,'result':result},ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({'task':tid,'revision':result['receipt']['revision'],'receipt':str(out),'sha256':sha(out)}),flush=True)
p=task.project()
print(json.dumps({'revision':p['receipt']['revision'],'accepted':[{k:t[k] for k in ('id','status','reviewed_by')} for t in p['projection']['settled'] if t['id'] in ('integration_prepare','integration_real')],'active':[{k:t[k] for k in ('id','status')} for t in p['projection']['active']]},ensure_ascii=False))
