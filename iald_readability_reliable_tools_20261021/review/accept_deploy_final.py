from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(W));import task
report=W/'review/FINAL_REVIEW.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=json.loads(report.read_bytes());assert d['status']=='PASS' and d['reviewer']=='codex-readability-reviewer'
assert all(sha(e['path'])==e['sha256'] for e in d['evidence'])
p=task.project();deploy=next(t for t in p['projection']['active'] if t['id']=='deploy')
assert deploy['status']=='review_pending' and deploy['submitted_by']=='codex-app-01a094df'
result=task.act('accept',actor='codex-readability-reviewer',task_id='deploy',event_id='readability-independent-deploy-accept-final-r1',review_evidence=[{'path':str(report),'sha256':sha(report)}])
out=W/'review/DEPLOY_ACCEPTED.json';raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8')
assert not out.exists()
tmp=out.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps({'receipt':result.get('receipt'),'task':result.get('task'),'path':str(out)},ensure_ascii=False))
