import TGLExt.V351AntiunitaryResolventPhase
import TGLExt.V351AverageFixedPair
import TGLExt.V351ScalarTomitaImaginaryConjugation
import TGLExt.V351ScalarImaginaryLeftTransport
import TGLExt.V351ScalarImaginaryCoreAction
import TGLExt.V351ModularFixedVectors
import TGLExt.V351ModularImplementation
import TGLExt.V351ModularCutBalance
import TGLExt.V351QuadraticTrace
import TGLExt.V351RegularCoreTraceConstruction
import TGLExt.SectorFluidClosure
import TGLExt.SectorFriedmann
import TGLExt.ThermodynamicFriedmann
import TGLExt.SectorRouteComparison
import TGLExt.TheAngleReachesTheMetric
import TGLExt.SectorFriedmannAdditive
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V351ScaledResolventFunctions
import TGLExt.V351ScaledResolventCalculus
import TGLExt.V351ImaginaryPowerScaling
import TGLExt.V351ScalarImaginaryRightTransport

set_option pp.universes true

#check TGLV350.Regular.complex_cfc_selfadjoint_intertwines
#print axioms TGLV350.Regular.complex_cfc_selfadjoint_intertwines
#check TGLV350.Regular.resolventDampingOperator_intertwines
#print axioms TGLV350.Regular.resolventDampingOperator_intertwines
#check TGLV350.Regular.resolventPhaseOperator_intertwines
#print axioms TGLV350.Regular.resolventPhaseOperator_intertwines
#check TGLV350.Regular.resolventImaginaryPower_intertwines
#print axioms TGLV350.Regular.resolventImaginaryPower_intertwines
#check TGLV350.Regular.scaledResolventCoordinate
#print axioms TGLV350.Regular.scaledResolventCoordinate
#check TGLV350.Regular.scaledResolventDampingFactor
#print axioms TGLV350.Regular.scaledResolventDampingFactor
#check TGLV350.Regular.scaledResolventDenominator_scalar_pos
#print axioms TGLV350.Regular.scaledResolventDenominator_scalar_pos
#check TGLV350.Regular.scaledResolventCoordinate_complement
#print axioms TGLV350.Regular.scaledResolventCoordinate_complement
#check TGLV350.Regular.scaledResolventCoordinate_ratio
#print axioms TGLV350.Regular.scaledResolventCoordinate_ratio
#check TGLV350.Regular.scaledResolventCoordinate_damping
#print axioms TGLV350.Regular.scaledResolventCoordinate_damping
#check TGLV350.Regular.scaledResolventCoordinate_phase
#print axioms TGLV350.Regular.scaledResolventCoordinate_phase
#check TGLV350.Regular.positive_contraction_spectrum_bounds
#print axioms TGLV350.Regular.positive_contraction_spectrum_bounds
#check TGLV350.Regular.scaledResolventDenominator_real_cfc
#print axioms TGLV350.Regular.scaledResolventDenominator_real_cfc
#check TGLV350.Regular.scaledResolventCoordinate_cfc
#print axioms TGLV350.Regular.scaledResolventCoordinate_cfc
#check TGLV350.Regular.scaledResolventCoordinate_continuousOn_spectrum
#print axioms TGLV350.Regular.scaledResolventCoordinate_continuousOn_spectrum
#check TGLV350.Regular.scaledResolventDampingFactor_continuousOn_spectrum
#print axioms TGLV350.Regular.scaledResolventDampingFactor_continuousOn_spectrum
#check TGLV350.Regular.scaledResolventDampingOperator
#print axioms TGLV350.Regular.scaledResolventDampingOperator
#check TGLV350.Regular.scaledResolventDampingOperator_isUnit
#print axioms TGLV350.Regular.scaledResolventDampingOperator_isUnit
#check TGLV350.Regular.scaledPositiveResolvent_damping
#print axioms TGLV350.Regular.scaledPositiveResolvent_damping
#check TGLV350.Regular.scaledPositiveResolvent_phase
#print axioms TGLV350.Regular.scaledPositiveResolvent_phase
#check TGLV350.Regular.scaledResolventDamping_denseRange
#print axioms TGLV350.Regular.scaledResolventDamping_denseRange
#check TGLV350.Regular.resolventImaginaryPower_scaled_intertwining
#print axioms TGLV350.Regular.resolventImaginaryPower_scaled_intertwining
#check TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling
#print axioms TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling
#check TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes
#check TGLV350.Regular.resolventPhaseFunction_reflection
#print axioms TGLV350.Regular.resolventPhaseFunction_reflection
#check TGLV350.Regular.antiunitaryConjugate_star
#print axioms TGLV350.Regular.antiunitaryConjugate_star
#check TGLV350.Regular.antiunitaryConjugate_add
#print axioms TGLV350.Regular.antiunitaryConjugate_add
#check TGLV350.Regular.antiunitaryConjugate_smul
#print axioms TGLV350.Regular.antiunitaryConjugate_smul
#check TGLV350.Regular.antiunitaryConjugateRealHom
#print axioms TGLV350.Regular.antiunitaryConjugateRealHom
#check TGLV350.Regular.antiunitaryConjugate_continuous
#print axioms TGLV350.Regular.antiunitaryConjugate_continuous
#check TGLV350.Regular.antiunitaryConjugate_selfadjoint
#print axioms TGLV350.Regular.antiunitaryConjugate_selfadjoint
#check TGLV350.Regular.antiunitaryConjugate_real_cfc
#print axioms TGLV350.Regular.antiunitaryConjugate_real_cfc
#check TGLV350.Regular.complex_cfc_real_imaginary
#print axioms TGLV350.Regular.complex_cfc_real_imaginary
#check TGLV350.Regular.antiunitaryConjugate_complex_cfc
#print axioms TGLV350.Regular.antiunitaryConjugate_complex_cfc
#check TGLV350.Regular.antiunitaryConjugate_resolventPhase
#print axioms TGLV350.Regular.antiunitaryConjugate_resolventPhase
#check TGLV350.Regular.antiunitaryConjugate_resolventDamping
#print axioms TGLV350.Regular.antiunitaryConjugate_resolventDamping
#check TGLV350.Regular.resolventImaginaryPower_antiunitary
#print axioms TGLV350.Regular.resolventImaginaryPower_antiunitary
#check TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes
#check TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate
#check TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator
#check TGLV350.Regular.scalarWeightStar_fixed_pair_of_polarRight
#print axioms TGLV350.Regular.scalarWeightStar_fixed_pair_of_polarRight
#check TGLV350.Regular.regularAverage_square_fixed_pair
#print axioms TGLV350.Regular.regularAverage_square_fixed_pair
#check TGLV350.Regular.matrixUnit_imaginaryPower_left_scaling
#print axioms TGLV350.Regular.matrixUnit_imaginaryPower_left_scaling
#check TGLV350.Regular.scalarTomitaImaginaryPower_regular_left_commutes
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_regular_left_commutes
#check TGLV350.Regular.matrixUnit_regular_core_conjugation
#print axioms TGLV350.Regular.matrixUnit_regular_core_conjugation
#check TGLV350.Regular.matrixUnit_imaginaryPower_base_scaling
#print axioms TGLV350.Regular.matrixUnit_imaginaryPower_base_scaling
#check TGLV350.Regular.scalarTomitaImaginaryPower_core_conjugation
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_core_conjugation
#check TGLV350.Regular.scalarTomitaImaginaryPower_fixed_of_fixed_pair
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_fixed_of_fixed_pair
#check TGLV350.Regular.regularAverage_square_modular_fixed
#print axioms TGLV350.Regular.regularAverage_square_modular_fixed
#check TGLV350.Regular.scalarTomitaImaginaryPower_eq_regular_implementation
#print axioms TGLV350.Regular.scalarTomitaImaginaryPower_eq_regular_implementation
#check TGLV350.Regular.scalarTomitaResolvent_double_cut_balance
#print axioms TGLV350.Regular.scalarTomitaResolvent_double_cut_balance
#check TGLV350.Regular.scalarInverseLimitWeight_tracial
#print axioms TGLV350.Regular.scalarInverseLimitWeight_tracial
#check TGLV350.Regular.scalarInverseLimitTraceData
#print axioms TGLV350.Regular.scalarInverseLimitTraceData
#check ChatgptAudit.FLRW.SectorFluid
#print axioms ChatgptAudit.FLRW.SectorFluid
#check ChatgptAudit.FLRW.SectorFluid.totalRho
#print axioms ChatgptAudit.FLRW.SectorFluid.totalRho
#check ChatgptAudit.FLRW.SectorFluid.totalPressure
#print axioms ChatgptAudit.FLRW.SectorFluid.totalPressure
#check ChatgptAudit.FLRW.SectorFluid.enthalpy
#print axioms ChatgptAudit.FLRW.SectorFluid.enthalpy
#check ChatgptAudit.FLRW.SectorFluid.wEff
#print axioms ChatgptAudit.FLRW.SectorFluid.wEff
#check ChatgptAudit.FLRW.SectorFluid.correctedRho
#print axioms ChatgptAudit.FLRW.SectorFluid.correctedRho
#check ChatgptAudit.FLRW.SectorFluid.correctedTotalRho
#print axioms ChatgptAudit.FLRW.SectorFluid.correctedTotalRho
#check ChatgptAudit.FLRW.SectorFluid.correctedTotalPressure
#print axioms ChatgptAudit.FLRW.SectorFluid.correctedTotalPressure
#check ChatgptAudit.FLRW.SectorFluid.enthalpy_eq
#print axioms ChatgptAudit.FLRW.SectorFluid.enthalpy_eq
#check ChatgptAudit.FLRW.SectorFluid.sector_rescaling_preserves_continuity
#print axioms ChatgptAudit.FLRW.SectorFluid.sector_rescaling_preserves_continuity
#check ChatgptAudit.FLRW.SectorFluid.corrected_closure
#print axioms ChatgptAudit.FLRW.SectorFluid.corrected_closure
#check ChatgptAudit.FLRW.SectorFluid.weighted_continuity
#print axioms ChatgptAudit.FLRW.SectorFluid.weighted_continuity
#check ChatgptAudit.FLRW.SectorFluid.total_continuity
#print axioms ChatgptAudit.FLRW.SectorFluid.total_continuity
#check ChatgptAudit.FLRW.SectorFluid.corrected_rho_deriv
#print axioms ChatgptAudit.FLRW.SectorFluid.corrected_rho_deriv
#check ChatgptAudit.FLRW.SectorFluid.corrected_pressure_differentiable
#print axioms ChatgptAudit.FLRW.SectorFluid.corrected_pressure_differentiable
#check ChatgptAudit.FLRW.SectorFluid.corrected_continuity
#print axioms ChatgptAudit.FLRW.SectorFluid.corrected_continuity
#check ChatgptAudit.FLRW.SectorFluid.effective_enthalpy
#print axioms ChatgptAudit.FLRW.SectorFluid.effective_enthalpy
#check ChatgptAudit.FLRW.SectorFluid.multiplicative_closure
#print axioms ChatgptAudit.FLRW.SectorFluid.multiplicative_closure
#check ChatgptAudit.FLRW.SectorFluid.three_sector_closure
#print axioms ChatgptAudit.FLRW.SectorFluid.three_sector_closure
#check ChatgptAudit.FLRW.sector_covariant_conservation
#print axioms ChatgptAudit.FLRW.sector_covariant_conservation
#check ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure
#print axioms ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure
#check ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological
#print axioms ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological
#check ChatgptAudit.FLRW.hubbleArea
#print axioms ChatgptAudit.FLRW.hubbleArea
#check ChatgptAudit.FLRW.entropyFactor
#print axioms ChatgptAudit.FLRW.entropyFactor
#check ChatgptAudit.FLRW.entropy_factor_pos
#print axioms ChatgptAudit.FLRW.entropy_factor_pos
#check ChatgptAudit.FLRW.hubble_area_derivative
#print axioms ChatgptAudit.FLRW.hubble_area_derivative
#check ChatgptAudit.FLRW.HubbleHorizonInput
#print axioms ChatgptAudit.FLRW.HubbleHorizonInput
#check ChatgptAudit.FLRW.modified_clausius_coefficient
#print axioms ChatgptAudit.FLRW.modified_clausius_coefficient
#check ChatgptAudit.FLRW.tgl_second_friedmann_from_clausius
#print axioms ChatgptAudit.FLRW.tgl_second_friedmann_from_clausius
#check ChatgptAudit.FLRW.radius_free_flux_consequence
#print axioms ChatgptAudit.FLRW.radius_free_flux_consequence
#check ChatgptAudit.FLRW.variable_entropy_derivative
#print axioms ChatgptAudit.FLRW.variable_entropy_derivative
#check ChatgptAudit.FLRW.tgl_first_friedmann_from_primitive
#print axioms ChatgptAudit.FLRW.tgl_first_friedmann_from_primitive
#check ChatgptAudit.FLRW.tgl_first_friedmann_constant_w
#print axioms ChatgptAudit.FLRW.tgl_first_friedmann_constant_w
#check ChatgptAudit.FLRW.variable_factor_first_equation_defect
#print axioms ChatgptAudit.FLRW.variable_factor_first_equation_defect
#check ChatgptAudit.FLRW.SectorFluid.secondMoment
#print axioms ChatgptAudit.FLRW.SectorFluid.secondMoment
#check ChatgptAudit.FLRW.SectorFluid.sectorVariance
#print axioms ChatgptAudit.FLRW.SectorFluid.sectorVariance
#check ChatgptAudit.FLRW.SectorFluid.fluxFactor
#print axioms ChatgptAudit.FLRW.SectorFluid.fluxFactor
#check ChatgptAudit.FLRW.SectorFluid.corrected_enthalpy
#print axioms ChatgptAudit.FLRW.SectorFluid.corrected_enthalpy
#check ChatgptAudit.FLRW.SectorFluid.centered_variance
#print axioms ChatgptAudit.FLRW.SectorFluid.centered_variance
#check ChatgptAudit.FLRW.SectorFluid.sector_variance_nonneg
#print axioms ChatgptAudit.FLRW.SectorFluid.sector_variance_nonneg
#check ChatgptAudit.FLRW.SectorFluid.sector_variance_zero_iff
#print axioms ChatgptAudit.FLRW.SectorFluid.sector_variance_zero_iff
#check ChatgptAudit.FLRW.the_two_routes_differ
#print axioms ChatgptAudit.FLRW.the_two_routes_differ
#check ChatgptAudit.FLRW.the_two_routes_equal_iff
#print axioms ChatgptAudit.FLRW.the_two_routes_equal_iff
#check ChatgptAudit.FLRW.the_two_hubble_rates_differ
#print axioms ChatgptAudit.FLRW.the_two_hubble_rates_differ
#check ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure
#print axioms ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure
#check ChatgptAudit.FLRW.sector_clausius_matches_closed_rate
#print axioms ChatgptAudit.FLRW.sector_clausius_matches_closed_rate
#check ChatgptAudit.FLRW.common_w_flux_factor
#print axioms ChatgptAudit.FLRW.common_w_flux_factor
#check ChatgptAudit.FLRW.zero_flux_has_no_unique_factor
#print axioms ChatgptAudit.FLRW.zero_flux_has_no_unique_factor
#check ChatgptAudit.FLRW.matter_vacuum_variance
#print axioms ChatgptAudit.FLRW.matter_vacuum_variance
#check ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality
#print axioms ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality
#check ChatgptAudit.FLRW.coupling_eq_sin_sq
#print axioms ChatgptAudit.FLRW.coupling_eq_sin_sq
#check ChatgptAudit.FLRW.the_angle_reaches_the_metric
#print axioms ChatgptAudit.FLRW.the_angle_reaches_the_metric
#check ChatgptAudit.FLRW.the_passage
#print axioms ChatgptAudit.FLRW.the_passage
#check ChatgptAudit.FLRW.the_angle_reads_sector_first
#print axioms ChatgptAudit.FLRW.the_angle_reads_sector_first
#check ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure_additive
#print axioms ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure_additive
#print TGLV350.Regular.antiunitaryConjugate_add
#print TGLV350.Regular.antiunitaryConjugate_smul
#print ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure_additive

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for name in [`TGLV350.Regular.antiunitaryConjugate_add,
      `TGLV350.Regular.antiunitaryConjugate_smul] do
    match env.getModuleIdxFor? name with
    | some idx =>
      let supplier := env.header.moduleNames[idx.toNat]!
      unless supplier == `TGLExt.V350LocalBasePolarCommutation do
        throwError "Unexpected supplier for {name}: {supplier}"
      logInfo m!"SUPPLIER {name} = {supplier}"
    | none => throwError "No imported supplier for {name}"
