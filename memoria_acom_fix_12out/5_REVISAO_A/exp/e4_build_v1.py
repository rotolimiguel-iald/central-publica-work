# -*- coding: utf-8 -*-
"""E4 step 1: a LARGE synthetic v1 database (frozen v1 code = installed store.py 2d4f6214fa433534).

Rows are computed with the v1 functions (_changes/_apply/_dump/_event_hash) and inserted directly (the v1
per-mutation whole-file backup is skipped for speed; the rows are byte-identical to what v1 writes).
usage: e4_build_v1.py OUT_STATE_DIR BIG_EVENTS RECORD_CHARS
"""
from __future__ import annotations
import hashlib
import json
import sys
import time
from pathlib import Path
from common import V1, SCOPE, AGENT, dump
sys.path.insert(0, str(V1))
import store_v1_frozen as v1  # noqa: E402

out = Path(sys.argv[1]); big = int(sys.argv[2]); chars = int(sys.argv[3])
assert hashlib.sha256((V1 / 'store_v1_frozen.py').read_bytes()).hexdigest().startswith('2d4f6214fa433534')
out.mkdir(parents=True, exist_ok=True)
v1.MemoryStore._backup = lambda self: None   # build speed only; rows identical
st = v1.MemoryStore(out)
plan = [('ctx.big', big, 'facts'), ('app:conv.0001', 300, 'mixed'), ('flow.only', 150, 'flow'), ('small.empty', 0, 'facts')]
for ctx, n, kind in plan:
    st.ensure_context(ctx, objective=('Objetivo sintético de %s — inscrição original com acentuação e emoji ✓ ' % ctx) * 8,
                      scope=SCOPE, actor=AGENT, constraints={'casa': 'IALD', 'gate_authority': False})
st.ensure_context('child.of.big', objective='filho', scope=SCOPE, actor=AGENT,
                  constraints={'casa': 'IALD', 'gate_authority': False}, parent_id='ctx.big')
conn = st._connect()
t0 = time.time()
conn.execute('BEGIN IMMEDIATE')
totals = {}
for ctx, n, kind in plan:
    snap, rows = st._read(conn, ctx, SCOPE)
    state = {'q': snap['q'], 'p': snap['p']}
    previous = snap['receipt']['event_hash']
    total_state = 0
    for i in range(1, n + 1):
        actor = AGENT if (kind != 'mixed' or i % 3) else {'id': 'modelo.x', 'kind': 'model'}
        if kind == 'flow':
            ch = {'flow': {'phase': 'fase %d' % i, 'next_action': 'próxima ação %d' % i,
                           'handles': [{'id': 'h%d' % (i % 5), 'n': i, 'txt': 'á' * 50}]}}
        else:
            rec = {'id': '%s_r%05d' % (ctx.replace(':', '_'), i), 'kind': 'fact', 'statute': 'REAL',
                   'text': ('registro %d — %s ' % (i, ctx)) + ('dados ' * (chars // 6)),
                   'sources': [{'kind': 'artifact', 'ref': 'synthetic/%d' % i}]}
            if actor['kind'] == 'model':
                rec.update(kind='candidate', statute='DECLARADO', sources=[{'kind': 'model', 'ref': 'm/%d' % i}])
            if i > 5 and i % 50 == 0 and actor['kind'] != 'model':
                rec.update(kind='erratum', supersedes='%s_r%05d' % (ctx.replace(':', '_'), i - 5))
            ch = {'records': [rec]}
            if i % 25 == 0 and actor['kind'] != 'model':
                ch['flow'] = {'phase': 'p%d' % i}
        norm = v1._changes(ch, actor)
        state = v1._apply(state, norm)
        sj = v1._dump(state)
        ssha = v1._sha(sj.encode('utf-8'))
        at = v1._now()
        aj, cj = v1._dump(actor), v1._dump(norm)
        eh = v1._event_hash(ctx, i, 'ev%05d' % i, aj, cj, ssha, previous, at)
        conn.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)', (ctx, i, 'ev%05d' % i, aj, cj, sj, ssha, previous, eh, at))
        previous = eh
        total_state += len(sj)
    totals[ctx] = {'events': n, 'sum_state_json_chars': total_state, 'final_state_chars': len(v1._dump(state))}
conn.commit()
conn.close()
build_s = time.time() - t0
# v1 must still read every context (public API)
check = {}
for ctx, n, kind in plan + [('child.of.big', 0, '')]:
    check[ctx] = st.verify(ctx, SCOPE)['event_count']
db = out / 'memory.sqlite3'
res = {'db_bytes': db.stat().st_size, 'build_s': round(build_s, 1), 'totals': totals, 'v1_verify_event_counts': check,
       'events_total': sum(check.values()), 'sha256': hashlib.sha256(db.read_bytes()).hexdigest()}
dump(out.parent / 'BUILD_V1.json', res)
print(json.dumps(res, ensure_ascii=False))
