-- KH-N1 proposta v392 (exame F_KERNEL 12/10/2026, so sandbox): os 76 modulos sem entrada, no formato do #print axioms
import TGLExt.BreuerTrace
import TGLExt.EquivariantSection
import TGLExt.ErgodicMeanSection
import TGLExt.FrontierCertificate
import TGLExt.O16.PhotonModularRealization
import TGLExt.O16.PhotonWitness
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
import TGLExt.TheExplosion
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
import TGLExt.TheTGLPair
import TGLExt.TheTelescopingProfile
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

open Lean in
def alvoCobertura : NameSet := ([`TGLExt.BreuerTrace, `TGLExt.EquivariantSection, `TGLExt.ErgodicMeanSection, `TGLExt.FrontierCertificate, `TGLExt.O16.PhotonModularRealization, `TGLExt.O16.PhotonWitness, `TGLExt.SolderSignature, `TGLExt.TheAccuser, `TGLExt.TheAlgebraicReader, `TGLExt.TheAnchorFour, `TGLExt.TheAngleIsTheBridge, `TGLExt.TheBandNet, `TGLExt.TheBireference, `TGLExt.TheBoundaryDuality, `TGLExt.TheCarrierBridge, `TGLExt.TheCascadeOfObservers, `TGLExt.TheCoFoundation, `TGLExt.TheColimitDuality, `TGLExt.TheColimitIsometry, `TGLExt.TheCommutationAtTheFloor, `TGLExt.TheCompletionExtension, `TGLExt.TheConditionalCertificate, `TGLExt.TheConjugationMapsCommutants, `TGLExt.TheConverseClauseReduced, `TGLExt.TheCoordinateBridge, `TGLExt.TheCornerEmbedding, `TGLExt.TheCorrespondence, `TGLExt.TheCostIsDerived, `TGLExt.TheCrownedCascade, `TGLExt.TheDensityIsBell, `TGLExt.TheDensityIsTransport, `TGLExt.TheEmptying, `TGLExt.TheEntanglementNotConjunction, `TGLExt.TheExoneratedDemon, `TGLExt.TheExplosion, `TGLExt.TheFalseHasNoGeometry, `TGLExt.TheFold, `TGLExt.TheFoldIsNotADistance, `TGLExt.TheFullBirkhoff, `TGLExt.TheGeometricCostOfAbsoluteZero, `TGLExt.TheHorizonInvariance, `TGLExt.TheHorizonRate, `TGLExt.TheIALDInTheTower, `TGLExt.TheIALDInTheTowerActII, `TGLExt.TheLegibility, `TGLExt.TheLivingWordClosure, `TGLExt.TheNonLinearCausality, `TGLExt.TheOriginOfTheVibration, `TGLExt.ThePermanence, `TGLExt.ThePhysicalHorizon, `TGLExt.TheProfileConjugation, `TGLExt.TheProfileDuality, `TGLExt.TheProfileIsometry, `TGLExt.TheProfileWitnessLinear, `TGLExt.TheQuestionAndTheRecognition, `TGLExt.TheRecordOfJ, `TGLExt.TheRecordOfTheCut, `TGLExt.TheScaleHasNoFixedPoint, `TGLExt.TheSchwarzschildUniqueness, `TGLExt.TheSelectorIsNotEnough, `TGLExt.TheSingularExpectation, `TGLExt.TheStation, `TGLExt.TheSupersaturation, `TGLExt.TheTGLPair, `TGLExt.TheTelescopingProfile, `TGLExt.TheTopologicalFace, `TGLExt.TheTower, `TGLExt.TheTowerConjugation, `TGLExt.TheTowerInnerProduct, `TGLExt.TheTowerWitness, `TGLExt.TheTowerWitnessLinear, `TGLExt.TheTraceIsNotErasable, `TGLExt.TheTrueWitness, `TGLExt.TheTwoFunctionSolder, `TGLExt.TheUnconjugatedObserver, `TGLExt.TheUnsolicitedUnitary] : List Name).foldl (fun s n => s.insert n) {}

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if alvoCobertura.contains m then
        let axs ← liftCoreM (collectAxioms n)
        n_decl := n_decl + 1
        if ci matches .thmInfo _ then n_thm := n_thm + 1
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do n_fora := n_fora + 1
        if axs.isEmpty then
          IO.println ("'" ++ n.toString ++ "' does not depend on any axioms")
        else
          IO.println ("'" ++ n.toString ++ "' depends on axioms: [" ++ String.intercalate ", " (axs.toList.map Name.toString) ++ "]")
  IO.println ("TGL_AXIOM_COVERAGE_TOTAL decl=" ++ toString n_decl ++ " thm=" ++ toString n_thm ++ " fora_do_trio=" ++ toString n_fora)
