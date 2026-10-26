import SchwartzMaxwellLinearR3

/-! Quantitative control by finitely many Schwartz seminorms and continuity
of the actual mass-shell restriction into the original H1. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.SchwartzRestriction
open scoped ENNReal Topology

local instance : momentumMeasure.IsAddHaarMeasure := by unfold momentumMeasure; infer_instance

def restrictionMajorant (f : SchwartzTensor) : ℝ :=
  128 * (2 ^ momentumMeasure.integrablePower *
    (∫ y : MomentumCoordinates,(1+‖y‖)^(-(momentumMeasure.integrablePower:ℝ)) ∂momentumMeasure) *
    (2*SchwartzMap.seminorm ℝ 1 0 f*SchwartzMap.seminorm ℝ 0 0 f+
      2*SchwartzMap.seminorm ℝ (momentumMeasure.integrablePower+1) 0 f*SchwartzMap.seminorm ℝ 0 0 f))

theorem restrictionMajorant_continuous : Continuous restrictionMajorant := by
  have hc (n : ℕ) : Continuous (SchwartzMap.seminorm ℝ n 0 : SchwartzTensor→ℝ) :=
    (schwartz_withSeminorms ℝ Spacetime TensorValue).continuous_seminorm (n,0)
  exact continuous_const.mul (continuous_const.mul ((continuous_const.mul (hc 1)).mul (hc 0) |>.add
    ((continuous_const.mul (hc (momentumMeasure.integrablePower+1))).mul (hc 0))))

theorem restrictionMajorant_zero : restrictionMajorant 0=0 := by simp [restrictionMajorant]

theorem shell_weighted_square_integral_bound (f : SchwartzTensor) :
    128*(∫ y,shellEnergy y*‖f (shellEmbedding y)‖^2 ∂momentumMeasure) ≤ restrictionMajorant f := by
  have hn (y : MomentumCoordinates) : ‖shellEnergy y*‖f (shellEmbedding y)‖^2‖=
      shellEnergy y*‖f (shellEmbedding y)‖^2 :=
    Real.norm_of_nonneg (mul_nonneg (shellEnergy_nonneg y) (sq_nonneg _))
  have hi := integral_pow_mul_le_of_le_of_pow_mul_le (μ:=momentumMeasure) (k:=0)
    (f:=fun y=>shellEnergy y*‖f (shellEmbedding y)‖^2)
    (fun y => by
      simpa [hn y] using (weighted_restriction_decay f shellEmbedding shellEnergy
        (by norm_num : (0:ℝ)≤2) shellEmbedding_proper_bound energy_le_twice_coordinate_norm 0 y))
    (fun y => by
      simpa [hn y] using (weighted_restriction_decay f shellEmbedding shellEnergy
        (by norm_num : (0:ℝ)≤2) shellEmbedding_proper_bound energy_le_twice_coordinate_norm
        momentumMeasure.integrablePower y))
  exact mul_le_mul_of_nonneg_left (by simpa only [pow_zero,one_mul,hn] using hi) (by norm_num)

theorem h1_norm_sq_integral (x : H1) : ‖x‖^2=∫ y,‖x y‖^2 ∂orbitalMeasure 0 := by
  calc
    ‖x‖^2=(inner ℂ x x).re := by simp only [inner_self_eq_norm_sq_to_K,← Complex.ofReal_pow,Complex.ofReal_re]
    _ = (∫ y,inner ℂ (x y) (x y) ∂orbitalMeasure 0).re := by rw [L2.inner_def]
    _ = ∫ y,(inner ℂ (x y) (x y)).re ∂orbitalMeasure 0 :=
      (integral_re (L2.integrable_inner (𝕜:=ℂ) x x)).symm
    _ = ∫ y,‖x y‖^2 ∂orbitalMeasure 0 := by simp only [inner_self_eq_norm_sq_to_K,← Complex.ofReal_pow,Complex.ofReal_re]

theorem momentumSmear_sq_bound (f : SchwartzTensor) :
    ‖momentumSmear f‖^2 ≤ restrictionMajorant f := by
  have hn : ‖momentumSmear f‖^2=∫ y,‖globalCoefficient f y‖^2 ∂orbitalMeasure 0 := by
    rw [h1_norm_sq_integral]
    apply integral_congr_ae
    filter_upwards [(globalCoefficient_memLp f).coeFn_toLp] with y hy
    change ‖((globalCoefficient_memLp f).toLp (globalCoefficient f)) y‖^2=_
    rw [hy]
  rw [hn]
  change (∫ y,‖globalCoefficient f y‖^2 ∂momentumMeasure.withDensity (orbitalWeight 0))≤_
  rw [integral_withDensity_eq_integral_toReal_smul (orbitalWeight_measurable 0)
    (Filter.Eventually.of_forall (fun y=>ENNReal.ofReal_lt_top))]
  apply le_trans _ (shell_weighted_square_integral_bound f)
  rw [← integral_const_mul]
  apply integral_mono_of_nonneg
  · filter_upwards with y using smul_nonneg ENNReal.toReal_nonneg (sq_nonneg _)
  · exact (shell_weighted_square_integrable f).const_mul 128
  · filter_upwards with y
    exact (le_abs_self _).trans (by simpa only [Real.norm_eq_abs] using density_normsq_bound f y)

theorem momentumSmear_continuous : Continuous momentumSmear := by
  apply continuous_of_tendsto_nhds_zero momentumSmearLinear
  apply tendsto_zero_iff_norm_tendsto_zero.mpr
  have ht : Tendsto (fun f=>Real.sqrt (restrictionMajorant f)) (𝓝 (0:SchwartzTensor)) (𝓝 0) := by
    simpa only [Function.comp_apply,restrictionMajorant_zero,Real.sqrt_zero] using
      (Real.continuous_sqrt.comp restrictionMajorant_continuous).continuousAt.tendsto (x:=0)
  exact squeeze_zero (fun f=>norm_nonneg _) (fun f=>Real.le_sqrt_of_sq_le (momentumSmear_sq_bound f)) ht

def momentumSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  ⟨momentumSmearLinear,momentumSmear_continuous⟩

def spacetimeSmearCLM : SchwartzTensor →L[ℂ] H1 :=
  momentumSmearCLM.comp ((SchwartzMap.compCLMOfContinuousLinearEquiv ℂ
    metricFlip.toContinuousLinearEquiv).comp (SchwartzMap.fourierTransformCLM ℂ))

theorem spacetimeSmearCLM_apply (f : SchwartzTensor) : spacetimeSmearCLM f=spacetimeSmear f := rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_sq_bound
#print axioms F1Fecho.MaxwellGlobal.momentumSmear_continuous
#print axioms F1Fecho.MaxwellGlobal.spacetimeSmearCLM_apply
