"""Run the core suites against the v2 copy, under the auditor guard, inside this folder only.

Environment fixed here: ACOM_AUDIT_ROOT (guard: no network, no write/sqlite outside this
folder, no confidential open), PYTHONPATH (guard + v2 lib + tests), TMP/TEMP inside the folder,
IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR inside the folder (never D:). Writes a JSON summary per suite.
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
NUCLEO = HERE.parent
LIB = NUCLEO / 'copia' / 'MEMORIA_IALD' / 'lib'
TMP = NUCLEO / 'tmp'
EVID = NUCLEO / 'evidencias'


def run(module, extra_env=None):
    TMP.mkdir(exist_ok=True); EVID.mkdir(exist_ok=True); (NUCLEO / 'guard_log').mkdir(exist_ok=True)
    env = dict(os.environ)
    env.update({
        'ACOM_AUDIT_ROOT': str(NUCLEO),
        'PYTHONPATH': os.pathsep.join([str(NUCLEO / 'guard'), str(LIB), str(HERE)]),
        'TMP': str(TMP), 'TEMP': str(TMP), 'TMPDIR': str(TMP),
        'IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR': str(TMP / 'arquivo_D_padrao'),
        'NUCLEO_EVIDENCIAS': str(EVID),
        'PYTHONIOENCODING': 'utf-8',
    })
    env.update(extra_env or {})
    started = time.time()
    proc = subprocess.run([sys.executable, '-X', 'utf8', '-m', 'unittest', '-v', module],
                          cwd=str(HERE), env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = proc.stdout + proc.stderr
    (EVID / f'unittest_{module}.txt').write_text(out, encoding='utf-8')
    results = []
    pending = None  # a test with a docstring prints its verdict on the following line
    for line in out.splitlines():
        m = re.match(r'^(test_\w+) \((\S+)\)(?: \.\.\.)? ... (ok|FAIL|ERROR|skipped.*)$', line)
        if not m:
            m = re.match(r'^(test_\w+) \((\S+)\) \.\.\. (ok|FAIL|ERROR|skipped.*)$', line)
        if m:
            results.append({'test': m.group(1), 'class': m.group(2), 'result': m.group(3)})
            pending = None
            continue
        head = re.match(r'^(test_\w+) \((\S+)\)$', line)
        if head:
            pending = (head.group(1), head.group(2))
            continue
        if pending:
            tail = re.match(r'^.* \.\.\. (ok|FAIL|ERROR|skipped.*)$', line)
            if tail:
                results.append({'test': pending[0], 'class': pending[1], 'result': tail.group(1)})
                pending = None
    summary = {'module': module, 'returncode': proc.returncode, 'seconds': round(time.time() - started, 2),
               'ran': len(results), 'ok': sum(r['result'] == 'ok' for r in results),
               'failed': sum(r['result'] != 'ok' for r in results), 'results': results,
               'tail': out.strip().splitlines()[-3:]}
    (EVID / f'unittest_{module}.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
    return summary


if __name__ == '__main__':
    modules = sys.argv[1:] or ['test_store', 'test_store_v2']
    total_fail = 0
    for module in modules:
        s = run(module)
        total_fail += s['failed'] + (1 if s['returncode'] else 0)
        print(f"{module}: ran {s['ran']} ok {s['ok']} failed {s['failed']} rc {s['returncode']} in {s['seconds']}s")
        for r in s['results']:
            if r['result'] != 'ok':
                print('   ', r['result'], r['test'])
        print('   ', ' | '.join(s['tail']))
    sys.exit(1 if total_fail else 0)
