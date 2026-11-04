"""Revisor independente F0.3 v407 - Q4 (somente leitura): fotografia propria da arvore canonical_memory e diff contra BASELINE_ANTES / BASELINE_APOS_PREPARE.
Uso: python rev_q4.py <tag>   -> escreve review\\REV_BASELINE_<tag>.json e review\\REV_DIFF_<tag>.json"""
import os, sys, json, hashlib, time
sys.dont_write_bytecode = True
from pathlib import Path

BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as cm

W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
REV = W / 'review'
EPOCH = 'v407_4323b401f15cc971'
tag = sys.argv[1] if len(sys.argv) > 1 else 'AGORA'
root = BASE / 'state' / 'canonical_memory'
assert Path(cm.ACTIVE).parent == root


def sha(b):
    return hashlib.sha256(b).hexdigest()


t0 = time.time()
arquivos = {}
for p in sorted(root.rglob('*')):
    if p.is_file():
        st = p.stat()
        rel = str(p.relative_to(root))
        item = {'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns, 'is_symlink': p.is_symlink()}
        if st.st_size <= 4 * 1024 * 1024:
            item['sha256'] = sha(p.read_bytes())
        arquivos[rel] = item
dirs = {}
for p in sorted(root.rglob('*')):
    if p.is_dir():
        dirs[str(p.relative_to(root))] = p.stat().st_mtime_ns
releases = sorted(d.name for d in Path(cm.RELEASES).iterdir() if d.is_dir())
manifests = {}
for r in releases:
    mp = Path(cm.RELEASES) / r / 'manifest.json'
    if mp.exists():
        manifests[r] = sha(mp.read_bytes())
active_raw = Path(cm.ACTIVE).read_bytes()
snap = {'raiz': str(root), 'tag': tag, 'taken_local': time.strftime('%Y-%m-%d %H:%M:%S'), 'active_sha256': sha(active_raw), 'active_bytes': len(active_raw),
        'active': json.loads(active_raw), 'releases': releases, 'manifests_sha256': manifests, 'n_arquivos': len(arquivos), 'arquivos': arquivos, 'dirs_mtime_ns': dirs}
(REV / ('REV_BASELINE_' + tag + '.json')).write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding='utf-8')


def diff(a, b, label, expected_prefix=None):
    A, B = a['arquivos'], b['arquivos']
    novos = sorted(set(B) - set(A))
    removidos = sorted(set(A) - set(B))
    alterados = sorted(k for k in set(A) & set(B) if (A[k]['bytes'], A[k].get('sha256'), A[k]['mtime_ns']) != (B[k]['bytes'], B[k].get('sha256'), B[k]['mtime_ns']))
    fora = [k for k in novos if expected_prefix and not k.replace('\\', '/').startswith(expected_prefix)]
    mudou = [r for r in a['manifests_sha256'] if a['manifests_sha256'][r] != b['manifests_sha256'].get(r)]
    # directory mtimes: which directories changed (informational; dirs change when entries are added)
    ad = a.get('dirs_mtime_ns') or {}
    bd = b.get('dirs_mtime_ns') or {}
    dir_changed = sorted(k for k in set(ad) & set(bd) if ad[k] != bd[k])
    return {
        'label': label, 'antes_n': len(A), 'depois_n': len(B),
        'novos': novos, 'n_novos': len(novos), 'removidos': removidos, 'alterados': alterados,
        'novos_fora_do_prefixo_esperado': fora,
        'active_sha_antes': a['active_sha256'], 'active_sha_depois': b['active_sha256'], 'active_inalterado': a['active_sha256'] == b['active_sha256'],
        'active_antes': a['active'], 'active_depois': b['active'],
        'releases_antes': len(a['releases']), 'releases_depois': len(b['releases']),
        'novos_releases': sorted(set(b['releases']) - set(a['releases'])),
        'manifests_de_releases_anteriores_alterados': mudou,
        'ACTIVE_family_files_changed_or_new': sorted(k for k in set(novos) | set(alterados) if k.startswith('ACTIVE')),
        'worker_lock_unchanged': (lambda x, y: x is not None and y is not None and (x['bytes'], x.get('sha256'), x['mtime_ns']) == (y['bytes'], y.get('sha256'), y['mtime_ns']))(A.get('ACTIVE.json.worker.lock'), B.get('ACTIVE.json.worker.lock')),
        'dirs_with_changed_mtime(only_if_both_have_dirs)': dir_changed,
    }


res = {}
ant = json.loads((W / 'BASELINE_ANTES.json').read_bytes())
apos = json.loads((W / 'BASELINE_APOS_PREPARE.json').read_bytes())
prefix = 'releases/' + EPOCH + '/'
res['agora_vs_ANTES'] = diff(ant, snap, 'AGORA vs BASELINE_ANTES (orquestrador)', prefix)
res['agora_vs_APOS_PREPARE'] = diff(apos, snap, 'AGORA vs BASELINE_APOS_PREPARE (orquestrador)', prefix)
res['apos_prepare_vs_ANTES'] = diff(ant, apos, 'BASELINE_APOS_PREPARE vs BASELINE_ANTES (reconferido por mim)', prefix)

# the 17 new files: all under the new release dir? sha of the small ones vs. their recorded pins
new_rel = res['agora_vs_ANTES']['novos']
res['novos_todos_sob_release_novo'] = all(k.replace('\\', '/').startswith(prefix) for k in new_rel)
res['n_novos_esperado_17'] = len(new_rel) == 17

# self-consistency of EVERY older release (load() hashes the index and all 13 sources against the release's own manifest)
selfcheck = {}
for r in releases:
    d = Path(cm.RELEASES) / r
    try:
        m, fresh = cm.load(d, refresh=False)
        selfcheck[r] = {'ok': True, 'freshness': fresh, 'chunks': m['chunks'], 'generation16': m['generation'][:16]}
    except Exception as ex:  # noqa
        selfcheck[r] = {'ok': False, 'error': type(ex).__name__ + ': ' + str(ex)[:200]}
res['cm_load_selfcheck_all_releases'] = selfcheck
res['elapsed_s'] = round(time.time() - t0, 1)
(REV / ('REV_DIFF_' + tag + '.json')).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

for k in ('agora_vs_ANTES', 'agora_vs_APOS_PREPARE', 'apos_prepare_vs_ANTES'):
    r = res[k]
    print('==', r['label'])
    print('   antes %d depois %d | novos %d removidos %d alterados %d | novos fora do prefixo %d' % (r['antes_n'], r['depois_n'], r['n_novos'], len(r['removidos']), len(r['alterados']), len(r['novos_fora_do_prefixo_esperado'])))
    print('   ACTIVE inalterado:', r['active_inalterado'], r['active_sha_antes'][:16], '->', r['active_sha_depois'][:16], '| novos releases:', r['novos_releases'])
    print('   manifests de releases anteriores alterados:', r['manifests_de_releases_anteriores_alterados'], '| ACTIVE-family changed/new:', r['ACTIVE_family_files_changed_or_new'], '| worker.lock unchanged:', r['worker_lock_unchanged'])
    if r['removidos']:
        print('   REMOVIDOS:', r['removidos'][:10])
    if r['alterados']:
        print('   ALTERADOS:', r['alterados'][:10])
print('novos_todos_sob_release_novo:', res['novos_todos_sob_release_novo'], '| n_novos==17:', res['n_novos_esperado_17'])
print('self-check (cm.load) por release:')
for r, v in selfcheck.items():
    print('  ', r, v)
print('elapsed', res['elapsed_s'])
