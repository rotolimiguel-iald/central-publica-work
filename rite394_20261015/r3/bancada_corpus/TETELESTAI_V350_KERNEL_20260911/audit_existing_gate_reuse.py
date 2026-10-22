"""Read-only source audit; write new evidence inside this workspace only."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'AUDITORIA_REUSO_GATE_20260913'
assert not OUT.exists()
OUT.mkdir()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def save(name, obj):
    path = OUT / name
    assert not path.exists()
    raw = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)

source = (ROOT / 'um.py').read_bytes()
tree = ast.parse(source)
maps = {}
embedded = None
for n in tree.body:
    if isinstance(n, ast.Assign):
        for target in n.targets:
            if isinstance(target, ast.Name):
                if target.id in ('_QG_CERTIFICATE_FLAGS', '_QG_PHYSICS_FLAGS',
                                 '_QG_FRONTIER_FLAGS', '_GRAVITY_PRICE_FLAGS'):
                    maps[target.id] = ast.literal_eval(n.value)
                if target.id == '_EMBEDDED_KERNEL_FILES':
                    embedded = ast.literal_eval(n.value)
gate_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == 'evaluate_quantum_gravity_closure')
namespace = {}
exec(compile(ast.Module(body=[gate_node], type_ignores=[]), '<isolated gate AST>', 'exec'), namespace)
evaluate = namespace[gate_node.name]
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
baseline = json.loads((ROOT / 'fontes/um_absoluto.json').read_bytes())
parent = json.loads((ROOT / 'paired_blocks_custody.json').read_bytes())
assert sha(source) == parent['working_sha256']
assert sha((ROOT / 'kernel_incremental_evidence.json').read_bytes()) == parent['artifacts']['kernel_incremental_evidence.json']
audit = Path(evidence['audit_stdout_path'])
assert sha(audit.read_bytes()) == evidence['audit_stdout_sha256']
formal = {k: evidence.get('qgc_' + k) is True for k in maps['_QG_CERTIFICATE_FLAGS']}
physics = {k: evidence.get('qgp_' + k) is True for k in maps['_QG_PHYSICS_FLAGS']}
experiment = baseline['core']['void_floor_v11']['experiment_feed']
result = evaluate(formal, physics, experiment)
assert all(formal.values()) and all(physics.values())
assert result == baseline['core']['qg_closure']['gate']
rows = []
for mapping, prefix, category in [('_QG_CERTIFICATE_FLAGS','qgc_','FORMAL'),
                                  ('_QG_PHYSICS_FLAGS','qgp_','PHYSICS')]:
    for flag, name in maps[mapping].items():
        ax = evidence['axiom_report'].get(name)
        assert isinstance(ax, list) and set(ax) <= {'propext','Classical.choice','Quot.sound'}
        short = name.rsplit('.', 1)[-1]
        pattern = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:noncomputable\s+)?(?:def|theorem|lemma)\s+' + re.escape(short) + r'\b', re.M)
        matches = []
        for filename, text in embedded.items():
            hit = pattern.search(text)
            if hit:
                path = ROOT / 'kernel' / filename
                raw = path.read_bytes()
                assert raw.decode('utf-8').replace('\r\n','\n') == text.replace('\r\n','\n')
                line = raw.decode('utf-8').splitlines()
                ln = next(i+1 for i,x in enumerate(line) if pattern.search(x))
                matches.append({'file': str(path), 'line': ln, 'sha256': sha(raw)})
        assert len(matches) == 1, (name, matches)
        rows.append({'category': category, 'flag': prefix+flag, 'value': evidence[prefix+flag],
                     'declaration': name, 'axioms': ax, 'source': matches[0]})
tests = []
for name in formal:
    case = dict(formal); case[name] = False
    assert evaluate(case, physics, experiment)['mathematical_model_constructed'] is False
    tests.append('remove_formal:'+name)
for name in physics:
    case = dict(physics); case[name] = False
    assert evaluate(formal, case, experiment)['physical_quantum_gravity_constructed'] is False
    tests.append('remove_physics:'+name)
# Evaluate all combinations of the eight frontier/price keys as additional inputs.
# None is read by the real gate: this is a dependency test, not a proof promotion.
extra_keys = ['qgf_'+k for k in maps['_QG_FRONTIER_FLAGS']] + ['gpf_'+k for k in maps['_GRAVITY_PRICE_FLAGS']]
for mask in range(1 << len(extra_keys)):
    extra = {k: bool(mask & (1 << i)) for i,k in enumerate(extra_keys)}
    assert evaluate(formal | extra, physics | extra, experiment | extra) == result
tests.append('all_256_frontier_price_combinations_leave_existing_gate_unchanged')
save('gate_evidence.json', {'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'working_sha256': sha(source), 'parent_custody_sha256': sha((ROOT/'paired_blocks_custody.json').read_bytes()),
    'gate_source_line': gate_node.lineno, 'gate_end_line': gate_node.end_lineno,
    'entries': rows, 'formal_count': len(formal), 'physics_count': len(physics),
    'gate_result': result, 'experiment_feed_provenance': 'existing baseline; no experiment rerun',
    'axiom_report_provenance': 'existing current incremental Audit; no new Lean build in this audit',
    'tests': tests, 'monolith_imported_or_executed': False, 'gate_changed': False})
print(json.dumps({'gate_entries_verified': len(rows), 'mutation_tests': 11,
                  'frontier_combinations_tested': 256, 'verdict': result['verdict']}), flush=True)

# Inventory all external Lean source paths, excluding dependencies and our work tree.
command = ['rg','--files','.', '-g','*.lean','-g','!**/.lake/**','-g','!**/packages/**',
           '-g','!**/build/**','-g','!**/TETELESTAI_V350_KERNEL_20260911/**','-g','!**/*.bak*']
scan = subprocess.run(command, cwd=ROOT.parent, capture_output=True)
assert scan.returncode == 0, scan.stderr.decode(errors='replace')
paths = [(ROOT.parent / x).resolve() for x in scan.stdout.decode('utf-8').splitlines()]
unique, failures = {}, []
for p in paths:
    assert not p.is_relative_to(ROOT)
    try:
        raw = p.read_bytes()
    except OSError as exc:
        failures.append({'path':str(p),'error':str(exc)})
        continue
    key = sha(raw)
    if key not in unique:
        unique[key] = {'raw':raw,'paths':[]}
    unique[key]['paths'].append(str(p))
def normalized(raw):
    text = raw.decode('utf-8-sig').replace('\r\n','\n')
    match = re.search(r'^import\s',text,re.M)
    if match:
        text = text[match.start():]
    return sha(text.strip().encode())
current = {}
for name,text in embedded.items():
    current.setdefault(normalized(text.encode()),[]).append(name)
matches, candidates = [], []
for pin,row in unique.items():
    norm = normalized(row['raw'])
    if norm in current:
        matches.append({'sha256':pin,'paths':row['paths'],'embedded_files':current[norm],
                        'normalized_sha256':norm})
    text = row['raw'].decode('utf-8-sig')
    heads = re.findall(r'^(?:theorem|lemma|def)\s+([^\s:(]+)[^\n]*',text,re.M)
    selected = [n for n in heads if re.search(r'(?:[Bb]lock|[Pp]rojection|[Vv]ariational).*(?:[Ll]ower|[Ii]nvers|[Ee]nergy|[Bb]ound)|[Ll]ower.*[Bb]lock',n)]
    if selected:
        candidates.append({'sha256':pin,'paths':row['paths'],'declarations':selected})
save('external_source_reuse.json',{'method':'Exact byte deduplication; normalized match removes leading material before first import and normalizes CRLF/edge whitespace only. No semantic equivalence inferred.',
    'paths_inventoried':len(paths),'files_read':sum(len(v['paths']) for v in unique.values()),
    'distinct_byte_hashes':len(unique),'failures':failures,
    'distinct_matching_hashes':len(matches),'matching_paths':sum(len(m['paths']) for m in matches),
    'matching_embedded_files':sorted({p for m in matches for p in m['embedded_files']}),
    'matches':matches,'gap_related_name_candidates_not_semantically_reviewed':candidates,
    'all_other_folders_unchanged_by_this_script':True})
print(json.dumps({'external_paths':len(paths),'distinct_hashes':len(unique),
    'matching_paths':sum(len(m['paths']) for m in matches),
    'matching_embedded_modules':len({p for m in matches for p in m['embedded_files']}),
    'read_failures':len(failures),'gap_name_candidate_sources':len(candidates)}), flush=True)
