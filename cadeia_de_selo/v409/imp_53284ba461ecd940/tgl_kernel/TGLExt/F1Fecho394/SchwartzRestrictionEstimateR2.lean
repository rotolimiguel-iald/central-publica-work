import Mathlib.Analysis.Distribution.SchwartzSpace.Basic

/-! A proper measurable restriction of a Schwartz function has an integrable
energy-weighted square when the energy grows at most linearly. The hypotheses
are geometric estimates on the restriction, not an integrability assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.SchwartzRestriction
open MeasureTheory SchwartzMap
variable {X E V : Type*}
  [NormedAddCommGroup X] [NormedSpace ℝ X] [MeasurableSpace X] [BorelSpace X]
  [SecondCountableTopology X] {μ : Measure X} [μ.HasTemperateGrowth]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup V] [NormedSpace ℝ V] [MeasurableSpace V] [BorelSpace V]

theorem weighted_restriction_decay (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (n : ℕ) (x : X) :
    ‖x‖^n*(w x*‖f (j x)‖^2) ≤
      C*(SchwartzMap.seminorm ℝ (n+1) 0 f)*(SchwartzMap.seminorm ℝ 0 0 f) := by
  have hN := f.norm_pow_mul_le_seminorm ℝ (n+1) (j x)
  have h0 := f.norm_le_seminorm ℝ (j x)
  have hp : ‖x‖^(n+1)*‖f (j x)‖≤SchwartzMap.seminorm ℝ (n+1) 0 f :=
    (mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) (hj x) _) (norm_nonneg _)).trans hN
  calc
    ‖x‖^n*(w x*‖f (j x)‖^2) ≤ ‖x‖^n*((C*‖x‖)*‖f (j x)‖^2) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right (hw x) (sq_nonneg _)) (by positivity)
    _ = C*(‖x‖^(n+1)*‖f (j x)‖)*‖f (j x)‖ := by rw [pow_succ]; ring
    _ ≤ C*(SchwartzMap.seminorm ℝ (n+1) 0 f)*(SchwartzMap.seminorm ℝ 0 0 f) := by
      exact mul_le_mul (mul_le_mul_of_nonneg_left hp hC) h0 (norm_nonneg _)
        (mul_nonneg hC (apply_nonneg _ _))

theorem energy_weighted_square_integrable (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (hwp : ∀ x,0≤w x) (hjm : Measurable j) (hwm : Measurable w) :
    Integrable (fun x => w x*‖f (j x)‖^2) μ := by
  have hn (x : X) : ‖w x*‖f (j x)‖^2‖=w x*‖f (j x)‖^2 :=
    Real.norm_of_nonneg (mul_nonneg (hwp x) (sq_nonneg _))
  have hmeas : AEStronglyMeasurable (fun x => w x*‖f (j x)‖^2) μ :=
    (hwm.mul ((f.continuous.measurable.comp hjm).norm.pow_const 2)).aestronglyMeasurable
  have hi := integrable_of_le_of_pow_mul_le (μ:=μ) (k:=0)
    (f:=fun x => w x*‖f (j x)‖^2)
    (fun x => by simpa [hn x] using weighted_restriction_decay f j w hC hj hw 0 x)
    (fun x => by simpa [hn x] using weighted_restriction_decay f j w hC hj hw μ.integrablePower x)
    hmeas
  simpa only [pow_zero,one_mul,hn] using hi

end F1Fecho.SchwartzRestriction
#print axioms F1Fecho.SchwartzRestriction.weighted_restriction_decay
#print axioms F1Fecho.SchwartzRestriction.energy_weighted_square_integrable
