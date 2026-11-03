import Lean
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic

/-! A2.3.a: analytic ingredients only. Density and closure in K remain separate obligations. -/
set_option autoImplicit false
noncomputable section

namespace ChatgptAudit.LightRayCore016

def multiplier (a : ℝ) (z : ℂ) : ℂ := Complex.exp (Complex.I * (a : ℂ) * Complex.exp z)

def twistedGaussian (b r : ℝ) (z : ℂ) : ℂ :=
  Complex.exp (-(b : ℂ) * (z - (r : ℂ) - Complex.I * ((Real.pi / 2 : ℝ) : ℂ)) ^ 2)

theorem multiplier_entire (a : ℝ) : Differentiable ℂ (multiplier a) := by
  unfold multiplier
  fun_prop

theorem gaussian_entire (b r : ℝ) : Differentiable ℂ (twistedGaussian b r) := by
  unfold twistedGaussian
  fun_prop

theorem multiplier_strip_norm (a x y : ℝ) :
    ‖multiplier a ((x : ℂ) + Complex.I * (y : ℂ))‖ =
      Real.exp (-a * Real.exp x * Real.sin y) := by
  unfold multiplier
  rw [Complex.norm_exp]
  congr 1
  simp [Complex.mul_re, Complex.mul_im, Complex.exp_im, mul_assoc]

theorem multiplier_strip_contraction (a x y : ℝ)
    (ha : 0 ≤ a) (hy0 : 0 ≤ y) (hypi : y ≤ Real.pi) :
    ‖multiplier a ((x : ℂ) + Complex.I * (y : ℂ))‖ ≤ 1 := by
  rw [multiplier_strip_norm, Real.exp_le_one_iff]
  exact mul_nonpos_of_nonpos_of_nonneg
    (mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr ha) (Real.exp_pos x).le)
    (Real.sin_nonneg_of_nonneg_of_le_pi hy0 hypi)

theorem gaussian_twist (b r x : ℝ) :
    twistedGaussian b r ((x : ℂ) + Complex.I * (Real.pi : ℂ)) =
      star (twistedGaussian b r (x : ℂ)) := by
  unfold twistedGaussian
  rw [Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp only [map_mul, map_neg, map_sub, map_pow, Complex.conj_ofReal, Complex.conj_I]
  push_cast
  ring

theorem multiplier_twist (a x : ℝ) :
    multiplier a ((x : ℂ) + Complex.I * (Real.pi : ℂ)) =
      star (multiplier a (x : ℂ)) := by
  unfold multiplier
  rw [Complex.exp_add, mul_comm Complex.I (Real.pi : ℂ), Complex.exp_pi_mul_I]
  rw [Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp [← Complex.exp_conj]

theorem product_twist (a b r x : ℝ) :
    multiplier a ((x : ℂ) + Complex.I * (Real.pi : ℂ)) *
      twistedGaussian b r ((x : ℂ) + Complex.I * (Real.pi : ℂ)) =
      star (multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ)) := by
  rw [multiplier_twist, gaussian_twist, star_mul']

theorem gaussian_real_norm (b r x : ℝ) :
    ‖twistedGaussian b r (x : ℂ)‖ =
      Real.exp (-b * (x-r)^2 + b * (Real.pi/2)^2) := by
  unfold twistedGaussian
  rw [Complex.norm_exp]
  congr 1
  simp [Complex.mul_re, Complex.mul_im, pow_two]
  ring

#print axioms multiplier_entire
#print axioms gaussian_entire
#print axioms multiplier_strip_norm
#print axioms multiplier_strip_contraction
#print axioms gaussian_twist
#print axioms multiplier_twist
#print axioms product_twist
#print axioms gaussian_real_norm

end ChatgptAudit.LightRayCore016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
