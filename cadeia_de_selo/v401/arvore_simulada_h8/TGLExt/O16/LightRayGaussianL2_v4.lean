import Lean
import TGLExt.O16.LightRayAnalyticCore_v3
import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform
import Mathlib.MeasureTheory.Function.L2Space

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal

namespace ChatgptAudit.LightRayCore016

theorem gaussian_slice_norm (b r x y : ℝ) :
    ‖twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))‖ =
      Real.exp (-b * (x-r)^2 + b * (y-Real.pi/2)^2) := by
  unfold twistedGaussian
  rw [Complex.norm_exp]
  congr 1
  simp [Complex.mul_re, Complex.mul_im, pow_two]
  ring

theorem gaussian_slice_memLp (b : ℝ) (hb : 0 < b) (r y : ℝ) :
    MemLp (fun x : ℝ => twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ)))
      2 (volume : Measure ℝ) := by
  have hm : AEStronglyMeasurable
      (fun x : ℝ => twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))) volume := by
    apply Continuous.aestronglyMeasurable
    unfold twistedGaussian
    fun_prop
  apply (memLp_two_iff_integrable_sq_norm hm).2
  have hi := (integrable_cexp_quadratic (b := ((2*b : ℝ) : ℂ))
    (by simpa using (show 0 < 2*b by positivity))
    ((4*b*r : ℝ) : ℂ) ((2*b*((y-Real.pi/2)^2-r^2) : ℝ) : ℂ)).re
  apply hi.congr
  apply Eventually.of_forall
  intro x
  change (Complex.exp (-((2*b : ℝ) : ℂ) * (x : ℂ)^2 + ((4*b*r : ℝ) : ℂ) * (x : ℂ) + ((2*b*((y-Real.pi/2)^2-r^2) : ℝ) : ℂ))).re = _
  dsimp only
  rw [gaussian_slice_norm, ← Real.exp_nat_mul]
  simp [Complex.exp_re, Complex.mul_re, Complex.mul_im, pow_two]
  congr 1
  ring

theorem gaussian_strip_bound (b : ℝ) (hb : 0 < b) (r x y : ℝ)
    (hy0 : 0 ≤ y) (hypi : y ≤ Real.pi) :
    ‖twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))‖ ≤
      ‖twistedGaussian b r (x : ℂ)‖ := by
  rw [gaussian_slice_norm, gaussian_real_norm, Real.exp_le_exp]
  have h : (y-Real.pi/2)^2 ≤ (Real.pi/2)^2 := by
    nlinarith [mul_nonneg hy0 (sub_nonneg.mpr hypi)]
  nlinarith

theorem product_slice_memLp (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r y : ℝ)
    (hy0 : 0 ≤ y) (hypi : y ≤ Real.pi) :
    MemLp (fun x : ℝ => multiplier a ((x : ℂ) + Complex.I * (y : ℂ)) *
      twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))) 2 (volume : Measure ℝ) := by
  apply (gaussian_slice_memLp b hb r y).of_le
  · apply Continuous.aestronglyMeasurable
    unfold multiplier twistedGaussian
    fun_prop
  · apply Eventually.of_forall
    intro x
    rw [norm_mul]
    simpa using mul_le_mul_of_nonneg_right
      (multiplier_strip_contraction a x y ha hy0 hypi)
      (norm_nonneg (twistedGaussian b r ((x : ℂ) + Complex.I * (y : ℂ))))

#print axioms gaussian_slice_norm
#print axioms gaussian_slice_memLp
#print axioms gaussian_strip_bound
#print axioms product_slice_memLp

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
