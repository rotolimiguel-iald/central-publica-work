from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib = kernel / '.lake/packages/mathlib/Mathlib'
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind': 'agent', 'id': 'codex-r8-mixed-stress-integral'}
request = {'operation': 'project', 'reference': str(ref), 'actor': actor, 'max_chars': 100000}
run = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8',
    r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(request), text=True,
    encoding='utf-8', capture_output=True, check=True)
response = json.loads(run.stdout)
assert response['ok'], response
p = response['result']

def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

sources = [base / f for f in ['CoherentNullStressMomentR1.lean', 'CompactFockNullStressMomentR1.lean']]
source_records = []
for path in sources:
    source = path.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', source, re.M), path
    source_records.append({**pin(path), 'lines': len(source.splitlines()),
        'public_theorems': len(re.findall(r'^theorem ', source, re.M)),
        'private_theorems': len(re.findall(r'^private theorem ', source, re.M)),
        'print_axioms': len(re.findall(r'^#print axioms ', source, re.M))})

files = [base / f for f in [
    'CompactFockBoostDerivativeR2.lean', 'CompactBoostMixedNullMomentR1.lean',
    'CompactBoostNullMomentLinkR5.lean', 'CompactBoostStrongDerivativeR2.lean',
    'NullSchwartzSameSignR2.lean', 'AngularWeightedPlancherelR3.lean',
    'WeightedSchwartzPlancherelR3.lean', 'MaxwellNullSchwartzConsumerR2.lean',
    'ConstructedNullSchwartzConsumerR1.lean', 'ConstructedRealNullStressMomentR1.lean',
    'MaxwellNullPlaneAlgebraR2.lean', 'MaxwellNullPlaneWaveR2.lean',
    'CoherentPointMaxwellR1.lean', 'CoherentPointStressR2.lean',
    'FiniteCoherentKernelR3.lean', 'FiniteCoherentKernelCalculusR2.lean',
    'RegularFockPointStressR4.lean', 'RegularMaxwellFockDomainR5.lean',
    'UnitaryFourierRealStressR2.lean', 'UnitaryFourierStressTensorR2.lean',
    'UnitaryFourierFockStressR1.lean', 'CalibratedFockStressDomainBridgeR1.lean',
    'RegularFockMaxwellCalibratedR1.lean', 'COMPACT_FOCK_BOOST_CANDIDATE_R47.json']]
files += [mathlib / f for f in ['MeasureTheory/Integral/Bochner/Basic.lean',
    'MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',
    'MeasureTheory/Function/L1Space/Integrable.lean',
    'Analysis/InnerProductSpace/Basic.lean']]
files += [out / 'mission_resume_20261016/LIVE_R47_MIXED_STRESS_HANDOFF_20261016T182947_666234Z_985f9740_RECEIPT.json',
    out / 'orbital_rotation/attempts/20261016T183037_597328Z/AXIOMS.txt',
    out / 'orbital_rotation/attempts/20261016T183826_075105Z/RECEIPT.json',
    out / 'orbital_rotation/attempts/20261016T183826_075105Z/AXIOMS.txt']
build_dir = out / 'orbital_rotation/attempts/20261016T183826_075105Z'
build = json.loads((build_dir / 'RECEIPT.json').read_text(encoding='utf-8-sig'))
assert build['exit_code'] == 0
assert (build_dir / 'CompactFockBoostDerivativeR2.lean').read_bytes() == (base / 'CompactFockBoostDerivativeR2.lean').read_bytes()
assert 'sorryAx' not in (build_dir / 'AXIOMS.txt').read_text(encoding='utf-8')

report = {
    'schema': 'iald-lean-candidate/v1', 'status': 'DECLARADO_UNCOMPILED',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actor': actor, 'reference': pin(ref), 'mission_receipt': p['receipt'],
    'projection_sha256': p['projection_sha256'], 'projection_chars': p['actual_chars'],
    'handle': 'r47-r8-mixed-stress-integral', 'sources': source_records,
    'chain': [
        'Expand the complex coherent square with its exact sqrt(2) factor into conjugated same-sign, mixed, and same-sign products.',
        'Weighted integrability is constructed for each term from the existing angular Schwartz integrability theorems and the conjugation continuous linear map.',
        'The two same-sign integrals vanish by the existing positive-null-frequency support theorem; the conjugated one vanishes by integral_conj.',
        'The remaining mixed term is evaluated by the existing angular_weighted_parseval with its full (2*pi)^3 factor.',
        'The actual tensor null contraction is expressed by stress_null_contraction and the constructed mixed coherent screen waves.',
        'The exact unitaryFourierStressScale cancels (2*pi)^3; the mixed H1 derivative bridge identifies the complex moment with -I*coherentBoostPair.',
        'A support-restricted integral theorem transports integrability and the equality through the actual finiteKernel and unique regularCoefficients.',
        'Taking the real part yields Im(regularFockBoostPair) for the whole diagonal finite sum, and the existing actual VF derivative proves HasBoostEnergy with this real tensor moment.'
    ],
    'mixed_statement': 'axisCompact_coherentNullStress_moment (h k : H1) (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) : (∫ x : NullFourierSpace, (x 0 : ℂ) * unitaryFourierCoherentNullStress h k x) = -Complex.I * coherentBoostPair h k',
    'mixed_statement_expansion': 'unitaryFourierCoherentNullStress is definitionally the four 00+01+10+11 components at nullPlanePoint (x 0) (nullFourierScreen x), exactly the prior manifest obligation.',
    'finite_statement': 'axisCompact_fockNullStress_moment (psi chi : regularFockDomain) (hpsi : AxisCompactFock psi) (hchi : AxisCompactFock chi) : (∫ x : NullFourierSpace, (x 0 : ℂ) * unitaryFourierFockNullStress psi chi x) = -Complex.I * regularFockBoostPair psi chi',
    'final_statement': 'axisCompact_fock_hasBoostEnergy_null_moment (psi : regularFockDomain) (hpsi : AxisCompactFock psi) : HasBoostEnergy VF psi.val (∫ x : NullFourierSpace, x 0 * (unitaryFourierFockNullStress psi psi x).re)',
    'premises': 'Only existing AxisCompactProfile/AxisCompactFock regularity in the final public identities. No integral equality, charge identity, HasDerivAt or integrability is added as a hypothesis there.',
    'unchanged_objects': ['Actual H1/Fock, orbital measure, B0/VF and unique regular coefficients',
        'Existing unitaryFourierCoherentStress and unitaryFourierPointStressForm',
        'Existing calibrated Maxwell form and its coefficient (2*pi)^(-3)'],
    'remaining': ['Compile both new modules and independently review them.',
        'Prove the named AxisCompact Fock core has vacuum, translation/boost invariance and the required density/nontriviality.',
        'Transport the Euclidean null Fourier coordinates/measure and screen reflection to the contract nullPlaneCharge product coordinates.',
        'Compose the calibrated tensor bridge and modular/boost convention into charge_link on the named domain.',
        'Construct a normalized Regular state with nonzero modular energy and discharge the other full R8 obligations.'],
    'not_claimed': ['Compilation', 'Independent acceptance', 'Full MaxwellCertificate',
        'Full charge_link in contract coordinates', 'Nonzero modular energy', 'Complete R8', 'Gate change'],
    'build_performed_by_author': False, 'pins': [pin(f) for f in files],
    'derivative_supplier': {'source': pin(base / 'CompactFockBoostDerivativeR2.lean'),
        'receipt': pin(build_dir / 'RECEIPT.json'), 'exit_code': build['exit_code'],
        'seconds': build['seconds'], 'attempt_source_matches': True},
    'pin_coverage': 'Consulted direct suppliers and mathlib APIs, exact handoff, prior candidate manifest and mixed H1 build axiom output. Not a transitive build custody.'
}
dst = base / 'COMPACT_FOCK_NULL_MOMENT_CANDIDATE_R47.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = dst.with_suffix('.json.tmp_r47')
with tmp.open('xb') as f:
    f.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dst)
print(json.dumps({'sources': source_records, 'manifest': pin(dst),
    'pins': len(files), 'revision': p['receipt']['revision']}, ensure_ascii=False))
