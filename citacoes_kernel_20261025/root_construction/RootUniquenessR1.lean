import TGLExt.V350ResolventSquareRoot
import TGLExt.ContinuousModularResolvent
import TGLExt.ContinuousModularReconstruction

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLExt.CitationRoots
open TGLV350.Regular ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The full partial graph determines its bounded resolvent. No positivity is needed here. -/
theorem resolvent_determined_by_graph (R Q : H →L[ℂ] H)
    (hiR : Function.Injective R) (hiQ : Function.Injective Q)
    (h : resolventGraphOperator R hiR = resolventGraphOperator Q hiQ) : R = Q := by
  apply ContinuousLinearMap.ext
  intro u
  have hp : (R u,(1-R) u) ∈ (resolventGraphOperator R hiR).graph :=
    (bounded_graph_param_iff R (1-R) hiR _ _).mpr ⟨u,rfl,rfl⟩
  rw [h] at hp
  have he := (resolvent_graph_equation Q hiQ _ _).mp hp
  change R u-Q (R u)=Q ((1-R) u) at he
  have hs : R u+(1-R) u=u := by change R u+(u-R u)=u; abel
  calc
    R u = Q (R u)+Q ((1-R) u) := by rw [← he]; abel
    _ = Q (R u+(1-R) u) := (map_add Q _ _).symm
    _ = Q u := by rw [hs]

/-- Uniqueness for the entire resolvent-constructed class, on full partial-map domains.
This does not assert that every abstract positive self-adjoint operator has this representation. -/
theorem resolvent_roots_unique_of_square (R Q : H →L[ℂ] H)
    (hR : 0 ≤ R) (hQ : 0 ≤ Q) (hiR : Function.Injective R) (hiQ : Function.Injective Q)
    (hR1 : R ≤ 1) (hQ1 : Q ≤ 1)
    (hsq : partialOperatorSquare (resolventSquareRoot R hR hiR) =
      partialOperatorSquare (resolventSquareRoot Q hQ hiQ)) :
    resolventSquareRoot R hR hiR = resolventSquareRoot Q hQ hiQ := by
  rw [resolventSquareRoot_square R hR hiR hR1,
      resolventSquareRoot_square Q hQ hiQ hQ1] at hsq
  have he := resolvent_determined_by_graph R Q hiR hiQ hsq
  subst Q
  rfl

theorem continuous_resolvent_positive (c : ℝ) : 0 ≤ continuousResolvent c :=
  Commute.mul_nonneg (spectralA_nonneg c) (spectralA_nonneg c) (Commute.refl _)

theorem continuous_resolvent_le_one (c : ℝ) : continuousResolvent c ≤ 1 := by
  apply sub_nonneg.mp
  rw [continuous_resolvent_complement]
  exact Commute.mul_nonneg (spectralB_nonneg c) (spectralB_nonneg c) (Commute.refl _)

theorem continuous_resolvent_injective (c : ℝ) :
    Function.Injective (continuousResolvent c) :=
  (spectralA_injective c).comp (spectralA_injective c)

/-- Existing exponential multiplier T_c equals the canonical root constructed from its
bounded resolvent. This is equality of partial operators, including their domains. -/
theorem continuous_operator_eq_resolvent_root (c : ℝ) :
    continuousModularOperator c = resolventSquareRoot (continuousResolvent c)
      (continuous_resolvent_positive c) (continuous_resolvent_injective c) := by
  apply LinearPMap.eq_of_eq_graph
  ext p
  rcases p with ⟨x,y⟩
  rw [continuous_modular_graph_from_cfc]
  exact (bounded_graph_param_iff _ _ _ x y).symm

/-- Every positive injective contraction whose constructed root squares to Delta_c
produces exactly T_c. The class restriction is explicit; this is not unrestricted Kato. -/
theorem continuous_root_unique_in_resolvent_class (c : ℝ) (R : SpectralHilbert →L[ℂ] SpectralHilbert)
    (hR : 0 ≤ R) (hiR : Function.Injective R) (hR1 : R ≤ 1)
    (hsq : partialOperatorSquare (resolventSquareRoot R hR hiR) = continuousModularDelta c) :
    resolventSquareRoot R hR hiR = continuousModularOperator c := by
  have hc : partialOperatorSquare (continuousModularOperator c) = continuousModularDelta c := rfl
  rw [continuous_operator_eq_resolvent_root c] at hc
  have he := resolvent_roots_unique_of_square R (continuousResolvent c)
    hR (continuous_resolvent_positive c) hiR (continuous_resolvent_injective c)
    hR1 (continuous_resolvent_le_one c) (hsq.trans hc.symm)
  exact he.trans (continuous_operator_eq_resolvent_root c).symm

#print axioms resolvent_determined_by_graph
#print axioms resolvent_roots_unique_of_square
#print axioms continuous_resolvent_positive
#print axioms continuous_resolvent_le_one
#print axioms continuous_resolvent_injective
#print axioms continuous_operator_eq_resolvent_root
#print axioms continuous_root_unique_in_resolvent_class
end
end TGLExt.CitationRoots
