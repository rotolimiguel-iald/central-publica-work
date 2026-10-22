"""Claim only this mission's reviewed deployment stage."""
import json
from task import act, check, new
result=act('claim',task_id='deploy',lease_seconds=43200,
           event_id='media-capacity-deploy-claim-r1')
new('DEPLOY_CLAIM_R1.json',result)
ready=check('deploy')
assert ready['ready'] is True
new('DEPLOY_PREFLIGHT_R1.json',dict(ok=True,result=ready))
print(json.dumps(dict(ready=True,receipt=ready['receipt']),ensure_ascii=False))
