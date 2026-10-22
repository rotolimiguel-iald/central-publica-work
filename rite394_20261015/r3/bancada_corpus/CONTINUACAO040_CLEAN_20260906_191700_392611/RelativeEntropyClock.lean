import BinaryRelativeQuartic
import Mathlib.Analysis.Calculus.LHopital
set_option autoImplicit false
set_option maxHeartbeats 2500000
namespace ChatgptAudit.Clock040
open Filter Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Response028
  ChatgptAudit.Quartic037 ChatgptAudit.Flow020
open scoped Topology
noncomputable section

/-- A cubic primitive limit from an actual derivative on the negative half-neighbourhood. -/
theorem primitive_cubic_limit (flux primitive : ℝ → ℝ) (coefficient : ℝ)
    (hderiv : ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt primitive (flux t) t)
    (hcontinuous : ContinuousAt primitive 0) (hzero : primitive 0 = 0)
    (hflux : Tendsto (fun t => flux t / t^2) (𝓝[<] 0) (𝓝 coefficient)) :
    Tendsto (fun t => primitive t / t^3) (𝓝[<] 0) (𝓝 (coefficient / 3)) := by
  have hg : ∀ᶠ t in 𝓝[<] (0:ℝ),
      HasDerivAt (fun s : ℝ => s^3) (3*t^2) t :=
    Filter.Eventually.of_forall (fun t => by simpa using (hasDerivAt_id t).pow 3)
  have hgn : ∀ᶠ t in 𝓝[<] (0:ℝ), 3*t^2 ≠ 0 := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_ne_zero (by norm_num) (pow_ne_zero _ (ne_of_lt ht))
  have hfzero : Tendsto primitive (𝓝[<] 0) (𝓝 0) := by
    simpa only [hzero] using hcontinuous.tendsto.mono_left nhdsWithin_le_nhds
  have hgzero : Tendsto (fun t : ℝ => t^3) (𝓝[<] 0) (𝓝 0) := by
    simpa using ((continuousAt_id : ContinuousAt (fun t : ℝ => t) 0).pow 3).tendsto.mono_left nhdsWithin_le_nhds
  have hratio : Tendsto (fun t => flux t/(3*t^2)) (𝓝[<] 0) (𝓝 (coefficient/3)) := by
    simpa only [mul_comm (3:ℝ), div_mul_eq_div_div] using hflux.div_const (3:ℝ)
  exact HasDerivAt.lhopital_zero_nhdsLT hderiv hg hgn hfzero hgzero hratio

def binaryEntropySlope (k y : ℝ) : ℝ :=
  k*(Real.log (1/3+k*y)-Real.log (1/3)) -
    k*(Real.log (1-(1/3+k*y))-Real.log (1-(1/3)))

def binaryEntropyCurvature (k y : ℝ) : ℝ :=
  k^2/(1/3+k*y)+k^2/(1-(1/3+k*y))

theorem binary_entropy_slope_zero (k : ℝ) : binaryEntropySlope k 0 = 0 := by
  simp [binaryEntropySlope]

theorem binary_entropy_curvature_zero (k : ℝ) :
    binaryEntropyCurvature k 0 = (9/2)*k^2 := by
  norm_num [binaryEntropyCurvature]; ring

theorem binary_entropy_curvature_derivative_zero (k : ℝ) :
    HasDerivAt (binaryEntropyCurvature k) (-(27/4)*k^3) 0 := by
  have hp := ((hasDerivAt_id (0:ℝ)).const_mul k).const_add (1/3:ℝ)
  have hq := hp.const_sub 1
  have h := ((hasDerivAt_const (0:ℝ) (k^2)).div hp (by norm_num)).add
    ((hasDerivAt_const (0:ℝ) (k^2)).div hq (by norm_num))
  convert h using 1 <;> first | rfl | norm_num <;> ring

theorem binary_entropy_positive_near (k : ℝ) :
    ∀ᶠ y in 𝓝 (0:ℝ), 0 < 1/3+k*y ∧ 0 < 1-(1/3+k*y) := by
  have hp := ((hasDerivAt_id (0:ℝ)).const_mul k).const_add (1/3:ℝ)
  have hq := hp.const_sub 1
  have ha := hp.continuousAt.eventually (Ioi_mem_nhds (by norm_num : (0:ℝ)<1/3+k*0))
  have hb := hq.continuousAt.eventually (Ioi_mem_nhds (by norm_num : (0:ℝ)<1-(1/3+k*0)))
  exact ha.and hb

theorem binary_entropy_slope_derivative (k y : ℝ)
    (hp : 1/3+k*y ≠ 0) (hq : 1-(1/3+k*y) ≠ 0) :
    HasDerivAt (binaryEntropySlope k) (binaryEntropyCurvature k y) y := by
  have ha := ((hasDerivAt_id y).const_mul k).const_add (1/3:ℝ)
  have hb := ha.const_sub 1
  have h := (((ha.log hp).sub_const (Real.log (1/3))).const_mul k).sub
    (((hb.log hq).sub_const (Real.log (1-(1/3)))).const_mul k)
  convert h using 1 <;> first | rfl | dsimp [binaryEntropyCurvature]; ring

theorem binary_entropy_actual_derivative (k : ℝ) :
    ∀ᶠ y in 𝓝[<] (0:ℝ),
      HasDerivAt
        (fun z => diagonalRelativeEntropy (siteW (1/3+k*z)) (siteW (1/3)))
        (binaryEntropySlope k y) y := by
  have h := relative_curve_derivative_past (binaryAffineCurve k)
    (siteW_pos (by norm_num) (by norm_num))
  filter_upwards [h] with y hy
  convert hy using 1
  · rfl
  · simp [relativeEntropyRate, binaryAffineCurve, binaryEntropySlope, siteW,
      Fin.sum_univ_two]
    ring

theorem binary_entropy_slope_quadratic_limit (k : ℝ) :
    Tendsto (fun y => (binaryEntropySlope k y-(9/2)*k^2*y)/y^2)
      (𝓝[<] 0) (𝓝 (-(27/8)*k^3)) := by
  have hc := binary_entropy_curvature_derivative_zero k
  have hs : Tendsto (fun y => (binaryEntropyCurvature k y-(9/2)*k^2)/y)
      (𝓝[<] 0) (𝓝 (-(27/4)*k^3)) := by
    simpa only [zero_add, binary_entropy_curvature_zero, sub_zero,
      smul_eq_mul, div_eq_mul_inv, mul_comm] using hc.tendsto_slope_zero_left
  have h := primitive_quadratic_limit
    (fun y => binaryEntropyCurvature k y-(9/2)*k^2)
    (fun y => binaryEntropySlope k y-(9/2)*k^2*y) (-(27/4)*k^3) ?_ ?_ ?_ hs
  · convert h using 1 <;> ring
  · filter_upwards [(binary_entropy_positive_near k).filter_mono nhdsWithin_le_nhds] with y hy
    exact (binary_entropy_slope_derivative k y (ne_of_gt hy.1) (ne_of_gt hy.2)).sub
      ((hasDerivAt_id y).const_mul ((9/2)*k^2))
  · exact ((binary_entropy_slope_derivative k 0 (by norm_num) (by norm_num)).continuousAt).sub
      (continuousAt_const.mul continuousAt_id)
  · simp [binary_entropy_slope_zero]

theorem binary_entropy_cubic_limit (k : ℝ) :
    Tendsto (fun y => (diagonalRelativeEntropy (siteW (1/3+k*y)) (siteW (1/3)) -
        (9/4)*k^2*y^2)/y^3)
      (𝓝[<] 0) (𝓝 (-(9/8)*k^3)) := by
  have h := primitive_cubic_limit
    (fun y => binaryEntropySlope k y-(9/2)*k^2*y)
    (fun y => diagonalRelativeEntropy (siteW (1/3+k*y)) (siteW (1/3)) -
      (9/4)*k^2*y^2) (-(27/8)*k^3) ?_ ?_ ?_
    (binary_entropy_slope_quadratic_limit k)
  · convert h using 1 <;> ring
  · filter_upwards [binary_entropy_actual_derivative k] with y hy
    have hd := ((hasDerivAt_id y).pow 2).const_mul ((9/4)*k^2)
    convert hy.sub hd using 1 <;> first | rfl | ring
  · exact (relative_curve_continuous_zero (binaryAffineCurve k)
      (siteW_pos (by norm_num) (by norm_num))).sub
        (continuousAt_const.mul (continuousAt_id.pow 2))
  · simp only [mul_zero, add_zero, relative_entropy_self, zero_pow (by norm_num : 2 ≠ 0), sub_zero]

theorem regular_parameter_square_sixth_limit :
    Tendsto (fun t : ℝ => (regularParameter t ^ 2 - t^4)/t^6)
      (𝓝[≠] 0) (𝓝 (-2)) := by
  have ht := quartic_time_tendsto_zero
  have h := ((ht.pow 2).const_add 2).neg.div (((ht.pow 2).const_add 1).pow 2) (by norm_num)
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht0
  dsimp [regularParameter]
  field_simp [ht0]
  <;> ring

/-- Sixth order of the actual existing one-site relative entropy. -/
theorem binary_relative_sixth_limit (k : ℝ) :
    Tendsto (fun t : ℝ => (binaryRelativeAt k t-(9/4)*k^2*t^4)/t^6)
      (𝓝[≠] 0) (𝓝 (-(9/2)*k^2+(9/8)*k^3)) := by
  have hbase := (binary_entropy_cubic_limit k).comp quartic_negative_regular_parameter_tendsto
  have hratio : Tendsto (fun t : ℝ => (-regularParameter t)^3/t^6)
      (𝓝[≠] 0) (𝓝 (-1)) := by
    have h := quartic_regular_parameter_ratio.neg.pow 3
    apply h.congr'
    filter_upwards [quartic_punctured_time_nonzero] with t ht0
    field_simp [ht0]
    <;> ring
  have h := (hbase.mul hratio).add
    (regular_parameter_square_sixth_limit.const_mul ((9/4)*k^2))
  have hvalue : (-(9/8)*k^3)*(-1)+((9/4)*k^2)*(-2) =
      -(9/2)*k^2+(9/8)*k^3 := by ring
  rw [hvalue] at h
  apply h.congr'
  filter_upwards [quartic_punctured_time_nonzero] with t ht0
  have hh : regularParameter t ≠ 0 := ne_of_gt (regular_parameter_positive t ht0)
  have he : 1/3+k*(-regularParameter t)=1/3-k*regularParameter t := by ring
  simp only [he, ← binaryRelativeAt]
  field_simp [ht0, hh]
  <;> ring

#print axioms primitive_cubic_limit
#print axioms binaryEntropySlope
#print axioms binaryEntropyCurvature
#print axioms binary_entropy_slope_zero
#print axioms binary_entropy_curvature_zero
#print axioms binary_entropy_curvature_derivative_zero
#print axioms binary_entropy_positive_near
#print axioms binary_entropy_slope_derivative
#print axioms binary_entropy_actual_derivative
#print axioms binary_entropy_slope_quadratic_limit
#print axioms binary_entropy_cubic_limit
#print axioms regular_parameter_square_sixth_limit
#print axioms binary_relative_sixth_limit
end
end ChatgptAudit.Clock040
