# -*- coding: utf-8 -*-
"""Reviewer r3 (second round) Q1/Q5: with MY 7 semantic classes (written before running, in r1) and the clause-by-clause text of the NEW reading.
Everything is recomputed from the SEALED core and from the decoded r3 capsule (independent decoder lib405; the codec's own KEEP_FLAG/LADDER_FLAG are NOT used to decide anything,
only quoted). Read-only; prints JSON."""
import json, re, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
kf = core['kernel_formalization']
AUD = 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE'

# ---- decode the r3 capsule (haiku_expanded) and the r1 capsule (superseded_r1) -----------------------------------------------------
def capsule(path):
    P = L.parse_prefix(Path(path).read_text('utf-8'))
    kind, dv = L.decode_block(P, 'kernel_formalization')
    assert kind == 'JSON'
    return dv

dv3 = capsule(W / 'app/packages/haiku_expanded/prefix.md')
dv1 = capsule(W / 'superseded_r1/app/packages/haiku_expanded/prefix.md')
cap3 = dv3[AUD]
lit3_true = {k for k, v in dv3.items() if v is True}
lit3_false = {k for k, v in dv3.items() if v is False}
true_src = [k for k, v in kf.items() if v is True]
false_src = [k for k, v in kf.items() if v is False]
cat3 = [k for k in true_src if k not in lit3_true]          # TRUE flags that live only in the source (catalogue), recomputed from the capsule, in source order
lit1_true = {k for k, v in dv1.items() if v is True}
cat1 = [k for k in true_src if k not in lit1_true]          # idem for r1
out = {'r3_capsule_fields': sorted(cap3), 'reading_r3': cap3['reading'],
       'counts': {'source_true': len(true_src), 'source_false': len(false_src), 'literal_true_r3': len(lit3_true), 'literal_false_r3': len(lit3_false), 'catalogued_true_r3': len(cat3), 'catalogued_true_r1': len(cat1),
                  'capsule_true_fields': cap3['true_fields'], 'capsule_true_fields_equals_catalogued': cap3['true_fields'] == len(cat3),
                  'catalog_sha256_capsule': cap3['catalog_sha256'], 'catalog_sha256_recomputed': L.sha(L.dump({k: True for k in cat3}).encode()), 'catalog_sha256_equal': cap3['catalog_sha256'] == L.sha(L.dump({k: True for k in cat3}).encode())}}

# ---- (1) my 7 classes, defined in r1 -------------------------------------------------------------------------------------------------
CLASSES = {'H1_H2_H3_in_name': re.compile(r'(^|_)H[123](_|$)'), 'discharge': re.compile(r'discharg', re.I), 'aggregate_all': re.compile(r'^all_'), 'verified_suffix': re.compile(r'verified$', re.I),
           'QG_headline_qgc_qgf_qgp': re.compile(r'^qg[cfp]_'), 'passage_gpc_gpf_gpi': re.compile(r'^gp[cfi]_'), 'conditional': re.compile(r'conditional', re.I)}
ESS_R1 = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
cat_r1_rule = [k for k in true_src if not ESS_R1.search(k)]   # the r1 catalogue (reproduces 9,953)
union52 = [k for k in cat_r1_rule if any(r.search(k) for r in CLASSES.values())]
out['r1_catalogue_reproduced'] = {'n': len(cat_r1_rule), 'equals_catalogued_true_r1_from_capsule': set(cat_r1_rule) == set(cat1)}
still_only_catalogue = [k for k in union52 if k not in lit3_true]
out['seven_classes'] = {'union_in_r1': len(union52), 'per_class_r1': {n: len([k for k in cat_r1_rule if r.search(k)]) for n, r in CLASSES.items()},
                        'still_catalogue_only_in_r3': len(still_only_catalogue), 'still_catalogue_only_names': still_only_catalogue,
                        'now_literal': len(union52) - len(still_only_catalogue)}
# classes applied to the r3 catalogue itself (independent of the r1 list)
out['seven_classes']['r3_catalogue_matching_classes'] = {n: [k for k in cat3 if r.search(k)] for n, r in CLASSES.items()}
out['seven_classes']['r3_catalogue_matching_any'] = sorted({k for k in cat3 if any(r.search(k) for r in CLASSES.values())})
# the focus flags of r1 (hypothesis discharge pairs, aggregates, headline)
focus = ['all_verified', 'all_unconditional_targets_verified', 'all_conditional_implications_verified', 'formal_release_ready', 'specific_AQFT_witness_constructed',
         'gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced', 'gpf_H1_internal_susy_relative_gap_discharged',
         'qgc_concrete_emergent_einstein_proved', 'qgp_massless_spin2_proved', 'qgf_unconditional_continuous_corner_proved']
out['focus_flags'] = {k: {'value': kf[k], 'literal_in_r3_capsule': (k in lit3_true or k in lit3_false)} for k in focus}

# ---- (2) FALSE flags and their TRUE counterparts --------------------------------------------------------------------------------------
GENERIC = {'ext', 'red', 'kernel', 'proved', 'checked', 'the', 'of', 'is', 'and', 'a', 'in', 'to', 'on', 'by', 'as', 'at', 'for', 'with', 'no', 'not', 'from', 'it', 'its', 'are', 'be', 'does', 'two', 'one'}


def toks(name):
    s = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    return {t.lower() for t in re.split(r'[_\W]+', s) if t and not t.isdigit() and t.lower() not in GENERIC and len(t) > 1}


pairs = {}
for f in false_src:
    tf = toks(f)
    stem = re.sub(r'^(gpf|gpc|gpi)_', '', f)
    siblings = [k for k in true_src if k != f and (re.sub(r'^(gpf|gpc|gpi)_', '', k) == stem or stem in k)]
    overlap = sorted(((len(tf & toks(k)), k) for k in true_src if k != f and len(tf & toks(k)) >= 3), reverse=True)[:10]
    pairs[f] = {'literal_false': f in lit3_false, 'same_stem_true_siblings': siblings, 'siblings_literal': {k: (k in lit3_true) for k in siblings},
                'true_flags_sharing_3plus_tokens': [(n, k, k in lit3_true) for n, k in overlap], 'catalogued_among_them': [k for n, k in overlap if k not in lit3_true]}
out['false_flags'] = pairs

# ---- (3) the reading, clause by clause ------------------------------------------------------------------------------------------------
FAM = re.compile(r'^(?:ext|red)_')
clauseA = [k for k in cat3 if not FAM.match(k)]
out['clause_A_catalogue_only_ext_or_red'] = {'catalogued_not_in_families': clauseA[:10], 'n_violations': len(clauseA), 'catalogued_by_family': dict(collections.Counter(k.split('_')[0] for k in cat3))}
outside = [k for k in true_src if not FAM.match(k)]
clauseB = [k for k in outside if k not in lit3_true]
out['clause_B_every_TRUE_outside_the_families_is_literal'] = {'true_outside_families': len(outside), 'not_literal': clauseB[:10], 'n_violations': len(clauseB)}
out['clause_E_every_FALSE_literal'] = {'false_total': len(false_src), 'literal': len(lit3_false), 'n_violations': len([k for k in false_src if k not in lit3_false])}
# vocabulary of the "dentro delas, tambem as que trazem no nome ..." clause: written by me from the reading text, NOT from KEEP_FLAG
VOCAB = {'enunciado': re.compile(r'enunciad|statement', re.I), 'hipotese': re.compile(r'hip[oó]tes|hypothes|assumption|premis', re.I), 'H1_H2_H3_anywhere_in_name': re.compile(r'H[123]'),
         'H1_H2_H3_any_case': re.compile(r'h[123]', re.I), 'formula': re.compile(r'f[oó]rmul|formula|equation|equa[cç]', re.I), 'veredito': re.compile(r'veredit|verdict', re.I),
         'descarga': re.compile(r'descarg|discharg', re.I), 'condicao': re.compile(r'condi[cç]|condition', re.I), 'verificacao': re.compile(r'verific|verif', re.I)}
vc = {n: [k for k in cat3 if r.search(k)] for n, r in VOCAB.items()}
out['clause_C_inside_families_names_carrying_the_vocabulary_are_literal'] = {n: {'catalogued_matches': len(v), 'names': v[:25]} for n, v in vc.items()}
out['clause_C_violations_strict_vocabulary'] = sorted({k for n, v in vc.items() if n != 'H1_H2_H3_any_case' for k in v})
# of the ext_/red_ TRUE flags that match the vocabulary, how many are literal (to show the clause does bite)
fam_true = [k for k in true_src if FAM.match(k)]
out['family_true'] = {'n': len(fam_true), 'literal_n': len([k for k in fam_true if k in lit3_true]), 'catalogued_n': len([k for k in fam_true if k not in lit3_true])}
out['family_true_vocab_literal'] = {n: len([k for k in fam_true if r.search(k) and k in lit3_true]) for n, r in VOCAB.items()}
# literal TRUE flags inside the families: why are they literal (which codec-visible word)?
out['family_literal_examples'] = [k for k in fam_true if k in lit3_true][:12]
print(json.dumps(out, ensure_ascii=False, indent=1))
