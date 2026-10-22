"""Own read-only artifact inspection. Never executes author code or Lean."""
from pathlib import Path
from collections import Counter
import ast, datetime, hashlib, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
REV = Path(__file__).resolve().parent
ROOT = REV.parent
OUT = Path((REV / 'square_resolvent_integrated_latest_run.txt').read_text().strip())
OLD = REV / 'bidual_right_support_integrated_20260913_043432_221716'
DEV = REV / 'square_adjoint_final_independent_20260913_054955_334589'
sha = lambda b: hashlib.sha256(b).hexdigest()
hf = lambda p: sha(Path(p).read_bytes())
load = lambda p: json.loads(Path(p).read_bytes())

def write(p, b):
    assert p.resolve().is_relative_to(REV) and not p.exists(), str(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_name(p.name + '.tmp')
    with q.open('xb') as f:
        f.write(b)
    assert q.read_bytes() == b
    q.replace(p)

def save(p, v):
    write(p, (json.dumps(v, ensure_ascii=False, indent=2) + '\n').encode())

def embedded(raw):
    t = ast.parse(raw)
    ns = [n for n in t.body if isinstance(n, ast.Assign) and any(
        isinstance(x, ast.Name) and x.id == '_EMBEDDED_KERNEL_FILES' for x in n.targets)]
    assert len(ns) == 1
    d = ast.literal_eval(ns[0].value)
    ns[0].value = ast.Constant('EXCLUDED_EMBEDDED_LEAN')
    return d, ast.dump(t, include_attributes=False)

def axioms(text):
    d = {}
    for n, v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", text, re.S):
        a = sorted(x.strip() for x in v.split(',') if x.strip())
        assert n not in d or d[n] == a, n
        d[n] = a
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms", text):
        assert n not in d or not d[n], n
        d[n] = []
    return d

assert '--author-green-notice' in sys.argv, 'Run only after author final build/test notice'
S = load(OUT / 'static_verification.json')
S['future_custody_artifacts_absent'] = ['square_resolvent_custody.json', 'square_resolvent_custody_verification.json', 'RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_INTEGRADA.md']
BM = load(OUT / 'build_manifest.json')
P = load(OUT / 'bidual_right_support_custody.json')
D = load(OUT / 'square_resolvent_draft_status.json')
I = load(OUT / 'integration.json')
for f, h in S['artifact_pins'].items():
    assert hf(ROOT / f) == h, f
for f in ['integration.json', 'integrated_compile.json', 'gate_tests.json', 'kernel_incremental_evidence.json']:
    assert hf(OLD / f) == P['artifacts'][f], f
assert hf(S['parent_working_backup']) == P['working_sha256']
oldembed, oldast = embedded(Path(S['parent_working_backup']).read_bytes())
um = (ROOT / 'um.py').read_bytes()
cur, curast = embedded(um)
assert sha(um) == I['working_sha256'] == S['working_sha256']
assert curast == oldast and sha(curast.encode()) == S['python_AST_sha256']
assert len(cur) == I['embedded_files'] == 918
assert hf(ROOT / 'gate_extension.py') == P['artifacts']['gate_extension.py']

files = ['integrated_compile.json', 'gate_tests.json', 'kernel_incremental_evidence.json']
for f in files:
    write(OUT / f, (ROOT / f).read_bytes())
B, G, E = [load(OUT / f) for f in files]
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
assert G['working_um_sha256'] == I['working_sha256']
assert E['incremental_build_ok'] and E['dependency_hashes_verified'] and E['changed_source_hashes_verified']
assert not E['full_monolithic_runtime_run']

C = load(DEV / 'compilation.json')
assert hf(DEV / 'compilation.json') == S['own_DEV_compilation_sha256']
assert hf(REV / 'REVIEW_SQUARE_RESOLVENT_DEV.md') == S['own_DEV_review_sha256']
assert C['complete'] and all(v is True for v in C.values() if isinstance(v, bool))
ownax = {n: sorted(a) for n, a in C['records'][-1]['axioms'].items()}
assert ownax == D['targets'] and len(ownax) == 20
for n,m in S['transposition'].items():
    devraw = (ROOT / 'kernel/TGLV350' / (n + '.lean')).read_bytes()
    assert devraw == (DEV / 'sources/TGLV350' / (n + '.lean')).read_bytes()
    assert sha(devraw) == D['modules'][n]['source_sha256']
    assert hf(ROOT / 'build/TGLV350' / (n + '.olean')) == hf(m['own_DEV_binary']) == D['modules'][n]['binary_sha256']
    key = 'TGLExt/V350' + n + '.lean'
    assert re.sub(rb'^import TGLV350\.', b'import TGLExt.V350', devraw, flags=re.M) == cur[key].encode()

newkeys = {'TGLExt/V350' + n + '.lean' for n in S['transposition']}
roots = {'TGLExt.lean', 'TGL/Audit.lean'}
assert set(cur) - set(oldembed) == newkeys and not (set(oldembed) - set(cur))
assert {k for k in oldembed if oldembed[k] != cur[k]} == roots
oldrecords = {Path(r['source']).relative_to(ROOT / 'kernel').as_posix(): r
              for r in load(OLD / 'integrated_compile.json')['records']}
oldpins = {r['file']: r for r in load(OLD / 'verification.json')['records']}
rows, seen, maps = [], set(), {}
for r in B['records']:
    src = Path(r['source']).resolve()
    assert src.is_relative_to(ROOT / 'kernel')
    rel = src.relative_to(ROOT / 'kernel')
    key = rel.as_posix()
    assert key not in seen
    seen.add(key)
    bp = ROOT / 'build' / rel.with_suffix('.olean')
    raw, binary = src.read_bytes(), bp.read_bytes()
    assert r['returncode'] == 0 and r['output_exists'] and r.get('lean_returncode', 0) == 0
    assert Path(r['command'][2]) == bp and Path(r['command'][3]) == src
    assert sha(raw) == r['sha256'] and sha(binary) == r['output_sha256']
    assert cur[key].encode() == raw
    row = {'file': key, 'source_sha256': sha(raw), 'binary_sha256': sha(binary),
           'returncode': r['returncode'], 'lean_returncode': r.get('lean_returncode'),
           'timestamp': r['timestamp'], 'source_unchanged_during_compile': r.get('source_unchanged_during_compile'),
           'same_record_as_parent': key in oldrecords and r == oldrecords[key]}
    for k in ['stdout', 'stderr']:
        p = Path(r[k]); data = p.read_bytes()
        write(OUT / 'logs' / p.name, data)
        row[k + '_sha256'] = sha(data)
        row[k + '_bytes'] = len(data)
        row[k + '_path'] = str(p)
    lp = Path(r['stdout'].replace('.stdout.txt', '.json'))
    lograw = lp.read_bytes()
    assert json.loads(lograw) == r
    write(OUT / 'logs' / lp.name, lograw)
    row['log_name'], row['log_sha256'] = lp.name, sha(lograw)
    text = Path(r['stdout']).read_text(encoding='utf-8')
    assert not re.search(r'error(?:\([^)]*\))?:', text), key
    row['warnings'] = [s for s in text.splitlines() if 'warning:' in s]
    if row['same_record_as_parent']:
        for pin in ['source_sha256', 'binary_sha256', 'stdout_sha256', 'stderr_sha256', 'log_sha256']:
            assert row[pin] == oldpins[key][pin], (key, pin)
    if key in newkeys:
        a = axioms(text)
        shorts = re.findall(r'^#print axioms ([\w.]+)$', raw.decode(), re.M)
        expected = {'TGLV350.Regular.' + n: ownax['TGLV350.Regular.' + n] for n in shorts}
        assert a == expected
        maps[key] = a
    if key in newkeys | roots:
        assert (OUT / 'sources' / rel).read_bytes() == raw
        deps = []
        for name in re.findall(r'^import\s+([\w.]+)', raw.decode(), re.M):
            if name.split('.')[0] in {'TGL', 'TGLExt', 'TGLV350'}:
                dp = ROOT / 'build' / Path(*name.split('.')).with_suffix('.olean')
                assert dp.is_file() and dp.stat().st_mtime_ns <= bp.stat().st_mtime_ns, (key, name)
                ds = ROOT / 'kernel' / Path(*name.split('.')).with_suffix('.lean')
                deps.append({'module': name, 'source_sha256': hf(ds), 'binary_sha256': hf(dp), 'fresh': True})
        row['direct_dependencies'] = deps
    rows.append(row)

assert len(rows) == 216 and seen == set(I['added_kernel_files'] + I['updated_kernel_files'])
assert sum(r['same_record_as_parent'] for r in rows) == 211
changed = [r for r in rows if not r['same_record_as_parent']]
assert len(changed) == 5 and {r['file'] for r in changed} == newkeys | roots
assert all(r['source_unchanged_during_compile'] is True and r['lean_returncode'] == 0 for r in changed)
assert [r['file'] for r in rows[-5:]] == ['TGLExt/V350' + n + '.lean' for n in S['transposition']] + ['TGLExt.lean', 'TGL/Audit.lean']
assert set(oldrecords) - roots == {r['file'] for r in rows if r['same_record_as_parent']}

ar = rows[-1]
a = axioms(Path(ar['stdout_path']).read_text(encoding='utf-8'))
OE = load(OLD / 'kernel_incremental_evidence.json')
oldax = {n: sorted(x) for n, x in load(OLD / 'axioms.json').items()}
assert oldax == {n: sorted(x) for n, x in OE['axiom_report'].items()}
assert len(a) == G['axiom_report_entries'] == 7106 and a == {n: sorted(x) for n, x in E['axiom_report'].items()}
assert len(oldax) == 7086 and set(a) - set(oldax) == set(ownax)
assert all(a[n] == x for n, x in oldax.items()) and all(a[n] == x for n, x in ownax.items())
assert all(set(x) <= {'propext', 'Classical.choice', 'Quot.sound'} for x in a.values())
assert E['audit_stdout_sha256'] == E['audit_capture_sha256_full'] == ar['stdout_sha256']
assert E['audit_stdout_path'] == ar['stdout_path'] and E['audit_returncode'] == 0
assert E['audit_hash_scope'] == 'CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES'
assert E['historical_v350_audit_metadata'] == OE['historical_v350_audit_metadata']
source_names = re.findall(r"^#print axioms ([\w.']+)", cur['TGL/Audit.lean'], re.M)
assert set(source_names) == set(a)
old_names = re.findall(r"^#print axioms ([\w.']+)", oldembed['TGL/Audit.lean'], re.M)
source_counts = Counter(source_names)
assert all(source_counts[n] == c for n, c in Counter(old_names).items())

OG = load(OLD / 'gate_tests.json')
checks = {c['name']: c['passed'] for c in G['checks']}
oldchecks = {c['name']: c['passed'] for c in OG['checks']}
assert len(checks) == len(G['checks']) == G['passed'] == 106 and all(v is True for v in checks.values())
assert all(checks.get(n) == v for n, v in oldchecks.items())
added = sorted(set(checks) - set(oldchecks))
assert added == ['rational_squares_and_original_adjoint_test_does_not_discharge_KMS_trace_or_physical_frontier']
assert G['legacy_gate'] == OG['legacy_gate'] and G['frontier'] == OG['frontier']
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete']
assert not G['full_monolithic_runtime_run']
flags = {k: E[k] for k in P['remaining_flags']}
assert len(flags) == 6 and all(v is False for v in flags.values())
assert E['v350_modular_scope'] == OE['v350_modular_scope']

for p, h in S['surface_pins'].items():
    assert hf(p) == h, p
assert not any((ROOT / n).exists() for n in S['future_custody_artifacts_absent'])
assert hf(load(ROOT / 'environment.json')['original_source']) == hf(ROOT / 'fontes/um_v350_original.py') == S['original_sha256']
for p, h in P['review_sha256'].items():
    assert hf(p) == h
assert hf(REV / 'REVIEW_SQUARE_RESOLVENT_DEV.md') == S['own_DEV_review_sha256']
for f, h in S['artifact_pins'].items():
    assert hf(ROOT / f) == h
assert all(hf(ROOT / f) == hf(OUT / f) for f in files)
assert hf(ROOT / 'um.py') == S['working_sha256']

v = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
     'mode': 'AUTHOR_FINAL_ARTIFACTS_VERIFIED__OWN_EXECUTION_PENDING', 'complete': False, 'author_final_artifacts_validated': True, 'path': str(OUT),
     'working_sha256': I['working_sha256'], 'original_sha256': S['original_sha256'],
     'parent_custody_sha256': S['parent_custody_sha256'], 'embedded_files': len(cur),
     'all_three_literal_import_rewrites': True, 'python_AST_outside_embedded_equal': True,
     'gate_extension_equal_parent': True, 'records': rows, 'new_records': changed,
     'integrated_records': len(rows), 'unchanged_parent_records': 211, 'new_author_compilations': 5,
     'all_source_binary_log_stream_pins_match': True, 'new_axioms_equal_own_DEV': len(ownax),
     'audit_distinct': len(a), 'parent_Audit_preserved': len(oldax), 'audit_all_allowed': True,
     'final_Audit_record': ar, 'current_Audit_global_hashes_verified': True,
     'historical_Audit_metadata_preserved': E['historical_v350_audit_metadata'],
     'gate_passed_author_records': len(checks), 'added_controls': added, 'six_flags': flags,
     'scope': G['frontier']['scope'], 'legacy_gate_changed': False, 'full_goal_complete': False,
     'full_runtime': False, 'memory_surface_count': len(S['surface_pins']),
     'all_34_memory_current_pins_reread_preserved': True,
     'new_custody_report_verification_absent': S['future_custody_artifacts_absent'],
     'artifact_pins': {**S['artifact_pins'], **{f: hf(OUT / f) for f in files}},
     'static_verification_sha256': hf(OUT / 'static_verification.json'),
     'own_DEV_review_sha256': S['own_DEV_review_sha256'], 'new_Lean_executions': None, 'own_build_manifest_sha256': hf(OUT / 'build_manifest.json'), 'own_integrated_binaries_equal_author': None, 'dependency_provenance_counts': BM['provenance_counts'], 'binary_inheritance_limitation': 'FRESH_EXECUTION_OF_FIVE_PENDING__EXPLICITLY_INHERITED_DEPS',
     'author_programs_executed': False, 'memory_written': False, 'P0': [], 'P1': [], 'P2': []}
v['helper_static_inspection_sha256'] = hf(OUT / 'helper_static_inspection.json')
save(OUT / 'author_verification.json', v)
save(OUT / 'axioms.json', a)
save(OUT / 'new_module_axioms.json', maps)
save(OUT / 'own_DEV_axioms.json', ownax)
print(json.dumps({k: v[k] for k in ['path', 'complete', 'working_sha256', 'integrated_records',
    'unchanged_parent_records', 'new_author_compilations', 'gate_passed_author_records',
    'audit_distinct', 'current_Audit_global_hashes_verified', 'added_controls']}, ensure_ascii=False))
