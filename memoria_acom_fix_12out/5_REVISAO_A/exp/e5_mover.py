# -*- coding: utf-8 -*-
"""E5: mover_backups_antigos.py (candidate) with 50 synthetic legacy backups, plus failure injection.

(a) dry-run moves nothing; (b) a source held open by another process (no FILE_SHARE_DELETE) -> visible abort,
source kept, re-run completes idempotently; (c) full run --keep 3: sha256 of every moved file equals the source
hash taken before; manifest lines; kept = 3 newest; (d) destination already holding a DIFFERENT file with the same
name; (e) throughput.
"""
from __future__ import annotations
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path
from common import RUNS, MEM_CAND, dump, sha256_file

BASE = RUNS / 'e5_mover'
SCRIPT = MEM_CAND / 'mover_backups_antigos.py'


def run(args):
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(SCRIPT)] + [str(a) for a in args], capture_output=True, timeout=3600)
    try:
        out = json.loads(p.stdout.decode())
    except ValueError:
        out = {'raw': p.stdout.decode()[-800:]}
    return p.returncode, out, round(time.time() - t0, 2), p.stderr.decode()[-600:]


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    state, dest = BASE / 'state', BASE / 'D' / 'backups_ate_20261012'
    state.mkdir(parents=True)
    rnd = random.Random(13)
    names = []
    total = 0
    for k in range(50):
        size = rnd.randint(8, 40) * 1024 * 1024 + rnd.randint(0, 4095)
        name = 'memory.sqlite3.bak_202610%02d_%02d%02d%02d_%06d_%08x' % (10 + k // 20, k % 24, k % 60, (k * 7) % 60, k * 1000, rnd.getrandbits(32))
        data = os.urandom(1024) * (size // 1024) + os.urandom(size % 1024)
        (state / name).write_bytes(data)
        names.append(name); total += size
    (state / 'memory.sqlite3').write_bytes(b'SQLite format 3\x00' + b'\x00' * 4080)
    (state / 'memory.sqlite3.pre_v2_20261013_000000_000000').write_bytes(b'pre')
    before = {n: sha256_file(state / n) for n in names}
    other = {p.name: sha256_file(p) for p in state.iterdir() if p.name not in before}
    res = {'files': 50, 'bytes': total}
    rc, out, s, err = run(['--state', state, '--dest', dest, '--keep', 3, '--dry-run'])
    res['a_dry_run'] = {'rc': rc, 'to_move': out.get('to_move'), 'moved': out.get('moved'),
                        'nothing_changed': all((state / n).exists() for n in names) and not dest.exists()}
    # (d) a different file with the same name already in the destination
    dest.mkdir(parents=True)
    victim = sorted(names)[5]
    (dest / victim).write_bytes(b'conteudo diferente pre-existente no destino')
    # (b) hold one source open in another process (CPython open = share read/write, no delete)
    held = sorted(names)[20]
    holder = subprocess.Popen([sys.executable, '-c', 'import sys,time; f=open(sys.argv[1],"rb"); print("open",flush=True); time.sleep(600)',
                               str(state / held)], stdout=subprocess.PIPE)
    holder.stdout.readline()
    rc, out, s, err = run(['--state', state, '--dest', dest, '--keep', 3])
    res['b_held_source'] = {'rc': rc, 'moved': out.get('moved'), 'failed': out.get('failed'), 'seconds': s,
                            'held_source_still_in_state': (state / held).exists(),
                            'held_copy_in_dest': (dest / held).exists(),
                            'manifest_lines': out.get('manifest_lines')}
    holder.kill(); holder.wait()
    rc, out, s, err = run(['--state', state, '--dest', dest, '--keep', 3])
    res['c_rerun'] = {'rc': rc, 'moved': out.get('moved'), 'moved_bytes': out.get('moved_bytes'), 'failed': out.get('failed'),
                      'kept': out.get('kept'), 'manifest_lines': out.get('manifest_lines'), 'seconds': s,
                      'already_archived_counter': out.get('already_archived')}
    moved = [n for n in names if not (state / n).exists()]
    kept = sorted(n for n in names if (state / n).exists())
    res['c_check'] = {'moved_files': len(moved), 'kept_files': kept, 'kept_are_3_newest': kept == sorted(names)[-3:],
                      'all_dest_sha_equal': all(sha256_file(dest / n) == before[n] for n in moved),
                      'others_untouched': all(sha256_file(state / n) == h for n, h in other.items()),
                      'victim_overwritten_by_source': sha256_file(dest / victim) == before[victim]}
    lines = [json.loads(l) for l in (dest / 'MANIFEST.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    res['c_manifest'] = {'lines': len(lines), 'unique_names': len({l['name'] for l in lines}),
                         'all_sha_match': all(before[l['name']] == l['sha256'] for l in lines)}
    secs = res['b_held_source']['seconds'] + res['c_rerun']['seconds']
    res['e_throughput_MBps'] = round(total / 1048576 / secs, 1)
    res['e_extrapolated_95GB_minutes_C_to_C'] = round(95_123_988_480 / (total / secs) / 60, 1)
    dump(RUNS / 'e5_mover.json', res)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == '__main__':
    main()
