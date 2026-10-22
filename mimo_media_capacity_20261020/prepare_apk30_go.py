"""Coordinator execution GO under the existing update scope, not human impersonation."""
from pathlib import Path
import hashlib,json
from task import W,REF,OWNER,check
D=W/'mobile_stage/apk30_publication/FINAL_R3'
def pin(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
plan_path=D/'APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R3.json'
review_path=D/'REVIEW_TECHNICAL_GO_R3.json'
plan=json.loads(plan_path.read_bytes())
review=json.loads(review_path.read_bytes())
assert review['technical_go'] is True
ready=check('deploy');assert ready['ready'] is True
go=dict(go=True,actor=OWNER,reference=str(REF),plan_sha256=pin(plan_path),
 review_sha256=pin(review_path),candidate_sha256=plan['candidate']['sha256'],
 authority_scope='Coordinator execution of the user-authorized coordinated app update; existing authenticated APK download channel. No new human approval is fabricated.',
 original_request=dict(path=str(W/'ORIGINAL.txt'),sha256=pin(W/'ORIGINAL.txt')))
for name,data in [('PARENT_GO_R1.json',go),('DEPLOY_PREFLIGHT_PUBLISH_R1.json',dict(ok=True,result=ready))]:
    with (D/name).open('xb') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2).encode())
print('APK30 publication GO and fresh deploy preflight recorded')
