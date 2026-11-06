import TGLExt.F1Fecho394.LowerGaussianControlR2

/-! The Gaussian regulator has the same lower-strip conjugate boundary as
the physical coefficient. Removing it later requires a separate L2 limit. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open Complex
namespace F1Fecho.WedgeLaplace
open ChatgptAudit.LightRayCore016

theorem lowerGaussian_reflect (b r : ℝ) :
    lowerGaussian b ((r:ℂ)-I*Real.pi)=star (lowerGaussian b r) := by
  unfold lowerGaussian twistedGaussian
  rw [Complex.star_def,←Complex.exp_conj]
  congr 1
  simp only [map_mul,map_sub,map_neg,map_pow,map_div,map_zero,map_ofNat,
    Complex.conj_I,Complex.conj_ofReal]
  push_cast
  ring

theorem lowerGaussian_real_bound (b : ℝ) (hb : 0 < b) (r : ℝ) :
    ‖lowerGaussian b r‖ ≤ Real.exp (b*Real.pi^2/4) := by
  have h := lowerGaussian_bound b hb r 0 (neg_nonpos.mpr Real.pi_pos.le) le_rfl
  simp only [ofReal_zero,zero_mul,add_zero] at h
  apply h.trans
  rw [gaussian_real_norm]
  apply Real.exp_le_exp.mpr
  nlinarith [sq_nonneg r]

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.lowerGaussian_reflect
#print axioms F1Fecho.WedgeLaplace.lowerGaussian_real_bound
