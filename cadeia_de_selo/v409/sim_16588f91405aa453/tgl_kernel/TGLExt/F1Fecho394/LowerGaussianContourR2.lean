import TGLExt.F1Fecho394.LowerGaussianControlR2

/-! All hypotheses of the strip contour transport are now discharged for
bounded analytic coefficients multiplied by a Gaussian and exp(k*z). -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Complex Set
open scoped Topology
namespace F1Fecho.WedgeLaplace
open ChatgptAudit.LightRayCore016

theorem regularized_continuous (b k p : ℝ) (F : ℂ → ℂ)
    (hc : ContinuousOn F lowerClosedStrip) :
    ContinuousOn (regularized b k p F) lowerClosedStrip := by
  exact ((by fun_prop : Continuous (fun z : ℂ => exp ((-2*(Real.pi:ℂ)*I*(p:ℂ)+(k:ℂ))*z))).continuousOn.mul
    (lowerGaussian_entire b).continuous.continuousOn).mul hc

theorem regularized_differentiable (b k p : ℝ) (F : ℂ → ℂ)
    (hd : DifferentiableOn ℂ F lowerOpenStrip) :
    DifferentiableOn ℂ (regularized b k p F) lowerOpenStrip := by
  exact ((by fun_prop : Differentiable ℂ (fun z : ℂ => exp ((-2*(Real.pi:ℂ)*I*(p:ℂ)+(k:ℂ))*z))).differentiableOn.mul
    (lowerGaussian_entire b).differentiableOn).mul hd

theorem regularized_slice_integrable (b : ℝ) (hb : 0 < b) (k p C y : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) (hy : -Real.pi ≤ y) (hy0 : y ≤ 0) :
    Integrable (fun x : ℝ => regularized b k p F ((x:ℂ)+(y:ℂ)*I)) := by
  have hgauss := ((gaussian_slice_integrable b hb (k/(2*b)) 0).norm).const_mul
    (regularizationBound b k p C)
  apply hgauss.mono'
  · apply Continuous.aestronglyMeasurable
    exact (regularized_continuous b k p F hc).comp_continuous (by fun_prop)
      (fun x => by simpa [lowerClosedStrip] using And.intro hy hy0)
  · apply ae_of_all
    intro x
    simpa using regularized_strip_bound b hb k p C x y F hC hF hy hy0

theorem regularized_vertical_bound (b : ℝ) (hb : 0 < b) (k p C x : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    ‖∫ y : ℝ in (0:ℝ)..(-Real.pi), regularized b k p F ((x:ℂ)+(y:ℂ)*I)‖ ≤
      (regularizationBound b k p C*‖twistedGaussian b (k/(2*b)) (x:ℂ)‖)*Real.pi := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const (fun y hy =>
    regularized_strip_bound b hb k p C x y F hC hF
      ((Set.uIoc_of_ge (neg_nonpos.mpr Real.pi_pos.le) ▸ hy).1.le)
      ((Set.uIoc_of_ge (neg_nonpos.mpr Real.pi_pos.le) ▸ hy).2))
  simpa [abs_of_nonneg Real.pi_pos.le] using h

theorem regularized_vertical_limit (b : ℝ) (hb : 0 < b) (k p C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    Tendsto (verticalDifference (regularized b k p F) (-Real.pi)) atTop (𝓝 0) := by
  have hpos : Tendsto (fun T : ℝ => ∫ y : ℝ in (0:ℝ)..(-Real.pi),
      regularized b k p F ((T:ℂ)+(y:ℂ)*I)) atTop (𝓝 0) := by
    rw [tendsto_zero_iff_norm_tendsto_zero]
    apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds
      (by simpa using ((gaussian_norm_atTop b hb (k/(2*b))).const_mul
        (regularizationBound b k p C)).mul_const Real.pi)
      (Eventually.of_forall fun _ => norm_nonneg _)
    exact Eventually.of_forall (fun T => regularized_vertical_bound b hb k p C T F hC hF)
  have hneg : Tendsto (fun T : ℝ => ∫ y : ℝ in (0:ℝ)..(-Real.pi),
      regularized b k p F ((-T:ℝ)+(y:ℂ)*I)) atTop (𝓝 0) := by
    rw [tendsto_zero_iff_norm_tendsto_zero]
    apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds
      (by simpa using ((gaussian_norm_neg_atTop b hb (k/(2*b))).const_mul
        (regularizationBound b k p C)).mul_const Real.pi)
      (Eventually.of_forall fun _ => norm_nonneg _)
    exact Eventually.of_forall (fun T => by
      simpa only [ofReal_neg] using (regularized_vertical_bound b hb k p C (-T) F hC hF))
  have h := (hpos.const_mul I).sub (hneg.const_mul I)
  convert h using 1 <;> try { funext T; simp only [verticalDifference,ofReal_neg] }
  all_goals simp only [mul_zero,sub_zero]

theorem regularized_contour_shift (b : ℝ) (hb : 0 < b) (k p C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    (∫ x : ℝ, regularized b k p F ((x:ℂ)+(-Real.pi:ℝ)*I)) =
      ∫ x : ℝ,regularized b k p F (x:ℂ) := by
  apply lower_horizontal_integral_eq_of_vertical_limit _
    (regularized_continuous b k p F hc) (regularized_differentiable b k p F hd)
  · simpa using regularized_slice_integrable b hb k p C 0 F hC hc hF
      (neg_nonpos.mpr Real.pi_pos.le) le_rfl
  · exact regularized_slice_integrable b hb k p C (-Real.pi) F hC hc hF le_rfl
      (neg_nonpos.mpr Real.pi_pos.le)
  · exact regularized_vertical_limit b hb k p C F hC hF

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.regularized_slice_integrable
#print axioms F1Fecho.WedgeLaplace.regularized_vertical_limit
#print axioms F1Fecho.WedgeLaplace.regularized_contour_shift
