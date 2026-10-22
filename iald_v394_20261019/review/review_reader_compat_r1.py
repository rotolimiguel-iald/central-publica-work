"""Independent byte-diff review and isolated replay of all supplied reader cases."""
from pathlib import Path
from datetime import datetime, timezone
import ast, copy, hashlib, importlib.util, json, os, sys, tempfile

W = Path(__file__).resolve().parents[1]
A = W / 'app'
C = W / 'review'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = lambda p: {'path': str(p), 'sha256': sha(Path(p).read_bytes())}
sys.path[:0] = [str(W), str(R)]
import task


def load(path, label):
    spec = importlib.util.spec_from_file_location(label, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p = task.project()
    requirement = next(x for x in p['projection']['active'] if x['id'] == 'reader_compat')
    assert requirement['status'] == 'review_pending'
    dpath = A / 'compat/DELIVERY_PREPARED_R1.json'
    assert requirement['evidence'] == [pin(dpath)]
    d = json.loads(dpath.read_bytes())
    for key in ['plan', 'tests', 'test_script', 'source_result', 'original_app_delivery']:
        row = d[key]
        b = Path(row['path']).read_bytes()
        assert sha(b) == row['sha256'] and len(b) == row['bytes']
    plan = json.loads(Path(d['plan']['path']).read_bytes())['files']
    assert len(plan) == 2
    for row, (name, before, after) in zip(plan, [
        ('iald_estado_publicado.py', b'else 10000000', b'else 32000000'),
        ('iald_core_indexado.py', b'total > 10000000', b'total > 32000000')]):
        assert Path(row['runtime_path']) == R / name
        raw = Path(row['runtime_path']).read_bytes()
        staged = Path(row['staged_path']).read_bytes()
        assert sha(raw) == row['baseline_sha256'] and sha(staged) == row['staged_sha256']
        assert raw.count(before) == 1 and staged == raw.replace(before, after)
        # Independent AST equality after reversing just the literal's value.
        old_tree, new_tree = ast.parse(raw), ast.parse(staged)
        old_dump = ast.dump(old_tree, include_attributes=False)
        new_dump = ast.dump(new_tree, include_attributes=False)
        assert new_dump.replace('value=32000000', 'value=10000000') == old_dump
    script = Path(d['test_script']['path']).read_text(encoding='utf-8')
    # Only the inspected test section is replayed, not builder preflight, preparation,
    # staging writes or submission. Fixture writes and cleanup stay below review/.
    tests_only = script[script.index('old_pub=load('):script.index("write(C/'TEST_RESULTS_R1.json'")]
    original_receipt = A / 'DELIVERY_PREPARED.json'
    original_receipt_pin = sha(original_receipt.read_bytes())
    stage = A / 'compat/staging'

    def guard(event, args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
            raise RuntimeError('Review is offline')
        if event == 'open':
            path, mode, flags = args
            if isinstance(path, int):
                return
            path = Path(os.fsdecode(path)).resolve()
            if path.name.lower() in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json'}:
                raise RuntimeError('Confidential source refused')
            writing = isinstance(mode, str) and any(x in mode for x in 'wax+') or isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)
            if writing and not path.is_relative_to(C):
                raise RuntimeError('Only reviewer output/fixtures may be written')
    sys.addaudithook(guard)
    env = dict(globals(), stage=stage, plan=plan, original_receipt=original_receipt, original_receipt_pin=original_receipt_pin)
    exec(compile(tests_only, '<independent-isolated-reader-test-replay>', 'exec'), env)
    tests = env['tests']
    supplied = json.loads(Path(d['tests']['path']).read_bytes())
    assert tests == supplied['tests'] and len(tests) == 21
    assert all(sha(Path(row['runtime_path']).read_bytes()) == row['baseline_sha256'] for row in plan)
    report = {
        'verdict': 'PASS', 'reviewer': 'codex-v394-reviewer',
        'checked_at': datetime.now(timezone.utc).isoformat(), 'reference': str(task.REF),
        'task_id': 'reader_compat', 'criterion': requirement['criterion'],
        'reviewed_submission': requirement['evidence'], 'mission_revision': p['receipt']['revision'],
        'review_script': pin(Path(__file__)), 'builder_test_script': pin(Path(d['test_script']['path'])),
        'independent_byte_comparison': 'Exactly one 10000000 -> 32000000 literal per file; all other bytes and AST nodes unchanged.',
        'files': plan, 'tests_reexecuted': tests, 'test_count': len(tests),
        'bounds': {'json_and_aggregate_bytes': 32000000, 'program_bytes_preserved': 64000000},
        'scope': 'Staged reader compatibility only. Tests use local syntax/hash fixtures, not evidence of v394 publication.',
        'network_calls': 0, 'api_calls': 0, 'token_count_calls': 0,
        'scientific_program_executed_or_imported': False, 'production_installed': False,
        'findings': [], 'app_accepted': False,
    }
    path = C / 'READER_COMPAT_R1.json'
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode()
    temp = path.with_suffix('.json.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and not path.exists()
    temp.replace(path)
    print(json.dumps({'verdict': report['verdict'], 'test_count': len(tests), 'report': pin(path)}))


if __name__ == '__main__':
    main()
