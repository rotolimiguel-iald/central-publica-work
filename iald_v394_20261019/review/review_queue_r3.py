"""Independent inactive scientific snapshot review. No build/activate/source import."""
from pathlib import Path
from datetime import datetime, timezone
from contextlib import closing
import hashlib, json, os, sqlite3, sys

W = Path(__file__).resolve().parents[1]
BASE = W.parents[1] / 'Chatgpt/IALD_ORQUESTRACAO_20260923'
Q = W / 'queue/R3'
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = {}


def read(path):
    path = Path(path)
    b = path.read_bytes()
    inputs[str(path)] = {'sha256': sha(b), 'bytes': len(b)}
    return b


def load(path):
    return json.loads(read(path))


def pin(row):
    b = read(row['path'])
    assert sha(b) == row['sha256'] and len(b) == row['bytes']
    return b


def jobs_state(path):
    # IDs and constraints only: no prompts, results, credentials or dispatch.
    with closing(sqlite3.connect(Path(path).as_uri() + '?mode=ro', uri=True)) as db:
        result = {}
        for table in ['tasks', 'coordination_jobs']:
            rows = db.execute('SELECT id,request_id,execution_constraints FROM ' + table + ' ORDER BY id').fetchall()
            result[table] = {ident: {'request_id': request, 'constraints_sha256': sha((constraints or '').encode()), 'memory_generation': ((json.loads(constraints) or {}).get('memory_generation') if constraints else None)} for ident, request, constraints in rows}
        bindings = db.execute('SELECT job_id,envelope_sha256,supplement_sha256,event_id,original_version FROM scientific_contract_bindings ORDER BY job_id').fetchall()
        result['scientific_contract_bindings'] = bindings
        return result


def main():
    sys.path.insert(0, str(W))
    import task
    p = task.project()
    t = next(x for x in p['projection']['active'] if x['id'] == 'queue')
    delivery_path = Q / 'DELIVERY_PREPARED_R3.json'
    assert t['status'] == 'review_pending'
    assert t['evidence'] == [{'path': str(delivery_path), 'sha256': sha(read(delivery_path))}]
    d = load(delivery_path)
    assert d['status'] == 'PREPARED_VERIFIED_INACTIVE' and d['activation_performed'] is False
    target = Path(d['stagedtarget'])
    m = json.loads(pin(d['manifest']))
    prep = json.loads(pin(d['preparation_receipt']))
    for row in d['approval_sources']:
        pin(row)
    pin(d['helper_pin'])
    for row in d['snapshot_inventory'].values():
        pin(row)
    assert sha(read(target / 'index.sqlite3')) == m['index_sha256']
    active_before = pin(d['active_pin_before'])
    assert d['active_pin_before'] == d['active_pin_after']
    assert json.loads(active_before) == d['previousACTIVE'] and json.loads(active_before)['release'] == 'v393'
    ledger = BASE / 'state/tasks.sqlite3'
    jobs_before = jobs_state(ledger)
    original_pins = {Path(row['path']).name: row for row in d['sourcepins']}
    assert len(original_pins) == len(d['sourcepins']) == len(m['documents']) == 13
    generation = sha(json.dumps([(Path(row['path']).name, row['sha256']) for row in d['sourcepins']], ensure_ascii=False).encode())
    assert generation == d['generation'] == m['generation']
    docs = {}
    for doc in m['documents']:
        source = pin(original_pins[doc['name']])
        snapshot = read(doc['path'])
        assert source == snapshot and sha(snapshot) == doc['sha256'] and len(snapshot) == doc['bytes']
        docs[doc['name']] = snapshot
    seal = json.loads(docs['um_absoluto_selo.json'])
    proof = json.loads(docs['tgl_kernel_proof_manifest.json'])
    assert seal['um_version'] == 'v394' and seal['formal_source_hash'] == proof['formal_source_hash']
    for name, data in docs.items():
        if name in seal['sha256']:
            assert sha(data) == seal['sha256'][name]
    assert seal['fail_closed_selftest'] == 'FAIL_CLOSED_SELFTEST_PASSED'
    chunk_counts = {}
    with closing(sqlite3.connect((target / 'index.sqlite3').as_uri() + '?mode=ro', uri=True)) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert db.execute('SELECT COUNT(*) FROM passages').fetchone()[0] == m['chunks'] == d['chunks'] == 27654
        assert {row[0] for row in db.execute('SELECT DISTINCT document FROM passages')} == set(docs)
        for name, data in docs.items():
            text = data.decode('utf-8-sig')
            lines = text.splitlines(keepends=True)
            rows = db.execute('SELECT first_line,last_line,body FROM passages WHERE document=? ORDER BY rowid', (name,)).fetchall()
            assert ''.join(row[2] for row in rows) == text, name
            line_fragments = {}
            for first, last, body in rows:
                first, last = int(first), int(last)
                assert 1 <= first <= last <= len(lines) and 0 < len(body) <= 2300
                if first == last and len(lines[first - 1]) > 2300:
                    offset = line_fragments.get(first, 0)
                    assert body == lines[first - 1][offset:offset + len(body)]
                    line_fragments[first] = offset + len(body)
                else:
                    assert body == ''.join(lines[first - 1:last])
            for number, length in line_fragments.items():
                assert length == len(lines[number - 1])
            chunk_counts[name] = len(rows)
        for name in prep['statute_record_names']:
            assert db.execute('SELECT 1 FROM passages WHERE passages MATCH ? LIMIT 1', ('"' + name + '"',)).fetchone()

    # No writes except reviewer artifact. The imported module exposes retrieval;
    # build/activate/ScientificMemorySync/um.py/Lean are never called/imported.
    def guard(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
            raise RuntimeError('Offline snapshot review')
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
    sys.path.insert(0, str(BASE))
    from iald_orchestrator import canonical_memory as cm
    assert sha(read(cm.__file__)) == prep['module_pin']['sha256']
    query = ' '.join(prep['statute_record_names'])
    retrieval = {}
    for mode in ['standard', 'maximum', 'deepseek_maximum']:
        packet = cm.prepare(query, target, allowed_sources=['um.py', 'um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md'], mode=mode, max_chars=24000)
        receipt = packet['receipt']
        assert receipt == d['verification']['retrieval'][mode]
        assert receipt['generation'] == generation and receipt['packet_sha256'] == sha(packet['prompt'].encode())
        for source in receipt['sources']:
            assert source['sha256'] == sha(docs[source['file']])
        retrieval[mode] = {key: receipt[key] for key in ['generation', 'packet_sha256', 'context_bytes', 'coverage', 'memory_mode']}
        retrieval[mode]['passages'] = len(receipt['sources'])
    assert pin(d['active_pin_after']) == active_before
    assert jobs_state(ledger) == jobs_before
    for source, row in inputs.items():
        assert sha(Path(source).read_bytes()) == row['sha256'], source
    report = {
        'verdict': 'PASS_PREPARATION_VERIFIED_INACTIVE', 'criterion_satisfied': True,
        'reviewer': 'codex-v394-reviewer', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'reference': str(task.REF), 'task_id': 'queue', 'criterion': t['criterion'],
        'reviewed_submission': t['evidence'], 'baseline_revision': p['receipt']['revision'],
        'inputs': inputs, 'generation': generation, 'epoch': d['epoch'],
        'documents': 13, 'chunks': 27654, 'chunk_counts': chunk_counts,
        'chunks_verification': 'Every source byte compared with snapshot; all chunk bodies reconstruct exact decoded UTF-8-sig text, each first/last line and long-line fragment checked independently.',
        'retrieval_reexecuted': retrieval, 'previous_ACTIVE': d['previousACTIVE'],
        'ACTIVE_bytes_unchanged': True,
        'queue_ids_constraints_bindings_before_and_after': jobs_before,
        'preservation_scope': 'All queue task/coordination IDs, request IDs, constraints hashes, fixed generations and scientific contract bindings independently equal before/after this read-only review. Builder preservation before review is its declared receipt, not a separate historical database snapshot assertion.',
        'findings': [], 'source_execution': False, 'provider_calls': 0,
        'activated': False, 'app_accepted': False, 'deploy_accepted': False,
        'gate_changed': False, 'pending': ['Principal-controlled activation only through existing API/CAS against the still-current ACTIVE baseline after final coordinated review.'],
    }
    dest = W / 'review/QUEUE_R3.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    temp = dest.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and not dest.exists()
    temp.replace(dest)
    print(json.dumps({'verdict': report['verdict'], 'documents': 13, 'chunks': 27654, 'retrieval': retrieval, 'report': str(dest), 'sha256': sha(raw)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
