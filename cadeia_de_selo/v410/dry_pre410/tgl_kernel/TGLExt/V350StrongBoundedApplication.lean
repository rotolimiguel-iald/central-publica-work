import TGLExt.V350ContractionAdjointLimit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Uniform operator bounds permit the vector to move in a strong limit.
No convergence in operator norm is required. -/
theorem bounded_application_tendsto {ι : Type*} (l : Filter ι)
    (A : ι → H →L[ℂ] H) (C : ℝ) (hbound : ∀ i, ‖A i‖ ≤ C)
    (v : ι → H) (v₀ w : H) (hv : Tendsto v l (𝓝 v₀))
    (hfixed : Tendsto (fun i => A i v₀) l (𝓝 w)) :
    Tendsto (fun i => A i (v i)) l (𝓝 w) := by
  have hd : Tendsto (fun i => ‖v i - v₀‖) l (𝓝 0) := by
    have hs : Tendsto (fun i => v i - v₀) l (𝓝 (v₀-v₀)) := hv.sub tendsto_const_nhds
    simpa only [sub_self, norm_zero] using hs.norm
  have hc : Tendsto (fun i => C * ‖v i - v₀‖) l (𝓝 0) := by
    simpa only [mul_zero] using (tendsto_const_nhds.mul hd :
      Tendsto (fun i => C * ‖v i - v₀‖) l (𝓝 (C*0)))
  have he (i : ι) : ‖A i (v i - v₀)‖ ≤ C * ‖v i - v₀‖ :=
    (ContinuousLinearMap.le_opNorm _ _).trans
      (mul_le_mul_of_nonneg_right (hbound i) (norm_nonneg _))
  have hz : Tendsto (fun i => A i (v i-v₀)) l (𝓝 0) := by
    apply tendsto_iff_dist_tendsto_zero.mpr
    simpa only [dist_zero_right] using squeeze_zero (fun i => norm_nonneg _) he hc
  simpa only [map_sub, sub_add_cancel, zero_add] using hz.add hfixed

#print axioms bounded_application_tendsto
end
end TGLV350.Regular
