"""Independent installed-byte verification and explicitly authorized M1 acceptance."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REF = ROOT.parent / 'FECHO_MISSION_REFERENCE.json'
CLI = Path(r'C:\IALD\MEMORIA_IALD\mission_cli.py')
PYTHON = r'C:\Python314\python.exe'
ACTOR = {'id': 'codex-mission-memory-review', 'kind': 'agent'}
TASK = 'M1_HANDOFF_CAPACITY'
CONTEXT = '34290aaa-3dcc-51d5-b224-f3eeec93509b'

def read(path):
    return json.loads(Path(path).read_bytes())

def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def validate(entry):
    actual = pin(entry['path'])
    assert actual['sha256'] == entry['sha256'], entry['path']
    if 'bytes' in entry:
        assert actual['bytes'] == entry['bytes'], entry['path']
    return actual

def fresh(name, value):
    path = ROOT / name
    assert not path.exists(), path
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw

def call(request):
    result = subprocess.run([PYTHON, '-B', '-X', 'utf8', str(CLI)],
        input=json.dumps(request, ensure_ascii=False), text=True, encoding='utf-8', capture_output=True)
    return {'exit_code': result.returncode, 'response': json.loads(result.stdout), 'stderr': result.stderr}

def project():
    result = call({'operation': 'project', 'reference': str(REF), 'max_chars': 100000})
    assert result['exit_code'] == 0 and result['response']['ok'], result
    state = result['response']['result']
    assert state['projection']['context_id'] == CONTEXT
    return result, state

def review():
    sync, state = project()
    p = state['projection']
    task = next(t for t in p['active'] if t['id'] == TASK)
    assert task['status'] == 'review_pending' and task['submitted_by'] != ACTOR['id']
    initial = read(ROOT / 'REVIEW_E1.json')
    assert initial['reviewer'] == ACTOR and initial['verdict'] == 'PASS_FOCAL_CANDIDATE'
    deploy = read(ROOT / 'DEPLOYMENT_E1.json')
    installed = read(ROOT / 'VERIFICATION_INSTALLED.json')
    candidate_test = read(ROOT / 'VERIFICATION_CANDIDATE.json')
    synthetic_test = read(ROOT / 'SYNTHETIC_MCP.json')
    assert deploy['ok'] and installed['ok'] and installed['mode'] == 'installed'
    assert candidate_test['ok'] and synthetic_test['ok']
    checked = [validate(e) for e in task['evidence']]
    checked.append(validate(deploy['review']))
    expected_prior = {r['target']: r['new_sha256'] for r in read(ROOT.parent / 'DEPLOYMENT.json')['files']}
    candidate = ROOT / 'mission_bridge_candidate.py'
    bridge = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\mission_bridge.py')
    protocol = Path(r'C:\IALD\MEMORIA_IALD\MISSION_PROTOCOL.md')
    assert {r['target'] for r in deploy['files']} == {str(bridge), str(protocol)}
    checked_rows = []
    for row in deploy['files']:
        target = Path(row['target'])
        backup = Path(row['backup']['path'])
        target_pin, backup_pin = pin(target), validate(row['backup'])
        assert target_pin['sha256'] == row['new_sha256'] and target_pin['bytes'] == row['bytes']
        assert backup_pin['sha256'] == row['old_sha256'] == expected_prior[str(target)]
        assert backup.parent == target.parent
        if target == bridge:
            assert target.read_bytes() == candidate.read_bytes()
            assert not row['append_only']
            assert backup.read_bytes() == (ROOT.parent / 'mission_bridge.py').read_bytes()
        else:
            assert row['append_only']
            assert target.read_bytes() == backup.read_bytes() + (ROOT / 'PROTOCOL_ADDENDUM.md').read_bytes()
        checked += [target_pin, backup_pin]
        checked_rows.append({'target': target_pin, 'backup': backup_pin,
                             'prior_deployment_hash_matches_backup': True,
                             'candidate_equal' if target == bridge else 'exact_byte_append': True})
    for name in ['reference', 'bridge', 'server']:
        checked.append(validate(installed[name]))
    assert installed['bridge']['sha256'] == pin(candidate)['sha256']
    assert candidate_test['bridge']['sha256'] == installed['bridge']['sha256'] == synthetic_test['bridge']['sha256']
    for name in ['exact_capacity_passed', 'mcp_schema_exposes_budget', 'mcp_handoff_equals_sync', 'unchanged_poll']:
        assert installed[name] is True
    assert len(installed['negative_checks']) == 4 and all(r['refused'] for r in installed['negative_checks'].values())
    assert installed['actual_chars'] == candidate_test['actual_chars'] > 24000
    assert installed['projection_sha256'] == candidate_test['projection_sha256']
    assert synthetic_test['chars'] > 24000 and synthetic_test['requirements'] == 8
    assert synthetic_test['sync_handoff_exact_match']
    # Prior bridge target intentionally changed; all other code/protocol/test inputs stay pinned.
    for entry in initial['inputs']:
        if entry['path'] != str(bridge):
            checked.append(validate(entry))
    for name in ['install.py', 'DEPLOYMENT_E1.json', 'VERIFICATION_INSTALLED.json', 'PROTOCOL_ADDENDUM.md']:
        checked.append(pin(ROOT / name))
    checked = list({r['path']: r for r in checked}.values())
    fresh('REVIEW_INSTALLED_E1_PROJECT.json', sync)
    report = {
        'schema': 'iald-independent-installed-review/v1',
        'time_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'reviewer': ACTOR, 'verdict': 'PASS_INSTALLED_TECHNICAL_REQUIREMENT', 'requirement': TASK,
        'mission_reference': pin(REF), 'context_id': CONTEXT, 'revision_observed': p['revision'],
        'criterion': task['criterion'], 'evidence': task['evidence'], 'submitted_by': task['submitted_by'],
        'prior_independent_review': pin(ROOT / 'REVIEW_E1.json'),
        'installed_files': checked_rows,
        'checks': {
            'exactly_two_expected_destinations': True,
            'installed_bridge_equals_reviewed_candidate_bytes': True,
            'same_directory_backups_match_prior_deployment_pins': True,
            'protocol_equals_backup_plus_exact_reviewed_addendum_bytes': True,
            'unchanged_controller_CLI_tests_and_candidate_inputs_checked': True,
            'installed_real_MCP_receipt_pin_matches_installed_bridge': True,
            'actual_chars_tested': installed['actual_chars'],
            'real_handoff_sync_projection_equal': True,
            'exact_budget_passes': True,
            'default_one_short_invalid_and_stale_refused': True,
            'synthetic_real_MCP_chars': synthetic_test['chars'], 'synthetic_requirements': 8,
            'four_tools_CAS_lease_overflow_integrity_preserved': 'Established in prior independent focal review; identical candidate now installed.'
        },
        'atomicity_and_custody': 'Install source uses exclusive byte backup, verified temporary file, concurrent-byte checks and os.replace; present destination/backup bytes and deployment receipts agree. Reviewer did not execute the installer.',
        'test_authorship': 'MCP real/synthetic executions belong to constructor; reviewer inspected test code, receipts and pins, and independently measured installed/backup bytes. No suite rerun.',
        'limits': ['Technical acceptance only; no global board FECHADA/AUDITADA, scientific proof or gate change.',
                   'Real installed MCP receipt used revision35; review observes the same exact mission at revision37 after submission. Accept requires a fresh projection.',
                   'Existing persistent MCP processes were not restarted; their reload limitation is explicit in the installed protocol.',
                   'No provider calls, scientific builds or global-memory-document edits by reviewer.'],
        'checked_pins': checked
    }
    fresh('REVIEW_INSTALLED_E1.json', report)
    print(json.dumps({'verdict': report['verdict'], 'revision': p['revision'],
                      'review': pin(ROOT / 'REVIEW_INSTALLED_E1.json'), 'checked_pins': len(checked)}, ensure_ascii=False))

def accept():
    report_path = ROOT / 'REVIEW_INSTALLED_E1.json'
    report = read(report_path)
    assert report['reviewer'] == ACTOR and report['verdict'] == 'PASS_INSTALLED_TECHNICAL_REQUIREMENT'
    assert not (ROOT / 'ACCEPT_E1_REQUEST.json').exists(), 'Reconcile existing acceptance request before retry'
    for entry in report['checked_pins']:
        validate(entry)
    validate(report['mission_reference'])
    sync, state = project()
    p = state['projection']
    tasks = {t['id']: t for t in p['active'] + p['settled']}
    task = tasks[TASK]
    assert task['status'] == 'review_pending' and task['submitted_by'] != ACTOR['id']
    assert task['criterion'] == report['criterion'] and task['evidence'] == report['evidence']
    assert all(tasks[d]['status'] == 'satisfied' for d in task['depends_on']) and not p['hold']
    fresh('ACCEPT_E1_PRE_PROJECT.json', sync)
    request = {'operation': 'accept', 'reference': str(REF), 'task_id': TASK, 'actor': ACTOR,
               'event_id': 'M1-handoff-capacity-independent-accept-20261016-e1',
               'expected_revision': p['revision'], 'projection_sha256': state['projection_sha256'],
               'review_evidence': [{k: v for k, v in pin(report_path).items() if k in {'path', 'sha256'}}],
               'note': 'Aceite técnico independente do repasse MCP com capacidade explícita, integralidade, recusas, instalação e backups conferidos. Não fecha quadro nem altera gate ou ciência.'}
    fresh('ACCEPT_E1_REQUEST.json', request)
    result = call(request)
    fresh('ACCEPT_E1_RECEIPT.json', result)
    assert result['exit_code'] == 0 and result['response']['ok'], result
    post, after_state = project()
    fresh('ACCEPT_E1_POST_PROJECT.json', post)
    after = after_state['projection']
    accepted = next(t for t in after['settled'] if t['id'] == TASK)
    assert accepted['status'] == 'satisfied' and accepted['reviewed_by'] == ACTOR['id']
    assert accepted['review_evidence'] == request['review_evidence']
    assert not after['tetelestai']
    print(json.dumps({'accepted': True, 'revision': after['revision'], 'task_id': TASK,
                      'tetelestai': after['tetelestai'], 'receipt': pin(ROOT / 'ACCEPT_E1_RECEIPT.json')}, ensure_ascii=False))

if __name__ == '__main__':
    accept() if sys.argv[1:] == ['--accept'] else review()
