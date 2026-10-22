# Revisor B: production-size rehearsal on a CONSISTENT COPY of the bank (sqlite backup API, source opened read-only).
# Migration + one due byte snapshot timed under the writer lock. Archive dir redirected into the sandbox.
# Prints metadata and timings only, never record text.
import os, sys, json, time, sqlite3, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), 'copia', 'MEMORIA_IALD', 'lib')
sys.path.insert(0, LIB)
SB = os.path.join(HERE, 'sb_prodsize')
if os.path.exists(SB):
    subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', SB])
state = os.path.join(SB, 'state'); os.makedirs(state)
archive = os.path.join(SB, 'archive_D'); os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR'] = archive
R = {}
src_path = r'C:\IALD\MEMORIA_IALD\state\memory.sqlite3'.replace(chr(92), '/')
t = time.perf_counter()
src = sqlite3.connect('file:' + src_path + '?mode=ro', uri=True)
dst = sqlite3.connect(os.path.join(state, 'memory.sqlite3'))
src.backup(dst); dst.execute('PRAGMA journal_mode=DELETE'); dst.commit(); dst.close(); src.close()
R['copy_seconds'] = round(time.perf_counter() - t, 2)
R['copy_bytes'] = os.path.getsize(os.path.join(state, 'memory.sqlite3'))
from iald_memory import migrate, MemoryStore
t = time.perf_counter()
try:
    dry = migrate.migrate(state, apply=False)
    R['dry_run'] = {'ok': True, 'seconds': round(time.perf_counter() - t, 2), 'contexts': len(dry.get('contexts', {}))}
except Exception as e:
    R['dry_run'] = {'ok': False, 'error': repr(e)[:300]}
t = time.perf_counter()
try:
    rec = migrate.migrate(state, apply=True, snapshot_archive_dir=archive)
    R['apply'] = {'ok': rec.get('ok'), 'seconds': round(time.perf_counter() - t, 2), 'head_mismatches': rec.get('head_mismatches'),
                  'backup_bytes': rec['backup']['bytes'], 'backup_sha16': rec['backup']['sha256'][:16],
                  'backup_equals_pre_copy': None, 'db_bytes_after': rec['after']['db_bytes'],
                  'journal_files': rec['after']['journal_files'],
                  'journal_ok_all': all(v['journal_ok'] for v in rec['verify_after'].values())}
except Exception as e:
    R['apply'] = {'ok': False, 'error': repr(e)[:400], 'seconds': round(time.perf_counter() - t, 2)}
# Timed due snapshot at production size: force the policy counter to 49, then one transition.
try:
    st = MemoryStore(state, snapshot_archive_dir=archive)
    c = sqlite3.connect(os.path.join(state, 'memory.sqlite3'), isolation_level=None)
    pol = json.loads(c.execute('SELECT policy_json FROM snapshot_policy WHERE id=1').fetchone()[0])
    pol['mutations_since_snapshot'] = 49
    c.execute('UPDATE snapshot_policy SET policy_json=? WHERE id=1', (json.dumps(pol, sort_keys=True),)); c.close()
    scope = {'house': 'IALD', 'principal': 'revisor_b'}
    st.ensure_context('revisor_b_probe', objective='sonda de tempo do revisor B', scope=scope, actor={'id': 'rb', 'kind': 'agent'})
    timings = []
    for i in range(1, 6):
        # each loop: force counter so that the transition is a due snapshot
        c = sqlite3.connect(os.path.join(state, 'memory.sqlite3'), isolation_level=None)
        pol = json.loads(c.execute('SELECT policy_json FROM snapshot_policy WHERE id=1').fetchone()[0])
        pol['mutations_since_snapshot'] = 49
        c.execute('UPDATE snapshot_policy SET policy_json=? WHERE id=1', (json.dumps(pol, sort_keys=True),)); c.close()
        t = time.perf_counter()
        st.transition('revisor_b_probe', scope, i - 1, 'probe%d' % i, {'id': 'rb', 'kind': 'agent'},
                      {'flow': {'phase': 'p%d' % i, 'next_action': 'n'}})
        timings.append(round(time.perf_counter() - t, 2))
    t = time.perf_counter()
    st.transition('revisor_b_probe', scope, 5, 'probe_plain', {'id': 'rb', 'kind': 'agent'}, {'flow': {'phase': 'plain', 'next_action': 'n'}})
    R['snapshot_due_transition_seconds'] = timings
    R['plain_transition_seconds'] = round(time.perf_counter() - t, 3)
    R['local_snapshots'] = len([n for n in os.listdir(os.path.join(state, 'snapshots')) if n.startswith('memory.sqlite3.snap_') and not n.endswith('.sha256')])
    R['archived_snapshots'] = len([n for n in os.listdir(archive) if n.startswith('memory.sqlite3.snap_') and not n.endswith('.sha256')]) if os.path.exists(archive) else 0
except Exception as e:
    R['snapshot_probe_error'] = repr(e)[:300]
with open(os.path.join(HERE, 't6_result.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
