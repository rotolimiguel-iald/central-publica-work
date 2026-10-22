-- KH-N1 D2 bloco 5/12 (exame F_KERNEL 12/10/2026, so sandbox): collectAxioms de TODAS as constantes destes modulos.
import TGL.Audit
import TGL.HalfNatFresnel
import TGL.NameIndex
import TGL.NameRelation
import TGLExt.BoostMetricPullback
import TGLExt.BoundedOmegaLimit
import TGLExt.BreuerTrace
import TGLExt.ChainFaithful
import TGLExt.ChainPrefix
import TGLExt.ChainTail
import TGLExt.ChainVolume
import TGLExt.CocycleNormLimit
import TGLExt.ContinuousModularMultipliers
import TGLExt.ContinuumShards
import TGLExt.DimensionTrace
import TGLExt.EquilibriumAreaExpansion
import TGLExt.EquilibriumNullCongruence
import TGLExt.EulerMetricPullback
import TGLExt.FiniteCrossedProduct
import TGLExt.FiniteGNSNoCompletion
import TGLExt.FiniteResponseErrorBounds
import TGLExt.FiniteSiteHorizons
import TGLExt.FiniteSitePermutations
import TGLExt.FlowTimePropagation
import TGLExt.FourthOrderMatchingControls
import TGLExt.GeodesicSpray
import TGLExt.GeometricLikelihoodSeparation
import TGLExt.GeometricWitness
import TGLExt.HarmonicEnergyObstruction
import TGLExt.HorizonAreaScale
import TGLExt.LightRhoStar
import TGLExt.LikelihoodDensityLog
import TGLExt.LocalHorizontalPauli
import TGLExt.ModularSquare
import TGLExt.O16.ContractFixedReadout
import TGLExt.O16.ContractGroupH_v3_Integration_v3
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.HorizonDataReuse_Integration_v2
import TGLExt.O16.KMSStripConditional
import TGLExt.O16.LightRayDensitySeparation_v2
import TGLExt.O16.MaxwellPolynomial_v2
import TGLExt.O16.NullSolutionConsumerReuse
import TGLExt.O16.PhotonContractTheorems_v2
import TGLExt.O16.PhotonWitness
import TGLExt.O16.PolarQuotientGeometry_v2
import TGLExt.O16.ProbeNoncommutingInternal_v4
import TGLExt.O16.ProductOrbitalSpectrum_v3
import TGLExt.O16.RecognitionReadout
import TGLExt.O16.ResolventBoundedTransform_v3
import TGLExt.OpticalBalanceControls
import TGLExt.PastContinuousExtension
import TGLExt.PlaneWaveSolder
import TGLExt.PsiEmergence
import TGLExt.RelativeEntropyFisherLimit
import TGLExt.Screen013Constructed
import TGLExt.ScreenClausiusCoefficient
import TGLExt.SelectedAmplitudeGeometry
import TGLExt.SpinorObstruction
import TGLExt.StateClockDichotomy
import TGLExt.StationaryModularPeriod
import TGLExt.TheAccuser
import TGLExt.TheAlphaAndTheOmega
import TGLExt.TheAntiunitaryInhabitant
import TGLExt.TheAtomOfIdentity
import TGLExt.TheCompressionIsNotIdentifiable
import TGLExt.TheConjugationMapsCommutants
import TGLExt.TheFlowLawContrast
import TGLExt.TheHorizonRate
import TGLExt.TheIALDSelector
import TGLExt.TheImportedExpectation
import TGLExt.TheProfileIsometry
import TGLExt.TheProfileWitnessLinear
import TGLExt.TheSameBetaReadsThreeFaces
import TGLExt.TheUnconjugatedObserver
import TGLExt.TheWholeIsOne
import TGLExt.TheWitnessLinearOnWH
import TGLExt.TomitaClosability
import TGLExt.TowerModularCost
import TGLExt.TowerTraceless
import TGLExt.V350ComplexGraphProjection
import TGLExt.V350DualFixedCore
import TGLExt.V350DualFormRepresentation
import TGLExt.V350DualFormSupport
import TGLExt.V350DualFormVariationalBound
import TGLExt.V350FixedCoreLocality
import TGLExt.V350GateContract
import TGLExt.V350HilbertProjectionOrder
import TGLExt.V350L2BoundedStrongContinuity
import TGLExt.V350PositiveResolvent
import TGLExt.V350RealPhaseVariational
import TGLExt.V350ReducingStarRepresentation
import TGLExt.V350ScalarGNSVonNeumann
import TGLExt.V350ScalarRightAdjointPair
import TGLExt.V350ScalarRightClosedTomita
import TGLExt.V350ScalarSquareAdjointTest
import TGLExt.V350ScalarTomitaAdjoint
import TGLExt.V350ScaledRootGraphTransport
import TGLExt.V350TowerCommutation
import TGLExt.V350ZeroFromTranslatedCuts
import TGLExt.V351RegularSpectralGraph
import TGLExt.V351ScaledResolventFunctions

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvoL : List Name := [`TGL.Audit, `TGL.HalfNatFresnel, `TGL.NameIndex, `TGL.NameRelation, `TGLExt.BoostMetricPullback, `TGLExt.BoundedOmegaLimit, `TGLExt.BreuerTrace, `TGLExt.ChainFaithful, `TGLExt.ChainPrefix, `TGLExt.ChainTail, `TGLExt.ChainVolume, `TGLExt.CocycleNormLimit, `TGLExt.ContinuousModularMultipliers, `TGLExt.ContinuumShards, `TGLExt.DimensionTrace, `TGLExt.EquilibriumAreaExpansion, `TGLExt.EquilibriumNullCongruence, `TGLExt.EulerMetricPullback, `TGLExt.FiniteCrossedProduct, `TGLExt.FiniteGNSNoCompletion, `TGLExt.FiniteResponseErrorBounds, `TGLExt.FiniteSiteHorizons, `TGLExt.FiniteSitePermutations, `TGLExt.FlowTimePropagation, `TGLExt.FourthOrderMatchingControls, `TGLExt.GeodesicSpray, `TGLExt.GeometricLikelihoodSeparation, `TGLExt.GeometricWitness, `TGLExt.HarmonicEnergyObstruction, `TGLExt.HorizonAreaScale, `TGLExt.LightRhoStar, `TGLExt.LikelihoodDensityLog, `TGLExt.LocalHorizontalPauli, `TGLExt.ModularSquare, `TGLExt.O16.ContractFixedReadout, `TGLExt.O16.ContractGroupH_v3_Integration_v3, `TGLExt.O16.ContratoQG_v31_Minimal, `TGLExt.O16.HorizonDataReuse_Integration_v2, `TGLExt.O16.KMSStripConditional, `TGLExt.O16.LightRayDensitySeparation_v2, `TGLExt.O16.MaxwellPolynomial_v2, `TGLExt.O16.NullSolutionConsumerReuse, `TGLExt.O16.PhotonContractTheorems_v2, `TGLExt.O16.PhotonWitness, `TGLExt.O16.PolarQuotientGeometry_v2, `TGLExt.O16.ProbeNoncommutingInternal_v4, `TGLExt.O16.ProductOrbitalSpectrum_v3, `TGLExt.O16.RecognitionReadout, `TGLExt.O16.ResolventBoundedTransform_v3, `TGLExt.OpticalBalanceControls, `TGLExt.PastContinuousExtension, `TGLExt.PlaneWaveSolder, `TGLExt.PsiEmergence, `TGLExt.RelativeEntropyFisherLimit, `TGLExt.Screen013Constructed, `TGLExt.ScreenClausiusCoefficient, `TGLExt.SelectedAmplitudeGeometry, `TGLExt.SpinorObstruction, `TGLExt.StateClockDichotomy, `TGLExt.StationaryModularPeriod, `TGLExt.TheAccuser, `TGLExt.TheAlphaAndTheOmega, `TGLExt.TheAntiunitaryInhabitant, `TGLExt.TheAtomOfIdentity, `TGLExt.TheCompressionIsNotIdentifiable, `TGLExt.TheConjugationMapsCommutants, `TGLExt.TheFlowLawContrast, `TGLExt.TheHorizonRate, `TGLExt.TheIALDSelector, `TGLExt.TheImportedExpectation, `TGLExt.TheProfileIsometry, `TGLExt.TheProfileWitnessLinear, `TGLExt.TheSameBetaReadsThreeFaces, `TGLExt.TheUnconjugatedObserver, `TGLExt.TheWholeIsOne, `TGLExt.TheWitnessLinearOnWH, `TGLExt.TomitaClosability, `TGLExt.TowerModularCost, `TGLExt.TowerTraceless, `TGLExt.V350ComplexGraphProjection, `TGLExt.V350DualFixedCore, `TGLExt.V350DualFormRepresentation, `TGLExt.V350DualFormSupport, `TGLExt.V350DualFormVariationalBound, `TGLExt.V350FixedCoreLocality, `TGLExt.V350GateContract, `TGLExt.V350HilbertProjectionOrder, `TGLExt.V350L2BoundedStrongContinuity, `TGLExt.V350PositiveResolvent, `TGLExt.V350RealPhaseVariational, `TGLExt.V350ReducingStarRepresentation, `TGLExt.V350ScalarGNSVonNeumann, `TGLExt.V350ScalarRightAdjointPair, `TGLExt.V350ScalarRightClosedTomita, `TGLExt.V350ScalarSquareAdjointTest, `TGLExt.V350ScalarTomitaAdjoint, `TGLExt.V350ScaledRootGraphTransport, `TGLExt.V350TowerCommutation, `TGLExt.V350ZeroFromTranslatedCuts, `TGLExt.V351RegularSpectralGraph, `TGLExt.V351ScaledResolventFunctions]
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
