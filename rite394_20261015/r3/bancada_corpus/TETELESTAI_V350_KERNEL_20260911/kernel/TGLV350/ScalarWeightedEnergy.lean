import TGLV350.WeightedVariationalEnergy
import TGLV350.ScalarWeightedProjectionTest

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt
noncomputable section

theorem scalarGNS_commutes_with_rightPair (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSVonNeumann P)
    (a : scalarPairedRightAlgebra P) : Commute T a.val := by
  have hm := (scalarPairedRightAlgebra_centralizer P).symm.subset hT
  exact (hm a.val a.property).symm

theorem scalarSelfadjointRightPair_fixed_original_F (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a=a) :
    ∃ hx : scalarRightPairVector P a ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarRightPairVector P a,hx⟩=scalarRightPairVector P a := by
  have hh : ∃ hx : scalarRightPairVector P a ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarRightPairVector P a,hx⟩=scalarRightPairVector P (star a) :=
    scalarRightPairVector_original_adjoint P a
  obtain ⟨hx,hval⟩ := hh
  exact ⟨hx,hval.trans (congrArg (scalarRightPairVector P) ha)⟩

/-- The energy estimate is applied to the actual phase solution and the same
right-pair algebra. The positive weight e remains explicitly quantified. -/
theorem scalarPhaseVariational_rightPair_energy (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a=a)
    (z : ℂ) (hz : 0 < z.re) (hz1 : z.re=1)
    (e : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hem : e ∈ scalarGNSVonNeumann P) (he : 0 ≤ e)
    (heA : Commute e (hilbertBlockA (scalarPairedMultiplicationGraph P
      (scalarPhaseVariational P z hz (scalarRightPairVector P a))).starProjection)) :
    let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz (scalarRightPairVector P a)
    let A := hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection
    let B := hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection
    (inner ℂ ((e*B*star B) η) η).re ≤ ‖a.val‖^2*(inner ℂ ((e*A*A) η) η).re := by
  let ξ : ScalarGNSHilbert P := scalarRightPairVector P a
  let η : ScalarGNSHilbert P := scalarPhaseVariational P z hz ξ
  let G := scalarPairedMultiplicationGraph P η
  let A := hilbertBlockA G.starProjection
  let B := hilbertBlockB G.starProjection
  have hf : ∃ hx : ξ ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨ξ,hx⟩=ξ := scalarSelfadjointRightPair_fixed_original_F P a ha
  obtain ⟨hx,hFx⟩ := hf
  have hs : ∃ hy : η ∈ scalarClosedTomitaDomain P,
      scalarClosedTomita P ⟨η,hy⟩=η := scalarPhaseVariational_fixed P z hz ξ
  obtain ⟨hy,hSy⟩ := hs
  refine weightedBlock_multiplier_energy_bound A B e a.val ξ η z hz1
    (hilbertBlockA_adjoint G) he (scalarPairedProjection_BBstar P η) heA
    (scalarGNS_commutes_with_rightPair P e hem a)
    (scalarGNS_commutes_with_rightPair P A (scalarPairedProjection_A_mem P η) a) ?_ ?_
  · exact scalarPairedProjection_B_left P ⟨η,hy⟩ hSy a
  · exact scalarPhaseVariational_weighted_block_equation P z hz ⟨ξ,hx⟩ hFx e hem
      (IsSelfAdjoint.of_nonneg he).star_eq heA

#print axioms scalarGNS_commutes_with_rightPair
#print axioms scalarSelfadjointRightPair_fixed_original_F
#print axioms scalarPhaseVariational_rightPair_energy
end
end TGLV350.Regular
