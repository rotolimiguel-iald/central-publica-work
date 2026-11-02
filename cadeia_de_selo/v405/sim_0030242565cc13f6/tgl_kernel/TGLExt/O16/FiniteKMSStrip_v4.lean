import Lean
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Complex Matrix
namespace ChatgptAudit.FiniteKMS016

def phase (a : ℝ) (z : ℂ) : ℂ := exp (I * z * (a : ℂ))

theorem phase_entire (a : ℝ) : Differentiable ℂ (phase a) := by
  unfold phase
  fun_prop

theorem phase_upper (a t : ℝ) :
    phase a ((t : ℂ)+I) = phase a t * (Real.exp (-a) : ℂ) := by
  unfold phase
  rw [show I * ((t : ℂ)+I) * (a : ℂ) = I * (t : ℂ) * (a : ℂ) + (-a : ℝ) by
    push_cast; calc
      _ = I * (t : ℂ) * (a : ℂ) + I^2 * (a : ℂ) := by ring
      _ = _ := by rw [I_sq]; ring]
  rw [exp_add, ofReal_exp]

theorem phase_strip_bound (a : ℝ) (z : ℂ) (h0 : 0 ≤ z.im) (h1 : z.im ≤ 1) :
    ‖phase a z‖ ≤ Real.exp |a| := by
  rw [phase, norm_exp]
  apply Real.exp_le_exp.mpr
  simp only [mul_re, I_re, I_im, ofReal_re, ofReal_im, zero_mul, one_mul, mul_zero, sub_zero, zero_sub]
  calc -z.im * a ≤ |z.im * a| := by simpa only [neg_mul] using neg_le_abs (z.im*a)
    _ = |z.im| * |a| := abs_mul _ _
    _ = z.im * |a| := by rw [abs_of_nonneg h0]
    _ ≤ 1 * |a| := mul_le_mul_of_nonneg_right h1 (abs_nonneg a)
    _ = |a| := one_mul _

def kmsFunction (A B : Matrix (Fin 2) (Fin 2) ℂ) (z : ℂ) : ℂ :=
  A 0 0 * B 0 0 / 3 + 2 * A 1 1 * B 1 1 / 3 +
    A 0 1 * B 1 0 / 3 * phase (-Real.log 2) z +
    2 * A 1 0 * B 0 1 / 3 * phase (Real.log 2) z

theorem kmsFunction_entire (A B : Matrix (Fin 2) (Fin 2) ℂ) :
    Differentiable ℂ (kmsFunction A B) := by
  unfold kmsFunction phase
  fun_prop

theorem phase_log2_upper (t : ℝ) :
    phase (Real.log 2) ((t : ℂ)+I) = phase (Real.log 2) t / 2 := by
  rw [phase_upper, Real.exp_neg, Real.exp_log (by norm_num : (0:ℝ)<2)]
  push_cast
  ring

theorem phase_neglog2_upper (t : ℝ) :
    phase (-Real.log 2) ((t : ℂ)+I) = 2 * phase (-Real.log 2) t := by
  rw [phase_upper, neg_neg, Real.exp_log (by norm_num : (0:ℝ)<2)]
  push_cast
  ring

theorem phase_neg_parameter (a t : ℝ) : phase a (-t : ℝ) = phase (-a) t := by
  unfold phase
  push_cast
  congr 1
  ring

theorem kmsFunction_upper_swaps_order (A B : Matrix (Fin 2) (Fin 2) ℂ) (t : ℝ) :
    kmsFunction A B ((t : ℂ)+I) = kmsFunction B A (-t : ℝ) := by
  unfold kmsFunction
  rw [phase_log2_upper, phase_neglog2_upper, phase_neg_parameter, phase_neg_parameter, neg_neg]
  ring

theorem kmsFunction_strip_bound (A B : Matrix (Fin 2) (Fin 2) ℂ) :
    ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ 1 → ‖kmsFunction A B z‖ ≤ M := by
  refine ⟨‖A 0 0 * B 0 0 / 3 + 2 * A 1 1 * B 1 1 / 3‖ +
    ‖A 0 1 * B 1 0 / 3‖ * Real.exp (abs (-Real.log 2)) +
    ‖2 * A 1 0 * B 0 1 / 3‖ * Real.exp (abs (Real.log 2)), ?_⟩
  intro z h0 h1
  unfold kmsFunction
  calc
    _ ≤ ‖A 0 0 * B 0 0 / 3 + 2 * A 1 1 * B 1 1 / 3‖ +
      ‖A 0 1 * B 1 0 / 3 * phase (-Real.log 2) z‖ +
      ‖2 * A 1 0 * B 0 1 / 3 * phase (Real.log 2) z‖ :=
        (norm_add_le _ _).trans (add_le_add_left (norm_add_le _ _) _)
    _ ≤ _ := by
      simp only [norm_mul]
      exact add_le_add (add_le_add_right
        (mul_le_mul_of_nonneg_left (phase_strip_bound _ z h0 h1) (norm_nonneg _)) _)
        (mul_le_mul_of_nonneg_left (phase_strip_bound _ z h0 h1) (norm_nonneg _))

theorem phase_log2_nontrivial : phase (Real.log 2) (Real.pi / Real.log 2 : ℝ) = -1 := by
  have hlog : Real.log 2 ≠ 0 := (Real.log_pos (by norm_num : (1:ℝ)<2)).ne'
  unfold phase
  have he : I * ((Real.pi / Real.log 2 : ℝ) : ℂ) * (Real.log 2 : ℂ) = (Real.pi : ℂ)*I := by
    push_cast
    have hc : (Real.log 2 : ℂ) ≠ 0 := by exact_mod_cast hlog
    field_simp [hc]
  rw [he, exp_pi_mul_I]

#print axioms phase_entire
#print axioms phase_upper
#print axioms phase_strip_bound
#print axioms kmsFunction_entire
#print axioms phase_log2_upper
#print axioms phase_neglog2_upper
#print axioms phase_neg_parameter
#print axioms kmsFunction_upper_swaps_order
#print axioms kmsFunction_strip_bound
#print axioms phase_log2_nontrivial
end ChatgptAudit.FiniteKMS016


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
