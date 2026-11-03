"""Reviewer (sonnet-app-v405-revisor) sources group 2: (a) re-hash the 36 custody artifacts against CUSTODY_MANIFEST and the seal; (b) staged release files == git blobs at the pinned commit == binding;
(c) every manifest entry URL decodes to a path TRACKED at the pinned commit (no inferred URL) and points to the pinned commit; (d) V404 pipeline folder untouched by the v405 build;
(e) the G1 custody plan state (read-only) to separate custody in progress from concluded. No network. Read-only."""
import hashlib, json, subprocess, sys, os, time
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.dont_write_bytecode = True
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
W4 = Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
ST = W / 'app/science/memory_stage'
sh = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
C1 = rd(W / 'app/RELEASE.json')['espelho_commit']


def git(*a):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + REPO.as_posix(), '-c', 'core.quotepath=false', '-C', str(REPO), *a])


out = {}
# (a) custody artifacts
cm_raw = (V / 'CUSTODY_MANIFEST.json').read_bytes()
cm = json.loads(cm_raw)
sv = rd(W / 'sources_verified.json')
seal = rd(V / 'um_absoluto_selo.json')
bad = []
n_seal = 0
for e in cm['artifacts']:
    blob = (V / e['file']).read_bytes()
    if sh(blob) != e['sha256']:
        bad.append(('manifest', e['file']))
    if e['file'] in seal['sha256']:
        n_seal += 1
        if sh(blob) != seal['sha256'][e['file']]:
            bad.append(('seal', e['file']))
sv_map = {a['file']: a for a in sv['artifacts']}
for e in cm['artifacts']:
    a = sv_map.get(e['file'])
    if not a or a['sha256'] != e['sha256'] or a['bytes'] != (V / e['file']).stat().st_size:
        bad.append(('sources_verified', e['file']))
out['custody'] = {'manifest_sha256': sh(cm_raw), 'equals_sources_verified_pin': sh(cm_raw) == sv['custody_manifest']['sha256'], 'artifacts': len(cm['artifacts']), 'sources_verified_artifacts': len(sv['artifacts']), 'also_pinned_by_seal': n_seal, 'mismatches': bad,
                  'manifest_declares_mismatches': cm['mismatches'], 'version': cm['version'], 'um_py_pin': cm['um_py_pin'], 'gate': cm['gate'], 'gate_identico_ao_da_v404': cm['gate_identico_ao_da_v404'],
                  'seal_gate_equals_manifest_gate': seal.get('qg_closure_verdict') == cm['gate'], 'kernel_counts': cm['kernel'], 'seal_timestamp': seal['timestamp']}
# (b) staged release files vs git blobs vs binding
bind = rd(W / 'app/PUBLIC_GIT_BINDING.json')['sources']
rows = []
for rel, row in bind.items():
    staged = ST / 'release' / rel
    blob = git('show', C1 + ':' + rel)
    rows.append({'rel': rel, 'staged_eq_blob': staged.read_bytes() == blob, 'blob_sha_eq_binding': sh(blob) == row['sha256']})
out['staged_release_vs_git'] = {'all_ok': all(r['staged_eq_blob'] and r['blob_sha_eq_binding'] for r in rows), 'n': len(rows)}
# (c) entry URLs
tracked = set(git('ls-tree', '-r', '--name-only', '-z', C1).decode().split('\0'))
m = rd(ST / 'manifest_staged.json')
url_rows = []
for row in m['entries'] + [m['published_evidence'][k] for k in ('program', 'seal', 'result', 'proof_manifest')]:
    u = urlparse(row['url'])
    parts = u.path.split('/')
    commit_in_url = parts[3]
    rel = unquote('/'.join(parts[4:]))
    url_rows.append({'id': row.get('id') or Path(rel).name, 'host_ok': u.netloc == 'raw.githubusercontent.com', 'repo_ok': parts[1:3] == ['rotolimiguel-iald', 'the_boundary'], 'commit_is_pinned': commit_in_url == C1, 'path_tracked_at_pinned': rel in tracked,
                     'public_sha256_eq_staged': (sh(Path(row['path']).read_bytes()) == row['public_sha256']) if 'public_sha256' in row else None})
out['manifest_urls'] = {'all_ok': all(r['host_ok'] and r['repo_ok'] and r['commit_is_pinned'] and r['path_tracked_at_pinned'] and r['public_sha256_eq_staged'] in (True, None) for r in url_rows), 'rows': url_rows}
hyp = m['published_evidence'].get('hypothesis_sources', [])
hy = []
for row in hyp:
    u = urlparse(row['url'])
    rel = unquote('/'.join(u.path.split('/')[4:]))
    hy.append({'catalog_path': row.get('catalog_path'), 'commit_is_pinned': u.path.split('/')[3] == C1, 'tracked': rel in tracked})
out['hypothesis_source_urls'] = {'n': len(hy), 'all_ok': all(x['commit_is_pinned'] and x['tracked'] for x in hy)}
# (d) V404 folder untouched
last = max((W4 / 'receipts').glob('*accept*.json'), key=lambda p: p.stat().st_mtime).stat().st_mtime
newer = [str(p.relative_to(W4)) for p in W4.rglob('*') if p.is_file() and p.stat().st_mtime > last + 1]
out['v404_folder_files_newer_than_its_last_accept_receipt'] = {'n': len(newer), 'sample': newer[:8]}
# (e) G1 custody plan (read-only)
plan_path = Path(r'C:\IALD\Central de Patentes\work\custodia_G1\PLANO_v405.json')
raw = plan_path.read_bytes()
pl = json.loads(raw)
out['custody_process_state_G1'] = {'plano_path': str(plan_path), 'plano_sha256': sh(raw), 'versao': pl['versao'], 'corrente': pl['corrente'], 'relacao_espelho': pl['relacao_espelho'], 'contagem': pl['contagem'], 'completo': pl['completo'], 'pendentes': pl['pendentes'],
                                   'pendentes_do_operador': [x['id'] for x in pl['pendentes_do_operador']], 'itens_pendentes': {i['id']: {'estado': i['estado'], 'passo': i['passo'], 'detalhe': i['detalhe'][:160]} for i in pl['itens'] if i['id'] in ('C19', 'C20', 'C17C', 'C21')}}
cf = rd(r'C:\IALD\Central de Patentes\work\custodia_v405_02nov\CONFERENCIA_FINAL_v405.json')
out['custody_final_conference'] = {'ok': cf['ok'], 'total': cf['total'], 'pin_equals_release': cf['pin'] == rd(W / 'app/RELEASE.json')['um_py_sha256']}
print(json.dumps(out, ensure_ascii=False, indent=1))
