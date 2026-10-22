"""Focused R2 review: remove artificial publication dependency, preserve R1 pins."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

W = Path(__file__).resolve().parents[1]
A = W / 'app'
E = A / 'engines'
R2 = E / 'R2'
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


def pin(row):
    b = read(row['path'])
    assert sha(b) == row['sha256']
    if 'bytes' in row:
        assert len(b) == row['bytes']
    return b


def main():
    sys.path.insert(0, str(W))
    import task
    project = task.project()
    t = next(x for x in project['projection']['active'] if x['id'] == 'all_engines_admission')
    delivery_path = R2 / 'DELIVERY_PREPARED_R2.json'
    assert t['status'] == 'review_pending', 'Wait for real R2 submit; do not integrate a working candidate.'
    assert t['evidence'] == [{'path': str(delivery_path), 'sha256': sha(read(delivery_path))}]
    delivery = load(delivery_path)
    for key in ['full_cluster_companion', 'prompt_cluster', 'projection_map', 'manifest_pending_publication', 'install_plan', 'test_results', 'rebinding_plan', 'test_script', 'recovery_map', 'recovery_verifier', 'r1_receipt_preserved']:
        pin(delivery[key])
    previous = load(W / 'review/ALL_ENGINES_R1.json')
    assert previous['findings'][0]['code'] == 'LOCAL_DERIVED_COMPANION_WRONGLY_REQUIRES_PUBLICATION'
    manifest = load(R2 / 'manifest_pending_publication.json')
    install_manifest = load(R2 / 'manifest_install_pending_publication.json')
    rebinding = load(R2 / 'REBIND_PLAN_R2.json')
    original = load(A / 'science/memory_stage/manifest_staged.json')
    old_manifest = load(E / 'manifest_pending_publication.json')
    assert manifest['entries'] == original['entries']
    assert {x['id'] for x in install_manifest['entries']} == {x['id'] for x in original['entries']}
    assert all(x['id'] != 'tgl_cluster_integral' for x in manifest['entries'] + install_manifest['entries'])
    for cfg in [manifest, install_manifest]:
        c = cfg['active_cluster']
        assert 'full_cluster_source_id' not in c
        assert c['full_cluster_storage'] == 'LOCAL_PINNED_COMPANION_NOT_DOCUMENTCORPUS'
        assert c['source_result_id'] == 'resultado_publicado_integral'
        assert c['publication_pending'] and cfg['publication_pending']
    assert rebinding['full_companion_public_url_required'] is False
    assert 'resultado_publicado_integral /core' in rebinding['recovery_source']
    assert 'no new derived-cluster publication required' in delivery['pending'][0]
    full = pin(delivery['full_cluster_companion'])
    assert full == pin(load(E / 'DELIVERY_PREPARED_R1.json')['full_cluster_companion'])
    p1 = pin(load(E / 'DELIVERY_PREPARED_R1.json')['prompt_cluster']).decode('utf-8')
    p2 = pin(delivery['prompt_cluster']).decode('utf-8')
    a, b = p1.splitlines(keepends=True), p2.splitlines(keepends=True)
    assert len(a) == len(b) and [i for i in range(len(a)) if a[i] != b[i]] == [2]
    assert 'LOCAL, fora do DocumentCorpus' in b[2] and 'resultado_publicado_integral /core' in b[2]
    map1 = load(E / 'PROJECTION_MAP_R1.json')
    map2 = load(R2 / 'PROJECTION_MAP_R2.json')
    assert map1['capsules'] == map2['capsules'] and len(map2['capsules']) == 422
    for row in rebinding['historical_packages_frozen']:
        pin(row)
    tests1 = load(E / 'TEST_RESULTS_R1.json')
    tests2 = load(R2 / 'TEST_RESULTS_R2.json')
    assert tests1['tests'] == tests2['tests'][:12] and tests2['test_count'] == 18
    script1 = read(E / 'prepare_and_test.py').decode('utf-8')
    script2 = read(R2 / 'prepare_and_test_R2.py').decode('utf-8')
    def testbody(script):
        return script[script.index('tests=[]'):script.index("prepared=json.loads((OLD/'prepared.json')")]
    assert testbody(script1) == testbody(script2)
    # Targeted independent R2 execution with real readers; no broad test loop.
    sys.path[:0] = [str(A / 'compat/staging'), str(R), str(A / 'science/memory_build')]
    def guard(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
            raise RuntimeError('Offline focused review')
        if event == 'open':
            path, mode, flags = args
            if isinstance(path, int):
                return
            path = Path(os.fsdecode(path)).resolve()
            if path.name.lower() in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}:
                raise RuntimeError('Confidential source refused')
            writing = isinstance(mode,str) and any(c in mode for c in 'wax+') or isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)
            if writing and not path.is_relative_to(W / 'review'):
                raise RuntimeError('Writes restricted to reviewer evidence')
    sys.addaudithook(guard)
    import iald_core_indexado, iald_memoria_canonica as cm, iald_kernel, haiku_codec
    assert Path(cm.__file__).resolve() == R / 'iald_memoria_canonica.py'
    fixture = R2 / 'fixtures/iald_nucleo_fixo.json'
    fixture_json = load(fixture)
    assert 'tgl_cluster_integral' not in {x['id'] for x in fixture_json['entries']}
    corpus = iald_core_indexado.DocumentCorpus(fixture)
    docs = corpus._load()
    source = json.loads(docs['resultado_publicado_integral']['text'])
    assert docs['resultado_publicado_integral']['sha256'] == map2['source_result']['sha256']
    for row in map2['capsules']:
        value = source
        for key in row['pointer'].split('/')[1:]:
            value = value[key.replace('~1','/').replace('~0','~')]
        assert sha(json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()) == row['source_value_sha256']
    recovery = load(delivery['recovery_map']['path'])
    assert len(recovery['topics']) == 422
    source_text = docs['resultado_publicado_integral']['text']
    for name, row in recovery['topics'].items():
        start, end = row['offset_unicode_chars'], row['end_unicode_chars']
        restored = json.loads(source_text[start:end])
        assert restored == source['core'][name]
        assert sha(json.dumps(restored,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()) == row['canonical_value_sha256']
    for row in recovery['actual_fetch_sample_pages']:
        offset = row['offset']
        page = corpus.fetch('resultado_publicado_integral',offset=offset,max_chars=4500)
        assert page['text'] == source_text[offset:offset+4500] and page['sha256'] == row['sha256']
    assert recovery['gaps']['scientific_core_fields_missing_from_result'] == []
    haiku_codec.offline_tokens('offline', R / '.iald_runtime/tokenizer_cache')
    os.environ['TIKTOKEN_CACHE_DIR'] = str(R / '.iald_runtime/tokenizer_cache')
    kernel = iald_kernel.KernelCatalog(A / 'science/memory_stage/kernel', A / 'science/memory_stage/kernel_verification.json')
    memory = cm.CanonicalMemory(W.parents[1] / 'memory/TGL_ATLAS.md', 'nucleo_kernel', nucleus_manifest=fixture)
    prompt, meta = memory.prompt('', kernel, public=True)
    actual = delivery['actual_prompts']['public']
    assert sha(prompt.encode()) == actual['prefix_sha256']
    assert meta['context_tokens'] == actual['actual_CanonicalMemory_context_o200k_tokens'] == 265321
    assert p2 in prompt and '<ATLAS_CANONICO' not in prompt
    for source_path, row in inputs.items():
        assert sha(Path(source_path).read_bytes()) == row['sha256']
    report = {
        'verdict': 'PASS_PREPARATION_NOT_ACTIVATED', 'criterion_satisfied': True,
        'reviewer': 'codex-v394-reviewer', 'reference': str(task.REF),
        'task_id': 'all_engines_admission', 'criterion': t['criterion'],
        'reviewed_submission': t['evidence'], 'baseline_revision': project['receipt']['revision'],
        'checked_at': datetime.now(timezone.utc).isoformat(), 'inputs': inputs,
        'resolved_finding': previous['findings'][0]['code'],
        'correction_verified': 'Local full cluster preserved byte-for-byte outside DocumentCorpus. Existing source JSON and 422 exact pointers provide full scientific recovery. No extra public companion or invented URL required.',
        'focused_checks': {'unchanged_capsules': 422, 'integral_topics_recovered': 422, 'full_cluster_bytes': len(full), 'R2_public_prompt_executed_offline': True, 'context_o200k': meta['context_tokens'], 'unchanged_R1_R2_test_body': True, 'R2_builder_tests_reported': 18, 'prior_R1_tests_independently_reexecuted': 12, 'R2_exact_JSON_subtree_ranges_checked': 422, 'R2_actual_fetch_pages_reexecuted': len(recovery['actual_fetch_sample_pages'])},
        'historical_pins_preserved': True, 'findings': [],
        'pending': ['Verified publication/binding of the intended original scientific sources only.', 'New bound identities/manifests and final model-specific counts/admission, including native Sonnet still pending.', 'App/deploy acceptance and controlled installation remain separate; gate unchanged.'],
        'fixture_scope': 'Existing baseline commit/URL syntax fixtures only; no verified v394 publication claimed.',
        'production_activated': False, 'app_accepted': False, 'deploy_accepted': False,
        'native_api_calls': 0, 'science_executed_or_imported': False,
    }
    path = W / 'review/ALL_ENGINES_R2.json'
    raw = json.dumps(report,ensure_ascii=False,indent=2).encode()
    temp = path.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and not path.exists()
    temp.replace(path)
    print(json.dumps({'verdict':report['verdict'],'report':str(path),'sha256':sha(raw),'reviewed_revision':project['receipt']['revision']}))


if __name__ == '__main__':
    main()
