"""Independent numerical gate for ADENDO C, before starting any render."""
from pathlib import Path
import hashlib, json, math, os, re
from finalizer_guards import validate_frozen_data

C = Path(__file__).resolve().parent
B = C / 'baseline_v400'
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'

def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def numeric_diff(a, b, path=''):
    if type(a) != type(b): return [(path, a, b)]
    if isinstance(a, dict):
        out = []
        for k in sorted(a.keys() | b.keys()):
            out += numeric_diff(a[k], b[k], path + '/' + k) if k in a and k in b else [(path + '/' + k, 'KEY_PRESENCE', 'CHANGED')]
        return out
    if isinstance(a, list):
        return [(path + '/length', len(a), len(b))] if len(a) != len(b) else [d for i, (x, y) in enumerate(zip(a, b)) for d in numeric_diff(x, y, path + '/' + str(i))]
    return [(path, a, b)] if isinstance(a, (int, float, bool)) and a != b else []

def main():
    assert (C / 'DATA_READY.json').exists(), 'Wait for integrated data readiness.'
    validate_frozen_data(C, V, N, require_parent=False)
    old, new = read(B / 'data/hud.json'), read(V / 'data/hud.json')
    seal = read(N / 'um_absoluto_selo.json')
    assert old['seal_version'] == 'v400' and new['seal_version'] == seal['um_version'] == 'v401'
    assert new['seal_pin'] == seal['sha256']['um.py'] == sha(V / 'source/um.py')
    for name in ['um_absoluto.json', 'tgl_kernel_proof_manifest.json']:
        assert sha(V / 'source' / name) == seal['sha256'][name]
    record = read(V / 'source/um_absoluto.json')['core']['estatuto_da_prova_v391']['prova_1_kernel']
    kernel = read(V / 'source/tgl_kernel_proof_manifest.json')
    expected = {'proof_ladder_clean': record['n_theorems_clean'], 'proof_ladder_total': record['n_theorems_expected'], 'formal_count': len(kernel['formal_files_sha256']), 'declaration_count': len(kernel['axiom_report'])}
    aliases = {'theorems': 'proof_ladder_clean', 'n_formal': 'formal_count'}
    permitted = set(expected) | set(aliases)
    for item in new['items']:
        if item['id'] in permitted:
            assert item['value'] == expected[aliases.get(item['id'], item['id'])]
    for key, value in expected.items(): assert new['extra'][key] == value
    old_items = {i['id']: i for i in old['items']}
    count_pairs = {(old_items[k]['value'], value) for k, value in expected.items()}
    rows, unexpected = [], []
    files = ['hud.json', 'frames.json', 'scene.json', 'PROVENANCE_PUBLIC.json', 'STDOUT_LINES.json']
    for name in files:
        a, b = read(B / 'data' / name), read(V / 'data' / name)
        diffs = numeric_diff(a, b)
        for path, before, after in diffs:
            allowed = False
            if name == 'hud.json':
                if path.startswith('/extra/') and path.rsplit('/', 1)[1] in expected: allowed = (before, after) in count_pairs
                m = re.fullmatch(r'/items/(\d+)/value', path)
                if m: allowed = b['items'][int(m[1])]['id'] in permitted and (before, after) in count_pairs
                if re.fullmatch(r'/stdout_lines/\d+/line', path): allowed = True
            elif name == 'PROVENANCE_PUBLIC.json':
                m = re.fullmatch(r'/anchors/(\d+)/(?:json_value|live_value)', path)
                if m:
                    anchor = b['anchors'][int(m[1])]
                    description = json.dumps(anchor, ensure_ascii=False)
                    allowed = (before, after) in count_pairs and any(k in description for k in ['n_theorems_', 'formal_files_sha256', 'declaracoes_auditadas', 'axiom_report'])
                if path in ['/kernel/axiom_report_entries', '/kernel/formal_files', '/kernel/theorems_clean', '/kernel/theorems_total']: allowed = (before, after) in count_pairs
                if re.fullmatch(r'/source_code_sections/[^/]+/(start|end)', path): allowed = True
                if re.fullmatch(r'/sources/[^/]+/bytes', path): allowed = True
                if path in ['/sources/rodada_v400_stdout.txt', '/sources/rodada_v401_stdout.txt']: allowed = True
            elif name == 'STDOUT_LINES.json' and re.fullmatch(r'/lines/\d+/line', path): allowed = True
            if not allowed: unexpected.append({'file': name, 'path': path, 'before': before, 'after': after})
        rows.append({'file': name, 'baseline_sha256': sha(B / 'data' / name), 'current_sha256': sha(V / 'data' / name), 'numeric_differences': diffs})
    assert not unexpected, unexpected
    stdout = (V / 'source/rodada_v401_stdout.txt').read_text(encoding='utf-8').splitlines()
    for line in new['stdout_lines']: assert stdout[line['line'] - 1] == line['text']
    prov = read(V / 'PROVENANCE_PUBLIC.json')
    assert prov['anchors_all_ok'] and len(prov['anchors']) >= 64
    for anchor in prov['anchors']:
        assert anchor['ok'] and math.isfinite(anchor['residual']) and abs(anchor['json_value'] - anchor['live_value']) <= anchor['tol']
    report = {'status': 'PASS_WITH_SCOPE', 'source': 'v401', 'source_sha256': new['seal_pin'], 'actor': 'codex-video-v7', 'method': 'Independent full-key numeric/boolean comparison of five data documents, preserving list lengths/types; only source coordinates/byte counts and authorized kernel counts admitted. Full textual comparison is separately covered by the data builder receipt.', 'expected_counts_read_from_sealed_sources': expected, 'files': rows, 'unexpected_differences': unexpected, 'anchors': len(prov['anchors']), 'anchors_all_ok': True, 'stdout_lines_verified': len(new['stdout_lines']), 'data_ready_sha256': sha(C / 'DATA_READY.json'), 'limitations': ['No new Lean compilation or empirical test.', 'Source line coordinates are provenance, not changed physical quantities.']}
    p = C / 'PARENT_NUMERIC_REVIEW.json'
    assert not p.exists()
    raw = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    temp = p.with_suffix('.tmp'); temp.write_bytes(raw); assert temp.read_bytes() == raw; os.replace(temp, p)
    print(json.dumps({'status': report['status'], 'anchors': len(prov['anchors']), 'counts': expected}))

if __name__ == '__main__': main()
