import TGLExt.F1Fecho394.WedgeLaplaceAnalyticR3
import TGLExt.O16.LightRayContourTransport_v2

/-! The existing O16 contour transport is reused with the actual weaker
hypothesis available for supported Schwartz tests: continuity on the closed
strip and complex differentiability in its interior, not entire analyticity.
The vertical limit and horizontal integrability remain explicit here. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Complex Set
open scoped Topology
namespace F1Fecho.WedgeLaplace
open ChatgptAudit.LightRayCore016

theorem lower_rectangle_identity (F : ℂ → ℂ)
    (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip) (T : ℝ) :
    (∫ x : ℝ in -T..T, F (x : ℂ)) -
      (∫ x : ℝ in -T..T, F ((x : ℂ) + (-Real.pi : ℝ) * I)) +
      verticalDifference F (-Real.pi) T = 0 := by
  have hp : -Real.pi ≤ 0 := neg_nonpos.mpr Real.pi_pos.le
  have h := integral_boundary_rect_eq_zero_of_continuousOn_of_differentiableOn
    F (-T) ((T : ℂ) + (-Real.pi : ℝ) * I)
    (hc.mono (by
      intro z hz
      have hi := hz.2
      simpa [lowerClosedStrip, uIcc, min_eq_right hp, max_eq_left hp] using hi))
    (hd.mono (by
      intro z hz
      have hi := hz.2
      simpa [lowerOpenStrip, min_eq_right hp, max_eq_left hp] using hi))
  have he :
      (∫ x : ℝ in -T..T, F (x : ℂ)) -
        (∫ x : ℝ in -T..T, F ((x : ℂ) + (-Real.pi : ℝ) * I)) +
        I * (∫ y : ℝ in (0:ℝ)..(-Real.pi), F ((T : ℂ) + (y : ℂ) * I)) -
        I * (∫ y : ℝ in (0:ℝ)..(-Real.pi), F ((-T : ℝ) + (y : ℂ) * I)) = 0 := by
    simpa only [neg_im, ofReal_im, neg_zero, ofReal_zero, zero_mul, add_zero, neg_re,
      ofReal_re, add_re, mul_re, I_re, mul_zero, I_im, tsub_zero, add_im, mul_im,
      mul_one, zero_add, smul_eq_mul, ofReal_neg] using h
  unfold verticalDifference
  linear_combination he

theorem lower_horizontal_integral_eq_of_vertical_limit
    (F : ℂ → ℂ) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (h0 : Integrable (fun x : ℝ => F (x : ℂ)))
    (hw : Integrable (fun x : ℝ => F ((x : ℂ) + (-Real.pi : ℝ) * I)))
    (hv : Tendsto (verticalDifference F (-Real.pi)) atTop (𝓝 0)) :
    (∫ x : ℝ, F ((x : ℂ) + (-Real.pi : ℝ) * I)) = ∫ x : ℝ, F (x : ℂ) := by
  have ht := intervalIntegral_tendsto_integral hw tendsto_neg_atTop_atBot tendsto_id
  have hb := intervalIntegral_tendsto_integral h0 tendsto_neg_atTop_atBot tendsto_id
  have he : (fun T : ℝ => ∫ x : ℝ in -T..T, F ((x : ℂ) + (-Real.pi : ℝ) * I)) =
      fun T : ℝ => (∫ x : ℝ in -T..T, F (x : ℂ)) + verticalDifference F (-Real.pi) T := by
    funext T
    have h := lower_rectangle_identity F hc hd T
    linear_combination -h
  simp only [id_eq] at ht hb
  rw [he] at ht
  simpa using tendsto_nhds_unique ht (hb.add hv)

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.lower_rectangle_identity
#print axioms F1Fecho.WedgeLaplace.lower_horizontal_integral_eq_of_vertical_limit
