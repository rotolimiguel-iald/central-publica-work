-- KH-N1 D2 bloco 4/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL.AreaScale
import TGL.Basic
import TGL.ContinuousCornerAbstract
import TGL.HalfNat
import TGL.VerbInhabitant
import TGLExt
import TGLExt.CentralizerLocal
import TGLExt.CharacterPrefixStability
import TGLExt.CoherentMatterControls
import TGLExt.ConstructedNullCongruence
import TGLExt.ContinuousModularReconstruction
import TGLExt.ContratoQG_v31_Teoremas
import TGLExt.CoordinateRaychaudhuri
import TGLExt.CovariantCorner
import TGLExt.CovariantScalarConservation
import TGLExt.DiagonalOperator
import TGLExt.EntropyGeometryControls
import TGLExt.Ergodicity
import TGLExt.ExistingTowerRealization
import TGLExt.ExpectationContractGap
import TGLExt.FiniteCoordinateCurvature
import TGLExt.FiniteModularHamiltonian
import TGLExt.FrontierCertificate
import TGLExt.GNSBridge
import TGLExt.GeneralNullCone
import TGLExt.GeneralSourceResponseReconstruction
import TGLExt.GeodesicFlowRegularity
import TGLExt.GibbsTilt
import TGLExt.GlobalProfileFaithfulness
import TGLExt.GravitonPolarization
import TGLExt.MixedLadder
import TGLExt.ModularSquareAdjoint
import TGLExt.NumberSelfAdjoint
import TGLExt.O16.ContinuousBoundedTransform
import TGLExt.O16.ContractGroupG_v3
import TGLExt.O16.DilationModularRecognition_v2
import TGLExt.O16.FiniteCenterFlow_v2
import TGLExt.O16.LightRayCoreExtension_v2
import TGLExt.O16.LightRayGaussianTransform_v5
import TGLExt.O16.NegativeControlsCompleteness_v2_Integration_v2
import TGLExt.O16.OrbitalTranslationOperators_v2
import TGLExt.O16.RecognitionInverse_v2
import TGLExt.O16.RecognitionSquare
import TGLExt.O16.UnboundedGraphTransform_v2
import TGLExt.O16.UnboundedTransformProjectionControl
import TGLExt.O16.WickBoostRotation_v2
import TGLExt.OpticalTidalScreen
import TGLExt.Order005Algebra
import TGLExt.PauliOperationalSurface
import TGLExt.PlaneWaveCurvature
import TGLExt.PoincareGroup
import TGLExt.PowersLadder
import TGLExt.QGCitationDischarge
import TGLExt.QGReaderUVLock
import TGLExt.QGSolutionComplete
import TGLExt.RelativeModularProduct
import TGLExt.Screen013NullFrame
import TGLExt.SectorFluidClosure
import TGLExt.SelectionOutcomeRecord
import TGLExt.SemifiniteSeed
import TGLExt.ShootingJetTransfer
import TGLExt.ShootingLocalInverse
import TGLExt.TensorNullCone
import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.TheCoFoundation
import TGLExt.TheCoinage
import TGLExt.TheColimitDuality
import TGLExt.TheCorrespondence
import TGLExt.TheDischargedOath
import TGLExt.TheFiveHalves
import TGLExt.TheFoldThroughJ
import TGLExt.TheMatrixAndTheModulator
import TGLExt.TheNonMinimalCoupling
import TGLExt.TheProfileConjugation
import TGLExt.TheSchwarzschildUniqueness
import TGLExt.TheStokesContour
import TGLExt.TheWideNet
import TGLExt.TheWitnessOnTheBoundary
import TGLExt.TriadMaster
import TGLExt.UniformQuadraticResponse
import TGLExt.V350AntiunitaryPositiveConjugation
import TGLExt.V350ClosedAntilinearResolvent
import TGLExt.V350DualClosedForm
import TGLExt.V350DualEnergyOnResolvent
import TGLExt.V350DualResolvent
import TGLExt.V350DualWeightExhaustion
import TGLExt.V350FormMinimizerUniqueness
import TGLExt.V350FourierUniqueness
import TGLExt.V350ReducingBicommutantLift
import TGLExt.V350ScalarCommutantSandwich
import TGLExt.V350ScalarGNSAction
import TGLExt.V350ScalarGNSGeneratorTransport
import TGLExt.V350ScalarGaussianImage
import TGLExt.V350ScalarRegularRightSquare
import TGLExt.V350ScalarTomitaGraphCore
import TGLExt.V351ModularImplementation
import TGLExt.V351ResolventPhaseCalculus
import TGLExt.V351ScalarGNSClosedness
import TGLExt.V354PolarIntertwining
import TGLExt.V354RegularLegacyWitness
import TGLExt.V354RegularSupport

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL.AreaScale, `TGL.Basic, `TGL.ContinuousCornerAbstract, `TGL.HalfNat, `TGL.VerbInhabitant, `TGLExt, `TGLExt.CentralizerLocal, `TGLExt.CharacterPrefixStability, `TGLExt.CoherentMatterControls, `TGLExt.ConstructedNullCongruence, `TGLExt.ContinuousModularReconstruction, `TGLExt.ContratoQG_v31_Teoremas, `TGLExt.CoordinateRaychaudhuri, `TGLExt.CovariantCorner, `TGLExt.CovariantScalarConservation, `TGLExt.DiagonalOperator, `TGLExt.EntropyGeometryControls, `TGLExt.Ergodicity, `TGLExt.ExistingTowerRealization, `TGLExt.ExpectationContractGap, `TGLExt.FiniteCoordinateCurvature, `TGLExt.FiniteModularHamiltonian, `TGLExt.FrontierCertificate, `TGLExt.GNSBridge, `TGLExt.GeneralNullCone, `TGLExt.GeneralSourceResponseReconstruction, `TGLExt.GeodesicFlowRegularity, `TGLExt.GibbsTilt, `TGLExt.GlobalProfileFaithfulness, `TGLExt.GravitonPolarization, `TGLExt.MixedLadder, `TGLExt.ModularSquareAdjoint, `TGLExt.NumberSelfAdjoint, `TGLExt.O16.ContinuousBoundedTransform, `TGLExt.O16.ContractGroupG_v3, `TGLExt.O16.DilationModularRecognition_v2, `TGLExt.O16.FiniteCenterFlow_v2, `TGLExt.O16.LightRayCoreExtension_v2, `TGLExt.O16.LightRayGaussianTransform_v5, `TGLExt.O16.NegativeControlsCompleteness_v2_Integration_v2, `TGLExt.O16.OrbitalTranslationOperators_v2, `TGLExt.O16.RecognitionInverse_v2, `TGLExt.O16.RecognitionSquare, `TGLExt.O16.UnboundedGraphTransform_v2, `TGLExt.O16.UnboundedTransformProjectionControl, `TGLExt.O16.WickBoostRotation_v2, `TGLExt.OpticalTidalScreen, `TGLExt.Order005Algebra, `TGLExt.PauliOperationalSurface, `TGLExt.PlaneWaveCurvature, `TGLExt.PoincareGroup, `TGLExt.PowersLadder, `TGLExt.QGCitationDischarge, `TGLExt.QGReaderUVLock, `TGLExt.QGSolutionComplete, `TGLExt.RelativeModularProduct, `TGLExt.Screen013NullFrame, `TGLExt.SectorFluidClosure, `TGLExt.SelectionOutcomeRecord, `TGLExt.SemifiniteSeed, `TGLExt.ShootingJetTransfer, `TGLExt.ShootingLocalInverse, `TGLExt.TensorNullCone, `TGLExt.TheAxiomAndTheFalseWitness, `TGLExt.TheCoFoundation, `TGLExt.TheCoinage, `TGLExt.TheColimitDuality, `TGLExt.TheCorrespondence, `TGLExt.TheDischargedOath, `TGLExt.TheFiveHalves, `TGLExt.TheFoldThroughJ, `TGLExt.TheMatrixAndTheModulator, `TGLExt.TheNonMinimalCoupling, `TGLExt.TheProfileConjugation, `TGLExt.TheSchwarzschildUniqueness, `TGLExt.TheStokesContour, `TGLExt.TheWideNet, `TGLExt.TheWitnessOnTheBoundary, `TGLExt.TriadMaster, `TGLExt.UniformQuadraticResponse, `TGLExt.V350AntiunitaryPositiveConjugation, `TGLExt.V350ClosedAntilinearResolvent, `TGLExt.V350DualClosedForm, `TGLExt.V350DualEnergyOnResolvent, `TGLExt.V350DualResolvent, `TGLExt.V350DualWeightExhaustion, `TGLExt.V350FormMinimizerUniqueness, `TGLExt.V350FourierUniqueness, `TGLExt.V350ReducingBicommutantLift, `TGLExt.V350ScalarCommutantSandwich, `TGLExt.V350ScalarGNSAction, `TGLExt.V350ScalarGNSGeneratorTransport, `TGLExt.V350ScalarGaussianImage, `TGLExt.V350ScalarRegularRightSquare, `TGLExt.V350ScalarTomitaGraphCore, `TGLExt.V351ModularImplementation, `TGLExt.V351ResolventPhaseCalculus, `TGLExt.V351ScalarGNSClosedness, `TGLExt.V354PolarIntertwining, `TGLExt.V354RegularLegacyWitness, `TGLExt.V354RegularSupport]
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
