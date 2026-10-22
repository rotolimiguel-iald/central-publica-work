import TGLExt.ModularFlow
import Mathlib.Tactic.NoncommRing

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
Exact algebraic criteria for an invisible modular cocycle.
These are implications about specified actions, not an assertion that a physical
vacuum flow is geometric. No QFT, trace, or density matrix is assumed here.
-/
namespace ModularRemainder

section Algebra
variable {A : Type*} [Ring A] [StarRing A]

theorem conjugation_eq_iff_commute (u x : A)
    (hleft : star u * u = 1) (hright : u * star u = 1) :
    u * x * star u = x ↔ Commute u x := by
  constructor
  · intro h
    have h' := congrArg (fun y : A => y * u) h
    show u * x = x * u
    simpa only [mul_assoc, hleft, mul_one] using h'
  · intro h
    rw [h.eq, mul_assoc, hright, mul_one]

theorem full_action_invisible_iff_central (u : A)
    (hleft : star u * u = 1) (hright : u * star u = 1) :
    (∀ x : A, u * x * star u = x) ↔ (∀ x : A, Commute u x) := by
  exact forall_congr' fun x => conjugation_eq_iff_commute u x hleft hright

omit [StarRing A] in
theorem corner_image (p x : A) (alpha : A ≃+* A)
    (hp : alpha p = p) (hx : p * x * p = x) :
    p * alpha x * p = alpha x := by
  simpa only [map_mul, hp] using congrArg alpha hx

omit [StarRing A] in
theorem corner_inverse_image (p x : A) (alpha : A ≃+* A)
    (hp : alpha p = p) (hx : p * x * p = x) :
    p * alpha.symm x * p = alpha.symm x := by
  apply corner_image p x alpha.symm _ hx
  exact (alpha.symm_apply_eq).mpr hp.symm

/-- Equality on every corner observable is exactly trivial cocycle action there.
The reference automorphism must preserve the corner. -/
theorem corner_flow_equality_iff (p u : A) (alpha : A ≃+* A)
    (hp : alpha p = p) (hleft : star u * u = 1)
    (hright : u * star u = 1) :
    (∀ x : A, p * x * p = x → u * alpha x * star u = alpha x) ↔
      (∀ x : A, p * x * p = x → Commute u x) := by
  constructor
  · intro h x hx
    have he := h (alpha.symm x) (corner_inverse_image p x alpha hp hx)
    simpa only [alpha.apply_symm_apply] using
      (conjugation_eq_iff_commute u (alpha (alpha.symm x)) hleft hright).mp he
  · intro h x hx
    exact (conjugation_eq_iff_commute u (alpha x) hleft hright).mpr
      (h (alpha x) (corner_image p x alpha hp hx))

end Algebra

section ScalarCorner
variable {A : Type*} [Ring A] [StarRing A] [Algebra ℂ A]

omit [StarRing A] in
/-- An invariant block with scalar compression has trivial conjugation on that
block. Invariance is a separate premise and cannot be removed. -/
theorem invariant_scalar_corner_commutes (p u : A) (c : ℂ)
    (hpp : p * p = p) (hup : Commute u p) (hphase : p * u * p = c • p)
    (x : A) (hx : p * x * p = x) : Commute u x := by
  have hpx : p * x = x := by
    calc p * x = p * (p * x * p) := by rw [hx]
         _ = (p * p) * x * p := by noncomm_ring
         _ = p * x * p := by rw [hpp]
         _ = x := hx
  have hxp : x * p = x := by
    calc x * p = (p * x * p) * p := by rw [hx]
         _ = p * x * p := by simp only [mul_assoc, hpp]
         _ = x := hx
  have hup' : u * p = c • p := by
    calc u * p = p * u * p := by rw [← hup.eq, mul_assoc, hpp]
         _ = c • p := hphase
  have hpu' : p * u = c • p := by rw [← hup.eq, hup']
  show u * x = x * u
  calc u * x = u * (p * x) := by rw [hpx]
       _ = (c • p) * x := by rw [← mul_assoc, hup']
       _ = c • x := by rw [smul_mul_assoc, hpx]
       _ = x * (c • p) := by rw [mul_smul_comm, hxp]
       _ = (x * p) * u := by rw [mul_assoc, hpu']
       _ = x * u := by rw [hxp]

theorem invariant_scalar_corner_invisible (p u : A) (c : ℂ)
    (hpp : p * p = p) (hup : Commute u p) (hphase : p * u * p = c • p)
    (hright : u * star u = 1) (x : A) (hx : p * x * p = x) :
    u * x * star u = x := by
  rw [(invariant_scalar_corner_commutes p u c hpp hup hphase x hx).eq,
      mul_assoc, hright, mul_one]

end ScalarCorner

#print axioms conjugation_eq_iff_commute
#print axioms full_action_invisible_iff_central
#print axioms corner_image
#print axioms corner_inverse_image
#print axioms corner_flow_equality_iff
#print axioms invariant_scalar_corner_commutes
#print axioms invariant_scalar_corner_invisible
end ModularRemainder
