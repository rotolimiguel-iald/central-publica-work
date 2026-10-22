-- KH-N1 D2 bloco 3/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.AffinityVectorCriterion
import TGLExt.AngularSelectorIntertwining
import TGLExt.AnsatzEinstein
import TGLExt.AperiodicPhaseAverage
import TGLExt.BoundaryEntropyBridge
import TGLExt.ChainLocality
import TGLExt.ClosedModulatorCandidate
import TGLExt.CondExpect
import TGLExt.ConstructedEinsteinReconstruction
import TGLExt.ContinuumTT
import TGLExt.CovariantCurvatureBianchi
import TGLExt.CovariantNullPreservation
import TGLExt.FallenLight
import TGLExt.FiniteCommutatorEvolution
import TGLExt.FiniteEinsteinNaturality
import TGLExt.FiniteEntropyAlgebra
import TGLExt.FiniteResponseReconstruction
import TGLExt.GeodesicFlowControls
import TGLExt.GeometricSectorObstruction
import TGLExt.GeometryFluctuation
import TGLExt.GibbsGravityControls
import TGLExt.IALDJones
import TGLExt.InfiniteCocycleDecoding
import TGLExt.LikelihoodCocycle
import TGLExt.LikelihoodCocycleControls
import TGLExt.LinearizedSpin2
import TGLExt.LocalPolarizerWitness
import TGLExt.ModularCostDerivative
import TGLExt.ModularFlowHilbert
import TGLExt.ModularFlowSpectrum
import TGLExt.ModularPower
import TGLExt.ModularSignatureObstruction
import TGLExt.O16
import TGLExt.O16.BilateralFirstOrderReuse
import TGLExt.O16.FourierStandardTransport_v3
import TGLExt.O16.InfiniteLimitUniformControl_v2
import TGLExt.O16.LightRayCoreMembership
import TGLExt.O16.ModularBoostEnergyReuse_v2
import TGLExt.O16.OrbitalBoostContinuity_v2
import TGLExt.O16.PhotonContract_v2
import TGLExt.O16.PositiveEnergyIntegral_v4
import TGLExt.O16.RotationGeneratorBridges
import TGLExt.O16.StressTensorDataLocal_v2
import TGLExt.O16.UnboundedTransformKernelGap_v3
import TGLExt.OpticalHeatFlow
import TGLExt.OpticalJacobiArea
import TGLExt.PauliInteractionWitness
import TGLExt.PhysicsIsTheReading
import TGLExt.RGStability
import TGLExt.SMatrix
import TGLExt.Screen013Controls
import TGLExt.SectorRouteComparison
import TGLExt.SigmaMatterConservation
import TGLExt.SignedGibbsFiniteRecord
import TGLExt.SiteLogLikelihood
import TGLExt.SolderSignature
import TGLExt.SusyRelativeGap
import TGLExt.TensorFieldLinearity
import TGLExt.TheAlgebraicReader
import TGLExt.TheAngleIsTheProjection
import TGLExt.TheBireference
import TGLExt.TheCommutationAtTheFloor
import TGLExt.TheConditionalCertificate
import TGLExt.TheContourOfTruth
import TGLExt.TheCouplingRunsBoundedBelow
import TGLExt.TheDeadChannel
import TGLExt.TheLightInterface
import TGLExt.TheSelectorCanRefuse
import TGLExt.TheVerbalCoupling
import TGLExt.ThermodynamicFriedmann
import TGLExt.ThreeLocksCorner
import TGLExt.TowerModular
import TGLExt.TransportedBorchersObstruction
import TGLExt.TransportedScreenControls
import TGLExt.UmPostoInscription
import TGLExt.UnitaryMarginalDynamics
import TGLExt.V350DualFormTransport
import TGLExt.V350DualOrbitVonNeumann
import TGLExt.V350FixedVectorGraphCore
import TGLExt.V350L2PositiveMultiplier
import TGLExt.V350L2Translation
import TGLExt.V350PartialOperatorSquare
import TGLExt.V350ReducingCommutantCompression
import TGLExt.V350RegularApproximation
import TGLExt.V350RegularDualAction
import TGLExt.V350RegularTopology
import TGLExt.V350ScalarGNSCutMaps
import TGLExt.V350ScalarGNSCutNorm
import TGLExt.V350ScalarGNSNormality
import TGLExt.V350ScalarRegularRightContinuity
import TGLExt.V350ScalarWeightOrbit
import TGLExt.V350TowerDuality
import TGLExt.V350UnitIntervalProjection
import TGLExt.V351InverseLimitSemifiniteness
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V351ScalarImaginaryRightTransport
import TGLExt.V351ScalarMultiplierCalculus
import TGLExt.V354CoreProjectionLattice
import TGLExt.V354RegularSusy

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.AffinityVectorCriterion, `TGLExt.AngularSelectorIntertwining, `TGLExt.AnsatzEinstein, `TGLExt.AperiodicPhaseAverage, `TGLExt.BoundaryEntropyBridge, `TGLExt.ChainLocality, `TGLExt.ClosedModulatorCandidate, `TGLExt.CondExpect, `TGLExt.ConstructedEinsteinReconstruction, `TGLExt.ContinuumTT, `TGLExt.CovariantCurvatureBianchi, `TGLExt.CovariantNullPreservation, `TGLExt.FallenLight, `TGLExt.FiniteCommutatorEvolution, `TGLExt.FiniteEinsteinNaturality, `TGLExt.FiniteEntropyAlgebra, `TGLExt.FiniteResponseReconstruction, `TGLExt.GeodesicFlowControls, `TGLExt.GeometricSectorObstruction, `TGLExt.GeometryFluctuation, `TGLExt.GibbsGravityControls, `TGLExt.IALDJones, `TGLExt.InfiniteCocycleDecoding, `TGLExt.LikelihoodCocycle, `TGLExt.LikelihoodCocycleControls, `TGLExt.LinearizedSpin2, `TGLExt.LocalPolarizerWitness, `TGLExt.ModularCostDerivative, `TGLExt.ModularFlowHilbert, `TGLExt.ModularFlowSpectrum, `TGLExt.ModularPower, `TGLExt.ModularSignatureObstruction, `TGLExt.O16, `TGLExt.O16.BilateralFirstOrderReuse, `TGLExt.O16.FourierStandardTransport_v3, `TGLExt.O16.InfiniteLimitUniformControl_v2, `TGLExt.O16.LightRayCoreMembership, `TGLExt.O16.ModularBoostEnergyReuse_v2, `TGLExt.O16.OrbitalBoostContinuity_v2, `TGLExt.O16.PhotonContract_v2, `TGLExt.O16.PositiveEnergyIntegral_v4, `TGLExt.O16.RotationGeneratorBridges, `TGLExt.O16.StressTensorDataLocal_v2, `TGLExt.O16.UnboundedTransformKernelGap_v3, `TGLExt.OpticalHeatFlow, `TGLExt.OpticalJacobiArea, `TGLExt.PauliInteractionWitness, `TGLExt.PhysicsIsTheReading, `TGLExt.RGStability, `TGLExt.SMatrix, `TGLExt.Screen013Controls, `TGLExt.SectorRouteComparison, `TGLExt.SigmaMatterConservation, `TGLExt.SignedGibbsFiniteRecord, `TGLExt.SiteLogLikelihood, `TGLExt.SolderSignature, `TGLExt.SusyRelativeGap, `TGLExt.TensorFieldLinearity, `TGLExt.TheAlgebraicReader, `TGLExt.TheAngleIsTheProjection, `TGLExt.TheBireference, `TGLExt.TheCommutationAtTheFloor, `TGLExt.TheConditionalCertificate, `TGLExt.TheContourOfTruth, `TGLExt.TheCouplingRunsBoundedBelow, `TGLExt.TheDeadChannel, `TGLExt.TheLightInterface, `TGLExt.TheSelectorCanRefuse, `TGLExt.TheVerbalCoupling, `TGLExt.ThermodynamicFriedmann, `TGLExt.ThreeLocksCorner, `TGLExt.TowerModular, `TGLExt.TransportedBorchersObstruction, `TGLExt.TransportedScreenControls, `TGLExt.UmPostoInscription, `TGLExt.UnitaryMarginalDynamics, `TGLExt.V350DualFormTransport, `TGLExt.V350DualOrbitVonNeumann, `TGLExt.V350FixedVectorGraphCore, `TGLExt.V350L2PositiveMultiplier, `TGLExt.V350L2Translation, `TGLExt.V350PartialOperatorSquare, `TGLExt.V350ReducingCommutantCompression, `TGLExt.V350RegularApproximation, `TGLExt.V350RegularDualAction, `TGLExt.V350RegularTopology, `TGLExt.V350ScalarGNSCutMaps, `TGLExt.V350ScalarGNSCutNorm, `TGLExt.V350ScalarGNSNormality, `TGLExt.V350ScalarRegularRightContinuity, `TGLExt.V350ScalarWeightOrbit, `TGLExt.V350TowerDuality, `TGLExt.V350UnitIntervalProjection, `TGLExt.V351InverseLimitSemifiniteness, `TGLExt.V351ResolventImaginaryIntertwining, `TGLExt.V351ScalarImaginaryRightTransport, `TGLExt.V351ScalarMultiplierCalculus, `TGLExt.V354CoreProjectionLattice, `TGLExt.V354RegularSusy]
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
