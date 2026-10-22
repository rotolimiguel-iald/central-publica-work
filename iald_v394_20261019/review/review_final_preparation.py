"""Review selected scientific projections, pinned receipts and data-only inventory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, sys

W = Path(__file__).resolve().parents[1]
A = W / 'app'
S = A / 'science/memory_stage'
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(path):
    path = Path(path)
    data = path.read_bytes()
    inputs[str(path)] = {'sha256': sha(data), 'bytes': len(data)}
    return data


def load(path):
    return json.loads(read(path))


def pincheck(row):
    raw = read(row['path'])
    assert sha(raw) == row['sha256']
    if 'bytes' in row:
        assert len(raw) == row['bytes']
    return raw


def child(p, key):
    return p + '/' + str(key).replace('~', '~0').replace('/', '~1')


def resolve(root, ptr):
    for key in ptr.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        root = root[int(key)] if isinstance(root, list) else root[key]
    return root


def main():
    sys.path.insert(0, str(W))
    import task
    project = task.project()
    app = next(t for t in project['projection']['active'] if t['id'] == 'app')
    assert app['status'] == 'review_pending'
    path = A / 'DELIVERY_PREPARED.json'
    assert app['evidence'] == [{'path': str(path), 'sha256': sha(read(path))}]
    delivery = load(path)
    foundation = load(W / 'review/APP_FOUNDATION_R1.json')
    # Recheck exactly the prior foundation bytes, without rerunning scientific code.
    for source, row in foundation['inputs'].items():
        assert sha(read(source)) == row['sha256'], source
    m = load(S / 'manifest_staged.json')
    result = load(m['published_evidence']['result']['path'])
    result_sha = sha(read(m['published_evidence']['result']['path']))
    baseline = load(A / 'runtime_baseline.json')
    for row in baseline['files']:
        pincheck(row)
    selection = load(A / 'PACKAGE_SELECTION.json')
    assert selection['selected'] == delivery['selected_packages']
    assert selection['rejected'] == delivery['rejected_packages']
    for key in ['source_program', 'custody_handoff', 'jev_source_bound_contract', 'expanded_reconstruction_validation', 'local_connectors_admission', 'runtime_baseline', 'proposed_destinations', 'package_selection', 'count_commands_and_history']:
        pincheck(delivery[key])
    packages = {}
    reference_records = []
    summary_records = []
    explicit_auxiliary = []
    validation_errors = []

    for role, selected in selection['selected'].items():
        prefix = pincheck(selected['prefix']).decode('utf-8')
        manifest = json.loads(pincheck(selected['manifest']))
        receipt = json.loads(pincheck(selected['count_receipt']))
        assert manifest['prefix_sha256'] == receipt['prefix_sha256'] == selected['prefix']['sha256']
        assert manifest['budget'] == receipt['budget'] == selected['budget']
        assert receipt['native_tools_sha256'] == manifest['tools_sha256'] == selected['tools_sha256']
        assert receipt['deployment'] == manifest['deployment']
        assert receipt['deployment']['source_sha256'] == delivery['source_program']['sha256']
        budget = receipt['budget']
        assert budget['ready'] and budget['fits']
        assert budget['remaining_tokens'] == 1000000 - budget['request_input_tokens'] - budget['reserved_output_tokens'] - budget['margin_tokens']
        assert budget['permanent_tokens'] == (877536 if role == 'haiku' else 395669)
        lines = prefix.splitlines()
        literals_marker = 'LITERAIS_COMPARTILHADOS' if role == 'haiku' else 'DICIONÁRIO DE LITERAIS'
        dictionary = json.loads(lines[lines.index(literals_marker) + 1])
        flags = json.loads(lines[lines.index('DICIONÁRIO DE INDICADORES LITERAIS') + 1]) if 'DICIONÁRIO DE INDICADORES LITERAIS' in lines else {}
        exposition = prefix.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
        alias = {'@F': '@SOURCE_FIELDS', '@I': '@SOURCE_ITEMS', '@L': '@TGL_LITERAL', '@X': '@EXPOSITION', '@Y': '@SUMMARY'}

        def decode(node, stack=()):
            if isinstance(node, list):
                return [decode(x, stack) for x in node]
            if not isinstance(node, dict):
                return node
            node = {alias.get(k, k): v for k, v in node.items()}
            if set(node) == {'@TGL_LITERAL'}:
                key = node['@TGL_LITERAL']
                assert key not in stack
                return decode(dictionary[key], stack + (key,))
            if set(node) == {'@enum'}:
                return node['@enum'].upper().replace(' ', '_')
            if set(node) == {'@upper'}:
                return node['@upper'].upper()
            if set(node) == {'@concat'}:
                return ''.join(decode(x, stack) for x in node['@concat'])
            if '@EXPOSITION' in node:
                span = node.get('span', node['@EXPOSITION'])
                assert isinstance(span, list) and len(span) == 2
                offset, length = span
                assert 0 <= offset and length > 0 and offset + length <= len(exposition)
                value = exposition[offset:offset + length]
                if 'starts_with' in node:
                    assert value.startswith(node['starts_with'])
                return value
            decoded = {k: decode(v, stack) for k, v in node.items() if k not in ['@SOURCE_FIELDS', '@SOURCE_ITEMS', '@B']}
            for tag in ['@SOURCE_FIELDS', '@SOURCE_ITEMS']:
                for k in node.get(tag, []):
                    assert k not in decoded
                    decoded[k] = {'@': '/' + k}
                    if tag == '@SOURCE_ITEMS':
                        decoded[k]['items'] = node[tag][k]
            if '@B' in node:
                extra = flags[node['@B']]
                assert not set(extra) & set(decoded)
                assert all(type(v) is bool for v in extra.values())
                decoded.update(extra)
            return decoded

        def restore(node, current, topic):
            expected = resolve(result, current)
            if isinstance(node, dict):
                if '@SUMMARY' in node:
                    coordinates = node['@SUMMARY']
                    if isinstance(coordinates, list):
                        suffix, start, length = coordinates
                        target = topic + suffix
                    else:
                        assert coordinates == topic.split('/')[-1]
                        target = node['source_pointer']
                        start, length = node['span']
                    assert target == current
                    assert 0 <= start and length > 0 and start + length <= len(exposition)
                    summary_records.append({'role': role, 'source_pointer': target, 'span': [start, length], 'summary_sha256': sha(exposition[start:start + length].encode()), 'scope': 'Explicit derived summary, not claimed as original literal; full source value independently recoverable.'})
                    return expected
                if '@' in node:
                    target = topic + node['@']
                    assert target == current
                    assert set(node) <= {'@', 'fields', 'items', 'true_fields', 'false_fields'}
                    if 'items' in node:
                        assert node['items'] == len(expected)
                    for suffix, value in node.get('fields', {}).items():
                        assert suffix.startswith('/')
                        assert restore(value, current + suffix, topic) == resolve(expected, suffix)
                    if 'true_fields' in node or 'false_fields' in node:
                        assert isinstance(expected, dict) and all(type(v) is bool for v in expected.values())
                        assert node['true_fields'] == sum(expected.values()) and node['false_fields'] == len(expected) - sum(expected.values())
                    reference_records.append({'role': role, 'pointer': target, 'kind': 'relative_source'})
                    return expected
                for tag in ['SOURCE_RELATIVE', 'DETAILS_IN_SOURCE', 'same_as']:
                    if tag in node:
                        target = topic + node[tag] if tag == 'SOURCE_RELATIVE' else node[tag]
                        assert resolve(result, target) == expected
                        if 'items' in node:
                            assert node['items'] == len(expected)
                        for k, value in node.get('semantic_fields', {}).items():
                            restore(value, child(current, k), topic)
                        for i, value in enumerate(node.get('first_records', [])):
                            restore(value, child(current, i), topic)
                        reference_records.append({'role': role, 'pointer': target, 'kind': tag})
                        return expected
                if 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE' in node:
                    aggregate = node['AUDIT_BOOLEAN_FIELDS_IN_SOURCE']
                    assert aggregate['source_pointer'] == current
                    bools = {k: v for k, v in expected.items() if type(v) is bool}
                    assert aggregate['true_fields'] == sum(bools.values()) and aggregate['false_fields'] == len(bools) - sum(bools.values())
                    node = {k: v for k, v in node.items() if k != 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE'}
                    assert not set(node) & set(bools)
                    node.update(bools)
                    reference_records.append({'role': role, 'pointer': current, 'kind': 'exact_boolean_aggregate', 'true': sum(bools.values()), 'false': len(bools) - sum(bools.values())})
                assert isinstance(expected, dict), current
                missing = set(expected) - set(node)
                if missing and role == 'shared':
                    # Shared explicitly uses capsules and implicit /core/<topic>
                    # source routes. Missing values are not resident literals.
                    # Verify retained literals below and recover each missing
                    # whole field through its exact pinned-source pointer.
                    node = dict(node)
                    for key in sorted(missing):
                        target = child(current, key)
                        node[key] = {'@': target[len(topic):]}
                        explicit_auxiliary.append({'role': role, 'pointer': target, 'value_sha256_canonical_json': sha(json.dumps(resolve(result,target),ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()), 'scope': 'Nonresident whole field in explicitly documented capsule; recovered from implicit topic source route, not claimed as a resident literal.'})
                assert set(node) == set(expected), (current, sorted(set(expected) - set(node)), sorted(set(node) - set(expected)))
                return {k: restore(v, child(current, k), topic) for k, v in node.items()}
            if isinstance(node, list):
                assert isinstance(expected, list) and len(node) == len(expected), current
                return [restore(v, child(current, i), topic) for i, v in enumerate(node)]
            assert type(node) is type(expected) and node == expected, (current, str(node)[:100], str(expected)[:100])
            return node

        topics = {}
        full_derived_capsules = []
        before = prefix.split('## Exposição canônica integral: fórmulas e derivações', 1)[0]
        for block in before.split('\n### ')[1:]:
            rows = block.splitlines()
            name = rows[0]
            if name not in result['core']:
                continue
            assert name not in topics
            candidates = []
            for line in rows[1:]:
                try:
                    candidates.append(json.loads(line))
                except ValueError:
                    pass
            if not candidates:
                assert name == 'contour_theory' and '/core/contour_theory' in block and 'Síntese derivada' in block
                topics[name] = result['core'][name]
                full_derived_capsules.append({'topic': name, 'scope': 'Explicit prose synthesis with exact source route; recovered full source, prose not certified as source literal.'})
                continue
            assert len(candidates) == 1, name
            p = child('/core', name)
            try:
                topics[name] = restore(decode(candidates[0]), p, p)
                assert topics[name] == result['core'][name]
            except (AssertionError, KeyError, TypeError, ValueError) as exc:
                validation_errors.append({'role': role, 'topic': name, 'error': str(exc)})
                topics[name] = None
        assert set(topics) == set(result['core']) and len(topics) == 422
        packages[role] = {'prefix_sha256': selected['prefix']['sha256'], 'budget': budget, 'topics': len(topics), 'topics_reconstructed_exactly': sum(topics[k] == result['core'][k] for k in topics), 'derived_prose_capsules': full_derived_capsules, 'native_admission_scope': selected['admission_scope']}

    prep = load(A / 'science/haiku_expanded_count/PREPARATION.json')
    assert prep['prefix_sha256'] == selection['selected']['haiku']['prefix']['sha256']
    base = read(prep['expansion_base_receipt'])
    assert sha(base) == prep['expansion_base_sha256']
    for row in prep['selected_whole_topics']:
        assert row['source_sha256'] == result_sha
        value = resolve(result, row['pointer'])
        for deferred in prep['deferred_whole_fields']:
            if deferred['json_pointer'].startswith(row['pointer'] + '/'):
                value = json.loads(json.dumps(value))
                rel = deferred['json_pointer'][len(row['pointer']):]
                parts = rel.split('/')[1:]
                node = value
                for k in parts[:-1]:
                    node = node[k]
                node[parts[-1]] = {'DETAILS_IN_SOURCE': deferred['json_pointer']}
        actual = sha(json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode())
        assert actual == row['resident_value_sha256_canonical_json'], row['topic']
    for row in prep['deferred_whole_fields']:
        value = resolve(result, row['json_pointer'])
        assert row['source_sha256'] == result_sha and len(value) == row['items']
        assert sha(json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()) == row['value_sha256_canonical_json']

    destinations = load(A / 'PROPOSED_DATA_DESTINATIONS.json')
    assert destinations['publication_pending'] and destinations['runtime_python_files_allowed'] == []
    installed_sources = set()
    for row in destinations['files']:
        pincheck(row)
        installed_sources.add(Path(row['path']).resolve())
        assert not any(x in Path(row['path']).parts for x in ['memory_build', 'compat', 'patches'])
        assert not (Path(row['path']).suffix == '.py' and Path(row['path']).name != 'um.py')
        if Path(row['path']).name == 'um.py':
            assert 'NEVER_IMPORT_OR_EXECUTE' in row['purpose']
    for role, package in selection['selected'].items():
        assert Path(package['prefix']['path']).resolve() in installed_sources
        assert Path(package['manifest']['path']).resolve() in installed_sources
    for label, package in selection['rejected'].items():
        if 'prefix' in package:
            pincheck(package['prefix'])
            rc = json.loads(pincheck(package['count_receipt']))
            assert not rc['budget']['ready']
            assert Path(package['prefix']['path']).resolve() not in installed_sources
    assert m['publication_pending'] and delivery['semantic_acceptance'] is False
    changed = [path for path, row in inputs.items() if sha(Path(path).read_bytes()) != row['sha256']]
    assert not changed, changed
    compat = load(W / 'review/READER_COMPAT_R1.json')
    assert compat['verdict'] == 'PASS' and compat['test_count'] == 21
    report = {
        'verdict': 'PASS_WITH_BLOCKS' if not validation_errors else 'FINDINGS',
        'reviewer': 'codex-v394-reviewer', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'task_id': 'app', 'reviewed_submission': app['evidence'],
        'mission_revision': project['receipt']['revision'], 'inputs': inputs,
        'selected_packages': packages, 'expansion_topics': len(prep['selected_whole_topics']),
        'deferred_whole_fields': prep['deferred_whole_fields'],
        'references_checked': reference_records, 'derived_summaries_checked': summary_records,
        'nonresident_whole_fields_recovery': explicit_auxiliary, 'validation_errors': validation_errors,
        'foundation_report_sha256': sha(read(W / 'review/APP_FOUNDATION_R1.json')),
        'reader_compat_report_sha256': sha(read(W / 'review/READER_COMPAT_R1.json')),
        'data_inventory_files': len(destinations['files']),
        'excluded_full_packages_verified': True, 'runtime_baseline_files_unchanged': len(baseline['files']),
        'pending': [
            'PUBLICATION_PENDING: verify immutable public v394 commit and raw bytes, then bind manifests and source URLs.',
            'Two final native count calls after publication/rebinding, for the changed selected Haiku request bytes; no repeats performed by reviewer.',
            'reader_compat is reviewed PASS as staged only; install its two limit changes with the reviewed deployment, preserving all existing guards.',
            'Final actual request admission including activity/history and OpenAI/provider-specific capacity remains a runtime requirement; selected synthetic budgets do not certify arbitrary histories.',
            'Queue preparation awaits its specific automatic-review authorization; no queue acceptance or activation inferred.',
            'Controlled deployment, post-install verification and human/mission acceptances remain separate.'
        ],
        'app_accepted': False, 'deployment_accepted': False, 'ready_for_activation': False,
        'network_calls': 0, 'api_calls': 0, 'native_count_calls': 0, 'science_execution': False,
        'scope': 'Documentary byte/pointer fidelity. Explicit derived capsules are not original source literals. Recoverable fields are not falsely represented as all resident. Reader sizing is an addressed compatibility task, not a new intrinsic reading hardblock.',
    }
    path = W / 'review/FINAL_PREPARATION_REVIEW.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    temp = path.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    if path.exists():
        previous = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as stream:
            stream.write(previous)
        assert backup.read_bytes() == previous
    temp.replace(path)
    print(json.dumps({'verdict': report['verdict'], 'packages': packages, 'errors': validation_errors, 'report_sha256': sha(raw), 'data_files': len(destinations['files'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
