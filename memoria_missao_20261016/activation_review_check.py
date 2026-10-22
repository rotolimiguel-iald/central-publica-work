"""Independent installed-artifact and migration checks; read-only production access."""
from pathlib import Path
import ast, base64, hashlib, json, os, sqlite3, subprocess, sys

WORK = Path(__file__).resolve().parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
REF = WORK / 'FECHO_MISSION_REFERENCE.json'
OUT = WORK / 'activation_review_evidence'
OUT.mkdir(exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(name, value):
    p = OUT / name
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    with p.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    return p
def call(cli, request):
    r = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CORE / cli)],
                       input=json.dumps(request), text=True, encoding='utf-8', capture_output=True)
    payload = json.loads(r.stdout)
    assert r.returncode == 0 and payload['ok'], payload
    return payload['result']

deployment = read(WORK / 'DEPLOYMENT.json')
installed = []
for item in deployment['files']:
    target, source = Path(item['target']), Path(item['source'])
    assert sha(target) == sha(source) == item['new_sha256'], str(target)
    if item['backup']:
        backup = Path(item['backup'])
        assert sha(backup) == item['old_sha256'], str(backup)
        if item['append_only']:
            assert target.read_bytes().startswith(backup.read_bytes()), str(target)
    installed.append({'target': str(target), 'sha256': sha(target), 'backup_verified': bool(item['backup'])})
assert len(installed) == 8
pin = read(WORK / 'SUPPLEMENT_FINAL_PIN.json')['current_source_sha256']
for name in ['mission.py', 'mission_cli.py', 'mission_bridge.py']:
    assert sha(WORK / name) == pin[str(WORK / name)]

mcp = read(WORK / 'INSTALLED_MCP_VERIFICATION.json')
assert mcp['ok'] and mcp['provider_calls'] == 0 and len(mcp['all_tools']) == 13 and len(mcp['new_tools']) == 4
for item in mcp['installed_files']: assert sha(item['path']) == item['sha256']
assert sha(mcp['reference']['path']) == mcp['reference']['sha256']
validation = read(WORK / 'VALIDATION_FINAL.json')
assert validation['ok']
for item in validation['tests']:
    assert item['exit'] == 0 and sha(item['log']) == item['sha256']

project = call('mission_cli.py', {'operation': 'project', 'reference': str(REF), 'max_chars': 48000})
projection = project['projection']
legacy = read(WORK / 'LEGACY_CHECKPOINT.json')
assert legacy['revision'] == 63
legacy_ref = Path(projection['constraints']['predecessor_reference'])
legacy_live = call('session_memory.py', {'operation': 'get', 'reference': str(legacy_ref)})
assert legacy_live['objective_bytes_b64'] == legacy['objective_bytes_b64']
assert legacy_live['objective_sha256'] == legacy['objective_sha256']
assert legacy_live['anchor_sha256'] == legacy['anchor_sha256']
assert legacy_live['q']['records'][:len(legacy['q']['records'])] == legacy['q']['records']
assert hashlib.sha256(base64.b64decode(legacy['objective_bytes_b64'])).hexdigest() == legacy['objective_sha256']
original_orders = [r for r in legacy['q']['records'] if r['kind'] == 'decision' and r['statute'] == 'INPUT']
assert len(original_orders) == 8
current_records = {r['id']: r for r in projection['current_records']}
for record in original_orders: assert current_records[record['id']] == record
origin = current_records['migration-origin-v1']
checkpoint_source = next(s for s in origin['sources'] if s['ref'] == str(WORK / 'LEGACY_CHECKPOINT.json'))
assert checkpoint_source['sha256'] == sha(WORK / 'LEGACY_CHECKPOINT.json')

completion = next(r for r in original_orders if r['id'] == 'full-completion-order-20261015')
requirements_source = next(s for s in completion['sources'] if s['ref'].endswith('REQUISITOS_ORIGINAIS_R1.json'))
assert sha(requirements_source['ref']) == requirements_source['sha256']
original_requirements = read(requirements_source['ref'])['requirements']
tasks = {t['id']: t for t in projection['active'] + projection['settled']}
assert len(tasks) == 11 and len(original_requirements) == 10
for r in original_requirements:
    assert tasks[r['id']]['criterion'] == r['requirement'] + '. ' + r['acceptance_evidence']
    assert 'M0_MEMORIA' in tasks[r['id']]['depends_on']
assert tasks['M0_MEMORIA']['status'] == 'review_pending'
assert tasks['M0_MEMORIA']['submitted_by'] != 'codex-mission-memory-review'
for e in tasks['M0_MEMORIA']['evidence']: assert sha(e['path']) == e['sha256']
assert sha(REF) == mcp['reference']['sha256']
assert sha(read(REF)['source']['path']) == projection['objective_sha256']

handles = {h['id']: h for h in projection['flow']['handles']}
old_handles = legacy['p']['handles']
assert len(old_handles) == 3
for old in old_handles:
    current = handles[old['id']]
    for key in ['request_id', 'job_id', 'provider', 'execution_task_id']:
        assert current.get(key) == old.get(key), (old['id'], key)
    assert current['no_repeat'] is True
queue = read(WORK / 'QUEUE_READ_ONLY.json')
db = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\tasks.sqlite3')
con = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)
con.row_factory = sqlite3.Row
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
table = next(t for t in tables if {'id', 'stage', 'execution_task_id'} <= {r[1] for r in con.execute('PRAGMA table_info("' + t + '")')})
queue_rows = []
for expected in queue['rows']:
    actual = dict(con.execute('SELECT id AS job_id,stage,execution_task_id FROM "' + table + '" WHERE id=?', (expected['job_id'],)).fetchone())
    assert actual == expected
    queue_rows.append(actual)
con.close()
pending_provider_ids = {r['job_id'] for r in queue_rows if r['stage'] != 'completed'}
assert len(pending_provider_ids) == 2
assert pending_provider_ids <= {h.get('job_id') for h in projection['unresolved_handles']}
assert projection['tetelestai'] is False

snapshot_path = save('REVIEW_PROJECT.json', project)
summary = {'ok': True, 'installed': installed,
    'legacy_revision': legacy['revision'], 'legacy_live_revision': legacy_live['revision'],
    'legacy_records_preserved': len(legacy['q']['records']), 'input_decisions_preserved': len(original_orders),
    'original_requirements_preserved': len(original_requirements), 'total_requirements': len(tasks),
    'external_identities_preserved': len(old_handles), 'provider_jobs_current': queue_rows,
    'unresolved_handles': projection['unresolved_handles'], 'mission_revision': project['receipt']['revision'],
    'projection_sha256': project['projection_sha256'], 'projection_snapshot': str(snapshot_path),
    'tetelestai': projection['tetelestai'], 'mcp_evidence': 'Coordinator receipt inspected and installed hashes remeasured; reviewer did not rerun stdio.',
    'sources': {str(p): sha(p) for p in [WORK / 'DEPLOYMENT.json', WORK / 'INSTALLED_MCP_VERIFICATION.json',
        WORK / 'LEGACY_CHECKPOINT.json', WORK / 'VALIDATION_FINAL.json', WORK / 'MISSION_REQUIREMENTS.json',
        WORK / 'QUEUE_READ_ONLY.json', REF, CORE / 'MISSION_PROTOCOL.md', Path(requirements_source['ref'])]}}
save('CHECKS.json', summary)
print(json.dumps({k: v for k, v in summary.items() if k not in ['installed', 'sources', 'unresolved_handles']}, ensure_ascii=False))
