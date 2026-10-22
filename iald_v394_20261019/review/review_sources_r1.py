"""Independent documentary review; never imports scientific executable code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W))
import task

V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v394')
N = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
P = Path(r'C:\IALD\Artigo\the_boundary')
ACTOR = 'codex-v394-reviewer'
sha = lambda data: hashlib.sha256(data).hexdigest()
pin = lambda path: {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    projection = task.project()
    requirement = next(t for t in projection['projection']['active'] if t['id'] == 'sources')
    assert requirement['status'] == 'review_pending'
    assert requirement['submitted_by'] != ACTOR
    source = json.loads((W / 'sources_verified.json').read_bytes())
    assert requirement['evidence'] == [pin(W / 'sources_verified.json')]
    manifest = json.loads((V / 'CUSTODY_MANIFEST.json').read_bytes())
    seal = json.loads((V / 'um_absoluto_selo.json').read_bytes())
    proof = json.loads((V / 'tgl_kernel_proof_manifest.json').read_bytes())
    result = json.loads((V / 'um_absoluto.json').read_bytes())
    checks = []

    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        assert condition, name

    check('submitted_custody_manifest_pin', source['custody_manifest'] == pin(V / 'CUSTODY_MANIFEST.json'))
    check('version_and_custody_completion', manifest['version'] == manifest['um_version_no_selo'] == seal['um_version'] == source['release'] == 'v394' and manifest['mismatches'] == 0)
    artifacts = []
    for entry in manifest['artifacts']:
        path = (V / entry['file']).resolve()
        check('custody_path:' + entry['file'], path.is_relative_to(V.resolve()))
        blob = path.read_bytes()
        measured = {'file': entry['file'], 'bytes': len(blob), 'sha256': sha(blob)}
        check('custody_digest:' + entry['file'], measured['sha256'] == entry['sha256'])
        artifacts.append(measured)
    check('forty_unique_artifacts', len(artifacts) == len({e['file'] for e in artifacts}) == manifest['n_artifacts'] == source['artifact_count'] == 40)
    check('submitted_inventory_exact', artifacts == source['artifacts'])
    seal_pins = []
    for name, expected in seal['sha256'].items():
        path = (V / name).resolve()
        check('seal_path:' + name, path.is_relative_to(V.resolve()))
        actual = pin(path)
        check('seal_digest:' + name, actual['sha256'] == expected)
        seal_pins.append(actual)
    for name in ['um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_forma_canonica.md']:
        check('canonical_equal:' + name, (N / name).read_bytes() == (V / name).read_bytes())
    check('program_pin', sha((V / 'um.py').read_bytes()) == manifest['um_py_pin'] == source['source_sha256'])
    check('formal_hash_consistency', seal['formal_source_hash'] == proof['formal_source_hash'] == manifest['formal_source_hash'] == source['formal_source_hash'])
    check('seal_time_and_selftest', seal['timestamp'] == source['seal_timestamp'] == manifest['seal_timestamp'] and seal['fail_closed_selftest'] == manifest['selftest'] == 'FAIL_CLOSED_SELFTEST_PASSED')
    check('kernel_counts_documentary', len(proof['formal_files_sha256']) == manifest['kernel']['formal_files'] == 1423 and len(proof['axiom_report']) == manifest['kernel']['declaracoes_no_axiom_report'] == 29026 and source['kernel_counts_declared_in_custody'] == manifest['kernel'])
    statutes = {}
    for key in ['tempo_frequencia_v394', 'regra_quadratica_v394', 'rede_fock_v394']:
        s = seal[key]
        r = result['core'][key]
        check('result_seal_scope:' + key, s['verdict'] == r['verdict'] and s['scope'] == r['scope'] and s['does_not_gate_core'] is True and r['does_not_gate_core'] is True)
        statutes[key] = {k: s[k] for k in ['verdict', 'scope', 'does_not_gate_core']}
    check('joint_contract_remains_open', seal['rede_fock_v394']['whole_certificate_inhabited'] is False and len(seal['rede_fock_v394']['open_joint_contract']) == 4)
    statutes['open_joint_contract'] = seal['rede_fock_v394']['open_joint_contract']
    statutes['cunhagens_v394'] = seal['registros_v394']['cunhagens_v394']['verdict']
    check('operator_input_not_creditation', 'OPERATOR_INPUT' in statutes['cunhagens_v394'] and 'KERNEL_VALIDITY_IS_NOT_CREDITATION' in statutes['cunhagens_v394'])

    def git(*args):
        return subprocess.check_output(['git', '-C', str(P), *args], timeout=30)

    head = git('rev-parse', 'HEAD').decode().strip()
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    tracked = git('ls-tree', '-r', '--name-only', '-z', head).decode().split('\0')
    seals = [p for p in tracked if Path(p).name == 'um_absoluto_selo.json']
    check('unique_tracked_public_seal', len(seals) == 1)
    public_seal = json.loads(git('show', head + ':' + seals[0]))
    publication = {'local_head': head, 'remote_main': remote, 'release': public_seal['um_version'], 'v394_ready': head == remote and public_seal['um_version'] == 'v394'}
    check('publication_receipt_rechecked', publication == source['published'])
    check('publication_gap_explicit', publication['release'] == 'v392' and not publication['v394_ready'])
    verifier = (W / 'verify_sources.py').read_text(encoding='utf-8')
    check('verifier_uses_tracked_public_path', "['ls-tree','-r','--name-only','-z',head]" in verifier and "public['um_version']" in verifier)
    check('verifier_documentary_scope', source['science_executed'] is False and source['gate_modified'] is False and 'Documentary verification' in source['custody_statistics_scope'])
    report = {
        'schema': 'iald-independent-sources-review/v1',
        'verdict': 'PASS_WITH_SCOPE',
        'criterion_satisfied': True,
        'reviewer': {'id': ACTOR, 'kind': 'agent', 'assignment': 'Explicit human assignment in this review session; actor label is not cryptographic authentication.'},
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'task_id': 'sources',
        'criterion': requirement['criterion'],
        'reviewed_submission': requirement['evidence'],
        'baseline_revision': projection['receipt']['revision'],
        'baseline_projection_sha256': projection['projection_sha256'],
        'inputs': [pin(W / 'verify_sources.py'), pin(V / 'CUSTODY_MANIFEST.json'), pin(V / 'um_absoluto_selo.json'), pin(V / 'tgl_kernel_proof_manifest.json'), pin(V / 'um_absoluto.json'), pin(Path(__file__))],
        'checks': checks, 'artifact_count': len(artifacts), 'artifacts': artifacts,
        'seal_pins': seal_pins, 'source_sha256': manifest['um_py_pin'],
        'seal_timestamp': seal['timestamp'], 'formal_source_hash': seal['formal_source_hash'],
        'statutes': statutes, 'gate_as_recorded_not_changed': manifest['gate'],
        'published': publication, 'tracked_public_seal_path': seals[0],
        'public_seal_blob_sha256': sha(git('show', head + ':' + seals[0])),
        'limitations': [
            'REAL: byte integrity, custody completion and documentary cross-checks only; no new scientific proof or nature confirmation.',
            'Kernel counts are documentary consistency checks; Lean and um.py were neither run nor imported.',
            'Publication remains v392 at the measured local/remote commit; no v394 URL was constructed or certified.',
            'This PASS satisfies sources only. App activation requires its final package and independently verified URLs; app, queue and deploy were not reviewed or accepted.',
            'M2 model identification, physical device/clock and the four joint-network obligations retain their explicit DERIVED/OPEN scope; operator inscriptions retain INPUT/ONTO scope.'
        ],
        'findings': [], 'runtime_changed': False, 'paid_network_used': False,
    }
    destination = W / 'review' / 'SOURCES_R1.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
    temporary = destination.with_suffix('.json.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw and len(raw) > 0
    assert not destination.exists()
    temporary.replace(destination)
    print(json.dumps({'verdict': report['verdict'], 'checks': len(checks), 'artifact_count': len(artifacts), 'seal_pins': len(seal_pins), 'report': pin(destination), 'published': publication}, ensure_ascii=False))


if __name__ == '__main__':
    main()
