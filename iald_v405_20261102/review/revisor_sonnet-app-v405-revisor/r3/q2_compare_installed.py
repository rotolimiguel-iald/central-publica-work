"""Reviewer Q2/Q3: topic-by-topic comparison of each v405 package with the INSTALLED v404 one (read-only on R).
For every topic in both sealed cores: raw block bytes, decoded size, decoded equality, literal-leaf loss.
usage: q2_compare_installed.py <new_package: haiku_expanded|shared|sonnet_public> <installed_dir under R/.iald_runtime: haiku55|haiku|none>"""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
pkg_new = sys.argv[1]
inst_dir = sys.argv[2]
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
res_old = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())
core_old = res_old['core']
V404 = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v404\um_absoluto.json')
assert L.sha(V404.read_bytes()) == L.sha(Path(m_inst['published_evidence']['result']['path']).read_bytes()), 'installed result is not the v404 vault core'
res_new = json.loads((Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405') / 'um_absoluto.json').read_bytes())
core_new = res_new['core']
Pn = L.parse_prefix((W / 'app/packages' / pkg_new / 'prefix.md').read_text('utf-8'))
# inst_dir either a folder under R/.iald_runtime (installed) or 'PATH:<file>' (e.g. the v404 BUILT sonnet_public prefix, never installed)
OLD_PREFIX_PATH = Path(inst_dir[5:]) if inst_dir.startswith('PATH:') else (R / '.iald_runtime' / inst_dir / 'prefix.md')
Po = L.parse_prefix(OLD_PREFIX_PATH.read_text('utf-8'))
common = [n for n in core_new if n in core_old]
only_new = [n for n in core_new if n not in core_old]
only_old = [n for n in core_old if n not in core_new]
changed = [n for n in common if core_new[n] != core_old[n]]
same = [n for n in common if core_new[n] == core_old[n]]
rows = []
for n in common:
    kn, dn = L.decode_block(Pn, n)
    ko, do = L.decode_block(Po, n)
    rb_new = len(Pn['body'][n].encode())
    rb_old = len(Po['body'][n].encode())
    row = {'topic': n, 'src_same': core_new[n] == core_old[n], 'kind_old': ko, 'kind_new': kn, 'raw_old': rb_old, 'raw_new': rb_new}
    if kn == 'JSON' and ko == 'JSON':
        # compare decoded carried information, ignoring dictionary renumbering; the catalog capsule is compared as-is
        co, cn = L.canon(do), L.canon(dn)
        row['decoded_equal'] = (co == cn)
        so, sn = len(L.dump(co).encode()), len(L.dump(cn).encode())
        row['dec_old'], row['dec_new'] = so, sn
        lo = L.literal_leaves(do, '/core/' + n)
        ln = L.literal_leaves(dn, '/core/' + n)
        lost = [p for p in lo if p not in ln]
        gained = [p for p in ln if p not in lo]
        row['literal_leaves_old'], row['literal_leaves_new'] = len(lo), len(ln)
        row['lost_literal_leaf_paths'] = len(lost)
        row['lost_sample'] = lost[:6]
        row['gained_literal_leaf_paths'] = len(gained)
        # lost leaves whose VALUE also changed vs. kept with a different value
        row['value_changed_leaves'] = len([p for p in lo if p in ln and lo[p] != ln[p]])
    else:
        row['decoded_equal'] = (do == dn) if (kn == ko) else False
        row['text_old'] = len(do) if ko == 'TEXT' else None
        row['text_new'] = len(dn) if kn == 'TEXT' else None
    rows.append(row)
summ = {
    'package': pkg_new, 'installed': inst_dir, 'common_topics': len(common), 'only_in_new_core': only_new, 'only_in_old_core': only_old,
    'src_changed_topics': len(changed), 'src_same_topics': len(same),
    'bytes_prefix_new': len((W / 'app/packages' / pkg_new / 'prefix.md').read_bytes()), 'bytes_prefix_old': len(OLD_PREFIX_PATH.read_bytes()),
}
# Classification
same_rows = [r for r in rows if r['src_same']]
summ['src_same_decoded_equal'] = sum(1 for r in same_rows if r['decoded_equal'])
summ['src_same_decoded_differ'] = [r['topic'] for r in same_rows if not r['decoded_equal']]
summ['src_same_shrunk_decoded'] = [(r['topic'], r.get('dec_old'), r.get('dec_new')) for r in same_rows if r.get('dec_new') is not None and r['dec_new'] < r['dec_old']]
summ['src_same_lost_literal_leaves'] = [(r['topic'], r['lost_literal_leaf_paths'], r['lost_sample']) for r in same_rows if r.get('lost_literal_leaf_paths')]
summ['src_same_kind_changed'] = [(r['topic'], r['kind_old'], r['kind_new']) for r in same_rows if r['kind_old'] != r['kind_new']]
summ['src_same_raw_shrunk_bytes'] = sorted([(r['topic'], r['raw_old'], r['raw_new']) for r in same_rows if r['raw_new'] < r['raw_old']], key=lambda t: t[2] - t[1])[:40]
ch_rows = [r for r in rows if not r['src_same']]
summ['src_changed_topic_list'] = [{'topic': r['topic'], 'raw_old': r['raw_old'], 'raw_new': r['raw_new'], 'dec_old': r.get('dec_old'), 'dec_new': r.get('dec_new'), 'lost_literal_leaves': r.get('lost_literal_leaf_paths'), 'gained': r.get('gained_literal_leaf_paths'), 'kind': (r['kind_old'], r['kind_new'])} for r in ch_rows]
summ['src_changed_shrunk'] = [(r['topic'], r.get('dec_old'), r.get('dec_new')) for r in ch_rows if r.get('dec_new') is not None and r['dec_new'] < r['dec_old']]
# new topics: form + exactness
new_info = []
for n in only_new:
    kn, dn = L.decode_block(Pn, n)
    rep = []
    try:
        dvc = L.catalog_full(dn, core_new[n]) if kn == 'JSON' and isinstance(dn, dict) else dn
        got = L.restore(dvc, res_new, '/core/' + n, rep, Pn['E']) if kn == 'JSON' else None
        exact = (got == core_new[n]) if kn == 'JSON' else None
    except Exception as e:
        exact = 'ERR ' + str(e)[:100]
    lv = L.literal_leaves(dn, '/core/' + n) if kn == 'JSON' else {}
    total_leaves = sum(1 for _ in L.leaves(core_new[n], '/core/' + n))
    new_info.append({'topic': n, 'kind': kn, 'restores_exact': exact, 'raw_bytes': len(Pn['body'][n].encode()), 'literal_leaves_in_prompt': len(lv), 'leaves_in_source': total_leaves, 'top_level_reference': (kn == 'JSON' and L.is_ref(dn))})
summ['new_topics'] = new_info
print(json.dumps(summ, ensure_ascii=False, indent=1))
json.dump(rows, open(Path(__file__).parent / ('q2_rows_%s.json' % pkg_new), 'w', encoding='utf8'), ensure_ascii=False)
