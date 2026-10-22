"""Submit the pinned local implementation to the real distinct reviewer."""
import hashlib
import json
from task import W, check, act, new

ready=check('implementation')
assert ready['ready'] is True
evidence=[]
for relative in ('install_plan.json','validation/final_checks.json',
                 'backend_stage/BACKEND_R4_HANDOFF.json',
                 'host_stage/HOST_FINAL_RECEIPT.json',
                 'client_stage/release_R6/DELIVERY_PREPARED_R6_FINAL.json'):
    path=W/relative
    evidence.append(dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
result=act('submit',task_id='implementation',lease_id=ready['lease_id'],
           event_id='media-capacity-implementation-submit-r1',evidence=evidence)
new('IMPLEMENTATION_SUBMITTED_R1.json',result)
print(json.dumps(dict(submitted=True,receipt=result.get('receipt')),ensure_ascii=False))
