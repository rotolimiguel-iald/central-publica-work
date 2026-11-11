import TGLExt.F1Fecho394.PhysicalFourierTranslationR3
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-! A genuine support-sensitive estimate for the positive-angular Fourier
kernel on the lower rapidity strip. This is only the scalar kernel estimate;
integrated Schwartz support, its L2 boundary and equality with KWR are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WedgeLaplace

def longitudinal (m t x : ℝ) (z : ℂ) : ℂ :=
  (m:ℂ)*(((t-x)/2:ℝ)*Complex.exp z+((t+x)/2:ℝ)*Complex.exp (-z))

def kernel (m t x v : ℝ) (z : ℂ) : ℂ :=
  Complex.exp (Complex.I*(longitudinal m t x z-(v:ℂ)))

theorem longitudinal_real (m t x r : ℝ) :
    longitudinal m t x r=(m*(t*Real.cosh r-x*Real.sinh r):ℝ) := by
  simp only [longitudinal,← Complex.ofReal_exp,← Complex.ofReal_neg,
    Real.cosh_eq,Real.sinh_eq]
  push_cast
  ring

theorem longitudinal_strip_im (m t x r θ : ℝ) :
    (longitudinal m t x ((r:ℂ)-Complex.I*θ)).im =
      m*Real.sin θ*((x-t)*Real.exp r+(x+t)*Real.exp (-r))/2 := by
  simp [longitudinal,Complex.exp_im,Complex.mul_im,Complex.sub_re,Complex.sub_im,
    Complex.neg_re,Complex.neg_im,Real.sin_neg]
  ring

theorem kernel_norm_strip (m t x v r θ : ℝ) :
    ‖kernel m t x v ((r:ℂ)-Complex.I*θ)‖ =
      Real.exp (-(m*Real.sin θ*((x-t)*Real.exp r+(x+t)*Real.exp (-r))/2)) := by
  rw [kernel,Complex.norm_exp]
  congr 1
  simp only [Complex.mul_re,Complex.I_re,Complex.I_im,zero_mul,one_mul,
    zero_sub,Complex.sub_im,Complex.ofReal_im,sub_zero,longitudinal_strip_im]

theorem kernel_norm_le_one_on_right_wedge (m t x v r θ : ℝ)
    (hm : 0 ≤ m) (hw : |t| ≤ x) (hθ : 0 ≤ θ) (hπ : θ ≤ Real.pi) :
    ‖kernel m t x v ((r:ℂ)-Complex.I*θ)‖ ≤ 1 := by
  rw [kernel_norm_strip]
  apply Real.exp_le_one_iff.mpr
  have hxt : 0 ≤ x-t := sub_nonneg.mpr ((le_abs_self t).trans hw)
  have hxp : 0 ≤ x+t := by linarith [neg_abs_le t]
  have hp : 0 ≤ (x-t)*Real.exp r+(x+t)*Real.exp (-r) :=
    add_nonneg (mul_nonneg hxt (Real.exp_pos r).le) (mul_nonneg hxp (Real.exp_pos (-r)).le)
  exact neg_nonpos.mpr (div_nonneg (mul_nonneg (mul_nonneg hm
    (Real.sin_nonneg_of_nonneg_of_le_pi hθ hπ)) hp) (by norm_num))

theorem kernel_norm_lt_one_inside (m t x v r θ : ℝ)
    (hm : 0 < m) (hw : |t| < x) (hθ : 0 < θ) (hπ : θ < Real.pi) :
    ‖kernel m t x v ((r:ℂ)-Complex.I*θ)‖ < 1 := by
  rw [kernel_norm_strip]
  apply Real.exp_lt_one_iff.mpr
  have hxt : 0 < x-t := sub_pos.mpr ((le_abs_self t).trans_lt hw)
  have hxp : 0 < x+t := by linarith [neg_abs_le t]
  have hp : 0 < (x-t)*Real.exp r+(x+t)*Real.exp (-r) :=
    add_pos (mul_pos hxt (Real.exp_pos r)) (mul_pos hxp (Real.exp_pos (-r)))
  exact neg_neg_of_pos (div_pos (mul_pos (mul_pos hm
    (Real.sin_pos_of_pos_of_lt_pi hθ hπ)) hp) (by norm_num))

theorem kernel_entire (m t x v : ℝ) : Differentiable ℂ (kernel m t x v) := by
  unfold kernel longitudinal
  fun_prop

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.longitudinal_real
#print axioms F1Fecho.WedgeLaplace.longitudinal_strip_im
#print axioms F1Fecho.WedgeLaplace.kernel_norm_le_one_on_right_wedge
#print axioms F1Fecho.WedgeLaplace.kernel_norm_lt_one_inside
#print axioms F1Fecho.WedgeLaplace.kernel_entire
