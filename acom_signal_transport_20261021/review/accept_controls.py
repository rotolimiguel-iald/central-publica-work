from pathlib import Path
import hashlib,json,sys
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W));import task
ACTOR='codex-readability-reviewer'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
lum=W/'review/LUMINIDIC_REVIEW_R1.json';fix=W/'review/FINAL_CONTROL_R2.json';err=W/'prototype_R2/PROVENANCE_ADDENDUM.json'
l=load(lum);f=load(fix)
assert l['status']=='PASS_WITH_SCOPE' and f['status']=='PASS' and l['reviewer']==f['reviewer']==ACTOR
assert sha(W/'CONTROL_MANIFEST_R2.json')==f['manifest_sha256']
for item in load(W/'CONTROL_MANIFEST_R2.json')['files']:assert sha(item['path'])==item['sha256']
for name,item in load(W/'science/luminidic_control/RECEIPT.json')['files'].items():assert sha(W/'science/luminidic_control'/name)==item['sha256']
for item in l['source_pins']:assert sha(item['path'])==item['sha256']
for item in load(err)['preserves']:assert sha(item['path'])==item['sha256']
assert any(x['id']=='LUM-01' and x['status']=='RESOLVED_BY_ADDITIVE_ERRATUM' for x in f['findings'])
for id,refs in [('luminidic_control',[lum,err,fix]),('control_fixes_r2',[fix,err])]:
    p=task.project();targets=p['projection']['active']+p['projection']['settled'];t=next(t for t in targets if t['id']==id)
    if t['status']=='satisfied':
        assert t['reviewed_by']==ACTOR
        print(json.dumps({'task':id,'already_satisfied':True,'revision':p['receipt']['revision']}));continue
    assert t['status']=='review_pending' and t['submitted_by']!=ACTOR
    for item in t['evidence']:assert sha(item['path'])==item['sha256']
    result=task.act('accept',actor=ACTOR,task_id=id,event_id='signal-independent-'+id+'-accept-r1',review_evidence=[dict(path=str(x),sha256=sha(x)) for x in refs])
    out=W/'review'/(id.upper()+'_ACCEPTED.json');raw=json.dumps(result,ensure_ascii=False,indent=2).encode()
    assert not out.exists();tmp=out.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
    print(json.dumps({'task':id,'receipt':result['receipt'],'status':result['task']['status'],'path':str(out)},ensure_ascii=False),flush=True)
