"""Record measured activation in this exact mission; keep pending UI scope explicit."""
import json
import hashlib
from pathlib import Path
import task
W = Path(__file__).resolve().parent
def pin(p): return {'kind': 'artifact', 'ref': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
assert task.check('verify')['ready']
for p in ('INSTALLED_VERIFICATION.json', 'LIVE_BACKEND.json', 'INSTALLED_RETRIEVAL.json', 'review/QUEUE_ACTIVATION_R1.json'):
    assert json.loads((W / p).read_bytes())['status'] == 'PASS'
deposit = json.loads((W / 'MEMORY_DELIVERY_RECEIPT.json').read_bytes())
assert deposit['ok'] is True
assert hashlib.sha256(Path(deposit['arquivo']).read_bytes()).hexdigest() == deposit['sha256_deposito']
current = task.call({'operation': 'get', 'reference': str(task.REF)}, False)
changes = {'records': [{
    'id': 'v409_activated_verified_engineering', 'kind': 'fact', 'statute': 'REAL',
    'text': 'App/JEV v409 installed and loaded: 1788 data destinations and 13 prior operational pins verified; only web child restarted under same supervisor, HTTP200. Queue v409 active with 13 documents and 33036 chunks, final paths reviewed before CAS, generation verified in a new process. Local scientific retrieval and 186 synthetic stream cases passed. Torre JEV current; one scheduled clock task remains stale outside scope. Memory deposit recorded for c1 triage.',
    'sources': [pin(W / 'TECHNICAL_DELIVERY_R1.json'), pin(W / 'MEMORY_DELIVERY_RECEIPT.json')]
}, {
    'id': 'v409_live_and_physical_scope', 'kind': 'pending', 'statute': 'OPEN',
    'text': 'No live model conversation or physical phone test in this release. Technical acceptance explicitly does not claim these checks. No native client changes or new store builds; shared server supplies v409. Original broader verification criterion preserved in history and amended explicitly with independent scope review.',
    'sources': [pin(W / 'VERIFY_SCOPE_AMENDMENT.json'), pin(W / 'review/VERIFY_SCOPE_OPINION_R2.json')]
}], 'flow': {**current['p'], 'phase': 'v409_activated_awaiting_final_review',
            'next_action': 'Independent acceptance of technical verification, then finalize ORDEM_009 handoff. Do not repeat counts, deployment or CAS.'}}
task.new('ACTIVATED_TRANSITION_CHANGES.json', changes)
r = task.call({'operation': 'transition', 'reference': str(task.REF),
               'expected_revision': current['revision'], 'event_id': 'v409-activated-verified-engineering',
               'actor': {'id': task.OWNER, 'kind': 'agent'}, 'changes_file': str(W / 'ACTIVATED_TRANSITION_CHANGES.json'),
               'changes_sha256': pin(W / 'ACTIVATED_TRANSITION_CHANGES.json')['sha256']}, False)
task.new('ACTIVATED_TRANSITION_RECEIPT.json', r)
print(json.dumps({'status': 'RECORDED', 'revision': r.get('revision')}))
