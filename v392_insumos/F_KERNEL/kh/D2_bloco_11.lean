-- KH-N1 D2 bloco 11/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.ApproximateBoostFlow
import TGLExt.BinaryRelativeQuartic
import TGLExt.BisognanoWichmann
import TGLExt.BoundedPositiveCongruence
import TGLExt.CentralScalarPhase
import TGLExt.ConeVolumeReconstruction
import TGLExt.ConjugateAct
import TGLExt.CurvatureControls
import TGLExt.DensityStateUniqueness
import TGLExt.ExpectationPositive
import TGLExt.ExpectationProjection
import TGLExt.FaithfulGeometricLocalization
import TGLExt.FlowGermUniqueness
import TGLExt.FlowSmoothGerm
import TGLExt.GeneralSourceEinsteinBridge
import TGLExt.GibbsMatterBridge
import TGLExt.GibbsSamplingWindow
import TGLExt.JointPreparationCovariance
import TGLExt.JointUnitaryPreparation
import TGLExt.LevelExpectationFamily
import TGLExt.LeviCivitaLieVariation
import TGLExt.LieMetricJets
import TGLExt.LightHelicityWigner
import TGLExt.LightOneParticleByTerm
import TGLExt.LikelihoodStateCovariance
import TGLExt.MixedGibbsFiniteAccuracy
import TGLExt.ModulatorPolar
import TGLExt.NoFullWitness
import TGLExt.NoNormalTrace
import TGLExt.NotIsEmptyWitness
import TGLExt.NullCongruenceField
import TGLExt.O16.ConstructedImportH3_v2
import TGLExt.O16.ContractCalibrationReuse
import TGLExt.O16.ContractGroupD_v3
import TGLExt.O16.DilationGeometry_v2
import TGLExt.O16.ExistingTraceCompletionAudit_v2
import TGLExt.O16.IsometricCocycleSpectrum_v2
import TGLExt.O16.OrbitTranslationFaithfulness_v2
import TGLExt.O16.OrbitalBoostUnitary_v2
import TGLExt.O16.ProbeFieldMutations_v2
import TGLExt.O16.ProbeForgedStressContract
import TGLExt.O16.RecognitionGraph_v2
import TGLExt.O16.ScreenMetricAlgebra_v3
import TGLExt.O16.TheEquationOfTruth_T20_controles_v3_Integration_v2
import TGLExt.O16.TheEquationOfTruth_T20_v3
import TGLExt.O16.TransverseCocycle_v3
import TGLExt.OpticalEquilibriumScreen
import TGLExt.OpticalNullCongruence
import TGLExt.PlaneWaveMatter
import TGLExt.PolarizerModularCost
import TGLExt.ProfileFactorTransport
import TGLExt.ProfileFlowTransport
import TGLExt.QuadraticGibbsCurve
import TGLExt.QuadraticStateResponse
import TGLExt.QuarticMatchingClockControls
import TGLExt.RelativeProfilePreparation
import TGLExt.RightMult
import TGLExt.SaturatedWitness
import TGLExt.SecondCone
import TGLExt.Solder4D
import TGLExt.SolvedEquation
import TGLExt.SpectatorCancellation
import TGLExt.SpectralReduction
import TGLExt.SummableProfileCurve
import TGLExt.TheAnchorFour
import TGLExt.TheCoordinateBridge
import TGLExt.TheCornerEmbedding
import TGLExt.TheCurrentConnectsTheCorners
import TGLExt.TheReservedConfirmation
import TGLExt.TheRootOfTheProofTree
import TGLExt.TheTopologicalFace
import TGLExt.UnitaryCocycleUniqueness
import TGLExt.V350BoundedDualValues
import TGLExt.V350ConstantFibreIdentification
import TGLExt.V350DualFixedFormAffiliation
import TGLExt.V350DualSupportOperator
import TGLExt.V350L2StrongContinuity
import TGLExt.V350LevelExpectationStrongLimit
import TGLExt.V350MatrixUnitRootScaling
import TGLExt.V350PositiveFormCone
import TGLExt.V350RegularNormality
import TGLExt.V350ScalarBoundedCuts
import TGLExt.V350ScalarCommutantRegularization
import TGLExt.V350ScalarCutVectorFunctional
import TGLExt.V350ScalarGaussianClosureTransport
import TGLExt.V350ScalarGaussianUnitary
import TGLExt.V350ScalarHomogeneousRightGNS
import TGLExt.V350ScalarRegularPolarCommutation
import TGLExt.V350ScalarRegularRightPolar
import TGLExt.V350ScalarRightGraphCore
import TGLExt.V350ScalarRightProjectionPair
import TGLExt.V350ScalarTomitaPolarInvolution
import TGLExt.V350ScalarTomitaRootGraphCore
import TGLExt.V350ScalarTomitaSelfAdjoint
import TGLExt.V350ScalarWeightTomitaIdentification
import TGLExt.V350ScalarWeightedProjectionTest
import TGLExt.V351AntiunitaryResolventPhase
import TGLExt.V351ScalarRightActionLimits
import TGLExt.V354FiniteTraceSupport
import TGLExt.V354TraceShiftEquivalence

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.ApproximateBoostFlow, `TGLExt.BinaryRelativeQuartic, `TGLExt.BisognanoWichmann, `TGLExt.BoundedPositiveCongruence, `TGLExt.CentralScalarPhase, `TGLExt.ConeVolumeReconstruction, `TGLExt.ConjugateAct, `TGLExt.CurvatureControls, `TGLExt.DensityStateUniqueness, `TGLExt.ExpectationPositive, `TGLExt.ExpectationProjection, `TGLExt.FaithfulGeometricLocalization, `TGLExt.FlowGermUniqueness, `TGLExt.FlowSmoothGerm, `TGLExt.GeneralSourceEinsteinBridge, `TGLExt.GibbsMatterBridge, `TGLExt.GibbsSamplingWindow, `TGLExt.JointPreparationCovariance, `TGLExt.JointUnitaryPreparation, `TGLExt.LevelExpectationFamily, `TGLExt.LeviCivitaLieVariation, `TGLExt.LieMetricJets, `TGLExt.LightHelicityWigner, `TGLExt.LightOneParticleByTerm, `TGLExt.LikelihoodStateCovariance, `TGLExt.MixedGibbsFiniteAccuracy, `TGLExt.ModulatorPolar, `TGLExt.NoFullWitness, `TGLExt.NoNormalTrace, `TGLExt.NotIsEmptyWitness, `TGLExt.NullCongruenceField, `TGLExt.O16.ConstructedImportH3_v2, `TGLExt.O16.ContractCalibrationReuse, `TGLExt.O16.ContractGroupD_v3, `TGLExt.O16.DilationGeometry_v2, `TGLExt.O16.ExistingTraceCompletionAudit_v2, `TGLExt.O16.IsometricCocycleSpectrum_v2, `TGLExt.O16.OrbitTranslationFaithfulness_v2, `TGLExt.O16.OrbitalBoostUnitary_v2, `TGLExt.O16.ProbeFieldMutations_v2, `TGLExt.O16.ProbeForgedStressContract, `TGLExt.O16.RecognitionGraph_v2, `TGLExt.O16.ScreenMetricAlgebra_v3, `TGLExt.O16.TheEquationOfTruth_T20_controles_v3_Integration_v2, `TGLExt.O16.TheEquationOfTruth_T20_v3, `TGLExt.O16.TransverseCocycle_v3, `TGLExt.OpticalEquilibriumScreen, `TGLExt.OpticalNullCongruence, `TGLExt.PlaneWaveMatter, `TGLExt.PolarizerModularCost, `TGLExt.ProfileFactorTransport, `TGLExt.ProfileFlowTransport, `TGLExt.QuadraticGibbsCurve, `TGLExt.QuadraticStateResponse, `TGLExt.QuarticMatchingClockControls, `TGLExt.RelativeProfilePreparation, `TGLExt.RightMult, `TGLExt.SaturatedWitness, `TGLExt.SecondCone, `TGLExt.Solder4D, `TGLExt.SolvedEquation, `TGLExt.SpectatorCancellation, `TGLExt.SpectralReduction, `TGLExt.SummableProfileCurve, `TGLExt.TheAnchorFour, `TGLExt.TheCoordinateBridge, `TGLExt.TheCornerEmbedding, `TGLExt.TheCurrentConnectsTheCorners, `TGLExt.TheReservedConfirmation, `TGLExt.TheRootOfTheProofTree, `TGLExt.TheTopologicalFace, `TGLExt.UnitaryCocycleUniqueness, `TGLExt.V350BoundedDualValues, `TGLExt.V350ConstantFibreIdentification, `TGLExt.V350DualFixedFormAffiliation, `TGLExt.V350DualSupportOperator, `TGLExt.V350L2StrongContinuity, `TGLExt.V350LevelExpectationStrongLimit, `TGLExt.V350MatrixUnitRootScaling, `TGLExt.V350PositiveFormCone, `TGLExt.V350RegularNormality, `TGLExt.V350ScalarBoundedCuts, `TGLExt.V350ScalarCommutantRegularization, `TGLExt.V350ScalarCutVectorFunctional, `TGLExt.V350ScalarGaussianClosureTransport, `TGLExt.V350ScalarGaussianUnitary, `TGLExt.V350ScalarHomogeneousRightGNS, `TGLExt.V350ScalarRegularPolarCommutation, `TGLExt.V350ScalarRegularRightPolar, `TGLExt.V350ScalarRightGraphCore, `TGLExt.V350ScalarRightProjectionPair, `TGLExt.V350ScalarTomitaPolarInvolution, `TGLExt.V350ScalarTomitaRootGraphCore, `TGLExt.V350ScalarTomitaSelfAdjoint, `TGLExt.V350ScalarWeightTomitaIdentification, `TGLExt.V350ScalarWeightedProjectionTest, `TGLExt.V351AntiunitaryResolventPhase, `TGLExt.V351ScalarRightActionLimits, `TGLExt.V354FiniteTraceSupport, `TGLExt.V354TraceShiftEquivalence]
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
