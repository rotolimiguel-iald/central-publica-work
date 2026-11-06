import TGLExt.F1Fecho394.GaussianLogScalarR4

/-! Fixed real Gaussian probability kernel and its exact angular Fourier
transform. A later group average uses this kernel with time c*t. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.GaussianLogScalar
open ChatgptAudit

def gaussianWeight (t:ℝ):ℝ:=(Real.sqrt Real.pi)⁻¹*Real.exp (-t^2)

theorem gaussianWeight_continuous : Continuous gaussianWeight := by unfold gaussianWeight; fun_prop

theorem gaussianWeight_integrable : Integrable gaussianWeight volume := by
  unfold gaussianWeight
  have h:= (integrable_exp_neg_mul_sq (by norm_num : (0:ℝ)<1)).const_mul ((Real.sqrt Real.pi)⁻¹)
  simpa only [gaussianWeight, neg_one_mul] using h

theorem gaussianWeight_nonneg (t:ℝ) : 0≤gaussianWeight t := by unfold gaussianWeight; positivity

theorem gaussianWeight_integral : ∫t:ℝ,gaussianWeight t=1 := by
  unfold gaussianWeight
  rw [integral_const_mul]
  have h: (∫t:ℝ,Real.exp (-t^2))=Real.sqrt Real.pi := by
    simpa only [neg_one_mul,div_one] using integral_gaussian 1
  rw [h,inv_mul_cancel₀ (ne_of_gt (Real.sqrt_pos.2 Real.pi_pos))]

theorem gaussian_fourier_constant : ((Real.pi:ℂ)/1)^(1/2:ℂ)=(Real.sqrt Real.pi:ℂ) := by
  have hr: (∫t:ℝ,Real.exp (-t^2))=Real.sqrt Real.pi := by
    simpa only [neg_one_mul,div_one] using integral_gaussian 1
  have h:=gaussian_fourier 1 (by norm_num) 0
  simp only [modularPhase,mul_zero,Complex.ofReal_zero,zero_mul,Complex.exp_zero,
    mul_one,neg_one_mul,zero_pow (by norm_num : (2:ℕ)≠0),neg_zero,zero_div,
    Complex.ofReal_one,div_one] at h ⊢
  rw [integral_complex_ofReal, hr] at h
  exact h.symm

theorem gaussianWeight_fourier (c l:ℝ) :
    (∫t:ℝ,(gaussianWeight t:ℂ)*modularPhase (c*t) l)=
      (Real.exp (-(c*l)^2/4):ℂ) := by
  have hp (t:ℝ):modularPhase (c*t) l=modularPhase t (c*l) := by
    unfold modularPhase
    congr 1
    push_cast
    ring
  simp only [gaussianWeight,Complex.ofReal_mul,mul_assoc,hp]
  rw [integral_const_mul]
  have h:=gaussian_fourier 1 (by norm_num) (c*l)
  simp only [neg_one_mul] at h
  rw [h]
  simp only [Complex.ofReal_one]
  rw [gaussian_fourier_constant]
  have hn:(Real.sqrt Real.pi:ℂ)≠0:=Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sqrt_pos.2 Real.pi_pos))
  rw [Complex.ofReal_inv,←mul_assoc,inv_mul_cancel₀ hn,one_mul,Complex.ofReal_exp]
  congr 1
  push_cast
  ring

end F1Fecho.GaussianLogScalar
#print axioms F1Fecho.GaussianLogScalar.gaussianWeight_integrable
#print axioms F1Fecho.GaussianLogScalar.gaussianWeight_integral
#print axioms F1Fecho.GaussianLogScalar.gaussianWeight_fourier
