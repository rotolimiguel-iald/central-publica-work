import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Topology.MetricSpace.Pseudo.Basic
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.CutoffDerivative
open Filter Topology
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem slope_norm_error_le (f g : ℝ → E) (e : ℝ) (he : 0 ≤ e)
    (hzero : g 0 = f 0) (hbound : ∀ t : ℝ, ‖f t-g t‖ ≤ |t| * e) (t : ℝ) :
    ‖slope f 0 t-slope g 0 t‖ ≤ e := by
  by_cases ht : t = 0
  · subst t
    simpa only [slope_def_module,sub_zero,inv_zero,zero_smul,sub_self,norm_zero] using he
  have hdiff : (f t-f 0)-(g t-g 0)=f t-g t := by
    rw [hzero]
    abel
  simp only [slope_def_module,sub_zero,←smul_sub,hdiff,norm_smul,norm_inv,Real.norm_eq_abs]
  calc
    |t|⁻¹ * ‖f t-g t‖ ≤ |t|⁻¹ * (|t| * e) :=
      mul_le_mul_of_nonneg_left (hbound t) (inv_nonneg.mpr (abs_nonneg t))
    _ = e := by rw [←mul_assoc,inv_mul_cancel₀ (abs_ne_zero.mpr ht),one_mul]

theorem hasDerivAt_of_linear_cutoff_error
    (f : ℝ → E) (fN : ℕ → ℝ → E) (dN : ℕ → E) (d : E) (e : ℕ → ℝ)
    (hzero : ∀ N, fN N 0=f 0)
    (hderiv : ∀ N, HasDerivAt (fN N) (dN N) 0)
    (hd : Tendsto dN atTop (𝓝 d))
    (he : ∀ N, 0≤e N) (he0 : Tendsto e atTop (𝓝 0))
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) :
    HasDerivAt f d 0 := by
  apply hasDerivAt_iff_tendsto_slope.mpr
  apply Metric.tendsto_nhds.mpr
  intro ε hε
  have hthird : 0<ε/3 := by positivity
  have hev := he0.eventually (gt_mem_nhds hthird)
  have hdv := Metric.tendsto_nhds.mp hd (ε/3) hthird
  obtain ⟨N,heN,hdN⟩ := (hev.and hdv).exists
  have hsv := Metric.tendsto_nhds.mp (hderiv N).tendsto_slope (ε/3) hthird
  filter_upwards [hsv] with t ht
  have herr : dist (slope f 0 t) (slope (fN N) 0 t)≤e N := by
    rw [dist_eq_norm]
    exact slope_norm_error_le f (fN N) (e N) (he N) (hzero N) (hbound N) t
  have h1 := dist_triangle (slope f 0 t) (slope (fN N) 0 t) d
  have h2 := dist_triangle (slope (fN N) 0 t) (dN N) d
  linarith

omit [NormedSpace ℝ E] in
theorem cutoff_base_value_eq (f : ℝ → E) (fN : ℕ → ℝ → E) (e : ℕ → ℝ)
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) (N : ℕ) :
    fN N 0=f 0 := by
  have hb := hbound N 0
  simp only [abs_zero,zero_mul] at hb
  exact (sub_eq_zero.mp (norm_eq_zero.mp (le_antisymm hb (norm_nonneg _)))).symm

theorem hasDerivAt_of_linear_cutoff_error_auto_base
    (f : ℝ → E) (fN : ℕ → ℝ → E) (dN : ℕ → E) (d : E) (e : ℕ → ℝ)
    (hderiv : ∀ N, HasDerivAt (fN N) (dN N) 0)
    (hd : Tendsto dN atTop (𝓝 d))
    (he : ∀ N, 0≤e N) (he0 : Tendsto e atTop (𝓝 0))
    (hbound : ∀ N t, ‖f t-fN N t‖≤ |t| * e N) :
    HasDerivAt f d 0 :=
  hasDerivAt_of_linear_cutoff_error f fN dN d e
    (cutoff_base_value_eq f fN e hbound) hderiv hd he he0 hbound

#print axioms slope_norm_error_le
#print axioms hasDerivAt_of_linear_cutoff_error
#print axioms cutoff_base_value_eq
#print axioms hasDerivAt_of_linear_cutoff_error_auto_base
end
end ChatgptAudit.CutoffDerivative
