"""Revisor independente F0.3 v407 - Q5 (somente leitura): itens de Chatgpt\\ com mtime >= 2026-11-04 07:30 local.
Uso: python rev_q5.py <saida.json> [limiar 'YYYY-MM-DD HH:MM']"""
import os, sys, json, time
from datetime import datetime
from pathlib import Path
sys.dont_write_bytecode = True

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
NEW_RELEASE = ROOT / 'IALD_ORQUESTRACAO_20260923' / 'state' / 'canonical_memory' / 'releases' / 'v407_4323b401f15cc971'
thr_s = sys.argv[2] if len(sys.argv) > 2 else '2026-11-04 07:30'
thr = datetime.strptime(thr_s, '%Y-%m-%d %H:%M').timestamp()
out_path = Path(sys.argv[1])
t0 = time.time()
hits = []
n_entries = 0
n_files = 0
n_dirs = 0
errors = []
excluded_new_release = {'files': 0, 'dirs': 0}
stack = [(str(ROOT), 0)]
newrel = str(NEW_RELEASE).lower()
while stack:
    d, depth = stack.pop()
    try:
        with os.scandir(d) as it:
            for e in it:
                n_entries += 1
                try:
                    isdir = e.is_dir(follow_symlinks=False)
                    st = e.stat(follow_symlinks=False)
                except OSError as ex:
                    errors.append((e.path, repr(ex)))
                    continue
                if isdir:
                    n_dirs += 1
                else:
                    n_files += 1
                low = e.path.lower()
                in_new = low == newrel or low.startswith(newrel + os.sep)
                if in_new:
                    excluded_new_release['dirs' if isdir else 'files'] += 1
                if st.st_mtime >= thr and not in_new:
                    hits.append({'path': e.path, 'type': 'd' if isdir else 'f', 'depth': depth + 1, 'bytes': st.st_size,
                                 'mtime': datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S.%f')})
                if isdir and not e.is_symlink():
                    stack.append((e.path, depth + 1))
    except OSError as ex:
        errors.append((d, repr(ex)))
hits.sort(key=lambda h: h['path'])
res = {'root': str(ROOT), 'threshold_local': thr_s, 'elapsed_s': round(time.time() - t0, 1),
       'n_entries_walked': n_entries, 'n_files': n_files, 'n_dirs': n_dirs,
       'excluded_new_release_entries': excluded_new_release, 'errors': errors[:20], 'n_errors': len(errors),
       'hits_all_depths': hits,
       'hits_depth_le_4': [h for h in hits if h['depth'] <= 4],
       'hits_under_canonical_memory_outside_new_release': [h for h in hits if os.sep + 'canonical_memory' in h['path'] or h['path'].endswith('canonical_memory')]}
out_path.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('walked', n_entries, 'entries (%d files, %d dirs) in %.1fs; errors %d' % (n_files, n_dirs, res['elapsed_s'], len(errors)))
print('excluded (new release):', excluded_new_release)
print('HITS (all depths):', len(hits), '| depth<=4:', len(res['hits_depth_le_4']), '| under canonical_memory outside new release:', len(res['hits_under_canonical_memory_outside_new_release']))
for h in hits[:120]:
    print(h['mtime'], h['type'], 'd%d' % h['depth'], h['bytes'], h['path'][len(str(ROOT)) + 1:])
if len(hits) > 120:
    print('... (%d more in JSON)' % (len(hits) - 120))
