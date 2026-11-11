import TGLExt.F1Fecho394.MaxwellContourR2
import TGLExt.F1Fecho394.ContourFourierBalanceR2
import TGLExt.F1Fecho394.LowerGaussianReflectionR1
import TGLExt.O16.LightRayFourierBoundary_v2

/-! Pointwise spectral balance of the genuine physical Maxwell coefficient,
with its Gaussian regulator. L2 partial-Fourier transport and removal of the
regulator remain separate obligations; this theorem does not assume them. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
open scoped FourierTransform
namespace F1Fecho.MaxwellStrip
open F1Fecho.MaxwellGlobal F1Fecho.WedgeLaplace
open ChatgptAudit.LightRayCore016 ChatgptAudit.WignerRapidityMeasure016

def regularizedMaxwell (b : ℝ) (q : Fin 2 → ℝ) (f : SchwartzTensor)
    (j : Fin 2) (r : ℝ) : ℂ := lowerGaussian b r * maxwellLaplace q f j r

theorem regularizedMaxwell_real (b : ℝ) (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (f : SchwartzTensor) (j : Fin 2) :
    regularizedMaxwell b y.1 f j y.2 = lowerGaussian b y.2 *
      globalCoefficient (physicalFourierCLM f) (rapidityChart 0 y) j := by
  rw [regularizedMaxwell,maxwellLaplace_real y hy]

theorem regularizedMaxwell_integrable (b : ℝ) (hb : 0 < b)
    (q : Fin 2 → ℝ) (f : SchwartzTensor) (hf : supportedTensorRight f) (j : Fin 2) :
    Integrable (regularizedMaxwell b q f j) := by
  have h := (maxwellLaplace_mem_contourSpace b hb 0 q f hf j).1
  have he : regSlice b 0 0 (maxwellLaplace q f j)=regularizedMaxwell b q f j := by
    funext r
    simp [regSlice,regularized,regularizedMaxwell]
  rw [← he]
  exact h

theorem maxwell_lower_regulator (b : ℝ) (q : Fin 2 → ℝ) (hq : q ≠ 0)
    (f : SchwartzTensor) (hf : IsRealTest f) (j : Fin 2) :
    regularizedLower b 0 (maxwellLaplace q f j)=
      fun r => star (regularizedMaxwell b (-q) f j r) := by
  funext r
  have he : (r:ℂ)+(-Real.pi:ℝ)*I=(r:ℂ)-I*Real.pi := by push_cast; ring
  simp only [regularizedLower,regularizedMaxwell,ofReal_zero,zero_mul,exp_zero,one_mul,he]
  rw [lowerGaussian_reflect,maxwellLaplace_lower_real q hq f hf j r,star_mul]
  exact mul_comm _ _

theorem maxwell_fourier_balance (b : ℝ) (hb : 0 < b) (q : Fin 2 → ℝ)
    (hq : q ≠ 0) (f : SchwartzTensor) (hf : supportedTensorRight f)
    (hr : IsRealTest f) (j : Fin 2) (p : ℝ) :
    (Real.exp (2*Real.pi^2*p):ℂ)*𝓕 (regularizedMaxwell b q f j) p =
      star (𝓕 (regularizedMaxwell b (-q) f j) (-p)) := by
  have h := contour_fourier_balance b p (maxwellLaplace q f j)
    (maxwellLaplace_mem_contourSpace b hb p q f hf j)
  rw [maxwell_lower_regulator b q hq f hr j,fourier_star_reverse] at h
  have he : regularizedReal b 0 (maxwellLaplace q f j)=regularizedMaxwell b q f j := by
    funext r
    simp [regularizedReal,regularizedMaxwell]
  rw [he] at h
  exact h

end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.regularizedMaxwell_real
#print axioms F1Fecho.MaxwellStrip.regularizedMaxwell_integrable
#print axioms F1Fecho.MaxwellStrip.maxwell_lower_regulator
#print axioms F1Fecho.MaxwellStrip.maxwell_fourier_balance
