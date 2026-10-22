# -*- coding: utf-8 -*-
"""E4 step 2: migrate the large synthetic v1 database with the CANDIDATE CLI; measure time, peak memory, receipts;
then post-migration load on the legacy context (latency incl. byte snapshots of a ~500 MB file under the writer lock).

usage: e4_migrate.py            (orchestrator)
       e4_migrate.py wrap ARGS  (internal: runs migrar_para_delta.main(ARGS) and prints peak working set)
"""
from __future__ import annotations
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from common import RUNS, MEM_CAND, V1, SCOPE, AGENT, record, pct, dump, dir_bytes, sha256_file


def peak_ws():
    class PMC(ctypes.Structure):
        _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t),
                    ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t),
                    ('PeakPagefileUsage', ctypes.c_size_t)]
    pmc = PMC(); pmc.cb = ctypes.sizeof(PMC)
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
    return pmc.PeakWorkingSetSize


def wrap(args):
    sys.path.insert(0, str(MEM_CAND))
    import migrar_para_delta
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = migrar_para_delta.main(args)
    print(json.dumps({'rc': rc, 'peak_working_set': peak_ws(), 'stdout_tail': buf.getvalue()[-6000:]}))


def run_wrap(args):
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', __file__, 'wrap'] + [str(a) for a in args],
                       capture_output=True, timeout=7200)
    out = json.loads(p.stdout.decode().strip().splitlines()[-1])
    out['wall_s'] = round(time.time() - t0, 2)
    out['stderr_tail'] = p.stderr.decode()[-800:]
    return out


def main():
    src = RUNS / 'e4_v1' / 'state'
    work = RUNS / 'e4_mig'
    if work.exists():
        shutil.rmtree(work)
    state = work / 'state'
    state.mkdir(parents=True)
    shutil.copyfile(src / 'memory.sqlite3', state / 'memory.sqlite3')
    v1_sha = sha256_file(state / 'memory.sqlite3')
    res = {'v1_db_bytes': (state / 'memory.sqlite3').stat().st_size, 'v1_sha256': v1_sha}
    arch = work / 'arquivo_D' / 'snapshots'
    dry = run_wrap(['--state', state, '--snapshot-archive-dir', arch])
    res['dry_run'] = {k: dry[k] for k in ('rc', 'peak_working_set', 'wall_s')}
    res['dry_run_db_unchanged'] = sha256_file(state / 'memory.sqlite3') == v1_sha and not (state / 'journal').exists()
    ap = run_wrap(['--state', state, '--apply', '--receipt', work / 'RECIBO_MIGRACAO.json',
                   '--second-copy-dir', work / 'arquivo_D' / 'pre_v2', '--snapshot-archive-dir', arch])
    res['apply'] = {k: ap[k] for k in ('rc', 'peak_working_set', 'wall_s', 'stderr_tail')}
    rec = json.loads((work / 'RECIBO_MIGRACAO.json').read_text(encoding='utf-8'))
    res['apply']['ok'] = rec.get('ok'); res['apply']['head_mismatches'] = rec.get('head_mismatches')
    res['apply']['backup'] = rec.get('backup')
    res['apply']['backup_equals_v1'] = rec['backup']['sha256'] == v1_sha
    res['apply']['after'] = {k: rec['after'].get(k) for k in ('db_bytes', 'schema_version', 'events', 'legacy_events',
                                                               'delta_events', 'snapshot_rows', 'context_state_rows', 'journal_files')}
    res['journal_bytes'] = dir_bytes(state / 'journal')
    again = run_wrap(['--state', state, '--apply', '--snapshot-archive-dir', arch])
    res['second_apply'] = {'rc': again['rc'], 'already_migrated': '"already_migrated": true' in again['stdout_tail'], 'wall_s': again['wall_s']}
    deep = run_wrap(['--state', state, '--verify-only', '--deep', '--snapshot-archive-dir', arch])
    res['verify_only_deep'] = {k: deep[k] for k in ('rc', 'peak_working_set', 'wall_s')}
    # v1 frozen code must refuse the migrated database
    sys.path.insert(0, str(V1))
    import store_v1_frozen as v1
    try:
        v1.MemoryStore(state).get('ctx.big', SCOPE)
        res['v1_refuses'] = False
    except Exception as exc:
        res['v1_refuses'] = type(exc).__name__ + ': ' + str(exc)[:120]
    # post-migration load on the legacy context
    sys.path.insert(0, str(MEM_CAND / 'lib'))
    from iald_memory import MemoryStore
    store = MemoryStore(state, snapshot_archive_dir=arch)
    lat, snap_lat = [], []
    t0 = time.perf_counter(); g = store.get('ctx.big', SCOPE); res['get_big_s'] = round(time.perf_counter() - t0, 3)
    rev = g['revision']
    for i in range(1, 211):
        before = len(list((state / 'snapshots').glob('memory.sqlite3.snap_*'))) if (state / 'snapshots').exists() else 0
        t0 = time.perf_counter()
        r = store.transition('ctx.big', SCOPE, rev, 'post%04d' % i, AGENT, {'records': [dict(record(i, 200), id='post_%04d' % i)]})
        dt = time.perf_counter() - t0
        rev = r['revision']
        after = len(list((state / 'snapshots').glob('memory.sqlite3.snap_*')))
        (snap_lat if after != before or i % 50 == 0 else lat).append(dt)
    res['post_transition'] = {'n': 210, 'median_ms': round(pct(lat, 0.5) * 1000, 1), 'p90_ms': round(pct(lat, 0.9) * 1000, 1),
                              'snapshot_transitions_s': [round(x, 2) for x in snap_lat]}
    t0 = time.perf_counter(); store.project('ctx.big', SCOPE, max_chars=4_000_000); res['project_big_s'] = round(time.perf_counter() - t0, 3)
    t0 = time.perf_counter(); v = store.verify('ctx.big', SCOPE, deep=True); res['verify_deep_big_s'] = round(time.perf_counter() - t0, 2)
    res['verify_deep_big'] = {k: v[k] for k in ('ok', 'legacy_events', 'delta_events', 'journal_ok', 'replay_from_revision')}
    res['db_bytes_after_load'] = (state / 'memory.sqlite3').stat().st_size
    res['snapshots_local'] = dir_bytes(state / 'snapshots'); res['archive'] = dir_bytes(work / 'arquivo_D')
    res['state_listing'] = sorted(p.name for p in state.iterdir())
    dump(RUNS / 'e4_migrate.json', res)
    print(json.dumps(res, ensure_ascii=False, default=str))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'wrap':
        wrap(sys.argv[2:])
    else:
        main()
