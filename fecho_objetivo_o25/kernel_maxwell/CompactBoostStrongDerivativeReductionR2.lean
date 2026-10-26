import AxisCompactProfileDensityR4
import MaxwellMomentTransportR3
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! A concrete H1 boost generator and the remaining strong-derivative reduction.

The generator is built from a smooth compact representative on the existing
momentum coordinates. Its continuity and compact support imply MemLp 2 for
the existing, locally finite orbital measure. No rapidity chart is extended
across its exceptional axis: the parameter derivative is taken at fixed
momentum and the shell energy is only used as a continuous coefficient.

The last theorem proves a strong H1 derivative from an explicit integrable
majorant for the squared slope error. It does NOT assume HasDerivAt in H1.
The majorant has not yet been constructed for every compact profile here.
Thus this component discharges the generator/L2-lifting obligations, not the
whole strong-derivative claim for AxisCompactProfile, and not a charge link.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option backward.isDefEq.respectTransparency false
noncomputable section

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open scoped Topology ContDiff

def momentumLongitudinalDirection : MomentumCoordinates := (0, 1)

def compactBoostGenerator (g : MomentumCoordinates → Fib) (y : MomentumCoordinates) : Fib :=
  (-shellEnergy y) • (fderiv ℝ g y momentumLongitudinalDirection)

theorem compactBoostGenerator_continuous (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) : Continuous (compactBoostGenerator g) := by
  exact shellEnergy_continuous.neg.smul
    ((hg.continuous_fderiv (by simp)).clm_apply continuous_const)

theorem compactBoostGenerator_compact (g : MomentumCoordinates → Fib)
    (hc : HasCompactSupport g) : HasCompactSupport (compactBoostGenerator g) := by
  simpa only [compactBoostGenerator, Pi.smul_apply] using
    (hc.fderiv_apply ℝ momentumLongitudinalDirection).smul_left
      (f := fun y : MomentumCoordinates => -shellEnergy y)

theorem compactBoostGenerator_memLp (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    MemLp (compactBoostGenerator g) 2 (orbitalMeasure 0) :=
  (compactBoostGenerator_continuous g hg).memLp_of_hasCompactSupport
    (compactBoostGenerator_compact g hc)

theorem compactBoostGenerator_square_integrable (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    Integrable (fun y => ‖compactBoostGenerator g y‖ ^ 2) (orbitalMeasure 0) :=
  (memLp_two_iff_integrable_sq_norm
    (compactBoostGenerator_continuous g hg).aestronglyMeasurable).mp
      (compactBoostGenerator_memLp g hg hc)

def compactBoostDerivative (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) : H1 :=
  (compactBoostGenerator_memLp g hg hc).toLp (compactBoostGenerator g)

theorem compactBoostDerivative_ae (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) :
    (compactBoostDerivative g hg hc : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0]
      compactBoostGenerator g :=
  (compactBoostGenerator_memLp g hg hc).coeFn_toLp

theorem coordinateBoost_negative_hasDerivAt_zero (y : MomentumCoordinates) :
    HasDerivAt (fun s : ℝ => coordinateBoost 0 (-s) y)
      ((-shellEnergy y) • momentumLongitudinalDirection) 0 := by
  have hcosh : HasDerivAt (fun s : ℝ => Real.cosh (-s)) 0 0 := by
    simpa using (Real.hasDerivAt_cosh (-(0 : ℝ))).comp 0 (hasDerivAt_id (0 : ℝ)).neg
  have hsinh : HasDerivAt (fun s : ℝ => Real.sinh (-s)) (-1) 0 := by
    simpa using (Real.hasDerivAt_sinh (-(0 : ℝ))).comp 0 (hasDerivAt_id (0 : ℝ)).neg
  have hl := (hcosh.mul_const y.2).add (hsinh.mul_const (shellEnergy y))
  convert! (hasDerivAt_const (0 : ℝ) y.1).prodMk hl using 1 <;>
    simp [coordinateBoost, shellEnergy, momentumLongitudinalDirection]

theorem compactBoost_profile_hasDerivAt_zero (g : MomentumCoordinates → Fib)
    (hg : ContDiff ℝ ∞ g) (y : MomentumCoordinates) :
    HasDerivAt (fun s : ℝ => g (coordinateBoost 0 (-s) y))
      (compactBoostGenerator g y) 0 := by
  have hd : HasFDerivAt g (fderiv ℝ g y) y :=
    (hg.differentiable (by simp) y).hasFDerivAt
  have hz : y = coordinateBoost 0 (-0) y := by simp [coordinateBoost]
  simpa only [Function.comp_def, map_smul, compactBoostGenerator] using
    hd.comp_hasDerivAt_of_eq 0 (coordinateBoost_negative_hasDerivAt_zero y) hz

theorem axisCompact_boost_generator_exists (h : H1) (hh : AxisCompactProfile h) :
    ∃ (g : MomentumCoordinates → Fib) (d : H1),
      (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g ∧
      ContDiff ℝ ∞ g ∧ HasCompactSupport g ∧
      (d : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] compactBoostGenerator g := by
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hh
  exact ⟨g, compactBoostDerivative g hg hc, he, hg, hc, compactBoostDerivative_ae g hg hc⟩

/-- Dominated convergence of actual representatives implies convergence in H1.
The square majorant is integrable; it is not a bound for a merely formal integral. -/
theorem orbitalL2_tendsto_of_square_majorant {ι : Type*} {l : Filter ι}
    [l.IsCountablyGenerated] (F : ι → H1) (D : H1)
    (r : ι → MomentumCoordinates → Fib) (d : MomentumCoordinates → Fib)
    (hr : ∀ i, (F i : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] r i)
    (hd : (D : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] d)
    (bound : MomentumCoordinates → ℝ)
    (hbound : ∀ᶠ i in l, ∀ᵐ y ∂orbitalMeasure 0, ‖r i y - d y‖ ^ 2 ≤ bound y)
    (hboundInt : Integrable bound (orbitalMeasure 0))
    (hlim : ∀ᵐ y ∂orbitalMeasure 0, Tendsto (fun i => r i y) l (𝓝 (d y))) :
    Tendsto F l (𝓝 D) := by
  have hI : Tendsto (fun i => ∫ y, ‖r i y - d y‖ ^ 2 ∂orbitalMeasure 0)
      l (𝓝 (∫ _y : MomentumCoordinates, (0 : ℝ) ∂orbitalMeasure 0)) := by
    apply tendsto_integral_filter_of_dominated_convergence bound
    · exact Eventually.of_forall (fun i =>
        (((Lp.aestronglyMeasurable (F i)).congr (hr i)).sub
          ((Lp.aestronglyMeasurable D).congr hd)).norm.pow 2)
    · filter_upwards [hbound] with i hi
      filter_upwards [hi] with y hy
      rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg (‖r i y - d y‖))]
      exact hy
    · exact hboundInt
    · filter_upwards [hlim] with y hy
      have ht := (hy.sub (tendsto_const_nhds (x := d y))).norm.pow 2
      simpa only [sub_self, norm_zero, zero_pow (by norm_num : (2 : ℕ) ≠ 0)] using ht
  have he (i : ι) : ‖F i - D‖ ^ 2 =
      ∫ y, ‖r i y - d y‖ ^ 2 ∂orbitalMeasure 0 := by
    have hnorm (u : H1) : (∫ y, ‖u y‖ ^ 2 ∂orbitalMeasure 0) = ‖u‖ ^ 2 := by
      have h := congrArg (RCLike.re : ℂ → ℝ) (L2.inner_def (𝕜 := ℂ) u u)
      rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) u u)] at h
      simpa only [inner_self_eq_norm_sq] using h.symm
    rw [← hnorm (F i - D)]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (F i) D, hr i, hd] with y hs hi hD
    simp only [Pi.sub_apply] at hs
    rw [hs, hi, hD]
  have hs : Tendsto (fun i => ‖F i - D‖ ^ 2) l (𝓝 (0 : ℝ)) := by
    simpa only [he, integral_zero] using hI
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp hs
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def, Real.sqrt_sq_eq_abs, abs_norm,
    Real.sqrt_zero, dist_eq_norm] using hn

def compactBoostSlopeError (g : MomentumCoordinates → Fib) (s : ℝ)
    (y : MomentumCoordinates) : Fib :=
  s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y) - compactBoostGenerator g y

/-- Precise remaining analytic obligation: construct this integrable majorant
from compactness/smoothness. The theorem then gives the actual strong H1
derivative of B0, not a derivative of a separately chosen pointwise orbit. -/
theorem compactBoost_hasDerivAt_of_square_majorant (h : H1)
    (g : MomentumCoordinates → Fib) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (he : (h : MomentumCoordinates → Fib) =ᵐ[orbitalMeasure 0] g)
    (bound : MomentumCoordinates → ℝ) (hboundInt : Integrable bound (orbitalMeasure 0))
    (hbound : ∀ᶠ s in 𝓝[≠] (0 : ℝ), ∀ᵐ y ∂orbitalMeasure 0,
      ‖compactBoostSlopeError g s y‖ ^ 2 ≤ bound y) :
    HasDerivAt (fun s : ℝ => B0 s h) (compactBoostDerivative g hg hc) 0 := by
  have hr (s : ℝ) : (s⁻¹ • (B0 s h - h) : H1) =ᵐ[orbitalMeasure 0]
      fun y => s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y) := by
    have ht := (coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae he
    filter_upwards [Lp.coeFn_smul s⁻¹ (B0 s h - h), Lp.coeFn_sub (B0 s h) h,
      B0_profile_ae s h, ht, he] with y hsm hsub hB hcomp hh
    simp only [Pi.smul_apply, Pi.sub_apply] at hsm hsub
    rw [hsm, hsub, hB, hcomp, hh]
  have hlim : ∀ᵐ y ∂orbitalMeasure 0,
      Tendsto (fun s : ℝ => s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y))
        (𝓝[≠] 0) (𝓝 (compactBoostGenerator g y)) := by
    apply ae_of_all
    intro y
    have hz : coordinateBoost 0 (-0) y = y := by simp [coordinateBoost]
    simpa only [zero_add, hz] using (compactBoost_profile_hasDerivAt_zero g hg y).tendsto_slope_zero
  have ht := orbitalL2_tendsto_of_square_majorant
    (fun s : ℝ => s⁻¹ • (B0 s h - h)) (compactBoostDerivative g hg hc)
    (fun s y => s⁻¹ • (g (coordinateBoost 0 (-s) y) - g y))
    (compactBoostGenerator g) hr (compactBoostDerivative_ae g hg hc)
    bound hbound hboundInt hlim
  apply hasDerivAt_iff_tendsto_slope_zero.mpr
  simpa only [zero_add, B0_zero, LinearIsometryEquiv.coe_refl, id_eq] using ht

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.compactBoostGenerator_continuous
#print axioms F1Fecho.MaxwellGlobal.compactBoostGenerator_compact
#print axioms F1Fecho.MaxwellGlobal.compactBoostGenerator_memLp
#print axioms F1Fecho.MaxwellGlobal.compactBoostGenerator_square_integrable
#print axioms F1Fecho.MaxwellGlobal.compactBoostDerivative_ae
#print axioms F1Fecho.MaxwellGlobal.coordinateBoost_negative_hasDerivAt_zero
#print axioms F1Fecho.MaxwellGlobal.compactBoost_profile_hasDerivAt_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompact_boost_generator_exists
#print axioms F1Fecho.MaxwellGlobal.orbitalL2_tendsto_of_square_majorant
#print axioms F1Fecho.MaxwellGlobal.compactBoost_hasDerivAt_of_square_majorant
