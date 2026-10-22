import TGLV350.ScalarWeightedEnergy
import TGLV350.ProjectionGapEnergy

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem densePairBlockZero {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j : E →ₗ[ℂ] H) (hj : DenseRange j)
    (A B e : H →L[ℂ] H) (η : H)
    (hB : ∀ b : E, B (j b)=A (b.val η))
    (he : ∀ b : E, Commute (e*A) b.val) (hzero : (e*A) η=0) : e*B=0 := by
  ext v
  refine hj.induction_on v (isClosed_eq (e*B).continuous continuous_const) ?_
  intro b
  change e (B (j b))=0
  rw [hB]
  change (e*A) (b.val η)=0
  have hh := congrArg (fun T : H →L[ℂ] H => T η) (he b).eq
  change (e*A) (b.val η)=b.val ((e*A) η) at hh
  rw [hh,hzero,map_zero]

theorem scalarPairedProjection_gapPart_mem (P : SiteProfile) (η : ScalarGNSHilbert P) (c : ℝ) :
    projectionGapPart (hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection) c ∈
      scalarGNSVonNeumann P := by
  apply scalarPairedCommutant_mem_GNS
  intro b
  exact projectionGapPart_commutes _ b.val c
    (scalarGNS_commutes_with_rightPair P _ (scalarPairedProjection_A_mem P η) b)

theorem scalarPhaseVariational_gapPart_block_zero (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a=a)
    (z : ℂ) (hz : 0 < z.re) (hz1 : z.re=1) :
    let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz (scalarRightPairVector P a)
    let A := hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection
    let B := hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection
    projectionGapPart A (1+‖a.val‖^2)*B=0 := by
  let ξ : ScalarGNSHilbert P := scalarRightPairVector P a
  let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz ξ
  let G := scalarPairedMultiplicationGraph P η
  let A := hilbertBlockA G.starProjection
  let B := hilbertBlockB G.starProjection
  let c : ℝ := 1+‖a.val‖^2
  let e := projectionGapPart A c
  have hem : e ∈ scalarGNSVonNeumann P := scalarPairedProjection_gapPart_mem P η c
  have heA : Commute e A := projectionGapPart_commutes A A c (Commute.refl A)
  have he : 0 ≤ e := projectionGapPart_nonneg A c
  have henergy := scalarPhaseVariational_rightPair_energy P a ha z hz hz1 e hem he heA
  have hzero : (e*A) η=0 := by
    apply projectionGapPart_energy_annihilates A B c η
      (scalarPairedProjection_A_positive_contraction P η).1
      (scalarPairedProjection_A_injective P η) (scalarPairedProjection_BBstar P η)
    have hc : c-1=‖a.val‖^2 := by dsimp only [c]; ring
    rw [hc]
    exact henergy
  have hs : ∃ hy : η ∈ scalarClosedTomitaDomain P,
      scalarClosedTomita P ⟨η,hy⟩=η := scalarPhaseVariational_fixed P z hz ξ
  obtain ⟨hy,hSy⟩ := hs
  refine densePairBlockZero (scalarPairedRightAlgebra P) (scalarRightPairVector P)
    (scalarRightPairVector_denseRange P) A B e η ?_ ?_ hzero
  · intro b
    exact scalarPairedProjection_B_left P ⟨η,hy⟩ hSy b
  · intro b
    exact scalarGNS_commutes_with_rightPair P (e*A)
      ((scalarGNSVonNeumann P).mul_mem hem (scalarPairedProjection_A_mem P η)) b

theorem scalarPhaseVariational_projection_lower_bound (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a=a)
    (z : ℂ) (hz : 0 < z.re) (hz1 : z.re=1) :
    (1+‖a.val‖^2)⁻¹ • (1 : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) ≤
      hilbertBlockA (scalarPairedMultiplicationGraph P
        (scalarPhaseVariational P z hz (scalarRightPairVector P a))).starProjection := by
  let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz (scalarRightPairVector P a)
  let G := scalarPairedMultiplicationGraph P η
  let A := hilbertBlockA G.starProjection
  let B := hilbertBlockB G.starProjection
  let c : ℝ := 1+‖a.val‖^2
  have hc : 1 ≤ c := le_add_of_nonneg_right (sq_nonneg _)
  have he : projectionGapPart A c=0 :=
    projectionGapPart_eq_zero_of_block_zero A B c hc (hilbertBlockA_adjoint G)
      (scalarPairedProjection_A_injective P η) (scalarPairedProjection_BBstar P η)
      (scalarPhaseVariational_gapPart_block_zero P a ha z hz hz1)
  exact projectionBlock_lower_bound_of_gap_zero A c (lt_of_lt_of_le zero_lt_one hc)
    (hilbertBlockA_adjoint G) he

theorem scalarPhaseVariational_projection_strictPositive (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a=a)
    (z : ℂ) (hz : 0 < z.re) (hz1 : z.re=1) :
    IsStrictlyPositive (hilbertBlockA (scalarPairedMultiplicationGraph P
      (scalarPhaseVariational P z hz (scalarRightPairVector P a))).starProjection) := by
  apply projectionBlock_strictPositive_of_lower_bound _ (1+‖a.val‖^2)
    (by positivity)
  exact scalarPhaseVariational_projection_lower_bound P a ha z hz hz1

#print axioms scalarPairedProjection_gapPart_mem
#print axioms scalarPhaseVariational_gapPart_block_zero
#print axioms scalarPhaseVariational_projection_lower_bound
#print axioms scalarPhaseVariational_projection_strictPositive
end
end TGLV350.Regular
