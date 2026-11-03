"""Reviewer Q2/Q3: for shared and sonnet_public, list ALL keys that decoded blocks omit versus the sealed core (not only the first), and classify them (auxiliary metadata vs anything else).
Adapted from the v404 reviewer's r3b with the own decoder (lib405). Read-only."""
import json, re, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
res = json.loads((V / 'um_absoluto.json').read_bytes())
core = res['core']
AUX = {'runtime_s', 'protocol_hash', 'frozen_hash', 'result_sha16', 'catalog_sha16', 'result_path'}


def alldiff(a, b, p, acc):
    if type(a) != type(b):
        acc.append((p, 'type'))
        return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a:
                acc.append((p + '/' + k, 'omitted'))
            elif k not in b:
                acc.append((p + '/' + k, 'extra'))
            else:
                alldiff(a[k], b[k], p + '/' + k, acc)
    elif isinstance(a, list):
        if len(a) != len(b):
            acc.append((p, 'len'))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            alldiff(x, y, p + '/' + str(i), acc)
    elif a != b:
        acc.append((p, 'value'))


status_like = re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|hypothes|hip[oó]tese|assumption|premiss|claim|declar|residue|conjecture|not_claimed|not_said|statement|enunciad|formula|equa|limites|^diz$|nao_diz', re.I)
out = {}
for pkg in ('shared', 'sonnet_public'):
    P = L.parse_prefix((W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8'))
    rows, texts, exact = [], [], 0
    for n in core:
        kind, dv = L.decode_block(P, n)
        if kind != 'JSON':
            texts.append(n)
            continue
        try:
            full = L.catalog_full(dv, core[n]) if n == 'kernel_formalization' else dv
            got = L.restore(full, res, '/core/' + n, [], P['E'])
        except Exception as e:
            rows.append({'topic': n, 'error': str(e)[:100]})
            continue
        acc = []
        alldiff(got, core[n], '', acc)
        if acc:
            rows.append({'topic': n, 'diffs': acc[:30], 'n': len(acc)})
        else:
            exact += 1
    omitted = collections.Counter()
    for r in rows:
        for p, k in r.get('diffs', []):
            omitted[(p.rsplit('/', 1)[-1], k)] += 1
    non_aux = [(k, kind, n) for (k, kind), n in omitted.items() if k not in AUX]
    out[pkg] = {'exact': exact, 'topics_with_omitted_keys': len([r for r in rows if 'diffs' in r]), 'errors': [r for r in rows if 'error' in r], 'text_syntheses': len(texts),
                'omitted_key_names': {f'{k}:{kind}': n for (k, kind), n in omitted.most_common()}, 'omitted_not_auxiliary': non_aux, 'status_like_omitted': [(k, n) for (k, kind), n in omitted.items() if status_like.search(k)],
                'sum': exact + len([r for r in rows if 'diffs' in r]) + len([r for r in rows if 'error' in r]) + len(texts)}
print(json.dumps(out, ensure_ascii=False, indent=1))
