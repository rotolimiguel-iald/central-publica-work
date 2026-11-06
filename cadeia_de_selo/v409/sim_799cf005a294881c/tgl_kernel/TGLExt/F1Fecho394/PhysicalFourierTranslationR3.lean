import TGLExt.F1Fecho394.MinkowskiSchwartzFourierR4
import TGLExt.O16.OrbitTranslationFaithfulness_v2

/-! Translation phases for the actual Fourier conventions. The inverse transform
at metricFlip(p)/(2*pi) has the positive angular phase used by U1. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
open scoped FourierTransform RealInnerProductSpace
namespace F1Fecho.PhysicalFourier
open F1Fecho.MaxwellGlobal ChatgptAudit.WignerOrbit016
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem fourier_translate (f : Spacetime → E) (a k : Spacetime) :
    𝓕 (fun x => f (x-a)) k =
      Complex.exp (((-2*Real.pi*inner ℝ a k : ℝ) : ℂ)*Complex.I) • 𝓕 f k := by
  have h := congrFun (VectorFourier.fourierIntegral_comp_add_right
    Real.fourierChar (volume : Measure Spacetime) (innerₗ Spacetime) f (-a)) k
  change 𝓕 (f ∘ fun x => x + -a) k =
    Real.fourierChar (inner ℝ (-a) k) • 𝓕 f k at h
  simpa [sub_eq_add_neg,Function.comp_def,Circle.smul_def,Real.fourierChar_apply,
    inner_neg_left,mul_neg,neg_mul] using h

theorem fourierInv_translate (f : Spacetime → E) (a k : Spacetime) :
    𝓕⁻ (fun x => f (x-a)) k =
      Complex.exp (((2*Real.pi*inner ℝ a k : ℝ) : ℂ)*Complex.I) • 𝓕⁻ f k := by
  rw [Real.fourierInv_eq_fourier_neg,fourier_translate,Real.fourierInv_eq_fourier_neg]
  simp only [inner_neg_right,mul_neg,neg_mul,neg_neg]

theorem angular_pairing (a p : Spacetime) :
    2*Real.pi*inner ℝ a ((2*Real.pi)⁻¹ • metricFlip p) =
      orbitPairing (fun i => a i) (fun i => p i) := by
  rw [real_inner_smul_right,real_inner_comm (metricFlip p) a,metricFlip_inner]
  unfold orbitPairing
  field_simp [Real.pi_ne_zero]
  <;> ring

theorem angular_inverse_fourier_translate (f : Spacetime → E) (a p : Spacetime) :
    𝓕⁻ (fun x => f (x-a)) ((2*Real.pi)⁻¹ • metricFlip p) =
      phase (orbitPairing (fun i => a i) (fun i => p i)) •
        𝓕⁻ f ((2*Real.pi)⁻¹ • metricFlip p) := by
  rw [fourierInv_translate,angular_pairing]
  rfl

theorem unscaled_forward_fourier_translate (f : Spacetime → E) (a p : Spacetime) :
    𝓕 (fun x => f (x-a)) (metricFlip p) =
      phase ((-2*Real.pi)*orbitPairing (fun i => a i) (fun i => p i)) •
        𝓕 f (metricFlip p) := by
  rw [fourier_translate,real_inner_comm (metricFlip p) a,metricFlip_inner]
  simp only [phase,orbitPairing,mul_comm]
end F1Fecho.PhysicalFourier
#print axioms F1Fecho.PhysicalFourier.fourier_translate
#print axioms F1Fecho.PhysicalFourier.fourierInv_translate
#print axioms F1Fecho.PhysicalFourier.angular_pairing
#print axioms F1Fecho.PhysicalFourier.angular_inverse_fourier_translate
#print axioms F1Fecho.PhysicalFourier.unscaled_forward_fourier_translate
