# -*- coding: utf-8 -*-
"""Reviewer r3 Q2 extras for haiku_expanded: (1) independent rebuild from the base haiku55 (no codec import); (2) the 18 _v404/_v405 topics fully inline;
(3) expansion selection == FINAL_PREPARATION.expanded_topics; (4) the r3 capsule differs from the r1 capsule ONLY in kernel_formalization (every other topic block decodes identically);
(5) file/byte pins of the haiku packages (file sha != text sha because of the CR inside the bootstrap chunk). Read-only."""
import ast, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
sha = lambda b: hashlib.sha256(b).hexdigest()
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
out = {}
# (1) independent rebuild
base = (W / 'app/packages/haiku55/prefix.md').read_text('utf-8')
rx = re.compile('lagrang|hamilton|lindblad|dephas|bootstrap|breuer|horizon|master|three_locks|continuous_modular_zero|light_eigen|the_imported|price_of_the_gravity')
sel = [n for n in core if n.endswith(('_v404', '_v405')) or rx.search(n)]
exp = base
for n in sel:
    pat = r'(?m)^### ' + re.escape(n) + r'\nFonte: [^\n]+\n[^\n]+(?=\n)'
    exp, k = re.subn(pat, lambda _: '### ' + n + '\nFonte: resultado_publicado_integral /core/' + n + '\n' + dump(core[n]), exp)
    assert k == 1, (n, k)
prog = (V / 'um.py').read_bytes()
lines = prog.decode('utf-8-sig').splitlines(keepends=True)
node = next(x for x in ast.parse(prog).body if isinstance(x, ast.FunctionDef) and x.name == 'prove_the_bootstrap')
chunk = ''.join(lines[node.lineno - 1:node.end_lineno])
exp += '\n<BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n' + dump({'source_sha256': sha(prog), 'symbol': node.name, 'lines': [node.lineno, node.end_lineno], 'chunk_sha256': sha(chunk.encode()), 'statute': 'SOURCE_DEFINITION_NOT_NEW_EXECUTION'}) + '\n```python\n' + chunk + '```\n</BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'
built = (W / 'app/packages/haiku_expanded/prefix.md').read_bytes()
out['rebuild_from_base_equals_built_bytes'] = exp.encode() == built
out['bytes'] = {'haiku_expanded_file_sha256': sha(built), 'haiku_expanded_bytes': len(built), 'haiku55_base_file_sha256': sha((W / 'app/packages/haiku55/prefix.md').read_bytes())}
# (2)+(3)
fp = json.loads((W / 'app/packages/haiku_expanded/FINAL_PREPARATION.json').read_bytes())
out['selection_equals_FINAL_PREPARATION'] = set(sel) == set(fp['expanded_topics'])
out['expanded_topics'] = len(fp['expanded_topics'])
P3 = L.parse_prefix((W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8'))
full = {}
for n in core:
    if n.endswith(('_v404', '_v405')):
        k, dv = L.decode_block(P3, n)
        lv = L.literal_leaves(dv, '/core/' + n)
        tot = sum(1 for _ in L.leaves(core[n], '/core/' + n))
        refs = json.dumps(L.canon(dv)).count('"@"')
        full[n] = (len(lv) == tot and refs == 0)
out['v404_v405_topics_full_inline'] = {'n': len(full), 'all_full': all(full.values()), 'not_full': [n for n, v in full.items() if not v]}
# (4) r3 vs r1 capsule: only kernel_formalization differs (decoded)
P1 = L.parse_prefix((W / 'superseded_r1/app/packages/haiku_expanded/prefix.md').read_text('utf-8'))
diff_topics = []
for n in core:
    k3, d3 = L.decode_block(P3, n)
    k1, d1 = L.decode_block(P1, n)
    if k3 != k1 or L.canon(d3) != L.canon(d1):
        diff_topics.append(n)
out['topics_whose_decoded_block_differs_r3_vs_r1'] = diff_topics
# the exposition and the nucleus
out['exposition_equals_sealed_canonical'] = P3['E'] == (V / 'um_absoluto_forma_canonica.md').read_bytes().decode('utf-8-sig')
print(json.dumps(out, ensure_ascii=False, indent=1))
