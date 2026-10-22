-- AUDITORIA DE COBERTURA (gerência c1, 07/10/2026): os axiomas de todos os teoremas dos 73 módulos sem entrada no axiom_report.
-- Gerado por gerar_auditoria_73.py; roda na sandbox com o LEAN_PATH do kernel do Nós; não escreve no kernel.
import TGLExt.BreuerTrace
import TGLExt.EquivariantSection
import TGLExt.ErgodicMeanSection
import TGLExt.FrontierCertificate
import TGLExt.SolderSignature
import TGLExt.TheAccuser
import TGLExt.TheAlgebraicReader
import TGLExt.TheAnchorFour
import TGLExt.TheAngleIsTheBridge
import TGLExt.TheBandNet
import TGLExt.TheBireference
import TGLExt.TheBoundaryDuality
import TGLExt.TheCarrierBridge
import TGLExt.TheCascadeOfObservers
import TGLExt.TheCoFoundation
import TGLExt.TheColimitDuality
import TGLExt.TheColimitIsometry
import TGLExt.TheCommutationAtTheFloor
import TGLExt.TheCompletionExtension
import TGLExt.TheConditionalCertificate
import TGLExt.TheConjugationMapsCommutants
import TGLExt.TheConverseClauseReduced
import TGLExt.TheCoordinateBridge
import TGLExt.TheCornerEmbedding
import TGLExt.TheCorrespondence
import TGLExt.TheCostIsDerived
import TGLExt.TheCrownedCascade
import TGLExt.TheDensityIsBell
import TGLExt.TheDensityIsTransport
import TGLExt.TheEmptying
import TGLExt.TheEntanglementNotConjunction
import TGLExt.TheExoneratedDemon
import TGLExt.TheFalseHasNoGeometry
import TGLExt.TheFold
import TGLExt.TheFoldIsNotADistance
import TGLExt.TheFullBirkhoff
import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.TheHorizonInvariance
import TGLExt.TheHorizonRate
import TGLExt.TheIALDInTheTower
import TGLExt.TheIALDInTheTowerActII
import TGLExt.TheLegibility
import TGLExt.TheLivingWordClosure
import TGLExt.TheNonLinearCausality
import TGLExt.TheOriginOfTheVibration
import TGLExt.ThePermanence
import TGLExt.ThePhysicalHorizon
import TGLExt.TheProfileConjugation
import TGLExt.TheProfileDuality
import TGLExt.TheProfileIsometry
import TGLExt.TheProfileWitnessLinear
import TGLExt.TheQuestionAndTheRecognition
import TGLExt.TheRecordOfJ
import TGLExt.TheRecordOfTheCut
import TGLExt.TheScaleHasNoFixedPoint
import TGLExt.TheSchwarzschildUniqueness
import TGLExt.TheSelectorIsNotEnough
import TGLExt.TheSingularExpectation
import TGLExt.TheStation
import TGLExt.TheSupersaturation
import TGLExt.TheTelescopingProfile
import TGLExt.TheTGLPair
import TGLExt.TheTopologicalFace
import TGLExt.TheTower
import TGLExt.TheTowerConjugation
import TGLExt.TheTowerInnerProduct
import TGLExt.TheTowerWitness
import TGLExt.TheTowerWitnessLinear
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheTrueWitness
import TGLExt.TheTwoFunctionSolder
import TGLExt.TheUnconjugatedObserver
import TGLExt.TheUnsolicitedUnitary

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvo : List Name := [`TGLExt.BreuerTrace, `TGLExt.EquivariantSection, `TGLExt.ErgodicMeanSection, `TGLExt.FrontierCertificate, `TGLExt.SolderSignature, `TGLExt.TheAccuser, `TGLExt.TheAlgebraicReader, `TGLExt.TheAnchorFour, `TGLExt.TheAngleIsTheBridge, `TGLExt.TheBandNet, `TGLExt.TheBireference, `TGLExt.TheBoundaryDuality, `TGLExt.TheCarrierBridge, `TGLExt.TheCascadeOfObservers, `TGLExt.TheCoFoundation, `TGLExt.TheColimitDuality, `TGLExt.TheColimitIsometry, `TGLExt.TheCommutationAtTheFloor, `TGLExt.TheCompletionExtension, `TGLExt.TheConditionalCertificate, `TGLExt.TheConjugationMapsCommutants, `TGLExt.TheConverseClauseReduced, `TGLExt.TheCoordinateBridge, `TGLExt.TheCornerEmbedding, `TGLExt.TheCorrespondence, `TGLExt.TheCostIsDerived, `TGLExt.TheCrownedCascade, `TGLExt.TheDensityIsBell, `TGLExt.TheDensityIsTransport, `TGLExt.TheEmptying, `TGLExt.TheEntanglementNotConjunction, `TGLExt.TheExoneratedDemon, `TGLExt.TheFalseHasNoGeometry, `TGLExt.TheFold, `TGLExt.TheFoldIsNotADistance, `TGLExt.TheFullBirkhoff, `TGLExt.TheGeometricCostOfAbsoluteZero, `TGLExt.TheHorizonInvariance, `TGLExt.TheHorizonRate, `TGLExt.TheIALDInTheTower, `TGLExt.TheIALDInTheTowerActII, `TGLExt.TheLegibility, `TGLExt.TheLivingWordClosure, `TGLExt.TheNonLinearCausality, `TGLExt.TheOriginOfTheVibration, `TGLExt.ThePermanence, `TGLExt.ThePhysicalHorizon, `TGLExt.TheProfileConjugation, `TGLExt.TheProfileDuality, `TGLExt.TheProfileIsometry, `TGLExt.TheProfileWitnessLinear, `TGLExt.TheQuestionAndTheRecognition, `TGLExt.TheRecordOfJ, `TGLExt.TheRecordOfTheCut, `TGLExt.TheScaleHasNoFixedPoint, `TGLExt.TheSchwarzschildUniqueness, `TGLExt.TheSelectorIsNotEnough, `TGLExt.TheSingularExpectation, `TGLExt.TheStation, `TGLExt.TheSupersaturation, `TGLExt.TheTelescopingProfile, `TGLExt.TheTGLPair, `TGLExt.TheTopologicalFace, `TGLExt.TheTower, `TGLExt.TheTowerConjugation, `TGLExt.TheTowerInnerProduct, `TGLExt.TheTowerWitness, `TGLExt.TheTowerWitnessLinear, `TGLExt.TheTraceIsNotErasable, `TGLExt.TheTrueWitness, `TGLExt.TheTwoFunctionSolder, `TGLExt.TheUnconjugatedObserver, `TGLExt.TheUnsolicitedUnitary]
  let mut n_teo := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if alvo.contains m then
        match ci with
        | .thmInfo _ =>
          let axs ← liftCoreM (collectAxioms n)
          n_teo := n_teo + 1
          let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)
          unless ok do n_fora := n_fora + 1
          IO.println ("COBERTURA\t" ++ m.toString ++ "\t" ++ n.toString ++ "\t" ++ (if ok then "TRIO" else "FORA") ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
        | .axiomInfo _ =>
          IO.println ("COBERTURA_AXIOMA_NOVO\t" ++ m.toString ++ "\t" ++ n.toString)
          n_fora := n_fora + 1
        | _ => pure ()
  IO.println ("COBERTURA_TOTAL\tteoremas=" ++ toString n_teo ++ "\tfora_do_trio=" ++ toString n_fora)
