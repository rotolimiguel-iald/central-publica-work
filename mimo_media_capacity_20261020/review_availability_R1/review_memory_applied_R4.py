import hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'memory_stage/FINAL_R4'
sys.path.insert(0,str(W));import task
current=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
plan=json.loads((H/'PLAN.json').read_bytes());receipt=json.loads((H/'APPLIED.json').read_bytes());intent=json.loads((H/'APPLY_INTENT.json').read_bytes())
assert receipt['status']=='APPLIED_8_ADDITIVE_SURFACES' and receipt['plan_sha256']==intent['plan_sha256']==sha(H/'PLAN.json')
review=json.loads(Path(intent['review']).read_bytes());go=json.loads(Path(intent['go']).read_bytes())
assert review['status']=='PASS' and review['scope']=='MEMORY_8_SURFACES' and review['actor']=='codex-mimo-capacity-reviewer'
assert go['go'] is True and go['actor']=='codex-app-01a094df' and go['review_sha256']==sha(intent['review']) and go['plan_sha256']==sha(H/'PLAN.json') and go['candidate_sha256']==sha(H/'audit_apply_parent.py')
assert intent['preflight']['context_id']==current['receipt']['context_id'] and intent['preflight']['revision']==9
applied={r['path']:r for r in receipt['applied']};assert len(applied)==len(plan['surfaces'])==8
checks=[]
for row in plan['surfaces']:
    rec=applied[row['path']];target=Path(row['path']);backup=Path(rec['backup']);append=Path(row['append']['path'])
    assert backup.parent==target.parent and backup.name.startswith(target.name+'.bak_')
    before=backup.read_bytes();after=target.read_bytes();suffix=append.read_bytes()
    assert sha(backup)==row['before_sha256']==rec['before_sha256'] and sha(target)==row['expected_after_sha256']==rec['after_sha256']
    assert sha(append)==row['append']['sha256'] and after==before+suffix
    assert len(after)==row['expected_after_bytes']==rec['bytes'] and len(before)==row['before_bytes']
    assert suffix.count(plan['marker'].encode())==2
    assert b'DRAFT_NEGATIVES_PRESERVED_R3_FINAL_ENGINEERING' not in suffix
    checks.append(dict(path=str(target),after_sha256=sha(target),backup=pin(backup),exact_append=True))
sources=plan['sources']['sources'];assert len(sources)==59
for e in sources:
    assert sha(e['path'])==e['sha256']
    if 'bytes' in e:assert Path(e['path']).stat().st_size==e['bytes']
    if Path(e['path']).name in ('FINAL_RUNTIME_PINS_R8.json','SCIENCE_BASELINE.json'):
        for r in json.loads(Path(e['path']).read_bytes())['files']:assert sha(r['path'])==r['sha256']
index=plan['index_policy'];assert sha(index['path'])==index['sha256']
assert json.loads((W/'extra_test_pending_unit.json').read_bytes())[0]['status']=='AGUARDA_OPERADOR'
assert not (W/'memory_stage/DRAFT_R3_FINAL_ENGINEERING/APPLIED.json').exists()
out=W/'REVIEW_MEMORY_APPLIED_R4.json';report=dict(status='PASS_APPLIED_8_SURFACES_WITH_DOCUMENTED_LIMITS',actor='codex-mimo-capacity-reviewer',reference=str(W/'SESSION_REFERENCE.json'),reviewed_revision=current['receipt']['revision'],final_delivery='NOT_ACCEPTED_AWAIT_REAL_DELIVERY_AND_DEPLOY_SUBMISSION',plan=pin(H/'PLAN.json'),applied=pin(H/'APPLIED.json'),intent=pin(H/'APPLY_INTENT.json'),review=pin(intent['review']),go=pin(intent['go']),surfaces=checks,source_pins_verified=59,runtime_verified=19,science_verified=5,index_unchanged=True,R3_not_applied=True,findings=[],limits=['All eight current files equal immediate byte backup plus the reviewed R4 append exactly.','No original/backup altered by reviewer; no provider request, new test or task acceptance.','Audio perception negative, video uncertain and estimate-not-invoice remain recorded; extra test remains AGUARDA_OPERADOR without inferred authorization.','Final parent engineering delivery/submission remains the next acceptance boundary.'])
raw=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.json.tmp');assert not out.exists()
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps(dict(status=report['status'],revision=current['receipt']['revision'],surfaces=8,source_pins=59,report=pin(out))))
