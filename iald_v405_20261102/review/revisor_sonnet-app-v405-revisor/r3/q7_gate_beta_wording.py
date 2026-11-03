"""Reviewer Q7b/c/d: (b) gate state in the prefixes vs the seal; (c) beta literal outside sealed content; (d) CONFIRMED/confirmada wording in NEW text (nucleus delta + windows not present in the previous prefix).
Decoded text = raw prefix with dictionary/enum/literal references expanded (own decoder). Read-only."""
import json, re, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
V5 = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
seal = json.loads((V5 / 'um_absoluto_selo.json').read_bytes())
core_new = json.loads((V5 / 'um_absoluto.json').read_bytes())
sealed_blob = (V5 / 'um_absoluto.json').read_text('utf-8-sig') + (V5 / 'um_absoluto_forma_canonica.md').read_text('utf-8-sig') + (V5 / 'um_absoluto_pt.txt').read_text('utf-8-sig') + (V5 / 'um_absoluto_selo.json').read_text('utf-8-sig')
GATE_RX = re.compile(r'TGL_QG_[A-Z0-9_]*(?:CLOSED|ARCHITECTURE|COMPLETED)[A-Z0-9_]*')
gate_seal = seal.get('qg_closure_verdict')
out = {'seal_qg_closure_verdict': gate_seal, 'seal_keys_with_verdict': [k for k in seal if 'verdict' in k.lower()][:10]}
BETA = re.compile(r'0[.,]0120313|0[.,]01203\b|1[.,]20313\s*[x×·*]\s*10\^?\{?-2|1[.,]2031e-?0?2', re.I)
CONF = re.compile(r'confirmed|confirmada|confirmado|confirmadas|confirmados|CONFIRMED|confirm(?:a|e)\w*', re.I)
QUAL = re.compile(r'not[_ ]|nunca|never|n[aã]o|NOT|creditaç|creditation|recus|proibid|forbidden|≠|!=|\bsem\b|without|nenhum|no ', re.I)


def decoded_text(pkg_text):
    P = L.parse_prefix(pkg_text)
    parts = [pkg_text.split('\n### ', 1)[0]]  # header + nucleus before first ### (raw; contains no encodings)
    for lid, val in P['D'].items():
        dv = L.dec_lit(val, P['D'], P['E'])
        parts.append(dv if isinstance(dv, str) else json.dumps(L.canon(dv), ensure_ascii=False))
    for n in P['body']:
        kind, dv = L.decode_block(P, n)
        parts.append(json.dumps(L.canon(dv), ensure_ascii=False) if kind == 'JSON' else dv)
    parts.append(P['E'])
    return '\n'.join(parts), P


prev = {'haiku_expanded': (R / '.iald_runtime/haiku55/prefix.md').read_text('utf-8'), 'shared': (R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'),
        'sonnet_public': (Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029') / 'app/packages/sonnet_public/prefix.md').read_text('utf-8')}
for pkg in ('haiku_expanded', 'shared', 'sonnet_public'):
    t = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
    dec, P = decoded_text(t)
    # (b) gate strings
    gates = collections.Counter(m.group(0) for m in GATE_RX.finditer(dec))
    gates_raw = collections.Counter(m.group(0) for m in GATE_RX.finditer(t))
    rec = {'gate_strings_decoded': dict(gates), 'gate_strings_raw': dict(gates_raw), 'seal_gate_present_decoded': gate_seal in dec if gate_seal else None}
    # (c) beta literal: where do numeric beta literals occur, and are they in sealed content?
    nuc = t.split('\n### ', 1)[0]
    beta_nuc = [(m.start(), nuc[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')) for m in BETA.finditer(nuc)]
    beta_nuc_prev = len(list(BETA.finditer(prev[pkg].split('\n### ', 1)[0])))
    beta_all = [m.group(0) for m in BETA.finditer(dec)]
    not_in_sealed = sorted({m.group(0) for m in BETA.finditer(dec) if m.group(0) not in sealed_blob})
    rec['beta'] = {'matches_in_nucleus_new': len(beta_nuc), 'matches_in_nucleus_previous_prefix': beta_nuc_prev, 'nucleus_samples': beta_nuc[:4], 'matches_in_decoded_all': len(beta_all),
                   'distinct_forms': sorted(set(beta_all))[:8], 'forms_not_found_in_sealed_core/canonical/article/seal': not_in_sealed[:8]}
    # (d) confirmation wording: windows (+-70) not present in the previous prefix text
    prevt = prev[pkg]
    new_windows = []
    total = 0
    for m in CONF.finditer(dec):
        total += 1
        w = dec[max(0, m.start() - 70):m.end() + 70]
        if w not in prevt:
            new_windows.append((m.start(), w.replace('\n', ' ')))
    unq = [x for x in new_windows if not QUAL.search(x[1])]
    # restrict to NUCLEUS text (builder-authored): raw nucleus diff windows
    nuc_new = [(m.start(), nuc[max(0, m.start() - 70):m.end() + 70].replace('\n', ' ')) for m in CONF.finditer(nuc) if nuc[max(0, m.start() - 70):m.end() + 70] not in prevt]
    rec['confirm_wording'] = {'hits_in_decoded_total': total, 'windows_not_in_previous_prefix': len(new_windows), 'unqualified_new_windows': len(unq), 'unqualified_samples': unq[:8], 'builder_authored_nucleus_new_windows': nuc_new[:6]}
    out[pkg] = rec
print(json.dumps(out, ensure_ascii=False, indent=1)[:14000])
