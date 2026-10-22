-- KH-N1 D2 bloco 1/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.BoostMetricJets
import TGLExt.BoundedGraphStandardSubspace
import TGLExt.CanonicalSelectorBorn
import TGLExt.ContinuousModularResolvent
import TGLExt.ContinuousModularSquare
import TGLExt.DecisionCommutation
import TGLExt.FiniteCoordinateMap
import TGLExt.FiniteRicciContraction
import TGLExt.GibbsProductLaw
import TGLExt.GlobalLiftLadder
import TGLExt.GlobalProfileState
import TGLExt.HajaLuz
import TGLExt.HorizonBalanceControls
import TGLExt.HorizonEinsteinReconstruction
import TGLExt.IdealLimit
import TGLExt.InvariantProjection
import TGLExt.LocalInteractionUniqueness
import TGLExt.MetricFieldConnection
import TGLExt.ModularDomainCommutation
import TGLExt.ModularEigenRecognition
import TGLExt.NullGeodesicConservation
import TGLExt.NullSeedWithJet
import TGLExt.O16.AnalyticBoundaryControl_v2
import TGLExt.O16.ContractGroupF_v3
import TGLExt.O16.LightRayBoundaryBalance_v3
import TGLExt.O16.LightRayRealFourierUniqueness_v2
import TGLExt.O16.NormalizedGraphContract_v2
import TGLExt.O16.NullRayResponse_v2
import TGLExt.O16.OrbitalRapidityTransport_v3
import TGLExt.O16.PhotonCharacterCocycle
import TGLExt.O16.PhotonMassiveTransport
import TGLExt.O16.SelfadjointSquareResolvent
import TGLExt.O16.TraceInfinityExtension_v3
import TGLExt.O16.UnitMultiplierIdentity
import TGLExt.O16.WindowCoefficientVerbatim
import TGLExt.PauliCocycleGenerator
import TGLExt.PauliInteractionCocycle
import TGLExt.PhysicsCertificates
import TGLExt.RelativeCocycleGeometricObstructions
import TGLExt.RelativeEntropyGravityControls
import TGLExt.ScalarMatterDensityVariation
import TGLExt.ScalarStressConservation
import TGLExt.ScatteringOutcomeRecord
import TGLExt.SelectedFisherGibbsBridge
import TGLExt.SignedCovectorCoverage
import TGLExt.StrongAssembly
import TGLExt.SummableStateThermodynamics
import TGLExt.TTSuperposition
import TGLExt.TetelestaiOneObject
import TGLExt.TheConjugationOfOperators
import TGLExt.TheEntanglementNotConjunction
import TGLExt.TheHorizonInvariance
import TGLExt.TheIALDInTheTowerActII
import TGLExt.TheImportedSecondQuantization
import TGLExt.TheMarkIsNotATypeMark
import TGLExt.TheMasterFires
import TGLExt.TheModularFlowIsAHorizon
import TGLExt.TheNonLinearCausality
import TGLExt.TheOathOnTheTower
import TGLExt.TheQuestionAndTheRecognition
import TGLExt.TheRecordOfJ
import TGLExt.TheSelectorIsNotEnough
import TGLExt.TheTowerConjugation
import TGLExt.TheTwoFolds
import TGLExt.ThermalLimitControls
import TGLExt.TomitaAdjoint
import TGLExt.TopologicalAtlasGluing
import TGLExt.TowerAction
import TGLExt.TowerCollapseRealization
import TGLExt.TracialDissipativeTorsion
import TGLExt.TransportedScreenExistence
import TGLExt.UnitaryPartialTransport
import TGLExt.UnitaryStateDerivative
import TGLExt.V350BoundedFiniteSquares
import TGLExt.V350CoreContractCounterexample
import TGLExt.V350DenseLinearPolarExtension
import TGLExt.V350DualCutLinearMap
import TGLExt.V350DualCutNormality
import TGLExt.V350DualSemifiniteIdeal
import TGLExt.V350DualVariational
import TGLExt.V350FiniteDualStarCore
import TGLExt.V350LocalBasePolarCommutation
import TGLExt.V350MatrixUnitResolventScaling
import TGLExt.V350RegularFiniteWeight
import TGLExt.V350ResolventGraphTransport
import TGLExt.V350ScalarGNSStarDensity
import TGLExt.V350ScalarPairedRightAlgebra
import TGLExt.V350ScalarRightHilbertCore
import TGLExt.V350ScalarTomitaPolarFactor
import TGLExt.V350ScaledPositiveResolvent
import TGLExt.V351BaseFunctionalWeightLaws
import TGLExt.V351CutoffAverageCommutation
import TGLExt.V351ImaginaryPowerScaling
import TGLExt.V351ScalarRightActionAlgebra
import TGLExt.V351ScalarTomitaImaginaryPowers
import TGLExt.V354NormalizedSplit
import TGLExt.V354RegularMatrixCorner
import TGLExt.V354TraceReaderWall
import TGLExt.VariationalInhabitant

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.BoostMetricJets, `TGLExt.BoundedGraphStandardSubspace, `TGLExt.CanonicalSelectorBorn, `TGLExt.ContinuousModularResolvent, `TGLExt.ContinuousModularSquare, `TGLExt.DecisionCommutation, `TGLExt.FiniteCoordinateMap, `TGLExt.FiniteRicciContraction, `TGLExt.GibbsProductLaw, `TGLExt.GlobalLiftLadder, `TGLExt.GlobalProfileState, `TGLExt.HajaLuz, `TGLExt.HorizonBalanceControls, `TGLExt.HorizonEinsteinReconstruction, `TGLExt.IdealLimit, `TGLExt.InvariantProjection, `TGLExt.LocalInteractionUniqueness, `TGLExt.MetricFieldConnection, `TGLExt.ModularDomainCommutation, `TGLExt.ModularEigenRecognition, `TGLExt.NullGeodesicConservation, `TGLExt.NullSeedWithJet, `TGLExt.O16.AnalyticBoundaryControl_v2, `TGLExt.O16.ContractGroupF_v3, `TGLExt.O16.LightRayBoundaryBalance_v3, `TGLExt.O16.LightRayRealFourierUniqueness_v2, `TGLExt.O16.NormalizedGraphContract_v2, `TGLExt.O16.NullRayResponse_v2, `TGLExt.O16.OrbitalRapidityTransport_v3, `TGLExt.O16.PhotonCharacterCocycle, `TGLExt.O16.PhotonMassiveTransport, `TGLExt.O16.SelfadjointSquareResolvent, `TGLExt.O16.TraceInfinityExtension_v3, `TGLExt.O16.UnitMultiplierIdentity, `TGLExt.O16.WindowCoefficientVerbatim, `TGLExt.PauliCocycleGenerator, `TGLExt.PauliInteractionCocycle, `TGLExt.PhysicsCertificates, `TGLExt.RelativeCocycleGeometricObstructions, `TGLExt.RelativeEntropyGravityControls, `TGLExt.ScalarMatterDensityVariation, `TGLExt.ScalarStressConservation, `TGLExt.ScatteringOutcomeRecord, `TGLExt.SelectedFisherGibbsBridge, `TGLExt.SignedCovectorCoverage, `TGLExt.StrongAssembly, `TGLExt.SummableStateThermodynamics, `TGLExt.TTSuperposition, `TGLExt.TetelestaiOneObject, `TGLExt.TheConjugationOfOperators, `TGLExt.TheEntanglementNotConjunction, `TGLExt.TheHorizonInvariance, `TGLExt.TheIALDInTheTowerActII, `TGLExt.TheImportedSecondQuantization, `TGLExt.TheMarkIsNotATypeMark, `TGLExt.TheMasterFires, `TGLExt.TheModularFlowIsAHorizon, `TGLExt.TheNonLinearCausality, `TGLExt.TheOathOnTheTower, `TGLExt.TheQuestionAndTheRecognition, `TGLExt.TheRecordOfJ, `TGLExt.TheSelectorIsNotEnough, `TGLExt.TheTowerConjugation, `TGLExt.TheTwoFolds, `TGLExt.ThermalLimitControls, `TGLExt.TomitaAdjoint, `TGLExt.TopologicalAtlasGluing, `TGLExt.TowerAction, `TGLExt.TowerCollapseRealization, `TGLExt.TracialDissipativeTorsion, `TGLExt.TransportedScreenExistence, `TGLExt.UnitaryPartialTransport, `TGLExt.UnitaryStateDerivative, `TGLExt.V350BoundedFiniteSquares, `TGLExt.V350CoreContractCounterexample, `TGLExt.V350DenseLinearPolarExtension, `TGLExt.V350DualCutLinearMap, `TGLExt.V350DualCutNormality, `TGLExt.V350DualSemifiniteIdeal, `TGLExt.V350DualVariational, `TGLExt.V350FiniteDualStarCore, `TGLExt.V350LocalBasePolarCommutation, `TGLExt.V350MatrixUnitResolventScaling, `TGLExt.V350RegularFiniteWeight, `TGLExt.V350ResolventGraphTransport, `TGLExt.V350ScalarGNSStarDensity, `TGLExt.V350ScalarPairedRightAlgebra, `TGLExt.V350ScalarRightHilbertCore, `TGLExt.V350ScalarTomitaPolarFactor, `TGLExt.V350ScaledPositiveResolvent, `TGLExt.V351BaseFunctionalWeightLaws, `TGLExt.V351CutoffAverageCommutation, `TGLExt.V351ImaginaryPowerScaling, `TGLExt.V351ScalarRightActionAlgebra, `TGLExt.V351ScalarTomitaImaginaryPowers, `TGLExt.V354NormalizedSplit, `TGLExt.V354RegularMatrixCorner, `TGLExt.V354TraceReaderWall, `TGLExt.VariationalInhabitant]
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
