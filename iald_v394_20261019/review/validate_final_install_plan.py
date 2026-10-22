"""Read-only preflight for the eventual v394 plan. Never imports deployment controls.

Usage: python -B -X utf8 validate_final_install_plan.py --plan <absolute.json>
Add --require-ready to fail while mission prerequisites remain unsatisfied.
This validator does not authorize, stop processes, install, activate queue, or restart.
Final public byte/count evidence still needs its separate substantive review.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import sys

W = Path(__file__).resolve().parents[1]
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD').resolve()
REFERENCE = W / 'SESSION_REFERENCE.json'
sha = lambda b: hashlib.sha256(b).hexdigest()
PREREQUISITES = ('sources', 'app', 'queue', 'reader_compat', 'all_engines_admission')
READER_NAMES = {'iald_estado_publicado.py', 'iald_core_indexado.py'}


def validate(plan_path, require_ready=False):
    plan_path = Path(plan_path).resolve()
    assert plan_path.is_relative_to(W.resolve()), 'Plan must be in the authorized task workspace'
    raw = plan_path.read_bytes()
    plan = json.loads(raw)
    assert isinstance(plan.get('files'), list) and plan['files'], 'Missing nonempty final files inventory'
    copies = json.loads((W / 'DEPLOYMENT_CONTROLS_PREPARED.json').read_bytes())
    controls = {}
    for row in copies['controls']:
        candidate = Path(row['candidate'])
        candidate_bytes = candidate.read_bytes()
        assert candidate_bytes == Path(row['source']).read_bytes(), 'Control differs from copied baseline'
        assert sha(candidate_bytes) == row['sha256'], 'Control pin changed; independent review required'
        ast.parse(candidate_bytes)
        controls[candidate.name] = sha(candidate_bytes)
    destinations = set()
    planned = {}
    for row in plan['files']:
        assert {'source', 'destination', 'sha256', 'baseline'} <= set(row), 'Incomplete transaction row'
        assert Path(row['source']).is_absolute() and Path(row['destination']).is_absolute()
        source = Path(row['source']).resolve()
        dest = Path(row['destination']).resolve()
        assert source.is_relative_to(W.resolve()) and dest.is_relative_to(ROOT), 'Path outside authorized install scope'
        key = str(dest).casefold()
        assert key not in destinations, 'Duplicate destination (case-insensitive): ' + str(dest)
        destinations.add(key)
        assert source.name.lower() not in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}, 'Confidential source refused'
        assert dest.name.lower() not in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}, 'Protected destination refused'
        assert dest.suffix.lower() not in {'.sqlite3', '.db'}, 'Operational ledger is outside this scientific release plan'
        data = source.read_bytes()
        assert data and sha(data) == row['sha256'], 'Empty/changed stage: ' + str(source)
        baseline = sha(dest.read_bytes()) if dest.exists() else None
        assert baseline == row['baseline'], 'Concurrent baseline change: ' + str(dest)
        if dest.suffix.lower() == '.py':
            if dest.parent == ROOT:
                assert dest.name in READER_NAMES, 'Unreviewed runtime Python replacement'
                reader_review = json.loads((W / 'review/READER_COMPAT_R1.json').read_bytes())
                evidence = next(x for x in reader_review['files'] if Path(x['runtime_path']).resolve() == dest)
                assert sha(data) == evidence['staged_sha256'] and baseline == evidence['baseline_sha256'], 'Reader differs from accepted candidate'
            else:
                assert dest.name == 'um.py' and 'release' in {p.casefold() for p in dest.parts}, 'Build helper/shim must not be installed as source data'
            ast.parse(data)
        planned[key] = {'source': str(source), 'sha256': row['sha256'], 'bytes': len(data)}
    sys.path.insert(0, str(W))
    import task
    projection = task.project()
    assert str(task.REF) == str(REFERENCE)
    tasks = {t['id']: t for group in ('active', 'settled') for t in projection['projection'][group]}
    pending = []
    accepted_evidence = []
    for name in PREREQUISITES:
        current = tasks.get(name)
        if not current or current['status'] != 'satisfied':
            pending.append(name)
            continue
        assert current.get('reviewed_by') and current['reviewed_by'] != current.get('submitted_by'), 'Real distinct review absent: ' + name
        assert current['review_evidence'], 'No review evidence: ' + name
        for evidence in current['evidence'] + current['review_evidence']:
            assert sha(Path(evidence['path']).read_bytes()) == evidence['sha256'], 'Broken mission evidence: ' + name
        accepted_evidence.append(name)
    if require_ready:
        assert not pending, 'Mission prerequisites pending: ' + ','.join(pending)
    return {
        'status': 'PLAN_BYTES_AND_BASELINES_CHECKED_NOT_AUTHORIZATION',
        'plan_sha256': sha(raw), 'files_checked': len(planned), 'control_sha256': controls,
        'mission_revision': projection['receipt']['revision'],
        'mission_projection_sha256': projection['projection_sha256'],
        'accepted_prerequisites': accepted_evidence, 'pending_prerequisites': pending,
        'ready_for_deployment': False,
        'remaining_final_review': [
            'Verify final immutable Git/raw HTTP bytes and binding of all intended public sources.',
            'Verify final model-specific native count receipts bound to exact selected prefixes/tools/identities.',
            'Verify queue snapshot, generation CAS baseline, fixed jobs and its authorized transition receipts.',
            'Review every manifest/deployment identity and coordinated queue/app activation order in the final plan.',
            'Obtain fresh deploy lease/preflight after satisfied prerequisites; validation/final_checks.json and validation/review_final.json must cover exact plan and controls.',
            'The deployment execution must still prove actual quiescence and current baselines; this read-only check does not substitute that window.'
        ],
        'installed': False, 'maintenance_executed': False, 'queue_activated': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', required=True)
    parser.add_argument('--require-ready', action='store_true')
    options = parser.parse_args()
    try:
        print(json.dumps(validate(options.plan, options.require_ready), ensure_ascii=False, indent=2))
    except Exception as error:
        print(json.dumps({'status': 'REFUSED', 'error_type': type(error).__name__, 'reason': str(error), 'installed': False}, ensure_ascii=False))
        sys.exit(2)
