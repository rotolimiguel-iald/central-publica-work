import TGLExt.V350ResolventSquareRoot

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit.Continuous049
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Commutation transports the actual graph and therefore its domain. -/
theorem bounded_graph_transport_of_commute (A B U : H →L[ℂ] H)
    (hi : Function.Injective A) (hAU : Commute A U) (hBU : Commute B U)
    (x y : H) (hxy : (x,y) ∈ (boundedGraphOperator A B hi).graph) :
    (U x,U y) ∈ (boundedGraphOperator A B hi).graph := by
  obtain ⟨z,hx,hy⟩ := (bounded_graph_param_iff A B hi x y).mp hxy
  apply (bounded_graph_param_iff A B hi (U x) (U y)).mpr
  refine ⟨U z,?_,?_⟩
  · exact (congrArg (fun T : H →L[ℂ] H => T z) hAU.eq).trans (congrArg U hx)
  · exact (congrArg (fun T : H →L[ℂ] H => T z) hBU.eq).trans (congrArg U hy)

theorem complement_commutes_of_commute (R U : H →L[ℂ] H)
    (h : Commute R U) : Commute (1-R) U := by
  change (1-R)*U = U*(1-R)
  simp only [sub_mul,mul_sub,one_mul,mul_one,h.eq]

theorem positive_sqrt_commutes_of_commute (R U : H →L[ℂ] H)
    (h : Commute R U) : Commute (CFC.sqrt R : H →L[ℂ] H) U := by
  rw [CFC.sqrt_eq_cfc]
  exact h.cfc_nnreal NNReal.sqrt

theorem resolvent_graph_transport_of_commute (R U : H →L[ℂ] H)
    (hi : Function.Injective R) (h : Commute R U)
    (x y : H) (hxy : (x,y) ∈ (resolventGraphOperator R hi).graph) :
    (U x,U y) ∈ (resolventGraphOperator R hi).graph :=
  bounded_graph_transport_of_commute R (1-R) U hi h
    (complement_commutes_of_commute R U h) x y hxy

theorem resolvent_sqrt_graph_transport_of_commute (R U : H →L[ℂ] H)
    (hR : 0 ≤ R) (hi : Function.Injective R) (h : Commute R U)
    (x y : H) (hxy : (x,y) ∈ (resolventSquareRoot R hR hi).graph) :
    (U x,U y) ∈ (resolventSquareRoot R hR hi).graph :=
  bounded_graph_transport_of_commute (CFC.sqrt R) (CFC.sqrt (1-R)) U
    (positive_sqrt_injective R hR hi) (positive_sqrt_commutes_of_commute R U h)
    (positive_sqrt_commutes_of_commute (1-R) U (complement_commutes_of_commute R U h))
    x y hxy

#print axioms bounded_graph_transport_of_commute
#print axioms complement_commutes_of_commute
#print axioms positive_sqrt_commutes_of_commute
#print axioms resolvent_graph_transport_of_commute
#print axioms resolvent_sqrt_graph_transport_of_commute
end
end TGLV350.Regular
