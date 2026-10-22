# -*- coding: utf-8 -*-
"""E2: 5 concurrent processes on 5 contexts (one root), then 3 processes on ONE context with CAS retry.

usage: e2_concurrency.py            (orchestrator)
       e2_concurrency.py worker ROOT CTX N TAG   (internal)
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from common import RUNS, SCOPE, AGENT, record, pct, dump, dir_bytes


def worker(root, ctx, n, tag):
    from iald_memory import MemoryStore, RevisionConflict
    store = MemoryStore(root, snapshot_archive_dir=Path(root).parent / 'arquivo_D')
    store.ensure_context(ctx, objective='E2 shared objective for ' + ctx.split('.')[0], scope=SCOPE, actor=AGENT)
    lat, errors, conflicts = [], {}, 0
    done = 0
    i = 0
    while done < n:
        i += 1
        snap = store.get(ctx, SCOPE)
        t0 = time.perf_counter()
        try:
            store.transition(ctx, SCOPE, snap['revision'], '%s.%05d' % (tag, i), AGENT,
                             {'records': [dict(record(i, 200), id='%s_%05d' % (tag, i))]})
            lat.append(time.perf_counter() - t0)
            done += 1
        except RevisionConflict:
            conflicts += 1
        except Exception as exc:  # visible: counted by type
            errors[type(exc).__name__ + ':' + str(exc)[:80]] = errors.get(type(exc).__name__ + ':' + str(exc)[:80], 0) + 1
            if sum(errors.values()) > 50:
                break
    print(json.dumps({'tag': tag, 'ctx': ctx, 'done': done, 'conflicts': conflicts, 'errors': errors,
                      'median_ms': round(pct(lat, 0.5) * 1000, 2) if lat else None,
                      'p99_ms': round(pct(lat, 0.99) * 1000, 2) if lat else None,
                      'max_ms': round(max(lat) * 1000, 2) if lat else None}))


def scenario(name, specs):
    root = RUNS / ('e2_' + name) / 'state'
    if root.parent.exists():
        shutil.rmtree(root.parent)
    root.mkdir(parents=True)
    # create the database first (schema) so workers race only on contexts/events
    from iald_memory import MemoryStore
    MemoryStore(root, snapshot_archive_dir=root.parent / 'arquivo_D')
    t0 = time.time()
    procs = [subprocess.Popen([sys.executable, '-B', '-X', 'utf8', __file__, 'worker', str(root), ctx, str(n), tag],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE) for ctx, n, tag in specs]
    outs = []
    for p in procs:
        o, e = p.communicate(timeout=1800)
        try:
            outs.append(json.loads(o.decode().strip().splitlines()[-1]))
        except Exception:
            outs.append({'rc': p.returncode, 'stdout': o.decode()[-500:], 'stderr': e.decode()[-1500:]})
    wall = time.time() - t0
    from iald_memory import migrate
    ver = migrate._summarize(migrate.verify_all(root, deep=True, snapshot_archive_dir=root.parent / 'arquivo_D'))
    res = {'scenario': name, 'wall_s': round(wall, 2), 'workers': outs,
           'verify_deep': {k: {kk: v[kk] for kk in ('ok', 'event_count', 'journal_ok', 'journal_lines', 'journal_voided',
                                                    'journal_orphans', 'journal_missing_events')} for k, v in ver.items()},
           'db_bytes': (root / 'memory.sqlite3').stat().st_size, 'journal': dir_bytes(root / 'journal'),
           'snapshots_local': dir_bytes(root / 'snapshots'), 'archive': dir_bytes(root.parent / 'arquivo_D')}
    dump(RUNS / ('e2_' + name + '.json'), res)
    print(json.dumps(res, ensure_ascii=False)[:3000])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'worker':
        worker(Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5])
    else:
        scenario('5ctx', [('ctx%d.e2' % k, 120, 'w%d' % k) for k in range(5)])
        scenario('1ctx_3proc', [('shared.e2', 80, 's%d' % k) for k in range(3)])
