"""Reviewer Q1/Q5 evidence (F1): for the TRUE flags of kernel_formalization that are catalogue-only and fall in 7 semantic classes (named hypothesis H1/H2/H3 in the name, discharge,
aggregate all_*, verified suffix, QG headline qgc/qgf/qgp, passage gpc/gpf/gpi, conditional), is the same fact carried LITERALLY elsewhere in the haiku_expanded prefix
(exact name or the stem after the gp?/qg? prefix, searched in the decoded nucleus + every other topic + dictionary + exposition, excluding the kernel_formalization capsule itself)?
Also repeats for the shared package. Read-only."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
kf = core['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
cat = [k for k, v in kf.items() if v is True and not ESS.search(k)]
CLASSES = {'H1_H2_H3_in_name': re.compile(r'(^|_)H[123](_|$)'), 'discharge': re.compile(r'discharg', re.I), 'aggregate_all': re.compile(r'^all_'), 'verified_suffix': re.compile(r'verified$', re.I),
           'QG_headline_qgc_qgf_qgp': re.compile(r'^qg[cfp]_'), 'passage_gpc_gpf_gpi': re.compile(r'^gp[cfi]_'), 'conditional': re.compile(r'conditional', re.I)}
union = [k for k in cat if any(r.search(k) for r in CLASSES.values())]


def decoded(pkg):
    t = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
    P = L.parse_prefix(t)
    parts = [t.split('\n### ', 1)[0]]
    for lid, val in P['D'].items():
        dv = L.dec_lit(val, P['D'], P['E'])
        parts.append(dv if isinstance(dv, str) else json.dumps(L.canon(dv), ensure_ascii=False))
    for n in P['body']:
        if n == 'kernel_formalization':
            continue
        k, dv = L.decode_block(P, n)
        parts.append(json.dumps(L.canon(dv), ensure_ascii=False) if k == 'JSON' else dv)
    parts.append(P['E'])
    return '\n'.join(parts)


out = {'catalogued_true': len(cat), 'classes': {n: len([k for k in cat if r.search(k)]) for n, r in CLASSES.items()}, 'union_7_classes': len(union)}
for pkg in ('haiku_expanded', 'shared'):
    D = decoded(pkg)
    carried, zero = [], []
    for k in union:
        stem = re.sub(r'^(gp[a-z]|qg[a-z])_', '', k)
        n_exact = len(re.findall(re.escape(k), D))
        n_stem = len(re.findall(re.escape(stem), D)) if stem != k else n_exact
        (carried if (n_exact or n_stem) else zero).append(k)
    out[pkg] = {'carried_literally_elsewhere': len(carried), 'catalogue_only': len(zero), 'catalogue_only_names': zero}
# the aggregate flags the reader would look for first
focus = ['all_verified', 'all_unconditional_targets_verified', 'all_conditional_implications_verified', 'formal_release_ready', 'specific_AQFT_witness_constructed',
         'gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced', 'gpf_H1_internal_susy_relative_gap_discharged']
Dh = decoded('haiku_expanded')
out['focus'] = {k: {'value': kf[k], 'catalogue_only_in_capsule': k in cat, 'exact_name_elsewhere': len(re.findall(re.escape(k), Dh)),
                    'stem_elsewhere': len(re.findall(re.escape(re.sub(r'^(gp[a-z]|qg[a-z])_', '', k)), Dh))} for k in focus}
print(json.dumps(out, ensure_ascii=False, indent=1))
