"""Accept only independently reviewed C; reconcile this reviewer's own handle."""
import importlib.util
import json
from pathlib import Path

W = Path(__file__).resolve().parents[1]
s = importlib.util.spec_from_file_location('core_accept_io', W / 'mission_io.py')
io = importlib.util.module_from_spec(s)
s.loader.exec_module(io)
A = {'id': 'codex-mission-memory-review', 'kind': 'agent'}
REF = W / 'SESSION_REFERENCE.json'
REVIEW = W / 'review_core/CORE_INDEPENDENT_REVIEW_R1.json'

def project(label):
    return io.call('mission_cli.py', {'operation': 'project', 'reference': str(REF),
        'actor': A, 'max_chars': 125000}, label)

def rows(value):
    return {t['id']: {k: v for k, v in t.items() if k != 'ready'}
        for t in value['projection']['active'] + value['projection']['settled']}

review = json.loads(REVIEW.read_bytes())
assert review['reviewer'] == A and review['verdict'] == 'PASS_CORE_WITH_SCOPE'
assert review['requirement'] == 'C' and review['requirement_satisfied'] is True
assert review['test_result']['tests_run'] == 64 and not review['blocking_findings']
assert review['reference'] == io.pin(REF)
for item in review['evidence'] + review['implementation'] + review['contracts']:
    assert io.pin(item['path']) == item
assert io.pin(review['independent_tests']['path']) == review['independent_tests']
fresh, before_path = project('core_accept_fresh')
before = rows(fresh)
t = before['C']
assert t['criterion'] == review['criterion'] and t['evidence'] == review['evidence']
assert t['status'] == 'review_pending' and t['submitted_by'] != A['id']
request = {
    'operation': 'accept', 'reference': str(REF), 'actor': A, 'task_id': 'C',
    'event_id': 'organism-C-independent-review-accept-r1',
    'expected_revision': fresh['receipt']['revision'],
    'projection_sha256': fresh['projection_sha256'],
    'review_evidence': [io.pin(REVIEW)],
    'note': 'Aceite técnico independente de C em staging: 64 testes reais, incluindo 12 adversariais próprios. Progresso autorizado pelo operador; integrações A/N/Q, revisão V, implantação D e memória M permanecem separadas.'
}
io.save(W / 'review_core/C_ACCEPT_REQUEST_R1.json', request)
result, accept_path = io.call('mission_cli.py', request, 'core_accept_independent')
after, after_path = project('core_accept_verify')
accepted = rows(after)
assert accepted['C']['status'] == 'satisfied'
assert accepted['C']['reviewed_by'] == A['id']
assert accepted['C']['review_evidence'] == [io.pin(REVIEW)]
assert {k:v for k,v in before.items() if k != 'C'} == {k:v for k,v in accepted.items() if k != 'C'}
assert fresh['projection']['flow'] == after['projection']['flow']
receipt = {'schema': 'organism-C-independent-accept/v1', 'actor': A,
    'reference': io.pin(REF), 'review': io.pin(REVIEW), 'before': io.pin(before_path),
    'accept': io.pin(accept_path), 'after': io.pin(after_path), 'transition': result,
    'revision_before': fresh['receipt']['revision'], 'revision_after': after['receipt']['revision'],
    'C_status': 'satisfied', 'other_requirements_unchanged': True,
    'flow_handles_unchanged_by_accept': True, 'installed': False, 'provider_calls': 0}
io.save(W / 'review_core/C_ACCEPTED_R1.json', receipt)

# The independently assigned review is completed. Only this handle is changed.
state, get_path = io.call('session_memory.py', {'operation': 'get', 'reference': str(REF),
    'actor': A}, 'core_review_handle_fresh')
handles = {h['id']: h for h in state['p']['handles']}
h = handles['org-core-review']
assert h['agent'] == '/root/mission_memory_review' and h['task_id'] == 'C'
assert h['status'] == 'running'
delta = {'id': h['id'], 'status': 'completed', 'review_evidence': io.pin(REVIEW)}
finished, finish_path = io.call('session_memory.py', {
    'operation': 'transition', 'reference': str(REF), 'actor': A,
    'expected_revision': state['revision'], 'event_id': 'organism-core-review-handle-completed-r1',
    'changes': {'flow': {'handles': [delta]}}}, 'core_review_handle_completed')
check, check_path = io.call('session_memory.py', {'operation': 'get', 'reference': str(REF),
    'actor': A}, 'core_review_handle_verify')
new_handles = {h['id']: h for h in check['p']['handles']}
assert {k:v for k,v in handles.items() if k != h['id']} == {k:v for k,v in new_handles.items() if k != h['id']}
assert new_handles[h['id']] == {**h, **delta}
assert state['q'] == check['q']
final, final_path = project('core_review_final_return')
io.save(W / 'review_core/C_REVIEW_COMPLETED_R1.json', {
    'actor': A, 'reference': io.pin(REF), 'acceptance': io.pin(W / 'review_core/C_ACCEPTED_R1.json'),
    'handle_before': io.pin(get_path), 'handle_transition': io.pin(finish_path),
    'handle_after': io.pin(check_path), 'final_project': io.pin(final_path),
    'revision': final['receipt']['revision'], 'C_status': 'satisfied',
    'handle': new_handles[h['id']], 'other_handles_unchanged': True,
    'requirements_unchanged_by_handle_transition': True,
    'next_ready': final['projection']['next_ready'], 'installed': False})
print(json.dumps({'accepted': io.pin(W / 'review_core/C_ACCEPTED_R1.json'),
    'completed': io.pin(W / 'review_core/C_REVIEW_COMPLETED_R1.json'),
    'revision': final['receipt']['revision'], 'C_status': 'satisfied',
    'next_ready': final['projection']['next_ready']}, ensure_ascii=False, indent=2))
