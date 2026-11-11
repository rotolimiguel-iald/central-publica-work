import Lean
import TGLExt.O16.LightRayFourierBoundary_v2
import TGLExt.O16.LightRayGaussianL2_v4
import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform

set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory Filter Complex
open scoped FourierTransform

namespace ChatgptAudit.LightRayCore016

def gaussianSpectralWeight (b p : ℝ) : ℝ :=
  Real.sqrt (Real.pi/b) * Real.exp (-Real.pi^2*p^2/b + Real.pi^2*p)

theorem gaussian_spectral_positive (b : ℝ) (hb : 0 < b) (p : ℝ) :
    0 < gaussianSpectralWeight b p := by
  unfold gaussianSpectralWeight
  positivity

theorem gaussian_spectral_reflection (b p : ℝ) :
    gaussianSpectralWeight b (-p) =
      Real.exp (-(2*Real.pi^2)*p) * gaussianSpectralWeight b p := by
  unfold gaussianSpectralWeight
  rw [← mul_assoc, mul_comm (Real.exp _) (Real.sqrt _), mul_assoc, ← Real.exp_add]
  congr 2
  ring

theorem gaussian_spectral_memLp (b : ℝ) (hb : 0 < b) :
    MemLp (fun p => (gaussianSpectralWeight b p : ℂ)) 2 (volume : Measure ℝ) := by
  have hm : AEStronglyMeasurable (fun p => (gaussianSpectralWeight b p : ℂ)) volume := by
    apply Continuous.aestronglyMeasurable
    unfold gaussianSpectralWeight
    fun_prop
  apply (memLp_two_iff_integrable_sq_norm hm).2
  have hi := ((integrable_cexp_quadratic (b := ((2*Real.pi^2/b : ℝ) : ℂ))
    (by simp only [ofReal_re]; positivity)
    ((2*Real.pi^2 : ℝ) : ℂ) 0).re).const_mul ((Real.sqrt (Real.pi/b))^2)
  apply hi.congr
  apply Eventually.of_forall
  intro p
  change (Real.sqrt (Real.pi/b))^2 * (exp (-((2*Real.pi^2/b : ℝ) : ℂ) * (p : ℂ)^2 + ((2*Real.pi^2 : ℝ) : ℂ) * (p : ℂ) + 0)).re = _
  dsimp only
  unfold gaussianSpectralWeight
  rw [norm_real, Real.norm_eq_abs, sq_abs, mul_pow, ← Real.exp_nat_mul]
  simp [Complex.exp_re, Complex.mul_re, Complex.mul_im, pow_two]
  ring_nf
  simp

/-- The complex contour justification is supplied by the proved quadratic Gaussian integral. -/
theorem twisted_gaussian_fourier (b : ℝ) (hb : 0 < b) (r p : ℝ) :
    𝓕 (fun x : ℝ => twistedGaussian b r (x : ℂ)) p =
      (gaussianSpectralWeight b p : ℂ) *
        exp (-2*(Real.pi : ℂ)*I*(r : ℂ)*(p : ℂ)) := by
  rw [fourier_explicit]
  let c : ℂ := 2*(b : ℂ)*((r : ℂ)+I*(Real.pi/2 : ℝ)) - 2*(Real.pi : ℂ)*I*(p : ℂ)
  let d : ℂ := -(b : ℂ)*((r : ℂ)+I*(Real.pi/2 : ℝ))^2
  have he : (fun x : ℝ => exp (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) *
      twistedGaussian b r (x : ℂ)) =
      (fun x : ℝ => exp (-(b : ℂ)*(x : ℂ)^2+c*(x : ℂ)+d)) := by
    funext x
    unfold twistedGaussian c d
    rw [← exp_add]
    congr 1
    push_cast
    ring
  rw [he, integral_cexp_quadratic (b := -(b : ℂ)) (by simpa using neg_neg_of_pos hb) c d]
  have hbC : (b : ℂ) ≠ 0 := ofReal_ne_zero.mpr hb.ne'
  have hexp : d-c^2/(4 * -(b : ℂ)) =
      ((-Real.pi^2*p^2/b+Real.pi^2*p : ℝ) : ℂ) +
        (-2*(Real.pi : ℂ)*I*(r : ℂ)*(p : ℂ)) := by
    dsimp [c,d]
    push_cast
    field_simp
    ring_nf
    simp only [I_sq]
    ring
  have hs : ((Real.pi : ℂ)/(b : ℂ))^(1/2 : ℂ) = (Real.sqrt (Real.pi/b) : ℂ) := by
    rw [Real.sqrt_eq_rpow, ofReal_cpow (by positivity), ofReal_div]
    norm_num
  rw [neg_neg, hs, hexp, exp_add, ← ofReal_exp]
  unfold gaussianSpectralWeight
  rw [ofReal_mul]
  ring

#print axioms gaussian_spectral_positive
#print axioms gaussian_spectral_reflection
#print axioms gaussian_spectral_memLp
#print axioms twisted_gaussian_fourier
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
