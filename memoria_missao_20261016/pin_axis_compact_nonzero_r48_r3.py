from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib = kernel / '.lake/packages/mathlib/Mathlib'
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind': 'agent', 'id': 'codex-r48-nonzero-boost-witness'}

def pin(path):
    path = Path(path)
    b = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def green(name):
    found = []
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
        assert lists and 'sorryAx' not in ax
        assert all(set(x.strip() for x in s.split(',')) <=
                   {'propext', 'Classical.choice', 'Quot.sound'} for s in lists)
        assert r['source']['sha256'] == pin(base / name)['sha256']
        found.append({'source': pin(base / name), 'receipt': pin(rp), 'axioms': pin(axp),
            'exit_code': 0, 'seconds': r['seconds'], 'axiom_lists': len(lists),
            'attempt_source_matches': True, 'only_standard_trio': True})
    assert found, name
    return found[-1]

sources = []
for name in ['AxisCompactBoostEnergyShiftR3.lean', 'AxisCompactFockNonzeroEnergyR3.lean']:
    path = base / name
    s = path.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', s, re.M)
    sources.append({**pin(path), 'lines': len(s.splitlines()),
        'public_theorems': len(re.findall(r'^theorem ', s, re.M)),
        'print_axioms': len(re.findall(r'^#print axioms ', s, re.M)),
        'status': 'DECLARADO_PENDING_BUILD'})
suppliers = [green(name) for name in [
    'AxisCompactFockTranslationR2.lean', 'CompactFockNullPlaneChargeR1.lean',
    'CompactFockBoostDerivativeR2.lean', 'CompactBoostMixedNullMomentR1.lean']]
files = [base / name for name in [
    'AxisCompactBoostEnergyShiftR1.lean', 'AxisCompactFockNonzeroEnergyR1.lean',
    'AxisCompactBoostEnergyShiftR2.lean', 'AxisCompactFockNonzeroEnergyR2.lean',
    'AXIS_COMPACT_NONZERO_ENERGY_CANDIDATE_R48_R2.json',
    'NullSchwartzCoreSeedR1.lean', 'AxisCompactProfileDensityR4.lean',
    'RegularMaxwellEnergyR2.lean', 'CartesianMaxwellBivectorR5.lean',
    'CompactBoostStrongDerivativeReductionR3.lean', 'CompactBoostStrongDerivativeR2.lean',
    'CompactBoostNullMomentLinkR5.lean', 'RegularFockPointStressR4.lean',
    'COMPACT_FOCK_NULL_PLANE_CHARGE_CANDIDATE_R47.json']]
files += [out / name for name in [
    'network_exponential/ExponentialVectorsR3.lean',
    'mission_resume_20261016/LIVE_HANDOFF_R8_20261016T190424_690000Z_6d1dad1a_RECEIPT.json',
    'orbital_rotation/attempts/20261016T191034_092274Z/AXIOMS.txt',
    'orbital_rotation/attempts/20261016T191034_092274Z/RECEIPT.json',
    'orbital_rotation/attempts/20261016T191532_328287Z/RECEIPT.json',
    'orbital_rotation/attempts/20261016T191532_328287Z/AXIOMS.txt']]
files += [kernel / name for name in [
    'TGLExt/O16/OrbitTranslationFaithfulness_v2.lean',
    'TGLExt/O16/OrbitalMeasureSupport_v2.lean',
    'TGLExt/ContratoQG_v31.lean', 'TGLExt/ContratoQG_v31_Teoremas.lean']]
files += [mathlib / name for name in [
    'Analysis/Complex/RealDeriv.lean', 'Analysis/Complex/Norm.lean',
    'Analysis/Calculus/Deriv/Mul.lean', 'Analysis/SpecialFunctions/ExpDeriv.lean',
    'Analysis/InnerProductSpace/Basic.lean', 'Data/Complex/Basic.lean',
    'MeasureTheory/Function/LpSpace/Basic.lean',
    'MeasureTheory/Integral/Bochner/Basic.lean',
    'MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean']]
pins = [pin(f) for f in files]
req = {'operation': 'project', 'reference': str(ref), 'actor': actor, 'max_chars': 100000}
r = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8',
    r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(req), text=True,
    encoding='utf-8', capture_output=True, check=True)
response = json.loads(r.stdout)
assert response['ok'], response
p = response['result']
report = {
    'schema': 'iald-lean-candidate/v1', 'status': 'DECLARADO_PENDING_BUILD',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reference': pin(ref), 'actor': actor, 'handle': 'r48-nonzero-boost-witness',
    'mission_receipt': p['receipt'], 'projection_sha256': p['projection_sha256'],
    'sources': sources, 'suppliers': suppliers, 'pins': pins,
    'construction': [
        'Use the existing spatial translation (0,1,0,0), with actual orbital phase exp(-i*p1).',
        'Differentiate this phase along the existing negative-coordinate boost orbit; its product with the smooth compact representative gives the translated generator.',
        'The diagonal boost coefficient increases by i times integral(shellEnergy*norm(h)^2), with the same measure and generator sign.',
        'The energy integral is strictly positive for nonzero StrongRegularProfile, since shellEnergy is positive off the measure-zero transverse axis and an Lp vector vanishing almost everywhere is zero.',
        'The existing nonzero AxisCompact seed therefore gives either itself or its actual U1 translation with nonzero imaginary boost coefficient.',
        'Its existing exponential vector has boost energy exp(norm(h)^2) times the one-particle value, hence nonzero.',
        'Scalar normalization by the inverse Fock norm preserves AxisCompactFock and scales the actual boost derivative by the nonzero norm-square factor.',
        'Existing lightH2 for explicit A,N supplies nonzero modular energy. The already constructed charge identity gives nonzero calibrated nullPlaneCharge for that same vector.'
    ],
    'interface': 'exists_axisCompact_normalized_nonzero_boostEnergy : ∃ psi : regularFockDomain, AxisCompactFock psi ∧ norm psi.val = 1 ∧ ∃ b : Real, HasBoostEnergy VF psi.val b ∧ b ≠ 0',
    'modular_interface': 'exists_axisCompact_normalized_nonzero_modularEnergy (A : RemainingModularCoreInput D) (N : KillingNormalization) : ∃ psi : regularFockDomain, AxisCompactFock psi ∧ norm psi.val = 1 ∧ ∃ k : Real, HasModularEnergy (lightDelta A.toCertificate) psi.val k ∧ k ≠ 0',
    'premises': 'The boost witness has no non-vacuity, derivative, stress-positivity or charge-equality premise. A and N occur only in modular/charge assembly and remain explicit. The construction does not select a physical clock or inhabit A.',
    'failed_original': 'ShiftR1 attempt 20261016T191034_092274Z exited 1 in 73.49s. strict energy-integral positivity elaborated with the standard trio; other declarations carried sorryAx from elaboration failures and are not accepted. R2 repairs explicit Complex.ofReal smoothness, derivative instance conversions and scalar algebra; no statements or limits were weakened.',
    'r3_repairs': 'ShiftR2 attempt 20261016T191532_328287Z exited 1 in 93.96s with two remaining elaboration failures. The phase derivative and strict positivity have standard-trio output. R3 states coordinateBoost 0 0 y = y explicitly and transports a typed real-to-complex integral equality through congrArg/convert!. The dependent R3 changes only its import. Statements and heartbeat limits are unchanged.',
    'remaining': ['Compile R3 modules and independently review them.',
        'Obtain the complete Regular clauses and Maxwell assembly from the separate authorized construction, on this same normalized AxisCompact vector.',
        'Discharge all remaining full R8 criteria, including unresolved assembly inputs.'],
    'not_claimed': ['Compilation of these candidates', 'Independent acceptance',
        'Complete Regular in these files', 'Inhabitant of RemainingModularCoreInput',
        'Physical clock selection', 'Satisfied R8', 'Production or gate change'],
    'author_builds': 0, 'pin_coverage': 'Consulted direct suppliers, their checked green build receipts and axioms, original failed source/log, and actual pinned mathlib APIs. Not a transitive dependency custody.',
    'script': pin(Path(__file__))
}
dst = base / 'AXIS_COMPACT_NONZERO_ENERGY_CANDIDATE_R48_R3.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = dst.with_suffix('.json.tmp_r48_r3')
with tmp.open('xb') as f:
    f.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dst)
assert dst.read_bytes() == data
print(json.dumps({'sources': sources, 'manifest': pin(dst), 'pins': len(pins),
    'revision': p['receipt']['revision']}, ensure_ascii=False))
