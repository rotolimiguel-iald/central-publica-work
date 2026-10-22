"""Bind coordinator GO to the distinct reviewed final memory append plan."""
import hashlib,json
from task import W,REF,OWNER,check
D=W/'memory_stage/FINAL_R4'
plan=json.loads((D/'PLAN.json').read_bytes())
review=D/'REVIEW_MEMORY_8_SURFACES_R4.json'
assert json.loads(review.read_bytes())['technical_go'] is True
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ready=check('deploy');assert ready['ready'] is True
go=dict(go=True,actor=OWNER,reference=str(REF),plan_sha256=sha(D/'PLAN.json'),
 review_sha256=sha(review),candidate_sha256=plan['apply_candidate']['sha256'],
 scope='Apply only eight reviewed additive operational fragments; no scientific promotion or fabricated approval of the pending extra test.')
for name,data in [('PARENT_GO_R1.json',go),('PARENT_PREFLIGHT_R1.json',dict(ok=True,result=ready))]:
    with (D/name).open('xb') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2).encode())
print('Reviewed memory GO and current deploy preflight recorded')
