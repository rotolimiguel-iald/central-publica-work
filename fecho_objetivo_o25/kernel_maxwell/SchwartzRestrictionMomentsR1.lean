import SchwartzRestrictionEstimateR2

/-! Every nonnegative integer energy moment of a proper Schwartz restriction is
integrable. This supplies a regular, concrete domain for pointwise wave kernels. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.SchwartzRestriction
open MeasureTheory SchwartzMap
variable {X E V : Type*}
  [NormedAddCommGroup X] [NormedSpace ℝ X] [MeasurableSpace X] [BorelSpace X]
  [SecondCountableTopology X] {μ : Measure X} [μ.HasTemperateGrowth]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup V] [NormedSpace ℝ V] [MeasurableSpace V] [BorelSpace V]

theorem weighted_restriction_moment_decay (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (hwp : ∀ x,0≤w x) (m n : ℕ) (x : X) :
    ‖x‖^n*(w x^m*‖f (j x)‖) ≤ C^m*SchwartzMap.seminorm ℝ (n+m) 0 f := by
  have hp : ‖x‖^(n+m)*‖f (j x)‖≤SchwartzMap.seminorm ℝ (n+m) 0 f :=
    (mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) (hj x) _) (norm_nonneg _)).trans
      (f.norm_pow_mul_le_seminorm ℝ (n+m) (j x))
  calc
    _ ≤ ‖x‖^n*((C*‖x‖)^m*‖f (j x)‖) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_right
        (pow_le_pow_left₀ (hwp x) (hw x) m) (norm_nonneg _)) (by positivity)
    _ = C^m*(‖x‖^(n+m)*‖f (j x)‖) := by rw [mul_pow,pow_add]; ring
    _ ≤ _ := mul_le_mul_of_nonneg_left hp (by positivity)

theorem energy_moment_restriction_integrable (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (hwp : ∀ x,0≤w x) (hjm : Measurable j) (hwm : Measurable w) (m : ℕ) :
    Integrable (fun x=>w x^m*‖f (j x)‖) μ := by
  have hn (x : X) : ‖w x^m*‖f (j x)‖‖=w x^m*‖f (j x)‖ :=
    Real.norm_of_nonneg (mul_nonneg (pow_nonneg (hwp x) _) (norm_nonneg _))
  have hm : AEStronglyMeasurable (fun x=>w x^m*‖f (j x)‖) μ :=
    ((hwm.pow_const m).mul (f.continuous.measurable.comp hjm).norm).aestronglyMeasurable
  have hi:=integrable_of_le_of_pow_mul_le (μ:=μ) (k:=0)
    (f:=fun x=>w x^m*‖f (j x)‖)
    (fun x=>by simpa [hn x] using weighted_restriction_moment_decay f j w hC hj hw hwp m 0 x)
    (fun x=>by simpa [hn x] using weighted_restriction_moment_decay f j w hC hj hw hwp m μ.integrablePower x) hm
  simpa only [pow_zero,one_mul,hn] using hi
end F1Fecho.SchwartzRestriction
#print axioms F1Fecho.SchwartzRestriction.weighted_restriction_moment_decay
#print axioms F1Fecho.SchwartzRestriction.energy_moment_restriction_integrable
