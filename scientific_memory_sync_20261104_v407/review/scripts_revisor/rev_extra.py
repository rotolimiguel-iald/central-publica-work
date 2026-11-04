"""Revisor independente F0.3 v407 - verificacoes extras (somente leitura). Saida: review\\REV_EXTRA.json"""
import sys, json, hashlib, re, datetime
sys.dont_write_bytecode = True
from pathlib import Path

W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
CM = BASE / 'state' / 'canonical_memory'
REL = CM / 'releases'
NEW = 'v407_4323b401f15cc971'
OLD = 'v404_302dc102683e9fb1'


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {}
# (a) last write time in the pre-existing tree
ant = json.loads((W / 'BASELINE_ANTES.json').read_bytes())
items = sorted(((v['mtime_ns'], k) for k, v in ant['arquivos'].items()), reverse=True)[:5]
out['baseline_ANTES_five_latest_mtimes'] = [(datetime.datetime.fromtimestamp(ns / 1e9).strftime('%Y-%m-%d %H:%M:%S'), k) for ns, k in items]
out['baseline_ANTES_n_files_with_mtime_today'] = sum(1 for v in ant['arquivos'].values() if datetime.datetime.fromtimestamp(v['mtime_ns'] / 1e9).date() >= datetime.date(2026, 11, 4))
cur = json.loads((W / 'review' / 'REV_BASELINE_A.json').read_bytes())
pre = {k: v for k, v in cur['arquivos'].items() if not k.replace('\\', '/').startswith('releases/' + NEW + '/')}
out['now_pre_existing_files_n'] = len(pre)
out['now_pre_existing_latest_mtime'] = max((datetime.datetime.fromtimestamp(v['mtime_ns'] / 1e9).strftime('%Y-%m-%d %H:%M:%S'), k) for k, v in pre.items())
out['now_pre_existing_n_with_mtime_today'] = sum(1 for v in pre.values() if datetime.datetime.fromtimestamp(v['mtime_ns'] / 1e9).date() >= datetime.date(2026, 11, 4))
out['canonical_memory_root_dir_mtime'] = datetime.datetime.fromtimestamp(CM.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
out['releases_dir_mtime'] = datetime.datetime.fromtimestamp(REL.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
# (b) v404 vs v407 documents
m_old = json.loads((REL / OLD / 'manifest.json').read_bytes())
m_new = json.loads((REL / NEW / 'manifest.json').read_bytes())
old = {d['name']: d for d in m_old['documents']}
new = {d['name']: d for d in m_new['documents']}
rows = []
for n in new:
    rows.append({'name': n, 'bytes_v404': old[n]['bytes'], 'bytes_v407': new[n]['bytes'], 'delta': new[n]['bytes'] - old[n]['bytes'], 'same_sha': old[n]['sha256'] == new[n]['sha256']})
out['v404_vs_v407_docs'] = rows
out['v404_chunks'] = m_old['chunks']
out['v407_chunks'] = m_new['chunks']
um_old = (REL / OLD / 'snapshots' / OLD / 'um.py').read_bytes().decode('utf-8-sig')
out['v404_um_py_UM_VERSION'] = re.findall(r'(?m)^UM_VERSION\s*=\s*["\'](v[0-9]+)["\']', um_old)
out['v404_release_manifest_keys_eq_v407'] = sorted(m_old) == sorted(m_new)
# structure parity with the previous release (file layout)
def layout(r):
    return sorted(re.sub(r'bak_\d{8}_\d{6}_\d+', 'bak_STAMP', str(p.relative_to(REL / r)).replace(OLD, 'EPOCH').replace(NEW, 'EPOCH')) for p in (REL / r).rglob('*') if p.is_file())
out['layout_parity_with_v404'] = layout(OLD) == layout(NEW)
out['layout_v404'] = layout(OLD)
print(json.dumps(out, ensure_ascii=False, indent=1))
(W / 'review' / 'REV_EXTRA.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
