import SchwartzRestrictionMomentsR1

/-! All quadratic energy moments of the same Schwartz restriction. L1 moments
alone give pointwise waves; these L2 moments also control finite kinetic energy. -/
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

theorem weighted_restriction_square_moment_decay (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (hwp : ∀ x,0≤w x) (m n : ℕ) (x : X) :
    ‖x‖^n*(w x^m*‖f (j x)‖^2) ≤
      C^m*SchwartzMap.seminorm ℝ (n+m) 0 f*SchwartzMap.seminorm ℝ 0 0 f := by
  have h:=mul_le_mul (weighted_restriction_moment_decay f j w hC hj hw hwp m n x)
    (f.norm_le_seminorm ℝ (j x)) (norm_nonneg _)
    (mul_nonneg (pow_nonneg hC _) (apply_nonneg _ _))
  calc
    _ = (‖x‖^n*(w x^m*‖f (j x)‖))*‖f (j x)‖ := by ring
    _ ≤ _ := h

theorem energy_moment_square_restriction_integrable (f : 𝓢(E,V)) (j : X→E) (w : X→ℝ)
    {C : ℝ} (hC : 0≤C) (hj : ∀ x,‖x‖≤‖j x‖) (hw : ∀ x,w x≤C*‖x‖)
    (hwp : ∀ x,0≤w x) (hjm : Measurable j) (hwm : Measurable w) (m : ℕ) :
    Integrable (fun x=>w x^m*‖f (j x)‖^2) μ := by
  have hn (x : X) : ‖w x^m*‖f (j x)‖^2‖=w x^m*‖f (j x)‖^2 :=
    Real.norm_of_nonneg (mul_nonneg (pow_nonneg (hwp x) _) (sq_nonneg _))
  have hm : AEStronglyMeasurable (fun x=>w x^m*‖f (j x)‖^2) μ :=
    ((hwm.pow_const m).mul ((f.continuous.measurable.comp hjm).norm.pow_const 2)).aestronglyMeasurable
  have hi:=integrable_of_le_of_pow_mul_le (μ:=μ) (k:=0)
    (f:=fun x=>w x^m*‖f (j x)‖^2)
    (fun x=>by simpa [hn x] using weighted_restriction_square_moment_decay f j w hC hj hw hwp m 0 x)
    (fun x=>by simpa [hn x] using weighted_restriction_square_moment_decay f j w hC hj hw hwp m μ.integrablePower x) hm
  simpa only [pow_zero,one_mul,hn] using hi
end F1Fecho.SchwartzRestriction
#print axioms F1Fecho.SchwartzRestriction.weighted_restriction_square_moment_decay
#print axioms F1Fecho.SchwartzRestriction.energy_moment_square_restriction_integrable
