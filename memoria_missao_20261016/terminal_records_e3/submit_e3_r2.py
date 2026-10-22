"""Submit installed E3; acceptance belongs to the independent reviewer."""
from support_e3 import *

update_agent('e3-installed-review-start','memory-e3-installed-reviewer','running')
p=preflight('E3_SUBMIT_PREFLIGHT')
t=next(t for t in p['projection']['active'] if t['id']==TASK)
names=['mission_candidate_r2.py','TEST_RESULTS_E3_R2.json','REVIEW_E3_R2.json',
       'SOURCE_BASELINE_E3_R2.json','DEPLOYMENT_E3.json','LIVE_VERIFICATION_E3.json',
       'PROTOCOL_ADDITION_E3_R2.txt','INSTRUCTIONS_ADDITION_E3.txt',
       'TRACKER_TEST_RESULTS_E3_R2.json']
evidence=[pin(BASE/n) for n in names]+[pin(OUT/'mission_resume_20261016/track_build_r45.py')]
result=call('mission_cli.py',dict(args(p),operation='submit',task_id=TASK,
    lease_id=t['lease']['id'],event_id='memory-e3-installed-submitted',evidence=evidence,
    note='Installed after independent R2 review; exact code/doc pins and real MCP verified. Await distinct installed acceptance.'),
    'SUBMIT_E3_RECEIPT')
print(json.dumps({'ok':True,'receipt':result.get('receipt')}))
