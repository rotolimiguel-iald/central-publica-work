"""Reviewer Q5/Q7: the NEW text outside the topic blocks (header, protocols, mother, operational core + v405 addendum, formal state, source index) versus the installed v404 one.
Prints the lines that changed, truncated, and the added operational-core section in full. Read-only."""
import difflib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
R = Path(r'C:\IALD\projetos_pyhton\IALD')


def nucleus(text, first_topic):
    i = text.index('\n### ' + first_topic + '\n')
    return text[:i]


m = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
core_new = json.loads((Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405') / 'um_absoluto.json').read_bytes())['core']
first = next(iter(core_new))
pairs = {'haiku_expanded': ('haiku55', W / 'app/packages/haiku_expanded/prefix.md'), 'shared': ('haiku', W / 'app/packages/shared/prefix.md')}
out = {}
for pkg, (inst, newp) in pairs.items():
    to = (R / '.iald_runtime' / inst / 'prefix.md').read_text('utf-8')
    tn = newp.read_text('utf-8')
    # first topic block differs by package; use the first topic heading present in both
    nuc_o = to[:to.index('\n### ' + first + '\n')] if ('\n### ' + first + '\n') in to else None
    nuc_n = tn[:tn.index('\n### ' + first + '\n')] if ('\n### ' + first + '\n') in tn else None
    lo, ln = nuc_o.split('\n'), nuc_n.split('\n')
    sm = difflib.SequenceMatcher(None, lo, ln, autojunk=False)
    changes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        changes.append({'op': tag, 'old_lines': [i1, i2], 'new_lines': [j1, j2], 'old': [x[:260] for x in lo[i1:i2]][:4], 'new': [x[:260] for x in ln[j1:j2]][:4], 'old_chars': sum(len(x) for x in lo[i1:i2]), 'new_chars': sum(len(x) for x in ln[j1:j2])})
    out[pkg] = {'nucleus_chars_old': len(nuc_o), 'nucleus_chars_new': len(nuc_n), 'n_changes': len(changes), 'changes': changes}
print(json.dumps(out, ensure_ascii=False, indent=1)[:14000])
