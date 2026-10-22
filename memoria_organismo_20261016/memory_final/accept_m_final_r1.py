"""One independently authorized M acceptance, with fresh exact-reference CAS."""
from pathlib import Path
import json
import sys
W = Path(__file__).resolve().parents[1]
F = W / 'memory_final'
sys.path.insert(0, str(W))
from mission_io import call, pin, save
A = {'kind': 'agent', 'id': 'codex-mission-memory-review'}
assert sys.argv[1:] == ['--run'], 'Explicit --run required'
review_path = F / 'M_FINAL_REVIEW_R1.json'
review = json.loads(review_path.read_text(encoding='utf-8'))
assert review['status'] == 'PASS_WITH_SCOPE' and review['requirement_satisfied'] is True
assert review['reviewer'] == A
for source in review['source_pins'] + review['verified_references']:
    assert pin(source['path']) == source, source
projection, fresh = call('mission_cli.py', {'operation': 'project',
    'reference': str(W/'SESSION_REFERENCE.json'), 'actor': A, 'max_chars': 125000},
    'M_accept_fresh_project')
task = next(x for x in projection['projection']['active'] if x['id'] == 'M')
assert task['status'] == 'review_pending' and task['criterion'] == review['criterion']
assert task['submitted_by'] != A['id']
verified = {x['path']: x['sha256'] for x in review['verified_references']}
for evidence in task['evidence']:
    assert pin(evidence['path']) == evidence
    assert verified[evidence['path']] == evidence['sha256']
request = {'operation': 'accept', 'reference': str(W/'SESSION_REFERENCE.json'),
    'actor': A, 'task_id': 'M', 'event_id': 'organism-M-independent-accept-r1',
    'expected_revision': projection['receipt']['revision'],
    'projection_sha256': projection['projection_sha256'],
    'review_evidence': [pin(review_path)],
    'note': 'PASS independente: 10 prefixos/backups exatos, protocolo e registros mapa1185/quadro932 ENTREGUE. Estado/desempenho/dispositivo e pendencias explicitos. Aceite tecnico M; nao AUDITADA/FECHADA c1 nem confirmacao cientifica.'}
save(F/'M_ACCEPT_REQUEST_R1.json', request)
result, accepted = call('mission_cli.py', request, 'M_independent_accept')
post, post_receipt = call('mission_cli.py', {'operation': 'project',
    'reference': str(W/'SESSION_REFERENCE.json'), 'actor': A, 'max_chars': 125000},
    'M_accepted_final_project')
settled = next(x for x in post['projection']['settled'] if x['id'] == 'M')
assert settled['status'] == 'satisfied' and settled['reviewed_by'] == A['id']
save(F/'M_ACCEPTED_R1.json', {'requirement': 'M', 'actor': A,
    'reference': str(W/'SESSION_REFERENCE.json'), 'revision': post['receipt']['revision'],
    'status': settled['status'], 'review': pin(review_path),
    'request': pin(F/'M_ACCEPT_REQUEST_R1.json'), 'fresh_project': pin(fresh),
    'accept_receipt': pin(accepted), 'final_project': pin(post_receipt),
    'board_status': 'ENTREGUE', 'c1_audited_or_closed': False,
    'limits': review['scope']})
print(json.dumps({'revision': post['receipt']['revision'], 'status': settled['status'],
                  'receipt': pin(F/'M_ACCEPTED_R1.json')}, ensure_ascii=False))
