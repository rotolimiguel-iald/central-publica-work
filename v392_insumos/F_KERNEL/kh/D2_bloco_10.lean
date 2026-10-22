-- KH-N1 D2 bloco 10/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.AffineSamplingObstruction
import TGLExt.ClosedTomitaOperator
import TGLExt.ColimitSeed
import TGLExt.ConservativeNullResponse
import TGLExt.ContratoQG_v32
import TGLExt.CornerFamily
import TGLExt.CorrelatedUnitaryState
import TGLExt.DerivativeFromLinearCutoffError
import TGLExt.FiniteCoherentSources
import TGLExt.FlowRegularityInduction
import TGLExt.GeneralExpectationPositive
import TGLExt.GeneralLinearizedGauge
import TGLExt.GeneralMetricClausius
import TGLExt.GeneralTensorReconstruction
import TGLExt.IALDGraviton
import TGLExt.IntrinsicFisherClock
import TGLExt.JacobiRiccatiProfile
import TGLExt.LikelihoodPreparedState
import TGLExt.LocalInteractionData
import TGLExt.MinimalSolder
import TGLExt.ModularFlowAlgebra
import TGLExt.ModularProbe
import TGLExt.ModularRemainderAction
import TGLExt.NullScreenAlgebra
import TGLExt.O16.ClosedIndexChecks_v2
import TGLExt.O16.ClosedLinearGraphResolvent_v2
import TGLExt.O16.ContractGroupC_v3
import TGLExt.O16.ExistingTomitaAudit
import TGLExt.O16.OperatorContourBridge_v2_Integration_v2
import TGLExt.O16.OrbitalBoostTransport
import TGLExt.O16.OrbitalRapidityMeasure_v4
import TGLExt.O16.ProbePositiveEnergy_v2
import TGLExt.O16.TeleologicalContractBridge_v3
import TGLExt.O16.TeleologicalTail_v3
import TGLExt.OpticalHeatClausius
import TGLExt.OpticalScreenInvariant
import TGLExt.OpticalVolterraBalance
import TGLExt.OrientedBoundaryFace
import TGLExt.PauliPerturbedDynamics
import TGLExt.PeriodicCentralizerExpectation
import TGLExt.ProductBorchersObstruction
import TGLExt.ProfileAffinityBound
import TGLExt.RelativePhaseCharacter
import TGLExt.RhoPlusPClosure
import TGLExt.ScreenImportIntegration
import TGLExt.SelectedProbabilitySigma
import TGLExt.SmallTimeLocalDynamics
import TGLExt.StaticDynamicUnitary
import TGLExt.SummableGravityControls
import TGLExt.TheCarrierBridge
import TGLExt.TheCrownedCascade
import TGLExt.TheDebtWithoutJ
import TGLExt.TheDensityIsBell
import TGLExt.TheElementaryReason
import TGLExt.TheGravitonIsTheConjugatedPhase
import TGLExt.TheIdentityOfIdentity
import TGLExt.TheLivingWordClosure
import TGLExt.ThePermanence
import TGLExt.ThePsionAndTheViscosity
import TGLExt.TheRecordOfTheCut
import TGLExt.TheSingularExpectation
import TGLExt.TowerEntropyScaling
import TGLExt.TowerGibbsPerturbation
import TGLExt.TowerThermalOverlap
import TGLExt.TracelessAlgebra
import TGLExt.TransverseInitialData
import TGLExt.UnitaryDuhamel
import TGLExt.V350CharacterLocality
import TGLExt.V350FibreVonNeumann
import TGLExt.V350FixedBaseEquivalence
import TGLExt.V350HomogeneousRightSquareDomain
import TGLExt.V350PartialSquareGraphCore
import TGLExt.V350ScalarClosedTomita
import TGLExt.V350ScalarCutCyclicSpace
import TGLExt.V350ScalarCutNormality
import TGLExt.V350ScalarGaussianRightPairs
import TGLExt.V350ScalarGaussianVacuum
import TGLExt.V350ScalarPhaseVariational
import TGLExt.V350ScalarRightAverage
import TGLExt.V350ScalarRightConjugateGraph
import TGLExt.V350ScalarRightSquareApproximation
import TGLExt.V350ScalarRightStarGraph
import TGLExt.V350ScalarTomitaAdjointPolar
import TGLExt.V350ScalarTomitaPolarResolvent
import TGLExt.V350ScalarTomitaResolvent
import TGLExt.V350ScalarWeightCompletion
import TGLExt.V350SeparatingRestrictionVonNeumann
import TGLExt.V350TwistedCommutantField
import TGLExt.V350VectorTomitaClosability
import TGLExt.V351InverseGeneratorCutoff
import TGLExt.V351InverseLimitFiniteMinorants
import TGLExt.V351InverseLimitTracialExtension
import TGLExt.V351InverseLimitWeight
import TGLExt.V351ModularCutBalance
import TGLExt.V351RegularDomainCut
import TGLExt.V351RegularFlowAbsorption
import TGLExt.V351ScalarImaginaryCoreAction
import TGLExt.V354PositiveShiftCompatibility
import TGLExt.V354ProjectionTraceSubadditivity
import TGLExt.WordExistence

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.AffineSamplingObstruction, `TGLExt.ClosedTomitaOperator, `TGLExt.ColimitSeed, `TGLExt.ConservativeNullResponse, `TGLExt.ContratoQG_v32, `TGLExt.CornerFamily, `TGLExt.CorrelatedUnitaryState, `TGLExt.DerivativeFromLinearCutoffError, `TGLExt.FiniteCoherentSources, `TGLExt.FlowRegularityInduction, `TGLExt.GeneralExpectationPositive, `TGLExt.GeneralLinearizedGauge, `TGLExt.GeneralMetricClausius, `TGLExt.GeneralTensorReconstruction, `TGLExt.IALDGraviton, `TGLExt.IntrinsicFisherClock, `TGLExt.JacobiRiccatiProfile, `TGLExt.LikelihoodPreparedState, `TGLExt.LocalInteractionData, `TGLExt.MinimalSolder, `TGLExt.ModularFlowAlgebra, `TGLExt.ModularProbe, `TGLExt.ModularRemainderAction, `TGLExt.NullScreenAlgebra, `TGLExt.O16.ClosedIndexChecks_v2, `TGLExt.O16.ClosedLinearGraphResolvent_v2, `TGLExt.O16.ContractGroupC_v3, `TGLExt.O16.ExistingTomitaAudit, `TGLExt.O16.OperatorContourBridge_v2_Integration_v2, `TGLExt.O16.OrbitalBoostTransport, `TGLExt.O16.OrbitalRapidityMeasure_v4, `TGLExt.O16.ProbePositiveEnergy_v2, `TGLExt.O16.TeleologicalContractBridge_v3, `TGLExt.O16.TeleologicalTail_v3, `TGLExt.OpticalHeatClausius, `TGLExt.OpticalScreenInvariant, `TGLExt.OpticalVolterraBalance, `TGLExt.OrientedBoundaryFace, `TGLExt.PauliPerturbedDynamics, `TGLExt.PeriodicCentralizerExpectation, `TGLExt.ProductBorchersObstruction, `TGLExt.ProfileAffinityBound, `TGLExt.RelativePhaseCharacter, `TGLExt.RhoPlusPClosure, `TGLExt.ScreenImportIntegration, `TGLExt.SelectedProbabilitySigma, `TGLExt.SmallTimeLocalDynamics, `TGLExt.StaticDynamicUnitary, `TGLExt.SummableGravityControls, `TGLExt.TheCarrierBridge, `TGLExt.TheCrownedCascade, `TGLExt.TheDebtWithoutJ, `TGLExt.TheDensityIsBell, `TGLExt.TheElementaryReason, `TGLExt.TheGravitonIsTheConjugatedPhase, `TGLExt.TheIdentityOfIdentity, `TGLExt.TheLivingWordClosure, `TGLExt.ThePermanence, `TGLExt.ThePsionAndTheViscosity, `TGLExt.TheRecordOfTheCut, `TGLExt.TheSingularExpectation, `TGLExt.TowerEntropyScaling, `TGLExt.TowerGibbsPerturbation, `TGLExt.TowerThermalOverlap, `TGLExt.TracelessAlgebra, `TGLExt.TransverseInitialData, `TGLExt.UnitaryDuhamel, `TGLExt.V350CharacterLocality, `TGLExt.V350FibreVonNeumann, `TGLExt.V350FixedBaseEquivalence, `TGLExt.V350HomogeneousRightSquareDomain, `TGLExt.V350PartialSquareGraphCore, `TGLExt.V350ScalarClosedTomita, `TGLExt.V350ScalarCutCyclicSpace, `TGLExt.V350ScalarCutNormality, `TGLExt.V350ScalarGaussianRightPairs, `TGLExt.V350ScalarGaussianVacuum, `TGLExt.V350ScalarPhaseVariational, `TGLExt.V350ScalarRightAverage, `TGLExt.V350ScalarRightConjugateGraph, `TGLExt.V350ScalarRightSquareApproximation, `TGLExt.V350ScalarRightStarGraph, `TGLExt.V350ScalarTomitaAdjointPolar, `TGLExt.V350ScalarTomitaPolarResolvent, `TGLExt.V350ScalarTomitaResolvent, `TGLExt.V350ScalarWeightCompletion, `TGLExt.V350SeparatingRestrictionVonNeumann, `TGLExt.V350TwistedCommutantField, `TGLExt.V350VectorTomitaClosability, `TGLExt.V351InverseGeneratorCutoff, `TGLExt.V351InverseLimitFiniteMinorants, `TGLExt.V351InverseLimitTracialExtension, `TGLExt.V351InverseLimitWeight, `TGLExt.V351ModularCutBalance, `TGLExt.V351RegularDomainCut, `TGLExt.V351RegularFlowAbsorption, `TGLExt.V351ScalarImaginaryCoreAction, `TGLExt.V354PositiveShiftCompatibility, `TGLExt.V354ProjectionTraceSubadditivity, `TGLExt.WordExistence]
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
