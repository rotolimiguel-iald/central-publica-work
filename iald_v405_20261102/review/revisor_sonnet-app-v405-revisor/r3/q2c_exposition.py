"""Reviewer Q2 extra: the EXPOSICAO_CANONICA block of the haiku packages vs the sealed canonical form (um_absoluto_forma_canonica.md).
Claim to test: the exposition equals the sealed canonical except (1) the typed boolean audit-ladder rows '- `name` = `True|False`' (retrievable) and (2) one inserted notice. Own code (no codec import).
Also: do removed rows include any False row? And is the removed-row count the one stated in the notice?"""
import hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
C = (V / 'um_absoluto_forma_canonica.md').read_bytes().decode('utf-8-sig')
out = {'canonical_sha256': hashlib.sha256((V / 'um_absoluto_forma_canonica.md').read_bytes()).hexdigest(), 'canonical_chars': len(C)}
rows = list(re.finditer(r'(?m)^- `[^`\r\n]+` = `(?:True|False)`\r?$', C))
starts = list(re.finditer(r'(?m)^\*\*Escada auditada \(', C))
out['audit_rows_in_canonical_total'] = len(rows)
out['ladder_headings'] = len(starts)
if starts:
    s = starts[0].start()
    e = C.find('\n**', s + 2)
    sel = [r for r in rows if s <= r.start() < e]
    out['rows_in_ladder_section'] = len(sel)
    out['rows_true'] = sum(1 for r in sel if r.group().rstrip('\r').endswith('`True`'))
    out['rows_false'] = sum(1 for r in sel if r.group().rstrip('\r').endswith('`False`'))
    out['rows_outside_ladder_section'] = len(rows) - len(sel)
    C2 = C
    for r in reversed(sel):
        C2 = C2[:r.start()] + C2[r.end():]
    for pkg in ('haiku_expanded', 'haiku55'):
        t = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
        P = L.parse_prefix(t)
        E = P['E']
        m = re.search(r'\nIndicadores individuais de auditoria disponíveis em um_forma_canonica_integral, offset=(\d+), via fetch_tgl/next_offset\. (\d+) registros documentais, não contagem nova de provas\.\n', E)
        rec = {'notice_found': bool(m)}
        if m:
            rec['notice_offset_in_text'] = int(m.group(1))
            rec['notice_count_in_text'] = int(m.group(2))
            rec['notice_offset_equals_first_removed_row_offset'] = int(m.group(1)) == sel[0].start()
            rec['notice_count_equals_removed_rows'] = int(m.group(2)) == len(sel)
            E2 = E[:m.start()] + E[m.end() - 1:]  # drop the inserted notice (it began with a newline and ended with a newline that belongs to it)
            # the codec inserts '\n' + text + '\n' before the ladder heading; remove exactly that
            rec['exposition_minus_notice_equals_canonical_minus_rows'] = (E2 == C2) or (E.replace(m.group(0), '', 1) == C2) or (E.replace(m.group(0), '\n', 1) == C2)
            rec['exposition_chars'] = len(E)
            rec['canonical_minus_rows_chars'] = len(C2)
        out[pkg] = rec
print(json.dumps(out, ensure_ascii=False, indent=1))
