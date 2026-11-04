-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
-- import TGL  -- REMOVIDO na transposicao: importar o root TGL fecharia o ciclo TGL->TGL.Audit->TGLExt(root)->TomitaClosability->TGL; o conteudo TGL.* chega transitivamente pelas pedras TGLExt.*
import TGLExt.Commutant
import TGLExt.LeftRight
import TGLExt.FiniteTomita
import TGLExt.ModularFlow
import TGLExt.CondExpect
import TGLExt.PPIndex
import TGLExt.MarkovTower
import TGLExt.Bicommutant
import TGLExt.SMatrix
import TGLExt.Cocycle
import TGLExt.Ergodicity
import TGLExt.FiniteCrossedProduct
import TGLExt.GlobalLiftLadder
import TGLExt.CornerFamily
import TGLExt.BisognanoWichmann
import TGLExt.GravitonPolarization
import TGLExt.GeometryFluctuation
import TGLExt.PageInformation
import TGLExt.ModularFirstLaw
import TGLExt.RGStability
import TGLExt.VariationalInhabitant
import TGLExt.GNSBridge
import TGLExt.FiniteGNSNoCompletion
import TGLExt.TransportWitness
import TGLExt.CovariantCorner
import TGLExt.HilbertHome
import TGLExt.PsiEmergence
import TGLExt.AbsoluteOne
import TGLExt.ContinuousModularZero
import TGLExt.MinimalSolder
import TGLExt.NoFullWitness
import TGLExt.Solder4D
import TGLExt.LocalBreuerGap
import TGLExt.SusyRelativeGap
import TGLExt.EmergenceTriad
import TGLExt.TriadMaster
import TGLExt.LinearizedSpin2
import TGLExt.SemifiniteSeed
import TGLExt.DimensionTrace
import TGLExt.ThreeLocksCorner
import TGLExt.SemifiniteLattice
import TGLExt.ClosedLattice
import TGLExt.InvariantProjection
import TGLExt.BicommutantSkeleton
import TGLExt.SpectralReduction
import TGLExt.WitnessSeed
import TGLExt.ExactWitness
import TGLExt.WordExistence
import TGLExt.InfiniteWord
import TGLExt.HilbertInhabitant
import TGLExt.AQFTCoreInhabitant
import TGLExt.ConcreteFourFrame
import TGLExt.TheMasterFires
import TGLExt.ClosureCertificate
import TGLExt.ProgrammerRule
import TGLExt.IsotoneNet
import TGLExt.IdealLimit
import TGLExt.BenchCertificate
import TGLExt.StrongFrame
import TGLExt.WitnessV2
import TGLExt.NumberOperator
import TGLExt.NumberSelfAdjoint
import TGLExt.TailNet
import TGLExt.StrongAssembly
import TGLExt.SolderField
import TGLExt.FirstCurvature
import TGLExt.AnsatzEinstein
import TGLExt.FallenLight
import TGLExt.SolvedEquation
import TGLExt.ReducedEmergence
import TGLExt.GeometricWitness
import TGLExt.GravitonReading
import TGLExt.ContinuumShards
import TGLExt.EmergentEinstein
import TGLExt.PoincareGroup
import TGLExt.PoincareWitness
import TGLExt.RegularRep
import TGLExt.TracelessAlgebra
import TGLExt.SemifiniteWeight
import TGLExt.FusedWitness
import TGLExt.PowersLadder
import TGLExt.MixedLadder
import TGLExt.TheNameIsTheGeneratingGroup
import TGLExt.TheMarkIsNotATypeMark
import TGLExt.TheVerbalCoupling
import TGLExt.TheDammingByExpansion
import TGLExt.TheDischargedOath
import TGLExt.TheOathOnTheTower
import TGLExt.TheImportedExpectation
import TGLExt.TheAlphaAndTheOmega
import TGLExt.ContinuumTT
import TGLExt.ColimitSeed
import TGLExt.TTSuperposition
import TGLExt.GNSTower
import TGLExt.SecondCone
import TGLExt.GNSQuotient
import TGLExt.ThirdCone
import TGLExt.GeneralNull
import TGLExt.TowerTraceless
import TGLExt.TowerModular
import TGLExt.SaturatedWitness
import TGLExt.ConjugateWitness
import TGLExt.ModularCurrent
import TGLExt.ScaleCurrent
import TGLExt.TowerDefinite
import TGLExt.TowerHilbert
import TGLExt.TowerAction
import TGLExt.TheFactorObject
import TGLExt.SignatureInTheLimit
import TGLExt.NoNormalTrace
import TGLExt.WitnessV3
import TGLExt.TheCoinage
import TGLExt.PhysicsCertificates
import TGLExt.RightMult
import TGLExt.WedgeNet
import TGLExt.BoundaryException
import TGLExt.GlobalLiftConditional
import TGLExt.ObserverInside
import TGLExt.ConjugateAct
import TGLExt.DecisionCommutation
import TGLExt.ForbiddenBoundary
import TGLExt.LightIsJ
import TGLExt.RhoPlusPClosure
import TGLExt.TheNucleus
import TGLExt.TheGreatAttractor
import TGLExt.TheFiveHalves
import TGLExt.TheLivingWord
import TGLExt.TheDeathOfTheSignal
import TGLExt.HajaLuz
import TGLExt.TheReservedConfirmation
import TGLExt.TheStokesContour
import TGLExt.TheQuittanceLaw
import TGLExt.TheNameOperator
import TGLExt.FractalUnitarity
import TGLExt.TheAtlasIndex
import TGLExt.EquivariantSection
import TGLExt.SolderSignature
import TGLExt.ErgodicMeanSection
import TGLExt.BreuerTrace
import TGLExt.TheStation
import TGLExt.TheExplosion
import TGLExt.TheBandNet
import TGLExt.TheFold
import TGLExt.TheRecordOfTheCut
import TGLExt.TheIALDSelector
import TGLExt.TheUnconjugatedObserver
import TGLExt.TheDarkSplit
import TGLExt.TheTwoPairings
import TGLExt.TheAlgebraicReader
import TGLExt.TheRecordOfJ
import TGLExt.TheSingularExpectation
import TGLExt.TheTerminalRankOne
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheAngleIsTheBridge
import TGLExt.TheSelectorIsNotEnough
import TGLExt.TheSelectorCanRefuse
import TGLExt.TheTwoFolds
import TGLExt.TheScaleHasNoFixedPoint
import TGLExt.TheCompressionIsNotIdentifiable
import TGLExt.TheEmptying
import TGLExt.TheCorrespondence
import TGLExt.TheHorizonInvariance
import TGLExt.TheAngleIsTheProjection
import TGLExt.TheFalseHasNoGeometry
import TGLExt.TheObserverReadsTheAngle
import TGLExt.TheCascadeOfObservers
import TGLExt.TheCoFoundation
import TGLExt.ThePermanence
import TGLExt.TheLightInterface
import TGLExt.TheBireference
import TGLExt.FrontierCertificate
import TGLExt.TheTower
import TGLExt.ThePhysicalHorizon
import TGLExt.TheHorizonRate
import TGLExt.TheAnchorFour
import TGLExt.TheTwoFunctionSolder
import TGLExt.TheSchwarzschildUniqueness
import TGLExt.TheCornerEmbedding
import TGLExt.TheCoordinateBridge
import TGLExt.TheFullBirkhoff
import TGLExt.TheCrownedCascade
import TGLExt.TheIALDInTheTower
import TGLExt.TheTrueWitness
import TGLExt.TheLegibility
import TGLExt.TheIALDInTheTowerActII
import TGLExt.TheJudgedThing
import TGLExt.TheCostIsDerived
import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.TheOriginOfTheVibration
import TGLExt.TheDeadChannel
import TGLExt.TheContourOfTruth
import TGLExt.TheAccuser
import TGLExt.TheTowerInnerProduct
import TGLExt.TheCompletionExtension
import TGLExt.TheSupersaturation
import TGLExt.TheTowerConjugation
import TGLExt.TheUnsolicitedUnitary
import TGLExt.TheTowerWitness
import TGLExt.TheTowerWitnessLinear
import TGLExt.TheProfileConjugation
import TGLExt.TheTelescopingProfile
import TGLExt.TheExoneratedDemon
import TGLExt.TheProfileIsometry
import TGLExt.TheProfileDuality
import TGLExt.TheFoldIsNotADistance
import TGLExt.TheColimitDuality
import TGLExt.TheColimitIsometry
import TGLExt.TheLivingWordClosure
import TGLExt.TheProfileWitnessLinear
import TGLExt.TheWitnessOnTheBoundary
import TGLExt.TheTopologicalFace
import TGLExt.TheBoundaryDuality
import TGLExt.TheConjugationMapsCommutants
import TGLExt.TheDensityIsTransport
import TGLExt.TheWitnessLinearOnWH
import TGLExt.TheConjugationOfOperators
import TGLExt.TheConverseClauseReduced
import TGLExt.TheDensityIsBell
import TGLExt.TheIdentityOfIdentity
import TGLExt.TheTGLPair
import TGLExt.TheQuestionAndTheRecognition
import TGLExt.TheIsometryOnWH
import TGLExt.TheCarrierBridge
import TGLExt.TheCommutationAtTheFloor
import TGLExt.TheEntanglementNotConjunction
import TGLExt.TheConditionalCertificate
import TGLExt.TheNonLinearCausality
import TGLExt.TheImportedEquilibrium
import TGLExt.TheIntersectionOfCommutants
import TGLExt.TheNonMinimalCoupling
import TGLExt.TheWeightIsNotTheRank
import TGLExt.TheScalarCorner
import TGLExt.TheCurrentConnectsTheCorners
import TGLExt.ThePsionReducesToTheCurrent
import TGLExt.TheNetFiresTheCorner
import TGLExt.TheTwoPolesHaveContent
import TGLExt.TheAtomOfIdentity
import TGLExt.TheFoldThroughJ
import TGLExt.TheAntiunitaryInhabitant
import TGLExt.TheGravitonIsTheConjugatedPhase
import TGLExt.TheImageAndTheReading
import TGLExt.TheImportedCommutation
import TGLExt.TheMatrixAndTheModulator
import TGLExt.TheModularRelations
import TGLExt.TheDebtWithoutJ
import TGLExt.TheNameAndItsReferent
import TGLExt.TheCornerOfThePackage
import TGLExt.TheWideNet
import TGLExt.TheClassicalImport
import TGLExt.TheAtermation
import TGLExt.TheImportedExpectation
import TGLExt.RightMult

set_option autoImplicit false
set_option maxHeartbeats 1000000

open Filter Topology

namespace ChatgptAudit

open TGLExt

noncomputable section

variable {P : SiteProfile}

/-- Identidade de dualidade com a direita limitada da torre. -/
theorem tomita_pairing
    {A : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ ((star A) (hOmega P)) (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) (A (hOmega P)) := by
  simp only [ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_left]
  have hc := congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P =>
    T (hOmega P)) (factor_comm_rTowerPi hA b)
  simpa only [mul_apply_eq_comp] using congrArg
    (fun z : TowerHilbert P => inner ℂ (hOmega P) z) hc

/-- Critério sequencial de fechabilidade no completamento genuíno.
    Não pressupõe TakesakiInput nem CommutationInput. -/
theorem tomita_sequential_closability
    (A : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : ∀ n, A n ∈ theFactorObject P)
    (y : TowerHilbert P)
    (hzero : Tendsto (fun n => A n (hOmega P)) atTop (𝓝 0))
    (hy : Tendsto (fun n => (star (A n)) (hOmega P)) atTop (𝓝 y)) :
    y = 0 := by
  apply (towerPre_denseRange (P := P)).eq_zero_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  have hleft := hy.inner (𝕜 := ℂ)
    (tendsto_const_nhds (x := rTowerPi P b (hOmega P)))
  have hright := (tendsto_const_nhds
    (x := (star (rTowerPi P b)) (hOmega P))).inner (𝕜 := ℂ) hzero
  have heq : (fun n => inner ℂ ((star (A n)) (hOmega P))
      (rTowerPi P b (hOmega P))) =
      (fun n => inner ℂ ((star (rTowerPi P b)) (hOmega P))
        (A n (hOmega P))) := funext (fun n => tomita_pairing (hA n) b)
  rw [heq] at hleft
  simpa only [inner_zero_right] using tendsto_nhds_unique hleft hright

/-- A regra AΩ ↦ A*Ω é bem definida pela separância já provada. -/
theorem tomita_well_defined
    {A B : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P)
    (h : A (hOmega P) = B (hOmega P)) :
    (star A) (hOmega P) = (star B) (hOmega P) := by
  have hz : A - B = 0 := factor_omega_separating
    ((theFactorObject P).sub_mem hA hB) (by simpa using sub_eq_zero.mpr h)
  have hab : A = B := sub_eq_zero.mp hz
  rw [hab]

/-- Gráfico do operador antilinear AΩ ↦ A*Ω no domínio MΩ. -/
def tomitaGraph (P : SiteProfile) : Set (TowerHilbert P × TowerHilbert P) :=
  {p | ∃ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A ∈ theFactorObject P ∧ p = (A (hOmega P), (star A) (hOmega P))}

/-- Ponte explícita ao operador S no andar: o adjunto matricial vive neste gráfico. -/
theorem local_tomita_graph {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (((tof P N a : TowerPre P) : TowerHilbert P),
      ((tof P N (Matrix.conjTranspose a) : TowerPre P) : TowerHilbert P)) ∈ tomitaGraph P := by
  refine ⟨towerPi P a, towerPi_mem_factor a, ?_⟩
  simp only [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, towerPi_omega]

/-- A identidade de dualidade sobrevive ao fecho topológico do gráfico. -/
theorem closure_graph_pairing
    {p : TowerHilbert P × TowerHilbert P}
    (hp : p ∈ closure (tomitaGraph P)) {N : ℕ}
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1 := by
  have hc : IsClosed {p : TowerHilbert P × TowerHilbert P |
      inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1} := by
    apply isClosed_eq <;> fun_prop
  apply closure_minimal (t := {p : TowerHilbert P × TowerHilbert P |
      inner ℂ p.2 (rTowerPi P b (hOmega P)) =
      inner ℂ ((star (rTowerPi P b)) (hOmega P)) p.1}) ?_ hc hp
  rintro p ⟨A, hA, rfl⟩
  exact tomita_pairing hA b

/-- Fechabilidade em forma topológica: o fecho não adquire fibra vertical não nula. -/
theorem tomita_graph_closure_vertical
    (y : TowerHilbert P) (hy : (0, y) ∈ closure (tomitaGraph P)) : y = 0 := by
  apply (towerPre_denseRange (P := P)).eq_zero_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  simpa only [inner_zero_right] using closure_graph_pairing hy b

/-- O fecho do gráfico é univalente, inclusive fora do domínio inicial MΩ. -/
theorem tomita_graph_closure_single_valued
    (x y z : TowerHilbert P)
    (hy : (x, y) ∈ closure (tomitaGraph P))
    (hz : (x, z) ∈ closure (tomitaGraph P)) : y = z := by
  apply (towerPre_denseRange (P := P)).eq_of_inner_left (𝕜 := ℂ)
  intro v
  obtain ⟨N, b, rfl⟩ := exists_tof v
  rw [← rTowerPi_omega]
  exact (closure_graph_pairing hy b).trans (closure_graph_pairing hz b).symm

/-- Densidade do domínio inicial, com a definição concreta do gráfico. -/
theorem tomita_graph_domain_dense :
    Dense (Prod.fst '' tomitaGraph P) := by
  apply Dense.mono ?_ (factor_omega_cyclic (P := P))
  rintro x ⟨A, hA, rfl⟩
  exact ⟨(A (hOmega P), (star A) (hOmega P)), ⟨A, hA, rfl⟩, rfl⟩

#print axioms tomita_pairing
#print axioms tomita_sequential_closability
#print axioms tomita_well_defined
#print axioms local_tomita_graph
#print axioms closure_graph_pairing
#print axioms tomita_graph_closure_vertical
#print axioms tomita_graph_closure_single_valued
#print axioms tomita_graph_domain_dense

end
end ChatgptAudit
