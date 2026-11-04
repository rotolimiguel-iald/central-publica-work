"""Revisor independente F0.3 v407 - recibos de preparo (somente leitura). Saida: review\\REV_RECIBOS.json"""
import sys, json, hashlib
sys.dont_write_bytecode = True
from pathlib import Path

W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
EPOCH = 'v407_4323b401f15cc971'
SNAP = BASE / 'state' / 'canonical_memory' / 'releases' / EPOCH / 'snapshots' / EPOCH


def sha(b):
    return hashlib.sha256(b).hexdigest()


J = lambda n: json.loads((W / n).read_bytes())
prep = J('PREPARATION_' + EPOCH + '.json')
pres = J('PREPARE_RESULT.json')
bi = J('BUILD_INTENT_' + EPOCH + '.json')
cat_staged = J('CATALOG_' + EPOCH + '.json')
cat_orig = json.loads((BASE / 'project_fisica' / 'MANIFESTO_LOCAL.json').read_bytes())
check = J('CHECK_ANTES_v407.json')
out = {}
out['PREPARE_RESULT_eq_PREPARATION'] = pres == prep
out['BUILD_INTENT_keys'] = sorted(bi)
out['BUILD_INTENT_sources_eq_PREPARATION_sources'] = bi['sources'] == prep['sources']
out['BUILD_INTENT_active_pin_eq_baseline_pin'] = bi['active_pin'] == prep['baseline_active_pin']
out['BUILD_INTENT_epoch_target'] = (bi['epoch'] == EPOCH, bi['target'] == prep['target'])
out['BUILD_INTENT_at'] = bi['at']
out['PREPARATION_at'] = prep['at']
out['CHECK_active_pin_eq_baseline_pin'] = check['active_pin'] == prep['baseline_active_pin']
out['CHECK_active_eq_previous_active'] = check['active'] == prep['previous_active']
out['CHECK_status'] = check['status']
# staged catalog: only the 13 non-PDF sources are redirected to the snapshot copies; everything else identical
diffs = []
ok = True
for a, b in zip(cat_orig['files'], cat_staged['files']):
    name = Path(a['source']).name
    if a['source'].lower().endswith('.pdf'):
        same = (a == b)
        if not same:
            ok = False
            diffs.append(('pdf-entry-changed', name))
    else:
        exp = dict(a, source=str(SNAP / name))
        if b != exp:
            ok = False
            diffs.append(('text-entry-differs', name, {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)}))
out['CATALOG_staged_only_redirects_13_text_sources_to_snapshot'] = ok and len(cat_orig['files']) == len(cat_staged['files'])
out['CATALOG_staged_diffs'] = diffs
out['CATALOG_staged_other_top_keys_equal'] = {k: cat_orig[k] == cat_staged[k] for k in cat_orig if k != 'files'}
est = J('ESTATUTOS_' + EPOCH + '.json')
out['ESTATUTOS_scope'] = est['scope']
out['ESTATUTOS_source_is_snapshot_um_absoluto'] = est['source']['path'] == str(SNAP / 'um_absoluto.json')
print(json.dumps(out, ensure_ascii=False, indent=1))
(W / 'review' / 'REV_RECIBOS.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
