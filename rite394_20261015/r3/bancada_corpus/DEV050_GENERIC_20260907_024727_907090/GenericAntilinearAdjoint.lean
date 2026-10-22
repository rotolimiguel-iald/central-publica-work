import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Continuous050
open Complex
noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The inner product identity follows from semilinearity and the norm, by polarization. -/
theorem antiunitary_inner_conj (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x y : H) :
    inner ℂ (J x) (J y) = star (inner ℂ x y) := by
  have hp : ‖J x + J y‖ = ‖x + y‖ := by
    rw [← map_add, J.norm_map]
  have hm : ‖J x - J y‖ = ‖x - y‖ := by
    rw [← map_sub, J.norm_map]
  have hip : ‖J x + I • J y‖ = ‖x - I • y‖ := by
    conv_rhs => rw [← J.norm_map (x - I • y)]
    rw [map_sub, map_smulₛₗ]
    simp
  have him : ‖J x - I • J y‖ = ‖x + I • y‖ := by
    conv_rhs => rw [← J.norm_map (x + I • y)]
    rw [map_add, map_smulₛₗ]
    simp [sub_eq_add_neg]
  rw [inner_eq_sum_norm_sq_div_four, inner_eq_sum_norm_sq_div_four]
  simp only [RCLike.I_to_complex, hp, hm, hip, him]
  simp
  ring

theorem antiunitary_pairing_flip (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (x y : H) :
    inner ℂ (J x) y = inner ℂ (J y) x := by
  have h := antiunitary_inner_conj J x (J y)
  rw [hJ y] at h
  change inner ℂ (J x) y = (starRingEnd ℂ) (inner ℂ x (J y)) at h
  simpa only [inner_conj_symm] using h

/-- The antilinear partial map S=JT has exactly the domain of T. -/
def genericTomita (T : H →ₗ.[ℂ] H) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    H →ₛₗ.[starRingEnd ℂ] H where
  domain := T.domain
  toFun := J.toLinearEquiv.toLinearMap.comp T.toFun

theorem generic_tomita_apply (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x : T.domain) :
    genericTomita T J x = J (T x) := rfl

/-- The candidate domain is later proved to equal the full adjoint domain. -/
def genericAdjointDomain (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) : Submodule ℂ H :=
  T.domain.comap J.toLinearEquiv.toLinearMap

def genericAdjointInput (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    genericAdjointDomain T J →ₛₗ[starRingEnd ℂ] T.domain :=
  ((J.toLinearEquiv.toLinearMap.domRestrict (genericAdjointDomain T J)).codRestrict
    T.domain (fun y => y.property))

theorem generic_adjoint_input_coe (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (y : genericAdjointDomain T J) :
    (genericAdjointInput T J y : H) = J (y : H) := rfl

/-- This partial map is identified as the maximal antilinear adjoint when T is self-adjoint. -/
def genericTomitaAdjoint (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) : H →ₛₗ.[starRingEnd ℂ] H where
  domain := genericAdjointDomain T J
  toFun := T.toFun.comp (genericAdjointInput T J)

theorem generic_tomita_adjoint_apply (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (y : genericAdjointDomain T J) :
    genericTomitaAdjoint T J y = T (genericAdjointInput T J y) := rfl

theorem generic_pairing_with_J (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : T.domain) (y : H) :
    inner ℂ (genericTomita T J x) y = inner ℂ (J y) (T x) :=
  antiunitary_pairing_flip J hJ (T x) y

/-- Adjoint convention: the representative lies in the first inner-product argument. -/
theorem generic_adjoint_pairing [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (x : T.domain) (y : genericAdjointDomain T J) :
    inner ℂ (genericTomita T J x) (y : H) =
      inner ℂ (genericTomitaAdjoint T J y) (x : H) := by
  have hs : T.IsFormalAdjoint T := by
    have h := LinearPMap.adjoint_isFormalAdjoint (T := T) hT.dense_domain
    simpa only [LinearPMap.isSelfAdjoint_def.mp hT] using h
  rw [generic_pairing_with_J]
  exact (hs (genericAdjointInput T J y) x).symm

/-- Maximality uses the actual Mathlib adjoint, not only the formal pairing identity. -/
theorem generic_adjoint_maximal [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) {y z : H}
    (h : ∀ x : T.domain,
      inner ℂ (genericTomita T J x) y = inner ℂ z (x : H)) :
    ∃ hy : y ∈ genericAdjointDomain T J, genericTomitaAdjoint T J ⟨y, hy⟩ = z := by
  have hadj : J y ∈ (LinearPMap.adjoint T).domain := by
    apply LinearPMap.mem_adjoint_domain_of_exists
    refine ⟨z, fun x => ?_⟩
    rw [← h x, generic_pairing_with_J T J hJ]
  have hy : y ∈ genericAdjointDomain T J := by
    change J y ∈ T.domain
    rwa [LinearPMap.isSelfAdjoint_def.mp hT] at hadj
  refine ⟨hy, ?_⟩
  apply hT.dense_domain.eq_of_inner_left ℂ
  intro x hx
  exact (generic_adjoint_pairing T hT J hJ ⟨x, hx⟩ ⟨y, hy⟩).symm.trans (h ⟨x, hx⟩)

theorem generic_adjoint_domain_iff [CompleteSpace H] (T : H →ₗ.[ℂ] H)
    (hT : IsSelfAdjoint T) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hJ : Function.Involutive J) (y : H) :
    y ∈ genericAdjointDomain T J ↔ ∃ z : H, ∀ x : T.domain,
      inner ℂ (genericTomita T J x) y = inner ℂ z (x : H) := by
  constructor
  · intro hy
    exact ⟨genericTomitaAdjoint T J ⟨y, hy⟩,
      fun x => generic_adjoint_pairing T hT J hJ x ⟨y, hy⟩⟩
  · rintro ⟨z, hz⟩
    exact (generic_adjoint_maximal T hT J hJ hz).choose

/-- The composition domain is paid explicitly; no invariance of all of D(T) is assumed. -/
theorem generic_composition_domain (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) (x : T.domain) :
    genericTomita T J x ∈ genericAdjointDomain T J ↔ T x ∈ T.domain := by
  change J (J (T x)) ∈ T.domain ↔ T x ∈ T.domain
  rw [hJ]

theorem generic_adjoint_comp (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : T.domain) (hx : T x ∈ T.domain) :
    genericTomitaAdjoint T J
      ⟨genericTomita T J x, (generic_composition_domain T J hJ x).mpr hx⟩ =
      T ⟨T x, hx⟩ := by
  change T (genericAdjointInput T J
    ⟨genericTomita T J x, (generic_composition_domain T J hJ x).mpr hx⟩) = T ⟨T x, hx⟩
  congr 1
  apply Subtype.ext
  exact hJ (T x)

#print axioms antiunitary_inner_conj
#print axioms antiunitary_pairing_flip
#print axioms genericTomita
#print axioms generic_tomita_apply
#print axioms genericAdjointDomain
#print axioms genericAdjointInput
#print axioms generic_adjoint_input_coe
#print axioms genericTomitaAdjoint
#print axioms generic_tomita_adjoint_apply
#print axioms generic_pairing_with_J
#print axioms generic_adjoint_pairing
#print axioms generic_adjoint_maximal
#print axioms generic_adjoint_domain_iff
#print axioms generic_composition_domain
#print axioms generic_adjoint_comp

end
end ChatgptAudit.Continuous050
