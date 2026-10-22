import OpticalAreaFreedom
import Mathlib.Analysis.Calculus.Taylor

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace ChatgptAudit.Quartic037
open Filter Set ChatgptAudit.Optical036
open scoped Topology
noncomputable section

/- The fourth Taylor polynomial is evaluated from the already proved derivatives.
Taylor--Peano then controls the remainder. Only after that theorem is applied do
we divide on the punctured neighbourhood and transport the result to inducedArea. -/

theorem optical_jacobi_taylor_four (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (t : ℝ) :
    taylorWithinEval (opticalJacobiArea a c) 4 univ 0 t =
      1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4 := by
  norm_num [taylor_within_apply,Finset.sum_range_succ,iteratedDerivWithin_univ,
    iteratedDeriv_zero,optical_jacobi_area_zero,
    optical_jacobi_area_iterated_one_zero a c ha hc,
    optical_jacobi_area_iterated_two_zero a c ha hc,
    optical_jacobi_area_iterated_three_zero a c ha hc,
    optical_jacobi_area_iterated_four_zero a c ha hc] <;> ring

theorem optical_jacobi_taylor_remainder_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ =>
      (opticalJacobiArea a c t-
        (1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4))/t^4)
      (𝓝 0) (𝓝 0) := by
  have h := Real.taylor_tendsto (f := opticalJacobiArea a c)
    (x₀ := 0) (n := 4) (s := univ) convex_univ (mem_univ 0)
    (optical_jacobi_area_contDiff a c).contDiffOn
  simpa only [nhdsWithin_univ,sub_zero,optical_jacobi_taylor_four a c ha hc] using h

theorem optical_jacobi_area_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 ((a^2+6*a*c+c^2)/24)) := by
  have h0 := (optical_jacobi_taylor_remainder_limit a c ha hc).mono_left
    (show 𝓝[≠] (0 : ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)
  have hq := h0.add_const ((a^2+6*a*c+c^2)/24)
  have he :
      (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ =>
        (opticalJacobiArea a c t-
          (1-(a+c)*t^2/2+(a^2+6*a*c+c^2)/24*t^4))/t^4+
            (a^2+6*a*c+c^2)/24) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have ht0 : t≠0 := ht
    field_simp [ht0] <;> ring
  exact (tendsto_congr' he).2 (by simpa only [zero_add] using hq)

/-- Effective fourth-order asymptotics of the geometric Jacobi screen area. -/
theorem geometric_jacobi_area_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    Tendsto (fun t : ℝ => (geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 ((a^2+6*a*c+c^2)/24)) := by
  have he :
      (fun t : ℝ => (geometricJacobiArea a c t-1+(a+c)*t^2/2)/t^4) =ᶠ[𝓝[≠] 0]
      (fun t : ℝ => (opticalJacobiArea a c t-1+(a+c)*t^2/2)/t^4) := by
    filter_upwards [(geometric_jacobi_area_agrees_near_zero a c ha hc).filter_mono
      (show 𝓝[≠] (0 : ℝ) ≤ 𝓝 0 from nhdsWithin_le_nhds)] with t ht
    rw [ht]
  exact (tendsto_congr' he).2 (optical_jacobi_area_quartic_limit a c ha hc)

theorem geometric_jacobi_area_rs_quartic_limit (r s : ℝ) (hs : |s|<r/2) :
    Tendsto (fun t : ℝ =>
      (geometricJacobiArea (r/2+s) (r/2-s) t-1+r*t^2/2)/t^4)
      (𝓝[≠] 0) (𝓝 (r^2/12-s^2/6)) := by
  obtain ⟨ha,hc⟩ := optical_rs_positive_coefficients r s hs
  have hsum : r/2+s+(r/2-s)=r := by ring
  have hcoeff :
      ((r/2+s)^2+6*(r/2+s)*(r/2-s)+(r/2-s)^2)/24=r^2/12-s^2/6 := by ring
  simpa only [hsum,hcoeff] using
    geometric_jacobi_area_quartic_limit (r/2+s) (r/2-s) ha.le hc.le

#print axioms optical_jacobi_taylor_four
#print axioms optical_jacobi_taylor_remainder_limit
#print axioms optical_jacobi_area_quartic_limit
#print axioms geometric_jacobi_area_quartic_limit
#print axioms geometric_jacobi_area_rs_quartic_limit

end
end ChatgptAudit.Quartic037
