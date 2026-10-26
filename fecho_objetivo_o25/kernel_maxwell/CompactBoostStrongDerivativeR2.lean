import CompactBoostStrongDerivativeReductionR3
import MaxwellBoostEnergyR2
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.MeasureTheory.Integral.IntegrableOn

/-! Strong differentiation of the existing boost on smooth compact profiles.

The majorant is a constant times the indicator of the compact boost orbit of
the support, for parameters in [-1,1]. Joint continuity bounds the parameter
derivative on a compact product; the mean value theorem bounds all nonzero
difference quotients. Outside the compact orbit, the existing almost-everywhere
inverse boost identity makes the quotient and the generator vanish.

The conclusion concerns the actual H1 and B0. It constructs the derivative
vector from the representative, with no derivative or majorant premise.
It does not assert a Maxwell charge identity or a complete certificate.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option backward.isDefEq.respectTransparency false
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped Topology ContDiff

theorem coordinateBoost_joint_continuous :
    Continuous (fun z : ℝ × MomentumCoordinates => coordinateBoost 0 z.1 z.2) := by
  change Continuous (fun z : ℝ × MomentumCoordinates =>
    (z.2.1, Real.cosh z.1 * z.2.2 + Real.sinh z.1 * shellEnergy z.2))
  exact continuous_snd.fst.prodMk
    (((Real.continuous_cosh.comp continuous_fst).mul continuous_snd.snd).add
      ((Real.continuous_sinh.comp continuous_fst).mul
        (shellEnergy_continuous.comp continuous_snd)))

def compactBoostVelocity (s : ℝ) (y : MomentumCoordinates) : MomentumCoordinates :=
  (0, (-Real.sinh (-s)) * y.2 + (-Real.cosh (-s)) * shellEnergy y)

def compactBoostOrbitDerivative (g : MomentumCoordinates → Fib)
    (z : ℝ × MomentumCoordinates) : Fib :=
  fderiv ℝ g (coordinateBoost 0 (-z.1) z.2) (compactBoostVelocity z.1 z.2)

theorem compactBoostVelocity_continuous :
    Continuous (fun z : ℝ × MomentumCoordinates => compactBoostVelocity z.1 z.2) := by
  exact continuous_const.prodMk
    ((((Real.continuous_sinh.comp continuous_fst.neg).neg).mul continuous_snd.snd).add
      (((Real.continuous_cosh.comp continuous_fst.neg).neg).mul
        (shellEnergy_continuous.comp continuous_snd)))

theorem compactBoostOrbitDerivative_continuous (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) : Continuous (compactBoostOrbitDerivative g) := by
  have hb : Continuous (fun z : ℝ × MomentumCoordinates =>
      coordinateBoost 0 (-z.1) z.2) :=
    coordinateBoost_joint_continuous.comp (continuous_fst.neg.prodMk continuous_snd)
  exact ((hg.continuous_fderiv (by simp)).comp hb).clm_apply compactBoostVelocity_continuous

theorem coordinateBoost_negative_hasDerivAt (s : ℝ) (y : MomentumCoordinates) :
    HasDerivAt (fun t : ℝ => coordinateBoost 0 (-t) y) (compactBoostVelocity s y) s := by
  have hcosh : HasDerivAt (fun t : ℝ => Real.cosh (-t)) (-Real.sinh (-s)) s := by
    simpa [Function.comp_def] using (Real.hasDerivAt_cosh (-s)).comp s (hasDerivAt_id s).neg
  have hsinh : HasDerivAt (fun t : ℝ => Real.sinh (-t)) (-Real.cosh (-s)) s := by
    simpa [Function.comp_def] using (Real.hasDerivAt_sinh (-s)).comp s (hasDerivAt_id s).neg
  convert! (hasDerivAt_const s y.1).prodMk
    ((hcosh.mul_const y.2).add (hsinh.mul_const (shellEnergy y))) using 1

theorem compactBoost_profile_hasDerivAt (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (s : ℝ) (y : MomentumCoordinates) :
    HasDerivAt (fun t : ℝ => g (coordinateBoost 0 (-t) y))
      (compactBoostOrbitDerivative g (s, y)) s := by
  exact ((hg.differentiable (by simp) (coordinateBoost 0 (-s) y)).hasFDerivAt).comp_hasDerivAt
    s (coordinateBoost_negative_hasDerivAt s y)

theorem compactBoostOrbitDerivative_zero (g : MomentumCoordinates → Fib)
    (y : MomentumCoordinates) :
    compactBoostOrbitDerivative g (0, y) = compactBoostGenerator g y := by
  have hv : compactBoostVelocity 0 y = (-shellEnergy y) • momentumLongitudinalDirection := by
    ext <;> simp [compactBoostVelocity, momentumLongitudinalDirection]
  simp [compactBoostOrbitDerivative, hv, coordinateBoost, compactBoostGenerator, map_smul]

def compactBoostOrbitSupport (g : MomentumCoordinates → Fib) : Set MomentumCoordinates :=
  (fun z : ℝ × MomentumCoordinates => coordinateBoost 0 z.1 z.2) ''
    (Icc (-1 : ℝ) 1 ×ˢ tsupport g)

theorem compactBoostOrbitSupport_compact (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) : IsCompact (compactBoostOrbitSupport g) :=
  (isCompact_Icc.prod hc).image coordinateBoost_joint_continuous

theorem tsupport_subset_compactBoostOrbitSupport (g : MomentumCoordinates → Fib) :
    tsupport g ⊆ compactBoostOrbitSupport g := by
  intro y hy
  refine ⟨(0, y), ⟨by norm_num, hy⟩, ?_⟩
  simp [coordinateBoost]

theorem compactBoostSlopeError_zero_off_orbit (g : MomentumCoordinates → Fib)
    (s : ℝ) (hs : s ∈ Icc (-1 : ℝ) 1) :
    ∀ᵐ y ∂orbitalMeasure 0, y ∉ compactBoostOrbitSupport g →
      compactBoostSlopeError g s y = 0 := by
  filter_upwards [coordinateBoost_inverse_ae s] with y hi
  intro hy
  have hn : y ∉ tsupport g := fun h => hy (tsupport_subset_compactBoostOrbitSupport g h)
  have hnb : coordinateBoost 0 (-s) y ∉ tsupport g := by
    intro hb
    apply hy
    refine ⟨(s, coordinateBoost 0 (-s) y), ⟨hs, hb⟩, ?_⟩
    simpa only [id_eq] using hi
  simp [compactBoostSlopeError, compactBoostGenerator,
    image_eq_zero_of_notMem_tsupport hn, image_eq_zero_of_notMem_tsupport hnb,
    fderiv_of_notMem_tsupport ℝ hn]

/-- A concrete integrable majorant exists for every smooth compact profile.
The almost-everywhere qualifier is exactly that of the existing inverse boost;
no extension of the rapidity chart over its exceptional axis is used. -/
theorem compactBoost_square_majorant_exists (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    ∃ bound : MomentumCoordinates → ℝ,
      Integrable bound (orbitalMeasure 0) ∧
      ∀ᶠ s in 𝓝[≠] (0 : ℝ), ∀ᵐ y ∂orbitalMeasure 0,
        ‖compactBoostSlopeError g s y‖ ^ 2 ≤ bound y := by
  classical
  let K := compactBoostOrbitSupport g
  have hK : IsCompact K := compactBoostOrbitSupport_compact g hc
  have hprod : IsCompact (Icc (-1 : ℝ) 1 ×ˢ K) := isCompact_Icc.prod hK
  obtain ⟨C, hC⟩ := hprod.exists_bound_of_continuousOn
    (compactBoostOrbitDerivative_continuous g hg).continuousOn
  have hC' (t : ℝ) (ht : t ∈ Icc (-1 : ℝ) 1) (y : MomentumCoordinates) (hy : y ∈ K) :
      ‖compactBoostOrbitDerivative g (t, y)‖ ≤ |C| :=
    (hC (t, y) ⟨ht, hy⟩).trans (le_abs_self C)
  let bound : MomentumCoordinates → ℝ := K.indicator (fun _ => (2 * |C|) ^ 2)
  refine ⟨bound, ?_, ?_⟩
  · apply (integrable_indicator_iff hK.measurableSet).mpr
    exact integrableOn_const hK.measure_lt_top.ne
  · have hsI : ∀ᶠ s in 𝓝[≠] (0 : ℝ), s ∈ Icc (-1 : ℝ) 1 :=
      mem_nhdsWithin_of_mem_nhds (Icc_mem_nhds (by norm_num) (by norm_num))
    have hsN : ∀ᶠ s in 𝓝[≠] (0 : ℝ), s ≠ 0 := by
      filter_upwards [self_mem_nhdsWithin] with s hs
      simpa only [mem_compl_iff, mem_singleton_iff] using hs
    filter_upwards [hsI, hsN] with s hs hs0
    filter_upwards [compactBoostSlopeError_zero_off_orbit g s hs] with y hz
    by_cases hy : y ∈ K
    · have h0 : (0 : ℝ) ∈ Icc (-1 : ℝ) 1 := by norm_num
      have hmv := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le
        (fun t (_ht : t ∈ Icc (-1 : ℝ) 1) =>
          (compactBoost_profile_hasDerivAt g hg t y).hasDerivWithinAt)
        (fun t ht => hC' t ht y hy) (convex_Icc (-1 : ℝ) 1) h0 hs
      have hdiff : ‖g (coordinateBoost 0 (-s) y) - g y‖ ≤ |C| * ‖s‖ := by
        simpa [coordinateBoost] using hmv
      have hquot : ‖s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y)‖ ≤ |C| := by
        calc
          _ = ‖s‖⁻¹ * ‖g (coordinateBoost 0 (-s) y) - g y‖ := by rw [norm_smul, norm_inv]
          _ ≤ ‖s‖⁻¹ * (|C| * ‖s‖) := mul_le_mul_of_nonneg_left hdiff (by positivity)
          _ = |C| := by
            rw [mul_left_comm, inv_mul_cancel₀ (norm_ne_zero_iff.mpr hs0), mul_one]
      have hd : ‖compactBoostGenerator g y‖ ≤ |C| := by
        simpa only [compactBoostOrbitDerivative_zero] using hC' 0 h0 y hy
      have herr : ‖compactBoostSlopeError g s y‖ ≤ 2 * |C| := by
        change ‖s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y) -
          compactBoostGenerator g y‖ ≤ 2 * |C|
        exact (norm_sub_le _ _).trans (by linarith)
      have hsq := pow_le_pow_left₀ (norm_nonneg (compactBoostSlopeError g s y)) herr 2
      simpa only [bound, Set.indicator_of_mem hy] using hsq
    · have hzero := hz hy
      simp only [hzero, norm_zero, zero_pow (by norm_num : (2 : ℕ) ≠ 0),
        bound, Set.indicator_of_notMem hy, le_refl]

theorem compactBoost_hasDerivAt (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    HasDerivAt (fun s : ℝ => B0 s h) (compactBoostDerivative g hg hc) 0 := by
  obtain ⟨bound, hInt, hbound⟩ := compactBoost_square_majorant_exists g hg hc
  exact compactBoost_hasDerivAt_of_square_majorant h g hg hc he bound hInt hbound

theorem axisCompact_boost_strong_derivative (h : H1) (hh : AxisCompactProfile h) :
    ∃ (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g),
      (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g ∧
      HasDerivAt (fun s : ℝ => B0 s h) (compactBoostDerivative g hg hc) 0 := by
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hh
  exact ⟨g, hg, hc, he, compactBoost_hasDerivAt h g hg hc he⟩

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.coordinateBoost_joint_continuous
#print axioms F1Fecho.MaxwellGlobal.compactBoostOrbitDerivative_continuous
#print axioms F1Fecho.MaxwellGlobal.compactBoost_profile_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.compactBoostOrbitSupport_compact
#print axioms F1Fecho.MaxwellGlobal.compactBoostSlopeError_zero_off_orbit
#print axioms F1Fecho.MaxwellGlobal.compactBoost_square_majorant_exists
#print axioms F1Fecho.MaxwellGlobal.compactBoost_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.axisCompact_boost_strong_derivative
