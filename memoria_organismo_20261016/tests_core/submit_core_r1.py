"""Authorized submit C only, own actor; no acceptance/installation."""
from pathlib import Path
import json
import sys

WORK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORK))
from mission_io import call, save, pin, REFERENCE

actor = {'id': 'codex-organism-core-build', 'kind': 'agent'}
delivery = WORK/'CORE_DELIVERY_R1.json'
manifest = json.loads(delivery.read_text(encoding='utf-8'))
for p in manifest['implementation'] + [manifest['tests'], manifest['api']]:
    assert pin(p['path']) == p
p, project_receipt = call('mission_cli.py', {'operation': 'project', 'reference': str(REFERENCE),
                                          'max_chars': 125000}, 'core_submit_project')
task = next(x for x in p['projection']['active'] if x['id'] == 'C')
assert task['status'] == 'working' and task['lease']['owner'] == actor['id']
common = {'reference': str(REFERENCE), 'actor': actor, 'task_id': 'C',
          'lease_id': task['lease']['id'], 'expected_revision': p['receipt']['revision'],
          'projection_sha256': p['projection_sha256']}
checked, check_receipt = call('mission_cli.py', dict(common, operation='check'), 'core_submit_check')
submitted, submit_receipt = call('mission_cli.py', dict(common, operation='submit',
    event_id='organism-core-C-submit-r1', evidence=[pin(delivery), manifest['api'], manifest['tests']]
        + manifest['implementation'], note='Candidato em staging; 52 testes privados passam. Sem autoaceite, instalação ou provedor.'),
    'core_submit')
snapshot, get_receipt = call('session_memory.py', {'operation': 'get', 'reference': str(REFERENCE)}, 'core_handle_finish_get')
handles = snapshot['p']['handles']
handle = next(h for h in handles if h['id'] == 'org-core-build')
assert handle['task_id'] == 'C' and handle['agent'] == '/root/maxwell_covariance_review'
handle.update(status='completed', no_repeat=True, result_evidence=[pin(delivery)],
              completion_scope='construction_submitted_not_accepted')
finished, handle_receipt = call('session_memory.py', {'operation': 'transition', 'reference': str(REFERENCE),
    'actor': actor, 'expected_revision': snapshot['revision'], 'event_id': 'organism-core-build-handle-completed-r1',
    'changes': {'flow': {'handles': handles}}}, 'core_handle_completed')
final, final_receipt = call('mission_cli.py', {'operation': 'project', 'reference': str(REFERENCE),
                                            'max_chars': 125000}, 'core_return_project')
row = next(t for t in final['projection']['active'] if t['id'] == 'C')
assert row['status'] == 'review_pending'
save(WORK/'CORE_SUBMITTED_R1.json', {'reference': str(REFERENCE), 'actor': actor,
    'requirement': 'C', 'status': row['status'], 'revision': final['receipt']['revision'],
    'delivery': pin(delivery), 'receipts': [pin(q) for q in [project_receipt, check_receipt,
           submit_receipt, get_receipt, handle_receipt, final_receipt]],
    'accepted': False, 'installed': False})
print(json.dumps({'revision': final['receipt']['revision'], 'status': row['status'],
                  'receipt': pin(WORK/'CORE_SUBMITTED_R1.json')}, ensure_ascii=False))
