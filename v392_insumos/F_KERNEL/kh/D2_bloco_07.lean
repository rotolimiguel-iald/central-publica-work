-- KH-N1 D2 bloco 7/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL
import TGL.CoreSupport
import TGL.FiniteThreeLocks
import TGL.GravitonShadow
import TGL.TransportData
import TGLExt.BoundedGraphOperator
import TGLExt.CanonicalCocycleDerivative
import TGLExt.CoherentEinsteinBridge
import TGLExt.CoherentHeatMatching
import TGLExt.ContractedBianchi
import TGLExt.CurvatureNonlinearVariation
import TGLExt.DirectionalUnitaryFamily
import TGLExt.EquivariantSection
import TGLExt.FLRWFieldEquations
import TGLExt.FlagNetV31
import TGLExt.GenericAntilinearAdjoint
import TGLExt.GibbsProductVariance
import TGLExt.GibbsVarianceResponse
import TGLExt.GlobalFilterLocalReduction
import TGLExt.GravitationalResponseRecord
import TGLExt.MarkovTower
import TGLExt.MetricCompatibleJet
import TGLExt.MetricEinsteinVariation
import TGLExt.MetricRicciVariation
import TGLExt.MicroscopicEinsteinBridge
import TGLExt.MixedGibbsGravitationalBridge
import TGLExt.ModularCornerCounterexample
import TGLExt.ModularFirstLaw
import TGLExt.MonotoneOperatorLimit
import TGLExt.NoncommutingLocalWitness
import TGLExt.NullCongruenceControls
import TGLExt.NumberOperator
import TGLExt.O16.CanonicalResponseCovarianceAudit
import TGLExt.O16.ConjugatedFormScope_v2
import TGLExt.O16.ContractGroupJ_v5
import TGLExt.O16.IdempotentDephasing_v2
import TGLExt.O16.InscriptionBridge_Integration_v2
import TGLExt.O16.LightRayGaussianL1
import TGLExt.O16.ModularGeneratorControl
import TGLExt.O16.OrbitalBoostCovariance_v2
import TGLExt.O16.RecognitionModular_v2
import TGLExt.O16.SelfadjointAbsoluteRoot
import TGLExt.O16.TeleologicalUniqueness
import TGLExt.O16.UnboundedTransformConstruction_v2
import TGLExt.O16.WeightControls_v2
import TGLExt.PauliMeasurementFisher
import TGLExt.PhaseFrequencySeparation
import TGLExt.PlaneWaveEntropyMatching
import TGLExt.ProfileOverlapFactorization
import TGLExt.RetaDeLuzEspectro
import TGLExt.SelectedGravitationalAtlas
import TGLExt.SignatureInTheLimit
import TGLExt.SignedGibbsResponse
import TGLExt.SitePauliObservables
import TGLExt.SummableNullIntegrability
import TGLExt.SummablePauliInteraction
import TGLExt.TailNet
import TGLExt.TheDeathOfTheSignal
import TGLExt.TheEquationOfTruth
import TGLExt.TheFold
import TGLExt.TheFoldIsNotADistance
import TGLExt.TheGreatAttractor
import TGLExt.TheKeyIsTheReader
import TGLExt.TheLegibility
import TGLExt.TheLiftFiresOnThePeriodicTower
import TGLExt.TheObserverReadsTheAngle
import TGLExt.TheOriginOfTheVibration
import TGLExt.TheTerminalRankOne
import TGLExt.TheTowerInnerProduct
import TGLExt.TheTowerWitness
import TGLExt.TowerDefinite
import TGLExt.TowerExpectation
import TGLExt.TracialCentralizerExpectation
import TGLExt.UmPostoRelacao
import TGLExt.UnifiedRecordedPreparation
import TGLExt.V350DualFormFaithfulness
import TGLExt.V350DualFormNormality
import TGLExt.V350DualOrbitStrongLimits
import TGLExt.V350DualSquareRoot
import TGLExt.V350GeneratedEquivariance
import TGLExt.V350L2CutIntegral
import TGLExt.V350LevelExpectationUniformBound
import TGLExt.V350PositiveSurjectiveResolvent
import TGLExt.V350ResolventGraph
import TGLExt.V350ScalarGNSStrongContinuity
import TGLExt.V350ScalarRightMultiplicationGraph
import TGLExt.V350ScalarRightRegularization
import TGLExt.V350ScalarTomitaPositiveRoot
import TGLExt.V350ScalarWeightAction
import TGLExt.V350ScalarWeightSandwich
import TGLExt.V350ShiftCharacterAverage
import TGLExt.V350StrongOperatorField
import TGLExt.V351BaseFunctionalEvaluation
import TGLExt.V351BaseMoreauApproximants
import TGLExt.V351InverseLimitScaling
import TGLExt.V351PerturbedWeightOrder
import TGLExt.V351RegularGeneratorDualScaling
import TGLExt.V351ResolventImaginaryContinuity
import TGLExt.V351ScalarWeightSemifiniteness
import TGLExt.V354PositiveTraceReader
import TGLExt.V354SelfAdjointPowerKernel

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL, `TGL.CoreSupport, `TGL.FiniteThreeLocks, `TGL.GravitonShadow, `TGL.TransportData, `TGLExt.BoundedGraphOperator, `TGLExt.CanonicalCocycleDerivative, `TGLExt.CoherentEinsteinBridge, `TGLExt.CoherentHeatMatching, `TGLExt.ContractedBianchi, `TGLExt.CurvatureNonlinearVariation, `TGLExt.DirectionalUnitaryFamily, `TGLExt.EquivariantSection, `TGLExt.FLRWFieldEquations, `TGLExt.FlagNetV31, `TGLExt.GenericAntilinearAdjoint, `TGLExt.GibbsProductVariance, `TGLExt.GibbsVarianceResponse, `TGLExt.GlobalFilterLocalReduction, `TGLExt.GravitationalResponseRecord, `TGLExt.MarkovTower, `TGLExt.MetricCompatibleJet, `TGLExt.MetricEinsteinVariation, `TGLExt.MetricRicciVariation, `TGLExt.MicroscopicEinsteinBridge, `TGLExt.MixedGibbsGravitationalBridge, `TGLExt.ModularCornerCounterexample, `TGLExt.ModularFirstLaw, `TGLExt.MonotoneOperatorLimit, `TGLExt.NoncommutingLocalWitness, `TGLExt.NullCongruenceControls, `TGLExt.NumberOperator, `TGLExt.O16.CanonicalResponseCovarianceAudit, `TGLExt.O16.ConjugatedFormScope_v2, `TGLExt.O16.ContractGroupJ_v5, `TGLExt.O16.IdempotentDephasing_v2, `TGLExt.O16.InscriptionBridge_Integration_v2, `TGLExt.O16.LightRayGaussianL1, `TGLExt.O16.ModularGeneratorControl, `TGLExt.O16.OrbitalBoostCovariance_v2, `TGLExt.O16.RecognitionModular_v2, `TGLExt.O16.SelfadjointAbsoluteRoot, `TGLExt.O16.TeleologicalUniqueness, `TGLExt.O16.UnboundedTransformConstruction_v2, `TGLExt.O16.WeightControls_v2, `TGLExt.PauliMeasurementFisher, `TGLExt.PhaseFrequencySeparation, `TGLExt.PlaneWaveEntropyMatching, `TGLExt.ProfileOverlapFactorization, `TGLExt.RetaDeLuzEspectro, `TGLExt.SelectedGravitationalAtlas, `TGLExt.SignatureInTheLimit, `TGLExt.SignedGibbsResponse, `TGLExt.SitePauliObservables, `TGLExt.SummableNullIntegrability, `TGLExt.SummablePauliInteraction, `TGLExt.TailNet, `TGLExt.TheDeathOfTheSignal, `TGLExt.TheEquationOfTruth, `TGLExt.TheFold, `TGLExt.TheFoldIsNotADistance, `TGLExt.TheGreatAttractor, `TGLExt.TheKeyIsTheReader, `TGLExt.TheLegibility, `TGLExt.TheLiftFiresOnThePeriodicTower, `TGLExt.TheObserverReadsTheAngle, `TGLExt.TheOriginOfTheVibration, `TGLExt.TheTerminalRankOne, `TGLExt.TheTowerInnerProduct, `TGLExt.TheTowerWitness, `TGLExt.TowerDefinite, `TGLExt.TowerExpectation, `TGLExt.TracialCentralizerExpectation, `TGLExt.UmPostoRelacao, `TGLExt.UnifiedRecordedPreparation, `TGLExt.V350DualFormFaithfulness, `TGLExt.V350DualFormNormality, `TGLExt.V350DualOrbitStrongLimits, `TGLExt.V350DualSquareRoot, `TGLExt.V350GeneratedEquivariance, `TGLExt.V350L2CutIntegral, `TGLExt.V350LevelExpectationUniformBound, `TGLExt.V350PositiveSurjectiveResolvent, `TGLExt.V350ResolventGraph, `TGLExt.V350ScalarGNSStrongContinuity, `TGLExt.V350ScalarRightMultiplicationGraph, `TGLExt.V350ScalarRightRegularization, `TGLExt.V350ScalarTomitaPositiveRoot, `TGLExt.V350ScalarWeightAction, `TGLExt.V350ScalarWeightSandwich, `TGLExt.V350ShiftCharacterAverage, `TGLExt.V350StrongOperatorField, `TGLExt.V351BaseFunctionalEvaluation, `TGLExt.V351BaseMoreauApproximants, `TGLExt.V351InverseLimitScaling, `TGLExt.V351PerturbedWeightOrder, `TGLExt.V351RegularGeneratorDualScaling, `TGLExt.V351ResolventImaginaryContinuity, `TGLExt.V351ScalarWeightSemifiniteness, `TGLExt.V354PositiveTraceReader, `TGLExt.V354SelfAdjointPowerKernel]
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
