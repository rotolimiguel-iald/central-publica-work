# -*- coding: utf-8 -*-
"""E3: process death in the middle of a transition; consistency of journal + sqlite; verify detection.

Part A: deterministic death points (child process, os._exit / TerminateProcess) at:
  A1 after the journal line is fsynced, before the sqlite commit
  A2 in the middle of the journal write (half a line written, no newline)
  A3 in the middle of the byte snapshot copy (tmp file half written), before any db write
  A4 after the sqlite commit, before the in-process journal cache is updated
  A5 during sqlite commit (hot -journal): kill between the INSERTs and COMMIT with the rollback journal present
Part B: 40 random hard kills (TerminateProcess) of a writer loop on 2 contexts.
Part C: tampering that verify must detect.
After every death: hot -journal?, PRAGMA integrity_check, verify fast+deep of every context, then a NEW transition
must succeed and void orphan journal lines.
"""
from __future__ import annotations
import json
import os
import random
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from common import RUNS, SCOPE, AGENT, record, dump

BASE = RUNS / 'e3_crash'


def child(root, mode, n):
    from iald_memory import MemoryStore, journal as J, snapshots as S
    import iald_memory.store as ST
    store = MemoryStore(root, snapshot_archive_dir=Path(root).parent / 'arquivo_D')
    for ctx in ('ctx.a', 'ctx.b'):
        store.ensure_context(ctx, objective='E3 ' + ctx, scope=SCOPE, actor=AGENT)
    if mode == 'A1':
        orig = store._journal_append
        def hook(*a, **k):
            r = orig(*a, **k)
            os._exit(91)
        store._journal_append = hook
    elif mode == 'A2':
        def half(journal_dir, context_id, kind, fields, committed, created_at, cached_tail=None):
            path = J.path_for(journal_dir, context_id)
            payload = J.canonical(dict(fields, seq=999, kind=kind, prev_line_sha256='x', line_sha256='y')).encode('ascii')
            with open(path, 'ab') as h:
                h.write(payload[: len(payload) // 2])
                h.flush(); os.fsync(h.fileno())
            os._exit(92)
        J.append = half
    elif mode == 'A3':
        def half_copy(src, dst):
            data = Path(src).read_bytes()
            with open(dst, 'wb') as h:
                h.write(data[: len(data) // 2]); h.flush(); os.fsync(h.fileno())
            os._exit(93)
        S._copy_bytes = half_copy
        # force the policy to be due at the next mutation
        conn = sqlite3.connect(str(Path(root) / 'memory.sqlite3'), isolation_level=None)
        conn.execute("UPDATE snapshot_policy SET policy_json=json_set(policy_json,'$.mutations_since_snapshot',49) WHERE id=1")
        conn.close()
    elif mode == 'A4':
        orig_commit = None
        class Wrap:
            pass
        orig_connect = store._connect
        def connect():
            c = orig_connect()
            class C:
                def __init__(s, c): s._c = c
                def __getattr__(s, k): return getattr(s._c, k)
                def commit(s):
                    s._c.commit(); os._exit(94)
            return C(c)
        store._connect = connect
    elif mode == 'A5':
        orig_connect = store._connect
        def connect():
            c = orig_connect()
            class C:
                def __init__(s, c): s._c = c
                def __getattr__(s, k): return getattr(s._c, k)
                def commit(s):
                    # force a spill of dirty pages to the main file while the rollback journal exists, then die
                    s._c.execute('PRAGMA cache_spill=ON')
                    s._c.execute("CREATE TEMP TABLE IF NOT EXISTS t(x)")
                    os._exit(95)
            return C(c)
        store._connect = connect
    rev = store.get('ctx.a', SCOPE)['revision']
    i = int(time.time() * 1000) % 10_000_000
    for k in range(n):
        ctx = 'ctx.a' if k % 2 == 0 else 'ctx.b'
        rev = store.get(ctx, SCOPE)['revision']
        store.transition(ctx, SCOPE, rev, 'ev%d_%d' % (i, k), AGENT, {'records': [dict(record(k, 2000), id='r%d_%d' % (i, k))]})
    print('done')


def check(root, label):
    from iald_memory import MemoryStore, migrate
    root = Path(root)
    out = {'label': label, 'hot_journal': (root / 'memory.sqlite3-journal').exists()}
    conn = sqlite3.connect(str(root / 'memory.sqlite3'))
    out['integrity_check'] = conn.execute('PRAGMA integrity_check').fetchone()[0]
    conn.close()
    out['hot_journal_after_open'] = (root / 'memory.sqlite3-journal').exists()
    try:
        fast = migrate._summarize(migrate.verify_all(root, deep=False, snapshot_archive_dir=root.parent / 'arquivo_D'))
        deep = migrate._summarize(migrate.verify_all(root, deep=True, snapshot_archive_dir=root.parent / 'arquivo_D'))
        out['verify'] = {c: {k: deep[c][k] for k in ('ok', 'event_count', 'journal_ok', 'journal_orphans', 'journal_voided',
                                                    'journal_missing_events')} for c in deep}
        out['fast_equals_deep_head'] = all(fast[c]['receipt'] == deep[c]['receipt'] for c in deep)
    except Exception as exc:
        out['verify_error'] = repr(exc)[:300]
    # a new transition must work and void orphan lines
    try:
        store = MemoryStore(root, snapshot_archive_dir=root.parent / 'arquivo_D')
        for ctx in ('ctx.a', 'ctx.b'):
            rev = store.get(ctx, SCOPE)['revision']
            store.transition(ctx, SCOPE, rev, 'after_%s_%s_%d' % (label, ctx, time.time_ns()), AGENT,
                             {'records': [dict(record(1, 100), id='after_%s_%s_%d' % (label, ctx.replace('.', '_'), time.time_ns()))]})
        after = migrate._summarize(migrate.verify_all(root, deep=True, snapshot_archive_dir=root.parent / 'arquivo_D'))
        out['after_new_transition'] = {c: {k: after[c][k] for k in ('ok', 'journal_ok', 'journal_orphans', 'journal_voided')} for c in after}
    except Exception as exc:
        out['after_error'] = repr(exc)[:300]
    snaps = root / 'snapshots'
    out['snapshot_tmp_left'] = sorted(p.name for p in snaps.glob('*.tmp')) if snaps.exists() else []
    return out


def fresh(name):
    from iald_memory import MemoryStore
    root = BASE / name / 'state'
    if root.parent.exists():
        shutil.rmtree(root.parent)
    store = MemoryStore(root, snapshot_archive_dir=root.parent / 'arquivo_D')
    for ctx in ('ctx.a', 'ctx.b'):
        store.ensure_context(ctx, objective='E3 ' + ctx, scope=SCOPE, actor=AGENT)
        for k in range(5):
            rev = store.get(ctx, SCOPE)['revision']
            store.transition(ctx, SCOPE, rev, 'seed_%s_%d' % (ctx, k), AGENT, {'records': [dict(record(k, 500), id='seed_%d' % k)]})
    return root


def run_child(root, mode, n, kill_after=None):
    p = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', __file__, 'child', str(root), mode, str(n)],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if kill_after is not None:
        time.sleep(kill_after)
        p.kill()  # TerminateProcess
    o, e = p.communicate(timeout=600)
    return p.returncode, o.decode()[-200:], e.decode()[-600:]


def tamper(results):
    from iald_memory import MemoryStore, migrate
    def ver(root):
        try:
            r = migrate._summarize(migrate.verify_all(root, deep=False, snapshot_archive_dir=root.parent / 'arquivo_D'))
            return {c: {k: r[c][k] for k in ('ok', 'journal_ok', 'journal_missing_events')} for c in r}
        except Exception as exc:
            return {'error': repr(exc)[:200]}
    # C1 delete last journal line of ctx.a
    root = fresh('C1'); p = root / 'journal' / 'ctx.a.events.jsonl'
    lines = p.read_bytes().splitlines(keepends=True); p.write_bytes(b''.join(lines[:-1]))
    results['C1_drop_last_journal_line'] = ver(root)
    # C2 flip one byte inside a journal line (middle)
    root = fresh('C2'); p = root / 'journal' / 'ctx.a.events.jsonl'
    raw = bytearray(p.read_bytes()); i = raw.find(b'registro'); raw[i] = ord('R'); p.write_bytes(bytes(raw))
    results['C2_flip_journal_byte'] = ver(root)
    # C3 change materialized state (context_state has no update trigger)
    root = fresh('C3'); c = sqlite3.connect(str(root / 'memory.sqlite3'), isolation_level=None)
    c.execute("UPDATE context_state SET state_json=replace(state_json,'registro','REGISTRO') WHERE context_id='ctx.a'"); c.close()
    results['C3_edit_context_state'] = ver(root)
    # C3b change materialized state AND its sha (self-consistent row), keep revision/event_hash
    root = fresh('C3b'); c = sqlite3.connect(str(root / 'memory.sqlite3'), isolation_level=None)
    import hashlib
    sj = c.execute("SELECT state_json FROM context_state WHERE context_id='ctx.a'").fetchone()[0].replace('registro', 'REGISTRO')
    c.execute("UPDATE context_state SET state_json=?, state_sha256=? WHERE context_id='ctx.a'", (sj, hashlib.sha256(sj.encode()).hexdigest())); c.close()
    results['C3b_edit_context_state_with_sha'] = ver(root)
    # C4 drop guard + edit an event delta
    root = fresh('C4'); c = sqlite3.connect(str(root / 'memory.sqlite3'), isolation_level=None)
    c.execute('DROP TRIGGER events_no_update')
    c.execute("UPDATE events SET changes_json=replace(changes_json,'registro','REGISTRO') WHERE context_id='ctx.a' AND revision=3")
    c.execute("CREATE TRIGGER events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append-only event'); END"); c.close()
    results['C4_edit_event_delta'] = ver(root)
    # C5 journal file removed
    root = fresh('C5'); (root / 'journal' / 'ctx.b.events.jsonl').unlink()
    results['C5_journal_missing'] = ver(root)
    # C6 snapshot table forged at an old revision (insert a wrong snapshot row) -> fast path base
    root = fresh('C6'); c = sqlite3.connect(str(root / 'memory.sqlite3'), isolation_level=None)
    row = c.execute("SELECT state_json, state_sha256, event_hash FROM events WHERE context_id='ctx.a' AND revision=0").fetchone()
    c.execute("INSERT INTO snapshots VALUES ('ctx.a', 2, ?, ?, ?, 'x', 'forged')", row); c.close()
    results['C6_forged_snapshot_row'] = ver(root)


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    results = {}
    for mode in ('A1', 'A2', 'A3', 'A4', 'A5'):
        root = fresh(mode)
        rc, o, e = run_child(root, mode, 5)
        results[mode] = {'child_rc': rc, 'child_stderr_tail': e[-300:], **check(root, mode)}
        print(mode, json.dumps(results[mode], ensure_ascii=False)[:900], flush=True)
    # Part B: random hard kills
    root = fresh('B')
    rnd = random.Random(20261013)
    kills = []
    for k in range(40):
        delay = rnd.uniform(0.15, 1.2)
        rc, o, e = run_child(root, 'none', 400, kill_after=delay)
        st = {'k': k, 'delay': round(delay, 3), 'rc': rc, 'hot_journal': (root / 'memory.sqlite3-journal').exists()}
        kills.append(st)
    results['B_random_kills'] = {'kills': kills, 'final': check(root, 'B')}
    print('B', json.dumps(results['B_random_kills']['final'], ensure_ascii=False)[:1500], flush=True)
    tamper(results)
    for k in [x for x in results if x.startswith('C')]:
        print(k, results[k])
    dump(RUNS / 'e3_crash.json', results)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'child':
        child(Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    else:
        main()
