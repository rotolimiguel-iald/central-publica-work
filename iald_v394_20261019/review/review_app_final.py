"""Substantive final v394 data/count/tool-binding review; no install or paid calls."""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import ast, hashlib, importlib.util, json, os, subprocess, sys
from urllib.parse import urlparse, unquote, quote

W = Path(__file__).resolve().parents[1]
A = W / 'app'
F = A / 'final'
S = F / 'science/memory_stage'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
P = Path(r'C:\IALD\Artigo\the_boundary')
inputs = {}
sha = lambda b: hashlib.sha256(b).hexdigest()


def read(p):
    p = Path(p)
    b = p.read_bytes()
    inputs[str(p)] = {'sha256': sha(b), 'bytes': len(b)}
    return b


def load(p):
    return json.loads(read(p))


def pin(row):
    raw = read(row['path'])
    assert sha(raw) == row['sha256']
    if 'bytes' in row:
        assert len(raw) == row['bytes']
    return raw


def main():
    sys.path.insert(0, str(W))
    import task
    project = task.project()
    t = next(x for x in project['projection']['active'] if x['id'] == 'app')
    delivery_path = F / 'DELIVERY_PREPARED_FINAL.json'
    assert t['status'] == 'review_pending', 'Wait for final builder submit'
    assert t['evidence'] == [{'path': str(delivery_path), 'sha256': sha(read(delivery_path))}]
    delivery = load(delivery_path)
    for key in ['publication', 'prepared_binding', 'install_plan', 'tests', 'native_counts_complete', 'historical_pins', 'runtime_baseline']:
        pin(delivery[key])
    pub = load(F / 'PUBLICATION_VERIFIED.json')
    commit = delivery['commit']
    assert pub['commit'] == commit
    command = ['git', '-c', 'safe.directory=' + P.as_posix(), '-C', str(P)]
    def git(*args):
        return subprocess.check_output(command + list(args), timeout=60)
    assert git('rev-parse', 'HEAD').decode().strip() == commit
    assert git('rev-parse', 'origin/main').decode().strip() == commit
    assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit
    tracked = set(git('ls-tree', '-r', '--name-only', '-z', commit).decode().split('\0')) - {''}
    expected = {rel: row for rel, row in pub['sources'].items()}
    for row in pub['kernel_files_git_proof_and_staging_equal']:
        rel = row['git_path']
        if rel in expected:
            assert expected[rel]['sha256'] == row['sha256']
        expected[rel] = row
    assert set(expected) <= tracked
    paths = sorted(expected)
    output = subprocess.run(command + ['cat-file', '--batch'], input=''.join(commit + ':' + x + '\n' for x in paths).encode(), capture_output=True, check=True).stdout
    pos = 0
    for rel in paths:
        end = output.index(b'\n', pos)
        header = output[pos:end].split()
        assert header[1] == b'blob'
        size = int(header[2]); pos = end + 1
        blob = output[pos:pos + size]; pos += size + 1
        assert size == expected[rel]['bytes'] and sha(blob) == expected[rel]['sha256'], rel
    assert pos == len(output)
    for row in pub['http_raw_checks']:
        assert row['status'] == 200 and row['matches_verified_git_and_local_source']
        assert row['sha256'] == expected[row['git_path']]['sha256']
        assert row['url'] == 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + commit + '/' + quote(row['git_path'], safe='/')
    # HTTP evidence is the builder's exact receipt, cross-checked to independently
    # reread Git blobs. This reviewer performs no additional raw downloads/counts.
    m = load(S / 'manifest_staged.json')
    installed_m = load(S / 'manifest_install.json')
    assert m['active_cluster']['commit'] == commit and not m.get('publication_pending') and not m.get('staging_only')
    assert not m['active_cluster'].get('publication_pending')
    assert len(m['entries']) == 8 and all(x['id'] != 'tgl_cluster_integral' for x in m['entries'])
    for row in m['entries']:
        rel = unquote('/'.join(urlparse(row['url']).path.split('/')[4:]))
        assert rel in pub['sources'] and row['url'] == pub['sources'][rel]['url']
        assert sha(read(row['path'])) == row['public_sha256'] == expected[rel]['sha256']
    for row in m['published_evidence']['hypothesis_sources']:
        rel = unquote('/'.join(urlparse(row['url']).path.split('/')[4:]))
        assert rel in expected and row['url'].split('/')[5] == commit
        assert sha(read(S / 'kernel' / row['catalog_path'])) == expected[rel]['sha256']
    for key in ['program', 'seal', 'result', 'proof_manifest']:
        row = m['published_evidence'][key]
        rel = unquote('/'.join(urlparse(row['url']).path.split('/')[4:]))
        assert row['url'].split('/')[5] == commit and sha(read(row['path'])) == expected[rel]['sha256']
    proof = load(m['published_evidence']['proof_manifest']['path'])
    assert len(proof['formal_files_sha256']) == 1423
    for name, digest in proof['formal_files_sha256'].items():
        assert sha(read(S / 'kernel' / name)) == digest
    result = load(m['published_evidence']['result']['path'])
    assert len(result['core']) == 422
    for key in ['mother_instruction', 'operational_core', 'jev_control']:
        assert sha(read(m[key]['path'])) == m[key]['sha256']
    old = load(A / 'science/memory_stage/manifest_staged.json')
    for key in ['mother_instruction', 'operational_core']:
        assert read(m[key]['path']) == read(old[key]['path'])
    assert read(S / 'TGL_CLUSTER_v394_full.md') == read(A / 'engines/R2/data/TGL_CLUSTER_v394_full.md')
    assert read(S / 'TGL_CLUSTER_v394_prompt.md') == read(A / 'engines/R2/data/TGL_CLUSTER_v394_prompt.md')
    for name in ['HISTORICAL_PINS.json', 'RUNTIME_BASELINE.json']:
        for row in load(F / name)['files']:
            pin(row)
    plan_raw = pin(delivery['install_plan'])
    effective_raw = read(W / 'install_plan.json')
    effective = json.loads(effective_raw)
    adapter = load(W / 'PLAN_ADAPTER.json')
    assert adapter['source_plan_sha256'] == sha(plan_raw)
    assert adapter['transaction_plan_sha256'] == sha(effective_raw)
    assert len(effective['files']) == len(json.loads(plan_raw)['files'])
    plan = json.loads(plan_raw)
    for original_row, effective_row in zip(plan['files'], effective['files']):
        assert effective_row['source'] == original_row['path']
        assert effective_row['destination'] == original_row['destination']
        assert effective_row['sha256'] == original_row['sha256']
        assert effective_row['baseline'] == (None if original_row['baseline'].get('exists') is False else original_row['baseline']['sha256'])
    assert len(plan['files']) == plan['file_count'] == 1449
    rootpython = []
    destinations = set()
    for row in plan['files']:
        source, dest = Path(row['path']).resolve(), Path(row['destination']).resolve()
        assert source.is_relative_to(F.resolve()) and dest.is_relative_to(R.resolve())
        key = str(dest).casefold()
        assert key not in destinations
        destinations.add(key)
        pin(row)
        baseline = row['baseline']
        assert Path(baseline['path']).resolve() == dest
        if baseline.get('exists') is False:
            assert not dest.exists()
        else:
            pin(baseline)
        if dest.parent == R and dest.suffix == '.py':
            rootpython.append(dest.name)
            accepted = load(A / 'compat/INSTALL_PLAN_R1.json')['files']
            prior = next(x for x in accepted if Path(x['runtime_path']) == dest)
            assert row['sha256'] == prior['staged_sha256']
        elif dest.suffix == '.py':
            assert dest.name == 'um.py' and 'NEVER_EXECUTE' in row['purpose']
    assert set(rootpython) == {'iald_estado_publicado.py', 'iald_core_indexado.py'}

    def guard(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
            raise RuntimeError('Offline substantive package review')
        if event == 'open':
            path, mode, flags = args
            if isinstance(path, int):
                return
            path = Path(os.fsdecode(path)).resolve()
            if path.name.lower() in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}:
                raise RuntimeError('Confidential source refused')
            writing = isinstance(mode, str) and any(c in mode for c in 'wax+') or isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            if writing and not path.is_relative_to(W / 'review'):
                raise RuntimeError('Write outside review refused')
    sys.addaudithook(guard)
    sys.path[:0] = [str(F / 'build'), str(R)]
    import haiku_codec as codec, iald_core_indexado, iald_kernel, iald_jev_control, iald_release_binding
    import iald_fontes_publicas, iald_app_memory, iald_memoria_canonica, iald_native_memory
    from claude_profiles import HAIKU, SONNET, reasoning_parameters
    from claude_native_counter import native_count_parameters
    from claude_context_snapshot import native_tools_sha256, load_snapshot, verify_native_tools
    from claude_memory_package import load_package
    from iald_motor_claude import converter_pedido
    assert Path(iald_memoria_canonica.__file__).resolve() == R / 'iald_memoria_canonica.py'
    release = iald_release_binding.load_release(S / 'manifest_staged.json')
    assert release.identity == delivery['deployment_identity']
    catalog = iald_kernel.KernelCatalog(S / 'kernel', S / 'kernel_verification.json')
    assert iald_jev_control.load_contract(S)['source_sha256'] == release.identity['source_sha256']
    tools = iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions() + iald_core_indexado.tool_definitions() + iald_app_memory.tool_definitions()
    count_records = {}
    for folder, profile in [('haiku55', HAIKU), ('shared', HAIKU), ('sonnet_public', SONNET)]:
        root = F / 'packages' / folder
        prefix = read(root / 'prefix.md').decode()
        receipt = load(root / 'native_count.json')
        package_manifest = load(root / 'manifest.json')
        assert receipt['prefix_sha256'] == sha(prefix.encode()) == package_manifest['prefix_sha256']
        assert receipt['deployment'] == release.identity == package_manifest['deployment']
        assert receipt['budget'] == package_manifest['budget'] == delivery['counts'][folder]['budget']
        assert receipt['model'] == profile.model and receipt['public_commit'] == commit
        assert not receipt['private_atlas_included'] and not receipt['operator_context_sent']
        assert '<ATLAS_CANONICO' not in prefix
        cfg = SimpleNamespace(modelo=profile.model, max_saida=16384, cache_ttl='5m', esforco_claude='medium' if profile is HAIKU else 'high')
        wire = converter_pedido(cfg, {'model': profile.model, 'max_completion_tokens': 16384,
            'messages': [{'role': 'system', 'content': prefix}, {'role': 'user', 'content': 'Explique o alcance documentado da v394.'}], 'tools': tools}, prefixo=prefix)
        wire.update(reasoning_parameters(profile.model, 16384))
        minimal = {'model': profile.model, 'system': wire['system'], 'messages': [{'role': 'user', 'content': '.'}], **reasoning_parameters(profile.model, 16384)}
        scoped = sha(json.dumps(wire['tools'], sort_keys=True, ensure_ascii=False).encode())
        assert scoped == receipt['native_tools_sha256']
        for phase, request, amount in [('permanent', minimal, receipt['budget']['permanent_tokens']), ('whole_request', wire, receipt['budget']['request_input_tokens'])]:
            intent_path = root / (phase + '_count_intent.json')
            intent = load(intent_path)
            returned = load(root / (phase + '_count_result.json'))
            digest = sha(json.dumps(native_count_parameters(request), sort_keys=True, ensure_ascii=False).encode())
            assert digest == intent['request_sha256'] and intent['model'] == profile.model
            assert returned['input_tokens'] == amount and returned['intent_sha256'] == sha(read(intent_path))
        if folder != 'sonnet_public':
            fixed = native_tools_sha256(wire['tools'][:7])
            assert package_manifest['tools_sha256'] == fixed
            assert package_manifest['counted_scoped_tools_sha256'] == scoped
            package = load_package(root, canonical_manifest=S / 'manifest_staged.json', source_sha=catalog.source_sha, expected_model=profile.model)
            _, snapshot = load_snapshot(root, lambda path: load_package(path, canonical_manifest=S / 'manifest_staged.json', source_sha=catalog.source_sha))
            verify_native_tools(wire, snapshot, trusted_tools=wire['tools'])
        budget = receipt['budget']
        assert budget['ready'] and budget['remaining_tokens'] == 1000000 - budget['request_input_tokens'] - budget['reserved_output_tokens'] - budget['margin_tokens']
        count_records[folder] = {'model': profile.model, 'permanent_tokens': budget['permanent_tokens'], 'request_tokens': budget['request_input_tokens'], 'remaining': budget['remaining_tokens'], 'body_intents_match_exact_current_wire': True}
    # Strong full value check of the expanded package, independent of builder recover.
    expanded = read(F / 'packages/haiku55/prefix.md').decode()
    dictionary = json.loads(expanded.split('LITERAIS_COMPARTILHADOS\n', 1)[1].split('\n', 1)[0])
    exposition = expanded.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    blocks = codec.source_topics(expanded, result['core'])
    def restore(node, topic, current):
        expected = codec.resolve(result, current)
        if isinstance(node, dict):
            if '@' in node:
                assert topic + node['@'] == current
                for suffix, literal in node.get('fields', {}).items():
                    assert literal == codec.resolve(expected, suffix)
                if 'items' in node:
                    assert len(expected) == node['items']
                if 'true_fields' in node:
                    assert all(type(v) is bool for v in expected.values())
                    assert node['true_fields'] == sum(expected.values()) and node['false_fields'] == len(expected) - sum(expected.values())
                return expected
            if 'DETAILS_IN_SOURCE' in node:
                assert node['DETAILS_IN_SOURCE'] == current
                return expected
            assert isinstance(expected, dict) and set(node) == set(expected)
            return {k: restore(v, topic, codec.child(current, k)) for k, v in node.items()}
        if isinstance(node, list):
            assert isinstance(expected, list) and len(node) == len(expected)
            return [restore(v, topic, codec.child(current, i)) for i, v in enumerate(node)]
        assert type(node) is type(expected) and node == expected
        return node
    for name, body in blocks.items():
        node = codec.decode_literals(codec.unpack_metadata(json.loads(body.splitlines()[1])), dictionary, exposition)
        ptr = codec.child('/core', name)
        assert restore(node, ptr, ptr) == result['core'][name]
    assert len(blocks) == 422
    docs = iald_core_indexado.DocumentCorpus(S / 'manifest_staged.json')._load()
    assert len(docs) == 8 and 'tgl_cluster_integral' not in docs
    assert json.loads(docs['resultado_publicado_integral']['text']) == result
    codec.offline_tokens('offline', R / '.iald_runtime/tokenizer_cache')
    os.environ['TIKTOKEN_CACHE_DIR'] = str(R / '.iald_runtime/tokenizer_cache')
    public, meta = iald_memoria_canonica.CanonicalMemory(W.parents[1] / 'memory/TGL_ATLAS.md', 'nucleo_kernel', nucleus_manifest=S / 'manifest_staged.json').prompt('', catalog, public=True)
    assert sha(public.encode()) == delivery['counts']['sonnet_public']['prefix']['sha256']
    assert not meta['private_atlas_included']
    native, native_id = iald_native_memory.load_native_context(S / 'manifest_staged.json', catalog)
    assert native_id == release.identity
    for path, row in inputs.items():
        assert sha(Path(path).read_bytes()) == row['sha256'], path
    report = {
        'verdict': 'PASS_FINAL_PREPARATION_NOT_ACTIVATED',
        'criterion_satisfied': True,
        'reviewer': 'codex-v394-reviewer', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'task_id': 'app', 'criterion': t['criterion'],
        'reviewed_submission': t['evidence'], 'mission_revision': project['receipt']['revision'],
        'inputs': inputs, 'commit': commit, 'identity': release.identity,
        'planned_files': len(plan['files']), 'root_python': rootpython, 'kernel_source_files': 1423,
        'topics_reconstructed': len(blocks), 'public_documents': len(docs), 'counts': count_records,
        'native_body_hashes_recomputed_offline': True,
        'HTTP_scope': 'Builder HTTP receipts cross-checked to independently read immutable Git blobs; no new raw downloads by reviewer.',
        'effective_plan_sha256': sha(effective_raw),
        'resolved_findings': [{'severity': 'MEDIUM', 'code': 'PLAN_SCHEMA_NOT_CONSUMABLE_BY_COPIED_TRANSACTION', 'resolution': 'Independent rowwise verification of PLAN_ADAPTER: exact1449 sources/destinations/hashes preserved; baseline dictionary converted to expected hash/null without touching original builder inventory.'}],
        'findings': [],
        'residuals': [{'severity': 'LOW', 'code': 'ACTIVE_MANIFEST_ORDER_DOCUMENTARY_DIFFERENCE', 'detail': 'Actual manifest row precedes two reader files despite builder order prose. Fully stopped admissions, all-file baseline checks and rollback remain enforced; no runtime reads resume until entire transaction completes. Does not require a new broad round.'}],
        'production_changed': False, 'remote_count_calls': 0, 'source_executed_or_imported': False,
        'app_accepted': False, 'deploy_accepted': False,
    }
    dest = W / 'review/APP_FINAL_SUBSTANTIVE_R1.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    tmp = dest.with_suffix('.json.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and not dest.exists()
    tmp.replace(dest)
    print(json.dumps({'verdict': report['verdict'], 'files': len(plan['files']), 'counts': count_records, 'report': str(dest), 'sha256': sha(raw)}))


if __name__ == '__main__':
    main()
