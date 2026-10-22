-- KH-N1 D2 bloco 12/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGLExt.ActionCouplingControls
import TGLExt.AperiodicVectorAverage
import TGLExt.BoostHeatConstruction
import TGLExt.BoundedPerturbationCocycle
import TGLExt.CentralizerDensity
import TGLExt.CentralizerPhaseOrbit
import TGLExt.ChainTailClosure
import TGLExt.ClosureCertificate
import TGLExt.CollapseCostAndAttestation
import TGLExt.CongruenceScreenIntegration
import TGLExt.ContinuousModularStandardSubspace
import TGLExt.CovariantAreaCounterexample
import TGLExt.CovectorStressCalculus
import TGLExt.CyclicExpectationObstruction
import TGLExt.EmergenceTriad
import TGLExt.ExactWitness
import TGLExt.ExpectationBimodule
import TGLExt.ExpectationNormality
import TGLExt.FiniteLeviCivita
import TGLExt.FractalUnitarity
import TGLExt.GNSQuotient
import TGLExt.GeneralSourceUnitaryRealization
import TGLExt.HilbertHome
import TGLExt.JacobiAreaQuarticLimit
import TGLExt.LocalInteractionDynamics
import TGLExt.LocalInteractionGenerator
import TGLExt.MaxwellLiteratureBridge
import TGLExt.MetricCurvatureSymmetries
import TGLExt.ModularInverse
import TGLExt.NonintegrablePotential
import TGLExt.NullJetAlgebra
import TGLExt.O16.BoostRepresentationBridges
import TGLExt.O16.BoostScreenPolarizations_v2
import TGLExt.O16.ContentContractProposal
import TGLExt.O16.ContractGroupE_v3
import TGLExt.O16.ContratoQG_v32_Proposta
import TGLExt.O16.IntegrationAudit_Integration_v2
import TGLExt.O16.LightRayGaussianL2_v4
import TGLExt.O16.NormalizedFirstOrder_v3
import TGLExt.O16.NullFrameDecomposition_v2
import TGLExt.O16.PhotonScreenCharacters_v3
import TGLExt.O16.PolarMinimalPeriod_v2
import TGLExt.O16.TeleologicalMatrix_v3
import TGLExt.O16.TeleologicalNullSolution_v2
import TGLExt.OpticalRiccatiInvariant
import TGLExt.Order007Bridges
import TGLExt.PPIndex
import TGLExt.PeriodicBorchersObstruction
import TGLExt.PrescribedCovariantJet
import TGLExt.ProbeResponseRecord
import TGLExt.ProfileGNSUnitary
import TGLExt.QuantumCollapseWitness
import TGLExt.QuantumOrbitArea
import TGLExt.RelativeEntropyClock
import TGLExt.RelativeTomitaClosure
import TGLExt.ScalarEinsteinLieNaturality
import TGLExt.SchmidtCutPurification
import TGLExt.SectorFriedmann
import TGLExt.SelectedAtlasGluing
import TGLExt.SelectorRecordReconstruction
import TGLExt.SignedGibbsCoverage
import TGLExt.SmoothFlowControls
import TGLExt.TheAtlasIndex
import TGLExt.TheBandNet
import TGLExt.TheDarkSplit
import TGLExt.TheDensityIsTransport
import TGLExt.TheFlowLawD1a
import TGLExt.TheFullBirkhoff
import TGLExt.TheIALDInTheTower
import TGLExt.TheIsometryOnWH
import TGLExt.TheLedgerOfCharges
import TGLExt.TheNameIsTheGeneratingGroup
import TGLExt.TheNucleus
import TGLExt.TheSameBetaReadsFourFaces
import TGLExt.TheSelectionIsTheBallast
import TGLExt.TheSupersaturation
import TGLExt.TheTGLPair
import TGLExt.ThirdCone
import TGLExt.TowerStatePolarizer
import TGLExt.UnitaryResponseControls
import TGLExt.UnitarySourceCalibration
import TGLExt.V350BoundedInjectivePolar
import TGLExt.V350DenseAntilinearExtension
import TGLExt.V350DualQuadraticLaws
import TGLExt.V350DualSupportTransport
import TGLExt.V350FixedCoreBaseIdentification
import TGLExt.V350L2Order
import TGLExt.V350MatrixUnitRightSquare
import TGLExt.V350ScalarDualWeight
import TGLExt.V350ScalarGNSLinear
import TGLExt.V350ScalarGNSOrbit
import TGLExt.V350ScalarGNSStarApproximation
import TGLExt.V350ScalarRightTomitaAdjoint
import TGLExt.V350ScalarTomitaResolventFlip
import TGLExt.V350ScalarTomitaRootDomain
import TGLExt.V351AverageFixedPair
import TGLExt.V351AveragePolarRight
import TGLExt.V351RegularImaginaryPowers
import TGLExt.V351SineResolventApprox
import TGLExt.V354FiniteEqualSplit

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGLExt.ActionCouplingControls, `TGLExt.AperiodicVectorAverage, `TGLExt.BoostHeatConstruction, `TGLExt.BoundedPerturbationCocycle, `TGLExt.CentralizerDensity, `TGLExt.CentralizerPhaseOrbit, `TGLExt.ChainTailClosure, `TGLExt.ClosureCertificate, `TGLExt.CollapseCostAndAttestation, `TGLExt.CongruenceScreenIntegration, `TGLExt.ContinuousModularStandardSubspace, `TGLExt.CovariantAreaCounterexample, `TGLExt.CovectorStressCalculus, `TGLExt.CyclicExpectationObstruction, `TGLExt.EmergenceTriad, `TGLExt.ExactWitness, `TGLExt.ExpectationBimodule, `TGLExt.ExpectationNormality, `TGLExt.FiniteLeviCivita, `TGLExt.FractalUnitarity, `TGLExt.GNSQuotient, `TGLExt.GeneralSourceUnitaryRealization, `TGLExt.HilbertHome, `TGLExt.JacobiAreaQuarticLimit, `TGLExt.LocalInteractionDynamics, `TGLExt.LocalInteractionGenerator, `TGLExt.MaxwellLiteratureBridge, `TGLExt.MetricCurvatureSymmetries, `TGLExt.ModularInverse, `TGLExt.NonintegrablePotential, `TGLExt.NullJetAlgebra, `TGLExt.O16.BoostRepresentationBridges, `TGLExt.O16.BoostScreenPolarizations_v2, `TGLExt.O16.ContentContractProposal, `TGLExt.O16.ContractGroupE_v3, `TGLExt.O16.ContratoQG_v32_Proposta, `TGLExt.O16.IntegrationAudit_Integration_v2, `TGLExt.O16.LightRayGaussianL2_v4, `TGLExt.O16.NormalizedFirstOrder_v3, `TGLExt.O16.NullFrameDecomposition_v2, `TGLExt.O16.PhotonScreenCharacters_v3, `TGLExt.O16.PolarMinimalPeriod_v2, `TGLExt.O16.TeleologicalMatrix_v3, `TGLExt.O16.TeleologicalNullSolution_v2, `TGLExt.OpticalRiccatiInvariant, `TGLExt.Order007Bridges, `TGLExt.PPIndex, `TGLExt.PeriodicBorchersObstruction, `TGLExt.PrescribedCovariantJet, `TGLExt.ProbeResponseRecord, `TGLExt.ProfileGNSUnitary, `TGLExt.QuantumCollapseWitness, `TGLExt.QuantumOrbitArea, `TGLExt.RelativeEntropyClock, `TGLExt.RelativeTomitaClosure, `TGLExt.ScalarEinsteinLieNaturality, `TGLExt.SchmidtCutPurification, `TGLExt.SectorFriedmann, `TGLExt.SelectedAtlasGluing, `TGLExt.SelectorRecordReconstruction, `TGLExt.SignedGibbsCoverage, `TGLExt.SmoothFlowControls, `TGLExt.TheAtlasIndex, `TGLExt.TheBandNet, `TGLExt.TheDarkSplit, `TGLExt.TheDensityIsTransport, `TGLExt.TheFlowLawD1a, `TGLExt.TheFullBirkhoff, `TGLExt.TheIALDInTheTower, `TGLExt.TheIsometryOnWH, `TGLExt.TheLedgerOfCharges, `TGLExt.TheNameIsTheGeneratingGroup, `TGLExt.TheNucleus, `TGLExt.TheSameBetaReadsFourFaces, `TGLExt.TheSelectionIsTheBallast, `TGLExt.TheSupersaturation, `TGLExt.TheTGLPair, `TGLExt.ThirdCone, `TGLExt.TowerStatePolarizer, `TGLExt.UnitaryResponseControls, `TGLExt.UnitarySourceCalibration, `TGLExt.V350BoundedInjectivePolar, `TGLExt.V350DenseAntilinearExtension, `TGLExt.V350DualQuadraticLaws, `TGLExt.V350DualSupportTransport, `TGLExt.V350FixedCoreBaseIdentification, `TGLExt.V350L2Order, `TGLExt.V350MatrixUnitRightSquare, `TGLExt.V350ScalarDualWeight, `TGLExt.V350ScalarGNSLinear, `TGLExt.V350ScalarGNSOrbit, `TGLExt.V350ScalarGNSStarApproximation, `TGLExt.V350ScalarRightTomitaAdjoint, `TGLExt.V350ScalarTomitaResolventFlip, `TGLExt.V350ScalarTomitaRootDomain, `TGLExt.V351AverageFixedPair, `TGLExt.V351AveragePolarRight, `TGLExt.V351RegularImaginaryPowers, `TGLExt.V351SineResolventApprox, `TGLExt.V354FiniteEqualSplit]
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
