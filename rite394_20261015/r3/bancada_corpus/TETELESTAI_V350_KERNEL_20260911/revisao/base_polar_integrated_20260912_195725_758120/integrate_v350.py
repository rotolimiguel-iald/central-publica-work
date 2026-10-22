"""Integrate verified tower proofs in the isolated, single-file program; never touch originals."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def write_atomic(path, raw):
    assert path.resolve().is_relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == raw:
        return
    if path.exists():
        stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        backup = path.with_name(path.name + '.bak_' + stamp)
        before = path.read_bytes()
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
    temporary.replace(path)


original = ROOT / 'fontes' / 'um_v350_original.py'
raw = original.read_bytes()
text = raw.decode('utf-8')
tree = ast.parse(text)
assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES'
                          for t in n.targets))
embedded = ast.literal_eval(assignment.value)
new = {}
module_names = ['CompressionLimit', 'TowerCommutation', 'TowerDuality', 'ModularCertificate', 'WedgeModularData',
                'L2OperatorLift', 'L2Translation', 'L2StrongContinuity',
                'RegularTowerRepresentation', 'RegularGeneratedAlgebra',
                'L2CharacterMultiplier', 'L2BoundedStrongContinuity',
                'GeneratedEquivariance', 'RegularDualAction', 'RegularTopology',
                'L2Order', 'RegularNormality', 'CoreContractCounterexample',
                'StrongOperatorIntegral', 'DualWeightCuts', 'DualWeightForm', 'DualWeightExhaustion',
                'DualQuadraticLaws', 'DualClosedForm', 'DualFormTransport', 'DualFormFaithfulness',
                'DualCutNormality', 'DualFormNormality', 'PositiveResolvent', 'DualResolvent',
                'DualVariational', 'DualFormSupport', 'ResolventGraph', 'DualSupportOperator',
                'DualEnergyOnResolvent', 'PartialOperatorSquare', 'ResolventSquareRoot', 'DualSquareRoot',
                'DualSquareRootFormBound', 'DualFormVariationalBound', 'DualFormRepresentation',
                'FormMinimizerUniqueness', 'DualResolventFixed', 'DualFixedCore',
                'ResolventGraphTransport', 'DualSupportTransport', 'DualFixedFormAffiliation', 'PositiveFormCone', 'DualFixedWeightLaws', 'RegularApproximation', 'FourierL1L2', 'RegularFiniteWeight', 'DualSemifiniteIdeal', 'BoundedDualValues', 'BoundedFiniteSquares', 'FixedCoreShiftCommutation', 'FourierUniqueness', 'CharacterLocality', 'L2MeasurableCut', 'FixedCoreLocality', 'UnitIntervalProjection', 'TranslationCorrelation', 'UnitIntervalShiftProjection', 'ConstantFibreCandidate', 'L2CutIntegral', 'ZeroFromTranslatedCuts', 'ConstantFibreIdentification', 'StrongOperatorField', 'OperatorFieldFaithfulness', 'TwistedCommutantField', 'RegularCoreCommutant', 'FixedCoreBaseIdentification', 'FixedBaseEquivalence', 'BoundedBaseDualValues', 'ScalarDualWeightFaithfulness', 'ScalarDualWeight', 'ScalarModularInvariance', 'RegularScalarWeightCertificate', 'ContractionAdjointLimit', 'StrongBoundedApplication', 'FiniteDualStarCore', 'ScalarGNSOrbit', 'ScalarGNSLinear', 'ScalarGNSAction', 'OperatorFieldAlgebra', 'ScalarGNSCompletion', 'DualOrbitRepresentation', 'ReducingStarRepresentation', 'ScalarGNSRepresentation', 'DualOrbitStrongLimits', 'ScalarGNSStarApproximation', 'ScalarGNSStarDensity', 'ScalarTomitaGraph', 'ScalarGNSStrongContinuity', 'ScalarGNSNormality', 'DualCutLinearMap', 'ScalarBoundedCuts', 'ScalarCutNormality', 'ScalarGNSCutMaps', 'ScalarGNSCutNorm']
tomita_batch = ['ScalarCutVacuum', 'ScalarCutCyclicSpace', 'ScalarCutVectorFunctional',
                'ScalarCutGNSProperties', 'L2PositiveMultiplier', 'L2GaussianProfile',
                'FibreVonNeumann', 'ScalarGaussianVacuum', 'SeparatingCyclicCommutant',
                'DualOrbitVonNeumann', 'ScalarGaussianGNSMap', 'VectorTomitaClosability',
                'ScalarGaussianClosureTransport', 'ScalarClosedTomita',
                'ScalarTomitaStandardSubspace', 'AntilinearAdjointGraph',
                'ScalarTomitaAdjoint', 'AntilinearComposition', 'ScalarTomitaSquare',
                'ClosedAntilinearResolvent', 'PositiveSurjectiveResolvent',
                'ScalarTomitaSelfAdjoint', 'PartialPositiveResolvent',
                'ScalarTomitaResolvent', 'ScalarTomitaPositiveRoot',
                'PartialSquareEnergy', 'ScalarTomitaRootEnergy',
                'RealGraphCore', 'ScalarTomitaGraphCore', 'PartialSquareGraphCore', 'GraphCoreNormTransfer', 'ScalarTomitaRootGraphCore', 'ScalarTomitaRootDomain', 'PartialSelfadjointRange', 'DenseAntilinearExtension', 'ScalarTomitaPolarFactor',
                'ScalarTomitaResolventFlip', 'ScalarTomitaPolarResolvent', 'AntiunitaryPositiveConjugation', 'ScalarTomitaPolarInvolution',
                'ScalarWeightDomain', 'ScalarWeightOrbit', 'ShiftCharacterAverage', 'ScalarRightAverage', 'ScalarWeightCompletion', 'ScalarWeightAction', 'ScalarWeightSandwich', 'ScalarWeightStarCore', 'ScalarWeightTomitaIdentification',
                'LocalRightModularTransport', 'HomogeneousCommutantTransport', 'ScalarHomogeneousRightOrbit', 'HomogeneousRightData', 'ScalarHomogeneousRightGNS',
                'ScalarRightStarGraph', 'ScalarRightClosedTomita', 'ScalarRightTomitaAdjoint',
                'HomogeneousRightSquareDomain', 'MatrixUnitRightSquare',
                'ScalarRegularRightGNS', 'ScalarRegularRightTomita', 'ScalarRegularRightSquare',
                'ScalarRegularRightPolar', 'ScalarRegularPolarCommutation', 'ScalarRegularRightContinuity',
                'PositiveRootIntertwining', 'ScaledPositiveResolvent', 'ScaledResolventRoots', 'ScaledRootGraphTransport', 'MatrixUnitResolventScaling', 'MatrixUnitRootScaling', 'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation',
                'LevelExpectationUniformBound', 'LevelExpectationStrongLimit', 'LocalBasePolarCommutation', 'BasePolarStrongLimit']
module_names.extend(tomita_batch)
for name in module_names:
    source = (ROOT / 'kernel' / 'TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    for dependency in module_names:
        source = source.replace('import TGLV350.' + dependency,
                                'import TGLExt.V350' + dependency)
    new['TGLExt/V350' + name + '.lean'] = source

new['TGLExt/V350GateContract.lean'] = '''import TGLExt.V350ModularCertificate

set_option autoImplicit false
namespace TGLExt.V350Gate
noncomputable section

/-- Exact type bridges, independent of the names read by the Python parser. -/
def checkedConverse : (P : SiteProfile) → ConverseClauseContract P :=
  qgConverse_JMJ_contains_commutant
def checkedModular : ModularRealizationCertificate :=
  qgFrontier_modularRealization
def checkedActIII : ModularRealizationCertificate :=
  qgPrice_towerActIII_inhabitantConstructed

#print axioms checkedConverse
#print axioms checkedModular
#print axioms checkedActIII
end
end TGLExt.V350Gate
'''
root_import = ('\nimport TGLExt.V350GateContract\nimport TGLExt.V350WedgeModularData\n'
               'import TGLExt.V350RegularGeneratedAlgebra\nimport TGLExt.V350RegularDualAction\n'
               'import TGLExt.V350L2BoundedStrongContinuity\nimport TGLExt.V350RegularTopology\n'
               'import TGLExt.V350RegularNormality\nimport TGLExt.V350CoreContractCounterexample\n'
               'import TGLExt.V350DualWeightExhaustion\nimport TGLExt.V350DualClosedForm\n'
               'import TGLExt.V350DualFormTransport\nimport TGLExt.V350DualFormFaithfulness\n'
               'import TGLExt.V350DualCutNormality\nimport TGLExt.V350DualFormNormality\n'
               'import TGLExt.V350PositiveResolvent\nimport TGLExt.V350DualResolvent\n'
               'import TGLExt.V350DualVariational\nimport TGLExt.V350DualFormSupport\n'
               'import TGLExt.V350ResolventGraph\nimport TGLExt.V350DualSupportOperator\n'
               'import TGLExt.V350DualEnergyOnResolvent\nimport TGLExt.V350PartialOperatorSquare\n'
               'import TGLExt.V350ResolventSquareRoot\nimport TGLExt.V350DualSquareRoot\n'
               'import TGLExt.V350DualSquareRootFormBound\nimport TGLExt.V350DualFormVariationalBound\n'
               'import TGLExt.V350DualFormRepresentation\n'
               'import TGLExt.V350FormMinimizerUniqueness\nimport TGLExt.V350DualResolventFixed\n'
               'import TGLExt.V350DualFixedCore\n'
               'import TGLExt.V350ResolventGraphTransport\nimport TGLExt.V350DualSupportTransport\n'
               'import TGLExt.V350DualFixedFormAffiliation\n'
               'import TGLExt.V350PositiveFormCone\nimport TGLExt.V350DualFixedWeightLaws\n'
               'import TGLExt.V350RegularApproximation\n'
               'import TGLExt.V350FourierL1L2\n'
               'import TGLExt.V350RegularFiniteWeight\n'
               'import TGLExt.V350DualSemifiniteIdeal\n'
               'import TGLExt.V350BoundedDualValues\n'
               'import TGLExt.V350BoundedFiniteSquares\n'
               'import TGLExt.V350FixedCoreShiftCommutation\n'
               'import TGLExt.V350FourierUniqueness\n'
               'import TGLExt.V350CharacterLocality\n'
               'import TGLExt.V350L2MeasurableCut\n'
               'import TGLExt.V350FixedCoreLocality\n'
               'import TGLExt.V350UnitIntervalProjection\n'
               'import TGLExt.V350TranslationCorrelation\n'
               'import TGLExt.V350UnitIntervalShiftProjection\n'
               'import TGLExt.V350ConstantFibreCandidate\n'
               'import TGLExt.V350L2CutIntegral\n'
               'import TGLExt.V350ZeroFromTranslatedCuts\n'
               'import TGLExt.V350ConstantFibreIdentification\n'
               'import TGLExt.V350StrongOperatorField\n'
               'import TGLExt.V350OperatorFieldFaithfulness\n'
               'import TGLExt.V350TwistedCommutantField\n'
               'import TGLExt.V350RegularCoreCommutant\n'
               'import TGLExt.V350FixedCoreBaseIdentification\n'
               'import TGLExt.V350FixedBaseEquivalence\n'
               'import TGLExt.V350BoundedBaseDualValues\n'
               'import TGLExt.V350ScalarDualWeightFaithfulness\n'
               'import TGLExt.V350ScalarDualWeight\n'
               'import TGLExt.V350ScalarModularInvariance\n'
               'import TGLExt.V350RegularScalarWeightCertificate\n'
               'import TGLExt.V350ContractionAdjointLimit\n'
               'import TGLExt.V350StrongBoundedApplication\n'
               'import TGLExt.V350FiniteDualStarCore\n'
               'import TGLExt.V350ScalarGNSOrbit\n'
               'import TGLExt.V350ScalarGNSLinear\n'
               'import TGLExt.V350ScalarGNSAction\n'
               'import TGLExt.V350OperatorFieldAlgebra\n'
               'import TGLExt.V350ScalarGNSCompletion\n'
               'import TGLExt.V350DualOrbitRepresentation\n'
               'import TGLExt.V350ReducingStarRepresentation\n'
               'import TGLExt.V350ScalarGNSRepresentation\n'
               'import TGLExt.V350DualOrbitStrongLimits\n'
               'import TGLExt.V350ScalarGNSStarApproximation\n'
               'import TGLExt.V350ScalarGNSStarDensity\n'
               'import TGLExt.V350ScalarTomitaGraph\n'
               'import TGLExt.V350ScalarGNSStrongContinuity\n'
               'import TGLExt.V350ScalarGNSNormality\n'
               'import TGLExt.V350DualCutLinearMap\n'
               'import TGLExt.V350ScalarBoundedCuts\n'
               'import TGLExt.V350ScalarCutNormality\n'
               'import TGLExt.V350ScalarGNSCutMaps\n'
               'import TGLExt.V350ScalarGNSCutNorm\n')
root_import += ''.join('import TGLExt.V350' + name + '\n' for name in tomita_batch)
new['TGLExt.lean'] = embedded['TGLExt.lean'].rstrip() + root_import
audit = embedded['TGL/Audit.lean']
new['TGL/Audit.lean'] = root_import + audit.rstrip() + '''

-- 2026-09-11, isolated v350 extension: closed modular certificate, product tower only.
#print axioms TGLExt.qgConverse_JMJ_contains_commutant
#print axioms TGLExt.qgFrontier_modularRealization
#print axioms TGLExt.qgPrice_towerActIII_inhabitantConstructed
#print axioms TGLExt.V350Gate.checkedConverse
#print axioms TGLExt.V350Gate.checkedModular
#print axioms TGLExt.V350Gate.checkedActIII
#print axioms TGLExt.V350Continuous.towerAntiunitary
#print axioms TGLExt.V350Continuous.factorFlow
#print axioms TGLExt.V350Continuous.towerWedgeData
#print axioms TGLExt.V350Continuous.same_conjugation

-- Regular continuous representation; no canonical trace or core flag is asserted.
#print axioms TGLV350.Regular.fibreRepresentation
#print axioms TGLV350.Regular.fibre_injective
#print axioms TGLV350.Regular.shift_mul
#print axioms TGLV350.Regular.shift_star
#print axioms TGLV350.Regular.shift_commutes_fibre
#print axioms TGLV350.Regular.shift_strongly_continuous
#print axioms TGLV350.Regular.fibre_jointly_continuous
#print axioms TGLV350.Regular.regular_mul
#print axioms TGLV350.Regular.regular_unitary
#print axioms TGLV350.Regular.regular_covariance_on_factor
#print axioms TGLV350.Regular.regular_strongly_continuous
#print axioms TGLV350.Regular.regularCoreAlgebra
#print axioms TGLV350.Regular.regularCoreEmbedding_injective
#print axioms TGLV350.Regular.regularCore_minimal

-- Dual automorphisms on the whole regular algebra and bounded strong limits.
-- These declarations do not supply a canonical trace or discharge Three Locks.
#print axioms TGLV350.Regular.characterMultiplier_unitary
#print axioms TGLV350.Regular.characterMultiplier_commutes_fibre
#print axioms TGLV350.Regular.characterMultiplier_weyl
#print axioms TGLV350.Regular.characterMultiplier_strongly_continuous
#print axioms TGLV350.Regular.generated_transport
#print axioms TGLV350.Regular.generatedAutomorphism
#print axioms TGLV350.Regular.regularDualAction
#print axioms TGLV350.Regular.regularDualAction_zero
#print axioms TGLV350.Regular.regularDualAction_add
#print axioms TGLV350.Regular.regularDualAction_fixes_embedding
#print axioms TGLV350.Regular.dualAmbient_regular
#print axioms TGLV350.Regular.regularDualAction_strongly_continuous
#print axioms TGLV350.Regular.dualAmbient_preserves_strong_continuity
#print axioms TGLV350.Regular.fibre_norm_le
#print axioms TGLV350.Regular.fibre_bounded_jointly_continuous
#print axioms TGLV350.Regular.fibre_bounded_strongly_continuous
#print axioms TGLV350.Regular.fibre_tendsto_of_uniformly_bounded
#print axioms TGLV350.Regular.vonNeumann_wot_closed
#print axioms TGLV350.Regular.regularCore_wot_closed

-- Order normality of the actual inclusion; no trace or core flag follows from this alone.
#print axioms TGLV350.Regular.fibre_nonneg_iff
#print axioms TGLV350.Regular.fibre_le_iff
#print axioms TGLV350.Regular.isLUB_fibre_of_monotone_strong_limit
#print axioms TGLV350.Regular.fibre_preserves_positive_isLUB
#print axioms TGLV350.Regular.strong_tendsto_wot
#print axioms TGLV350.Regular.vonNeumann_mem_of_strong_limit
#print axioms TGLV350.Regular.vonNeumann_isLUB_of_coe_isLUB
#print axioms TGLV350.Regular.vonNeumann_exists_positive_isLUB
#print axioms TGLV350.Regular.vonNeumann_isLUB_coe
#print axioms TGLV350.Regular.vonNeumann_exists_positive_isLUB_of_bddAbove
#print axioms TGLV350.Regular.regularCoreEmbedding_coe
#print axioms TGLV350.Regular.regularCoreEmbedding_preserves_positive_isLUB
#print axioms TGLV350.Regular.regularCoreEmbedding_preserves_positive_directed_isLUB

-- A legacy core contract admits zero trace, but this countermodel cannot have Three Locks.
#print axioms TGLV350.ContractAudit.zeroTraceLegacyCore
#print axioms TGLV350.ContractAudit.legacy_contract_accepts_zero_trace
#print axioms TGLV350.ContractAudit.zeroTraceLegacyCore_has_no_threeLocks

-- Strong dual cuts and extended quadratic evaluations, not yet a canonical trace.
#print axioms TGLV350.StrongIntegral.operatorIntegral
#print axioms TGLV350.StrongIntegral.operatorIntegral_norm_le
#print axioms TGLV350.StrongIntegral.operatorIntegral_mem
#print axioms TGLV350.StrongIntegral.inner_operatorIntegral
#print axioms TGLV350.StrongIntegral.operatorIntegral_nonneg
#print axioms TGLV350.StrongIntegral.operatorIntegral_mono_interval
#print axioms TGLV350.Regular.dualIntegralFamily
#print axioms TGLV350.Regular.dualWeightCut_apply
#print axioms TGLV350.Regular.dualWeightCut_norm_le
#print axioms TGLV350.Regular.dualWeightCut_nonneg
#print axioms TGLV350.Regular.dualWeightCut_mono_radius
#print axioms TGLV350.Regular.dualWeightCut_mem
#print axioms TGLV350.Regular.dualWeightCut_fibre
#print axioms TGLV350.Regular.dualWeightCut_one
#print axioms TGLV350.Regular.normalizedDualCut_nonneg
#print axioms TGLV350.Regular.normalizedDualCut_mem
#print axioms TGLV350.Regular.dualQuadraticIntegral_zero
#print axioms TGLV350.Regular.dualQuadraticIntegral_add
#print axioms TGLV350.Regular.dualQuadraticIntegral_dual_invariant
#print axioms TGLV350.Regular.dualWeightCut_quadratic
#print axioms TGLV350.Regular.dualWeightCut_quadratic_le
#print axioms TGLV350.Regular.dualQuadraticIntegral_one
#print axioms TGLV350.Regular.lintegral_eq_iSup_symmetric_cuts
#print axioms TGLV350.Regular.dualQuadraticIntegral_eq_iSup_cuts
#print axioms TGLV350.Regular.dual_unit_cut_supremum_infinite

-- Closed positive forms and finite domains, not a spectral operator or canonical trace.
#print axioms TGLV350.Regular.operatorQuadratic_smul
#print axioms TGLV350.Regular.operatorQuadratic_parallelogram
#print axioms TGLV350.Regular.dualQuadraticIntegral_smul_vector
#print axioms TGLV350.Regular.dualQuadraticIntegral_smul_operator
#print axioms TGLV350.Regular.dualQuadraticIntegral_parallelogram
#print axioms TGLV350.Regular.dualQuadraticIntegral_add_vector_le
#print axioms TGLV350.Regular.dualCutEvaluation_continuous
#print axioms TGLV350.Regular.dualQuadraticIntegral_lowerSemicontinuous
#print axioms TGLV350.Regular.ClosedPositiveForm.finiteDomain
#print axioms TGLV350.Regular.ClosedPositiveForm.isClosed_sublevel
#print axioms TGLV350.Regular.dualClosedPositiveForm
#print axioms TGLV350.Regular.dualClosedPositiveForm_one_domain
#print axioms TGLV350.Regular.dualClosedPositiveForm_zero_domain
#print axioms TGLV350.Regular.dualQuadraticIntegral_commutant_invariant
#print axioms TGLV350.Regular.dualAffiliatedPositiveForm

-- Bimodule and dual transport laws, plus faithfulness of the positive evaluation family.
-- These are not a construction of a canonical scalar trace or its semifinitude.
#print axioms TGLV350.Regular.operatorQuadratic_conjugate
#print axioms TGLV350.Regular.dualQuadraticIntegral_bimodule
#print axioms TGLV350.Regular.base_conjugate_mem
#print axioms TGLV350.Regular.dualBaseConjugatedForm
#print axioms TGLV350.Regular.dualBaseConjugatedForm_value
#print axioms TGLV350.Regular.dualAmbient_commute
#print axioms TGLV350.Regular.dualQuadraticIntegral_transport
#print axioms TGLV350.Regular.dualQuadraticIntegral_vector_dual_invariant
#print axioms TGLV350.Regular.dualFiniteDomain_dual_invariant
#print axioms TGLV350.Regular.dualQuadraticIntegrand_continuous
#print axioms TGLV350.Regular.dualQuadraticIntegral_zero_iff_integrand_zero
#print axioms TGLV350.Regular.dualQuadraticIntegral_zero_implies_apply_zero
#print axioms TGLV350.Regular.dualQuadraticIntegral_faithful
#print axioms TGLV350.Regular.dualQuadraticIntegral_detects_nonzero_positive
#print axioms TGLV350.Regular.dualQuadraticIntegral_mono

-- Normality of extended form evaluations on arbitrary positive directed nets.
-- A base-valued weight, its semifinitude and the canonical scalar trace remain open.
#print axioms TGLV350.Regular.intervalIntegral_tendsto_of_uniform
#print axioms TGLV350.Regular.dualRealQuadratic_continuous
#print axioms TGLV350.Regular.dualRealQuadratic_mono
#print axioms TGLV350.Regular.dualAmbient_tendsto_strong
#print axioms TGLV350.Regular.dualRealQuadratic_uniform_on_compact
#print axioms TGLV350.Regular.dualWeightCut_tendsto_quadratic
#print axioms TGLV350.Regular.dualQuadraticIntegral_of_monotone_strong_limit
#print axioms TGLV350.Regular.dualQuadraticIntegral_preserves_positive_isLUB
#print axioms TGLV350.Regular.dualQuadraticIntegral_preserves_internal_isLUB
#print axioms TGLV350.Regular.regularDualForm_preserves_internal_isLUB

-- Strong resolvent limit in the same core, with a finite-domain energy bound.
-- Spectral representation of the form and the canonical trace remain open.
#print axioms TGLV350.Regular.positiveResolvent_left_inverse
#print axioms TGLV350.Regular.positiveResolvent_right_inverse
#print axioms TGLV350.Regular.positiveResolvent_nonneg
#print axioms TGLV350.Regular.positiveResolvent_le_one
#print axioms TGLV350.Regular.positiveResolvent_antitone
#print axioms TGLV350.Regular.positiveResolvent_injective
#print axioms TGLV350.Regular.positiveResolvent_mem
#print axioms TGLV350.Regular.vonNeumann_antitone_contraction_limit
#print axioms TGLV350.Regular.normalizedDualCut_mono_radius
#print axioms TGLV350.Regular.normalizedDualCut_quadratic
#print axioms TGLV350.Regular.dualQuadraticIntegral_eq_iSup_normalized_cuts
#print axioms TGLV350.Regular.dualCutResolvent_antitone
#print axioms TGLV350.Regular.exists_dualResolvent_limit
#print axioms TGLV350.Regular.positiveResolvent_energy_bound
#print axioms TGLV350.Regular.dualResolvent_limit_energy_bound
#print axioms TGLV350.Regular.dualResolvent_limit_range_finite
#print axioms TGLV350.Regular.dualResolvent_limit_one_eq_zero
#print axioms TGLV350.Regular.dualCutResolvent_zero
#print axioms TGLV350.Regular.dualResolvent_limit_zero_eq_one

-- Variational minimum, actual form support, and a positive self-adjoint graph.
-- The square-root form equality and canonical trace are not yet discharged.
#print axioms TGLV350.Regular.positiveResolvent_energy_identity
#print axioms TGLV350.Regular.positiveResolvent_minimizes_energy
#print axioms TGLV350.Regular.dualEnergy_eq_iSup_cuts
#print axioms TGLV350.Regular.dualResolvent_limit_minimizes_energy
#print axioms TGLV350.Regular.linear_coefficient_zero_of_nonnegative_quadratic
#print axioms TGLV350.Regular.ClosedPositiveForm.zero_minimizer_orthogonal
#print axioms TGLV350.Regular.dualResolvent_kernel_eq_finiteDomain_orthogonal
#print axioms TGLV350.Regular.dualResolvent_range_closure_eq_finiteDomain_closure
#print axioms TGLV350.Regular.resolvent_graph_equation
#print axioms TGLV350.Regular.resolvent_graph_closed
#print axioms TGLV350.Regular.resolvent_graph_domain_dense
#print axioms TGLV350.Regular.resolvent_graph_selfadjoint
#print axioms TGLV350.Regular.resolvent_graph_positive
#print axioms TGLV350.Regular.resolvent_graph_resolvent_equation
#print axioms TGLV350.Regular.dualResolvent_maps_into_support
#print axioms TGLV350.Regular.dualSupportResolvent_apply
#print axioms TGLV350.Regular.dualSupportResolvent_nonneg
#print axioms TGLV350.Regular.dualSupportResolvent_le_one
#print axioms TGLV350.Regular.dualSupportResolvent_injective
#print axioms TGLV350.Regular.dualSupportOperator_closed
#print axioms TGLV350.Regular.dualSupportOperator_dense
#print axioms TGLV350.Regular.dualSupportOperator_selfadjoint
#print axioms TGLV350.Regular.dualSupportOperator_positive
#print axioms TGLV350.Regular.dualSupportOperator_resolvent_equation
#print axioms TGLV350.Regular.exists_dualSupportOperator

-- Finite operator-domain energy, a positive self-adjoint square root, and S^2=T.
-- Equality of the full finite form domain with D(S), and the canonical trace, remain open.
#print axioms TGLV350.Regular.ClosedPositiveForm.minimizer_energy_identity
#print axioms TGLV350.Regular.dualResolvent_limit_energy_identity
#print axioms TGLV350.Regular.dualSupportOperator_inverse_parameter
#print axioms TGLV350.Regular.dualSupportOperator_domain_finite
#print axioms TGLV350.Regular.dualSupportOperator_energy_identity
#print axioms TGLV350.Regular.dualSupportOperator_energy_ennreal
#print axioms TGLV350.Regular.partialOperatorSquare
#print axioms TGLV350.Regular.partialOperatorSquare_domain_iff
#print axioms TGLV350.Regular.partialOperatorSquare_graph_iff
#print axioms TGLV350.Regular.boundedGraph_square_eq_resolvent
#print axioms TGLV350.Regular.positive_sqrt_injective
#print axioms TGLV350.Regular.resolvent_sqrt_pair_commute
#print axioms TGLV350.Regular.resolvent_sqrt_pair_square_sum
#print axioms TGLV350.Regular.resolventSquareRoot_domain
#print axioms TGLV350.Regular.resolventSquareRoot_closed
#print axioms TGLV350.Regular.resolventSquareRoot_dense
#print axioms TGLV350.Regular.resolventSquareRoot_formalAdjoint
#print axioms TGLV350.Regular.resolventSquareRoot_selfadjoint
#print axioms TGLV350.Regular.resolventSquareRoot_positive
#print axioms TGLV350.Regular.resolventSquareRoot_square
#print axioms TGLV350.Regular.boundedPositiveSquareRoot
#print axioms TGLV350.Regular.boundedPositiveSquareRoot_sq
#print axioms TGLV350.Regular.dualSupportSquareRoot_domain
#print axioms TGLV350.Regular.dualSupportSquareRoot_closed
#print axioms TGLV350.Regular.dualSupportSquareRoot_dense
#print axioms TGLV350.Regular.dualSupportSquareRoot_selfadjoint
#print axioms TGLV350.Regular.dualSupportSquareRoot_positive
#print axioms TGLV350.Regular.dualSupportSquareRoot_square
#print axioms TGLV350.Regular.dualSupportSquareRoot_energy_on_operator_domain
#print axioms TGLV350.Regular.exists_dualSupportSquareRoot

-- Full form representation now proved on the same support. The canonical trace remains open.
#print axioms TGLV350.Regular.lsc_le_continuous_of_dense
#print axioms TGLV350.Regular.bounded_graph_form_upper_bound
#print axioms TGLV350.Regular.resolventSquareRoot_form_upper_bound
#print axioms TGLV350.Regular.dualSupportSquareRoot_form_upper_bound
#print axioms TGLV350.Regular.dualSupportSquareRoot_domain_finite
#print axioms TGLV350.Regular.inner_norm_bound_of_variational_bound
#print axioms TGLV350.Regular.exists_preimage_of_inner_bound
#print axioms TGLV350.Regular.dualResolvent_variational_dual_bound
#print axioms TGLV350.Regular.boundedPositiveSquareRoot_energy
#print axioms TGLV350.Regular.resolvent_sqrt_pair_norm_sum
#print axioms TGLV350.Regular.resolventSquareRoot_form_lower_bound
#print axioms TGLV350.Regular.dualSupportSquareRoot_form_lower_bound
#print axioms TGLV350.Regular.dualSupportSquareRoot_domain_iff_finite
#print axioms TGLV350.Regular.dualSupportSquareRoot_form_eq
#print axioms TGLV350.Regular.dualQuadraticIntegral_finite_iff_squareRoot_domain
#print axioms TGLV350.Regular.exists_dualFormRepresentation

-- The same variational resolvent lies in the concrete dual fixed-point algebra.
-- Equality of this algebra with the amplified base and the canonical weight remain open.
#print axioms TGLV350.Regular.ClosedPositiveForm.midpoint_finite_and_bound
#print axioms TGLV350.Regular.norm_midpoint_sub_identity
#print axioms TGLV350.Regular.ClosedPositiveForm.minimizer_unique
#print axioms TGLV350.Regular.ClosedPositiveForm.minimizer_transport
#print axioms TGLV350.Regular.ClosedPositiveForm.resolvent_equivariant
#print axioms TGLV350.Regular.dualResolvent_limit_commutes_character
#print axioms TGLV350.Regular.dualResolvent_limit_dual_fixed
#print axioms TGLV350.Regular.dualResolvent_limit_commutes_unitary_commutant
#print axioms TGLV350.Regular.exists_dualResolvent_fixed
#print axioms TGLV350.Regular.starCommutantAlgebra
#print axioms TGLV350.Regular.dualAmbient_fixed_iff_commutes
#print axioms TGLV350.Regular.dualFixedCore
#print axioms TGLV350.Regular.dualFixedCore_mem_iff
#print axioms TGLV350.Regular.amplified_factor_mem_dualFixedCore
#print axioms TGLV350.Regular.dualResolvent_mem_dualFixedCore
#print axioms TGLV350.Regular.exists_dualFixedFormRepresentation

-- Affiliation of the same extended form with the concrete fixed algebra.
-- This includes the infinite part, but does not identify the fixed algebra with the base.
#print axioms TGLV350.Regular.bounded_graph_transport_of_commute
#print axioms TGLV350.Regular.complement_commutes_of_commute
#print axioms TGLV350.Regular.positive_sqrt_commutes_of_commute
#print axioms TGLV350.Regular.resolvent_graph_transport_of_commute
#print axioms TGLV350.Regular.resolvent_sqrt_graph_transport_of_commute
#print axioms TGLV350.Regular.range_closure_maps_of_commute
#print axioms TGLV350.Regular.dualSupport_maps_of_commute
#print axioms TGLV350.Regular.dualSupportCommutingMap
#print axioms TGLV350.Regular.dualSupportCommutingMap_apply
#print axioms TGLV350.Regular.dualSupportResolvent_commutes_map
#print axioms TGLV350.Regular.dualSupportOperator_graph_transport
#print axioms TGLV350.Regular.dualSupportSquareRoot_graph_transport
#print axioms TGLV350.Regular.selfadjoint_commutes_star_of_commute
#print axioms TGLV350.Regular.graph_transport_iff_of_left_inverse
#print axioms TGLV350.Regular.dualSupportCommutingMap_star_cancel
#print axioms TGLV350.Regular.dualSupportOperator_unitary_graph_iff
#print axioms TGLV350.Regular.dualSupportSquareRoot_unitary_graph_iff
#print axioms TGLV350.Regular.dualQuadraticIntegral_finite_unitary_commuting
#print axioms TGLV350.Regular.dualQuadraticIntegral_unitary_commuting
#print axioms TGLV350.Regular.dualQuadraticIntegral_fixed_commutant_invariant
#print axioms TGLV350.Regular.dualFixedAffiliatedPositiveForm
#print axioms TGLV350.Regular.dualFixedAffiliatedPositiveForm_value

-- Ordered affiliated forms and the faithful normal form-valued weight into F.
-- Base identification, algebraic semifiniteness and the canonical trace remain open.
#print axioms TGLV350.Regular.ClosedPositiveForm.ext
#print axioms TGLV350.Regular.ClosedPositiveForm.zeroForm
#print axioms TGLV350.Regular.ClosedPositiveForm.addForm
#print axioms TGLV350.Regular.ClosedPositiveForm.scaleForm
#print axioms TGLV350.Regular.ClosedPositiveForm.precompose
#print axioms TGLV350.Regular.AffiliatedPositiveForm.ext
#print axioms TGLV350.Regular.AffiliatedPositiveForm.le_iff
#print axioms TGLV350.Regular.AffiliatedPositiveForm.zeroForm
#print axioms TGLV350.Regular.AffiliatedPositiveForm.addForm
#print axioms TGLV350.Regular.AffiliatedPositiveForm.scaleForm
#print axioms TGLV350.Regular.AffiliatedPositiveForm.conjugate
#print axioms TGLV350.Regular.AffiliatedPositiveForm.add_comm
#print axioms TGLV350.Regular.AffiliatedPositiveForm.add_assoc
#print axioms TGLV350.Regular.AffiliatedPositiveForm.zero_add
#print axioms TGLV350.Regular.AffiliatedPositiveForm.scale_laws
#print axioms TGLV350.Regular.AffiliatedPositiveForm.zero_le
#print axioms TGLV350.Regular.AffiliatedPositiveForm.add_mono
#print axioms TGLV350.Regular.AffiliatedPositiveForm.scale_mono
#print axioms TGLV350.Regular.PositiveCoreInput.zero
#print axioms TGLV350.Regular.PositiveCoreInput.add
#print axioms TGLV350.Regular.PositiveCoreInput.scale
#print axioms TGLV350.Regular.PositiveCoreInput.conjugate
#print axioms TGLV350.Regular.dualFixedWeight
#print axioms TGLV350.Regular.dualFixedWeight_value
#print axioms TGLV350.Regular.dualFixedWeight_zero
#print axioms TGLV350.Regular.dualFixedWeight_add
#print axioms TGLV350.Regular.dualFixedWeight_scale
#print axioms TGLV350.Regular.dualQuadraticIntegral_fixed_bimodule
#print axioms TGLV350.Regular.dualFixedWeight_bimodule
#print axioms TGLV350.Regular.dualFixedWeight_mono
#print axioms TGLV350.Regular.dualFixedWeight_faithful
#print axioms TGLV350.Regular.positive_internal_isLUB_nonneg
#print axioms TGLV350.Regular.dualFixedWeight_preserves_internal_isLUB

-- Finite-square left ideal, exact Fourier weight and strong approximation.
-- F=base, the scalar trace and full physical gate remain separate obligations.
#print axioms TGLV350.Regular.regularBundledUnitary
#print axioms TGLV350.Regular.regular_norm_map
#print axioms TGLV350.Regular.regularIntegralFamily
#print axioms TGLV350.Regular.regularAverage
#print axioms TGLV350.Regular.regularAverage_apply
#print axioms TGLV350.Regular.regularAverage_mem
#print axioms TGLV350.Regular.regularAverage_norm_le_one
#print axioms TGLV350.Regular.regularAverage_tendsto_identity
#print axioms TGLV350.Regular.regularAverage_mul_tendsto
#print axioms TGLV350.Regular.dualAmbient_strongIntegral_apply
#print axioms TGLV350.Regular.regularAverage_dual_apply
#print axioms TGLV350.Fourier.fourier_integrable_continuous
#print axioms TGLV350.Fourier.fourier_test_pairing
#print axioms TGLV350.Fourier.fourier_integral_ae_eq_L2
#print axioms TGLV350.Fourier.fourier_integral_memLp_two
#print axioms TGLV350.Fourier.L2_integral_norm_sq
#print axioms TGLV350.Fourier.integral_norm_sq_eq_L2
#print axioms TGLV350.Fourier.fourier_integral_norm_sq
#print axioms TGLV350.Fourier.fourier_integral_lintegral_norm_sq
#print axioms TGLV350.Regular.regularOrbitCut
#print axioms TGLV350.Regular.regularOrbitCut_memLp
#print axioms TGLV350.Regular.regularOrbitCut_integrable
#print axioms TGLV350.Regular.regularOrbitCut_integral_norm_sq
#print axioms TGLV350.Regular.regularAverage_dual_fourier
#print axioms TGLV350.Regular.regularAverage_dual_sq_integrable
#print axioms TGLV350.Regular.regularAverage_dual_integral_norm_sq
#print axioms TGLV350.Regular.dualQuadraticIntegrand_star_mul
#print axioms TGLV350.Regular.regularAverage_dualQuadraticIntegral
#print axioms TGLV350.Regular.regularAverage_dualQuadraticIntegral_lt_top
#print axioms TGLV350.Regular.HasFiniteDualSquare
#print axioms TGLV350.Regular.dualQuadraticIntegral_left_square_le
#print axioms TGLV350.Regular.HasFiniteDualSquare.zero
#print axioms TGLV350.Regular.HasFiniteDualSquare.left_mul
#print axioms TGLV350.Regular.dualSquare_add_le
#print axioms TGLV350.Regular.HasFiniteDualSquare.add
#print axioms TGLV350.Regular.HasFiniteDualSquare.smul
#print axioms TGLV350.Regular.finiteDualLeftIdeal
#print axioms TGLV350.Regular.finiteDualLeftIdeal_left_mul
#print axioms TGLV350.Regular.regularAverage_hasFiniteDualSquare
#print axioms TGLV350.Regular.finiteDualLeftIdeal_strong_approximation

-- Bounded dual values in the same fixed algebra and dense finite-square inputs.
-- The identification F=base and canonical trace remain separate obligations.
#print axioms TGLV350.Regular.selfAdjoint_le_of_quadratic_le
#print axioms TGLV350.Regular.selfAdjoint_eq_of_quadratic_eq
#print axioms TGLV350.Regular.positive_le_scalar_of_quadratic_bound
#print axioms TGLV350.Regular.normalizedDualCut_le_of_uniform_bound
#print axioms TGLV350.Regular.exists_boundedDualCutLimit
#print axioms TGLV350.Regular.quadratic_le_of_operator_le
#print axioms TGLV350.Regular.dualQuadraticIntegral_eq_boundedCutLimit
#print axioms TGLV350.Regular.boundedDualValue_unique
#print axioms TGLV350.Regular.boundedDualValue_dual_fixed
#print axioms TGLV350.Regular.exists_boundedDualValue_in_fixedCore
#print axioms TGLV350.Regular.HasFiniteDualSquare.exists_bounded_value
#print axioms TGLV350.Regular.regularAverage_bounded_value
#print axioms TGLV350.Regular.boundedFiniteSquares_strong_approximation

-- Locality of the fixed algebra, not yet constant-fibre identification.
#print axioms TGLV350.Regular.shift_commutes_regularUnitary
#print axioms TGLV350.Regular.regularCore_le_shiftCommutant
#print axioms TGLV350.Regular.shift_mem_regularCommutant
#print axioms TGLV350.Regular.dualFixedCore_commutes_shift_and_character
#print axioms TGLV350.Fourier.fourier_integral_ae_injective
#print axioms TGLV350.Regular.fourier_eq_character_integral
#print axioms TGLV350.Regular.fourier_inner_eq_character_pairing
#print axioms TGLV350.Regular.character_commutation_local_pairing
#print axioms TGLV350.Regular.measurableCutLp
#print axioms TGLV350.Regular.measurableCutLinear
#print axioms TGLV350.Regular.measurableCutLp_norm_le
#print axioms TGLV350.Regular.measurableCut
#print axioms TGLV350.Regular.measurableCut_ae
#print axioms TGLV350.Regular.measurableCut_inner
#print axioms TGLV350.Regular.character_commutation_measurableCut
#print axioms TGLV350.Regular.dualFixedCore_commutes_measurableCut

-- Constant fibre action on the entire regular Hilbert space.
-- Membership of that fibre operator in the original base remains open.
#print axioms TGLV350.Regular.testEmbedding
#print axioms TGLV350.Regular.testEmbedding_adjoint
#print axioms TGLV350.Regular.unitIntervalProjection_apply
#print axioms TGLV350.Regular.unitIntervalProjection_idempotent
#print axioms TGLV350.Regular.unitIntervalProjection_selfAdjoint
#print axioms TGLV350.Regular.translationCorrelation_integrable
#print axioms TGLV350.Regular.integral_translationCorrelation
#print axioms TGLV350.Regular.inner_unitCut_shift
#print axioms TGLV350.Regular.unitCut_correlation_support
#print axioms TGLV350.Regular.unitIntervalProjection_eq_cut_shift_integral
#print axioms TGLV350.Regular.commutes_unitIntervalProjection
#print axioms TGLV350.Regular.dualFixedCore_commutes_unitIntervalProjection
#print axioms TGLV350.Regular.unitIntervalProjection_testVector
#print axioms TGLV350.Regular.testEmbedding_adjoint_projection
#print axioms TGLV350.Regular.commutation_testVector_action
#print axioms TGLV350.Regular.commutation_fibreCandidate_read
#print axioms TGLV350.Regular.dualFixedCore_testVector_action
#print axioms TGLV350.Regular.setIntegral_measurableCut
#print axioms TGLV350.Regular.unitCut_integral_eq_read_cut
#print axioms TGLV350.Regular.testEmbedding_adjoint_fibre
#print axioms TGLV350.Regular.fibre_commutes_measurableCut
#print axioms TGLV350.Regular.unitCut_mul_eq_zero_of_zero_read
#print axioms TGLV350.Regular.eq_zero_of_shift_commutation_unitCut_zero
#print axioms TGLV350.Regular.eq_fibre_of_shift_character_commutation
#print axioms TGLV350.Regular.existsUnique_fibre_of_shift_character_commutation
#print axioms TGLV350.Regular.dualFixedCore_eq_fibre_candidate

-- Same-representation identification of the dual-fixed algebra with the base.
#print axioms TGLV350.Regular.operatorField_jointly_continuous
#print axioms TGLV350.Regular.operatorField_memLp
#print axioms TGLV350.Regular.operatorFieldLinear
#print axioms TGLV350.Regular.operatorFieldLift
#print axioms TGLV350.Regular.operatorFieldLift_ae
#print axioms TGLV350.Regular.operatorFieldLift_norm_le
#print axioms TGLV350.Regular.operatorFieldLift_commutes_fibre
#print axioms TGLV350.Regular.continuous_operator_action_eq_of_L2_tests
#print axioms TGLV350.Regular.operatorFieldLift_faithful
#print axioms TGLV350.Regular.operatorFieldLift_commutation_reflects
#print axioms TGLV350.Regular.modularConjugation_preserves_commutant
#print axioms TGLV350.Regular.modularFlow_jointly_continuous
#print axioms TGLV350.Regular.modularConjugation_strongly_continuous
#print axioms TGLV350.Regular.twistedCommutantField
#print axioms TGLV350.Regular.twistedCommutantField_zero
#print axioms TGLV350.Regular.twistedCommutantField_intertwines
#print axioms TGLV350.Regular.operatorFieldLift_commutes_regular_of_intertwining
#print axioms TGLV350.Regular.mem_regularCommutant_of_generators
#print axioms TGLV350.Regular.twistedCommutantLift_mem
#print axioms TGLV350.Regular.fibre_mem_regularCore_iff
#print axioms TGLV350.Regular.dualFixedCore_fibreCandidate_mem
#print axioms TGLV350.Regular.dualFixedCore_eq_amplified_base
#print axioms TGLV350.Regular.dualFixedCore_existsUnique_base

-- Faithful normal scalar dual weight and square-finite strong density; no trace yet.
#print axioms TGLV350.Regular.fixedBaseEmbedding_bijective
#print axioms TGLV350.Regular.fixedBaseEquiv
#print axioms TGLV350.Regular.fixedBaseEquiv_apply
#print axioms TGLV350.Regular.fixedBaseEquiv_symm_apply
#print axioms TGLV350.Regular.fixedBaseOrderIso
#print axioms TGLV350.Regular.exists_boundedDualValue_in_base
#print axioms TGLV350.Regular.HasFiniteDualSquare.exists_base_value
#print axioms TGLV350.Regular.boundedBaseDualValue_unique
#print axioms TGLV350.Regular.finiteBaseValues_strong_approximation
#print axioms TGLV350.Regular.regularVacuum_norm
#print axioms TGLV350.Regular.fixedCore_regularVacuum_separating
#print axioms TGLV350.Regular.dualResolvent_fixes_zero_form_vector
#print axioms TGLV350.Regular.dualQuadraticIntegral_vacuum_faithful
#print axioms TGLV350.Regular.scalarDualWeight
#print axioms TGLV350.Regular.scalarDualWeight_zero
#print axioms TGLV350.Regular.scalarDualWeight_add
#print axioms TGLV350.Regular.scalarDualWeight_scale
#print axioms TGLV350.Regular.scalarDualWeight_mono
#print axioms TGLV350.Regular.scalarDualWeight_faithful
#print axioms TGLV350.Regular.scalarDualWeight_normal
#print axioms TGLV350.Regular.HasFiniteDualSquare.scalar_finite
#print axioms TGLV350.Regular.scalarDualWeight_square_finite_strong_density
#print axioms TGLV350.Regular.scalarDualWeight_bounded_base_value

-- Candidate flow invariance and a bounded strongly dense star domain; KMS remains open.
#print axioms TGLV350.Regular.regular_conjugation_eq_fibre_modular
#print axioms TGLV350.Regular.fibre_modular_fixes_regularVacuum
#print axioms TGLV350.Regular.dualQuadraticIntegral_regular_conjugate_vacuum
#print axioms TGLV350.Regular.PositiveCoreInput.regularConjugate
#print axioms TGLV350.Regular.scalarDualWeight_regular_invariant
#print axioms TGLV350.Regular.regularScalarWeightCertificate
#print axioms TGLV350.Regular.contraction_adjoint_tendsto_identity
#print axioms TGLV350.Regular.regularAverage_star_tendsto_identity
#print axioms TGLV350.Regular.bounded_application_tendsto
#print axioms TGLV350.Regular.finiteDualStarCore
#print axioms TGLV350.Regular.regularSandwich
#print axioms TGLV350.Regular.regularSandwich_star
#print axioms TGLV350.Regular.regularSandwich_mem_finiteDualStarCore
#print axioms TGLV350.Regular.regularSandwich_norm_le
#print axioms TGLV350.Regular.regularSandwich_tendsto
#print axioms TGLV350.Regular.finiteDualStarCore_strongStar_approximation
#print axioms TGLV350.Regular.finiteDualStarCore_scalar_squares_finite

-- Faithful star representation on the completed finite-ideal orbit range.
#print axioms TGLV350.Regular.scalarOrbit_memLp
#print axioms TGLV350.Regular.scalarGNSOrbit
#print axioms TGLV350.Regular.scalarGNSOrbit_norm_sq
#print axioms TGLV350.Regular.dualAmbient_add_apply
#print axioms TGLV350.Regular.scalarGNSOrbit_ae
#print axioms TGLV350.Regular.scalarGNSOrbit_add
#print axioms TGLV350.Regular.scalarGNSOrbit_smul
#print axioms TGLV350.Regular.scalarGNSLinear
#print axioms TGLV350.Regular.scalarGNSOrbit_zero_iff
#print axioms TGLV350.Regular.scalarGNSLinear_injective
#print axioms TGLV350.Regular.scalarGNSLeftProduct
#print axioms TGLV350.Regular.scalarGNSAmbientAction
#print axioms TGLV350.Regular.scalarGNSAmbientAction_norm_le
#print axioms TGLV350.Regular.scalarGNSAmbientAction_intertwines
#print axioms TGLV350.Regular.operatorFieldLift_constant
#print axioms TGLV350.Regular.operatorFieldLift_add
#print axioms TGLV350.Regular.operatorFieldLift_mul
#print axioms TGLV350.Regular.operatorFieldLift_smul
#print axioms TGLV350.Regular.operatorFieldLift_star
#print axioms TGLV350.Regular.scalarGNSSubspace
#print axioms TGLV350.Regular.scalarGNSCompleteSpace
#print axioms TGLV350.Regular.scalarGNSEmbedding
#print axioms TGLV350.Regular.scalarGNSEmbedding_injective
#print axioms TGLV350.Regular.scalarGNSAmbientAction_preserves
#print axioms TGLV350.Regular.scalarGNSAction
#print axioms TGLV350.Regular.scalarGNSAction_apply
#print axioms TGLV350.Regular.scalarGNSAction_norm_le
#print axioms TGLV350.Regular.scalarGNSAction_intertwines
#print axioms TGLV350.Regular.dualOrbitRepresentation
#print axioms TGLV350.Regular.dualOrbitRepresentation_scalar_apply
#print axioms TGLV350.Regular.reducingStarRepresentation
#print axioms TGLV350.Regular.scalarGNSRepresentation
#print axioms TGLV350.Regular.scalarGNSEmbedding_denseRange
#print axioms TGLV350.Regular.scalarGNSRepresentation_zero_iff
#print axioms TGLV350.Regular.scalarGNSRepresentation_injective

-- Norm-dense initial involutive graph on the finite-ideal GNS space.
#print axioms TGLV350.Regular.dualCharacterField
#print axioms TGLV350.Regular.dualOrbit_factorization
#print axioms TGLV350.Regular.dualOrbit_tendsto_of_uniformly_bounded
#print axioms TGLV350.Regular.scalarGNSLeftRegularization
#print axioms TGLV350.Regular.scalarGNSLeftRegularization_mem_starCore
#print axioms TGLV350.Regular.scalarGNSOrbit_leftRegularization_tendsto
#print axioms TGLV350.Regular.scalarGNSStarEmbedding
#print axioms TGLV350.Regular.scalarGNSEmbedding_leftRegularization_tendsto
#print axioms TGLV350.Regular.scalarGNSStarEmbedding_denseRange
#print axioms TGLV350.Regular.scalarGNSStarEmbedding_injective
#print axioms TGLV350.Regular.scalarTomitaGraph
#print axioms TGLV350.Regular.scalarTomitaGraph_single_valued
#print axioms TGLV350.Regular.scalarTomitaGraph_swap
#print axioms TGLV350.Regular.scalarTomitaGraph_domain_dense

-- Order normality of the actual finite-ideal GNS representation.
#print axioms TGLV350.Regular.scalarGNSRepresentation_tendsto_of_uniformly_bounded
#print axioms TGLV350.Regular.operator_le_of_sub_nonneg
#print axioms TGLV350.Regular.dualOrbitRepresentation_nonneg
#print axioms TGLV350.Regular.scalarGNSRepresentation_nonneg
#print axioms TGLV350.Regular.scalarGNSRepresentation_monotone
#print axioms TGLV350.Regular.scalarGNSRepresentation_preserves_positive_isLUB
#print axioms TGLV350.Regular.scalarGNSRepresentation_preserves_positive_directed_isLUB

-- Bounded positive functionals dominated by the actual scalar weight.
#print axioms TGLV350.Regular.dualWeightCut_add
#print axioms TGLV350.Regular.dualWeightCut_smul
#print axioms TGLV350.Regular.dualWeightCutCLM
#print axioms TGLV350.Regular.dualCutFunctional
#print axioms TGLV350.Regular.dualCutFunctional_apply
#print axioms TGLV350.Regular.dualCutFunctional_nonneg
#print axioms TGLV350.Regular.dualCutFunctional_ofReal_re
#print axioms TGLV350.Regular.scalarDualWeight_dominates_cut
#print axioms TGLV350.Regular.scalarDualWeight_eq_iSup_boundedCuts
#print axioms TGLV350.Regular.dualCutFunctional_re_tendsto
#print axioms TGLV350.Regular.scalarCut_tendsto_internal_isLUB

-- Concrete contractions realizing bounded scalar cuts in ambient GNS space.
#print axioms TGLV350.Regular.measurableCut_operatorFieldLift
#print axioms TGLV350.Regular.measurableCut_nat_joint_zero
#print axioms TGLV350.Regular.scalarGNSCutMap
#print axioms TGLV350.Regular.scalarGNSCutMap_norm_le
#print axioms TGLV350.Regular.scalarGNSCutMap_intertwines
#print axioms TGLV350.Regular.scalarGNSCutMap_joint_zero
#print axioms TGLV350.Regular.measurableCut_norm_sq
#print axioms TGLV350.Regular.dualCutFunctional_square_re
#print axioms TGLV350.Regular.scalarGNSCutMap_embedding_norm_sq
'''

batch_targets = []
for name in tomita_batch:
    source = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    batch_targets.extend('TGLV350.Regular.' + short for short in
                         re.findall(r'^#print axioms ([\w.]+)$', source, re.M))
assert len(batch_targets) == len(set(batch_targets)) == 463
new['TGL/Audit.lean'] += '\n-- Closed original GNS graph; KMS and canonical trace still open.\n'
new['TGL/Audit.lean'] += ''.join('#print axioms ' + name + '\n' for name in batch_targets)

lines = text.splitlines(keepends=True)
starts = [0]
for line in lines:
    starts.append(starts[-1] + len(line))


def position(line, column):
    return starts[line - 1] + len(lines[line - 1].encode('utf-8')[:column].decode('utf-8'))


def span(node):
    return position(node.lineno, node.col_offset), position(node.end_lineno, node.end_col_offset)


patches = []
for key, value in zip(assignment.value.keys, assignment.value.values):
    if key.value in new:
        patches.append((*span(value), repr(new[key.value])))
added = {key: value for key, value in new.items() if key not in embedded}
closing = span(assignment.value)[1] - 1
patches.append((closing, closing, ''.join(
    '\n    ' + repr(key) + ': ' + repr(value) + ',' for key, value in added.items()) + '\n'))

extension = (ROOT / 'gate_extension.py').read_text(encoding='utf-8')
evaluator = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == 'evaluate_quantum_gravity_closure')
start = span(evaluator)[0]
patches.append((start, start, extension + '\n\n'))

verifier = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == 'verify_tgl_kernel_formalization')
last_return = verifier.body[-1]
assert isinstance(last_return, ast.Return) and isinstance(last_return.value, ast.Name)
patches.append((*span(last_return), 'return finalize_v350_modular_frontier(res)'))

gate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'prove_qg_closure_gate')
gate_assignment = next(n for n in gate.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'gate' for t in n.targets))
end = span(gate_assignment)[1]
patches.append((end, end, '\n    gate["kernel_frontier"] = evaluate_v350_kernel_frontier(kf99)'))
# Verify the existing variable name instead of silently injecting an undefined alias.
assert any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'kf99'
           for t in n.targets) for n in gate.body)

# Preserve historical modules, but stop treating the absence of a future proof as an invariant.
changes = []
for function in (n for n in tree.body if isinstance(n, ast.FunctionDef)):
    for node in ast.walk(function):
        if not (isinstance(node, ast.Tuple) and len(node.elts) == 2):
            continue
        label, value = node.elts
        label_text = text[slice(*span(label))]
        expression = text[slice(*span(value))]
        updated = expression
        for flag in ('red_clause_JMJ_contains', 'gpf_tower_act_III_inhabitant_constructed'):
            updated = updated.replace('not kf.get("' + flag + '")',
                                      'v350_frontier_flag_has_proof(kf, "' + flag + '")')
        updated = updated.replace('not [k for k in kf if k.startswith("gpf_") and kf.get(k)]',
                                  'v350_gravity_flags_have_proof(kf)')
        updated = updated.replace('not any(kf.get(k) for k in kf if k.startswith("gpf_"))',
                                  'v350_gravity_flags_have_proof(kf)')
        if updated != expression:
            patches.append((*span(value), updated))
            new_label = '[ERRATA v350+ / proveniência] As flags modular e Ato III exigem prova tipada; este módulo isolado não as quita.'
            patches.append((*span(label), repr(new_label)))
            changes.append({'function': function.name, 'original_line': node.lineno,
                            'historical_label_source': label_text,
                            'old_expression': expression, 'new_expression': updated})

patches.sort(reverse=True)
previous = len(text) + 1
for start, end, replacement in patches:
    assert end <= previous, ('overlapping patches', start, end, previous)
    text = text[:start] + replacement + text[end:]
    previous = start
parsed = ast.parse(text)
integrated = ast.literal_eval(next(n for n in parsed.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)).value)
assert len(integrated) == len(embedded) + len(added)
for key, content in embedded.items():
    if key not in new:
        assert integrated[key] == content
for key, content in new.items():
    assert integrated[key] == content
    write_atomic(ROOT / 'kernel' / key, content.encode('utf-8'))
write_atomic(ROOT / 'um.py', text.encode('utf-8'))
record = {'base_sha256': hashlib.sha256(raw).hexdigest(),
          'working_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
          'added_kernel_files': list(added), 'updated_kernel_files': [k for k in new if k in embedded],
          'embedded_files': len(integrated), 'historical_checks_updated': changes,
          'status': 'INTEGRATED_SOURCE__FULL_RUNTIME_NOT_YET_EXECUTED'}
write_atomic(ROOT / 'integration.json', json.dumps(record, indent=2, ensure_ascii=False).encode('utf-8'))
print(json.dumps({k: v for k, v in record.items() if k != 'historical_checks_updated'}, ensure_ascii=False))
print('historical_checks_updated=' + str(len(changes)))
