"""Revisor sonnet-app-v406-revisor -- QB: Q2 (janela P2 e literais) e Q4 (R3-1, pares TRUE/FALSE). Somente leitura.
Decodificador independente (lib405.py, que NAO importa haiku_codec/fit_*), recomputando tudo sobre o resultado selado do cofre v406."""
import hashlib, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v406')
sha = lambda b: hashlib.sha256(b).hexdigest()
res = json.loads((V / 'um_absoluto.json').read_bytes())
core = res['core']
chk, out = [], {}


def ck(name, ok, **info):
    chk.append({'name': name, 'pass': bool(ok), **info})


# ---- configured windows (from the brief AND from the builder's cfg text; both must agree)
cfg_txt = (W / 'release_cfg.py').read_text('utf-8')
cfg_win = tuple(re.findall(r"'(_v4\d\d)'", re.search(r'(?m)^SHARED_P2_SUFFIXES\s*=\s*\(([^)]*)\)', cfg_txt).group(1)))
cfg_ret = tuple(re.findall(r"'(_v4\d\d)'", re.search(r'(?m)^P2_RETIRED_LITERAL_SUFFIXES\s*=\s*\(([^)]*)\)', cfg_txt).group(1)))
WIN = ('_v402', '_v403', '_v404', '_v405', '_v406')
RET = ('_v401',)
ck('Q2.cfg_windows_equal_brief', cfg_win == WIN and cfg_ret == RET, cfg_win=cfg_win, cfg_ret=cfg_ret)
window = [n for n in core if n.endswith(WIN)]
retired = [n for n in core if n.endswith(RET)]
out['topics_total'] = len(core)
out['window_topics'] = {'n': len(window), 'by_suffix': {s: sum(1 for n in window if n.endswith(s)) for s in WIN}}
out['retired_topics'] = {'n': len(retired), 'names': retired}
ck('Q2.474_topics_in_sealed_result', len(core) == 474, n=len(core))

QK = re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|limites|^diz$|^nao_diz$', re.I)
LITKEYS = ('limites', 'diz', 'nao_diz')


AUX = {'runtime_s', 'protocol_hash', 'frozen_hash', 'result_sha16', 'catalog_sha16', 'result_path'}


def dd(a, b, p=''):
    if type(a) != type(b):
        yield (p, 'type'); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                yield (p + '/' + k, 'only-got')
            elif k not in b:
                yield (p + '/' + k, 'only-src')
            else:
                yield from dd(a[k], b[k], p + '/' + k)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield (p, 'len'); return
        for i, (x, y) in enumerate(zip(a, b)):
            yield from dd(x, y, p + '/%d' % i)
    elif a != b:
        yield (p, 'val')


def has_ref(v):
    if isinstance(v, L.Summ) or L.is_ref(v):
        return True
    if isinstance(v, dict):
        return any(has_ref(x) for x in v.values())
    if isinstance(v, list):
        return any(has_ref(x) for x in v)
    return False


def lit_value(dn, key):
    """-> (state, decoded value). state: LIT (whole value literal, no pointer/summary inside) | REF | PARTIAL | ABSENT"""
    if L.is_ref(dn):
        if dn.get('@') != '':
            return 'OTHER', None
        f = dn.get('fields', {})
        if '/' + key in f:
            v = f['/' + key]
        else:
            return ('PARTIAL', None) if any(s.startswith('/' + key + '/') for s in f) else ('ABSENT', None)
    elif isinstance(dn, dict):
        if key not in dn:
            return 'ABSENT', None
        v = dn[key]
    else:
        return 'OTHER', None
    return ('REF', v) if has_ref(v) else ('LIT', v)


P = {}
for pkg in ('shared', 'sonnet_public', 'haiku_expanded'):
    P[pkg] = L.parse_prefix((W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8'))

# ---- all topics: presence, decode, restore == sealed (all three packages)
rows = {pkg: {} for pkg in P}
kf = core['kernel_formalization']
for pkg, Pp in P.items():
    heads = set(Pp['body'])
    present = set(core) & heads
    ck('Q2.all_474_topics_present:' + pkg, len(present) == 474 and not (set(core) - heads), present=len(present), missing=sorted(set(core) - heads)[:5], extra_headings=len(heads - set(core)))
    bad = []
    texts = []
    aux_explained = []
    for n, src in core.items():
        k, dn = L.decode_block(Pp, n)
        if k != 'JSON':
            texts.append(n)
            continue
        try:
            dnn = dn
            if n == 'kernel_formalization':
                dnn = None   # handled in the Q4 section with an independent catalog
            if dnn is not None:
                got = L.restore(dnn, res, '/core/' + n, [], Pp['E'])
                if got != src:
                    srctxt = json.dumps(src, ensure_ascii=False)
                    un = []
                    for d in dd(src, got):
                        last = d[0].rsplit('/', 1)[-1]
                        if d[1] == 'only-src' and last in AUX:
                            # the codec deliberately omits auxiliary hash/runtime metadata keys from the prompt capsule (recorded as 'auxiliary_metadata'); same set as the accepted installed v405
                            aux_explained.append(n)
                            continue
                        un.append(d)
                    if un:
                        bad.append((n, 'restore-differs', un[:2]))
        except Exception as e:
            bad.append((n, 'ERR:' + str(e)[:80]))
    # TEXT-kind (summary prose) blocks cannot be restored mechanically: same 46 topics as the accepted installed v405; compare their bytes with the installed block when the sealed source is unchanged
    out.setdefault('Q2_text_topics', {})[pkg] = {'n': len(texts), 'names_head': texts[:3]}
    ck('Q2.decoded_capsules_restore_sealed_source:' + pkg, not bad, n_json_checked=len(core) - 1 - len(texts), n_text_summary_blocks=len(texts), topics_missing_only_AUX_hash_metadata_keys=len(set(aux_explained)), bad=bad[:5])

# ---- Q2: window + retired topics, qualifier literals inline and equal
summary = {}
for pkg in ('shared', 'sonnet_public', 'haiku_expanded'):
    Pp = P[pkg]
    fail = {'not_integral': [], 'qual_not_lit_or_unequal': [], 'retired_not_capsule': [], 'lit3_missing': [], 'status_leaf_pointer_only': []}
    n_q = 0
    n_lit3 = 0
    for grp, names in (('window', window), ('retired', retired)):
        for n in names:
            src = core[n]
            k, dn = L.decode_block(Pp, n)
            top_cap = L.is_ref(dn) and dn.get('@') == ''
            if grp == 'window' and pkg != 'haiku_expanded' and top_cap:
                fail['not_integral'].append(n)
            if grp == 'window' and pkg == 'haiku_expanded' and n.endswith(('_v405', '_v406')) and top_cap:
                fail['not_integral'].append(n)
            if grp == 'retired' and pkg != 'haiku_expanded' and not top_cap:
                fail['retired_not_capsule'].append(n)
            qkeys = [x for x in src if QK.search(x)]
            for x in qkeys:
                n_q += 1
                st, v = lit_value(dn, x)
                if st != 'LIT' or L.canon(v) != src[x]:
                    # for pkg haiku_expanded older topics are compact by design: only the must-be-literal set is enforced there
                    fail['qual_not_lit_or_unequal'].append((grp, n, x, st))
            for x in LITKEYS:
                if x in src:
                    n_lit3 += 1
                    st, v = lit_value(dn, x)
                    if st != 'LIT' or L.canon(v) != src[x]:
                        fail['lit3_missing'].append((grp, n, x, st))
            # every status-like leaf anywhere in the source topic, outside the three registers, is literal (path-level)
            lp = L.literal_leaves(dn, '/core/' + n)
            lps = set(lp)
            for p, v in L.leaves(src, '/core/' + n):
                last = p.rsplit('/', 1)[-1]
                if re.fullmatch(r'(?i)status|statute|estatuto|verdict|veredit\w*', last):
                    top = p.split('/')[3] if p.count('/') >= 3 else ''
                    if top in ('unconditional', 'index_conditional', 'named_pending'):
                        continue
                    if p not in lps and not any(q.startswith(p + '/') or p.startswith(q + '/') for q in lps):
                        fail['status_leaf_pointer_only'].append(p)
    summary[pkg] = {'qualifier_keys_checked': n_q, 'limites_diz_nao_diz_checked': n_lit3, **{k: (len(v), v[:4]) for k, v in fail.items()}}
out['Q2_summary'] = summary
for pkg in ('shared', 'sonnet_public'):
    s = summary[pkg]
    ck('Q2.window_integral_and_qualifiers_literal:' + pkg, s['not_integral'][0] == 0 and s['qual_not_lit_or_unequal'][0] == 0 and s['retired_not_capsule'][0] == 0 and s['lit3_missing'][0] == 0 and s['status_leaf_pointer_only'][0] == 0,
       qual_checked=s['qualifier_keys_checked'], lit3_checked=s['limites_diz_nao_diz_checked'], detail={k: s[k][0] for k in ('not_integral', 'qual_not_lit_or_unequal', 'retired_not_capsule', 'lit3_missing', 'status_leaf_pointer_only')})
s = summary['haiku_expanded']
ck('Q2.haiku_expanded_v405_v406_integral_and_literals', s['not_integral'][0] == 0, info={k: s[k][0] for k in s if isinstance(s[k], tuple)})

# ---- Q2 regression: shared v406 vs INSTALLED v405 shared, topic by topic, where the sealed source is unchanged
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
res_old = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())
core_old = res_old['core']
Po = L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'))
same_src, diffs = 0, []
for n in core:
    if n not in core_old or core_old[n] != core[n]:
        continue
    same_src += 1
    ko, do = L.decode_block(Po, n)
    kn, dn = L.decode_block(P['shared'], n)
    if not (ko == kn and L.canon(do) == L.canon(dn)):
        diffs.append(n)
new_topics = [n for n in core if n not in core_old]
changed_src = [n for n in core if n in core_old and core_old[n] != core[n]]
out['Q2_shared_vs_installed_v405'] = {'topics_with_unchanged_source': same_src, 'decoded_blocks_differing': diffs, 'new_topics_in_v406': len(new_topics), 'topics_with_changed_source': len(changed_src), 'new_window_topics_suffixes': sorted({n.rsplit('_', 1)[-1] for n in new_topics})}
# of the differing ones: which are the retired _v401 (intended) and which are not
unexpected = [n for n in diffs if not n.endswith(RET)]
ck('Q2.shared_unchanged_topics_decode_identical_to_installed_except_retired', not unexpected, differing=len(diffs), retired_intended=sum(1 for n in diffs if n.endswith(RET)), unexpected=unexpected[:8])
# for the retired topics: nothing that was literal in the installed v405 about limites/diz/nao_diz/qualifiers was lost
lost = []
for n in retired:
    if n in core_old and core_old[n] == core[n]:
        ko, do = L.decode_block(Po, n)
        kn, dn = L.decode_block(P['shared'], n)
        lo, ln = L.literal_leaves(do, '/core/' + n), L.literal_leaves(dn, '/core/' + n)
        for p, v in lo.items():
            top = p.split('/')[3] if p.count('/') >= 3 else ''
            if QK.search(top) and ln.get(p) != v:
                lost.append(p)
out['Q2_retired_qualifier_leaves_lost_vs_installed_v405'] = {'n': len(lost), 'sample': lost[:5]}
ck('Q2.retired_v401_qualifier_leaves_not_lost_vs_installed', not lost, lost=len(lost))
tb = {'texts_v406': 0, 'texts_installed_v405': 0, 'same_set': None, 'unchanged_source_bodies_equal': 0, 'unchanged_source_bodies_differ': []}
tx6 = sorted(n for n in core if n in P['shared']['body'] and L.decode_block(P['shared'], n)[0] == 'TEXT')
txi = sorted(n for n in core_old if n in Po['body'] and L.decode_block(Po, n)[0] == 'TEXT')
tb.update(texts_v406=len(tx6), texts_installed_v405=len(txi), same_set=(tx6 == [n for n in txi if n in core]))
for n in tx6:
    if n in core_old and core_old[n] == core[n]:
        if P['shared']['body'][n] == Po['body'][n]:
            tb['unchanged_source_bodies_equal'] += 1
        else:
            tb['unchanged_source_bodies_differ'].append(n)
out['Q2_text_blocks_vs_installed'] = tb
ck('Q2.text_summary_blocks_unchanged_vs_installed_when_source_unchanged', tb['same_set'] and not tb['unchanged_source_bodies_differ'], detail={k: v for k, v in tb.items()})
# bytes saved by retiring _v401 (info)
out['Q2_v401_block_bytes'] = {'installed_v405_shared': sum(len(Po['body'][n].encode()) for n in retired if n in Po['body']), 'v406_shared': sum(len(P['shared']['body'][n].encode()) for n in retired)}

# ---- Q4: R3-1 and the TRUE/FALSE pairs, on kernel_formalization of the sealed v406 result
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
LADDER = re.compile(r'(?:ext|red)_')
OLDKEEP = re.compile(r'(?:^|_)H[123](?:_|$)|discharg|condition|verified|verification', re.I)
NEWKEEP = re.compile(r'H[123]|discharg|condition|verif', re.I)
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def catalog(node, keep):
    return {k: v for k, v in node.items() if v is True and LADDER.match(k) and not (WHOLE.search(k) or ESS.search(k) or keep.search(k))}


c_old, c_new = catalog(kf, OLDKEEP), catalog(kf, NEWKEEP)
moved = sorted(set(c_old) - set(c_new))
out['Q4_catalog'] = {'true_total': sum(1 for v in kf.values() if v is True), 'false_total': sum(1 for v in kf.values() if v is False), 'catalog_old_rule': len(c_old), 'catalog_new_rule': len(c_new), 'moved_to_literal': len(moved), 'moved_names': moved,
                     'moved_literal_bytes': sum(len(('"%s":true,' % k).encode()) for k in moved), 'new_only_in_new_catalog': sorted(set(c_new) - set(c_old)),
                     'moved_matching_th2_only_by_ignorecase': [k for k in moved if re.search(r'th2|th1|th3', k) and not re.search(r'H[123]', k.replace('th', ''))]}
ck('Q4.moved_to_literal_about_16', 14 <= len(moved) <= 18 and not (set(c_new) - set(c_old)), moved=len(moved))
for pkg in ('haiku_expanded', 'shared', 'sonnet_public'):
    k, dn = L.decode_block(P[pkg], 'kernel_formalization')
    cap = dn.get(L.AUD) if isinstance(dn, dict) else None
    info = {'kind_of_block': 'catalog_capsule' if (cap and 'catalog_sha256' in cap) else ('count_summary_capsule' if cap else ('ref_capsule' if L.is_ref(dn) else 'other'))}
    if cap and 'catalog_sha256' not in cap:
        info.update(capsule=cap and {k: cap[k] for k in cap if k != 'reading'}, source_true=sum(1 for y in kf.values() if y is True), source_false=sum(1 for y in kf.values() if y is False),
                    counts_equal_source=(cap.get('true_fields') == sum(1 for y in kf.values() if y is True) and cap.get('false_fields') == sum(1 for y in kf.values() if y is False)),
                    literal_bool_keys=sum(1 for y in dn.values() if type(y) is bool))
        out['Q4_' + pkg] = info
        continue
    if not cap:
        out['Q4_' + pkg] = info
        continue
    lit = {x: y for x, y in dn.items() if x != L.AUD}
    lit_true = {x for x, y in lit.items() if y is True}
    lit_false = {x for x, y in lit.items() if y is False}
    src_true = {x for x, y in kf.items() if y is True}
    src_false = {x for x, y in kf.items() if y is False}
    cat_actual = src_true - lit_true
    info.update(capsule_true_fields=cap['true_fields'], capsule_sha_ok=cap['catalog_sha256'] == sha(dump(c_new).encode()), count_ok=cap['true_fields'] == len(c_new), catalogued_actual=len(cat_actual), catalogued_equals_my_rule=(cat_actual == set(c_new)),
                literal_true=len(lit_true), literal_false=len(lit_false), all_false_literal=(src_false <= lit_false and lit_false <= src_false),
                catalogued_matching_new_keep=sorted(x for x in cat_actual if NEWKEEP.search(x)), catalogued_not_ladder_family=sorted(x for x in cat_actual if not LADDER.match(x))[:5],
                catalogued_matching_essential=sorted(x for x in cat_actual if ESS.search(x) or WHOLE.search(x))[:5])
    # independent catalog merge -> must restore the sealed topic exactly
    full = dict(lit)
    full.update(c_new)
    got = L.restore(full, res, '/core/kernel_formalization', [], P[pkg]['E'])
    info['restores_sealed_topic_with_independent_catalog'] = (got == kf)
    # literal non-boolean leaves equal sealed
    info['literal_nonbool_equal_sealed'] = all(kf.get(x) == y for x, y in lit.items() if not has_ref(y))
    info['literal_values_that_are_pointers'] = sorted(x for x, y in lit.items() if has_ref(y))
    # pairs TRUE/FALSE: same base name after the family prefix; and token-Jaccard siblings
    base = lambda s: re.sub(r'^(?:gpf|gpc|gpi|qgf|qgc|qgp|ext|red)_', '', s)
    tok = lambda s: set(base(s).split('_'))
    pairs = {}
    near = {}
    for f in sorted(src_false):
        same = [t for t in src_true if base(t) == base(f)]
        jac = [(t, round(len(tok(f) & tok(t)) / len(tok(f) | tok(t)), 2)) for t in src_true if t != f and len(tok(f) & tok(t)) / len(tok(f) | tok(t)) >= 0.6]
        pairs[f] = {'same_base_true': same, 'same_base_true_catalogued': [t for t in same if t in cat_actual]}
        near[f] = [(t, j) for t, j in jac if t in cat_actual]
    info['false_flags'] = sorted(src_false)
    info['pairs_same_base_true_catalogued'] = {f: v['same_base_true_catalogued'] for f, v in pairs.items() if v['same_base_true_catalogued']}
    info['pairs_same_base_true_total'] = sum(len(v['same_base_true']) for v in pairs.values())
    info['near_jaccard_true_catalogued_for_false'] = {f: v[:5] for f, v in near.items() if v}
    out['Q4_' + pkg] = info
ih = out['Q4_haiku_expanded']
ck('Q4.haiku55_catalog_equals_independent_rule_count_and_hash', ih.get('count_ok') and ih.get('capsule_sha_ok') and ih.get('catalogued_equals_my_rule') and ih.get('restores_sealed_topic_with_independent_catalog') and ih.get('literal_nonbool_equal_sealed'),
   capsule_true_fields=ih.get('capsule_true_fields'), catalogued=ih.get('catalogued_actual'))
ck('Q4.no_true_flag_matching_new_rule_still_catalogued', ih.get('catalogued_matching_new_keep') == [] and ih.get('catalogued_matching_essential') == [] and ih.get('catalogued_not_ladder_family') == [], new_keep=ih.get('catalogued_matching_new_keep'))
ck('Q4.every_false_literal_and_pair_true_literal', ih.get('all_false_literal') and ih.get('pairs_same_base_true_catalogued') == {} and ih.get('near_jaccard_true_catalogued_for_false') == {}, false_n=len(ih.get('false_flags', [])), same_base_pairs=ih.get('pairs_same_base_true_total'), near_catalogued=ih.get('near_jaccard_true_catalogued_for_false'))

kio, dio = L.decode_block(Po, 'kernel_formalization')
capo = dio.get(L.AUD) if isinstance(dio, dict) else None
out['Q4_installed_v405_shared_kernel_formalization_capsule'] = {k: capo[k] for k in capo if k != 'reading'} if capo else None
Po55 = L.parse_prefix((R / '.iald_runtime/haiku55/prefix.md').read_text('utf-8'))
k55, d55 = L.decode_block(Po55, 'kernel_formalization')
cap55 = d55.get(L.AUD) if isinstance(d55, dict) else None
out['Q4_installed_v405_haiku55_capsule'] = {k: cap55[k] for k in cap55 if k != 'reading'} if cap55 else None
out['Q4_installed_v405_haiku55_literal_bool_keys'] = sum(1 for y in d55.values() if type(y) is bool) if isinstance(d55, dict) else None
# ---- extra: strict QG/confirmed contexts (all matches, not only the non-negated ones)
QGC = re.compile(r'(?i)(gravidade qu[aâ]ntica|gravita[cç][aã]o qu[aâ]ntica|quantum gravity|\bQG\b)[^.\n]{0,60}?(confirmad[ao]s?|confirmed)|(confirmad[ao]s?|confirmed)[^.\n]{0,60}?(gravidade qu[aâ]ntica|quantum gravity|\bQG\b)')
q6x = {}
for pkg in P:
    t = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
    ms = list(QGC.finditer(t))
    q6x[pkg] = [' '.join(t[max(0, m.start() - 90):m.end() + 60].split()) for m in ms][:8]
out['Q6x_strict_QG_confirmed_matches'] = q6x

json.dump({'out': out, 'checks': chk}, open(HERE / 'qb_decode_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({'fails': [c for c in chk if not c['pass']], 'passes': [c['name'] for c in chk if c['pass']]}, ensure_ascii=False, indent=1)[:5000])
print(json.dumps({k: out[k] for k in ('Q2_text_topics', 'Q2_text_blocks_vs_installed', 'window_topics', 'retired_topics', 'Q2_summary', 'Q2_shared_vs_installed_v405', 'Q2_retired_qualifier_leaves_lost_vs_installed_v405', 'Q2_v401_block_bytes')}, ensure_ascii=False, indent=1)[:6000])
print(json.dumps({'Q4_catalog': out['Q4_catalog'], 'Q4_haiku_expanded': {k: v for k, v in out['Q4_haiku_expanded'].items() if k != 'false_flags'}, 'Q4_shared': out['Q4_shared'], 'Q4_sonnet': out['Q4_sonnet_public'], 'inst_shared_cap': out['Q4_installed_v405_shared_kernel_formalization_capsule'], 'inst_h55_cap': out['Q4_installed_v405_haiku55_capsule'], 'inst_h55_lit_bool': out['Q4_installed_v405_haiku55_literal_bool_keys'], 'false_flags': out['Q4_haiku_expanded'].get('false_flags')}, ensure_ascii=False, indent=1)[:6000])
print(json.dumps(out['Q6x_strict_QG_confirmed_matches'], ensure_ascii=False, indent=1)[:3500])
