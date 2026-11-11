import Mathlib.Analysis.Distribution.SchwartzSpace.Basic
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Tactic

/-! Uniform derivative control of a fixed smooth compact cutoff under dilations.
This is the first estimate for compact approximation in Schwartz topology. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter
open scoped Topology ContDiff
namespace F1Fecho.SchwartzCutoff
abbrev E := EuclideanSpace ℝ (Fin 4)

def bump : ContDiffBump (0:E) := ⟨1,2,by norm_num,by norm_num⟩
def bumpSchwartz : SchwartzMap E ℝ := bump.hasCompactSupport.toSchwartzMap bump.contDiff

def residual (s:ℝ) (x:E) : ℝ := 1-bump (s • x)
def bound (n:ℕ) : ℝ := 1+SchwartzMap.seminorm ℝ 0 n bumpSchwartz

theorem residual_smooth (s:ℝ) : ContDiff ℝ ∞ (residual s) :=
  contDiff_const.sub (bump.contDiff.comp (contDiff_id.const_smul s))

theorem derivative_scaled (s:ℝ) (hs:0≤s) (hs1:s≤1) (n:ℕ) (x:E) :
    ‖iteratedFDeriv ℝ n (fun y:E=>bump (s • y)) x‖≤
      SchwartzMap.seminorm ℝ 0 n bumpSchwartz := by
  rw [iteratedFDeriv_comp_const_smul s (bump.contDiff : ContDiff ℝ n bump)]
  rw [norm_smul,Real.norm_of_nonneg (pow_nonneg hs n)]
  have hb:=bumpSchwartz.le_seminorm ℝ 0 n (s • x)
  simp only [pow_zero,one_mul] at hb
  change ‖iteratedFDeriv ℝ n (fun y:E=>bump y) (s • x)‖≤SchwartzMap.seminorm ℝ 0 n bumpSchwartz at hb
  have hs':s^n≤1 := pow_le_one₀ hs hs1
  exact (mul_le_mul_of_nonneg_right hs' (norm_nonneg _)).trans (by simpa only [one_mul] using hb)

theorem residual_derivative_bound (s:ℝ) (hs:0≤s) (hs1:s≤1) (n:ℕ) (x:E) :
    ‖iteratedFDeriv ℝ n (residual s) x‖≤bound n := by
  have hc:‖iteratedFDeriv ℝ n (fun _:E=>(1:ℝ)) x‖≤1 := by
    cases n with
    | zero => simp
    | succ n => simp [iteratedFDeriv_const_of_ne (Nat.succ_ne_zero n)]
  have he:iteratedFDeriv ℝ n (residual s) x=
      iteratedFDeriv ℝ n (fun _:E=>(1:ℝ)) x-
      iteratedFDeriv ℝ n (fun y:E=>bump (s • y)) x :=
    iteratedFDeriv_sub_apply contDiffAt_const
      ((bump.contDiff.comp (contDiff_id.const_smul s) :
        ContDiff ℝ n (fun y:E=>bump (s • y))).contDiffAt)
  rw [he]
  exact (norm_sub_le _ _).trans (add_le_add hc (derivative_scaled s hs hs1 n x))

theorem residual_eventually_zero (s:ℝ) (x:E) (hx:‖s • x‖<1) :
    residual s =ᶠ[𝓝 x] 0 := by
  have h:=bump.eventuallyEq_one_of_mem_ball (by simpa [bump,Metric.mem_ball,dist_zero_right] using hx)
  have hc:Continuous (fun y:E=>s • y):=continuous_const.smul continuous_id
  filter_upwards [hc.continuousAt.preimage_mem_nhds h] with y hy
  change bump (s • y)=1 at hy
  simp only [residual,Pi.zero_apply,hy,sub_self]

theorem residual_product_derivative_zero {F:Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (s:ℝ) (f:E→F) (n:ℕ) (x:E) (hx:‖s • x‖<1) :
    iteratedFDeriv ℝ n (fun y=>residual s y • f y) x=0 := by
  have h:(fun y=>residual s y • f y)=ᶠ[𝓝 x] 0 := by
    filter_upwards [residual_eventually_zero s x hx] with y hy
    simp only [hy,zero_smul,Pi.zero_apply]
  have hh:=(h.iteratedFDeriv (𝕜:=ℝ) n).eq_of_nhds
  simpa using hh

end F1Fecho.SchwartzCutoff
#print axioms F1Fecho.SchwartzCutoff.residual_derivative_bound
#print axioms F1Fecho.SchwartzCutoff.residual_product_derivative_zero
