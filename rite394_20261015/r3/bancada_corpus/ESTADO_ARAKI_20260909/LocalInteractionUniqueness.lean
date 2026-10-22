import UnitaryCocycleUniqueness
import LocalInteractionGenerator
import LocalInteractionDynamics

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.LocalUniqueness
open TGLExt ChatgptAudit.UnitaryDuhamel ChatgptAudit.LocalInteraction
  ChatgptAudit.LocalCocycle ChatgptAudit.LocalGenerator ChatgptAudit.LocalDynamics
  ChatgptAudit.CocycleUniqueness
noncomputable section

theorem local_cocycle_unique (P : SiteProfile) (c : LocalInteractionData P)
    (u : ℝ → Operator P)
    (hc : ∀ s t, u (s+t) = u s * modularConjugation P s (u t))
    (hd : HasDerivAt u (Complex.I • localPotential P c) 0)
    (h0 : u 0 = 1) : u = localCocycle P c :=
  canonical_cocycle_unique_from_derivative P u (localCocycle P c) (localPotential P c)
    (local_potential_selfadjoint P c) hc (local_cocycle_twisted P c)
    hd (local_cocycle_generator_zero P c) h0 (local_cocycle_zero P c)
    (local_cocycle_unitary P c)

theorem same_potential_same_cocycle (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localPotential P c = localPotential P d) :
    localCocycle P c = localCocycle P d := by
  apply local_cocycle_unique P d (localCocycle P c) (local_cocycle_twisted P c)
  · rw [← h]
    exact local_cocycle_generator_zero P c
  · exact local_cocycle_zero P c

theorem same_potential_same_dynamics (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localPotential P c = localPotential P d) (t : ℝ) (A : Operator P) :
    localDynamics P c t A = localDynamics P d t A := by
  simp only [local_dynamics_formula, same_potential_same_cocycle P c d h]

theorem same_cocycle_same_potential (P : SiteProfile) (c d : LocalInteractionData P)
    (h : localCocycle P c = localCocycle P d) :
    localPotential P c = localPotential P d := by
  have hc := local_cocycle_generator_zero P c
  rw [h] at hc
  have he := hc.unique (local_cocycle_generator_zero P d)
  have hz : Complex.I • (localPotential P c - localPotential P d) = 0 := by
    rw [smul_sub, he, sub_self]
  exact sub_eq_zero.mp ((smul_eq_zero.mp hz).resolve_left Complex.I_ne_zero)

theorem potential_eq_iff_cocycle_eq (P : SiteProfile) (c d : LocalInteractionData P) :
    localPotential P c = localPotential P d ↔ localCocycle P c = localCocycle P d :=
  ⟨same_potential_same_cocycle P c d, same_cocycle_same_potential P c d⟩

#print axioms local_cocycle_unique
#print axioms same_potential_same_cocycle
#print axioms same_potential_same_dynamics
#print axioms same_cocycle_same_potential
#print axioms potential_eq_iff_cocycle_eq
end
end ChatgptAudit.LocalUniqueness
