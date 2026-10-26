import Mathlib.Analysis.Normed.Lp.SmoothApprox
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Smooth cutoff away from the kernel of an actual continuous linear map.
The kernel must have measure zero, which is an explicit measure hypothesis;
no approximation or invariant gauge class is assumed. This generalizes the
proved origin cutoff by composing its bump with the map. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.SmoothLinearMomentumCutoff
open MeasureTheory Set Filter
open scoped Topology ContDiff
variable {E V : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup V] [InnerProductSpace ℂ V] [CompleteSpace V]
variable {Z : Type*} [NormedAddCommGroup Z] [NormedSpace ℝ Z]
  [FiniteDimensional ℝ Z]
variable (L : E→L[ℝ]Z)
variable (μ : Measure E) [IsFiniteMeasureOnCompacts μ] [NoAtoms μ]

def bump : ContDiffBump (0:Z) := ⟨1,2,by norm_num,by norm_num⟩
def cut (g : E→V) (n : ℕ) (x : E) : V :=
  (1-(bump : ContDiffBump (0:Z)) (((n:ℝ)+1) • L x)) • g x

theorem cut_smooth (g : E→V) (hg : ContDiff ℝ ∞ g) (n : ℕ) :
    ContDiff ℝ ∞ (cut L g n) := by
  unfold cut
  have hs : ContDiff ℝ ∞ (fun x : E=>((n:ℝ)+1) • L x) := contDiff_const.smul L.contDiff
  exact (contDiff_const.sub ((bump : ContDiffBump (0:Z)).contDiff.comp hs)).smul hg

theorem cut_compact (g : E→V) (hg : HasCompactSupport g) (n : ℕ) :
    HasCompactSupport (cut L g n) := hg.smul_left

theorem cut_near_zero (g : E→V) (n : ℕ) :
    ∃ε : ℝ,0<ε ∧ ∀x : E,‖L x‖≤ε→cut L g n x=0 := by
  refine ⟨1/((n:ℝ)+1),by positivity,?_⟩
  intro x hx
  have hn : 0<(n:ℝ)+1 := by positivity
  have hb : (bump : ContDiffBump (0:Z)) (((n:ℝ)+1) • L x)=1 := by
    apply ContDiffBump.one_of_mem_closedBall
    change dist (((n:ℝ)+1) • L x) 0≤1
    rw [dist_zero_right,norm_smul,Real.norm_of_nonneg hn.le]
    simpa only [mul_comm] using (le_div_iff₀ hn).mp hx
  simp only [cut,hb,sub_self,zero_smul]

theorem cut_norm_le (g : E→V) (n : ℕ) (x : E) : ‖cut L g n x‖≤‖g x‖ := by
  have hlo : 0≤(bump : ContDiffBump (0:Z)) (((n:ℝ)+1) • L x) := ContDiffBump.nonneg _
  have hhi : (bump : ContDiffBump (0:Z)) (((n:ℝ)+1) • L x)≤1 := ContDiffBump.le_one _
  rw [cut,norm_smul,Real.norm_of_nonneg (sub_nonneg.mpr hhi)]
  exact mul_le_of_le_one_left (norm_nonneg _) (by linarith)

theorem cut_eventually_eq (g : E→V) (x : E) (hx : L x≠0) :
    (fun n : ℕ=>cut L g n x)=ᶠ[atTop] fun _=>g x := by
  obtain ⟨N,hN⟩:=exists_nat_gt (2/‖L x‖)
  have hxpos : 0<‖L x‖ := norm_pos_iff.mpr hx
  have hN' : 2<(N:ℝ)*‖L x‖ := (div_lt_iff₀ hxpos).mp hN
  filter_upwards [eventually_ge_atTop N] with n hn
  have hn' : (N:ℝ)≤n := by exact_mod_cast hn
  have hb : (bump : ContDiffBump (0:Z)) (((n:ℝ)+1) • L x)=0 := by
    apply ContDiffBump.zero_of_le_dist
    change 2≤dist (((n:ℝ)+1) • L x) 0
    rw [dist_zero_right,norm_smul,Real.norm_of_nonneg (by positivity)]
    nlinarith
  simp only [cut,hb,sub_zero,one_smul]

theorem l2_integral_norm_sq (u : Lp V 2 μ) : (∫x,‖u x‖^2 ∂μ)=‖u‖^2 := by
  have h:=congrArg (RCLike.re : ℂ→ℝ) (L2.inner_def (𝕜:=ℂ) u u)
  rw [← integral_re (L2.integrable_inner (𝕜:=ℂ) u u)] at h
  simpa only [inner_self_eq_norm_sq] using h.symm

def cutLp (g : E→V) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g) (n : ℕ) :
    Lp V 2 μ := ((cut_smooth L g hg n).continuous.memLp_of_hasCompactSupport
      (cut_compact L g hc n)).toLp (cut L g n)

theorem cutLp_tendsto (g : E→V) (hg : ContDiff ℝ ∞ g) (hc : HasCompactSupport g)
    (hL : ∀ᵐ x ∂μ,L x≠0) :
    Tendsto (cutLp L μ g hg hc) atTop
      (𝓝 ((hg.continuous.memLp_of_hasCompactSupport hc : MemLp g 2 μ).toLp g)) := by
  let v : Lp V 2 μ := (hg.continuous.memLp_of_hasCompactSupport hc).toLp g
  have hmem : MemLp g 2 μ := hg.continuous.memLp_of_hasCompactSupport hc
  have hI : Tendsto (fun n=>∫x,‖cut L g n x-g x‖^2 ∂μ) atTop (𝓝 (0:ℝ)) := by
    have ht : Tendsto (fun n=>∫x,‖cut L g n x-g x‖^2 ∂μ) atTop
        (𝓝 (∫x,(0:ℝ) ∂μ)) := by
      apply tendsto_integral_of_dominated_convergence (fun x=>4*‖g x‖^2)
      · intro n
        exact (((cut_smooth L g hg n).continuous.sub hg.continuous).norm.pow 2).aestronglyMeasurable
      · exact ((memLp_two_iff_integrable_sq_norm hg.continuous.aestronglyMeasurable).mp hmem).const_mul 4
      · intro n
        apply ae_of_all
        intro x
        have hle : ‖cut L g n x-g x‖≤2*‖g x‖ := by
          calc
            _ ≤ ‖cut L g n x‖+‖g x‖ := norm_sub_le _ _
            _ ≤ 2*‖g x‖ := by linarith [cut_norm_le L g n x]
        rw [Real.norm_of_nonneg (sq_nonneg _)]
        nlinarith [norm_nonneg (cut L g n x-g x),norm_nonneg (g x)]
      · have hne : ∀ᵐ x ∂μ,L x≠0 := hL
        filter_upwards [hne] with x hx
        have he:=cut_eventually_eq L g x hx
        apply tendsto_const_nhds.congr'
        filter_upwards [he] with n hn
        simp [hn]
    simpa only [integral_zero] using ht
  have he (n : ℕ) : ‖cutLp L μ g hg hc n-v‖^2=∫x,‖cut L g n x-g x‖^2 ∂μ := by
    rw [← l2_integral_norm_sq μ]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (cutLp L μ g hg hc n) v,
      ((cut_smooth L g hg n).continuous.memLp_of_hasCompactSupport
        (cut_compact L g hc n) : MemLp (cut L g n) 2 μ).coeFn_toLp,hmem.coeFn_toLp] with x hs hn hv
    simp only [hs,Pi.sub_apply]
    simp only [cutLp,v]
    rw [hn,hv]
  have hn:=Real.continuous_sqrt.continuousAt.tendsto.comp
    (show Tendsto (fun n=>‖cutLp L μ g hg hc n-v‖^2) atTop (𝓝 (0:ℝ)) by simpa only [he] using hI)
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,dist_eq_norm] using hn

end F1Fecho.SmoothLinearMomentumCutoff
#print axioms F1Fecho.SmoothLinearMomentumCutoff.cut_smooth
#print axioms F1Fecho.SmoothLinearMomentumCutoff.cut_near_zero
#print axioms F1Fecho.SmoothLinearMomentumCutoff.cut_eventually_eq
#print axioms F1Fecho.SmoothLinearMomentumCutoff.cutLp_tendsto
