import Lean
import TGLExt.O16.LightRayGaussianL1

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Complex
open scoped Topology

namespace ChatgptAudit.LightRayCore016

def verticalDifference (F : ℂ → ℂ) (w T : ℝ) : ℂ :=
  I * (∫ y : ℝ in (0:ℝ)..w, F ((T : ℂ) + (y : ℂ) * I)) -
  I * (∫ y : ℝ in (0:ℝ)..w, F ((-T : ℝ) + (y : ℂ) * I))

theorem rectangle_identity (F : ℂ → ℂ) (hF : Differentiable ℂ F) (w T : ℝ) :
    (∫ x : ℝ in -T..T, F (x : ℂ)) -
      (∫ x : ℝ in -T..T, F ((x : ℂ) + (w : ℂ) * I)) +
      verticalDifference F w T = 0 := by
  have h := integral_boundary_rect_eq_zero_of_differentiableOn F (-T)
    ((T : ℂ) + (w : ℂ) * I) hF.differentiableOn
  have he :
      (∫ x : ℝ in -T..T, F (x : ℂ)) -
        (∫ x : ℝ in -T..T, F ((x : ℂ) + (w : ℂ) * I)) +
        I * (∫ y : ℝ in (0:ℝ)..w, F ((T : ℂ) + (y : ℂ) * I)) -
        I * (∫ y : ℝ in (0:ℝ)..w, F ((-T : ℝ) + (y : ℂ) * I)) = 0 := by
    simpa only [neg_im, ofReal_im, neg_zero, ofReal_zero, zero_mul, add_zero, neg_re,
      ofReal_re, add_re, mul_re, I_re, mul_zero, I_im, tsub_zero, add_im, mul_im,
      mul_one, zero_add, smul_eq_mul, ofReal_neg] using h
  unfold verticalDifference
  linear_combination he

/-- No Hardy theorem is assumed: this is exactly Cauchy plus three explicit limits. -/
theorem horizontal_integral_eq_of_vertical_limit
    (F : ℂ → ℂ) (hF : Differentiable ℂ F) (w : ℝ)
    (h0 : Integrable (fun x : ℝ => F (x : ℂ)))
    (hw : Integrable (fun x : ℝ => F ((x : ℂ) + (w : ℂ) * I)))
    (hv : Tendsto (verticalDifference F w) atTop (𝓝 0)) :
    (∫ x : ℝ, F ((x : ℂ) + (w : ℂ) * I)) = ∫ x : ℝ, F (x : ℂ) := by
  have ht := intervalIntegral_tendsto_integral hw tendsto_neg_atTop_atBot tendsto_id
  have hb := intervalIntegral_tendsto_integral h0 tendsto_neg_atTop_atBot tendsto_id
  have he : (fun T : ℝ => ∫ x : ℝ in -T..T, F ((x : ℂ) + (w : ℂ) * I)) =
      fun T : ℝ => (∫ x : ℝ in -T..T, F (x : ℂ)) + verticalDifference F w T := by
    funext T
    have h := rectangle_identity F hF w T
    linear_combination -h
  simp only [id_eq] at ht hb
  rw [he] at ht
  simpa using tendsto_nhds_unique ht (hb.add hv)

#print axioms rectangle_identity
#print axioms horizontal_integral_eq_of_vertical_limit

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
