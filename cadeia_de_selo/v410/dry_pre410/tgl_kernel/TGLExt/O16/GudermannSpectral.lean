import Lean
import TGLExt.ContinuousModularZero
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.Gudermann016

/-- Spectral, dimensionless coordinate; not surface gravity. -/
def gd (x : ℝ) : ℝ := Real.arcsin (Real.tanh x)

theorem gd_mem_principal (x : ℝ) :
    gd x ∈ Set.Icc (-(Real.pi/2)) (Real.pi/2) :=
  Real.arcsin_mem_Icc _

theorem sin_gd (x : ℝ) : Real.sin (gd x) = Real.tanh x := by
  exact Real.sin_arcsin (Real.neg_one_lt_tanh x).le (Real.tanh_lt_one x).le

theorem spectral_q_is_sine (kappa : ℝ) :
    TGLExt.qKappa kappa = Real.sin (gd (kappa/2)) :=
  (sin_gd (kappa/2)).symm

theorem spectral_q_iff_principal (kappa theta : ℝ)
    (hl : -(Real.pi/2) ≤ theta) (hu : theta ≤ Real.pi/2) :
    TGLExt.qKappa kappa = Real.sin theta ↔ theta = gd (kappa/2) := by
  constructor
  · intro h
    calc
      theta = Real.arcsin (Real.sin theta) := (Real.arcsin_sin hl hu).symm
      _ = gd (kappa/2) := congrArg Real.arcsin h.symm
  · intro h
    rw [h]
    exact spectral_q_is_sine kappa

theorem spectral_alpha_is_cosine (kappa : ℝ) :
    TGLExt.alphaKappa kappa = Real.cos (gd (kappa/2)) := by
  have hc : 0 ≤ Real.cos (gd (kappa/2)) := Real.cos_arcsin_nonneg _
  have ha : 0 < TGLExt.alphaKappa kappa := by
    exact inv_pos.mpr (Real.cosh_pos _)
  have hsq := TGLExt.one_eq_q_sq_add_alpha_sq kappa
  have htrig := Real.sin_sq_add_cos_sq (gd (kappa/2))
  rw [← spectral_q_is_sine] at htrig
  nlinarith

/-- The unrestricted equivalence is false: the sine does not select a branch. -/
theorem unrestricted_branch_counterexample :
    TGLExt.qKappa 0 = Real.sin (2*Real.pi) ∧ 2*Real.pi ≠ gd (0/2) := by
  constructor
  · simp
  · simp only [zero_div, gd, Real.tanh_zero, Real.arcsin_zero]
    exact mul_ne_zero (by norm_num) Real.pi_ne_zero

#print axioms gd_mem_principal
#print axioms sin_gd
#print axioms spectral_q_is_sine
#print axioms spectral_q_iff_principal
#print axioms spectral_alpha_is_cosine
#print axioms unrestricted_branch_counterexample
end ChatgptAudit.Gudermann016


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
