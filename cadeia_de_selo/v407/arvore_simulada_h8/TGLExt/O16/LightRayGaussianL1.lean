import Lean
import TGLExt.O16.LightRayGaussianL2_v4

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter

namespace ChatgptAudit.LightRayCore016

theorem gaussian_slice_integrable (b : ℝ) (hb : 0 < b) (r y : ℝ) :
    Integrable (fun x : ℝ => twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))) := by
  have hi := (GaussianFourier.integrable_cexp_neg_mul_sq_add_real_mul_I
    (b := (b : ℂ)) (by simpa using hb) (y-Real.pi/2)).comp_sub_right r
  apply hi.congr
  apply Eventually.of_forall
  intro x
  dsimp only
  unfold twistedGaussian
  congr 1
  push_cast
  ring

theorem product_slice_integrable (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r y : ℝ)
    (hy0 : 0 ≤ y) (hypi : y ≤ Real.pi) :
    Integrable (fun x : ℝ => multiplier a ((x : ℂ) + Complex.I * (y : ℂ)) *
      twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))) := by
  apply (gaussian_slice_integrable b hb r y).norm.mono'
  · apply Continuous.aestronglyMeasurable
    unfold multiplier twistedGaussian
    fun_prop
  · apply Eventually.of_forall
    intro x
    rw [norm_mul]
    simpa using mul_le_mul_of_nonneg_right
      (multiplier_strip_contraction a x y ha hy0 hypi)
      (norm_nonneg (twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))))

theorem product_uniform_strip_bound (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r x y : ℝ)
    (hy0 : 0 ≤ y) (hypi : y ≤ Real.pi) :
    ‖multiplier a ((x : ℂ) + Complex.I * (y : ℂ)) *
      twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))‖ ≤
      ‖twistedGaussian b r (x : ℂ)‖ := by
  rw [norm_mul]
  calc
    _ ≤ 1 * ‖twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))‖ :=
      mul_le_mul_of_nonneg_right (multiplier_strip_contraction a x y ha hy0 hypi) (norm_nonneg _)
    _ ≤ _ := by simpa using gaussian_strip_bound b hb r x y hy0 hypi

#print axioms gaussian_slice_integrable
#print axioms product_slice_integrable
#print axioms product_uniform_strip_bound

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
