# -*- coding: utf-8 -*-
"""E8: hard kill (TerminateProcess) of migrar_para_delta.py --apply at several moments on the 488 MB synthetic v1
database; then: schema, integrity_check, -journal, leftovers; then a clean --apply must succeed with the v1 heads."""
from __future__ import annotations
import json
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from common import RUNS, MEM_CAND, dump, sha256_file

SRC = RUNS / 'e4_v1' / 'state' / 'memory.sqlite3'
CLI = MEM_CAND / 'migrar_para_delta.py'


def state_of(st):
    c = sqlite3.connect(str(st / 'memory.sqlite3'))
    sv = c.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
    ic = c.execute('PRAGMA quick_check').fetchone()[0]
    tables = sorted(r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'"))
    c.close()
    return {'schema_version': sv, 'quick_check': ic, 'tables': tables,
            'listing': sorted(p.name for p in st.iterdir()),
            'journal_lines': {p.name: sum(1 for _ in p.open('rb')) for p in (st / 'journal').glob('*.jsonl')} if (st / 'journal').exists() else {}}


def main():
    out = {}
    v1_sha = sha256_file(SRC)
    for delay in (2.0, 7.0, 9.5, 12.0):
        work = RUNS / ('e8_kill_%s' % str(delay).replace('.', '_'))
        if work.exists():
            shutil.rmtree(work)
        st = work / 'state'; st.mkdir(parents=True)
        shutil.copyfile(SRC, st / 'memory.sqlite3')
        p = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', str(CLI), '--state', str(st), '--apply',
                              '--snapshot-archive-dir', str(work / 'arquivo_D')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(delay)
        killed = p.poll() is None
        p.kill(); o, e = p.communicate()
        res = {'killed_while_running': killed, 'stderr_tail': e.decode()[-400:], 'after_kill': state_of(st)}
        res['db_equals_v1_after_kill'] = sha256_file(st / 'memory.sqlite3') == v1_sha
        t0 = time.time()
        q = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CLI), '--state', str(st), '--apply',
                            '--snapshot-archive-dir', str(work / 'arquivo_D')], capture_output=True)
        try:
            r = json.loads(q.stdout.decode())
        except ValueError:
            r = {'raw': q.stdout.decode()[-600:]}
        res['rerun'] = {'rc': q.returncode, 'seconds': round(time.time() - t0, 1), 'ok': r.get('ok'),
                        'already_migrated': r.get('already_migrated'), 'head_mismatches': r.get('head_mismatches'),
                        'error': r.get('error'),
                        'verify': {c: {k: v[k] for k in ('ok', 'journal_ok', 'journal_lines', 'journal_orphans', 'event_count')}
                                   for c, v in (r.get('verify_after') or {}).items()}}
        res['final'] = state_of(st)
        out[str(delay)] = res
        print(delay, json.dumps(res, ensure_ascii=False)[:1500], flush=True)
    dump(RUNS / 'e8_migration_kill.json', out)


if __name__ == '__main__':
    main()
