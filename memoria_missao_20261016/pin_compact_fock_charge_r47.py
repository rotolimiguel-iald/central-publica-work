from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib = kernel / '.lake/packages/mathlib/Mathlib'
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind': 'agent', 'id': 'codex-r8-nullplane-charge-adapter'}


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def checked_supplier(name):
    source = base / name
    matches = []
    for attempt_source in sorted((out / 'orbital_rotation/attempts').glob('*/' + name)):
        receipt_path = attempt_source.parent / 'RECEIPT.json'
        if not receipt_path.is_file():
            continue
        receipt = json.loads(receipt_path.read_text(encoding='utf-8-sig'))
        if receipt.get('exit_code') != 0:
            continue
        if attempt_source.read_bytes() != source.read_bytes():
            continue
        assert receipt['source']['sha256'] == pin(source)['sha256']
        axioms_path = attempt_source.parent / 'AXIOMS.txt'
        axioms = axioms_path.read_text(encoding='utf-8')
        lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', axioms)
        assert lists and 'sorryAx' not in axioms
        assert all(set(x.strip() for x in row.split(',')) <=
                   {'propext', 'Classical.choice', 'Quot.sound'} for row in lists)
        assert receipt['readonly_dependencies_unchanged']
        assert receipt['dependency_cache_unchanged']
        matches.append({'source': pin(source), 'receipt': pin(receipt_path),
            'axioms': pin(axioms_path), 'exit_code': receipt['exit_code'],
            'seconds': receipt['seconds'], 'axiom_lists': len(lists),
            'only_standard_trio': True, 'attempt_source_matches': True,
            'dependency_immutability_reported_by_build': True})
    assert matches, 'No matching green build: ' + name
    return matches[-1]


suppliers = [checked_supplier(name) for name in [
    'CoherentNullStressMomentR3.lean', 'CompactFockNullStressMomentR4.lean',
    'CalibratedFockStressDomainBridgeR1.lean']]
source = base / 'CompactFockNullPlaneChargeR1.lean'
source_text = source.read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s', source_text, re.M)
source_record = {**pin(source), 'lines': len(source_text.splitlines()),
    'public_theorems': len(re.findall(r'^(?:@\[[^\n]*\]\s*)?theorem ', source_text, re.M)),
    'private_theorems': len(re.findall(r'^private theorem ', source_text, re.M)),
    'print_axioms': len(re.findall(r'^#print axioms ', source_text, re.M))}
files = [base / name for name in [
    'MaxwellNullSchwartzConsumerR2.lean', 'MaxwellNullPlaneWaveR2.lean',
    'RegularFockMaxwellCalibratedR1.lean', 'UnitaryFourierFockStressR1.lean',
    'UnitaryFourierStressTensorR2.lean', 'CompactFockBoostDerivativeR2.lean',
    'CompactBoostMixedNullMomentR1.lean', 'CompactBoostNullMomentLinkR5.lean',
    'COMPACT_FOCK_NULL_MOMENT_CANDIDATE_R47.json']]
files += [out / name for name in [
    'weyl_net_wiring/CanonicalModularCoreAssemblyR1.lean',
    'weyl_net_wiring/CanonicalWeylAssemblyR5.lean',
    'network_antiunitary/CanonicalFockAntiAssemblyR4.lean',
    'network_reuse/CanonicalFockAssemblyR1.lean',
    'mission_resume_20261016/LIVE_R47_CHARGE_HANDOFF_20261016T184306_330868Z_f29f3936_RECEIPT.json']]
files += [out.parent / 'F1.REDE/fock_construction/BosonicFockGroupActions.lean']
files += [kernel / name for name in [
    'TGLExt/ContratoQG_v31.lean', 'TGLExt/ContratoQG_v31_Teoremas.lean',
    'TGLExt/TheImportedSecondQuantization.lean', 'TGLExt/MaxwellLiteratureBridge.lean']]
files += [mathlib / name for name in [
    'MeasureTheory/Group/Integral.lean', 'MeasureTheory/Group/Measure.lean',
    'MeasureTheory/Group/MeasurableEquiv.lean', 'MeasureTheory/Measure/Prod.lean',
    'MeasureTheory/MeasurableSpace/Embedding.lean',
    'MeasureTheory/Integral/Bochner/Basic.lean',
    'MeasureTheory/Function/L1Space/Integrable.lean',
    'Dynamics/Ergodic/MeasurePreserving.lean']]
pins = [pin(path) for path in files]

request = {'operation': 'project', 'reference': str(ref), 'actor': actor, 'max_chars': 100000}
run = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8',
    r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(request), text=True,
    encoding='utf-8', capture_output=True, check=True)
response = json.loads(run.stdout)
assert response['ok'], response
p = response['result']
report = {
    'schema': 'iald-lean-candidate/v1', 'status': 'DECLARADO_UNCOMPILED',
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actor': actor, 'reference': pin(ref), 'mission_receipt': p['receipt'],
    'projection_sha256': p['projection_sha256'], 'projection_chars': p['actual_chars'],
    'handle': 'r47-nullplane-charge-adapter', 'source': source_record,
    'chain': [
        'Compose the existing nullCoordinateEquiv with id times screen negation. The product reflection preserves volume by the existing measurePreserving_neg theorem.',
        'The composed coordinates have longitudinal component lambda and nullFourierScreen equal to the original screen variable; the actual nullPlanePoint is lambda*nullDir + screenEmbed.',
        'Expand the contract pairing with nullDir into the 00+01+10+11 tensor components and reuse calibratedStress_eq_unitaryFourierFock for the actual tensor on regularFockDomain.',
        'Transport the real moment integrability to the exact product-coordinate integrand and transport the integral using MeasurePreserving.integral_comp\u0027.',
        'Reuse the compiled finite Fock moment derivative to obtain HasBoostEnergy VF with the exact nullPlaneCharge.',
        'Compose lightH2 for arbitrary explicit KillingNormalization N using modularEnergy_of_boostEnergy. The same certificate has Gamma=gamma, so its boost is VF.',
        'Uniqueness of actual modular derivatives gives k=2*pi*nullPlaneCharge on AxisCompactFock.'
    ],
    'reuse_detail': 'The coordinate transport is the measure-preserving equivalence underlying integral_nullFourierCoordinates. Its real-valued product integral is used directly, without a new Jacobian or replacement coordinates.',
    'final_statement': 'axisCompact_calibrated_modular_charge_link (A : RemainingModularCoreInput D) (N : KillingNormalization) (psi : regularFockDomain) (hpsi : AxisCompactFock psi) (k : Real) (hk : HasModularEnergy (lightDelta A.toCertificate) psi.val k) : k = 2 * Real.pi * nullPlaneCharge (toStress (regularMaxwellCalibratedForm A)).toStressTensorData psi.val',
    'premises': [
        'RemainingModularCoreInput A is an explicit still-uninhabited assembly interface with unresolved trace/PF data; no inhabitant is supplied or asserted.',
        'KillingNormalization N is explicit and arbitrary. This construction does not select a physical clock or discharge the physical normalization requirement.',
        'AxisCompactFock is the existing predicate on the unique coefficients in the same regularFockDomain; no tensor, measure, generator or regular domain is replaced.',
        'The preceding HasBoostEnergy and HasModularEnergy conclusions require no assumed derivative, integrability or charge equality. hk in the uniqueness theorem only identifies another energy with the independently constructed one.'
    ],
    'remaining': [
        'Compile this candidate and independently review the final statements and dependency custody.',
        'Construct the named invariant smooth certificate domain, with vacuum, inclusion, density and translation/boost invariance as required; this file only proves charge on its AxisCompact coefficient predicate.',
        'Discharge full Regular conditions and construct the normalized nonzero modular-energy witness in the same domain.',
        'Complete the outstanding assembly data and all other full R8 obligations; no complete MaxwellCertificate or acceptance is claimed.'
    ],
    'not_claimed': ['Compilation of this candidate', 'Independent acceptance',
        'Full MaxwellCertificate', 'Nonzero modular energy witness', 'Physical clock selection',
        'Satisfied R8', 'Gate change'],
    'build_performed_by_author': False, 'checked_suppliers': suppliers, 'pins': pins,
    'pin_coverage': 'Source, direct consulted suppliers/mathlib APIs, exact handoff and checked build receipt/axiom output of the three immediate suppliers. Not a transitive build custody.',
    'provenance_script': pin(Path(__file__))
}
dst = base / 'COMPACT_FOCK_NULL_PLANE_CHARGE_CANDIDATE_R47.json'
data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
tmp = dst.with_suffix('.json.tmp_r47')
with tmp.open('xb') as stream:
    stream.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dst)
assert dst.read_bytes() == data
print(json.dumps({'source': source_record, 'manifest': pin(dst),
    'pins': len(pins), 'revision': p['receipt']['revision'],
    'suppliers': [{k: v for k, v in x.items() if k in
        ['source', 'exit_code', 'seconds', 'axiom_lists']} for x in suppliers]}, ensure_ascii=False))
