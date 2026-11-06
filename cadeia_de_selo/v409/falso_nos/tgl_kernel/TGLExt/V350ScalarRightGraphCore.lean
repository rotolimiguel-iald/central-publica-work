import TGLExt.V350FixedVectorGraphCore
import TGLExt.V350ScalarRightProjectionPair
import TGLExt.V350ScalarRightHilbertCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt ClosedSubmodule ChatgptAudit.Continuous049
noncomputable section

private theorem originalFixedSetClosure {H A : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [AddCommGroup A] [Module ℂ A] [StarAddMonoid A] [StarModule ℂ A]
    (j : A →ₗ[ℂ] H) (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hc : IsClosed (Set.range (fun x : D => ((x : H),F x))))
    (hj : ∀ a : A, ∃ hv : j a ∈ D, F ⟨j a,hv⟩ = j (star a))
    (hd : ∀ η : D, F η = (η : H) → (η : H) ≠ 0 →
      ∃ a : A, star a = a ∧ 0 < (inner ℂ (η : H) (j a)).re) :
    closure {x : H | ∃ a : A, star a = a ∧ j a = x} =
      {x : H | ∃ hx : x ∈ D, F ⟨x,hx⟩ = x} :=
  congrArg (fun V : Submodule ℝ H => (V : Set H))
    (selfadjointVectorSubmodule_closure j D F hc hj hd)

private theorem originalGraphByDetection {H A : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [AddCommGroup A] [Module ℂ A] [StarAddMonoid A] [StarModule ℂ A]
    (j : A →ₗ[ℂ] H) (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hc : IsClosed (Set.range (fun x : D => ((x : H),F x))))
    (hj : ∀ a : A, ∃ hv : j a ∈ D, F ⟨j a,hv⟩ = j (star a))
    (hmaps : ∀ x : D, F x ∈ D)
    (hinv : ∀ x : D, F ⟨F x,hmaps x⟩ = (x : H))
    (hd : ∀ η : D, F η = (η : H) → (η : H) ≠ 0 →
      ∃ a : A, star a = a ∧ 0 < (inner ℂ (η : H) (j a)).re) :
    closure (Set.range (fun a : A => (j a,j (star a)))) =
      Set.range (fun x : D => ((x : H),F x)) :=
  conjugateGraph_closure_eq_original j D F hc hj hmaps hinv
    (selfadjointVectorSubmodule_closure j D F hc hj hd)

/-- Density is in the real fixed space of the original maximal adjoint F. -/
theorem scalarRightSelfadjointVectors_closure (P : SiteProfile) :
    closure {x : ScalarGNSHilbert P | ∃ a : scalarPairedRightAlgebra P,
      star a = a ∧ scalarRightPairVector P a = x} =
      {x : ScalarGNSHilbert P | ∃ hx : x ∈ scalarTomitaAdjointDomain P,
        scalarTomitaAdjoint P ⟨x,hx⟩ = x} := by
  refine originalFixedSetClosure (H := ScalarGNSHilbert P)
    (A := scalarPairedRightAlgebra P) (scalarRightPairVector P)
    (scalarTomitaAdjointDomain P) (scalarTomitaAdjoint P).toFun
    ?_ ?_ ?_
  · exact scalarTomitaAdjoint_isClosed P
  · intro a
    exact scalarRightPairVector_original_adjoint P a
  · intro η hη hn
    exact scalarRight_selfadjoint_detects_fixed P η hη hn

/-- The closure is the graph of the already defined original F, not a new
operator defined by the right algebra. All graph-core hypotheses are proved. -/
theorem scalarRightPairGraph_closure_eq_original (P : SiteProfile) :
    closure (scalarRightPairGraph P) = Set.range (fun y : scalarTomitaAdjointDomain P =>
      ((y : ScalarGNSHilbert P),scalarTomitaAdjoint P y)) := by
  refine originalGraphByDetection (H := ScalarGNSHilbert P)
    (A := scalarPairedRightAlgebra P) (scalarRightPairVector P)
    (scalarTomitaAdjointDomain P) (scalarTomitaAdjoint P).toFun
    ?_ ?_ ?_ ?_ ?_
  · exact scalarTomitaAdjoint_isClosed P
  · intro a
    exact scalarRightPairVector_original_adjoint P a
  · intro η
    exact scalarTomitaAdjoint_maps_domain P η
  · intro η
    exact scalarTomitaAdjoint_involutive P η
  · intro η hη hn
    exact scalarRight_selfadjoint_detects_fixed P η hη hn

theorem scalarRightPairGraph_original_subset_closure (P : SiteProfile) :
    Set.range (fun y : scalarTomitaAdjointDomain P =>
      ((y : ScalarGNSHilbert P),scalarTomitaAdjoint P y)) ⊆ closure (scalarRightPairGraph P) :=
  (scalarRightPairGraph_closure_eq_original P).symm.subset

#print axioms scalarRightSelfadjointVectors_closure
#print axioms scalarRightPairGraph_closure_eq_original
#print axioms scalarRightPairGraph_original_subset_closure
end
end TGLV350.Regular
