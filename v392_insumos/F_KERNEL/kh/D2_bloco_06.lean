-- KH-N1 D2 bloco 6/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL.HalfNatJonesTower
import TGL.Main
import TGLExt.AQFTCoreInhabitant
import TGLExt.AffineClockAndRegion
import TGLExt.AngularAreaObservability
import TGLExt.AngularScreenMetric
import TGLExt.BondLocalityEstimates
import TGLExt.ChainVolumePositive
import TGLExt.ConcreteFourFrame
import TGLExt.ConstructedHeatPrimitive
import TGLExt.ExpectationBounded
import TGLExt.ExpectationContinuity
import TGLExt.FLRWGeometry
import TGLExt.FiniteLevelExponentials
import TGLExt.GeodesicInitialRegularity
import TGLExt.HermitianConeRigidity
import TGLExt.HorizonGNSImplementation
import TGLExt.HorizontalAreaSelection
import TGLExt.IsotoneNet
import TGLExt.LeftRight
import TGLExt.LocalCentralizerExpectation
import TGLExt.LocalFilterLorentzAction
import TGLExt.MicroscopicClausiusBridge
import TGLExt.ModularFlowLevel
import TGLExt.ModulatorSelfAdjoint
import TGLExt.O16.AxiomasContorno
import TGLExt.O16.ContractGroupI_v3
import TGLExt.O16.ExactTypeReader_v2
import TGLExt.O16.GudermannSpectral
import TGLExt.O16.LightRayGaussianOrthogonality_v2
import TGLExt.O16.ModularChargeLink
import TGLExt.O16.PenaltyThreeLocksBridge_v2
import TGLExt.O16.PeriodHeatCalibration_v3
import TGLExt.O16.ReaderPositive_v2
import TGLExt.O16.RetaDeLuzBorchersAudited
import TGLExt.O16.SameSquareDomain
import TGLExt.O16.ScalarGraphRealization_v3
import TGLExt.O16.TeleologicalShift_v3
import TGLExt.O16.UnboundedTransformEnergy
import TGLExt.ObserverInside
import TGLExt.PeriodAverageOperator
import TGLExt.PlaneWaveConnection
import TGLExt.PlaneWaveReconstructionControls
import TGLExt.ProbabilityRecordState
import TGLExt.RelativeFilterInverse
import TGLExt.SmoothGeodesicFlow
import TGLExt.SolderField
import TGLExt.SpectralMetricGeometry
import TGLExt.StateClockObstruction
import TGLExt.SummableRelativeQuartic
import TGLExt.TheAngleReachesTheMetric
import TGLExt.TheBoundaryDuality
import TGLExt.TheCompletionExtension
import TGLExt.TheCostIsDerived
import TGLExt.TheDammingByExpansion
import TGLExt.TheLivingWord
import TGLExt.TheMatrixRule
import TGLExt.TheModularRelations
import TGLExt.TheNameAndItsReferent
import TGLExt.TheNameIsTheInstrument
import TGLExt.TheNameOperator
import TGLExt.TheTowerWitnessLinear
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheTrueWitness
import TGLExt.TheTwoPairings
import TGLExt.TheUnsolicitedUnitary
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TowerHilbert
import TGLExt.TransportWitness
import TGLExt.TwoLevelSchrodinger
import TGLExt.UnitaryClausiusBridge
import TGLExt.UnitaryEntropyResponse
import TGLExt.V350AntilinearComposition
import TGLExt.V350ConstantFibreCandidate
import TGLExt.V350ContractionAdjointLimit
import TGLExt.V350CorePolarInclusion
import TGLExt.V350DualFixedWeightLaws
import TGLExt.V350DualResolventFixed
import TGLExt.V350DualSquareRootFormBound
import TGLExt.V350FiniteSetFibreRead
import TGLExt.V350FixedCoreShiftCommutation
import TGLExt.V350FourierL1L2
import TGLExt.V350L2CharacterMultiplier
import TGLExt.V350MatrixUnitPolarCommutation
import TGLExt.V350PositiveRootIntertwining
import TGLExt.V350RegularScalarWeightCertificate
import TGLExt.V350ResolventSquareRoot
import TGLExt.V350ScalarPairedProjectionBlocks
import TGLExt.V350ScalarRightFunctionalStability
import TGLExt.V350ScalarRightPairVector
import TGLExt.V350ScalarTomitaGraph
import TGLExt.V350ScalarTomitaSquare
import TGLExt.V350StrongBoundedApplication
import TGLExt.V350WedgeModularData
import TGLExt.V351FourierTranslation
import TGLExt.V351PerturbedWeightNorm
import TGLExt.V351RegularGeneratorAffiliation
import TGLExt.V351ResolventPhaseFunctions
import TGLExt.V351ScaledResolventCalculus
import TGLExt.VariationalFlow
import TGLExt.WedgeNet

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL.HalfNatJonesTower, `TGL.Main, `TGLExt.AQFTCoreInhabitant, `TGLExt.AffineClockAndRegion, `TGLExt.AngularAreaObservability, `TGLExt.AngularScreenMetric, `TGLExt.BondLocalityEstimates, `TGLExt.ChainVolumePositive, `TGLExt.ConcreteFourFrame, `TGLExt.ConstructedHeatPrimitive, `TGLExt.ExpectationBounded, `TGLExt.ExpectationContinuity, `TGLExt.FLRWGeometry, `TGLExt.FiniteLevelExponentials, `TGLExt.GeodesicInitialRegularity, `TGLExt.HermitianConeRigidity, `TGLExt.HorizonGNSImplementation, `TGLExt.HorizontalAreaSelection, `TGLExt.IsotoneNet, `TGLExt.LeftRight, `TGLExt.LocalCentralizerExpectation, `TGLExt.LocalFilterLorentzAction, `TGLExt.MicroscopicClausiusBridge, `TGLExt.ModularFlowLevel, `TGLExt.ModulatorSelfAdjoint, `TGLExt.O16.AxiomasContorno, `TGLExt.O16.ContractGroupI_v3, `TGLExt.O16.ExactTypeReader_v2, `TGLExt.O16.GudermannSpectral, `TGLExt.O16.LightRayGaussianOrthogonality_v2, `TGLExt.O16.ModularChargeLink, `TGLExt.O16.PenaltyThreeLocksBridge_v2, `TGLExt.O16.PeriodHeatCalibration_v3, `TGLExt.O16.ReaderPositive_v2, `TGLExt.O16.RetaDeLuzBorchersAudited, `TGLExt.O16.SameSquareDomain, `TGLExt.O16.ScalarGraphRealization_v3, `TGLExt.O16.TeleologicalShift_v3, `TGLExt.O16.UnboundedTransformEnergy, `TGLExt.ObserverInside, `TGLExt.PeriodAverageOperator, `TGLExt.PlaneWaveConnection, `TGLExt.PlaneWaveReconstructionControls, `TGLExt.ProbabilityRecordState, `TGLExt.RelativeFilterInverse, `TGLExt.SmoothGeodesicFlow, `TGLExt.SolderField, `TGLExt.SpectralMetricGeometry, `TGLExt.StateClockObstruction, `TGLExt.SummableRelativeQuartic, `TGLExt.TheAngleReachesTheMetric, `TGLExt.TheBoundaryDuality, `TGLExt.TheCompletionExtension, `TGLExt.TheCostIsDerived, `TGLExt.TheDammingByExpansion, `TGLExt.TheLivingWord, `TGLExt.TheMatrixRule, `TGLExt.TheModularRelations, `TGLExt.TheNameAndItsReferent, `TGLExt.TheNameIsTheInstrument, `TGLExt.TheNameOperator, `TGLExt.TheTowerWitnessLinear, `TGLExt.TheTraceIsNotErasable, `TGLExt.TheTrueWitness, `TGLExt.TheTwoPairings, `TGLExt.TheUnsolicitedUnitary, `TGLExt.TheVerbSelectsTheAction, `TGLExt.TowerHilbert, `TGLExt.TransportWitness, `TGLExt.TwoLevelSchrodinger, `TGLExt.UnitaryClausiusBridge, `TGLExt.UnitaryEntropyResponse, `TGLExt.V350AntilinearComposition, `TGLExt.V350ConstantFibreCandidate, `TGLExt.V350ContractionAdjointLimit, `TGLExt.V350CorePolarInclusion, `TGLExt.V350DualFixedWeightLaws, `TGLExt.V350DualResolventFixed, `TGLExt.V350DualSquareRootFormBound, `TGLExt.V350FiniteSetFibreRead, `TGLExt.V350FixedCoreShiftCommutation, `TGLExt.V350FourierL1L2, `TGLExt.V350L2CharacterMultiplier, `TGLExt.V350MatrixUnitPolarCommutation, `TGLExt.V350PositiveRootIntertwining, `TGLExt.V350RegularScalarWeightCertificate, `TGLExt.V350ResolventSquareRoot, `TGLExt.V350ScalarPairedProjectionBlocks, `TGLExt.V350ScalarRightFunctionalStability, `TGLExt.V350ScalarRightPairVector, `TGLExt.V350ScalarTomitaGraph, `TGLExt.V350ScalarTomitaSquare, `TGLExt.V350StrongBoundedApplication, `TGLExt.V350WedgeModularData, `TGLExt.V351FourierTranslation, `TGLExt.V351PerturbedWeightNorm, `TGLExt.V351RegularGeneratorAffiliation, `TGLExt.V351ResolventPhaseFunctions, `TGLExt.V351ScaledResolventCalculus, `TGLExt.VariationalFlow, `TGLExt.WedgeNet]
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
