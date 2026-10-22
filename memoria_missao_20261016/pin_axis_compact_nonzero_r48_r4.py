from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
work = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
mathlib = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages\mathlib\Mathlib')
ref = work / 'FECHO_MISSION_REFERENCE.json'
actor = {'kind': 'agent', 'id': 'codex-r48-nonzero-boost-witness'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

checked = {}
def verify_embedded(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            key = (obj['path'], obj['sha256'])
            if key not in checked:
                actual = pin(obj['path'])
                assert actual['sha256'] == obj['sha256'], actual['path']
                if 'bytes' in obj:
                    assert actual['bytes'] == obj['bytes'], actual['path']
                checked[key] = actual
        for value in obj.values():
            verify_embedded(value)
    elif isinstance(obj, list):
        for value in obj:
            verify_embedded(value)

def green(name):
    hits = []
    for src in sorted((out / 'orbital_rotation/attempts').glob('*/' + name)):
        rp = src.parent / 'RECEIPT.json'
        if not rp.is_file():
            continue
        r = json.loads(rp.read_text(encoding='utf-8-sig'))
        if r.get('exit_code') != 0 or src.read_bytes() != (base / name).read_bytes():
            continue
        axp = src.parent / 'AXIOMS.txt'
        ax = axp.read_text(encoding='utf-8')
        lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', ax)
        assert lists and 'sorryAx' not in ax and 'error:' not in ax
        assert all(set(x.strip() for x in s.split(',')) <=
            {'propext', 'Classical.choice', 'Quot.sound'} for s in lists)
        verify_embedded(r)
        hits.append({'source': pin(base / name), 'receipt': pin(rp), 'axioms': pin(axp),
            'exit_code': 0, 'seconds': r['seconds'], 'axiom_lists': len(lists),
            'attempt_source_matches': True, 'only_standard_trio': True})
    assert hits, name
    return hits[-1]

old = base / 'AxisCompactFockNonzeroEnergyR3.lean'
new = base / 'AxisCompactFockNonzeroEnergyR4.lean'
before = old.read_text(encoding='utf-8')
after = new.read_text(encoding='utf-8')
def statements(s):
    return [part.split(':= by', 1)[0] for part in re.split(r'^theorem ', s, flags=re.M)[1:]]
assert statements(before) == statements(after)
assert len(statements(after)) == 7
assert re.findall(r'^set_option .*$', before, re.M) == re.findall(r'^set_option .*$', after, re.M)
assert re.findall(r'^import .*$', before, re.M) == re.findall(r'^import .*$', after, re.M)
assert re.findall(r'^#print axioms .*$', before, re.M) == re.findall(r'^#print axioms .*$', after, re.M)
assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', after, re.M)
failed = out / 'orbital_rotation/attempts/20261016T192025_434393Z'
failure = json.loads((failed / 'RECEIPT.json').read_text(encoding='utf-8-sig'))
assert failure['exit_code'] == 1
assert (failed / old.name).read_bytes() == old.read_bytes()
assert failure['source']['sha256'] == pin(old)['sha256']
suppliers = [green('AxisCompactBoostEnergyShiftR3.lean'), green('CompactFockNullPlaneChargeR1.lean')]
files = [old, failed / 'RECEIPT.json', failed / 'AXIOMS.txt',
    base / 'AXIS_COMPACT_NONZERO_ENERGY_CANDIDATE_R48_R3.json',
    work / 'repair_axis_compact_nonzero_r4.py']
files += [mathlib / f for f in ['Analysis/InnerProductSpace/Basic.lean',
    'Data/Complex/Basic.lean', 'Analysis/Complex/Exponential.lean',
    'Analysis/Calculus/Deriv/Basic.lean', 'Analysis/Calculus/Deriv/Mul.lean']]
req = {'operation': 'project', 'reference': str(ref), 'actor': actor, 'max_chars': 100000}
r = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8',
    r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(req), text=True,
    encoding='utf-8', capture_output=True, check=True)
response = json.loads(r.stdout)
assert response['ok'], response
p = response['result']
report = {
    'schema': 'iald-lean-candidate-repair/v1', 'status': 'DECLARADO_PENDING_BUILD',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reference': pin(ref), 'actor': actor, 'handle': 'r48-nonzero-r4-repair',
    'mission_receipt': p['receipt'], 'projection_sha256': p['projection_sha256'],
    'source': pin(new), 'previous_source': pin(old), 'suppliers': suppliers,
    'pins': [pin(f) for f in files], 'script': pin(Path(__file__)),
    'supplier_receipt_embedded_pins_verified': len(checked),
    'supplier_receipt_embedded_bytes_verified': sum(x['bytes'] for x in checked.values()),
    'verification_scope': 'All path/sha256 objects in the two direct suppliers\' build receipts were read and matched. No new compilation or recursive parsing of dependency receipts.',
    'repair': [
        'Convert the inner-self theorem into an explicitly typed complex equality; transport the real power and exponential by typed equalities, and simplify only complex multiplication components.',
        'Prove the scalar derivative identity as a complex equality; use a typed HasDerivAt for const_mul and congr_deriv with convert! to align instances.'
    ],
    'source_checks': {'same_seven_statements': True, 'same_imports': True,
        'same_options_and_heartbeat_limit': True, 'same_seven_print_axioms': True,
        'no_sorry_admit_axiom_opaque': True, 'previous_sources_untouched': True},
    'failed_attempt': {'path': str(failed), 'exit_code': failure['exit_code'],
        'seconds': failure['seconds'], 'not_accepted': True},
    'scope': 'Same normalized AxisCompact witness in the concrete Fock. Boost witness has no non-vacuity premise. Modular and calibrated-charge corollaries retain explicit A : RemainingModularCoreInput D and N : KillingNormalization. The repair adds no assumption and changes no factor or sign.',
    'remaining': ['Root compilation and independent review of R4.',
        'All full R8 criteria remain intact; this repair does not inhabit A or accept R8.'],
    'requirement_satisfied': False, 'author_builds': 0,
    'production_changes': False, 'mission_mutations': False
}
dst = base / 'AXIS_COMPACT_NONZERO_ENERGY_CANDIDATE_R48_R4.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
assert not dst.exists()
tmp = dst.with_name(dst.name + '.tmp_r48_r4')
with tmp.open('xb') as f:
    f.write(data)
    f.flush()
    os.fsync(f.fileno())
assert tmp.read_bytes() == data
os.rename(tmp, dst)
assert dst.read_bytes() == data
print(json.dumps({'source': pin(new), 'manifest': pin(dst),
    'suppliers': [{k: v for k, v in x.items() if k in ['exit_code', 'seconds', 'axiom_lists']} for x in suppliers],
    'verified_pins': len(checked), 'revision': p['receipt']['revision']}, ensure_ascii=False))
