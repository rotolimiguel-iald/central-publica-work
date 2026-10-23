import TGLExt.V350RegularApproximation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Strong convergence of contractions to the identity also controls their
adjoints. This uses the contraction bound, not SOT continuity of star. -/
theorem contraction_adjoint_tendsto_identity {ι : Type*} (l : Filter ι)
    (A : ι → H →L[ℂ] H) (hbound : ∀ i, ‖A i‖ ≤ 1)
    (hstrong : ∀ v, Tendsto (fun i => A i v) l (𝓝 v)) (v : H) :
    Tendsto (fun i => star (A i) v) l (𝓝 v) := by
  have hb (i : ι) : ‖star (A i) v‖ ≤ ‖v‖ := by
    calc
      _ ≤ ‖star (A i)‖ * ‖v‖ := ContinuousLinearMap.le_opNorm _ _
      _ ≤ 1 * ‖v‖ := mul_le_mul_of_nonneg_right (by simpa using hbound i) (norm_nonneg _)
      _ = _ := one_mul _
  have he (i : ι) : ‖star (A i) v - v‖ ^ 2 ≤
      2 * (‖v‖ ^ 2 - (inner ℂ v (A i v)).re) := by
    rw [norm_sub_sq (𝕜 := ℂ)]
    change ‖star (A i) v‖ ^ 2 - 2 * (inner ℂ (star (A i) v) v).re + ‖v‖ ^ 2 ≤ _
    have hadj : inner ℂ (star (A i) v) v = inner ℂ v (A i v) :=
      ContinuousLinearMap.adjoint_inner_left (A i) v v
    rw [hadj]
    nlinarith [pow_le_pow_left₀ (norm_nonneg (star (A i) v)) (hb i) 2]
  have hi : Tendsto (fun i => (inner ℂ v (A i v)).re) l (𝓝 (‖v‖ ^ 2)) := by
    have hi0 : Tendsto (fun i => inner ℂ v (A i v)) l (𝓝 (inner ℂ v v)) :=
      tendsto_const_nhds.inner (hstrong v)
    have hi1 : Tendsto (fun i => (inner ℂ v (A i v)).re) l (𝓝 (inner ℂ v v).re) :=
      RCLike.continuous_re.continuousAt.tendsto.comp hi0
    have hv : (inner ℂ v v).re = ‖v‖ ^ 2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
    rw [hv] at hi1
    exact hi1
  have hr : Tendsto (fun i => 2 * (‖v‖ ^ 2 - (inner ℂ v (A i v)).re)) l (𝓝 0) := by
    have hr0 : Tendsto (fun i => 2 * (‖v‖ ^ 2 - (inner ℂ v (A i v)).re)) l
        (𝓝 (2 * (‖v‖ ^ 2 - ‖v‖ ^ 2))) :=
      tendsto_const_nhds.mul (tendsto_const_nhds.sub hi)
    simpa using hr0
  have hs := squeeze_zero (fun i => sq_nonneg ‖star (A i) v - v‖) he hr
  have hn : Tendsto (fun i => ‖star (A i) v - v‖) l (𝓝 0) := by
    simpa only [Function.comp_def, Real.sqrt_sq_eq_abs, abs_norm, Real.sqrt_zero] using
      Real.continuous_sqrt.continuousAt.tendsto.comp hs
  exact tendsto_iff_dist_tendsto_zero.mpr (by simpa only [dist_eq_norm] using hn)

theorem regularAverage_star_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => star (regularAverage P h) v) (𝓝[≠] 0) (𝓝 v) :=
  contraction_adjoint_tendsto_identity _ _ (regularAverage_norm_le_one P)
    (regularAverage_tendsto_identity P) v

#print axioms contraction_adjoint_tendsto_identity
#print axioms regularAverage_star_tendsto_identity
end
end TGLV350.Regular
