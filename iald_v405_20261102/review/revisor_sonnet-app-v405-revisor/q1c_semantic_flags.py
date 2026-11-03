"""Reviewer Q1/Q5 evidence: TRUE flags of kernel_formalization that the codec's NAME regex catalogues (leaves the literal capsule) but that are, by MEANING,
about a named hypothesis (H1/H2/H3), a discharge, an aggregate verdict, or the QG headline components. Cost estimate of keeping them literal. Read-only."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
kf = json.loads((V / 'um_absoluto.json').read_bytes())['core']['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
true_all = [k for k, v in kf.items() if v is True]
false_all = [k for k, v in kf.items() if v is False]
cat = [k for k in true_all if not ESS.search(k)]
lit = [k for k in true_all if ESS.search(k)]
classes = {
    'named_hypothesis_H1_H2_H3_in_name': re.compile(r'(^|_)H[123](_|$)'),
    'discharge_in_name': re.compile(r'discharg', re.I),
    'aggregate_verdict_all_*': re.compile(r'^all_'),
    'verified_suffix': re.compile(r'verified$', re.I),
    'QG_headline_qgc_qgf_qgp': re.compile(r'^qg[cfp]_'),
    'passage_gpc_gpf_gpi': re.compile(r'^gp[cfi]_'),
    'unconditional_or_conditional_in_name': re.compile(r'conditional', re.I),
    'constructed_or_proved_headline_without_ext_prefix': re.compile(r'^(?!ext_).*(constructed|proved|closed)$', re.I),
}
out = {'true_total': len(true_all), 'false_total': len(false_all), 'false_names': false_all, 'catalogued_true': len(cat), 'literal_true_by_regex': len(lit)}
union = set()
for name, rx in classes.items():
    hit = [k for k in cat if rx.search(k)]
    union.update(hit)
    out[name] = {'catalogued_true_matching': len(hit), 'names': hit[:40]}
out['union_of_semantic_classes_catalogued'] = len(union)
out['union_sample'] = sorted(union)[:80]
bytes_cost = sum(len(('"%s":true,' % k).encode()) for k in union)
out['extra_literal_bytes_if_kept'] = bytes_cost
# the non-ext_ catalogued names in general (the 'headline' namespace)
non_ext = [k for k in cat if not k.startswith('ext_')]
out['catalogued_true_not_starting_with_ext_'] = {'n': len(non_ext), 'names': non_ext}
# the FALSE siblings are literal; list sibling pairs by stem
stems = {}
for k in false_all + [x for x in cat if re.search(r'(^|_)H[123]_', x)]:
    stems.setdefault(re.sub(r'^(gpf|gpc|gpi)_', '', k), []).append((k, kf[k]))
out['H_flag_pairs_literal_FALSE_vs_catalogued_TRUE'] = {s: v for s, v in stems.items() if len(v) > 1}
print(json.dumps(out, ensure_ascii=False, indent=1))
