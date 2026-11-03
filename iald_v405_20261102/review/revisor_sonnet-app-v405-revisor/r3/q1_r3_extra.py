# -*- coding: utf-8 -*-
"""r3 extra: (1) why the 386 TRUE flags inside the ext_/red_ families are literal beyond the reading's listed vocabulary; (2) the 81 TRUE flags outside the families by group;
(3) 'por declaracao': do the catalogued ext_/red_ flags correspond to per-theorem entries of the source ladder? Read-only."""
import json, re, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102'); V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']; kf = core['kernel_formalization']
P3 = L.parse_prefix((W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8')); k, dv = L.decode_block(P3, 'kernel_formalization')
lit = {x for x, v in dv.items() if v is True}
FAM = re.compile(r'^(?:ext|red)_')
fam_true = [x for x, v in kf.items() if v is True and FAM.match(x)]
fam_lit = [x for x in fam_true if x in lit]
VOCAB = re.compile(r'enunciad|statement|hip[oó]tes|hypothes|assumption|premis|H[123]|f[oó]rmul|formula|equation|equa[cç]|veredit|verdict|descarg|discharg|condi[cç]|condition|verific|verif', re.I)
EXTRA = {'theorem': re.compile(r'theorem|teorema', re.I), 'commut': re.compile(r'commut|comuta', re.I), 'lagrang': re.compile(r'lagrang', re.I), 'hamilton': re.compile(r'hamilton', re.I), 'lindblad': re.compile(r'lindblad', re.I),
         'dephas': re.compile(r'dephas', re.I), 'status': re.compile(r'status|estatuto', re.I), 'scope': re.compile(r'scope|escopo', re.I), 'claim': re.compile(r'claim', re.I)}
not_in_vocab = [x for x in fam_lit if not VOCAB.search(x)]
out = {'family_true': len(fam_true), 'family_literal': len(fam_lit), 'family_literal_matching_reading_vocabulary': len(fam_lit) - len(not_in_vocab), 'family_literal_not_in_reading_vocabulary': len(not_in_vocab),
       'those_by_extra_word': {n: len([x for x in not_in_vocab if r.search(x)]) for n, r in EXTRA.items()}, 'those_with_no_known_word': [x for x in not_in_vocab if not any(r.search(x) for r in EXTRA.values())][:10]}
outside = [x for x, v in kf.items() if v is True and not FAM.match(x)]
grp = collections.Counter()
for x in outside:
    if x.startswith('all_'): grp['all_* (agregados)'] += 1
    elif re.match(r'(gp[cfi]|qg[cfp])_', x): grp['gp*/qg* (portoes)'] += 1
    elif re.search(r'build|lake|toolchain|audit|capture|sorry|trust|forbidden|sentinel|axioms_absent|release', x, re.I): grp['build/auditoria'] += 1
    else: grp['outras (pedras fundacionais e demais)'] += 1
out['outside_true_by_group'] = dict(grp)
out['outside_true_total'] = len(outside)
out['outside_true_other_sample'] = [x for x in outside if not (x.startswith('all_') or re.match(r'(gp[cfi]|qg[cfp])_', x) or re.search(r'build|lake|toolchain|audit|capture|sorry|trust|forbidden|sentinel|axioms_absent|release', x, re.I))][:12]
# per declaration: catalogued ext_ names present as keys of the source per-theorem ladder?
pt = core['external_ladder']['per_theorem']
cat = [x for x, v in kf.items() if v is True and x not in lit]
cat_ext = [x for x in cat if x.startswith('ext_')]
cat_red = [x for x in cat if x.startswith('red_')]
out['per_declaration'] = {'catalogued_ext': len(cat_ext), 'ext_in_external_ladder_per_theorem': len([x for x in cat_ext if x in pt]), 'catalogued_red': len(cat_red), 'red_in_external_ladder_per_theorem': len([x for x in cat_red if x in pt]),
                          'per_theorem_total': len(pt), 'per_theorem_all_true': all(v is True for v in pt.values())}
# red_ flags: do they appear as declarations in the axiom report (suffix after red_)?
ar = kf['axiom_report']
def decl_hit(name):
    stem = re.sub(r'^(ext|red)_', '', name)
    stem = re.sub(r'_(kernel_proved|kernel_checked)$', '', stem)
    return any(k.endswith('.' + stem) or k.endswith('.red_' + stem) or ('.' + stem + '.' in k) for k in ar)
out['per_declaration']['sample_ext_with_axiom_report_declaration'] = sum(1 for x in cat_ext[:300] if decl_hit(x))
out['per_declaration']['sample_ext_n'] = len(cat_ext[:300])
out['per_declaration']['sample_red_with_axiom_report_declaration'] = sum(1 for x in cat_red if decl_hit(x))
out['per_declaration']['sample_red_n'] = len(cat_red)
print(json.dumps(out, ensure_ascii=False, indent=1))
