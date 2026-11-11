"""Bind the explicit human reply received in this chat to the reviewed plans."""
import hashlib
import json
from pathlib import Path
import task

W = Path(__file__).resolve().parent
Q = W.parent / 'scientific_memory_sync_20261106_v409'

def pin(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

schema = json.loads((Q / 'promotion/APPROVAL_REQUIREMENTS.json').read_bytes())
auth = schema['f03']
checks = {
    'plan_sha256': Q / 'promotion/PLAN.json',
    'promotion_cli_sha256': Q / 'promote_v409.py',
    'reviewed_staging_plan_sha256': Q / 'PROMOTION_PLAN.json',
    'parent_reference_sha256': W / 'SESSION_REFERENCE.json',
}
for field, path in checks.items():
    assert auth[field] == pin(path), field
source = W / 'OPERATOR_APPROVAL_V409.txt'
approval = {
    'release': 'v409', 'restart_web_8082': True,
    'operator_reply_path': str(source), 'operator_reply_sha256': pin(source),
    'operator_order': {'path': str(source), 'sha256': pin(source)},
    'question_item_id': '["request_user_input_async","call_37f39e3fd960412d95187fd0939300ad",0]',
    'human_answer_verbatim': 'Autorizo a ativação completa da v409',
    'f03': auth,
    'scope': 'Reviewed v409 activation only; quiet web maintenance and final-path queue verification before CAS remain mandatory.',
}
task.new('APROVACAO_V409.json', approval)
p = task.call({'operation': 'project', 'reference': str(task.REF), 'max_chars': 100000}, False)
changes = {'records': [{
    'id': 'v409_explicit_human_activation_reply', 'kind': 'decision', 'statute': 'INPUT',
    'text': 'Human reply received: Autorizo a ativação completa da v409. Scope is the exact question: app/JEV v409, protected F0.3 snapshot write and activation, and only web child 8082 restart after quiet checks.',
    'sources': [{'kind': 'artifact', 'ref': str(source), 'sha256': pin(source)}]
}], 'flow': {'phase': 'v409_activation_authorized', 'next_action': 'Materialize/review final queue paths; activate with CAS; deploy reviewed app in quiet maintenance and verify.'}}
task.new('APPROVAL_TRANSITION_CHANGES.json', changes)
r = task.call({'operation': 'transition', 'reference': str(task.REF), 'expected_revision': p['receipt']['revision'],
               'event_id': 'v409-explicit-human-activation-reply', 'actor': {'id': task.OWNER, 'kind': 'agent'},
               'changes_file': str(W / 'APPROVAL_TRANSITION_CHANGES.json'),
               'changes_sha256': pin(W / 'APPROVAL_TRANSITION_CHANGES.json')}, False)
task.new('APPROVAL_TRANSITION_RECEIPT.json', r)
print(json.dumps({'approval_sha256': pin(W / 'APROVACAO_V409.json'), 'revision': r.get('revision')}))
