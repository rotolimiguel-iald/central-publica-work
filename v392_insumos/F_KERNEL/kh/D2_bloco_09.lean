-- KH-N1 D2 bloco 9/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL.SpecificAQFTWitness
import TGLExt.AperiodicAveragePrefix
import TGLExt.BicommutantSkeleton
import TGLExt.CentralizerRemainderPerturbation
import TGLExt.ChainSiteFlow
import TGLExt.Commutant
import TGLExt.ConjugateWitness
import TGLExt.ContinuousModularZero
import TGLExt.CoordinateCurvature
import TGLExt.CovariantVectorCalculus
import TGLExt.CurvatureJetAlgebra
import TGLExt.DiagonalRelativeEntropy
import TGLExt.EmergentEinstein
import TGLExt.EquilibriumCongruenceControls
import TGLExt.EquilibriumScreenIntegration
import TGLExt.ExpectationAlgebra
import TGLExt.FiniteCharacterResolution
import TGLExt.FiniteCurvatureAlgebra
import TGLExt.FlowDifferentiabilityControls
import TGLExt.FlowLinearizationError
import TGLExt.GeneralExpectationCP
import TGLExt.GeneralMetricEinstein
import TGLExt.GeometricAreaHorizon
import TGLExt.GeometricScreenControls
import TGLExt.GibbsAffinity
import TGLExt.HermitianLocalCoordinates
import TGLExt.IALDRhoStar
import TGLExt.InfiniteWord
import TGLExt.JointCoherentGravitation
import TGLExt.LeviCivitaMetricVariation
import TGLExt.LightIsJ
import TGLExt.MixedQuadraticGibbsResponse
import TGLExt.ModularCurrent
import TGLExt.ModularFlowPre
import TGLExt.ModularOpticalIdentity
import TGLExt.ModularRemainderDensity
import TGLExt.O16.BoundedTransformKernel
import TGLExt.O16.ContractGroupB_v3
import TGLExt.O16.ContractTypeLoad
import TGLExt.O16.FiniteGapRate_v2
import TGLExt.O16.OrbitalL2Equivalence_v2
import TGLExt.O16.OrbitalMeasureSupport_v2
import TGLExt.O16.OrbitalPositiveEnergy_v3
import TGLExt.O16.PhotonModularRealization
import TGLExt.O16.ProbeForgedStress_v2
import TGLExt.O16.ProbeNonKMS_v3
import TGLExt.O16.QubitEntropyDerivative_v3
import TGLExt.O16.TeleologicalBoundary_v2
import TGLExt.O16.WedgeDraggedFrame_v6
import TGLExt.OperatorBlockRepresentation
import TGLExt.ProfileModularTransport
import TGLExt.ProfileTomitaTransport
import TGLExt.ProfileTransportControls
import TGLExt.ReducedEmergence
import TGLExt.RegularRep
import TGLExt.RelativeEntropyProductBounds
import TGLExt.RelativeModularOperator
import TGLExt.RenormalizedNegativeExpectation
import TGLExt.ScaleCurrent
import TGLExt.ScreenFrameCompletion
import TGLExt.SectorFriedmannAdditive
import TGLExt.SiteModularInvariance
import TGLExt.SmoothSelectedAtlasGluing
import TGLExt.SummableInteractionModularOrbit
import TGLExt.SymplecticPolarizer
import TGLExt.TheClassicalImport
import TGLExt.TheExoneratedDemon
import TGLExt.TheFactorObject
import TGLExt.TheFalseHasNoGeometry
import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.TheImageAndTheReading
import TGLExt.TheNameIsTheCharacterization
import TGLExt.TheStation
import TGLExt.TheTwoFunctionSolder
import TGLExt.TheWeightIsNotTheRank
import TGLExt.TorsionShearDecay
import TGLExt.V350FibreSlices
import TGLExt.V350GraphCoreNormTransfer
import TGLExt.V350L2GaussianProfile
import TGLExt.V350L2OperatorLift
import TGLExt.V350OperatorFieldAlgebra
import TGLExt.V350PartialSelfadjointRange
import TGLExt.V350RealGraphCore
import TGLExt.V350RegularCoreCommutant
import TGLExt.V350RegularGeneratedAlgebra
import TGLExt.V350RegularTowerRepresentation
import TGLExt.V350ScalarGNSCompletion
import TGLExt.V350ScalarGaussianGNSMap
import TGLExt.V350ScalarHomogeneousRightOrbit
import TGLExt.V350ScalarRegularRightTomita
import TGLExt.V350ScalarTomitaBidual
import TGLExt.V350SquareResolventSupport
import TGLExt.V350StrongOperatorIntegral
import TGLExt.V350TranslationCorrelation
import TGLExt.V350UnitIntervalShiftProjection
import TGLExt.V351InverseLimitFaithful
import TGLExt.V351RegulatorWeightOrder
import TGLExt.V351ScalarTomitaImaginaryConjugation
import TGLExt.V354PositiveTraceTransport
import TGLExt.WitnessV3

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL.SpecificAQFTWitness, `TGLExt.AperiodicAveragePrefix, `TGLExt.BicommutantSkeleton, `TGLExt.CentralizerRemainderPerturbation, `TGLExt.ChainSiteFlow, `TGLExt.Commutant, `TGLExt.ConjugateWitness, `TGLExt.ContinuousModularZero, `TGLExt.CoordinateCurvature, `TGLExt.CovariantVectorCalculus, `TGLExt.CurvatureJetAlgebra, `TGLExt.DiagonalRelativeEntropy, `TGLExt.EmergentEinstein, `TGLExt.EquilibriumCongruenceControls, `TGLExt.EquilibriumScreenIntegration, `TGLExt.ExpectationAlgebra, `TGLExt.FiniteCharacterResolution, `TGLExt.FiniteCurvatureAlgebra, `TGLExt.FlowDifferentiabilityControls, `TGLExt.FlowLinearizationError, `TGLExt.GeneralExpectationCP, `TGLExt.GeneralMetricEinstein, `TGLExt.GeometricAreaHorizon, `TGLExt.GeometricScreenControls, `TGLExt.GibbsAffinity, `TGLExt.HermitianLocalCoordinates, `TGLExt.IALDRhoStar, `TGLExt.InfiniteWord, `TGLExt.JointCoherentGravitation, `TGLExt.LeviCivitaMetricVariation, `TGLExt.LightIsJ, `TGLExt.MixedQuadraticGibbsResponse, `TGLExt.ModularCurrent, `TGLExt.ModularFlowPre, `TGLExt.ModularOpticalIdentity, `TGLExt.ModularRemainderDensity, `TGLExt.O16.BoundedTransformKernel, `TGLExt.O16.ContractGroupB_v3, `TGLExt.O16.ContractTypeLoad, `TGLExt.O16.FiniteGapRate_v2, `TGLExt.O16.OrbitalL2Equivalence_v2, `TGLExt.O16.OrbitalMeasureSupport_v2, `TGLExt.O16.OrbitalPositiveEnergy_v3, `TGLExt.O16.PhotonModularRealization, `TGLExt.O16.ProbeForgedStress_v2, `TGLExt.O16.ProbeNonKMS_v3, `TGLExt.O16.QubitEntropyDerivative_v3, `TGLExt.O16.TeleologicalBoundary_v2, `TGLExt.O16.WedgeDraggedFrame_v6, `TGLExt.OperatorBlockRepresentation, `TGLExt.ProfileModularTransport, `TGLExt.ProfileTomitaTransport, `TGLExt.ProfileTransportControls, `TGLExt.ReducedEmergence, `TGLExt.RegularRep, `TGLExt.RelativeEntropyProductBounds, `TGLExt.RelativeModularOperator, `TGLExt.RenormalizedNegativeExpectation, `TGLExt.ScaleCurrent, `TGLExt.ScreenFrameCompletion, `TGLExt.SectorFriedmannAdditive, `TGLExt.SiteModularInvariance, `TGLExt.SmoothSelectedAtlasGluing, `TGLExt.SummableInteractionModularOrbit, `TGLExt.SymplecticPolarizer, `TGLExt.TheClassicalImport, `TGLExt.TheExoneratedDemon, `TGLExt.TheFactorObject, `TGLExt.TheFalseHasNoGeometry, `TGLExt.TheGeometricCostOfAbsoluteZero, `TGLExt.TheImageAndTheReading, `TGLExt.TheNameIsTheCharacterization, `TGLExt.TheStation, `TGLExt.TheTwoFunctionSolder, `TGLExt.TheWeightIsNotTheRank, `TGLExt.TorsionShearDecay, `TGLExt.V350FibreSlices, `TGLExt.V350GraphCoreNormTransfer, `TGLExt.V350L2GaussianProfile, `TGLExt.V350L2OperatorLift, `TGLExt.V350OperatorFieldAlgebra, `TGLExt.V350PartialSelfadjointRange, `TGLExt.V350RealGraphCore, `TGLExt.V350RegularCoreCommutant, `TGLExt.V350RegularGeneratedAlgebra, `TGLExt.V350RegularTowerRepresentation, `TGLExt.V350ScalarGNSCompletion, `TGLExt.V350ScalarGaussianGNSMap, `TGLExt.V350ScalarHomogeneousRightOrbit, `TGLExt.V350ScalarRegularRightTomita, `TGLExt.V350ScalarTomitaBidual, `TGLExt.V350SquareResolventSupport, `TGLExt.V350StrongOperatorIntegral, `TGLExt.V350TranslationCorrelation, `TGLExt.V350UnitIntervalShiftProjection, `TGLExt.V351InverseLimitFaithful, `TGLExt.V351RegulatorWeightOrder, `TGLExt.V351ScalarTomitaImaginaryConjugation, `TGLExt.V354PositiveTraceTransport, `TGLExt.WitnessV3]
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
