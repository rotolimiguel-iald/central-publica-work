import TGLExt.F1Fecho394.RegularizedContourSpaceR4
import TGLExt.F1Fecho394.LowerStripFourierBalanceR4

/-! Fourier balance follows from the linear contour domain, independently
of the particular coefficient used to establish membership. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
open scoped FourierTransform
namespace F1Fecho.WedgeLaplace

theorem contour_integral_balance (b p : ℝ) (F : ℂ → ℂ)
    (hF : F ∈ contourSpace b p) :
    (Real.exp (2*Real.pi^2*p):ℂ)*
      (∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedReal b 0 F x) =
      ∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedLower b 0 F x := by
  have h := hF.2.2
  simp only [regSlice,ofReal_zero,zero_mul,add_zero] at h
  simp_rw [regularized_real_factor,regularized_lower_factor] at h
  rw [integral_const_mul] at h
  have he : (Real.exp (2*Real.pi^2*p):ℂ)*(Real.exp (-2*Real.pi^2*p):ℂ)=1 := by
    rw [←ofReal_mul,←Real.exp_add]
    ring_nf
    simp
  calc
    _ = (Real.exp (2*Real.pi^2*p):ℂ)*((Real.exp (-2*Real.pi^2*p):ℂ)*
        (∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedLower b 0 F x)) :=
      congrArg (fun z : ℂ => (Real.exp (2*Real.pi^2*p):ℂ)*z) h.symm
    _ = _ := by rw [←mul_assoc,he,one_mul]

theorem contour_fourier_balance (b p : ℝ) (F : ℂ → ℂ)
    (hF : F ∈ contourSpace b p) :
    (Real.exp (2*Real.pi^2*p):ℂ)*𝓕 (regularizedReal b 0 F) p =
      𝓕 (regularizedLower b 0 F) p := by
  have he (g : ℝ → ℂ) : 𝓕 g p =
      ∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*g x := by
    rw [Real.fourier_eq']
    apply integral_congr_ae
    apply ae_of_all
    intro x
    simp only [Real.inner_apply,smul_eq_mul]
    congr 1
    congr 1
    push_cast
    ring
  rw [he,he]
  exact contour_integral_balance b p F hF

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.contour_integral_balance
#print axioms F1Fecho.WedgeLaplace.contour_fourier_balance
