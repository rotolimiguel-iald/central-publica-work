"""Read actual installed hashes/backups/processes and effective queue; no mutation."""
from pathlib import Path
from datetime import datetime, timezone
from contextlib import closing
import hashlib, http.client, json, os, sqlite3, sys

W = Path(__file__).resolve().parents[1]
R = Path(r'C:\IALD\projetos_pyhton\IALD')
BASE = W.parents[1] / 'Chatgpt/IALD_ORQUESTRACAO_20260923'
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(p):
    p = Path(p); b = p.read_bytes()
    inputs[str(p)] = {'sha256': sha(b), 'bytes': len(b)}
    return b


def load(p):
    return json.loads(read(p))


def main():
    sys.path.insert(0, str(W))
    import task
    p = task.project()
    t = next(x for x in p['projection']['active'] if x['id'] == 'deploy')
    assert t['status'] == 'review_pending' and t['submitted_by'] != 'codex-v394-reviewer'
    for row in t['evidence']:
        assert sha(read(row['path'])) == row['sha256']
    reviewed = load(W / 'validation/review_final.json')
    plan = load(W / 'install_plan.json')
    dep = load(W / 'deployment.json')
    active = load(W / 'ACTIVATION_RESULT.json')
    intent = load(W / 'ACTIVATION_INTENT.json')
    qa = load(W / 'queue_activation.json')
    restart = load(W / 'restart.json')
    maintenance = load(W / 'maintenance.json')
    installed = load(W / 'installed_verification.json')
    qe = load(W / 'queue_effective_generation.json')
    assert dep['plan_sha256'] == reviewed['plan_sha256'] == sha(read(W / 'install_plan.json')) == active['app_plan_sha256'] == intent['plan_sha256']
    assert len(plan['files']) == len(dep['files']) == installed['files_verified'] == 1449
    for row in plan['files']:
        dest = Path(row['destination']); now = read(dest)
        assert sha(now) == row['sha256'] == dep['files'][str(dest)]
        if row['baseline'] is not None and row['baseline'] != row['sha256']:
            assert sha(read(dep['backups'][str(dest)])) == row['baseline']
    assert len(dep['backups']) == 7
    for key, name in [('transaction_sha256','transaction.py'),('maintenance_sha256','maintenance.py'),('deploy_controlled_sha256','deploy_controlled.py'),('activation_sha256','activate_v394.py'),('verify_installed_sha256','verify_installed_v394.py')]:
        assert sha(read(W / name)) == reviewed[key]
    pointer = load(BASE / 'state/canonical_memory/ACTIVE.json')
    queue_prepared = load(W / 'queue/R3/DELIVERY_PREPARED_R3.json')
    assert pointer == qa['pointer'] == active['queue']['pointer']
    assert pointer['generation'] == qe['generation'] == queue_prepared['generation']
    assert pointer['release'] == 'v394' and pointer['manifest_sha256'] == queue_prepared['manifest']['sha256']
    target = Path(queue_prepared['stagedtarget'])
    assert sha(read(target / 'manifest.json')) == pointer['manifest_sha256']
    assert restart['status'] == 'PASS' and restart['http_status'] == 200
    for key in ['old_web_pid','supervisor_pid','supervisor_created']:
        assert restart[key] == maintenance[key]
    import psutil
    web = psutil.Process(restart['new_web_pid']); parent = web.parent()
    assert parent.pid == restart['supervisor_pid'] and parent.create_time() == restart['supervisor_created']
    assert parent.status() != psutil.STATUS_STOPPED and web.status() != psutil.STATUS_STOPPED
    assert any(Path(x).name == 'iald_web_server.py' for x in web.cmdline())
    assert any(Path(x).name == 'start_iald_web.ps1' for x in parent.cmdline())
    conn = http.client.HTTPConnection('127.0.0.1', 8082, timeout=10)
    try:
        conn.request('GET', '/login'); response = conn.getresponse(); response.read()
        assert response.status == 200
    finally:
        conn.close()
    # Only pure installed loaders; cached tokenizer configured before any prompt.
    os.environ['TIKTOKEN_CACHE_DIR'] = str(R / '.iald_runtime/tokenizer_cache')
    assert Path(os.environ['TIKTOKEN_CACHE_DIR']).is_dir()
    sys.path.insert(0, str(R))
    from iald_release_binding import load_release
    from iald_kernel import KernelCatalog
    from claude_memory_package import load_package
    from iald_jev_control import load_contract
    from iald_native_memory import load_native_context
    manifest = R / 'iald_nucleo_fixo.json'; config = load(manifest)
    catalog = KernelCatalog(config['active_cluster']['kernel_bundle'], config['active_cluster']['kernel_verification'])
    release = load_release(manifest, source_sha=catalog.source_sha)
    assert release.identity == installed['identity'] and release.identity['release'] == 'v394'
    assert config['active_cluster']['commit'] == installed['public_commit']
    assert load_contract(R)['source_sha256'] == release.identity['source_sha256']
    full = load_package(R / '.iald_runtime/haiku55', canonical_manifest=manifest, source_sha=catalog.source_sha)
    shared = load_package(R / '.iald_runtime/haiku', canonical_manifest=manifest, source_sha=catalog.source_sha)
    assert full.measurement.permanent_tokens == installed['haiku_permanent_tokens'] == 879526
    assert len(shared.prefix.encode()) == installed['shared_prefix_bytes']
    native, native_id = load_native_context(manifest, catalog)
    assert native_id == release.identity and len(native.encode()) == installed['native_prefix_bytes']
    sys.path.insert(0, str(BASE))
    from iald_orchestrator import canonical_memory as cm
    retrieval = {}
    # Same recorded query may be unavailable in receipt; verify each mode's
    # effective ACTIVE resolution independently, never promote or dispatch.
    for mode in ['standard','maximum','deepseek_maximum']:
        packet = cm.prepare('tempo_frequencia_v394 rede_fock_v394', mode=mode, max_chars=24000)
        receipt = packet['receipt']
        assert receipt['generation'] == pointer['generation']
        assert receipt['packet_sha256'] == sha(packet['prompt'].encode())
        retrieval[mode] = {'generation':receipt['generation'],'packet_sha256':receipt['packet_sha256'],'context_bytes':receipt['context_bytes']}
    prior = load(W / 'review/QUEUE_R3.json')['queue_ids_constraints_bindings_before_and_after']
    with closing(sqlite3.connect((BASE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True)) as db:
        for table in ['tasks','coordination_jobs']:
            rows = {ident:(req, constraints) for ident,req,constraints in db.execute('SELECT id,request_id,execution_constraints FROM '+table)}
            for ident, row in prior[table].items():
                req, constraints = rows[ident]
                assert req == row['request_id'] and sha((constraints or '').encode()) == row['constraints_sha256']
        bindings = {row[0]:list(row) for row in db.execute('SELECT job_id,envelope_sha256,supplement_sha256,event_id,original_version FROM scientific_contract_bindings')}
        for row in prior['scientific_contract_bindings']:
            assert bindings[row[0]] == row
    for path,row in inputs.items():
        assert sha(Path(path).read_bytes()) == row['sha256']
    report = {'verdict':'PASS_DEPLOYMENT_VERIFIED_LIVE_TEST_PENDING','criterion_satisfied':True,
        'reviewer':'codex-v394-reviewer','reference':str(task.REF),'task_id':'deploy','criterion':t['criterion'],
        'reviewed_submission':t['evidence'],'mission_revision':p['receipt']['revision'],
        'checked_at':datetime.now(timezone.utc).isoformat(),'inputs':inputs,
        'installed_files':1449,'byte_backups_verified':7,'identity':release.identity,
        'web_pid':web.pid,'same_supervisor_pid':parent.pid,'localhost_HTTP':200,
        'queue_ACTIVE':pointer,'effective_retrieval':retrieval,'original_pinned_jobs_constraints_preserved':True,
        'initial_tokenizer_attempt':'Main reported initial CLI attempt failed to resolve tokenizer download; same verifier pin remains unchanged. Subsequent installed PASS uses existing explicit tokenizer cache; no model inference inferred from tokenizer setup.',
        'findings':[],'verify_task_accepted':False,'live_dialog_tested':False,
        'physical_device_verified':False,'reviewer_model_calls':0,'source_execution':False,'gate_changed':False}
    dest = W / 'review/DEPLOYMENT_ACCEPTANCE_R1.json'
    raw=json.dumps(report,ensure_ascii=False,indent=2).encode();temp=dest.with_suffix('.json.tmp')
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw and not dest.exists();temp.replace(dest)
    print(json.dumps({'verdict':report['verdict'],'files':1449,'backups':7,'web_pid':web.pid,'supervisor_pid':parent.pid,'report':str(dest),'sha256':sha(raw)}))


if __name__ == '__main__':
    main()
