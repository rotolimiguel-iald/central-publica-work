"""Reviewer Q2: what changed in the sealed core between v404 and v405 (66 topics), by leaf path; and the 1-char shrink in ringdown_dephasing_result_v2."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

R = Path(r'C:\IALD\projetos_pyhton\IALD')
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
core_old = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())['core']
core_new = json.loads((Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405') / 'um_absoluto.json').read_bytes())['core']
AUX = {'runtime_s', 'protocol_hash', 'frozen_hash', 'result_sha16', 'catalog_sha16', 'result_path'}


def diffs(a, b, p=''):
    out = []
    if type(a) != type(b):
        return [(p, 'type', repr(a)[:60], repr(b)[:60])]
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                out.append((p + '/' + k, 'removed', repr(a[k])[:60], ''))
            else:
                out += diffs(a[k], b[k], p + '/' + k)
        for k in b:
            if k not in a:
                out.append((p + '/' + k, 'added', '', repr(b[k])[:60]))
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((p, 'len', len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            out += diffs(x, y, p + '/' + str(i))
    elif a != b:
        out.append((p, 'value', repr(a)[:70], repr(b)[:70]))
    return out


changed = [n for n in core_new if n in core_old and core_new[n] != core_old[n]]
rows = []
aux_only = []
for n in changed:
    d = diffs(core_old[n], core_new[n])
    leaf_keys = [x[0].rsplit('/', 1)[-1] for x in d]
    only_aux = all(k in AUX for k in leaf_keys)
    if only_aux:
        aux_only.append(n)
    rows.append({'topic': n, 'n_diffs': len(d), 'aux_only': only_aux, 'sample': d[:3]})
print('changed topics:', len(changed), '| auxiliary-only (runtime_s/hash fields):', len(aux_only))
for r in rows:
    if not r['aux_only']:
        print(' NON-AUX', r['topic'], r['n_diffs'], r['sample'])
print('--- ringdown_dephasing_result_v2')
for x in diffs(core_old['ringdown_dephasing_result_v2'], core_new['ringdown_dephasing_result_v2'])[:10]:
    print('  ', x)
print('--- kernel_formalization key-set delta (count) old vs new')
ko, kn = core_old['kernel_formalization'], core_new['kernel_formalization']
print('keys old', len(ko), 'keys new', len(kn), 'added', len(set(kn) - set(ko)), 'removed', len(set(ko) - set(kn)))
print('bool old', sum(1 for v in ko.values() if type(v) is bool), 'bool new', sum(1 for v in kn.values() if type(v) is bool))
added = [k for k in kn if k not in ko]
print('added keys sample', added[:12])
print('non-boolean top-level keys with changed value:', [k for k in ko if k in kn and type(ko[k]) is not bool and ko[k] != kn[k]][:20])
print('declaration_sources_v394 old/new len', len(ko['declaration_sources_v394']), len(kn['declaration_sources_v394']))
print('axiom_report old/new len', len(ko['axiom_report']), len(kn['axiom_report']))
