from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib = kernel / '.lake/packages/mathlib/Mathlib'
fock = out.parent / 'F1.REDE/fock_construction'
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind': 'agent', 'id': 'codex-r8-fock-charge'}
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

sources = [base / f for f in ['CompactBoostMixedNullMomentR1.lean', 'CompactFockBoostDerivativeR1.lean']]
source_records = []
for path in sources:
    source = path.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', source, re.M), path
    source_records.append({**pin(path), 'lines': len(source.splitlines()),
        'theorems': len(re.findall(r'^theorem ', source, re.M)),
        'print_axioms': len(re.findall(r'^#print axioms ', source, re.M))})
assert sources[0].read_text(encoding='utf-8').startswith('import CompactBoostNullMomentLinkR5\n')

files = [base / f for f in [
    'CompactBoostNullMomentLinkR5.lean', 'CompactBoostStrongDerivativeR2.lean',
    'CompactBoostStrongDerivativeReductionR3.lean', 'NullFrequencyBochnerR2.lean',
    'MaxwellNullSchwartzConsumerR2.lean', 'ConstructedNullSchwartzConsumerR1.lean',
    'NullSchwartzCoreSeedR1.lean', 'AxisCompactProfileDensityR4.lean',
    'RegularMaxwellFockDomainR5.lean', 'RegularMaxwellDensityR2.lean',
    'RegularFockPointStressR4.lean', 'RegularCoherentTransportR1.lean',
    'FiniteCoherentKernelR3.lean', 'FiniteCoherentKernelCalculusR2.lean',
    'CoherentPointMaxwellR1.lean', 'CoherentPointStressR2.lean',
    'ConstructedRealNullStressMomentR1.lean', 'UnitaryFourierStressTensorR2.lean',
    'UnitaryFourierFockStressR1.lean']]
files += [out / 'network_exponential' / f for f in ['ExponentialVectorsR3.lean', 'ExponentialTotalityR4.lean']]
files += [fock / 'BosonicFockGroupActions.lean',
    kernel / 'TGLExt/ContratoQG_v31.lean', kernel / 'TGLExt/TheImportedSecondQuantization.lean',
    out / 'candidate_r8/tgl_kernel/TGLExt/O16/OrbitalBoostUnitary_v2.lean']
files += [mathlib / f for f in ['Analysis/InnerProductSpace/Calculus.lean',
    'Analysis/InnerProductSpace/Basic.lean', 'Analysis/InnerProductSpace/LinearMap.lean',
    'Analysis/Calculus/Deriv/Star.lean', 'Analysis/Calculus/Deriv/Comp.lean',
    'Analysis/SpecialFunctions/ExpDeriv.lean', 'Data/Finsupp/Single.lean',
    'LinearAlgebra/Finsupp/LinearCombination.lean', 'MeasureTheory/Function/L2Space.lean']]
files += [out / 'mission_resume_20261016/LIVE_R47_R8_HANDOFF_20261016T181527_773885Z_81c3e154_RECEIPT.json',
    out / 'mission_review_20261016/R46_FOCK_STRESS_REVIEW_R1.json']

report = {
    'schema': 'iald-lean-candidate/v1', 'status': 'DECLARADO_UNCOMPILED',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actor': actor, 'reference': pin(ref), 'mission_receipt': p['receipt'],
    'projection_sha256': p['projection_sha256'], 'projection_chars': p['actual_chars'],
    'handle': 'r47-r8-fock-charge-construction', 'sources': source_records,
    'chain': [
        'A mixed H1 inner product with the actual strong boost derivative is integrable; only the right representative is differentiated.',
        'The existing transverse polarization and Bochner Jacobian transport inner(h,d(k)) to two mixed Schwartz line-derivative integrals.',
        'oneParticleBoostPair is defined by deriv of the actual B0 matrix element; differentiability on the AxisCompact core is proved from the existing strong H1 derivative.',
        'The exact gamma_exponential and exponential_inner identities give exp(inner(h,k))*oneParticleBoostPair(h,k) as the derivative of the actual Fock matrix element.',
        'The unique regularCoefficients give the actual finite sum of all mixed matrix elements, including off-diagonal terms.',
        'A support-restricted finite-sum differentiation theorem proves the matrix-element derivative when the right coefficient support is AxisCompact.',
        'VF(-s)=VF(s).symm and conjugate symmetry force the diagonal derivative real part to vanish, yielding HasBoostEnergy VF on the complete finite sum.'
    ],
    'domain': {
        'unchanged_objects': ['H1', 'orbitalMeasure 0', 'B0', 'F1Rede.BosonicFock.F',
            'BosonicFockGroupActions.VF', 'regularFockDomain', 'regularCoefficients'],
        'named_core': 'AxisCompactFock psi := forall h in (regularCoefficients psi).support, AxisCompactProfile h.val',
        'scope': 'No differentiability is asserted for every StrongRegularProfile. The core is inside the existing regularFockDomain; no replacement Fock or new tensor is defined.',
        'remaining': ['Prove the named core contains the vacuum and is invariant under the existing translations.',
            'Prove density/nontriviality of the named core in the same Fock, with appropriate regularity for the full certificate.']
    },
    'final_statement': 'axisCompact_regularFock_hasBoostEnergy (psi : regularFockDomain) (hpsi : AxisCompactFock psi) : HasBoostEnergy VF psi.val (regularFockBoostPair psi psi).im',
    'mixed_stress_next_statement': '''∀ (h k : H1), AxisCompactProfile h → AxisCompactProfile k →
  (∫ x : NullFourierSpace, (x 0 : ℂ) *
    (unitaryFourierCoherentStress h k 0 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierCoherentStress h k 0 1 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierCoherentStress h k 1 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierCoherentStress h k 1 1 (nullPlanePoint (x 0) (nullFourierScreen x))))
  = -Complex.I * coherentBoostPair h k''',
    'next_route': 'First prove weighted integrability and the displayed mixed coherent null-stress identity using the existing same-sign cancellation and mixed weighted Parseval. Then commute the finiteKernel sums and the integral and identify the real diagonal with Im(regularFockBoostPair).',
    'premises': 'Final energy theorem assumes only membership in the explicit AxisCompact coefficient core. Neither HasDerivAt nor a target charge/stress equality is supplied as a hypothesis.',
    'not_claimed': ['Compilation or independent acceptance', 'Strong vector derivative in Fock',
        'Mixed Fock stress moment equality', 'Full charge_link', 'Nonzero modular energy witness',
        'Full MaxwellCertificate', 'Complete R8', 'Gate change'],
    'build_performed_by_author': False, 'pins': [pin(f) for f in files],
    'pin_coverage': 'Consulted direct suppliers, pinned mathlib APIs, exact handoff, prior independent Fock stress review. Not transitive build custody. The R5 import is the parent repair candidate pending its own build status.'
}
dst = base / 'COMPACT_FOCK_BOOST_CANDIDATE_R47.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = dst.with_suffix('.json.tmp_r47')
with tmp.open('xb') as f:
    f.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dst)
print(json.dumps({'sources': source_records, 'manifest': pin(dst),
    'pins': len(files), 'revision': p['receipt']['revision']}, ensure_ascii=False))
