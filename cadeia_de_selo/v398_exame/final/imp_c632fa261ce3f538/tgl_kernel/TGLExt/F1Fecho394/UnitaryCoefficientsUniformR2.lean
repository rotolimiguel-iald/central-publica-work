import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Topology.MetricSpace.UniformConvergence
import Mathlib.Tactic
set_option autoImplicit false
noncomputable section
open Filter Set
open scoped Topology
namespace F1Fecho.UnitaryCoefficientsUniform
variable {H X : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem left (U : X→H≃ₗᵢ[ℂ]H) (v : H) (u : ℕ→H) (x : H)
    (hu : Tendsto u atTop (𝓝 x)) :
    TendstoUniformlyOn (fun n t => inner ℂ (u n) (U t v))
      (fun t => inner ℂ x (U t v)) atTop univ := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro ε hε
  have ht : Tendsto (fun n => ‖u n-x‖*‖v‖) atTop (𝓝 0) := by
    simpa using (hu.sub (tendsto_const_nhds (x:=x))).norm.mul_const ‖v‖
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with n hn
  intro t _
  rw [dist_comm,dist_eq_norm,← inner_sub_left]
  have hb : ‖inner ℂ (u n-x) (U t v)‖ ≤ ‖u n-x‖*‖v‖ := by
    simpa only [(U t).norm_map] using (norm_inner_le_norm (𝕜:=ℂ) (u n-x) (U t v))
  exact hb.trans_lt hn

theorem right (U : X→H≃ₗᵢ[ℂ]H) (v : H) (u : ℕ→H) (x : H)
    (hu : Tendsto u atTop (𝓝 x)) :
    TendstoUniformlyOn (fun n t => inner ℂ v (U t (u n)))
      (fun t => inner ℂ v (U t x)) atTop univ := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro ε hε
  have ht : Tendsto (fun n => ‖v‖*‖u n-x‖) atTop (𝓝 0) := by
    simpa using (hu.sub (tendsto_const_nhds (x:=x))).norm.const_mul ‖v‖
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with n hn
  intro t _
  rw [dist_comm,dist_eq_norm,← inner_sub_right,← map_sub]
  have hb : ‖inner ℂ v (U t (u n-x))‖ ≤ ‖v‖*‖u n-x‖ := by
    simpa only [(U t).norm_map] using (norm_inner_le_norm (𝕜:=ℂ) v (U t (u n-x)))
  exact hb.trans_lt hn

end F1Fecho.UnitaryCoefficientsUniform
#print axioms F1Fecho.UnitaryCoefficientsUniform.left
#print axioms F1Fecho.UnitaryCoefficientsUniform.right
