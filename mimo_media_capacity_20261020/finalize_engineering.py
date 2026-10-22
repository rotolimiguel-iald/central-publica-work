"""Custody the engineering delivery with explicitly unresolved provider limitations."""
import json,hashlib
from task import W,new,check,act
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
check('deploy')
ap=W/'memory_stage/FINAL_R4/APPLIED.json'
a=json.loads(ap.read_bytes())
for item in a['applied']:
    from pathlib import Path
    assert sha(Path(item['path']))==item['after_sha256']
    assert sha(Path(item['backup']))==item['before_sha256']
d=json.loads((W/'ENGINEERING_DELIVERY_PRE_MEMORY.json').read_bytes())
d['memory_closeout']={'status':a['status'],'receipt':str(ap),'sha256':sha(ap),'independent_review':str(W/'REVIEW_MEMORY_APPLIED_R4.json')}
d['final_mission_acceptance']=False
d['scope_limit']='Engineering delivery; larger-media perception remains unvalidated. Extra paid test pending human answer; uncertain video is not retried.'
new('delivery.json',d)
paths=[W/'delivery.json',W/'FINAL_RUNTIME_PINS_R8.json',W/'AVAILABILITY_MATRIX.json',ap,W/'REVIEW_MEMORY_APPLIED_R4.json',W/'live_stage/TEST_COST_ROLLUP_R1.json']
p=check('deploy')
result=act('submit',task_id='deploy',lease_id='12dc20ae-0ca7-41d2-8620-411ead664b34',event_id='media-capacity-deploy-submit-rfinal',evidence=[{'path':str(x),'sha256':sha(x)} for x in paths])
new('DEPLOY_SUBMITTED_RFINAL.json',result)
print(json.dumps({'status':'SUBMITTED_ENGINEERING_WITH_PROVIDER_LIMITS','revision':result['receipt']['revision'],'memory_surfaces':len(a['applied'])}))
