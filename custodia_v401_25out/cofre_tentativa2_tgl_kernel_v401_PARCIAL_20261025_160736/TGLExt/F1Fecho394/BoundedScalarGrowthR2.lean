import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic
/-! A bounded scalar orbit cannot have a nonzero real exponential growth
rate. Used to eliminate adjoint deficiency vectors of a unitary generator. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.DeficiencyCriterion

theorem bounded_growth_zero (f : ℝ → ℂ) (a C : ℝ) (ha : a ≠ 0)
    (hd : ∀ t : ℝ, HasDerivAt f ((a:ℂ)*f t) t)
    (hb : ∀ t : ℝ, ‖f t‖ ≤ C) : f 0=0 := by
  let g : ℝ → ℂ := fun t => (Real.exp (-a*t):ℂ)*f t
  have hg (t : ℝ) : HasDerivAt g 0 t := by
    have he := (((hasDerivAt_id t).const_mul (-a)).exp).ofReal_comp
    have hh := he.mul (hd t)
    convert! hh using 1 <;> simp [g,Pi.mul_apply] <;> ring
  have hconst (t : ℝ) : (Real.exp (-a*t):ℂ)*f t=f 0 := by
    simpa [g] using is_const_of_deriv_eq_zero (fun t => (hg t).differentiableAt)
      (fun t => (hg t).deriv) t 0
  have hsolve (t : ℝ) : (Real.exp (a*t):ℂ)*f 0=f t := by
    rw [← hconst t,← mul_assoc,← Complex.ofReal_mul,← Real.exp_add]
    simp
  by_contra hf
  have hn : 0<‖f 0‖ := norm_pos_iff.mpr hf
  have hC : 0≤C := le_trans (norm_nonneg (f 0)) (hb 0)
  let u := C/‖f 0‖+1
  have hu : 0<u := by dsimp [u]; positivity
  let t := Real.log u/a
  have hat : a*t=Real.log u := by dsimp [t]; field_simp
  have hnorm : ‖f t‖=u*‖f 0‖ := by
    rw [← hsolve t,norm_mul,Complex.norm_real,Real.norm_eq_abs,abs_of_pos (Real.exp_pos _),
      hat,Real.exp_log hu]
  have ht := hb t
  rw [hnorm] at ht
  have hu' : u*‖f 0‖=C+‖f 0‖ := by dsimp [u]; field_simp <;> ring
  rw [hu'] at ht
  linarith

end F1Fecho.DeficiencyCriterion
#print axioms F1Fecho.DeficiencyCriterion.bounded_growth_zero
