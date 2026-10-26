import TGLExt.V350DualFormTransport
import TGLExt.V350DualFormFaithfulness
import Mathlib.Topology.UniformSpace.Dini

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory Filter Set
open scoped ENNReal Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Uniform convergence on a compact interval controls its integral for any filter. -/
theorem intervalIntegral_tendsto_of_uniform {ι : Type*} {l : Filter ι}
    (F : ι → ℝ → ℝ) (f : ℝ → ℝ) (a b : ℝ)
    (hF : ∀ i, Continuous (F i)) (hf : Continuous f)
    (hu : TendstoUniformlyOn F f l (Set.uIcc a b)) :
    Tendsto (fun i => ∫ s in a..b, F i s) l (𝓝 (∫ s in a..b, f s)) := by
  apply Metric.tendsto_nhds.mpr
  intro eps heps
  let delta : ℝ := eps / (|b-a| + 1)
  have hd : 0 < delta := div_pos heps (by positivity)
  have he : delta * (|b-a| + 1) = eps := div_mul_cancel₀ _ (by positivity)
  have hsmall : delta * |b-a| < eps := by nlinarith
  have hun := (Metric.tendstoUniformlyOn_iff.mp hu) delta hd
  filter_upwards [hun] with i hi
  rw [dist_eq_norm, ← intervalIntegral.integral_sub
    ((hF i).intervalIntegrable a b) (hf.intervalIntegrable a b)]
  apply lt_of_le_of_lt (intervalIntegral.norm_integral_le_of_norm_le_const ?_) hsmall
  intro s hs
  have ht := hi s (Set.uIoc_subset_uIcc hs)
  simpa only [dist_eq_norm, norm_sub_rev] using ht.le

theorem dualRealQuadratic_continuous
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    Continuous (fun s : ℝ => (inner ℂ v (dualAmbient s A v)).re) :=
  Complex.continuous_re.comp (continuous_const.inner (dualAmbient_strongly_continuous A v))

theorem dualRealQuadratic_mono
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hAB : A ≤ B)
    (v : RegularHilbert H) (s : ℝ) :
    (inner ℂ v (dualAmbient s A v)).re ≤ (inner ℂ v (dualAmbient s B v)).re := by
  have hp := dualQuadratic_nonneg (B-A) (sub_nonneg.mpr hAB) v s
  simpa only [map_sub, _root_.sub_apply, inner_sub_right, Complex.sub_re, sub_nonneg] using hp

/-- Fixed implemented conjugation preserves strong convergence of arbitrary nets. -/
theorem dualAmbient_tendsto_strong {ι : Type*} {l : Filter ι}
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (S v))) (s : ℝ) (v : RegularHilbert H) :
    Tendsto (fun i => dualAmbient s (A i) v) l (𝓝 (dualAmbient s S v)) := by
  change Tendsto (fun i => characterMultiplier s (A i (star (characterMultiplier s) v))) l
    (𝓝 (characterMultiplier s (S (star (characterMultiplier s) v))))
  exact ((characterMultiplier (H := H) s).continuous.tendsto
      (S (star (characterMultiplier (H := H) s) v))).comp
      (hlim (star (characterMultiplier (H := H) s) v))

/-- Dini's theorem is used with an arbitrary preorder, not a countable sequence. -/
theorem dualRealQuadratic_uniform_on_compact {ι : Type*} [Preorder ι]
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (S v)))
    (v : RegularHilbert H) (C : Set ℝ) (hC : IsCompact C) :
    TendstoUniformlyOn (fun i s => (inner ℂ v (dualAmbient s (A i) v)).re)
      (fun s => (inner ℂ v (dualAmbient s S v)).re) atTop C := by
  apply Monotone.tendstoUniformlyOn_of_forall_tendsto hC
    (fun i => (dualRealQuadratic_continuous (A i) v).continuousOn)
    (fun s _ i j hij => dualRealQuadratic_mono (A i) (A j) (hmono hij) v s)
    (dualRealQuadratic_continuous S v).continuousOn
  intro s _
  exact Complex.continuous_re.continuousAt.tendsto.comp
    (tendsto_const_nhds.inner (dualAmbient_tendsto_strong A S hlim s v))

/-- Every actual finite strong cut preserves monotone strong limits in quadratic readings. -/
theorem dualWeightCut_tendsto_quadratic {ι : Type*} [Preorder ι]
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (S v)))
    (v : RegularHilbert H) (R : ℝ) :
    Tendsto (fun i => (inner ℂ v (dualWeightCut R (A i) v)).re) atTop
      (𝓝 ((inner ℂ v (dualWeightCut R S v)).re)) := by
  simp only [dualWeightCut, StrongIntegral.re_inner_operatorIntegral]
  exact intervalIntegral_tendsto_of_uniform _ _ (-R) R
    (fun i => dualRealQuadratic_continuous (A i) v) (dualRealQuadratic_continuous S v)
    (dualRealQuadratic_uniform_on_compact A S hmono hlim v _ isCompact_uIcc)

#print axioms intervalIntegral_tendsto_of_uniform
#print axioms dualRealQuadratic_continuous
#print axioms dualRealQuadratic_mono
#print axioms dualAmbient_tendsto_strong
#print axioms dualRealQuadratic_uniform_on_compact
#print axioms dualWeightCut_tendsto_quadratic
end
end TGLV350.Regular
