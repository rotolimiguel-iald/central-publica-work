import CompactBoostStrongDerivativeR2
import UnitaryFourierRealStressR2
import TGLExt.ContratoQG_v31
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Topology.Instances.Rat
import Mathlib.Topology.DenseEmbedding

/-! The existing strong H1 boost derivative and normalized real null moment.

All representatives, polarizations, measures and signs are the existing ones.
Countably many orbital equalities (rational boost parameters), followed by
continuity of both smooth orbits, identify the generator of the chosen
Schwartz representative. Thus no derivative identity is imposed as data.
The same L2 inner product is transported by the existing null Bochner theorem.
Unitarity removes its real part, giving the contract's derivative i*b.

This is a candidate for the one-particle axis-compact core. It does not extend
the result to finite coherent Fock sums or claim the full MaxwellCertificate.
-/
set_option autoImplicit false
set_option maxHeartbeats 2200000
set_option backward.isDefEq.respectTransparency false
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory SchwartzMap
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency
open scoped Topology ContDiff LineDeriv

def nullScreenCLM (y : MomentumCoordinates) (a : Fin 2) : Fib →L[ℂ] ℂ :=
  ∑ j : Fin 2, (nullPolarization y a j : ℂ) •
    PiLp.proj (𝕜 := ℂ) 2 (fun _ : Fin 2 => ℂ) j

theorem nullScreenCLM_apply (y : MomentumCoordinates) (a : Fin 2) (v : Fib) :
    nullScreenCLM y a v = ∑ j : Fin 2, (nullPolarization y a j : ℂ) * v j := by
  simp [nullScreenCLM, smul_eq_mul]

theorem nullScreenCLM_inner (y : MomentumCoordinates) (hy : y.1 ≠ 0) (v w : Fib) :
    inner ℂ v w = inner ℂ (nullScreenCLM y 0 v) (nullScreenCLM y 0 w) +
      inner ℂ (nullScreenCLM y 1 v) (nullScreenCLM y 1 w) := by
  have hr : (transverseRatio y 0 : ℂ)^2 + (transverseRatio y 1 : ℂ)^2 = 1 := by
    exact_mod_cast transverseRatio_sq_sum y hy
  simp [nullScreenCLM_apply, nullPolarization, Fin.sum_univ_two,
    PiLp.inner_apply, RCLike.inner_apply]
  linear_combination -((w 0) * starRingEnd ℂ (v 0) + (w 1) * starRingEnd ℂ (v 1)) * hr

theorem nullSchwartz_compact_orbit_ae (h : H1) (g : MomentumCoordinates → Fib)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g)
    (a : Fin 2) (D : NullSchwartzData h a) (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,
      nullScreenCLM y a (g (coordinateBoost 0 (-s) y)) =
        D.profile (nullFrequencyDilation s (nullFourierProfilePoint y)) := by
  have hc := (coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae he
  filter_upwards [hc, B0_profile_ae s h, nullSchwartz_B0_ae s h a D] with y hg hB hD
  calc
    _ = nullScreenCLM y a (B0 s h y) := by rw [hB, hg]
    _ = nullProfileAmplitude (B0 s h) a y := nullScreenCLM_apply y a _
    _ = _ := hD

/-- The null-profile derivative is obtained by uniqueness of actual derivatives.
The countable intersection is over rational parameters, before continuity is used. -/
theorem nullSchwartz_compact_generator_ae (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g)
    (a : Fin 2) (D : NullSchwartzData h a) :
    ∀ᵐ y ∂orbitalMeasure 0,
      nullScreenCLM y a (compactBoostGenerator g y) =
        shellNullFrequency y • (∂_{nullFrequencyDirection} D.profile) (nullFourierProfilePoint y) := by
  have hrat : ∀ᵐ y ∂orbitalMeasure 0, ∀ r : ℚ,
      nullScreenCLM y a (g (coordinateBoost 0 (-(r : ℝ)) y)) =
        D.profile (nullFrequencyDilation (r : ℝ) (nullFourierProfilePoint y)) :=
    ae_all_iff.mpr (fun r => nullSchwartz_compact_orbit_ae h g he a D (r : ℝ))
  filter_upwards [hrat] with y hy
  have hleft : Continuous (fun s : ℝ => nullScreenCLM y a (g (coordinateBoost 0 (-s) y))) :=
    (nullScreenCLM y a).continuous.comp (hg.continuous.comp
      (coordinateBoost_joint_continuous.comp (continuous_id.neg.prodMk continuous_const)))
  have hright : Continuous (fun s : ℝ => D.profile
      (nullFrequencyDilation s (nullFourierProfilePoint y))) := by
    apply D.profile.continuous.comp
    unfold nullFrequencyDilation
    fun_prop
  have horbit : (fun s : ℝ => nullScreenCLM y a (g (coordinateBoost 0 (-s) y))) =
      fun s : ℝ => D.profile (nullFrequencyDilation s (nullFourierProfilePoint y)) :=
    Rat.denseRange_cast.equalizer hleft hright (funext hy)
  have hder : HasDerivAt (fun s : ℝ => nullScreenCLM y a (g (coordinateBoost 0 (-s) y)))
      (nullScreenCLM y a (compactBoostGenerator g y)) 0 :=
    ((nullScreenCLM y a).restrictScalars ℝ).hasFDerivAt.comp_hasDerivAt 0
      (compactBoost_profile_hasDerivAt_zero g hg y)
  rw [horbit] at hder
  exact hder.unique (nullSchwartz_profile_generator h a D y)

theorem compactBoost_inner_profile_integrable (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    Integrable (fun y => inner ℂ (g y) (compactBoostGenerator g y)) (orbitalMeasure 0) := by
  apply (L2.integrable_inner (𝕜 := ℂ) h (compactBoostDerivative g hg hc)).congr
  filter_upwards [he, compactBoostDerivative_ae g hg hc] with y hh hd
  rw [hh, hd]

theorem compactBoost_inner_profile (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    inner ℂ h (compactBoostDerivative g hg hc) =
      ∫ y, inner ℂ (g y) (compactBoostGenerator g y) ∂orbitalMeasure 0 := by
  rw [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [he, compactBoostDerivative_ae g hg hc] with y hh hd
  rw [hh, hd]

theorem nullSchwartz_inner_lineDeriv_integrable (f : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun p => inner ℂ (f p) ((∂_{nullFrequencyDirection} f) p)) := by
  apply (L2.integrable_inner (𝕜 := ℂ) (f.toLp 2 volume)
    ((∂_{nullFrequencyDirection} f).toLp 2 volume)).congr
  filter_upwards [f.coeFn_toLp 2 volume, (∂_{nullFrequencyDirection} f).coeFn_toLp 2 volume] with p hp hd
  rw [hp, hd]

theorem nullFourier_integral_positive (F : NullFourierSpace → ℂ) (hF : Integrable F)
    (hz : ∀ p, p 0 ≤ 0 → F p = 0) :
    (∫ p, F p) = ∫ q : Transverse, ∫ u in Ioi 0, F (nullFourierCoordinates q u) := by
  rw [integral_nullFourierCoordinates F hF]
  apply integral_congr_ae
  filter_upwards [] with q
  have hi : (Ioi (0 : ℝ)).indicator (fun u => F (nullFourierCoordinates q u)) =
      fun u => F (nullFourierCoordinates q u) := by
    funext u
    by_cases hu : 0 < u
    · simp [hu]
    · simp only [indicator_of_notMem (show u ∉ Ioi (0 : ℝ) from hu)]
      exact (hz (nullFourierCoordinates q u) (le_of_not_gt hu)).symm
  conv_lhs => rw [← hi]
  rw [integral_indicator measurableSet_Ioi]

theorem compactBoost_inner_null_integrals (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g)
    (D0 : NullSchwartzData h 0) (D1 : NullSchwartzData h 1) :
    inner ℂ h (compactBoostDerivative g hg hc) =
      (∫ p, inner ℂ (D0.profile p) ((∂_{nullFrequencyDirection} D0.profile) p)) +
      (∫ p, inner ℂ (D1.profile p) ((∂_{nullFrequencyDirection} D1.profile) p)) := by
  let F : NullFourierSpace → ℂ := fun p =>
    inner ℂ (D0.profile p) ((∂_{nullFrequencyDirection} D0.profile) p) +
      inner ℂ (D1.profile p) ((∂_{nullFrequencyDirection} D1.profile) p)
  have hF : Integrable F := (nullSchwartz_inner_lineDeriv_integrable D0.profile).add
    (nullSchwartz_inner_lineDeriv_integrable D1.profile)
  have hz : ∀ p, p 0 ≤ 0 → F p = 0 := by
    intro p hp
    simp [F, D0.zero_nonpositive p hp, D1.zero_nonpositive p hp]
  have hpoint : (fun y => inner ℂ (g y) (compactBoostGenerator g y)) =ᵐ[orbitalMeasure 0]
      fun y => shellNullFrequency y • F (nullFourierProfilePoint y) := by
    filter_upwards [he, transverseProjection_ne_zero_ae, D0.orbital_ae, D1.orbital_ae,
      nullSchwartz_compact_generator_ae h g hg he 0 D0,
      nullSchwartz_compact_generator_ae h g hg he 1 D1] with y hy haxis h0 h1 hd0 hd1
    have hv (a : Fin 2) : nullScreenCLM y a (g y) = nullProfileAmplitude h a y := by
      rw [nullScreenCLM_apply, nullProfileAmplitude, hy]
    rw [nullScreenCLM_inner y haxis, hv 0, hv 1, hd0, hd1, h0, h1]
    simp only [inner_smul_right_eq_smul, ← smul_add, F]
  have hInt : Integrable (fun y => shellNullFrequency y • F (nullFourierProfilePoint y))
      (orbitalMeasure 0) := (compactBoost_inner_profile_integrable h g hg hc he).congr hpoint
  calc
    _ = ∫ y, shellNullFrequency y • F (nullFourierProfilePoint y) ∂orbitalMeasure 0 := by
      rw [compactBoost_inner_profile h g hg hc he]
      exact integral_congr_ae hpoint
    _ = ∫ q : Transverse, ∫ u in Ioi 0,
        F (nullFourierProfilePoint (nullMomentumCoordinates q u)) :=
      orbital_nullFrequency_bochner_cancel (fun y => F (nullFourierProfilePoint y)) hInt
    _ = ∫ q : Transverse, ∫ u in Ioi 0, F (nullFourierCoordinates q u) := by
      apply integral_congr_ae
      filter_upwards [] with q
      apply integral_congr_ae
      filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
      congr 1
      unfold nullFourierProfilePoint
      change nullFourierCoordinates q
        (energy (transverseMass 0 q) (inverseLongitudinal (transverseMass 0 q) u) -
          inverseLongitudinal (transverseMass 0 q) u) = _
      rw [null_inverseLongitudinal (transverseMass 0 q) u hu]
    _ = ∫ p, F p := (nullFourier_integral_positive F hF hz).symm
    _ = _ := integral_add (nullSchwartz_inner_lineDeriv_integrable D0.profile)
      (nullSchwartz_inner_lineDeriv_integrable D1.profile)

theorem compactBoost_expectation_hasDerivAt (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    HasDerivAt (fun s : ℝ => inner ℂ h (B0 s h))
      (inner ℂ h (compactBoostDerivative g hg hc)) 0 := by
  simpa only [inner_zero_left, add_zero] using
    (hasDerivAt_const (0 : ℝ) h).inner ℂ (compactBoost_hasDerivAt h g hg hc he)

theorem compactBoost_inner_re_zero (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    (inner ℂ h (compactBoostDerivative g hg hc)).re = 0 := by
  let d := compactBoostDerivative g hg hc
  have hd := compactBoost_hasDerivAt h g hg hc he
  have hn := hd.inner ℂ hd
  simp only [LinearIsometryEquiv.inner_map_map, B0_zero,
    LinearIsometryEquiv.coe_refl, id_eq] at hn
  have hz := hn.unique (hasDerivAt_const (0 : ℝ) (inner ℂ h h))
  have hr := congrArg (RCLike.re : ℂ → ℝ) hz
  simp only [map_add, map_zero] at hr
  change (inner ℂ h d).re = 0
  change (inner ℂ h d).re + (inner ℂ d h).re = 0 at hr
  have hs : (inner ℂ d h).re = (inner ℂ h d).re := inner_re_symm
  rw [hs] at hr
  linarith

theorem compactBoost_hasBoostEnergy (h : H1) (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    HasBoostEnergy B0 h (inner ℂ h (compactBoostDerivative g hg hc)).im := by
  have hz := compactBoost_inner_re_zero h g hg hc he
  have heq : inner ℂ h (compactBoostDerivative g hg hc) =
      Complex.I * ((inner ℂ h (compactBoostDerivative g hg hc)).im : ℂ) := by
    apply Complex.ext <;> simp [hz]
  unfold HasBoostEnergy
  rw [← heq]
  exact compactBoost_expectation_hasDerivAt h g hg hc he

theorem axisCompact_normalized_moment_eq_generator (h : H1) (hh : AxisCompactProfile h)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g) :
    (∫ x : NullFourierSpace, x 0 * unitaryFourierRealNullStress h x) =
      (inner ℂ h (compactBoostDerivative g hg hc)).im := by
  rw [axisCompact_unitaryFourierRealNullStress_moment h hh,
    compactBoost_inner_null_integrals h g hg hc he (axisCompactNullData h hh 0)
      (axisCompactNullData h hh 1)]
  simp [Complex.mul_re, Complex.add_im]

theorem axisCompact_hasBoostEnergy_normalized_moment (h : H1) (hh : AxisCompactProfile h) :
    HasBoostEnergy B0 h (∫ x : NullFourierSpace, x 0 * unitaryFourierRealNullStress h x) := by
  have hhcopy := hh
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hhcopy
  rw [axisCompact_normalized_moment_eq_generator h hh g hg hc he]
  exact compactBoost_hasBoostEnergy h g hg hc he

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullScreenCLM_inner
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_compact_generator_ae
#print axioms F1Fecho.MaxwellGlobal.compactBoost_inner_profile_integrable
#print axioms F1Fecho.MaxwellGlobal.compactBoost_inner_null_integrals
#print axioms F1Fecho.MaxwellGlobal.compactBoost_expectation_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.compactBoost_inner_re_zero
#print axioms F1Fecho.MaxwellGlobal.compactBoost_hasBoostEnergy
#print axioms F1Fecho.MaxwellGlobal.axisCompact_normalized_moment_eq_generator
#print axioms F1Fecho.MaxwellGlobal.axisCompact_hasBoostEnergy_normalized_moment
