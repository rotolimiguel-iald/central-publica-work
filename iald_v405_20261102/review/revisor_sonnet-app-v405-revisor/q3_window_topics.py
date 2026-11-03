"""Reviewer Q3 (adapted from the v404 reviewer's q2_check18): for the P2-window topics (_v401.._v405) in shared and sonnet_public (and haiku_expanded for information):
 (a) block decodes and restores EXACTLY to the sealed topic;
 (b) every source top-level key that is a qualifier (status|statute|estatuto|verdict|veredit|scope|escopo|limites|diz|nao_diz|not_claimed|...) is INLINE and equal to the source;
 (c) every status-like leaf (last path component status|statute|estatuto|verdict|veredit*) outside the registers `unconditional`, `index_conditional`, `named_pending` is literal;
 (d) the block is NOT a top-level compact capsule;
 (e) topics that existed in the installed v404 shared decode IDENTICALLY to the installed block (no literal that was inline left)."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
res_old = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())
core_old = res_old['core']
res_new = json.loads((Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405') / 'um_absoluto.json').read_bytes())
core_new = res_new['core']
rel_cfg = (W / 'release_cfg.py').read_text('utf-8')
suffixes = tuple(re.findall(r"'(_v4\d\d)'", re.search(r'(?m)^SHARED_P2_SUFFIXES\s*=\s*\(([^)]*)\)', rel_cfg).group(1)))
window = [n for n in core_new if n.endswith(suffixes)]
QK = re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|limites|^diz$|^nao_diz$', re.I)  # strict set = the v404 reviewer's check 18
QKX = re.compile(r'not_claimed|not_said|declar|conditional|condicional|hypothes|hip[oó]tese', re.I)  # extended set (information only)
SL = re.compile(r'^(?:status|statute|estatuto|verdict|veredit\w*)$', re.I)
EXEMPT = {'unconditional', 'index_conditional', 'named_pending'}
out = {'suffixes': suffixes, 'window_topics': len(window), 'window_list': window}
for pkg in ('shared', 'sonnet_public', 'haiku_expanded'):
    Pn = L.parse_prefix((W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8'))
    rows = {}
    for n in window:
        kn, dn = L.decode_block(Pn, n)
        src = core_new[n]
        row = {'kind': kn}
        if kn != 'JSON':
            row['ok'] = False
            rows[n] = row
            continue
        rep = []
        try:
            got = L.restore(L.catalog_full(dn, src) if n == 'kernel_formalization' else dn, res_new, '/core/' + n, rep, Pn['E'])
            exact = (got == src)
        except Exception as e:
            exact = False
            row['err'] = str(e)[:100]
        top_cap = L.is_ref(dn) and dn.get('@') == ''
        # inline top-level keys
        if L.is_ref(dn):
            inl = {k.split('/')[1] for k in dn.get('fields', {}) if k.count('/') >= 1}
        else:
            inl = {k for k, x in dn.items() if not L.is_ref(x)}
        qkeys = [k for k in src if QK.search(k)]
        missing = [k for k in qkeys if k not in inl]
        qx = [k for k in src if QKX.search(k) and not QK.search(k)]
        row['extended_qualifier_keys_not_inline'] = [k for k in qx if k not in inl]
        lp = L.literal_leaves(dn, '/core/' + n)
        lps = set(lp)
        stat_missing = []
        stat_exempt = 0
        for p, v in L.leaves(src, '/core/' + n):
            last = p.rsplit('/', 1)[-1]
            if not SL.match(last):
                continue
            if p in lps or any(q.startswith(p + '/') or p.startswith(q + '/') for q in lps):
                continue
            top = p.split('/')[3] if p.count('/') >= 3 else ''
            if top in EXEMPT:
                stat_exempt += 1
            else:
                stat_missing.append(p)
        # qualifier leaves total/literal
        qleaves = [(p, v) for p, v in L.leaves(src, '/core/' + n) if any(QK.search(part) for part in p.split('/')[3:4])]
        qlit = sum(1 for p, v in qleaves if p in lps)
        row.update(exact=exact, top_level_capsule=top_cap, qualifier_keys=qkeys, qualifier_keys_not_inline=missing, status_leaves_pointer_only_outside_registers=stat_missing, status_leaves_exempt_registers=stat_exempt,
                   source_top_keys=len(src), literal_leaf_fraction=round(len(lp) / max(1, sum(1 for _ in L.leaves(src, '/core/' + n))), 3))
        row['ok'] = bool(exact and not top_cap and not missing and not stat_missing)
        rows[n] = row
    out[pkg] = {'all_ok': all(r['ok'] for r in rows.values()), 'failing': [n for n, r in rows.items() if not r['ok']], 'rows': rows}
# (e) identity against the installed v404 shared for window topics that existed there
Po = L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'))
Pn = L.parse_prefix((W / 'app/packages/shared/prefix.md').read_text('utf-8'))
ident = {}
for n in window:
    if n in core_old:
        ko, do = L.decode_block(Po, n)
        kn, dn = L.decode_block(Pn, n)
        same_src = core_old[n] == core_new[n]
        ident[n] = {'src_same': same_src, 'decoded_identical_to_installed': (ko == kn and L.canon(do) == L.canon(dn)) if ko == 'JSON' and kn == 'JSON' else None}
out['shared_vs_installed_for_window_topics_existing_before'] = ident
out['shared_vs_installed_summary'] = {'topics': len(ident), 'src_same': sum(1 for v in ident.values() if v['src_same']), 'decoded_identical_and_src_same': sum(1 for v in ident.values() if v['src_same'] and v['decoded_identical_to_installed']),
                                      'src_changed_window_topics': [n for n, v in ident.items() if not v['src_same']]}
print(json.dumps({k: (v if k not in ('shared', 'sonnet_public', 'haiku_expanded') else {'all_ok': v['all_ok'], 'failing': v['failing']}) for k, v in out.items() if k != 'shared_vs_installed_for_window_topics_existing_before'}, ensure_ascii=False, indent=1))
json.dump(out, open(Path(__file__).parent / 'q3_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
