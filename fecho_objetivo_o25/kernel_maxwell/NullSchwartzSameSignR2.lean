import MaxwellNullSchwartzConsumerR2

/-! Same-sign first moments for positive-null-frequency Schwartz profiles.

The existing bilinear Fourier identity avoids introducing a conjugate-reflected
Schwartz map. Fourier squared is reflection, and the derivative of a profile
vanishing on the nonpositive half-space is zero on the negative open half-space.
Thus the reflected frequency product vanishes pointwise. Angular dilation and
the mixed weighted Parseval formula are reused with their exact constants.

Integrability is proved separately. The real-part conclusion is a Schwartz
wave identity; it is not a Maxwell charge link, a strong H1 derivative,
HasBoostEnergy, or a full certificate. This is an uncompiled candidate.
R2 repairs only elaboration and rewrites; all public statements are unchanged.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option backward.isDefEq.respectTransparency false
noncomputable section

namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Set SchwartzMap FourierTransform Module
open F1Fecho.WeightedPlancherel
open scoped FourierTransform LineDeriv Topology ComplexConjugate

theorem nullSchwartz_fourier_twice (f : 𝓢(NullFourierSpace, ℂ))
    (p : NullFourierSpace) : (𝓕 (𝓕 f)) p = f (-p) := by
  have hi := congrArg (fun k : 𝓢(NullFourierSpace, ℂ) => k (-p))
    (FourierTransform.fourierInv_fourier_eq (F := 𝓢(NullFourierSpace, ℂ)) f)
  change (𝓕 (𝓕 f)) (-(-p)) = f (-p) at hi
  simpa only [neg_neg] using hi

theorem nullSchwartz_lineDeriv_zero_negative (g : 𝓢(NullFourierSpace, ℂ))
    (hg : ∀ p, p 0 ≤ 0 → g p = 0) (p m : NullFourierSpace) (hp : p 0 < 0) :
    (∂_{m} g) p = 0 := by
  have hc : Continuous (fun y : NullFourierSpace => y 0) := by fun_prop
  have hn : ∀ᶠ y in 𝓝 p, y 0 < 0 := hc.continuousAt.eventually (gt_mem_nhds hp)
  have he : (g : NullFourierSpace → ℂ) =ᶠ[𝓝 p] fun _ => 0 :=
    hn.mono (fun y hy => hg y hy.le)
  rw [SchwartzMap.lineDerivOp_apply_eq_fderiv, he.fderiv_eq]
  simp

theorem nullFourier_weighted_product_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => (x 0 : ℂ) * (𝓕 f x) * (𝓕 g x)) := by
  have ht : (fun x : NullFourierSpace => inner ℝ x nullFrequencyDirection).HasTemperateGrowth :=
    by fun_prop
  let fg : 𝓢(NullFourierSpace, ℂ) :=
    SchwartzMap.pairing (ContinuousLinearMap.mul ℂ ℂ) (𝓕 f) (𝓕 g)
  have hi : Integrable (fun x : NullFourierSpace =>
      SchwartzMap.smulLeftCLM ℂ (fun y => inner ℝ y nullFrequencyDirection) fg x) :=
    (SchwartzMap.smulLeftCLM ℂ (fun y => inner ℝ y nullFrequencyDirection) fg).integrable
  apply hi.congr
  filter_upwards [] with x
  rw [SchwartzMap.smulLeftCLM_apply_apply ht]
  change (inner ℝ x nullFrequencyDirection) • ((𝓕 f x) * (𝓕 g x)) = _
  rw [nullFrequencyDirection_inner, ← Complex.coe_smul, smul_eq_mul]
  ring

theorem nullFourier_weighted_same_sign_zero (f g : 𝓢(NullFourierSpace, ℂ))
    (hf : ∀ p, p 0 ≤ 0 → f p = 0) (hg : ∀ p, p 0 ≤ 0 → g p = 0) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) * (𝓕 f x) * (𝓕 g x)) = 0 := by
  have hp : (∫ x : NullFourierSpace,
      (𝓕 f x) * (𝓕 (∂_{nullFrequencyDirection} g) x)) = 0 := by
    rw [SchwartzMap.integral_fourier_mul_eq]
    apply integral_eq_zero_of_ae
    filter_upwards [] with p
    change f p * (𝓕 (𝓕 (∂_{nullFrequencyDirection} g)) p) = (0 : ℂ)
    rw [nullSchwartz_fourier_twice]
    by_cases hpos : p 0 ≤ 0
    · rw [hf p hpos, zero_mul]
    · have hn : (-p) 0 < 0 := by
        change -(p 0) < 0
        exact neg_lt_zero.mpr (lt_of_not_ge hpos)
      rw [nullSchwartz_lineDeriv_zero_negative g hg (-p) nullFrequencyDirection hn,
        mul_zero]
  have ht : (fun x : NullFourierSpace => inner ℝ x nullFrequencyDirection).HasTemperateGrowth :=
    by fun_prop
  have he : (∫ x : NullFourierSpace,
      (𝓕 f x) * (𝓕 (∂_{nullFrequencyDirection} g) x)) =
      (2 * Real.pi * Complex.I) *
        ∫ x : NullFourierSpace, (x 0 : ℂ) * (𝓕 f x) * (𝓕 g x) := by
    rw [SchwartzMap.fourier_lineDerivOp_eq]
    simp only [SchwartzMap.smul_apply, SchwartzMap.smulLeftCLM_apply_apply ht]
    simp only [nullFrequencyDirection_inner, ← Complex.coe_smul, smul_eq_mul]
    rw [← integral_const_mul]
    apply integral_congr_ae
    filter_upwards [] with x
    ring
  have hc : (2 * Real.pi * Complex.I : ℂ) ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (by norm_num)
      (by exact_mod_cast Real.pi_ne_zero)) Complex.I_ne_zero
  exact (mul_eq_zero.mp (he.symm.trans hp)).resolve_left hc

theorem nullAngular_weighted_same_sign_zero (f g : 𝓢(NullFourierSpace, ℂ))
    (hf : ∀ p, p 0 ≤ 0 → f p = 0) (hg : ∀ p, p 0 ≤ 0 → g p = 0) :
    (∫ x : NullFourierSpace,
      (x 0 : ℂ) * angularForward f x * angularForward g x) = 0 := by
  have hd := linear_weight_dilation (fun x : NullFourierSpace => (𝓕 f x) * (𝓕 g x))
    nullFrequencyDirection (2 * Real.pi) (by positivity)
  have hz : (∫ x : NullFourierSpace,
      (inner ℝ x nullFrequencyDirection : ℂ) * ((𝓕 f x) * (𝓕 g x))) = 0 := by
    simpa only [nullFrequencyDirection_inner, mul_assoc] using
      nullFourier_weighted_same_sign_zero f g hf hg
  rw [hz, smul_zero] at hd
  simpa only [angularForward, nullFrequencyDirection_inner, mul_assoc] using hd

theorem nullAngular_weighted_product_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace =>
      (x 0 : ℂ) * angularForward f x * angularForward g x) := by
  have hc : (2 * Real.pi : ℝ) ≠ 0 := by positivity
  have hi := ((nullFourier_weighted_product_integrable f g).comp_smul
    (inv_ne_zero hc)).const_mul (2 * Real.pi : ℂ)
  apply hi.congr
  filter_upwards [] with x
  simp only [angularForward, PiLp.smul_apply, smul_eq_mul]
  push_cast
  field_simp [Real.pi_ne_zero] <;> ring

theorem nullAngular_weighted_mixed_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace =>
      (x 0 : ℂ) * inner ℂ (angularForward f x) (angularForward g x)) := by
  apply (nullAngular_weighted_product_integrable f g).norm.mono'
  · have hc : Continuous (fun x : NullFourierSpace =>
        (x 0 : ℂ) * inner ℂ (angularForward f x) (angularForward g x)) := by
      unfold angularForward
      fun_prop
    exact hc.aestronglyMeasurable
  · filter_upwards [] with x
    simp [RCLike.inner_apply', norm_mul, mul_assoc, mul_comm, mul_left_comm]

private theorem nullReal_product_pointwise (w : ℝ) (a b : ℂ) :
    2 * (w * a.re * b.re) =
      ((w : ℂ) * a * b).re + ((w : ℂ) * inner ℂ a b).re := by
  simp only [RCLike.inner_apply', Complex.mul_re, Complex.mul_im,
    Complex.ofReal_re, Complex.ofReal_im, Complex.conj_re, Complex.conj_im]
  ring

theorem nullAngular_real_product_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace =>
      x 0 * (angularForward f x).re * (angularForward g x).re) := by
  have hi := ((nullAngular_weighted_product_integrable f g).re.add
    (nullAngular_weighted_mixed_integrable f g).re).const_mul (1 / 2 : ℝ)
  apply hi.congr
  filter_upwards [] with x
  change (1 / 2 : ℝ) *
    (((x 0 : ℂ) * angularForward f x * angularForward g x).re +
      ((x 0 : ℂ) * inner ℂ (angularForward f x) (angularForward g x)).re) = _
  rw [← nullReal_product_pointwise]
  ring

theorem nullAngular_real_product_eq_mixed (f g : 𝓢(NullFourierSpace, ℂ))
    (hf : ∀ p, p 0 ≤ 0 → f p = 0) (hg : ∀ p, p 0 ≤ 0 → g p = 0) :
    2 * (∫ x : NullFourierSpace,
      x 0 * (angularForward f x).re * (angularForward g x).re) =
      (∫ x : NullFourierSpace,
        (x 0 : ℂ) * inner ℂ (angularForward f x) (angularForward g x)).re := by
  rw [← integral_const_mul]
  simp_rw [nullReal_product_pointwise]
  have hs := (nullAngular_weighted_product_integrable f g).re
  have hm := (nullAngular_weighted_mixed_integrable f g).re
  simp only [RCLike.re_eq_complex_re] at hs hm
  rw [integral_add hs hm]
  have hsr := integral_re (nullAngular_weighted_product_integrable f g)
  have hmr := integral_re (nullAngular_weighted_mixed_integrable f g)
  simp only [RCLike.re_eq_complex_re] at hsr hmr
  rw [hsr, hmr, nullAngular_weighted_same_sign_zero f g hf hg]
  simp

theorem nullAngular_real_product_weighted_parseval (f g : 𝓢(NullFourierSpace, ℂ))
    (hf : ∀ p, p 0 ≤ 0 → f p = 0) (hg : ∀ p, p 0 ≤ 0 → g p = 0) :
    2 * (∫ x : NullFourierSpace,
      x 0 * (angularForward f x).re * (angularForward g x).re) =
      ((-Complex.I * (2 * Real.pi : ℝ)^3) *
        ∫ p, inner ℂ (f p) ((∂_{nullFrequencyDirection} g) p)).re := by
  rw [nullAngular_real_product_eq_mixed f g hf hg]
  congr 1
  simpa only [nullFrequencyDirection_inner, finrank_euclideanSpace_fin] using
    angular_weighted_parseval f g nullFrequencyDirection

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_fourier_twice
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_lineDeriv_zero_negative
#print axioms F1Fecho.MaxwellGlobal.nullFourier_weighted_product_integrable
#print axioms F1Fecho.MaxwellGlobal.nullFourier_weighted_same_sign_zero
#print axioms F1Fecho.MaxwellGlobal.nullAngular_weighted_same_sign_zero
#print axioms F1Fecho.MaxwellGlobal.nullAngular_weighted_product_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_weighted_mixed_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_real_product_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_real_product_eq_mixed
#print axioms F1Fecho.MaxwellGlobal.nullAngular_real_product_weighted_parseval
