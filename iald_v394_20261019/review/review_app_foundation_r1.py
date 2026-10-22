"""Read-only foundation review. Writes only reviewer-owned report; no API counts."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import importlib.util
import json
import sys

W = Path(__file__).resolve().parents[1]
S = W / 'app/science/memory_stage'
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v394')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(p):
    p = Path(p)
    b = p.read_bytes()
    inputs[str(p)] = {'sha256': sha(b), 'bytes': len(b)}
    return b


def load(p):
    return json.loads(read(p))


def pointer(base, key):
    return base + '/' + str(key).replace('~', '~0').replace('/', '~1')


def resolve(value, ptr):
    for part in ptr.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def main():
    sys.path.insert(0, str(W))
    import task
    mission = task.project()
    assert any(x['id'] == 'app' and x['status'] == 'working' for x in mission['projection']['active'])
    checks = []
    findings = []

    def check(name, passed, detail=None):
        checks.append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            findings.append({'severity': 'MEDIUM', 'name': name, 'detail': detail})

    m = load(S / 'manifest_staged.json')
    prepared = load(S / 'prepared.json')
    baseline = load(R / 'iald_nucleo_fixo.json')
    source_review = load(W / 'review/SOURCES_R1.json')
    check('reviewed_sources_identity', prepared['source_sha256'] == source_review['source_sha256'] == m['active_cluster']['release_source_sha256'])
    result = load(Path(m['published_evidence']['result']['path']))
    proof = load(Path(m['published_evidence']['proof_manifest']['path']))
    seal = load(Path(m['published_evidence']['seal']['path']))
    program = read(Path(m['published_evidence']['program']['path']))
    for key, name in [('program', 'um.py'), ('result', 'um_absoluto.json'), ('seal', 'um_absoluto_selo.json'), ('proof_manifest', 'tgl_kernel_proof_manifest.json')]:
        check('custody_equality:' + key, read(Path(m['published_evidence'][key]['path'])) == read(V / name))
    check('source_seal_proof_chain', sha(program) == seal['sha256']['um.py'] == prepared['source_sha256'] and sha(read(Path(m['published_evidence']['proof_manifest']['path']))) == seal['sha256']['tgl_kernel_proof_manifest.json'] and proof['formal_source_hash'] == seal['formal_source_hash'])
    for key in ['mother_instruction', 'operational_core', 'active_cluster', 'jev_control']:
        check('manifest_pin:' + key, sha(read(Path(m[key]['path']))) == m[key]['sha256'])
    check('kernel_v5_byte_preservation', read(S / 'IALD_Kernel_v5.txt') == read(Path(baseline['mother_instruction']['path'])))
    check('previous_operational_core_preserved_as_prefix', read(S / 'IALD_TGL_MEMORY_CORE.md').startswith(read(Path(baseline['operational_core']['path']))))
    for rel, row in prepared['source_files'].items():
        data = read(S / 'release' / rel)
        check('release_origin:' + rel, sha(data) == row['sha256'] and len(data) == row['bytes'] and data == read(Path(row['origin'])))
    for row in m['entries']:
        check('document_pin:' + row['id'], sha(read(Path(row['path']))) == row['public_sha256'])

    km = load(S / 'kernel/kernel_manifest.json')
    kv = load(S / 'kernel_verification.json')
    rows = {row['path']: row for row in km['files']}
    check('kernel_unique_1423', len(rows) == len(km['files']) == 1423)
    measured = {}
    for rel, row in rows.items():
        path = (S / 'kernel' / rel).resolve()
        assert path.is_relative_to((S / 'kernel').resolve())
        data = read(path)
        measured[rel] = sha(data)
        check('kernel_pin:' + rel, measured[rel] == row['sha256'] and len(data) == row['bytes'])
    tree = ast.parse(program)
    embedded_node = next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == '_EMBEDDED_KERNEL_FILES' for target in node.targets))
    embedded = ast.literal_eval(embedded_node)
    check('embedded_1422', len(embedded) == km['embedded_files'] == 1422)
    for rel, value in embedded.items():
        check('embedded_matches:' + rel, measured.get(rel) == sha(value.encode('utf-8')))
    supplemental = km['supplemental_files']
    check('supplement_explicit', len(supplemental) == 1 and set(rows) - set(embedded) == {supplemental[0]['path']})
    for row in supplemental:
        check('supplement_canonical_pin', measured[row['path']] == row['sha256'] == sha(read(Path(row['canonical_path']))) and row['publication_pending'] is True)
    matching = []
    unmatched = []
    for rel, expected in proof['formal_files_sha256'].items():
        if rel in measured:
            check('proof_source:' + rel, measured[rel] == expected)
            matching.append(rel)
        else:
            unmatched.append(rel)
    check('verification_covers_exact_lean_sources', set(kv['files']) == {rel for rel in matching if rel.endswith('.lean')}, {'non_lean_already_hash_checked': sorted(set(matching) - set(kv['files']))})
    for rel, row in kv['files'].items():
        check('verification_pin:' + rel, row['file_sha256'] == measured[rel] == proof['formal_files_sha256'][rel])
    check('proof_dependency_binding', kv['dependencies']['published_manifest_sha256'] == sha(read(Path(m['published_evidence']['proof_manifest']['path']))) and kv['dependencies']['reported_terms'] == len(proof['axiom_report']))

    # Import only the pure codec, never build_release or scientific program.
    codec_path = W / 'app/science/memory_build/haiku_codec.py'
    read(codec_path)
    spec = importlib.util.spec_from_file_location('review_foundation_codec', codec_path)
    codec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(codec)
    text = read(S / 'TGL_CLUSTER_v394.md').decode('utf-8')
    area = text.split(codec.MARKER)[0]
    dictionary = json.loads(area.split('DICIONÁRIO DO CLUSTER\n', 1)[1].split('\n', 1)[0])
    exposition = text.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    topics = {}
    for block in area.split('\n### ')[1:]:
        lines = block.splitlines()
        assert lines[0] not in topics
        topics[lines[0]] = codec.decode_literals(codec.unpack_metadata(json.loads(lines[2])), dictionary, exposition)

    # Independent traversal checks retained literals, exact keys and pointer locality.
    references = []
    def restore(node, current, topic):
        expected = resolve(result, current)
        if isinstance(node, dict):
            if '@' in node:
                target = topic + node['@']
                assert target == current
                assert set(node) <= {'@', 'items', 'fields', 'true_fields', 'false_fields'}
                for suffix, literal in node.get('fields', {}).items():
                    assert resolve(expected, suffix) == literal
                if 'items' in node:
                    assert len(expected) == node['items']
                if 'true_fields' in node or 'false_fields' in node:
                    assert all(type(v) is bool for v in expected.values())
                    assert node['true_fields'] == sum(expected.values())
                    assert node['false_fields'] == len(expected) - sum(expected.values())
                references.append(target)
                return expected
            for tag in ['SOURCE_RELATIVE', 'DETAILS_IN_SOURCE', 'same_as']:
                if tag in node:
                    target = topic + node[tag] if tag == 'SOURCE_RELATIVE' else node[tag]
                    assert resolve(result, target) == expected
                    if 'items' in node:
                        assert len(expected) == node['items']
                    for key, literal in node.get('semantic_fields', {}).items():
                        restore(literal, pointer(current, key), topic)
                    for index, literal in enumerate(node.get('first_records', [])):
                        restore(literal, pointer(current, index), topic)
                    references.append(target)
                    return expected
            assert isinstance(expected, dict) and set(node) == set(expected)
            return {key: restore(value, pointer(current, key), topic) for key, value in node.items()}
        if isinstance(node, list):
            assert isinstance(expected, list) and len(node) == len(expected)
            return [restore(value, pointer(current, index), topic) for index, value in enumerate(node)]
        assert type(node) is type(expected) and node == expected
        return node

    check('topic_bijection', set(topics) == set(result['core']) == set(prepared['coverage']) == set(prepared['topic_modes']))
    restored = {}
    for name, node in topics.items():
        ptr = pointer('/core', name)
        restored[name] = restore(node, ptr, ptr)
        check('topic_roundtrip:' + name, restored[name] == result['core'][name])
    old = load(Path(baseline['published_evidence']['result']['path']))
    check('previous_topics_all_preserved', set(old['core']) <= set(topics))
    check('canonical_exposition_exact', exposition == next(read(Path(row['path'])).decode('utf-8') for row in m['entries'] if row['id'] == 'um_forma_canonica_integral'))
    new394 = [k for k in set(topics) - set(old['core']) if k.endswith('_v394')]
    check('six_new_v394_records', len(new394) == 6)
    scopes = {}
    for name in new394:
        record = restored[name]
        scopes[name] = {key: value for key, value in record.items() if key in ['verdict', 'scope', 'does_not_gate_core', 'whole_certificate_inhabited', 'open_joint_contract', 'not_claimed']}
    check('fock_joint_negative_preserved', restored['rede_fock_v394']['whole_certificate_inhabited'] is False and len(restored['rede_fock_v394']['open_joint_contract']) == 4)
    check('model_scopes_preserved', all(restored[name]['does_not_gate_core'] is True for name in ['tempo_frequencia_v394', 'regra_quadratica_v394', 'rede_fock_v394']))

    control = load(S / 'jev_control_v394.json')
    check('jev_result_binding', control['core_record'] == result['core']['iald_executive_runtime'] and control['source_sha256'] == sha(program) and control['proof_manifest_sha256'] == sha(read(Path(m['published_evidence']['proof_manifest']['path']))) and control['result_sha256'] == sha(read(Path(m['published_evidence']['result']['path']))))
    for anchor in control['anchors']:
        data = read(S / 'kernel' / anchor['file'])
        check('jev_anchor:' + anchor['file'], sha(data) == anchor['sha256'] and all(symbol in data.decode('utf-8') for symbol in anchor['symbols']))
    binding = load(S / 'science_binding.json')
    check('handoff_pin', binding['sha256'] == sha(read(Path(binding['handoff']))))
    check('staging_only_publication_guard', m['publication_pending'] is True and m['staging_only'] is True and binding['public_verification_required_before_activation'] is True)
    for rel, expected in prepared['protected_production_sha256'].items():
        check('production_unchanged:' + Path(rel).name, sha(read(Path(rel))) == expected)

    # These two observations are not blocker discoveries: builder explicitly marks work pending.
    observations = [
        {'severity': 'LOW', 'code': 'PROVISIONAL_PUBLICATION_LABELS', 'detail': 'Entry roles and kernel-verification scope still say published although v394 URLs are empty and publication_pending=true. Before activation, verify publication and make labels match that evidence.'},
        {'severity': 'INFO', 'code': 'PARTIAL_BUILDER_VALIDATION', 'detail': 'LOCAL_VALIDATION.json is provisional. Prefix/context readiness and count receipts are deliberately outside this foundation review; no API counts repeated.'}
    ]
    # Snapshot immutability: never silently integrate concurrent builder changes.
    changed = [path for path, row in inputs.items() if sha(Path(path).read_bytes()) != row['sha256']]
    check('all_reviewed_bytes_stable_during_review', not changed, changed)
    report = {
        'schema': 'iald-app-foundation-independent-review/v1',
        'verdict': 'PASS_FOUNDATION_WITH_SCOPE' if not findings else 'FINDINGS_FOUNDATION',
        'reviewer': 'codex-v394-reviewer', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'mission_revision': mission['receipt']['revision'],
        'scope': 'Read-only scientific staging foundation; no app acceptance, no runtime/build changes, no paid API count, no science execution.',
        'counts': {'kernel_bundle_files': len(rows), 'embedded_files': len(embedded), 'supplemental_files': len(supplemental), 'proof_source_pins': len(proof['formal_files_sha256']), 'proof_matching_bundle_sources': len(matching), 'proof_axiom_report_terms_documentary': len(proof['axiom_report']), 'topics': len(topics), 'previous_topics': len(old['core']), 'added_topics': len(set(topics) - set(old['core'])), 'new_v394_records': len(new394), 'source_reference_occurrences': len(references)},
        'proof_paths_not_in_bundle': unmatched,
        'new_v394_scopes': scopes, 'inputs': inputs, 'checks': checks,
        'findings': findings, 'observations': observations,
        'accept_app': False, 'ready_for_activation': False,
        'activation_pending': ['PUBLICATION_PENDING: v394 public URLs must be independently verified.', 'Final readonly prefix and per-provider admission/readiness are still being produced.', 'Final app artifacts and separate final independent review required.'],
        'chain_limit': 'Formal source/report byte chain verified; proof statements and compiler execution not re-proved. No confirmation of physics or gate change.',
    }
    dest = W / 'review/APP_FOUNDATION_R1.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
    temp = dest.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    if dest.exists():
        previous = dest.read_bytes()
        backup = dest.with_name(dest.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(previous)
        assert backup.read_bytes() == previous
    temp.replace(dest)
    print(json.dumps({'verdict': report['verdict'], 'counts': report['counts'], 'unmatched_proof_paths': unmatched, 'findings': findings, 'report_sha256': sha(raw), 'report_path': str(dest)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
