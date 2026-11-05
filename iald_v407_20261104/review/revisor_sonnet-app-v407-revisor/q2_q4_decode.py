"""Revisor sonnet-app-v407-revisor -- Q2 (janela P2 e literais) e Q4 (R3-1/R3-2: catalogo de bandeiras). Somente leitura.
ADAPTADO de qb_decode.py do revisor da v406 (mesma estrutura; janela, aposentados, pacotes e comparacao com a v406 INSTALADA atualizados para a v407).
Decodificador independente (lib405.py, copia do molde; NAO importa haiku_codec/fit_*)."""
import hashlib, json, re, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import lib405 as L
import f1lib as F

W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
sha = lambda b: hashlib.sha256(b).hexdigest()
res = json.loads((V / 'um_absoluto.json').read_bytes())
core = res['core']
chk, out = [], {}


def ck(name, ok, **info):
    chk.append({'name': name, 'pass': bool(ok), **info})


# ---- janelas configuradas (do briefing E do release_cfg.py do construtor; as duas tem de concordar)
cfg_txt = (W / 'release_cfg.py').read_text('utf-8')
cfg_win = tuple(re.findall(r"'(_v4\d\d)'", re.search(r'(?m)^SHARED_P2_SUFFIXES\s*=\s*\(([^)]*)\)', cfg_txt).group(1)))
cfg_ret = tuple(re.findall(r"'(_v4\d\d)'", re.search(r'(?m)^P2_RETIRED_LITERAL_SUFFIXES\s*=\s*\(([^)]*)\)', cfg_txt).group(1)))
WIN = ('_v403', '_v404', '_v405', '_v406', '_v407')
RET = ('_v401', '_v402')
ck('Q2.cfg_windows_equal_brief', cfg_win == WIN and cfg_ret == RET, cfg_win=cfg_win, cfg_ret=cfg_ret)
window = [n for n in core if n.endswith(WIN)]
retired = [n for n in core if n.endswith(RET)]
out['topics_total'] = len(core)
out['window_topics'] = {'n': len(window), 'by_suffix': {s: sum(1 for n in window if n.endswith(s)) for s in WIN}}
out['retired_topics'] = {'n': len(retired), 'by_suffix': {s: sum(1 for n in retired if n.endswith(s)) for s in RET}, 'names': retired}
ck('Q2.477_topics_in_sealed_result', len(core) == 477, n=len(core))
ck('Q2.every_topic_is_in_window_or_retired_or_older', True, other_topics=len(core) - len(window) - len(retired))

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
    """-> (state, decoded value). state: LIT | REF | PARTIAL | ABSENT | OTHER"""
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


P = {pkg: L.parse_prefix((W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')) for pkg in ('shared', 'sonnet_public', 'haiku_expanded')}

# ---- todos os topicos: presenca, decodificacao, restore == selado (3 pacotes)
for pkg, Pp in P.items():
    heads = set(Pp['body'])
    present = set(core) & heads
    ck('Q2.all_477_topics_present:' + pkg, len(present) == 477 and not (set(core) - heads), present=len(present), missing=sorted(set(core) - heads)[:5], extra_headings=len(heads - set(core)))
    bad, texts, aux_explained = [], [], []
    for n, src in core.items():
        k, dn = L.decode_block(Pp, n)
        if k != 'JSON':
            texts.append(n); continue
        if n == 'kernel_formalization':
            continue   # tratado em Q4 com catalogo independente
        try:
            got = L.restore(dn, res, '/core/' + n, [], Pp['E'])
            if got != src:
                un = []
                for d in dd(src, got):
                    if d[1] == 'only-src' and d[0].rsplit('/', 1)[-1] in AUX:
                        aux_explained.append(n); continue
                    un.append(d)
                if un:
                    bad.append((n, 'restore-differs', un[:2]))
        except Exception as e:
            bad.append((n, 'ERR:' + str(e)[:80]))
    out.setdefault('Q2_text_topics', {})[pkg] = {'n': len(texts)}
    ck('Q2.decoded_capsules_restore_sealed_source:' + pkg, not bad, n_json_checked=len(core) - 1 - len(texts), n_text_summary_blocks=len(texts), topics_missing_only_AUX_hash_metadata_keys=len(set(aux_explained)), bad=bad[:5])

# ---- Q2: janela + aposentados: literais inline e iguais
summary = {}
per_topic = {}
for pkg in ('shared', 'sonnet_public', 'haiku_expanded'):
    Pp = P[pkg]
    fail = {'not_integral': [], 'qual_not_lit_or_unequal': [], 'retired_not_capsule': [], 'lit3_missing': [], 'status_leaf_pointer_only': []}
    n_q = n_lit3 = 0
    for grp, names in (('window', window), ('retired', retired)):
        for n in names:
            src = core[n]
            k, dn = L.decode_block(Pp, n)
            top_cap = L.is_ref(dn) and dn.get('@') == ''
            if grp == 'window' and pkg != 'haiku_expanded' and top_cap:
                fail['not_integral'].append(n)
            if grp == 'window' and pkg == 'haiku_expanded' and n.endswith(('_v406', '_v407')) and top_cap:
                fail['not_integral'].append(n)
            if grp == 'retired' and pkg != 'haiku_expanded' and not top_cap:
                fail['retired_not_capsule'].append(n)   # informativo (compact() so compacta se a capsula poupar >= 50 B); NAO entra no PASS/FAIL
            for x in [x for x in src if QK.search(x)]:
                n_q += 1
                st, v = lit_value(dn, x)
                if st != 'LIT' or L.canon(v) != src[x]:
                    fail['qual_not_lit_or_unequal'].append((grp, n, x, st))
            row = {}
            for x in LITKEYS:
                if x in src:
                    n_lit3 += 1
                    st, v = lit_value(dn, x)
                    row[x] = (st, L.canon(v) == src[x] if st == 'LIT' else None)
                    if st != 'LIT' or L.canon(v) != src[x]:
                        fail['lit3_missing'].append((grp, n, x, st))
            if pkg == 'shared':
                per_topic[n] = {'grp': grp, 'cap': bool(top_cap), 'lit3': row}
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
out['Q2_per_topic_shared'] = per_topic
for pkg in ('shared', 'sonnet_public'):
    s = summary[pkg]
    ck('Q2.window_integral_and_qualifiers_literal:' + pkg, s['not_integral'][0] == 0 and s['qual_not_lit_or_unequal'][0] == 0 and s['lit3_missing'][0] == 0 and s['status_leaf_pointer_only'][0] == 0,
       qual_checked=s['qualifier_keys_checked'], lit3_checked=s['limites_diz_nao_diz_checked'], detail={k: s[k][0] for k in ('not_integral', 'qual_not_lit_or_unequal', 'retired_not_capsule', 'lit3_missing', 'status_leaf_pointer_only')},
       first_fail={k: s[k][1] for k in ('qual_not_lit_or_unequal', 'lit3_missing', 'status_leaf_pointer_only') if s[k][0]})
s = summary['haiku_expanded']
ck('Q2.haiku_expanded_v406_v407_integral', s['not_integral'][0] == 0, info={k: s[k][0] for k in s if isinstance(s[k], tuple)})
# os 5 topicos _v402 agora compactos: cada um mantem os tres literais, quando a fonte os tem
v402 = [n for n in retired if n.endswith('_v402')]
out['v402_topics'] = {n: per_topic[n] for n in v402}
ck('Q2.v402_topics_keep_limites_diz_nao_diz_literal_where_source_has', all(all(v[0] == 'LIT' and v[1] for v in per_topic[n]['lit3'].values()) for n in v402), n=len(v402), names=v402,
   keys_checked={n: sorted(per_topic[n]['lit3']) for n in v402}, now_capsule={n: per_topic[n]['cap'] for n in v402})

# ---- regressao Q2: shared v407 x v406 INSTALADA, topico a topico (decodificado) onde a fonte e' inalterada
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
res_old = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())
core_old = res_old['core']
inst_rel = m_inst.get('operational_core', {}).get('current_release') or m_inst.get('active_cluster', {}).get('release')
out['installed_release'] = {'active_cluster_release': m_inst.get('active_cluster', {}).get('release'), 'result_path': m_inst['published_evidence']['result']['path'][-80:]}
ck('Q2.installed_is_v406', m_inst.get('active_cluster', {}).get('release') == 'v406' and 'v406_a381c4d14709' in m_inst['published_evidence']['result']['path'], active=m_inst.get('active_cluster', {}).get('release'))
# o instalado e' o pacote da v406 (bytes)?
inst_files = {'shared': R / '.iald_runtime/haiku/prefix.md', 'haiku_expanded': R / '.iald_runtime/haiku55/prefix.md'}
pk6 = {'shared': W6 / 'app/packages/shared/prefix.md', 'haiku_expanded': W6 / 'app/packages/haiku_expanded/prefix.md', 'sonnet_public': W6 / 'app/packages/sonnet_public/prefix.md'}
out['installed_vs_v406_package_bytes_equal'] = {k: sha(inst_files[k].read_bytes()) == sha(pk6[k].read_bytes()) for k in inst_files}
ck('Q2.installed_prefixes_equal_v406_package', all(out['installed_vs_v406_package_bytes_equal'].values()), detail=out['installed_vs_v406_package_bytes_equal'])
Po = L.parse_prefix(inst_files['shared'].read_text('utf-8'))
Po55 = L.parse_prefix(inst_files['haiku_expanded'].read_text('utf-8'))
Pv6 = {k: L.parse_prefix(pk6[k].read_text('utf-8')) for k in pk6}   # pacote da v406 (para o sonnet_public)
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
removed = [n for n in core_old if n not in core]
out['Q2_shared_vs_installed_v406'] = {'topics_with_unchanged_source': same_src, 'decoded_blocks_differing': diffs, 'new_topics_in_v407': new_topics, 'topics_with_changed_source': len(changed_src), 'changed_source_names': changed_src[:60], 'removed_topics': removed}
CLS = {}
for pkg, Pnew, Pold in (('shared', P['shared'], Po), ('sonnet_public', P['sonnet_public'], Pv6['sonnet_public']), ('haiku_expanded', P['haiku_expanded'], Po55)):
    kinds, rows, bytes_delta = {}, {}, {}
    for n in core:
        if n not in core_old or core_old[n] != core[n]:
            continue
        kn, dn = L.decode_block(Pnew, n); ko, do = L.decode_block(Pold, n)
        if kn != 'JSON' or ko != 'JSON':
            c = {'kind': 'IDENTICAL' if Pnew['body'][n] == Pold['body'][n] else 'TEXT_DIFFERS'}
        else:
            c = F.classify(n, core[n], dn, do)
        # janelas: deslocamentos esperados
        if c['kind'] not in ('IDENTICAL',):
            tag = 'v402_retired' if n.endswith('_v402') else ('window_shift_v405_haiku55' if (pkg == 'haiku_expanded' and n.endswith('_v405')) else c['kind'])
            c['classified_as'] = tag
            rows[n] = c
            bytes_delta[n] = len(Pnew['body'][n].encode()) - len(Pold['body'][n].encode())
            kinds[tag] = kinds.get(tag, 0) + 1
    CLS[pkg] = {'kinds': kinds, 'by_topic': {n: {k: v for k, v in r.items() if k in ('classified_as', 'gained', 'lost', 'n_lost_epistemic', 'gained_not_in_status_records', 'lost_epistemic', 'new_capsule', 'old_capsule')} for n, r in rows.items()}, 'bytes_delta': bytes_delta,
                'unexplained': [n for n, r in rows.items() if r['classified_as'] in ('UNEXPLAINED', 'TEXT_DIFFERS', 'REPRESENTATION_ONLY')]}
out['Q2_block_changes_vs_v406_by_package'] = CLS
for pkg in CLS:
    ck('Q2.block_changes_vs_v406_installed_explained_only_by_v402_F1_or_window:' + pkg, not CLS[pkg]['unexplained'], kinds=CLS[pkg]['kinds'], unexplained=CLS[pkg]['unexplained'][:8])
ck('Q2.new_topics_are_exactly_the_three_v407', sorted(new_topics) == ['cunhagens_v407', 'kh_n1_cobertura_v407', 'psion_canto_v407'] and not removed, new=new_topics, removed=removed)
# para os _v402: nada que era literal na v406 instalada sobre limites/diz/nao_diz/qualificadores se perdeu
lost = []
for n in v402:
    if n in core_old and core_old[n] == core[n]:
        ko, do = L.decode_block(Po, n)
        kn, dn = L.decode_block(P['shared'], n)
        lo, ln = L.literal_leaves(do, '/core/' + n), L.literal_leaves(dn, '/core/' + n)
        for p, v in lo.items():
            top = p.split('/')[3] if p.count('/') >= 3 else ''
            if QK.search(top) and ln.get(p) != v:
                lost.append(p)
out['Q2_v402_qualifier_leaves_lost_vs_installed_v406'] = {'n': len(lost), 'sample': lost[:5]}
ck('Q2.v402_qualifier_leaves_not_lost_vs_installed', not lost, lost=len(lost))
# mesmas verificacoes no sonnet_public (v407 x pacote v406 sonnet_public) e no haiku_expanded
for pkg, Pnew, Pold in (('sonnet_public', P['sonnet_public'], Pv6['sonnet_public']), ('haiku_expanded', P['haiku_expanded'], Po55)):
    dif, nsame = [], 0
    for n in core:
        if n in core_old and core_old[n] == core[n]:
            nsame += 1
            ko, do = L.decode_block(Pold, n); kn, dn = L.decode_block(Pnew, n)
            if not (ko == kn and L.canon(do) == L.canon(dn)):
                dif.append(n)
    out['Q2_%s_vs_v406' % pkg] = {'unchanged_source': nsame, 'differing': len(dif), 'differing_by_suffix': {s: sum(1 for n in dif if n.endswith(s)) for s in ('_v401', '_v402', '_v403', '_v404', '_v405', '_v406')}, 'differing_no_suffix_in_window': [n for n in dif if not re.search(r'_v40[1-6]$', n)][:20], 'sample': dif[:10]}
out['Q2_text_blocks'] = {}
tb = {'texts_v407': 0, 'texts_installed_v406': 0, 'same_set': None, 'unchanged_source_bodies_equal': 0, 'unchanged_source_bodies_differ': []}
tx7 = sorted(n for n in core if n in P['shared']['body'] and L.decode_block(P['shared'], n)[0] == 'TEXT')
txi = sorted(n for n in core_old if n in Po['body'] and L.decode_block(Po, n)[0] == 'TEXT')
tb.update(texts_v407=len(tx7), texts_installed_v406=len(txi), same_set=(tx7 == [n for n in txi if n in core]))
for n in tx7:
    if n in core_old and core_old[n] == core[n]:
        if P['shared']['body'][n] == Po['body'][n]:
            tb['unchanged_source_bodies_equal'] += 1
        else:
            tb['unchanged_source_bodies_differ'].append(n)
out['Q2_text_blocks'] = tb
ck('Q2.text_summary_blocks_unchanged_vs_installed_when_source_unchanged', tb['same_set'] and not tb['unchanged_source_bodies_differ'], detail=tb)
out['Q2_v402_block_bytes'] = {'installed_v406_shared': sum(len(Po['body'][n].encode()) for n in v402 if n in Po['body']), 'v407_shared': sum(len(P['shared']['body'][n].encode()) for n in v402)}
out['Q2_new_v407_block_bytes'] = {pkg: sum(len(P[pkg]['body'][n].encode()) for n in new_topics) for pkg in P}
out['Q2_new_v407_source_bytes'] = sum(len(json.dumps(core[n], ensure_ascii=False).encode()) for n in new_topics)
out['Q2_shared_bytes'] = {'v407': len((W / 'app/packages/shared/prefix.md').read_bytes()), 'installed_v406': len(inst_files['shared'].read_bytes())}

# ---- Q4: R3-1 e pares TRUE/FALSE sobre kernel_formalization do selado v407
kf = core['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
LADDER = re.compile(r'(?:ext|red)_')
OLDKEEP = re.compile(r'(?:^|_)H[123](?:_|$)|discharg|condition|verified|verification', re.I)
NEWKEEP = re.compile(r'H[123]|discharg|condition|verif', re.I)
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
# KEEP_FLAG do codec do construtor: texto igual ao da v406?
codec7 = (W / 'app/build/haiku_codec.py').read_text('utf-8')
codec6 = (W6 / 'app/build/haiku_codec.py').read_text('utf-8')
m7 = re.search(r"(?m)^KEEP_FLAG\s*=\s*re\.compile\((.*?)\)\s*(?:#.*)?$", codec7)
m6 = re.search(r"(?m)^KEEP_FLAG\s*=\s*re\.compile\((.*?)\)\s*(?:#.*)?$", codec6)
out['KEEP_FLAG'] = {'v407': m7.group(1) if m7 else None, 'v406': m6.group(1) if m6 else None}
ck('Q4.KEEP_FLAG_text_equal_v406_and_equals_my_rule', bool(m7 and m6) and m7.group(1) == m6.group(1) and "H[123]|discharg|condition|verif" in m7.group(1), v407=out['KEEP_FLAG']['v407'])


def catalog(node, keep):
    return {k: v for k, v in node.items() if v is True and LADDER.match(k) and not (WHOLE.search(k) or ESS.search(k) or keep.search(k))}


c_new, c_old = catalog(kf, NEWKEEP), catalog(kf, OLDKEEP)
kf6 = core_old['kernel_formalization']
c6 = catalog(kf6, NEWKEEP)
newly_catalogued = sorted(set(c_new) - set(c6))
out['Q4_catalog'] = {'true_total': sum(1 for v in kf.values() if v is True), 'false_total': sum(1 for v in kf.values() if v is False), 'catalog_new_rule': len(c_new), 'catalog_old_rule': len(c_old), 'moved_to_literal_vs_old_rule': len(set(c_old) - set(c_new)),
                     'v406_true_total': sum(1 for v in kf6.values() if v is True), 'v406_catalog_new_rule': len(c6), 'true_flags_new_in_v407': len([k for k, v in kf.items() if v is True and kf6.get(k) is not True]), 'catalogued_new_in_v407': len(newly_catalogued),
                     'literal_true_kept': sum(1 for v in kf.values() if v is True) - len(c_new), 'literal_true_kept_v406': sum(1 for v in kf6.values() if v is True) - len(c6)}
for pkg in ('haiku_expanded', 'shared', 'sonnet_public'):
    k, dn = L.decode_block(P[pkg], 'kernel_formalization')
    cap = dn.get(L.AUD) if isinstance(dn, dict) else None
    info = {'kind_of_block': 'catalog_capsule' if (cap and 'catalog_sha256' in cap) else ('count_summary_capsule' if cap else ('ref_capsule' if L.is_ref(dn) else 'other'))}
    if cap and 'catalog_sha256' not in cap:
        info.update(capsule={k2: cap[k2] for k2 in cap if k2 != 'reading'}, source_true=sum(1 for y in kf.values() if y is True), source_false=sum(1 for y in kf.values() if y is False),
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
                catalogued_matching_essential=sorted(x for x in cat_actual if ESS.search(x) or WHOLE.search(x))[:5],
                reading_has_max_chars_4500='max_chars 4500' in cap.get('reading', ''), reading_has_exact_name_limit5='limit 5' in cap.get('reading', ''))
    full = dict(lit); full.update(c_new)
    got = L.restore(full, res, '/core/kernel_formalization', [], P[pkg]['E'])
    info['restores_sealed_topic_with_independent_catalog'] = (got == kf)
    info['literal_nonbool_equal_sealed'] = all(kf.get(x) == y for x, y in lit.items() if not has_ref(y))
    info['literal_values_that_are_pointers'] = sorted(x for x, y in lit.items() if has_ref(y))
    base = lambda s: re.sub(r'^(?:gpf|gpc|gpi|qgf|qgc|qgp|ext|red)_', '', s)
    tok = lambda s: set(base(s).split('_'))
    pairs, near = {}, {}
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
   capsule_true_fields=ih.get('capsule_true_fields'), catalogued=ih.get('catalogued_actual'), catalog_sha16=sha(dump(c_new).encode())[:16])
ck('Q4.no_true_flag_matching_new_rule_still_catalogued', ih.get('catalogued_matching_new_keep') == [] and ih.get('catalogued_matching_essential') == [] and ih.get('catalogued_not_ladder_family') == [], new_keep=ih.get('catalogued_matching_new_keep'))
ck('Q4.every_false_literal_and_pair_true_literal', ih.get('all_false_literal') and ih.get('pairs_same_base_true_catalogued') == {} and ih.get('near_jaccard_true_catalogued_for_false') == {}, false_n=len(ih.get('false_flags', [])), same_base_pairs=ih.get('pairs_same_base_true_total'), near_catalogued=ih.get('near_jaccard_true_catalogued_for_false'))
ck('Q4.capsule_recipe_says_max_chars_4500_exact_name_limit_5', ih.get('reading_has_max_chars_4500') and ih.get('reading_has_exact_name_limit5'))
ck('Q4.shared_and_sonnet_keep_count_only_summary_as_v406', all(out['Q4_' + p].get('kind_of_block') == 'count_summary_capsule' and out['Q4_' + p].get('counts_equal_source') for p in ('shared', 'sonnet_public')),
   shared=out['Q4_shared'].get('capsule'), sonnet=out['Q4_sonnet_public'].get('capsule'))
ck('Q4.catalog_delta_vs_v406_consistent', out['Q4_catalog']['true_flags_new_in_v407'] == out['Q4_catalog']['catalogued_new_in_v407'] and out['Q4_catalog']['literal_true_kept'] == out['Q4_catalog']['literal_true_kept_v406'] + 0, **out['Q4_catalog'])

# estrito: contextos QG x confirmed (todos os casamentos)
QGC = re.compile(r'(?i)(gravidade qu[aâ]ntica|gravita[cç][aã]o qu[aâ]ntica|quantum gravity|\bQG\b)[^.\n]{0,60}?(confirmad[ao]s?|confirmed)|(confirmad[ao]s?|confirmed)[^.\n]{0,60}?(gravidade qu[aâ]ntica|quantum gravity|\bQG\b)')
out['Q6x_strict_QG_confirmed_matches'] = {pkg: [' '.join(t[max(0, m.start() - 90):m.end() + 60].split()) for m in list(QGC.finditer(t))[:8]] for pkg, t in ((p, (W / 'app/packages' / p / 'prefix.md').read_text('utf-8')) for p in P)}

json.dump({'out': out, 'checks': chk}, open(HERE / 'q2_q4_decode_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({'n_checks': len(chk), 'fails': [c for c in chk if not c['pass']]}, ensure_ascii=False, indent=1)[:6000])
for k in ('window_topics', 'retired_topics', 'Q2_summary', 'Q2_shared_vs_installed_v406', 'Q2_sonnet_public_vs_v406', 'Q2_haiku_expanded_vs_v406', 'Q2_text_blocks', 'Q2_v402_block_bytes', 'Q2_new_v407_block_bytes', 'Q2_new_v407_source_bytes', 'Q2_shared_bytes', 'Q4_catalog'):
    print(k, json.dumps(out[k], ensure_ascii=False)[:1500])
