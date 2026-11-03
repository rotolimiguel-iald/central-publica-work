# -*- coding: utf-8 -*-
"""Reviewer r3 Q7/Q8 over the NEW text only: everything that differs between the r1 and the r3 haiku packages (haiku_expanded and the haiku55 base).
Method: (1) raw line diff r1 vs r3; (2) decoded-block diff (which topics differ; for kernel_formalization, the keys added/changed); (3) scan the new text for beta literals,
CONFIRMED/confirmada wording, the superseded phrase '15 calculadas e 3 literais', confidential names, Escritorio paths, secret patterns, the private atlas block. Read-only."""
import difflib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
BETA = re.compile(r'0[.,]0120313|0[.,]01203\b|1[.,]20313\s*[x×·*]\s*10|1[.,]2031e-?0?2|β\s*=|beta\s*=', re.I)
CONF = re.compile(r'confirmed|confirmad|confirm(?:a|e)\w*|CONFIRMED', re.I)
OLD = re.compile(r'15[\s\W_]{1,12}(?:as[\s\W_]{1,12})?(?:calculad\w*|computad\w*|computed|calculated)[\s\W_]{1,12}(?:e|and|plus|\+|mais|com)?[\s\W_]{1,12}3[\s\W_]{1,12}(?:as[\s\W_]{1,12})?liter\w*', re.I)
CONFNAMES = re.compile(r'iald_stack_v7|iald_psion_state|\.env\b|auth\.json|\.credentials\.json|\.iald_keys|\.tgl_site|\.iald_privado|Escritorio|ATLAS_CANONICO', re.I)
SEC = [re.compile(p) for p in (r'sk-ant-[A-Za-z0-9_\-]{20,}', r'\bsk-[A-Za-z0-9]{32,}', r'AKIA[0-9A-Z]{16}', r'ghp_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}', r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
                               r'(?i)"(?:api_key|apikey|secret|password|passwd|authorization|access_token|refresh_token)"\s*:\s*"[^"\s]{8,}"', r'eyJ[A-Za-z0-9_\-]{20,}\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}')]
QUAL = re.compile(r'not[_ ]|nunca|never|n[aã]o|NOT|creditaç|creditation|recus|proibid|forbidden|≠|!=|\bsem\b|without|nenhum|no ', re.I)
AUD = 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE'
out = {}


def scan(text):
    return {'beta_literal_matches': [m.group(0) for m in BETA.finditer(text)], 'confirm_matches': [(m.group(0), bool(QUAL.search(text[max(0, m.start() - 70):m.end() + 70]))) for m in CONF.finditer(text)],
            'superseded_phrase': len(OLD.findall(text)), 'confidential_names': sorted(set(x.lower() for x in CONFNAMES.findall(text))), 'secret_patterns': sum(len(rx.findall(text)) for rx in SEC)}


for pkg in ('haiku_expanded', 'haiku55'):
    t3 = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
    t1 = (W / 'superseded_r1/app/packages' / pkg / 'prefix.md').read_text('utf-8')
    l1, l3 = t1.split('\n'), t3.split('\n')
    sm = difflib.SequenceMatcher(None, l1, l3, autojunk=False)
    changed_new, changed_old = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != 'equal':
            changed_old += l1[i1:i2]
            changed_new += l3[j1:j2]
    rec = {'lines_r1': len(l1), 'lines_r3': len(l3), 'changed_lines_r3': [(len(x), x[:90]) for x in changed_new], 'changed_lines_r1': [(len(x), x[:90]) for x in changed_old]}
    # decoded-block diff
    P1, P3 = L.parse_prefix(t1), L.parse_prefix(t3)
    differing = [n for n in P3['body'] if n not in P1['body'] or L.decode_block(P1, n)[0] != L.decode_block(P3, n)[0] or L.canon(L.decode_block(P1, n)[1]) != L.canon(L.decode_block(P3, n)[1])]
    rec['topics_whose_decoded_block_differs'] = differing
    rec['dictionary_equal'] = P1['D'] == P3['D']
    rec['exposition_equal'] = P1['E'] == P3['E']
    k1, d1 = L.decode_block(P1, 'kernel_formalization')
    k3, d3 = L.decode_block(P3, 'kernel_formalization')
    added = [k for k in d3 if k not in d1 and k != AUD]
    removed_from_literal = [k for k in d1 if k not in d3 and k != AUD]
    changed_vals = [k for k in d1 if k in d3 and k != AUD and L.canon(d1[k]) != L.canon(d3[k])]
    rec['kernel_formalization_delta'] = {'literal_keys_added_r3': len(added), 'added_sample': added[:6], 'all_added_values_True': all(d3[k] is True for k in added), 'literal_keys_removed_r3': len(removed_from_literal), 'changed_values': changed_vals,
                                         'aud_r1': d1[AUD], 'aud_r3': d3[AUD]}
    # NEW text = header lines + the AUD object + the added flag names (their values are sealed booleans)
    new_text = '\n'.join(changed_new)
    # the capsule line itself is large; scan only the new parts of it
    capsule_new_parts = json.dumps(d3[AUD], ensure_ascii=False) + '\n' + '\n'.join(added)
    header_new = [x for x in changed_new if len(x) < 5000]
    rec['scan_header_and_small_changed_lines'] = scan('\n'.join(header_new))
    rec['scan_capsule_new_parts_(AUD_object_+_added_flag_names)'] = scan(capsule_new_parts)
    rec['header_sentence_r3'] = [x for x in changed_new if 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE' in x and len(x) < 5000]
    out[pkg] = rec
print(json.dumps(out, ensure_ascii=False, indent=1)[:16000])
