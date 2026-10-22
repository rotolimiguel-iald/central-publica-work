from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
attempt = out / 'orbital_rotation/attempts/20261016T191655_039766Z'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind': 'agent', 'id': 'codex-r48-regular-independent-review'}

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def pin(path):
    path = Path(path)
    b = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def collect(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get('path'), str) and isinstance(obj.get('sha256'), str):
            yield obj
        for v in obj.values():
            yield from collect(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from collect(v)

manifest = read_json(base / 'AXIS_COMPACT_REGULAR_CANDIDATE_R2.json')
receipt = read_json(attempt / 'RECEIPT.json')
cache = read_json(attempt / 'DEPENDENCY_CACHE.json')
unique = {}
for obj in [manifest, receipt, cache]:
    for item in collect(obj):
        key = (str(Path(item['path']).resolve()).casefold(), item['sha256'].lower())
        unique[key] = item
failures = []
checked_bytes = 0
for item in unique.values():
    try:
        actual = pin(item['path'])
        checked_bytes += actual['bytes']
        if actual['sha256'] != item['sha256'].lower() or (
                'bytes' in item and actual['bytes'] != item['bytes']):
            failures.append({'expected': item, 'actual': actual})
    except Exception as e:
        failures.append({'path': item['path'], 'error': str(e)})
assert not failures, failures
source = base / 'AxisCompactRegularR2.lean'
assert source.read_bytes() == (attempt / source.name).read_bytes()
s = source.read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', s, re.M)
assert receipt['exit_code'] == 0
assert receipt['readonly_dependencies_unchanged'] and receipt['dependency_cache_unchanged']
assert receipt['production_modified'] is False
ax = (attempt / 'AXIOMS.txt').read_text(encoding='utf-8')
lists = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", ax)
assert len(lists) == 4 and 'sorryAx' not in ax
assert all(set(v.strip() for v in row.split(',')) <=
           {'propext', 'Classical.choice', 'Quot.sound'} for _, row in lists)

request = {'operation': 'project', 'reference': str(ref), 'actor': actor, 'max_chars': 100000}
run = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8',
    r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(request), text=True,
    encoding='utf-8', capture_output=True, check=True)
response = json.loads(run.stdout)
assert response['ok'], response
p = response['result']
report = {
    'schema': 'iald-independent-review/v1', 'verdict': 'PASS_COMPONENT_WITH_SCOPE',
    'requirement': 'R8', 'requirement_satisfied': False,
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer': actor, 'source_author': manifest['author'],
    'independence': 'Reviewer did not construct AxisCompactRegularR1/R2. Reviewer authored prior charge-coordinate and boost components; this review is limited to the separate Regular construction and the bytes of its suppliers.',
    'reference': pin(ref), 'mission_receipt': p['receipt'],
    'projection_sha256': p['projection_sha256'], 'handle': 'r48-regular-independent-review',
    'source': pin(source), 'candidate_manifest': pin(base / 'AXIS_COMPACT_REGULAR_CANDIDATE_R2.json'),
    'build': {'receipt': pin(attempt / 'RECEIPT.json'), 'exit_code': receipt['exit_code'],
        'seconds': receipt['seconds'], 'axioms': pin(attempt / 'AXIOMS.txt'),
        'declarations': [name for name, _ in lists], 'only_standard_trio': True,
        'source_bytes_match_attempt': True},
    'pin_verification': {'unique_path_hash_pairs': len(unique), 'bytes_hashed': checked_bytes,
        'mismatches': 0, 'coverage': 'All path+sha256 pins recursively present in the R2 candidate manifest, build receipt and dependency-cache manifest; every original and copied cache module pin was read. This is not a new Lean rebuild.'},
    'literal_regular_clauses': [
        {'clause': 'psi in Dom', 'proof': 'mem_axisCompactFockDomain_iff from the existing exact AxisCompact coefficient predicate, inside the unchanged Fock.'},
        {'clause': 'For every base point x, product-plane first-moment integrability', 'proof': 'axisCompact_calibrated_nullCharge_integrable applied to the actual U1(-x) translated vector; translation preserves AxisCompactFock and tensor covariance identifies the entire integrand for every x.'},
        {'clause': 'norm psi = 1', 'proof': 'Exact explicit hn premise, unchanged in the final Regular conjunction.'},
        {'clause': 'For every x, continuity along u -> x + u*nullDir', 'proof': 'At zero base point the actual stress restriction is a Schwartz function; translation covariance extends to arbitrary x.'},
        {'clause': 'For every x and l, unweighted integrability on Ioi l', 'proof': 'The zero-base ray is full-line integrable as a Schwartz restriction; translated vectors supply each x, and Integrable.integrableOn supplies every Ioi l.'},
        {'clause': 'For every x and l, weighted integrability of u*Tnn on Ioi l', 'proof': 'Multiplication of the Schwartz ray by the polynomial u is integrable; the same covariance and restriction discharge every x,l.'}
    ],
    'adversarial_checks': [
        'The Fourier restriction uses a nonzero line direction and proves the proper-growth bound; an arbitrary non-proper restriction is not assumed Schwartz.',
        'Finite coherent sums retain all mixed terms and the actual unique coefficients, using both AxisCompact supports.',
        'The covariance argument uses the negative state translation and identifies x+y with the contract base-point shift; no quantifier is limited to x=0.',
        'The final theorem consumes only A, psi in regularFockDomain, AxisCompactFock psi and the stated unit norm. No Regular clause, tail estimate, charge equality or nonzero-energy premise is added.',
        'The global calibrated tensor is reused and is not made zero outside a newly invented domain. The final domain is exactly axisCompactFockDomain.'
    ],
    'scope_limits': [
        'RemainingModularCoreInput A is an explicit assembly premise; this component does not construct its unresolved trace/PF data.',
        'Unit norm is an explicit condition. This theorem does not itself construct a normalized state or a nonzero modular-energy witness.',
        'No physical clock selection, complete MaxwellCertificate, full R8 acceptance or gate change is certified here.'
    ],
    'findings': [],
    'nonblocking_residue': ['Deprecation and unused-simplifier warnings in the existing successful build do not change theorem statements or axioms.'],
    'consulted_contract': pin(kernel / 'TGLExt/TheImportedSecondQuantization.lean'),
    'review_script': pin(Path(__file__)), 'own_builds': 0, 'accept_transition_performed': False
}
dest = out / 'mission_review_20261016/R48_REGULAR_INDEPENDENT_REVIEW_R1.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = dest.with_suffix('.json.tmp_review_r48')
with tmp.open('xb') as stream:
    stream.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dest)
assert dest.read_bytes() == data
print(json.dumps({'verdict': report['verdict'], 'review': pin(dest),
    'source': pin(source), 'pins': len(unique), 'bytes_hashed': checked_bytes,
    'revision': p['receipt']['revision']}, ensure_ascii=False))
