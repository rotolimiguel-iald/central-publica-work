import TGLExt.PauliInteractionCocycle
import TGLExt.DerivativeFromLinearCutoffError
import TGLExt.CanonicalCocycleDerivative

set_option autoImplicit false
set_option maxHeartbeats 700000
namespace ChatgptAudit.PauliGenerator
open TGLExt Filter Topology Set ChatgptAudit ChatgptAudit.UnitaryDuhamel
  ChatgptAudit.SummableInteraction ChatgptAudit.AdmissibleInteraction
  ChatgptAudit.PauliCocycle ChatgptAudit.CutoffDerivative ChatgptAudit.CocycleDerivative
noncomputable section

theorem cutoff_generators_tendsto (P : SiteProfile) (c : SummableCouplingData) :
    Tendsto (fun N => Complex.I • certifiedPrefix P c N) atTop
      (𝓝 (Complex.I • certifiedInteraction P c)) :=
  tendsto_const_nhds.smul (certified_prefix_converges P c)

/-- The derivative of the infinite cocycle is derived from its linear cutoff error. -/
theorem pauli_cocycle_generator_zero (P : SiteProfile) (c : SummableCouplingData) :
    HasDerivAt (pauliCocycle P c) (Complex.I • certifiedInteraction P c) 0 :=
  hasDerivAt_of_linear_cutoff_error_auto_base
    (pauliCocycle P c) (pauliCutoffCocycle P c)
    (fun N => Complex.I • certifiedPrefix P c N) (Complex.I • certifiedInteraction P c)
    (pauliCutoffError c) (pauli_cutoff_generator P c) (cutoff_generators_tendsto P c)
    (pauli_cutoff_error_nonnegative c) (pauli_cutoff_error_tendsto c)
    (pauli_cocycle_cutoff_bound P c)

theorem pauli_cocycle_generator_equation (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    HasDerivAt (pauliCocycle P c)
      (pauliCocycle P c t * (Complex.I • modularConjugation P t (certifiedInteraction P c))) t :=
  canonical_cocycle_generator_equation P (pauliCocycle P c) (certifiedInteraction P c)
    (pauli_cocycle_twisted P c) (pauli_cocycle_generator_zero P c) t

theorem pauli_cocycle_differentiable (P : SiteProfile) (c : SummableCouplingData) :
    Differentiable ℝ (pauliCocycle P c) :=
  fun t => (pauli_cocycle_generator_equation P c t).differentiableAt

theorem constant_cocycle_forces_zero_interaction (P : SiteProfile) (c : SummableCouplingData)
    (h : ∀ t, pauliCocycle P c t = 1) : certifiedInteraction P c = 0 := by
  have he : pauliCocycle P c = (fun _ : ℝ => (1 : Operator P)) := funext h
  have hd := pauli_cocycle_generator_zero P c
  rw [he] at hd
  have hz := hd.unique (hasDerivAt_const (0 : ℝ) (1 : Operator P))
  have hn := congrArg norm hz
  simp only [norm_smul, Complex.norm_I, one_mul, norm_zero] at hn
  exact norm_eq_zero.mp hn

theorem single_bond_interaction_ne_zero (P : SiteProfile) :
    certifiedInteraction P singleBondData ≠ 0 := by
  intro h
  have hc := certified_single_bond_interacts P
  apply hc
  rw [h]
  simp

theorem single_bond_cocycle_nontrivial (P : SiteProfile) :
    ¬ ∀ t : ℝ, pauliCocycle P singleBondData t = 1 := by
  intro h
  exact single_bond_interaction_ne_zero P
    (constant_cocycle_forces_zero_interaction P singleBondData h)

#print axioms cutoff_generators_tendsto
#print axioms pauli_cocycle_generator_zero
#print axioms pauli_cocycle_generator_equation
#print axioms pauli_cocycle_differentiable
#print axioms constant_cocycle_forces_zero_interaction
#print axioms single_bond_interaction_ne_zero
#print axioms single_bond_cocycle_nontrivial
end
end ChatgptAudit.PauliGenerator
