# -*- coding: utf-8 -*-
"""E1: growth with N transitions on one context (candidate lib). Half facts, half optional candidates."""
from __future__ import annotations
import shutil
import sys
import time
from pathlib import Path
from common import RUNS, SCOPE, AGENT, record, pct, dump, dir_bytes
from iald_memory import MemoryStore

N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
root = RUNS / ('e1_growth_N%d' % N)
if root.exists():
    shutil.rmtree(root)
archive = root / 'arquivo_D'
store = MemoryStore(root / 'state', snapshot_archive_dir=archive)
store.ensure_context('ctx.growth', objective='E1 growth objective ' * 20, scope=SCOPE, actor=AGENT,
                     constraints={'no_gate': True})
times, checkpoints = [], []
rev = 0
for i in range(1, N + 1):
    kind = 'fact' if i % 2 else 'candidate'
    ch = {'records': [record(i, 300, kind)]}
    if i % 10 == 0:
        ch['flow'] = {'phase': 'fase %d' % i, 'next_action': 'seguir %d' % i,
                      'handles': [{'id': 'h%d' % (i % 7), 'estado': i}]}
    t0 = time.perf_counter()
    rec = store.transition('ctx.growth', SCOPE, rev, 'e%05d' % i, AGENT, ch)
    times.append(time.perf_counter() - t0)
    rev = rec['revision']
    if i % 100 == 0:
        cp = {'n': i}
        t0 = time.perf_counter(); store.get('ctx.growth', SCOPE); cp['get_s'] = round(time.perf_counter() - t0, 4)
        t0 = time.perf_counter(); pr = store.project('ctx.growth', SCOPE, max_chars=4000000, current_input='registro fase seguir')
        cp['project_s'] = round(time.perf_counter() - t0, 4); cp['project_chars'] = pr['actual_chars']
        cp['project_required_chars'] = pr['required_chars']
        t0 = time.perf_counter(); v = store.verify('ctx.growth', SCOPE); cp['verify_s'] = round(time.perf_counter() - t0, 4)
        cp['verify_ok'] = v['ok']
        cp['median_last100_ms'] = round(pct(times[-100:], 0.5) * 1000, 2)
        cp['p90_last100_ms'] = round(pct(times[-100:], 0.9) * 1000, 2)
        cp['max_last100_ms'] = round(max(times[-100:]) * 1000, 2)
        cp['db_bytes'] = (root / 'state' / 'memory.sqlite3').stat().st_size
        cp['journal'] = dir_bytes(root / 'state' / 'journal')
        cp['snapshots_local'] = dir_bytes(root / 'state' / 'snapshots')
        cp['snapshots_archive'] = dir_bytes(archive)
        checkpoints.append(cp)
        print(cp, flush=True)
# a projection overflow probe: required (facts) alone vs. a small budget
try:
    store.project('ctx.growth', SCOPE, max_chars=12000)
    overflow = 'no'
except Exception as exc:  # expected: ProjectionOverflow once required facts exceed 12000 chars
    overflow = type(exc).__name__
t0 = time.perf_counter(); vd = store.verify('ctx.growth', SCOPE, deep=True); deep_s = time.perf_counter() - t0
out = {'N': N, 'median_ms': round(pct(times, 0.5) * 1000, 2), 'p90_ms': round(pct(times, 0.9) * 1000, 2),
       'max_ms': round(max(times) * 1000, 2), 'checkpoints': checkpoints, 'project_12000': overflow,
       'verify_deep_s': round(deep_s, 3), 'verify_deep_ok': vd['ok'], 'journal_lines': vd['journal_lines'],
       'event_count': vd['event_count'], 'snapshot_rows': vd['snapshot_rows'],
       'replay_from_revision_fast': store.verify('ctx.growth', SCOPE)['replay_from_revision']}
dump(RUNS / ('e1_growth_N%d.json' % N), out)
print({k: v for k, v in out.items() if k != 'checkpoints'})
