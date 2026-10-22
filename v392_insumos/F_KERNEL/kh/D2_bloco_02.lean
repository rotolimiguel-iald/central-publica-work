-- KH-N1 D2 bloco 2/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.AbsoluteOne
import TGLExt.AdmissiblePauliInteraction
import TGLExt.AffinityProducts
import TGLExt.AperiodicCentralizerExpectation
import TGLExt.BenchCertificate
import TGLExt.CartanTracialSupplier
import TGLExt.CentralizerContractBridge
import TGLExt.ChainSiteOperators
import TGLExt.ClosedAntilinearStandardSubspace
import TGLExt.Cocycle
import TGLExt.ConstructedClausiusControls
import TGLExt.ContinuousModularDomain
import TGLExt.ContratoQG_v31
import TGLExt.DiagonalStateCurve
import TGLExt.DiamondConformalCurrent
import TGLExt.DifferentialFlowExistence
import TGLExt.ErgodicMeanSection
import TGLExt.ExpectationSlice
import TGLExt.Fundacao
import TGLExt.GNSTower
import TGLExt.GeometricEinsteinReconstruction
import TGLExt.GeometricScreenTransport
import TGLExt.GlobalLiftConditional
import TGLExt.GlobalProfileControls
import TGLExt.HermitianTwoLevelFlow
import TGLExt.HilbertInhabitant
import TGLExt.InfiniteFisherGeometry
import TGLExt.JointCurvatureVariation
import TGLExt.LocalBreuerGap
import TGLExt.LocalHorizonBalance
import TGLExt.LocalTowerProjections
import TGLExt.ModularFlow
import TGLExt.ModulatorPositive
import TGLExt.NameIsTheContent
import TGLExt.O16.BoostHomonymBridge
import TGLExt.O16.BoundedTransformFinite_v2
import TGLExt.O16.BoundedTransformGap
import TGLExt.O16.EmptyImportControl
import TGLExt.O16.FiniteKMSStrip_v4
import TGLExt.O16.FourierLightRayBridge
import TGLExt.O16.LightRayFourierBoundary_v2
import TGLExt.O16.LightRayGaussianDensity_v2
import TGLExt.O16.LightRayTwistWidth_v3
import TGLExt.O16.LightRayVerticalDecay_v4
import TGLExt.O16.NullScreenFrame_v2
import TGLExt.O16.OrbitalPositiveEnergyContract
import TGLExt.O16.WindowLemmasVerbatim
import TGLExt.OpticalAreaFreedom
import TGLExt.OpticalFiniteBalance
import TGLExt.PageInformation
import TGLExt.PauliProbabilityModel
import TGLExt.PeriodAveragePrefix
import TGLExt.ProfileGNSPre
import TGLExt.QuarticClockTransport
import TGLExt.RecordCharacterMeshControl
import TGLExt.RetaDeLuzBorchers
import TGLExt.ScreenEntropyObstruction
import TGLExt.ScreenPairTransport
import TGLExt.SelectionAngleReconstruction
import TGLExt.SemifiniteLattice
import TGLExt.SemifiniteWeight
import TGLExt.SitePhaseCovariance
import TGLExt.SpatialScreenConstruction
import TGLExt.StrongFrame
import TGLExt.SummableLikelihoodGenerator
import TGLExt.TensorReconstructionControls
import TGLExt.TheAtermation
import TGLExt.TheCascadeOfObservers
import TGLExt.TheColimitIsometry
import TGLExt.TheImportedEquilibrium
import TGLExt.TheIntersectionOfCommutants
import TGLExt.TheJudgedThing
import TGLExt.ThePsionReducesToTheCurrent
import TGLExt.TheQuittanceLaw
import TGLExt.TheScalarCorner
import TGLExt.TheTwoPolesHaveContent
import TGLExt.TowerTailRigidity
import TGLExt.TransverseGibbsResponse
import TGLExt.V350BasePolarStrongLimit
import TGLExt.V350CompressionLimit
import TGLExt.V350DualOrbitRepresentation
import TGLExt.V350HomogeneousCommutantTransport
import TGLExt.V350HomogeneousRightData
import TGLExt.V350MatrixUnitPolarTransport
import TGLExt.V350ScalarCutGNSProperties
import TGLExt.V350ScalarGNSRepresentation
import TGLExt.V350ScalarModularInvariance
import TGLExt.V350ScalarRegularRightGNS
import TGLExt.V350ScalarWeightStarCore
import TGLExt.V350ScaledResolventRoots
import TGLExt.V350SeparatingCyclicCommutant
import TGLExt.V351AllPositiveWeightOrder
import TGLExt.V351QuadraticTrace
import TGLExt.V351RegularPositiveGraph
import TGLExt.V351ScalarImaginaryLeftTransport
import TGLExt.V354BoundedPolar
import TGLExt.V354CyclicTraceCompletion
import TGLExt.VectorCurvatureCommutator
import TGLExt.WitnessSeed

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.AbsoluteOne, `TGLExt.AdmissiblePauliInteraction, `TGLExt.AffinityProducts, `TGLExt.AperiodicCentralizerExpectation, `TGLExt.BenchCertificate, `TGLExt.CartanTracialSupplier, `TGLExt.CentralizerContractBridge, `TGLExt.ChainSiteOperators, `TGLExt.ClosedAntilinearStandardSubspace, `TGLExt.Cocycle, `TGLExt.ConstructedClausiusControls, `TGLExt.ContinuousModularDomain, `TGLExt.ContratoQG_v31, `TGLExt.DiagonalStateCurve, `TGLExt.DiamondConformalCurrent, `TGLExt.DifferentialFlowExistence, `TGLExt.ErgodicMeanSection, `TGLExt.ExpectationSlice, `TGLExt.Fundacao, `TGLExt.GNSTower, `TGLExt.GeometricEinsteinReconstruction, `TGLExt.GeometricScreenTransport, `TGLExt.GlobalLiftConditional, `TGLExt.GlobalProfileControls, `TGLExt.HermitianTwoLevelFlow, `TGLExt.HilbertInhabitant, `TGLExt.InfiniteFisherGeometry, `TGLExt.JointCurvatureVariation, `TGLExt.LocalBreuerGap, `TGLExt.LocalHorizonBalance, `TGLExt.LocalTowerProjections, `TGLExt.ModularFlow, `TGLExt.ModulatorPositive, `TGLExt.NameIsTheContent, `TGLExt.O16.BoostHomonymBridge, `TGLExt.O16.BoundedTransformFinite_v2, `TGLExt.O16.BoundedTransformGap, `TGLExt.O16.EmptyImportControl, `TGLExt.O16.FiniteKMSStrip_v4, `TGLExt.O16.FourierLightRayBridge, `TGLExt.O16.LightRayFourierBoundary_v2, `TGLExt.O16.LightRayGaussianDensity_v2, `TGLExt.O16.LightRayTwistWidth_v3, `TGLExt.O16.LightRayVerticalDecay_v4, `TGLExt.O16.NullScreenFrame_v2, `TGLExt.O16.OrbitalPositiveEnergyContract, `TGLExt.O16.WindowLemmasVerbatim, `TGLExt.OpticalAreaFreedom, `TGLExt.OpticalFiniteBalance, `TGLExt.PageInformation, `TGLExt.PauliProbabilityModel, `TGLExt.PeriodAveragePrefix, `TGLExt.ProfileGNSPre, `TGLExt.QuarticClockTransport, `TGLExt.RecordCharacterMeshControl, `TGLExt.RetaDeLuzBorchers, `TGLExt.ScreenEntropyObstruction, `TGLExt.ScreenPairTransport, `TGLExt.SelectionAngleReconstruction, `TGLExt.SemifiniteLattice, `TGLExt.SemifiniteWeight, `TGLExt.SitePhaseCovariance, `TGLExt.SpatialScreenConstruction, `TGLExt.StrongFrame, `TGLExt.SummableLikelihoodGenerator, `TGLExt.TensorReconstructionControls, `TGLExt.TheAtermation, `TGLExt.TheCascadeOfObservers, `TGLExt.TheColimitIsometry, `TGLExt.TheImportedEquilibrium, `TGLExt.TheIntersectionOfCommutants, `TGLExt.TheJudgedThing, `TGLExt.ThePsionReducesToTheCurrent, `TGLExt.TheQuittanceLaw, `TGLExt.TheScalarCorner, `TGLExt.TheTwoPolesHaveContent, `TGLExt.TowerTailRigidity, `TGLExt.TransverseGibbsResponse, `TGLExt.V350BasePolarStrongLimit, `TGLExt.V350CompressionLimit, `TGLExt.V350DualOrbitRepresentation, `TGLExt.V350HomogeneousCommutantTransport, `TGLExt.V350HomogeneousRightData, `TGLExt.V350MatrixUnitPolarTransport, `TGLExt.V350ScalarCutGNSProperties, `TGLExt.V350ScalarGNSRepresentation, `TGLExt.V350ScalarModularInvariance, `TGLExt.V350ScalarRegularRightGNS, `TGLExt.V350ScalarWeightStarCore, `TGLExt.V350ScaledResolventRoots, `TGLExt.V350SeparatingCyclicCommutant, `TGLExt.V351AllPositiveWeightOrder, `TGLExt.V351QuadraticTrace, `TGLExt.V351RegularPositiveGraph, `TGLExt.V351ScalarImaginaryLeftTransport, `TGLExt.V354BoundedPolar, `TGLExt.V354CyclicTraceCompletion, `TGLExt.VectorCurvatureCommutator, `TGLExt.WitnessSeed]
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
