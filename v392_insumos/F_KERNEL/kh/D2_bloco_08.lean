-- KH-N1 D2 bloco 8/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL.ModularRealization
import TGLExt.AperiodicTowerLift
import TGLExt.Bicommutant
import TGLExt.BoundaryException
import TGLExt.CanonicalModularStationarity
import TGLExt.ClosedLattice
import TGLExt.CoherentScalarStress
import TGLExt.CollapseContract
import TGLExt.ConstructedHorizonPencil
import TGLExt.ExpectationBlockPositive
import TGLExt.FiniteTomita
import TGLExt.FirstCurvature
import TGLExt.FisherCorrectedEinstein
import TGLExt.FisherInformationTensor
import TGLExt.FlowDifferentiability
import TGLExt.ForbiddenBoundary
import TGLExt.FusedWitness
import TGLExt.GeneralAngularTensorCodec
import TGLExt.GeneralNull
import TGLExt.GeodesicShooting
import TGLExt.GravitationalChartGluing
import TGLExt.GravitonReading
import TGLExt.LocalGeodesicFlow
import TGLExt.LocalInteractionCocycle
import TGLExt.LorentzMetricField
import TGLExt.ModularDephasingBridge
import TGLExt.ModularHorizontalRotation
import TGLExt.NullStressCompletion
import TGLExt.O16.BoundedTransformCore_v2
import TGLExt.O16.ContractGroupA_v3
import TGLExt.O16.ContractLoad
import TGLExt.O16.ExistingKillingCalibration
import TGLExt.O16.LightRayAnalyticCore_v3
import TGLExt.O16.LightRayContourTransport_v2
import TGLExt.O16.OrbitalStateAnalytic
import TGLExt.O16.QubitScalarEntropy
import TGLExt.O16.RapidityJacobian_v2
import TGLExt.O16.StrictCocycleGauge
import TGLExt.O16.UVScope016_v3
import TGLExt.O16.VectorRapiditySpectrum
import TGLExt.O16.WidthFromContraction_v2
import TGLExt.OpticalConstructedHeat
import TGLExt.PoincareWitness
import TGLExt.PolarizerCostSeries
import TGLExt.ProfileEntropyLimits
import TGLExt.ProgrammerRule
import TGLExt.RicciLieNaturality
import TGLExt.ScreenAreaCalculus
import TGLExt.ScreenTransportODE
import TGLExt.SelectedFisherLorentzMetric
import TGLExt.SmoothMatrixCalculus
import TGLExt.StateClockMatchingControls
import TGLExt.StaticDynamicMixture
import TGLExt.SummableGravityBridge
import TGLExt.TailNotCyclic
import TGLExt.TheAngleIsTheBridge
import TGLExt.TheConverseClauseReduced
import TGLExt.TheCornerOfThePackage
import TGLExt.TheEmptying
import TGLExt.TheExplosion
import TGLExt.TheImportedCommutation
import TGLExt.TheNetFiresTheCorner
import TGLExt.ThePhysicalHorizon
import TGLExt.TheProfileDuality
import TGLExt.TheScaleHasNoFixedPoint
import TGLExt.TheScreenIsFounded
import TGLExt.TheTelescopingProfile
import TGLExt.TheTower
import TGLExt.ThermalCutoffResponse
import TGLExt.TowerDephasingStationary
import TGLExt.TowerThermalProfile
import TGLExt.V350AntilinearAdjointGraph
import TGLExt.V350BoundedBaseDualValues
import TGLExt.V350DualWeightCuts
import TGLExt.V350DualWeightForm
import TGLExt.V350HilbertProjectionBlocks
import TGLExt.V350L2MeasurableCut
import TGLExt.V350LocalRightModularTransport
import TGLExt.V350ModularCertificate
import TGLExt.V350OperatorFieldFaithfulness
import TGLExt.V350PartialPositiveResolvent
import TGLExt.V350PartialSquareEnergy
import TGLExt.V350ReducingCommutantTransport
import TGLExt.V350ScalarCutVacuum
import TGLExt.V350ScalarDualWeightFaithfulness
import TGLExt.V350ScalarPairedMultiplicationGraph
import TGLExt.V350ScalarTomitaRootEnergy
import TGLExt.V350ScalarTomitaStandardSubspace
import TGLExt.V350ScalarWeightDomain
import TGLExt.V351BaseSeriesNormality
import TGLExt.V351ExtendedBaseDualWeight
import TGLExt.V351InverseCutoffCFC
import TGLExt.V351ModularFixedVectors
import TGLExt.V351RegularCoreTraceConstruction
import TGLExt.V351RegularCoreTraceContract
import TGLExt.V351ResolventImaginaryPowers
import TGLExt.V351WeightAverageRecovery
import TGLExt.V354SpectralThreshold
import TGLExt.WedgeNetFiniteDiamond
import TGLExt.WitnessV2

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL.ModularRealization, `TGLExt.AperiodicTowerLift, `TGLExt.Bicommutant, `TGLExt.BoundaryException, `TGLExt.CanonicalModularStationarity, `TGLExt.ClosedLattice, `TGLExt.CoherentScalarStress, `TGLExt.CollapseContract, `TGLExt.ConstructedHorizonPencil, `TGLExt.ExpectationBlockPositive, `TGLExt.FiniteTomita, `TGLExt.FirstCurvature, `TGLExt.FisherCorrectedEinstein, `TGLExt.FisherInformationTensor, `TGLExt.FlowDifferentiability, `TGLExt.ForbiddenBoundary, `TGLExt.FusedWitness, `TGLExt.GeneralAngularTensorCodec, `TGLExt.GeneralNull, `TGLExt.GeodesicShooting, `TGLExt.GravitationalChartGluing, `TGLExt.GravitonReading, `TGLExt.LocalGeodesicFlow, `TGLExt.LocalInteractionCocycle, `TGLExt.LorentzMetricField, `TGLExt.ModularDephasingBridge, `TGLExt.ModularHorizontalRotation, `TGLExt.NullStressCompletion, `TGLExt.O16.BoundedTransformCore_v2, `TGLExt.O16.ContractGroupA_v3, `TGLExt.O16.ContractLoad, `TGLExt.O16.ExistingKillingCalibration, `TGLExt.O16.LightRayAnalyticCore_v3, `TGLExt.O16.LightRayContourTransport_v2, `TGLExt.O16.OrbitalStateAnalytic, `TGLExt.O16.QubitScalarEntropy, `TGLExt.O16.RapidityJacobian_v2, `TGLExt.O16.StrictCocycleGauge, `TGLExt.O16.UVScope016_v3, `TGLExt.O16.VectorRapiditySpectrum, `TGLExt.O16.WidthFromContraction_v2, `TGLExt.OpticalConstructedHeat, `TGLExt.PoincareWitness, `TGLExt.PolarizerCostSeries, `TGLExt.ProfileEntropyLimits, `TGLExt.ProgrammerRule, `TGLExt.RicciLieNaturality, `TGLExt.ScreenAreaCalculus, `TGLExt.ScreenTransportODE, `TGLExt.SelectedFisherLorentzMetric, `TGLExt.SmoothMatrixCalculus, `TGLExt.StateClockMatchingControls, `TGLExt.StaticDynamicMixture, `TGLExt.SummableGravityBridge, `TGLExt.TailNotCyclic, `TGLExt.TheAngleIsTheBridge, `TGLExt.TheConverseClauseReduced, `TGLExt.TheCornerOfThePackage, `TGLExt.TheEmptying, `TGLExt.TheExplosion, `TGLExt.TheImportedCommutation, `TGLExt.TheNetFiresTheCorner, `TGLExt.ThePhysicalHorizon, `TGLExt.TheProfileDuality, `TGLExt.TheScaleHasNoFixedPoint, `TGLExt.TheScreenIsFounded, `TGLExt.TheTelescopingProfile, `TGLExt.TheTower, `TGLExt.ThermalCutoffResponse, `TGLExt.TowerDephasingStationary, `TGLExt.TowerThermalProfile, `TGLExt.V350AntilinearAdjointGraph, `TGLExt.V350BoundedBaseDualValues, `TGLExt.V350DualWeightCuts, `TGLExt.V350DualWeightForm, `TGLExt.V350HilbertProjectionBlocks, `TGLExt.V350L2MeasurableCut, `TGLExt.V350LocalRightModularTransport, `TGLExt.V350ModularCertificate, `TGLExt.V350OperatorFieldFaithfulness, `TGLExt.V350PartialPositiveResolvent, `TGLExt.V350PartialSquareEnergy, `TGLExt.V350ReducingCommutantTransport, `TGLExt.V350ScalarCutVacuum, `TGLExt.V350ScalarDualWeightFaithfulness, `TGLExt.V350ScalarPairedMultiplicationGraph, `TGLExt.V350ScalarTomitaRootEnergy, `TGLExt.V350ScalarTomitaStandardSubspace, `TGLExt.V350ScalarWeightDomain, `TGLExt.V351BaseSeriesNormality, `TGLExt.V351ExtendedBaseDualWeight, `TGLExt.V351InverseCutoffCFC, `TGLExt.V351ModularFixedVectors, `TGLExt.V351RegularCoreTraceConstruction, `TGLExt.V351RegularCoreTraceContract, `TGLExt.V351ResolventImaginaryPowers, `TGLExt.V351WeightAverageRecovery, `TGLExt.V354SpectralThreshold, `TGLExt.WedgeNetFiniteDiamond, `TGLExt.WitnessV2]
  let alvo : NameSet := alvoL.foldl (fun s n => s.insert n) {}
  let mut n_decl := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if alvo.contains m then
        let axs ← liftCoreM (collectAxioms n)
        let kind : String := match ci with
          | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM"
          | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot" | .inductInfo _ => "induct"
          | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
        n_decl := n_decl + 1
        let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)
        unless ok do n_fora := n_fora + 1
        IO.println ("COB\t" ++ m.toString ++ "\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ (if ok then "TRIO" else "FORA") ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
  IO.println ("COB_TOTAL\tdecl=" ++ toString n_decl ++ "\tfora_do_trio=" ++ toString n_fora)
