import Mathlib.Algebra.Group.Commute.Defs
import Mathlib.Algebra.Star.Basic
import Mathlib.Tactic

set_option autoImplicit false

namespace TGLV354.TraceCompletion

/-- Algebraic shift equivalence with a positive lag. The intended consumer is
the cyclic completion of the regular core's positive trace. -/
def ShiftRelated {A : Type*} [Monoid A] (a b : A) : Prop :=
  ∃ n : ℕ, 0 < n ∧ ∃ r s : A,
    a * r = r * b ∧ s * a = b * s ∧ a ^ n = r * s ∧ b ^ n = s * r

namespace ShiftRelated
variable {A : Type*} [Monoid A] {a b c : A}

theorem refl (a : A) : ShiftRelated a a := by
  exact ⟨1, Nat.one_pos, 1, a, by simp, by simp, by simp, by simp⟩

theorem symm (h : ShiftRelated a b) : ShiftRelated b a := by
  obtain ⟨n, hn, r, s, hr, hs, ha, hb⟩ := h
  exact ⟨n, hn, s, r, hs.symm, hr.symm, hb, ha⟩

theorem trans (h : ShiftRelated a b) (k : ShiftRelated b c) : ShiftRelated a c := by
  obtain ⟨n, hn, r, s, hr, hs, ha, hb⟩ := h
  obtain ⟨m, hm, u, v, hu, hv, hb', hc⟩ := k
  have hp : ∀ j : ℕ, a ^ j * r = r * b ^ j := by
    intro j
    exact ((show SemiconjBy r b a from hr.symm).pow_right j).eq.symm
  have hq : ∀ j : ℕ, v * b ^ j = c ^ j * v := by
    intro j
    exact ((show SemiconjBy v b c from hv).pow_right j).eq
  refine ⟨n+m, by omega, r*u, v*s, ?_, ?_, ?_, ?_⟩
  · calc
      a * (r*u) = (a*r)*u := (mul_assoc _ _ _).symm
      _ = (r*b)*u := by rw [hr]
      _ = r*(b*u) := mul_assoc _ _ _
      _ = r*(u*c) := by rw [hu]
      _ = (r*u)*c := (mul_assoc _ _ _).symm
  · calc
      (v*s)*a = v*(s*a) := mul_assoc _ _ _
      _ = v*(b*s) := by rw [hs]
      _ = (v*b)*s := (mul_assoc _ _ _).symm
      _ = (c*v)*s := by rw [hv]
      _ = c*(v*s) := mul_assoc _ _ _
  · calc
      a ^ (n+m) = a ^ m * a ^ n := by rw [Nat.add_comm, pow_add]
      _ = a ^ m * (r*s) := by rw [ha]
      _ = (a ^ m*r)*s := (mul_assoc _ _ _).symm
      _ = (r*b ^ m)*s := by rw [hp]
      _ = (r*(u*v))*s := by rw [hb']
      _ = (r*u)*(v*s) := by simp only [mul_assoc]
  · calc
      c ^ (n+m) = c ^ n * c ^ m := pow_add _ _ _
      _ = c ^ n * (v*u) := by rw [hc]
      _ = (c ^ n*v)*u := (mul_assoc _ _ _).symm
      _ = (v*b ^ n)*u := by rw [hq]
      _ = (v*(s*r))*u := by rw [hb]
      _ = (v*s)*(r*u) := by simp only [mul_assoc]

theorem cyclic (x y : A) : ShiftRelated (x*y) (y*x) := by
  exact ⟨1, Nat.one_pos, x, y, by simp only [mul_assoc],
    by simp only [mul_assoc], by simp, by simp⟩

theorem map {B : Type*} [Monoid B] (f : A →* B) (h : ShiftRelated a b) :
    ShiftRelated (f a) (f b) := by
  obtain ⟨n, hn, r, s, hr, hs, ha, hb⟩ := h
  refine ⟨n, hn, f r, f s, ?_, ?_, ?_, ?_⟩
  · simpa only [map_mul] using congrArg f hr
  · simpa only [map_mul] using congrArg f hs
  · simpa only [map_mul, map_pow] using congrArg f ha
  · simpa only [map_mul, map_pow] using congrArg f hb

theorem star_transport [StarMul A] (h : ShiftRelated a b) :
    ShiftRelated (star a) (star b) := by
  obtain ⟨n, hn, r, s, hr, hs, ha, hb⟩ := h
  refine ⟨n, hn, star s, star r, ?_, ?_, ?_, ?_⟩
  · simpa only [star_mul] using congrArg star hs
  · simpa only [star_mul] using congrArg star hr
  · simpa only [star_mul, star_pow] using congrArg star ha
  · simpa only [star_mul, star_pow] using congrArg star hb

end ShiftRelated
end TGLV354.TraceCompletion
