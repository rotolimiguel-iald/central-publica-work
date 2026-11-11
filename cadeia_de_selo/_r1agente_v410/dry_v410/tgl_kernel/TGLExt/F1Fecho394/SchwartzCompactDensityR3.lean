import TGLExt.F1Fecho394.SchwartzCutoffEstimateR5
import Mathlib.Analysis.SpecificLimits.Basic

/-! Every Schwartz test is the limit, in its own Schwartz topology, of
smooth compactly supported tests obtained with a fixed real cutoff. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open Filter SchwartzMap
open scoped Topology ContDiff
namespace F1Fecho.SchwartzCutoff
variable {F:Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]

theorem cutoff_compact (s:ℝ) (hs:0<s) (f:SchwartzMap E F) :
    HasCompactSupport (cutoff s f:E→F) := by
  apply (isCompact_closedBall (0:E) (2/s)).of_isClosed_subset isClosed_closure
  apply closure_minimal _ Metric.isClosed_closedBall
  intro x hx
  have hb:bump (s • x)≠0 := by
    intro hh
    exact hx (by simp [cutoff_apply,hh])
  have hball:s • x∈Metric.ball (0:E) 2 := by
    have hm : s • x ∈ Function.support (bump:E→ℝ) := hb
    rw [bump.support_eq] at hm
    exact hm
  have hn:s*‖x‖<2 := by
    simpa only [Metric.mem_ball,dist_zero_right,norm_smul,Real.norm_of_nonneg hs.le] using hball
  rw [Metric.mem_closedBall,dist_zero_right]
  exact (le_div_iff₀ hs).mpr (by nlinarith)

def cutoffSequence (f:SchwartzMap E F) (n:ℕ) : SchwartzMap E F :=
  cutoff (1/((n:ℝ)+1)) f

theorem cutoffSequence_tendsto (f:SchwartzMap E F) :
    Tendsto (cutoffSequence f) atTop (𝓝 f) := by
  apply (schwartz_withSeminorms ℝ E F).tendsto_nhds _ _ |>.mpr
  rintro ⟨k,n⟩ ε hε
  have ht:Tendsto (fun m:ℕ=>(1/((m:ℝ)+1))*errorBound k n f) atTop (𝓝 0) := by
    simpa using (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜:=ℝ)).mul_const (errorBound k n f)
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with m hm
  have hb:=error_seminorm_bound (1/((m:ℝ)+1)) (by positivity)
    (show 1/((m:ℝ)+1)≤1 by apply (div_le_one (by positivity)).mpr; linarith [Nat.cast_nonneg (α:=ℝ) m]) f k n
  change SchwartzMap.seminorm ℝ k n (cutoffSequence f m-f)<ε
  rw [←neg_sub f (cutoffSequence f m),map_neg_eq_map]
  exact hb.trans_lt hm

theorem compact_tests_dense :
    Dense {f:SchwartzMap E F|HasCompactSupport (f:E→F)} := by
  intro f
  exact isClosed_closure.mem_of_tendsto (cutoffSequence_tendsto f)
    (Eventually.of_forall (fun n=>subset_closure (cutoff_compact _ (by positivity) f)))

end F1Fecho.SchwartzCutoff
#print axioms F1Fecho.SchwartzCutoff.cutoff_compact
#print axioms F1Fecho.SchwartzCutoff.cutoffSequence_tendsto
#print axioms F1Fecho.SchwartzCutoff.compact_tests_dense
