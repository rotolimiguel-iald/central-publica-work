"""Submit installed E2 for a real independent acceptance; no self-acceptance."""
from support_e2 import *

update_agent('e2-installed-review-start', 'memory-e2-installed-reviewer', 'running')
p = preflight('E2_SUBMIT_PREFLIGHT')
t = next(t for t in p['projection']['active'] if t['id'] == TASK)
names = ['mission_candidate.py', 'TEST_RESULTS_E2.json', 'REVIEW_E2.json',
         'DEPLOYMENT_E2.json', 'LIVE_VERIFICATION_E2.json',
         'LIVE_ATTEMPT_1_ENVIRONMENT.json', 'PROTOCOL_ADDITION_E2.txt',
         'INSTRUCTIONS_ADDITION_E2.txt']
result = call('mission_cli.py', dict(args(p), operation='submit', task_id=TASK,
    lease_id=t['lease']['id'], event_id='memory-e2-installed-submitted',
    evidence=[pin(BASE/n) for n in names],
    note='Installed after independent candidate review. Real MCP read-only verification passed. Awaiting distinct installed reviewer.'),
    'SUBMIT_E2_RECEIPT')
print(json.dumps({'ok': True, 'receipt': result.get('receipt')}))
