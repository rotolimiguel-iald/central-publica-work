import OpticalEquilibriumScreen
import OpticalHeatClausius

set_option autoImplicit false
set_option maxHeartbeats 3000000
namespace ChatgptAudit.Optical043
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Flow019 ChatgptAudit.Flow020
  ChatgptAudit.Wave029 ChatgptAudit.Optical036 ChatgptAudit.Heat041
open scoped Topology ContDiff
noncomputable section

/-- The integral of any admissible extension agrees with the original integrand
on a sufficiently small past interval, not necessarily globally. -/
theorem past_integral_original_germ (f : ℝ → ℝ) (E : PastContinuousExtension f) :
    pastIntegral E =ᶠ[𝓝[<] (0:ℝ)] (fun t => ∫ s in (0:ℝ)..t, f s) := by
  obtain ⟨l,hl,hsub⟩ := mem_nhdsLT_iff_exists_Ioo_subset.mp E.matches_past
  filter_upwards [Ioo_mem_nhdsLT hl] with t ht
  apply intervalIntegral.integral_congr
  intro s hs
  have hst : s∈Icc t 0 := by
    simpa only [uIcc_of_ge ht.2.le] using hs
  by_cases hz : s=0
  · subst s
    exact E.at_zero
  · exact hsub ⟨lt_of_lt_of_le ht.1 hst.1,lt_of_le_of_ne hst.2 hz⟩

/-- The actual constructed flux, with no entropy or matching hypothesis. -/
theorem optical_screen_heat_flux (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass t : ℝ) :
    screenHeatFlux (opticalEquilibriumScreen a c ha hc) (waveMatter a c mass) rate t =
      opticalHeatFlux a c rate mass t := by
  unfold screenHeatFlux
  rw [optical_equilibrium_velocity_central a c ha hc t,
    optical_equilibrium_curve a c ha hc,optical_equilibrium_columns a c ha hc]
  exact (optical_heat_flux_geometric a c rate mass t).symm

/-- This is constructedHeat of the explicit geometric screen, not heat defined
from an area or Clausius identity. -/
def opticalScreenHeat (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (rate mass : ℝ) : ℝ → ℝ :=
  constructedHeat (opticalEquilibriumScreen a c ha hc) (waveMatter a c mass) rate
    isOpen_univ (frame_metric_smooth univ (waveSolder a c) (wave_solder_smooth a c))
    (fun i j => (wave_matter_smooth a c mass i j).differentiableOn (by simp))

theorem optical_screen_heat_germ (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass : ℝ) :
    opticalScreenHeat a c ha hc rate mass =ᶠ[𝓝[<] (0:ℝ)] opticalHeat a c rate mass := by
  have h := past_integral_original_germ
    (screenHeatFlux (opticalEquilibriumScreen a c ha hc) (waveMatter a c mass) rate)
    (screenHeatExtension (opticalEquilibriumScreen a c ha hc) (waveMatter a c mass) rate
      isOpen_univ (frame_metric_smooth univ (waveSolder a c) (wave_solder_smooth a c))
      (fun i j => (wave_matter_smooth a c mass i j).differentiableOn (by simp)))
  simpa only [optical_screen_heat_flux] using h

theorem optical_screen_heat_zero (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (rate mass : ℝ) :
    opticalScreenHeat a c ha hc rate mass 0=0 :=
  constructed_heat_zero _ _ _ _ _ _

theorem optical_screen_heat_quadratic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass : ℝ) :
    Tendsto (fun t => opticalScreenHeat a c ha hc rate mass t/t^2)
      (𝓝[<] 0) (𝓝 (-rate*mass/2)) := by
  have h := constructed_heat_quadratic_limit
    (opticalEquilibriumScreen a c ha hc) (waveMatter a c mass) rate
    isOpen_univ (frame_metric_smooth univ (waveSolder a c) (wave_solder_smooth a c))
    (fun i j => (wave_matter_smooth a c mass i j).differentiableOn (by simp))
  simpa only [wave_matter_quad,central_direction_frequency,one_pow,mul_one] using h

/-- The existing horizon balance primitive evaluated on the explicit screen. -/
def opticalScreenClausiusDefect (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) : ℝ → ℝ :=
  horizonBalancePrimitive rate eta
    (inducedArea (frameMetricField (waveSolder a c))
      (opticalEquilibriumScreen a c ha hc).curve
      (opticalEquilibriumScreen a c ha hc).screen.vectors)
    (opticalScreenHeat a c ha hc rate mass)

theorem optical_screen_clausius_germ (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) :
    opticalScreenClausiusDefect a c ha hc rate mass eta =ᶠ[𝓝[<] (0:ℝ)]
      opticalClausiusDefect a c rate mass eta := by
  filter_upwards [optical_screen_heat_germ a c ha hc rate mass] with t ht
  simp only [opticalScreenClausiusDefect,horizonBalancePrimitive,optical_equilibrium_area,
    geometric_jacobi_area_zero,ht,opticalClausiusDefect]

/-- The full coefficient before imposing any entropy-area or matter-curvature matching. -/
theorem optical_screen_clausius_quadratic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) :
    Tendsto (fun t => opticalScreenClausiusDefect a c ha hc rate mass eta t/t^2)
      (𝓝[<] 0) (𝓝 (rate*(eta*(a+c)-2*Real.pi*mass)/(4*Real.pi))) := by
  have hle : 𝓝[<] (0:ℝ) ≤ 𝓝[≠] (0:ℝ) :=
    nhdsWithin_mono 0 (fun _ ht => ne_of_lt ht)
  have hA := (geometric_area_quadratic_limit a c ha hc).mono_left hle
  have h := (optical_screen_heat_quadratic_limit a c ha hc rate mass).sub
    (hA.const_mul (rate/(2*Real.pi)*eta))
  have hscalar : -rate*mass/2-(rate/(2*Real.pi)*eta)*(-(a+c)/2)=
      rate*(eta*(a+c)-2*Real.pi*mass)/(4*Real.pi) := by
    field_simp [Real.pi_ne_zero]
    ring
  rw [hscalar] at h
  have he : (fun t => opticalScreenClausiusDefect a c ha hc rate mass eta t/t^2) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => opticalScreenHeat a c ha hc rate mass t/t^2-
        (rate/(2*Real.pi)*eta)*((geometricJacobiArea a c t-1)/t^2)) := by
    apply Filter.Eventually.of_forall
    intro t
    simp only [opticalScreenClausiusDefect,horizonBalancePrimitive,optical_equilibrium_area,
      geometric_jacobi_area_zero]
    ring
  exact (tendsto_congr' he).2 h

/-- The geometric construction does not erase the independent matching condition. -/
theorem optical_screen_quadratic_balance_iff (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hrate : rate≠0) :
    Tendsto (fun t => opticalScreenClausiusDefect a c ha hc rate mass eta t/t^2)
      (𝓝[<] 0) (𝓝 0) ↔ eta*(a+c)=2*Real.pi*mass := by
  constructor
  · intro hz
    have h := tendsto_nhds_unique
      (optical_screen_clausius_quadratic_limit a c ha hc rate mass eta) hz
    have hm := congrArg (fun y : ℝ => y*(4*Real.pi)) h
    rw [div_mul_cancel₀ _ (mul_ne_zero (by norm_num) Real.pi_ne_zero),zero_mul] at hm
    exact sub_eq_zero.mp ((mul_eq_zero.mp hm).resolve_left hrate)
  · intro hmatch
    simpa only [hmatch,sub_self,mul_zero,zero_div] using
      optical_screen_clausius_quadratic_limit a c ha hc rate mass eta

theorem optical_screen_clausius_quartic_limit (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    Tendsto (fun t => opticalScreenClausiusDefect a c ha hc rate mass eta t/t^4)
      (𝓝[<] 0) (𝓝 (rate*eta*(a^2+c^2)/(24*Real.pi))) := by
  have h := (optical_clausius_quartic_limit a c rate mass eta ha hc hmatch).mono_left
    (nhdsWithin_mono 0 (fun _ ht => ne_of_lt ht))
  have he : (fun t => opticalScreenClausiusDefect a c ha hc rate mass eta t/t^4) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => opticalClausiusDefect a c rate mass eta t/t^4) := by
    filter_upwards [optical_screen_clausius_germ a c ha hc rate mass eta] with t ht
    rw [ht]
  exact (tendsto_congr' he).2 h

theorem optical_screen_clausius_eventually_positive (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hrate : 0<rate) (heta : 0<eta)
    (hcurvature : 0<a+c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), 0<opticalScreenClausiusDefect a c ha hc rate mass eta t := by
  have hp := (optical_clausius_eventually_positive a c rate mass eta
    ha hc hrate heta hcurvature hmatch).filter_mono
      (nhdsWithin_mono 0 (fun _ ht => ne_of_lt ht))
  filter_upwards [optical_screen_clausius_germ a c ha hc rate mass eta,hp] with t ht hpos
  rw [ht]
  exact hpos

theorem optical_screen_clausius_not_eventually_zero (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (rate mass eta : ℝ) (hrate : 0<rate) (heta : 0<eta)
    (hcurvature : 0<a+c) (hmatch : eta*(a+c)=2*Real.pi*mass) :
    ¬ ∀ᶠ t in 𝓝[<] (0:ℝ), opticalScreenClausiusDefect a c ha hc rate mass eta t=0 := by
  intro hz
  have hp := optical_screen_clausius_eventually_positive a c ha hc rate mass eta
    hrate heta hcurvature hmatch
  obtain ⟨t,ht,hzero⟩ := (hp.and hz).exists
  exact (ne_of_gt ht) hzero

/-- Geometry exists in this flat control, while nonzero matter forbids quadratic balance. -/
theorem flat_screen_not_quadratically_balanced (rate mass eta : ℝ)
    (hrate : rate≠0) (hmass : mass≠0) :
    ¬ Tendsto (fun t => opticalScreenClausiusDefect 0 0 (by norm_num) (by norm_num)
      rate mass eta t/t^2) (𝓝[<] 0) (𝓝 0) := by
  intro h
  have hm := (optical_screen_quadratic_balance_iff 0 0 (by norm_num) (by norm_num)
    rate mass eta hrate).1 h
  exact hmass (flat_matching_forces_zero_mass eta mass hm)

theorem optical_equilibrium_flat_area (t : ℝ) :
    inducedArea (frameMetricField (waveSolder 0 0))
      (opticalEquilibriumScreen 0 0 (by norm_num) (by norm_num)).curve
      (opticalEquilibriumScreen 0 0 (by norm_num) (by norm_num)).screen.vectors t=1 := by
  rw [optical_equilibrium_area,geometric_jacobi_area_abs]
  simp [opticalJacobiArea,jacobiOscillator]

#print axioms past_integral_original_germ
#print axioms optical_screen_heat_flux
#print axioms opticalScreenHeat
#print axioms optical_screen_heat_germ
#print axioms optical_screen_heat_zero
#print axioms optical_screen_heat_quadratic_limit
#print axioms opticalScreenClausiusDefect
#print axioms optical_screen_clausius_germ
#print axioms optical_screen_clausius_quadratic_limit
#print axioms optical_screen_quadratic_balance_iff
#print axioms optical_screen_clausius_quartic_limit
#print axioms optical_screen_clausius_eventually_positive
#print axioms optical_screen_clausius_not_eventually_zero
#print axioms flat_screen_not_quadratically_balanced
#print axioms optical_equilibrium_flat_area
end
end ChatgptAudit.Optical043
