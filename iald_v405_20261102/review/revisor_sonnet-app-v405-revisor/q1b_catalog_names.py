"""Reviewer Q1: which TRUE booleans of kernel_formalization leave the haiku package (9,953) -- classification by name against a BROADER keyword set
than the codec's own regex, to look for hypothesis / statement / formula / verdict flags that the codec's regex failed to keep literal."""
import json, re, collections, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
kf = core['kernel_formalization']
CODEC_ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
CODEC_WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
# independent, broader list (my own): anything that smells like a hypothesis / statement / formula / verdict / status / open-item / discharge flag
BROAD = re.compile(r'hyp|hip|assum|premis|postul|conject|statement|enunc|formul|equat|equa|verdict|veredit|claim|status|estatut|scope|escop|theor|teorem|lemma|corol|defin|axiom|discharg|open|aberto|conditional|condicion|not_|no_|never|nunca|unconditional|incondicion|H1|H2|H3|\bh[123]_|_h[123]_|law|lei_|identity|identidade|truth|verdade', re.I)
true_all = [k for k, v in kf.items() if v is True]
false_all = [k for k, v in kf.items() if v is False]
lit_true = [k for k in true_all if CODEC_ESS.search(k)]  # what stays literal by the codec rule (WHOLE_FIELD is a subset of ESSENTIAL)
cat_true = [k for k in true_all if not CODEC_ESS.search(k)]
print('source TRUE', len(true_all), 'FALSE', len(false_all))
print('literal-by-regex TRUE', len(lit_true), '| catalogued TRUE', len(cat_true))
print('FALSE flags (all stay literal):', false_all)
# prefix distribution of catalogued names
pref = collections.Counter(re.sub(r'(_[0-9]+)+$', '', k).split('_')[0] + '_' + (k.split('_')[1] if '_' in k else '') for k in cat_true)
print('top prefixes among catalogued:', pref.most_common(25))
suffix = collections.Counter(k.rsplit('_', 2)[-2] + '_' + k.rsplit('_', 1)[-1] if k.count('_') >= 2 else k for k in cat_true)
print('top suffix pairs among catalogued:', suffix.most_common(15))
# broad keyword hits among catalogued names
hits = [k for k in cat_true if BROAD.search(k)]
print('catalogued TRUE names matching my BROAD list:', len(hits))
byrx = collections.Counter()
for k in hits:
    for m in set(x.lower() for x in BROAD.findall(k)):
        byrx[m] += 1
print('by keyword:', byrx.most_common(30))
# show a sample for the semantically heavier keywords
for kw in ('discharg', 'hyp', 'open', 'conditional', 'unconditional', 'not_', 'verdict', 'status', 'axiom', 'law', 'H3'):
    s = [k for k in hits if re.search(kw, k, re.I)]
    print('  %-14s %5d  e.g. %s' % (kw, len(s), s[:6]))
# names that look like 'open' / 'not proved' statements but are TRUE (i.e., TRUE means the NEGATIVE statement holds)
neg = [k for k in cat_true if re.search(r'(^|_)(not|no|never|without|absent|unconditional_.*false|open)(_|$)', k, re.I)]
print('catalogued TRUE names containing not/no/never/without/absent/open:', len(neg), neg[:15])
# the 4 FALSE and the literal TRUE sample
print('literal TRUE sample:', lit_true[:5], '...', lit_true[-5:])
json.dump({'catalogued_true_count': len(cat_true), 'catalogued_names_sha256': L.sha(L.dump({k: True for k in cat_true}).encode()), 'broad_hits': hits[:400]}, open(Path(__file__).parent / 'q1b_out.json', 'w', encoding='utf8'), ensure_ascii=False)
