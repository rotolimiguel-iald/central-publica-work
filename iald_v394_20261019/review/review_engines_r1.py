"""Independent offline engines review, pinned capsules and isolated test replay."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, importlib.util, json, os, re, sys
from types import SimpleNamespace

W = Path(__file__).resolve().parents[1]
A = W / 'app'
S = A / 'science'
OLD = S / 'memory_stage'
SOURCE = A / 'engines'
E = W / 'review/engines_replay_r1'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(path):
    path = Path(path)
    raw = path.read_bytes()
    inputs[str(path)] = {'sha256': sha(raw), 'bytes': len(raw)}
    return raw


def load(path):
    return json.loads(read(path))


def checkpin(row):
    raw = read(row['path'])
    assert sha(raw) == row['sha256']
    if 'bytes' in row:
        assert len(raw) == row['bytes']
    return raw


def save(path, raw):
    path = Path(path).resolve()
    assert path.is_relative_to(E.resolve())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
    assert path.read_bytes() == raw


def write(path, value):
    save(path, json.dumps(value, ensure_ascii=False, indent=2).encode())


def capsules(text, marker, names):
    end = text.index('\n' + marker)
    headers = [m for m in re.finditer(r'(?m)^### ([^\n]+)\n', text[:end]) if m.group(1) in names]
    result = {}
    for index, match in enumerate(headers):
        name = match.group(1)
        assert name not in result
        stop = headers[index + 1].start() if index + 1 < len(headers) else end
        result[name] = text[match.end():stop].strip()
    return result


def main():
    sys.path.insert(0, str(W))
    import task
    project = task.project()
    requirement = next(t for t in project['projection']['active'] if t['id'] == 'all_engines_admission')
    assert requirement['status'] == 'review_pending'
    delivery_path = SOURCE / 'DELIVERY_PREPARED_R1.json'
    assert requirement['evidence'] == [{'path': str(delivery_path), 'sha256': sha(read(delivery_path))}]
    delivery = load(delivery_path)
    for key in ['full_cluster_companion', 'prompt_cluster', 'projection_map', 'manifest_pending_publication', 'install_plan', 'test_results', 'rebinding_plan', 'test_script']:
        checkpin(delivery[key])
    mapping = load(delivery['projection_map']['path'])
    manifest = load(delivery['manifest_pending_publication']['path'])
    result_raw = checkpin(mapping['source_result'])
    result = json.loads(result_raw)
    projection = checkpin(mapping['projected_cluster']).decode('utf-8')
    full = checkpin(mapping['full_cluster'])
    assert full == read(OLD / 'TGL_CLUSTER_v394.md')
    previous_review = load(W / 'review/FINAL_PREPARATION_REVIEW.json')
    selection = load(A / 'PACKAGE_SELECTION.json')
    frozen_paths = [A / 'DELIVERY_PREPARED.json', A / 'PACKAGE_SELECTION.json']
    for role, package in selection['selected'].items():
        assert package['prefix']['sha256'] == previous_review['selected_packages'][role]['prefix_sha256']
        for key in ['prefix', 'manifest', 'count_receipt']:
            checkpin(package[key])
            frozen_paths.append(Path(package[key]['path']))
    frozen = [{'path': str(p), 'sha256': sha(read(p))} for p in frozen_paths]
    runtime_rows = load(A / 'runtime_baseline.json')['files']
    for row in runtime_rows:
        checkpin(row)
    runtime = {row['path']: row['sha256'] for row in runtime_rows if Path(row['path']).suffix == '.py'}
    shared = read(OLD / 'shared_prefix.md').decode('utf-8')
    assert sha(shared.encode()) == selection['selected']['shared']['prefix']['sha256']

    # Independent capsule extraction: compare every byte other than an added
    # explicit source anchor. Inherits reviewed shared literals/formulas/scopes.
    marker = '## Exposição canônica integral: fórmulas e derivações'
    source_capsules = capsules(shared, marker, result['core'])
    projected_capsules = capsules(projection, marker, result['core'])
    assert set(source_capsules) == set(projected_capsules) == set(result['core'])
    rows = {row['topic']: row for row in mapping['capsules']}
    assert len(rows) == len(mapping['capsules']) == len(result['core']) == 422
    anchors_added = 0
    for name, body in source_capsules.items():
        ptr = '/core/' + name.replace('~', '~0').replace('/', '~1')
        row = rows[name]
        added = '/core/' + name not in body
        expected = 'Fonte: resultado_publicado_integral ' + ptr + '\n' + body if added else body
        assert projected_capsules[name] == expected
        assert row['pointer'] == ptr and row['explicit_source_anchor_added'] is added
        assert sha(body.encode()) == row['original_shared_capsule_sha256']
        assert sha(expected.encode()) == row['capsule_sha256']
        original_value = json.dumps(result['core'][name], ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()
        assert sha(original_value) == row['source_value_sha256']
        anchors_added += added
    expo = shared.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    assert projection.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0] == expo
    heading = shared.index('DICIONÁRIO DE INDICADORES LITERAIS\n')
    legend_end = shared.index('\n', heading + len('DICIONÁRIO DE INDICADORES LITERAIS\n'))
    assert shared[:legend_end].replace('### nome →', 'Tópico nome →') in projection
    assert manifest['publication_pending'] and manifest['active_cluster']['publication_pending']
    assert manifest['active_cluster']['sha256'] == sha(projection.encode())
    assert manifest['active_cluster']['full_cluster_sha256'] == sha(full)
    assert manifest['active_cluster']['full_cluster_source_id'] == 'tgl_cluster_integral'
    companion = next(row for row in manifest['entries'] if row['id'] == 'tgl_cluster_integral')
    assert companion['public_sha256'] == sha(full) and companion['url'] == ''
    script = checkpin(delivery['test_script']).decode('utf-8')
    supplied_tests = load(delivery['test_results']['path'])
    for key in ['CanonicalMemory_implementation', 'cluster_loader_implementation']:
        checkpin(supplied_tests[key])
    for row in supplied_tests['reader_shims']:
        checkpin(row)
    # Isolated replay uses actual runtime CanonicalMemory and the two already
    # accepted reader candidates. All output redirected to reviewer fixtures.
    E.mkdir()
    sys.path[:0] = [str(A / 'compat/staging'), str(R), str(S / 'memory_build')]

    def guard(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
            raise RuntimeError('Offline engines review')
        if event == 'open':
            p, mode, flags = args
            if isinstance(p, int):
                return
            p = Path(os.fsdecode(p)).resolve()
            if p.name.lower() in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}:
                raise RuntimeError('Confidential source refused')
            writing = isinstance(mode, str) and any(x in mode for x in 'wax+') or isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            if writing and not p.is_relative_to((W / 'review').resolve()):
                raise RuntimeError('Write outside reviewer files refused')
    sys.addaudithook(guard)
    import iald_memoria_canonica as cm, iald_cluster, iald_release_binding, iald_native_memory
    import iald_kernel, iald_estado_publicado, iald_core_indexado, iald_fontes_publicas, iald_app_memory
    import haiku_codec as codec
    assert Path(cm.__file__).resolve() == (R / 'iald_memoria_canonica.py').resolve()
    assert Path(iald_cluster.__file__).resolve() == (R / 'iald_cluster.py').resolve()
    assert Path(iald_estado_publicado.__file__).resolve().parent == (A / 'compat/staging').resolve()
    codec.offline_tokens('offline', R / '.iald_runtime/tokenizer_cache')
    os.environ['TIKTOKEN_CACHE_DIR'] = str(R / '.iald_runtime/tokenizer_cache')
    baseline = load(R / 'iald_nucleo_fixo.json')
    fixture = copy.deepcopy(manifest)
    fixture['offline_fixture_not_publication'] = True
    fixture['active_cluster']['commit'] = baseline['active_cluster']['commit']
    for entry in fixture['entries']:
        old = next((x for x in baseline['entries'] if x['id'] == entry['id']), baseline['entries'][0])
        if not entry.get('url'):
            entry['url'] = old['url']
    for key in ['program', 'seal', 'result', 'proof_manifest']:
        fixture['published_evidence'][key]['url'] = baseline['published_evidence'][key]['url']
    for entry in fixture['published_evidence']['hypothesis_sources']:
        entry['url'] = next(x['url'] for x in baseline['published_evidence']['hypothesis_sources'] if x['id'] == entry['id'])
    fixture_path = E / 'fixtures/iald_nucleo_fixo.json'
    write(fixture_path, fixture)
    write(E / 'manifest_pending_publication.json', manifest)
    catalog = iald_kernel.KernelCatalog(OLD / 'kernel', OLD / 'kernel_verification.json')
    identity = iald_release_binding.load_release(fixture_path, source_sha=catalog.source_sha).identity
    oldidentity = load(OLD / 'prepared.json')['deployment_identity']
    assert identity != oldidentity
    section = script[script.index('tests=[]'):script.index("prepared=json.loads((OLD/'prepared.json')")]
    env = dict(globals(), manifest=manifest, baseline=baseline, fixture=fixture, fixture_path=fixture_path,
               catalog=catalog, identity=identity, oldidentity=oldidentity, projection=projection, full=full,
               frozen=frozen, runtime=runtime, cm=cm, iald_cluster=iald_cluster,
               iald_release_binding=iald_release_binding, iald_native_memory=iald_native_memory,
               iald_kernel=iald_kernel, iald_estado_publicado=iald_estado_publicado,
               iald_core_indexado=iald_core_indexado, iald_fontes_publicas=iald_fontes_publicas,
               iald_app_memory=iald_app_memory, codec=codec, data=SOURCE / 'data')
    exec(compile(section, '<isolated-engines-test-replay>', 'exec'), env)
    assert env['tests'] == supplied_tests['tests'] and len(env['tests']) == 12
    assert env['outputs'] == supplied_tests['actual_prompts'] == delivery['actual_prompts']
    for source, row in inputs.items():
        assert sha(Path(source).read_bytes()) == row['sha256'], source
    report = {
        'verdict': 'PASS_OFFLINE_PREPARATION_WITH_SCOPE', 'criterion_satisfied': True,
        'reviewer': 'codex-v394-reviewer', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'task_id': 'all_engines_admission',
        'criterion': requirement['criterion'], 'reviewed_submission': requirement['evidence'],
        'mission_revision': project['receipt']['revision'], 'inputs': inputs,
        'review_script': {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())},
        'counts': {'topics': len(rows), 'anchors_added': anchors_added, 'full_cluster_bytes': len(full), 'projection_bytes': len(projection.encode()), 'tests_reexecuted': 12},
        'projection_fidelity': 'Every capsule, dictionary, boolean aggregation legend and exposition preserved from independently reviewed shared package; only explicit source anchors added. All original fields remain in the pinned source JSON and full companion. Resident vs recoverable distinction retained.',
        'actual_prompts': env['outputs'], 'tests_reexecuted': env['tests'],
        'new_fixture_identity': identity, 'historical_identity': oldidentity,
        'frozen_packages': frozen, 'findings': [],
        'limitations': [
            'PASS and acceptance concern preparation offline only, as explicitly scoped by the human reviewer assignment.',
            'URLs and commit used by tests are v392 syntax fixtures, never evidence of v394 publication.',
            'Native Sonnet count and final provider admission remain unmeasured; o200k and native-wire byte estimates retain their labels.',
            'New active-cluster identity requires new bound manifests/provenance and final public-byte measurements. Historic Haiku/shared receipts are unchanged and cannot be silently rebound.',
            'App/deploy remain pending publication, final binding/counts and controlled installation; no gate/science claim changed.'
        ],
        'app_accepted': False, 'deploy_accepted': False, 'production_installed': False,
        'api_calls': 0, 'native_count_calls': 0, 'science_executed_or_imported': False,
    }
    destination = W / 'review/ALL_ENGINES_R1.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    save(destination, raw) if destination.is_relative_to(E) else None
    temp = destination.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and not destination.exists()
    temp.replace(destination)
    print(json.dumps({'verdict': report['verdict'], 'counts': report['counts'], 'report_path': str(destination), 'report_sha256': sha(raw)}))


if __name__ == '__main__':
    main()
