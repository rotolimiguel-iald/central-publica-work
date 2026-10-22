import LocalInteractionCocycle
import DerivativeFromLinearCutoffError
import CanonicalCocycleDerivative

set_option autoImplicit false
set_option maxHeartbeats 700000
namespace ChatgptAudit.LocalGenerator
open TGLExt Filter Topology Set ChatgptAudit ChatgptAudit.UnitaryDuhamel
  ChatgptAudit.SummableInteraction ChatgptAudit.LocalInteraction
  ChatgptAudit.LocalCocycle ChatgptAudit.CutoffDerivative ChatgptAudit.CocycleDerivative
noncomputable section

theorem local_cutoff_generators_tendsto (P : SiteProfile) (c : LocalInteractionData P) :
    Tendsto (fun N => Complex.I • localPrefix P c N) atTop
      (𝓝 (Complex.I • localPotential P c)) :=
  tendsto_const_nhds.smul (local_prefix_tendsto P c)

/-- The derivative of the infinite cocycle is derived from its linear cutoff error. -/
theorem local_cocycle_generator_zero (P : SiteProfile) (c : LocalInteractionData P) :
    HasDerivAt (localCocycle P c) (Complex.I • localPotential P c) 0 :=
  hasDerivAt_of_linear_cutoff_error_auto_base
    (localCocycle P c) (localCutoffCocycle P c)
    (fun N => Complex.I • localPrefix P c N) (Complex.I • localPotential P c)
    (localCutoffError P c) (local_cutoff_generator P c) (local_cutoff_generators_tendsto P c)
    (local_cutoff_error_nonnegative P c) (local_cutoff_error_tendsto P c)
    (local_cocycle_cutoff_bound P c)

theorem local_cocycle_generator_equation (P : SiteProfile) (c : LocalInteractionData P) (t : ℝ) :
    HasDerivAt (localCocycle P c)
      (localCocycle P c t * (Complex.I • modularConjugation P t (localPotential P c))) t :=
  canonical_cocycle_generator_equation P (localCocycle P c) (localPotential P c)
    (local_cocycle_twisted P c) (local_cocycle_generator_zero P c) t

theorem local_cocycle_differentiable (P : SiteProfile) (c : LocalInteractionData P) :
    Differentiable ℝ (localCocycle P c) :=
  fun t => (local_cocycle_generator_equation P c t).differentiableAt

theorem constant_local_cocycle_forces_zero_potential (P : SiteProfile) (c : LocalInteractionData P)
    (h : ∀ t, localCocycle P c t = 1) : localPotential P c = 0 := by
  have he : localCocycle P c = (fun _ : ℝ => (1 : Operator P)) := funext h
  have hd := local_cocycle_generator_zero P c
  rw [he] at hd
  have hz := hd.unique (hasDerivAt_const (0 : ℝ) (1 : Operator P))
  have hn := congrArg norm hz
  simp only [norm_smul, Complex.norm_I, one_mul, norm_zero] at hn
  exact norm_eq_zero.mp hn


theorem nonzero_local_potential_has_nontrivial_cocycle (P : SiteProfile) (c : LocalInteractionData P)
    (h : localPotential P c ≠ 0) : ¬ ∀ t : ℝ, localCocycle P c t = 1 := by
  intro ht
  exact h (constant_local_cocycle_forces_zero_potential P c ht)

#print axioms local_cutoff_generators_tendsto
#print axioms local_cocycle_generator_zero
#print axioms local_cocycle_generator_equation
#print axioms local_cocycle_differentiable
#print axioms constant_local_cocycle_forces_zero_potential
#print axioms nonzero_local_potential_has_nontrivial_cocycle
end
end ChatgptAudit.LocalGenerator
