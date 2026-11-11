"""Record reviewed preparation; never install or infer operator approval."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import task
import preservation_guard

W = Path(__file__).resolve().parent
Q = W.parent / 'scientific_memory_sync_20261106_v409'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path)
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

review = read(W / 'validation/review_final.json')
assert review['status'] == 'PASS'
assert review['plan_sha256'] == pin(W / 'install_plan.json')['sha256']
assert not (W / 'deployment.json').exists()
assert not (W / 'APROVACAO_V409.json').exists()
preserved = preservation_guard.verify()
runtime = read(preservation_guard.ROOT / 'iald_nucleo_fixo.json')
assert runtime['operational_core']['current_release'] == 'v408'
evidence = [pin(W / name) for name in (
    'install_plan.json', 'validation/review_final.json', 'review/APP_ACCEPT_R2.json',
    'review/QUEUE_RECONSTRUCTION.json', 'review/QUEUE_HELPER_R1.json',
    'QUEUE_ACCEPT_R1.json', 'QUEUE_HELPER_ACCEPT_R1.json',
    'BUILDER_MEASUREMENTS.json', 'app/LIMITS_FINAL_R2.json',
    'app/NATIVE_COUNTS_COMPLETE.json', 'PRESERVATION_BASELINE.json')]
evidence += [pin(Q / 'PROMOTION_PLAN.json'), pin(Q / 'promotion/PLAN.json'), pin(Q / 'promote_v409.py')]
report = {
    'status': 'PREPARED_REVIEWED_AWAITING_V409_OPERATOR_GATE',
    'at': datetime.now(timezone.utc).isoformat(), 'release_prepared': 'v409',
    'release_current': runtime['operational_core']['current_release'],
    'files_prepared': review['files'], 'topics': review['P2']['full_cluster'],
    'runtime_preservation_files': len(preserved), 'runtime_preserved': all(preserved.values()),
    'app_review': 'PASS', 'queue_review': 'PASS_STAGING_AND_HELPER',
    'paid_generation_calls': 0, 'new_public_native_count_calls': 6,
    'production_deployments': 0, 'restarts': 0,
    'approval_pending': 'Version-specific web restart and protected F0.3 write/activation required by ORDEM_009; asked directly in this chat; no reply received at this record.',
    'next_steps': ['Record actual operator reply and its hash',
                   'Materialize and fully verify final queue paths, obtain independent review, then activate with CAS',
                   'Deploy app in quiet maintenance window, submit and independently accept deploy before verify claim',
                   'Verify installed loaders and HTTP; refresh Torre and issue actual delivery receipt'],
    'ui_validation': 'Not performed: Computer Use stopped this turn because browser URL could not be identified reliably. No browser workaround attempted.',
    'mobile': 'Backend/data update only. No client change, new native build or physical installation in this preparation.',
    'evidence': evidence, 'reference': str(task.REF),
}
task.new('PREPARATION_REVIEWED_R1.json', report)
current = task.call({'operation': 'project', 'reference': str(task.REF), 'max_chars': 100000}, False)
changes = {'records': [{
    'id': 'v409_reviewed_preparation_gate', 'kind': 'fact', 'statute': 'REAL',
    'text': 'App v409 staging independently reviewed PASS: 1788 data destinations, 483 topics, native counts checked. Queue staging and promotion helper independently reviewed. Runtime remains v408, 13 preservation hashes match. No deployment/restart. Specific v409 operator gate requested under ORDEM_009; awaiting reply.',
    'sources': [{'kind': 'artifact', 'ref': str(W / 'PREPARATION_REVIEWED_R1.json'), 'sha256': pin(W / 'PREPARATION_REVIEWED_R1.json')['sha256']}]
}], 'flow': {'phase': 'v409_reviewed_awaiting_operator',
            'next_action': 'Receive explicit v409 gate reply; preserve original and then use reviewed CAS/maintenance helpers. Do not repeat COUNTs or build staging.'}}
task.new('PREPARATION_TRANSITION_CHANGES.json', changes)
r = task.call({'operation': 'transition', 'reference': str(task.REF),
               'expected_revision': current['receipt']['revision'],
               'event_id': 'v409-reviewed-preparation-operator-gate',
               'actor': {'id': task.OWNER, 'kind': 'agent'},
               'changes_file': str(W / 'PREPARATION_TRANSITION_CHANGES.json'),
               'changes_sha256': pin(W / 'PREPARATION_TRANSITION_CHANGES.json')['sha256']}, False)
task.new('PREPARATION_TRANSITION_RECEIPT.json', r)
print(json.dumps({'status': report['status'], 'current': report['release_current'], 'receipt': r.get('receipt', r.get('revision')), 'report': pin(W / 'PREPARATION_REVIEWED_R1.json')}))
