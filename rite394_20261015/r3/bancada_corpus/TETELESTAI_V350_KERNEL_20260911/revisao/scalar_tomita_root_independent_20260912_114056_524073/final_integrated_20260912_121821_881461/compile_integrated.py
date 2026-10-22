"""Compile every changed formal module and both roots, retaining each Lean invocation."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
records = []


def compile_one(relative):
    source = ROOT / 'kernel' / relative
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    output = ROOT / 'build' / Path(relative).with_suffix('.olean')
    dependencies = [ROOT / 'build' / Path(*name.split('.')).with_suffix('.olean')
                    for line in source.read_text(encoding='utf-8').splitlines()
                    if line.startswith('import ')
                    for name in line[7:].split() if re.fullmatch(r'[\w.]+', name)]
    cache_fresh = output.exists() and all(
        not dependency.exists() or dependency.stat().st_mtime_ns <= output.stat().st_mtime_ns
        for dependency in dependencies)
    output_digest = hashlib.sha256(output.read_bytes()).hexdigest() if output.is_file() else None
    for path in sorted((ROOT / 'logs').glob(source.stem + '_*.json'), reverse=True):
        previous = json.loads(path.read_bytes())
        if (previous['source'] == str(source) and previous['sha256'] == digest
                and previous['returncode'] == 0 and previous['output_exists']
                and previous.get('output_sha256') == output_digest and output_digest is not None
                and cache_fresh):
            print(json.dumps({'module': relative, 'returncode': 0, 'reused_verified_log': str(path)}), flush=True)
            return previous
    result = subprocess.run([sys.executable, str(ROOT / 'compile_lean.py'), relative],
                            cwd=ROOT, capture_output=True)
    stdout = result.stdout.decode('utf-8', errors='replace')
    try:
        record = json.loads(stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        print(stdout, flush=True)
        print(result.stderr.decode('utf-8', errors='replace'), flush=True)
        raise
    print(json.dumps({'module': relative, 'returncode': result.returncode,
                      'record': record['timestamp']}, ensure_ascii=False), flush=True)
    if result.returncode:
        print(stdout[:6000], flush=True)
    return record


with ThreadPoolExecutor(max_workers=2) as pool:
    records.extend(pool.map(compile_one, [
        'TGLExt/V350CompressionLimit.lean', 'TGLExt/V350TowerCommutation.lean']))
for relative in ['TGLExt/V350TowerDuality.lean', 'TGLExt/V350ModularCertificate.lean',
                 'TGLExt/V350GateContract.lean', 'TGLExt/V350WedgeModularData.lean',
                 'TGLExt/V350L2OperatorLift.lean', 'TGLExt/V350L2Translation.lean',
                 'TGLExt/V350L2StrongContinuity.lean', 'TGLExt/V350RegularTowerRepresentation.lean',
                 'TGLExt/V350RegularGeneratedAlgebra.lean',
                 'TGLExt/V350L2CharacterMultiplier.lean',
                 'TGLExt/V350L2BoundedStrongContinuity.lean',
                 'TGLExt/V350GeneratedEquivariance.lean', 'TGLExt/V350RegularDualAction.lean',
                 'TGLExt/V350RegularTopology.lean',
                 'TGLExt/V350L2Order.lean', 'TGLExt/V350RegularNormality.lean',
                 'TGLExt/V350CoreContractCounterexample.lean',
                 'TGLExt/V350StrongOperatorIntegral.lean', 'TGLExt/V350DualWeightCuts.lean',
                 'TGLExt/V350DualWeightForm.lean', 'TGLExt/V350DualWeightExhaustion.lean',
                 'TGLExt/V350DualQuadraticLaws.lean', 'TGLExt/V350DualClosedForm.lean',
                 'TGLExt/V350DualFormTransport.lean', 'TGLExt/V350DualFormFaithfulness.lean',
                 'TGLExt/V350DualCutNormality.lean', 'TGLExt/V350DualFormNormality.lean',
                 'TGLExt/V350PositiveResolvent.lean', 'TGLExt/V350DualResolvent.lean',
                 'TGLExt/V350DualVariational.lean', 'TGLExt/V350DualFormSupport.lean',
                 'TGLExt/V350ResolventGraph.lean', 'TGLExt/V350DualSupportOperator.lean',
                 'TGLExt/V350DualEnergyOnResolvent.lean', 'TGLExt/V350PartialOperatorSquare.lean',
                 'TGLExt/V350ResolventSquareRoot.lean', 'TGLExt/V350DualSquareRoot.lean',
                 'TGLExt/V350DualSquareRootFormBound.lean', 'TGLExt/V350DualFormVariationalBound.lean',
                 'TGLExt/V350DualFormRepresentation.lean',
                 'TGLExt/V350FormMinimizerUniqueness.lean',
                 'TGLExt/V350DualResolventFixed.lean', 'TGLExt/V350DualFixedCore.lean',
                 'TGLExt/V350ResolventGraphTransport.lean', 'TGLExt/V350DualSupportTransport.lean',
                 'TGLExt/V350DualFixedFormAffiliation.lean',
                 'TGLExt/V350PositiveFormCone.lean', 'TGLExt/V350DualFixedWeightLaws.lean',
                 'TGLExt/V350RegularApproximation.lean',
                 'TGLExt/V350FourierL1L2.lean',
                 'TGLExt/V350RegularFiniteWeight.lean',
                 'TGLExt/V350DualSemifiniteIdeal.lean',
                 'TGLExt/V350BoundedDualValues.lean',
                 'TGLExt/V350BoundedFiniteSquares.lean',
                 'TGLExt/V350FixedCoreShiftCommutation.lean',
                 'TGLExt/V350FourierUniqueness.lean',
                 'TGLExt/V350CharacterLocality.lean',
                 'TGLExt/V350L2MeasurableCut.lean',
                 'TGLExt/V350FixedCoreLocality.lean',
                 'TGLExt/V350UnitIntervalProjection.lean',
                 'TGLExt/V350TranslationCorrelation.lean',
                 'TGLExt/V350UnitIntervalShiftProjection.lean',
                 'TGLExt/V350ConstantFibreCandidate.lean',
                 'TGLExt/V350L2CutIntegral.lean',
                 'TGLExt/V350ZeroFromTranslatedCuts.lean',
                 'TGLExt/V350ConstantFibreIdentification.lean',
                 'TGLExt/V350StrongOperatorField.lean',
                 'TGLExt/V350OperatorFieldFaithfulness.lean',
                 'TGLExt/V350TwistedCommutantField.lean',
                 'TGLExt/V350RegularCoreCommutant.lean',
                 'TGLExt/V350FixedCoreBaseIdentification.lean',
                 'TGLExt/V350FixedBaseEquivalence.lean',
                 'TGLExt/V350BoundedBaseDualValues.lean',
                 'TGLExt/V350ScalarDualWeightFaithfulness.lean',
                 'TGLExt/V350ScalarDualWeight.lean',
                 'TGLExt/V350ScalarModularInvariance.lean',
                 'TGLExt/V350RegularScalarWeightCertificate.lean',
                 'TGLExt/V350ContractionAdjointLimit.lean',
                 'TGLExt/V350StrongBoundedApplication.lean',
                 'TGLExt/V350FiniteDualStarCore.lean',
                 'TGLExt/V350ScalarGNSOrbit.lean',
                 'TGLExt/V350ScalarGNSLinear.lean',
                 'TGLExt/V350ScalarGNSAction.lean',
                 'TGLExt/V350OperatorFieldAlgebra.lean',
                 'TGLExt/V350ScalarGNSCompletion.lean',
                 'TGLExt/V350DualOrbitRepresentation.lean',
                 'TGLExt/V350ReducingStarRepresentation.lean',
                 'TGLExt/V350ScalarGNSRepresentation.lean',
                 'TGLExt/V350DualOrbitStrongLimits.lean',
                 'TGLExt/V350ScalarGNSStarApproximation.lean',
                 'TGLExt/V350ScalarGNSStarDensity.lean',
                 'TGLExt/V350ScalarTomitaGraph.lean',
                 'TGLExt/V350ScalarGNSStrongContinuity.lean',
                 'TGLExt/V350ScalarGNSNormality.lean',
                 'TGLExt/V350DualCutLinearMap.lean',
                 'TGLExt/V350ScalarBoundedCuts.lean',
                 'TGLExt/V350ScalarCutNormality.lean',
                 'TGLExt/V350ScalarGNSCutMaps.lean',
                 'TGLExt/V350ScalarGNSCutNorm.lean',
                 'TGLExt/V350ScalarCutVacuum.lean',
                 'TGLExt/V350ScalarCutCyclicSpace.lean',
                 'TGLExt/V350ScalarCutVectorFunctional.lean',
                 'TGLExt/V350ScalarCutGNSProperties.lean',
                 'TGLExt/V350L2PositiveMultiplier.lean',
                 'TGLExt/V350L2GaussianProfile.lean',
                 'TGLExt/V350FibreVonNeumann.lean',
                 'TGLExt/V350ScalarGaussianVacuum.lean',
                 'TGLExt/V350SeparatingCyclicCommutant.lean',
                 'TGLExt/V350DualOrbitVonNeumann.lean',
                 'TGLExt/V350ScalarGaussianGNSMap.lean',
                 'TGLExt/V350VectorTomitaClosability.lean',
                 'TGLExt/V350ScalarGaussianClosureTransport.lean',
                 'TGLExt/V350ScalarClosedTomita.lean',
                 'TGLExt/V350ScalarTomitaStandardSubspace.lean',
                 'TGLExt/V350AntilinearAdjointGraph.lean',
                 'TGLExt/V350ScalarTomitaAdjoint.lean',
                 'TGLExt/V350AntilinearComposition.lean',
                 'TGLExt/V350ScalarTomitaSquare.lean',
                 'TGLExt/V350ClosedAntilinearResolvent.lean',
                 'TGLExt/V350PositiveSurjectiveResolvent.lean',
                 'TGLExt/V350ScalarTomitaSelfAdjoint.lean',
                 'TGLExt/V350PartialPositiveResolvent.lean',
                 'TGLExt/V350ScalarTomitaResolvent.lean',
                 'TGLExt/V350ScalarTomitaPositiveRoot.lean',
                 'TGLExt/V350PartialSquareEnergy.lean',
                 'TGLExt/V350ScalarTomitaRootEnergy.lean',
                 'TGLExt.lean', 'TGL/Audit.lean']:
    if any(r['returncode'] for r in records):
        break
    records.append(compile_one(relative))
integration = json.loads((ROOT / 'integration.json').read_bytes())
expected = set(integration['added_kernel_files'] + integration['updated_kernel_files'])
observed = {Path(r['source']).relative_to(ROOT / 'kernel').as_posix() for r in records}
valid = observed == expected and all(r['returncode'] == 0 for r in records)
for record in records:
    assert hashlib.sha256(Path(record['source']).read_bytes()).hexdigest() == record['sha256']
    if record['returncode'] == 0:
        output = ROOT / 'build' / Path(record['source']).relative_to(ROOT / 'kernel').with_suffix('.olean')
        assert hashlib.sha256(output.read_bytes()).hexdigest() == record['output_sha256']
report = {'mode': 'INCREMENTAL_LEAN_BUILD_WITH_PINNED_V350_PROJECT_ARTIFACTS',
          'incremental_build_ok': valid, 'full_monolithic_runtime_run': False,
          'records': records}
target = ROOT / 'integrated_compile.json'
if target.exists():
    before = target.read_bytes()
    backup = target.with_name(target.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(before)
    assert backup.read_bytes() == before
temporary = target.with_suffix('.json.tmp')
temporary.write_text(json.dumps(report, indent=2), encoding='utf-8')
assert temporary.stat().st_size > 0
temporary.replace(target)
print(json.dumps({'incremental_build_ok': valid, 'compiled_modules': len(records)}), flush=True)
sys.exit(0 if valid else 1)
