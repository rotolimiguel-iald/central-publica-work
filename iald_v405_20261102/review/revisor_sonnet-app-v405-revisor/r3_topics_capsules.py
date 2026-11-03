"""Reviewer (sonnet-app-v405-revisor) Q2/Q3 base: topics present in each package, 0 lost, capsules restore exactly against the SEALED core.
OWN decoder (does not import haiku_codec / fit_*). Adapted from the v404 reviewer's r3 with an explicit, independent handling of the
AUDIT_BOOLEAN_FIELDS_IN_SOURCE capsule of kernel_formalization (recomputed from the sealed source, not from the codec).
Read-only. usage: script <release_dir>  -> JSON on stdout. Also importable (set sys.argv before import)."""
import json, re, sys, hashlib
from pathlib import Path

W = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
rel = W.name.split('_')[1]  # v405
VAULT = Path(r'C:\IALD\Central de Patentes\vault\originals_copy') / ('um_unificado_' + rel)
sha = lambda b: hashlib.sha256(b).hexdigest()
res_raw = (VAULT / 'um_absoluto.json').read_bytes()
seal = json.loads((VAULT / 'um_absoluto_selo.json').read_bytes())
assert sha(res_raw) == seal['sha256']['um_absoluto.json'], 'core not the sealed one'
res = json.loads(res_raw)
core = res['core']
MARK = '## Exposição canônica integral: fórmulas e derivações'
AUD = 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE'
ALIAS = {'"@F"': '"@SOURCE_FIELDS"', '"@I"': '"@SOURCE_ITEMS"', '"@L"': '"@TGL_LITERAL"', '"@Y"': '"@SUMMARY"', '"@X"': '"@EXPOSITION"'}
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def unalias(s):
    for sh_, lg in ALIAS.items():
        s = s.replace(sh_, lg)
    return s


def resolve(v, ptr):
    if ptr == '':
        return v
    assert ptr.startswith('/'), ptr
    for part in ptr.split('/')[1:]:
        k = part.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def child(p, k):
    return p + '/' + str(k).replace('~', '~0').replace('/', '~1')


def unpack(v):
    if isinstance(v, list):
        return [unpack(x) for x in v]
    if not isinstance(v, dict):
        return v
    out = {k: unpack(x) for k, x in v.items() if k not in ('@SOURCE_FIELDS', '@SOURCE_ITEMS')}
    if '@SOURCE_FIELDS' in v:
        for k in v['@SOURCE_FIELDS']:
            out[k] = {'@': '/' + k}
    if '@SOURCE_ITEMS' in v:
        for k, n in v['@SOURCE_ITEMS'].items():
            out[k] = {'@': '/' + k, 'items': n}
    return out


class Summ:
    def __init__(self, ptr, a, n, topic=None):
        self.ptr = ptr
        self.a = a
        self.n = n
        self.topic = topic


SUMM_COUNT = [0]


def dec_lit(v, D, E):
    if isinstance(v, list):
        return [dec_lit(x, D, E) for x in v]
    if not isinstance(v, dict):
        return v
    ks = set(v)
    if ks == {'@concat'}:
        return ''.join(dec_lit(x, D, E) for x in v['@concat'])
    if ks == {'@upper'}:
        return v['@upper'].upper()
    if ks == {'@enum'}:
        return v['@enum'].upper().replace(' ', '_')
    if ks == {'@TGL_LITERAL'}:
        return dec_lit(D[v['@TGL_LITERAL']], D, E)
    if ks == {'@EXPOSITION'}:
        s, l = v['@EXPOSITION']
        return E[s:s + l]
    if ks == {'@SUMMARY'} and isinstance(v['@SUMMARY'], list):
        return Summ(v['@SUMMARY'][0], v['@SUMMARY'][1], v['@SUMMARY'][2])
    if ks == {'@SUMMARY', 'source_pointer', 'span'}:
        return Summ(v['source_pointer'], v['span'][0], v['span'][1], v['@SUMMARY'])
    return {k: dec_lit(x, D, E) for k, x in v.items()}


def restore(v, src, cur, rep, E=''):
    if isinstance(v, Summ):
        topic = cur.split('/')[2]
        root = '/core/' + topic
        ptr = v.ptr if v.ptr.startswith('/core/') else root + v.ptr
        piece = E[v.a:v.a + v.n]
        assert piece.startswith('**Estatutos [' + topic + ']**'), ('stale summary', cur)
        SUMM_COUNT[0] += 1
        return resolve(src, ptr)
    if isinstance(v, dict) and '@' in v:
        assert set(v) <= {'@', 'fields', 'items', 'true_fields', 'false_fields'}, ('unknown meta', sorted(v))
        actual = resolve(src, cur)  # the '@' path must equal the place it sits at
        assert v['@'] == cur[len(cur) - len(v['@']):] if v['@'] else True
        for suf, val in v.get('fields', {}).items():
            fv = restore(val, src, cur + suf, rep, E)
            assert resolve(actual, suf) == fv, ('field differs', cur, suf)
            rep.append((cur + suf, fv))
        if 'items' in v:
            assert len(actual) == v['items'], ('items', cur)
        if 'true_fields' in v:
            assert v['true_fields'] == sum(actual.values()) and v['false_fields'] == len(actual) - sum(actual.values())
        return actual
    if isinstance(v, dict):
        return {k: restore(x, src, child(cur, k), rep, E) for k, x in v.items()}
    if isinstance(v, list):
        return [restore(x, src, child(cur, i), rep, E) for i, x in enumerate(v)]
    return v


STATUS = re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|hypothes|hip[oó]tese|assumption|premiss|claim|declar|residue|conjecture|not_claimed|not_said|statement|enunciad|formula|equa', re.I)


def status_paths(v, p=''):
    out = {}
    if isinstance(v, dict):
        for k, x in v.items():
            q = child(p, k)
            if STATUS.search(str(k)):
                out[q] = x
            else:
                out.update(status_paths(x, q))
    elif isinstance(v, list):
        for i, x in enumerate(v):
            out.update(status_paths(x, child(p, i)))
    return out


def firstdiff(a, b, p=''):
    if type(a) != type(b):
        return p + ' type ' + type(a).__name__ + ' vs ' + type(b).__name__ + ' :: ' + repr(a)[:80] + ' vs ' + repr(b)[:80]
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a:
                return p + '/' + k + ' missing-in-got'
            if k not in b:
                return p + '/' + k + ' extra-in-got'
            r = firstdiff(a[k], b[k], p + '/' + k)
            if r:
                return r
        return ''
    if isinstance(a, list):
        if len(a) != len(b):
            return p + ' len %d vs %d' % (len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            r = firstdiff(x, y, p + '/' + str(i))
            if r:
                return r
        return ''
    return '' if a == b else p + ' :: ' + repr(a)[:80] + ' vs ' + repr(b)[:80]


def catalog_merge(n, dv):
    """Independent verification of the AUDIT_BOOLEAN_FIELDS_IN_SOURCE capsule against the SEALED source.
    Returns (dv_with_source_booleans_restored, report). The set of booleans carried only by the catalog is recomputed here from the
    sealed topic (TRUE booleans that are not literal in the capsule); count and sha256 of its canonical dump must match the capsule."""
    cap = dv.get(AUD)
    if cap is None:
        return dv, None
    src = core[n]
    assert cap['source_pointer'] == '/core/' + n
    lit = {k: x for k, x in dv.items() if k != AUD}
    src_bool = {k: x for k, x in src.items() if type(x) is bool}
    lit_bool = {k: x for k, x in lit.items() if type(x) is bool}
    carried_elsewhere = {k: x for k, x in src_bool.items() if k in lit_bool}
    only_by_catalog = {k: x for k, x in src_bool.items() if k not in lit_bool}  # source order preserved
    rep = {'source_booleans': len(src_bool), 'source_true': sum(1 for x in src_bool.values() if x), 'source_false': sum(1 for x in src_bool.values() if not x),
           'literal_true_in_capsule': sum(1 for x in lit_bool.values() if x), 'literal_false_in_capsule': sum(1 for x in lit_bool.values() if not x),
           'only_by_catalog_true': sum(1 for x in only_by_catalog.values() if x), 'only_by_catalog_false': sum(1 for x in only_by_catalog.values() if not x),
           'literal_booleans_equal_source_values': all(src_bool[k] == x for k, x in lit_bool.items()), 'capsule_fields': sorted(cap)}
    if 'catalog_sha256' in cap:  # v405 haiku form: TRUE-only catalog, count + sha256 of the canonical dump
        only_true = {k: x for k, x in only_by_catalog.items() if x}
        rep.update(form='TRUE_CATALOG_WITH_SHA256', catalog_count_matches=(cap['true_fields'] == len(only_true)),
                   catalog_sha256_matches=(cap['catalog_sha256'] == sha(dump(only_true).encode())), recomputed_sha256=sha(dump(only_true).encode()),
                   no_false_goes_only_by_catalog=(rep['only_by_catalog_false'] == 0), catalog_names_sample=list(only_true)[:3])
        rep['ok'] = rep['catalog_count_matches'] and rep['catalog_sha256_matches'] and rep['no_false_goes_only_by_catalog'] and rep['literal_booleans_equal_source_values']
    else:  # shared/sonnet form: counts of ALL booleans (inherited rule)
        rep.update(form='COUNTS_ONLY', true_matches=(cap['true_fields'] == rep['source_true']), false_matches=(cap['false_fields'] == rep['source_false']))
        rep['ok'] = rep['true_matches'] and rep['false_matches'] and rep['literal_booleans_equal_source_values']
    full = dict(lit)
    full.update(only_by_catalog)
    return full, rep


def analyse(name, keep_blocks=False):
    SUMM_COUNT[0] = 0
    t = (W / 'app/packages' / name / 'prefix.md').read_text('utf-8')
    head, sep, expo_part = t.partition(MARK)
    head = unalias(head)
    D = {}
    E = ''
    m = re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n', head)
    if m:
        D = json.loads(m.group(1))
    m2 = re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n', head)
    FL = json.loads(m2.group(1)) if m2 else {}
    if '<EXPOSICAO_CANONICA>\n' in expo_part:
        E = expo_part.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    hs = list(re.finditer(r'(?m)^### ([^\n]+)\n', head))
    body = {}
    for i, h in enumerate(hs):
        stop = hs[i + 1].start() if i + 1 < len(hs) else len(head)
        body[h[1]] = head[h.end():stop]
    present = [n for n in core if n in body]
    lost = [n for n in core if n not in body]
    nonjson = []
    mism = []
    compact = 0
    full = 0
    partial = 0
    stat_cmp = 0
    stat_vis_missing = 0
    stat_total = 0
    catalog_reports = {}
    exact_names = []
    for n in present:
        lines = [l for l in body[n].split('\n') if l.strip()]
        js = [l for l in lines if not l.startswith('Fonte:')]
        if not js:
            nonjson.append(n)
            continue
        try:
            v = json.loads(js[0])
        except Exception as e:
            nonjson.append((n, str(e)[:60]))
            continue
        top_at = isinstance(v, dict) and '@' in v
        if isinstance(v, dict) and '@B' in v:
            ident = str(v.pop('@B'))
            flags = FL[ident]
            assert not (set(flags) & set(v))
            v.update(flags)
        try:
            dv = dec_lit(unpack(v), D, E)
            if n == 'kernel_formalization' and isinstance(dv, dict):
                dv, crep = catalog_merge(n, dv)
                if crep is not None:
                    catalog_reports[n] = crep
                    if not crep['ok']:
                        mism.append((n, 'CATALOG_NOT_OK ' + json.dumps(crep, ensure_ascii=False)[:300]))
            rep = []
            got = restore(dv, res, '/core/' + n, rep, E)
            ok = got == core[n]
            if not ok:
                mism.append((n, 'DIFF ' + firstdiff(got, core[n])))
            else:
                exact_names.append(n)
            has_ref = '"@"' in js[0]
            if top_at:
                compact += 1
            elif has_ref:
                partial += 1
            else:
                full += 1
            sp = status_paths(core[n])
            stat_total += len(sp)
            vis = set(p for p, _ in rep)

            def inline(x, p, acc):
                if isinstance(x, dict) and '@' in x:
                    return
                if isinstance(x, dict):
                    for k, y in x.items():
                        inline(y, child(p, k), acc)
                elif isinstance(x, list):
                    for i, y in enumerate(x):
                        inline(y, child(p, i), acc)
                else:
                    acc.add(p)
            acc = set()
            inline(dv, '/core/' + n, acc)
            vis |= acc
            for p, val in sp.items():
                full_p = '/core/' + n + p
                if any(q == full_p or q.startswith(full_p + '/') or full_p.startswith(q + '/') for q in vis):
                    stat_cmp += 1
                else:
                    stat_vis_missing += 1
        except Exception as e:
            mism.append((n, type(e).__name__ + ': ' + str(e)[:160]))
    out = {'package': name, 'bytes': len(t.encode()), 'headings': len(hs), 'core_topics': len(core), 'present': len(present), 'lost': lost,
           'topics_restoring_exactly': len(exact_names), 'mismatch_or_error': mism[:60], 'n_mismatch': len(mism), 'nonjson': nonjson[:8], 'n_nonjson': len(nonjson),
           'form': {'top_level_capsule': compact, 'partial_refs': partial, 'full_inline': full},
           'status_like_source_paths': stat_total, 'status_paths_visible_in_prompt': stat_cmp, 'status_paths_only_by_pointer': stat_vis_missing,
           'summary_refs_resolved': SUMM_COUNT[0], 'prefix_sha256': sha(t.encode()), 'catalog_reports': catalog_reports}
    if keep_blocks:
        out['_body'] = body
        out['_D'] = D
        out['_E'] = E
        out['_FL'] = FL
    return out


if __name__ == '__main__':
    out = {'release': rel, 'sealed_core_sha256': sha(res_raw), 'core_topics': len(core), 'packages': {}}
    for p in ('haiku_expanded', 'shared', 'sonnet_public', 'haiku55'):
        out['packages'][p] = analyse(p)
    print(json.dumps(out, ensure_ascii=False, indent=1))
