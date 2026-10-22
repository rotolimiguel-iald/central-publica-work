import PauliInteractionCocycle
import Mathlib.Algebra.Star.UnitaryStarAlgAut

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.PerturbedDynamics
open TGLExt Filter Topology Set ChatgptAudit
  ChatgptAudit.UnitaryDuhamel ChatgptAudit.PauliCocycle
  ChatgptAudit.SummableInteraction ChatgptAudit.AdmissibleInteraction
  ChatgptAudit.InteractionOrbit
noncomputable section

def pauliCocycleUnitary (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    unitary (Operator P) := ⟨pauliCocycle P c t,pauli_cocycle_unitary P c t⟩

def perturbedAction (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    Operator P ≃⋆ₐ[ℂ] Operator P :=
  (modularConjugation P t).trans
    (Unitary.conjStarAlgAut ℂ (Operator P) (pauliCocycleUnitary P c t))

theorem perturbed_action_formula (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    perturbedAction P c t A =
      pauliCocycle P c t * modularConjugation P t A * star (pauliCocycle P c t) := rfl

theorem perturbed_action_zero (P : SiteProfile) (c : SummableCouplingData) (A : Operator P) :
    perturbedAction P c 0 A=A := by
  rw [perturbed_action_formula,pauli_cocycle_zero,canonical_conjugation_zero,star_one,
    one_mul,mul_one]

theorem perturbed_action_zero_equiv (P : SiteProfile) (c : SummableCouplingData) :
    perturbedAction P c 0=(StarAlgEquiv.refl : Operator P ≃⋆ₐ[ℂ] Operator P) := by
  apply StarAlgEquiv.ext
  intro A
  exact perturbed_action_zero P c A

theorem perturbed_action_group (P : SiteProfile) (c : SummableCouplingData) (s t : ℝ)
    (A : Operator P) :
    perturbedAction P c s (perturbedAction P c t A)=perturbedAction P c (s+t) A := by
  change pauliCocycle P c s *
    modularConjugation P s (pauliCocycle P c t * modularConjugation P t A *
      star (pauliCocycle P c t)) * star (pauliCocycle P c s) =
    pauliCocycle P c (s+t) * modularConjugation P (s+t) A * star (pauliCocycle P c (s+t))
  rw [map_mul,map_mul,map_star,canonical_conjugation_group]
  rw [pauli_cocycle_twisted P c s t]
  simp only [star_mul,mul_assoc]

theorem perturbed_action_inverse_left (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    perturbedAction P c (-t) (perturbedAction P c t A)=A := by
  rw [perturbed_action_group,neg_add_cancel,perturbed_action_zero]

theorem perturbed_action_inverse_right (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    perturbedAction P c t (perturbedAction P c (-t) A)=A := by
  rw [perturbed_action_group,add_neg_cancel,perturbed_action_zero]

theorem perturbed_action_symm (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    (perturbedAction P c t).symm=perturbedAction P c (-t) := by
  apply StarAlgEquiv.ext
  intro A
  apply (perturbedAction P c t).injective
  change perturbedAction P c t ((perturbedAction P c t).symm A)=
    perturbedAction P c t (perturbedAction P c (-t) A)
  rw [StarAlgEquiv.apply_symm_apply,perturbed_action_inverse_right]

theorem perturbed_action_mul (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A B : Operator P) :
    perturbedAction P c t (A*B)=perturbedAction P c t A*perturbedAction P c t B :=
  map_mul _ A B

theorem perturbed_action_star (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    perturbedAction P c t (star A)=star (perturbedAction P c t A) :=
  map_star _ A

theorem perturbed_action_mem_factor (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) (hA : A∈theFactorObject P) :
    perturbedAction P c t A∈theFactorObject P := by
  rw [perturbed_action_formula]
  exact (theFactorObject P).mul_mem
    ((theFactorObject P).mul_mem (pauli_cocycle_mem_factor P c t)
      ((modularConjugation_preserves_factor P t A).mp hA))
    ((theFactorObject P).toStarSubalgebra.star_mem' (pauli_cocycle_mem_factor P c t))

theorem perturbed_action_factor_iff (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    A∈theFactorObject P ↔ perturbedAction P c t A∈theFactorObject P := by
  constructor
  · exact perturbed_action_mem_factor P c t A
  · intro h
    have hb := perturbed_action_mem_factor P c (-t) (perturbedAction P c t A) h
    rwa [perturbed_action_inverse_left] at hb

theorem perturbed_action_norm (P : SiteProfile) (c : SummableCouplingData) (t : ℝ)
    (A : Operator P) :
    ‖perturbedAction P c t A‖=‖A‖ := by
  rw [perturbed_action_formula,
    CStarRing.norm_mul_mem_unitary _ (Unitary.star_mem (pauli_cocycle_unitary P c t)),
    CStarRing.norm_mem_unitary_mul _ (pauli_cocycle_unitary P c t),
    canonical_conjugation_norm]

theorem perturbed_action_isometry (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    Isometry (perturbedAction P c t) := by
  apply isometry_iff_dist_eq.mpr
  intro A B
  rw [dist_eq_norm,dist_eq_norm,←map_sub,perturbed_action_norm]

theorem perturbed_action_operator_continuous (P : SiteProfile) (c : SummableCouplingData)
    (t : ℝ) : Continuous (perturbedAction P c t) :=
  (perturbed_action_isometry P c t).continuous

theorem perturbed_orbit_continuous_of_canonical (P : SiteProfile) (c : SummableCouplingData)
    (A : Operator P) (hA : Continuous (fun t : ℝ => modularConjugation P t A)) :
    Continuous (fun t : ℝ => perturbedAction P c t A) := by
  simp only [perturbed_action_formula]
  exact ((pauli_cocycle_continuous P c).mul hA).mul
    (pauli_cocycle_continuous P c).star

theorem perturbed_potential_orbit_continuous (P : SiteProfile) (c : SummableCouplingData) :
    Continuous (fun t : ℝ => perturbedAction P c t (certifiedInteraction P c)) :=
  perturbed_orbit_continuous_of_canonical P c _ (interaction_orbit_continuous P c)


#print axioms pauliCocycleUnitary
#print axioms perturbedAction
#print axioms perturbed_action_formula
#print axioms perturbed_action_zero
#print axioms perturbed_action_zero_equiv
#print axioms perturbed_action_group
#print axioms perturbed_action_inverse_left
#print axioms perturbed_action_inverse_right
#print axioms perturbed_action_symm
#print axioms perturbed_action_mul
#print axioms perturbed_action_star
#print axioms perturbed_action_mem_factor
#print axioms perturbed_action_factor_iff
#print axioms perturbed_action_norm
#print axioms perturbed_action_isometry
#print axioms perturbed_action_operator_continuous
#print axioms perturbed_orbit_continuous_of_canonical
#print axioms perturbed_potential_orbit_continuous
end
end ChatgptAudit.PerturbedDynamics
