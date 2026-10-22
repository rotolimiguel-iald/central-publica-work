"""Root review of the final integrated run; no redundant execution or deployment."""
import json
from datetime import datetime, timezone
from pathlib import Path
from mission_io import WORK, pin, project, save

root=WORK/'validation_final'; report=root/'V_ROOT_REVIEW_R1.json'
if report.exists(): raise SystemExit('Immutable review exists')
state,receipt=project()
task=next(t for t in state['projection']['active'] if t['id']=='V')
assert task['status']=='review_pending' and task['submitted_by']!='codex-gerente-tgl'
d=json.loads((root/'V_DELIVERY_R1.json').read_bytes())
assert d['verification']=='PASS_LOCAL_INTEGRATION' and d['total_tests']==170
checked=[]
def verify(p):
    a=pin(p['path']); assert a['sha256']==p['sha256'],p['path']; checked.append(a)
for p in d['evidence']: verify(p)
manifest=json.loads((root/'ASSEMBLY_PROVENANCE_R1.json').read_bytes())
for row in manifest['files']:
    verify(row['source']);verify(row['copy'])
preserved=json.loads((root/'PRESERVATION_R1.json').read_bytes())
assert preserved['status']=='PASS'
for p in preserved['production_baselines']:verify(p)
processes=json.loads((root/'PROCESS_CORE_PROVENANCE_R1.json').read_bytes())
assert processes['status']=='PASS'
for row in processes['processes']:verify(row['receipt'])
tests=[]
for suite,folder in [('core','results'),('native','results_r2'),('queue','results'),('app','results'),('jev','results')]:
    r=json.loads((root/folder/(suite+'_result.json')).read_bytes())
    assert r['status']=='PASS' and r['failures']==r['errors']==0
    tests.extend(r['test_ids'])
assert len(tests)==170 and len(set(tests))==170
coverage=json.loads((root/'COVERAGE_MATRIX_R1.json').read_bytes())
for row in coverage['rows']:
    assert row['tests'] and set(row['tests']).issubset(tests)
mcp=json.loads((root/'tests_queue/MCP_STDIO_RESULT_V3.json').read_bytes())
assert mcp['verdict']=='PASS' and mcp['exit_code']==0
save(report,{'status':'PASS','author':'codex-gerente-tgl','builder':d['actor'],
    'time_utc':datetime.now(timezone.utc).isoformat(),'requirement':'V','tests':d['tests'],
    'mcp_checks':d['mcp_checks'],'verified_pins':checked,'delivery':pin(root/'V_DELIVERY_R1.json'),
    'reviewed_snapshot':pin(receipt),'review_scope':[
        'All five consumers loaded the same frozen core C2; accepted component sources match the integrated copies.',
        'The final native hooks run against final A, not the earlier native snapshot; final A includes the J overlay.',
        'All 170 unique test identities cover steering, stale results, partition, concurrent single dispatch, restart, custody and explicit review.',
        'Fixture repairs are limited to expected pin/path, missing baseline and Windows stdlib socketpair access. Earlier failures remain preserved.',
        'MCP new process passed seven checks. This does not claim existing MCP processes were reloaded.',
        'Authenticated live browser and mobile distribution remain D; no live provider call or production modification is asserted here.'
    ]})
print(json.dumps({'review':pin(report),'tests':len(tests),'mcp_checks':d['mcp_checks']}))
