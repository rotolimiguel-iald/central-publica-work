import TGLExt.V351AveragePolarRight
import TGLExt.V350ScalarRightAdjointPair
import TGLExt.V351AntiunitaryResolventPhase

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- A selfadjoint element with the actual polar right identity produces a
vector fixed by both original closed S and its maximal adjoint F. -/
theorem scalarWeightStar_fixed_pair_of_polarRight (P : SiteProfile)
    (A : scalarWeightStarCore P) (hstar : star A = A)
    (hE : A.val ∈ scalarPolarRightAlgebra P) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P A ∧
    ∃ hF : scalarWeightStarEmbedding P A ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarWeightStarEmbedding P A,hF⟩ =
        scalarWeightStarEmbedding P A := by
  have hs : star A.val = A.val := congrArg Subtype.val hstar
  change ScalarPolarRight P A.val ∧ ScalarPolarRight P (star A.val) at hE
  let z : scalarWeightLeftIdeal P := ⟨A.val,A.property.1⟩
  let B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
    antiunitaryConjugate (scalarTomitaPolarFactor P)
    (scalarGNSRepresentation P (star A.val))
  have hB : IsSelfAdjoint B := by
    apply antiunitaryConjugate_selfadjoint
    change star (scalarGNSRepresentation P (star A.val)) =
      scalarGNSRepresentation P (star A.val)
    rw [← map_star,star_star,hs]
  have hr (a : scalarWeightLeftIdeal P) :
      B (scalarWeightGNSEmbedding P a) =
        scalarGNSRepresentation P a.val (scalarWeightStarEmbedding P A) := by
    have hex : ∃ ha : a.val*A.val ∈ scalarWeightLeftIdeal P,
        scalarWeightGNSEmbedding P ⟨a.val*A.val,ha⟩ =
          B (scalarWeightGNSEmbedding P a) := hE.1 a
    obtain ⟨ha,he⟩ := hex
    have heq : (⟨a.val*A.val,ha⟩ : scalarWeightLeftIdeal P) =
        scalarWeightLeftProduct P a.val z := Subtype.ext rfl
    exact he.symm.trans ((congrArg (scalarWeightGNSEmbedding P) heq).trans
      (scalarWeightGNSAction_intertwines P a.val z).symm)
  let d : ScalarRightAdjointPair P B :=
    { vector := scalarWeightStarEmbedding P A
      adjointVector := scalarWeightStarEmbedding P A
      right := hr
      adjoint := by
        intro a
        exact (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
          T (scalarWeightGNSEmbedding P a)) hB.star_eq).trans (hr a) }
  constructor
  · exact (scalarClosedTomita_extends_weight_star P A).trans
      (congrArg (scalarWeightStarEmbedding P) hstar)
  · exact scalarRightAdjointPair_maximal (P := P) (R := B) d

/-- The square e*e of the SAME one-sided average yields actual simultaneous
fixed vectors. No new weight, modular operator or average is substituted. -/
theorem regularAverage_square_fixed_pair (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ A : scalarWeightStarCore P,
      A.val.val = star (regularAverage P δ)*regularAverage P δ ∧
      scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
        scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P A ∧
      ∃ hF : scalarWeightStarEmbedding P A ∈ scalarTomitaAdjointDomain P,
        scalarTomitaAdjoint P ⟨scalarWeightStarEmbedding P A,hF⟩ =
          scalarWeightStarEmbedding P A := by
  let e : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularAverage P δ,regularAverage_mem P δ⟩
  have hefin : e ∈ scalarWeightLeftIdeal P :=
    HasFiniteDualSquare.scalar_finite P _ (regularAverage_hasFiniteDualSquare P δ hδ)
  have hz : star e*e ∈ scalarWeightLeftIdeal P :=
    scalarWeightLeftIdeal_left_mul P (star e) e hefin
  have hzs : star (star e*e) = star e*e := by rw [star_mul,star_star]
  have hfin : star e*e ∈ scalarWeightStarCore P := by
    constructor
    · exact hz
    · change star (star e*e) ∈ scalarWeightLeftIdeal P
      rw [hzs]
      exact hz
  let A : scalarWeightStarCore P := ⟨star e*e,hfin⟩
  have hstar : star A = A := Subtype.ext hzs
  have heE : e ∈ scalarPolarRightAlgebra P :=
    regularAverage_mem_scalarPolarRightAlgebra P δ hδ
  have hE : A.val ∈ scalarPolarRightAlgebra P :=
    (scalarPolarRightAlgebra P).mul_mem ((scalarPolarRightAlgebra P).star_mem' heE) heE
  exact ⟨A,rfl,scalarWeightStar_fixed_pair_of_polarRight P A hstar hE⟩

end
end TGLV350.Regular
