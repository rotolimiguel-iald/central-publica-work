import JointUnitaryPreparation

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.StaticDynamic
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.JointUnitary
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

def mixedWeights (q : ι → ℝ) (r : κ → ℝ) : ι ⊕ κ → ℝ :=
  Sum.elim (fun i => (1/2 : ℝ) * q i) (fun j => (1/2 : ℝ) * r j)

theorem mixed_weights_normalized (q : ι → ℝ) (r : κ → ℝ)
    (hq : ∑ i, q i = 1) (hr : ∑ j, r j = 1) :
    ∑ k, mixedWeights q r k = 1 := by
  simp only [mixedWeights, Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr,
    ← Finset.mul_sum, hq, hr]
  norm_num

theorem mixed_weights_positive (q : ι → ℝ) (r : κ → ℝ)
    (hq : ∀ i, 0 < q i) (hr : ∀ j, 0 < r j) :
    ∀ k, 0 < mixedWeights q r k := by
  intro k
  cases k with
  | inl i => exact mul_pos (by norm_num) (hq i)
  | inr j => exact mul_pos (by norm_num) (hr j)

theorem mixed_static_readout (q : ι → ℝ) (r : κ → ℝ) (i : ι) :
    2 * mixedWeights q r (Sum.inl i) = q i := by
  simp only [mixedWeights, Sum.elim_inl]
  ring

theorem mixed_dynamic_readout (q : ι → ℝ) (r : κ → ℝ) (j : κ) :
    2 * mixedWeights q r (Sum.inr j) = r j := by
  simp only [mixedWeights, Sum.elim_inr]
  ring

theorem dilation_tendsto_past :
    Tendsto (fun t : ℝ => Real.sqrt 2 * t) (𝓝[<] 0) (𝓝[<] 0) := by
  apply tendsto_nhdsWithin_iff.mpr
  constructor
  · have h : Tendsto (fun t : ℝ => Real.sqrt 2 * t) (𝓝 0) (𝓝 (Real.sqrt 2 * 0)) :=
      tendsto_const_nhds.mul tendsto_id
    simpa only [mul_zero] using h.mono_left nhdsWithin_le_nhds
  · filter_upwards [self_mem_nhdsWithin] with t ht
    exact mul_neg_of_pos_of_neg (Real.sqrt_pos.2 (by norm_num)) ht

theorem dilated_weight_derivative {p : κ → ℝ} (X : DiagonalStateCurve p)
    (t : ℝ) (j : κ)
    (hd : HasDerivAt (fun s => X.weights s j) (X.tangent (Real.sqrt 2*t) j) (Real.sqrt 2*t)) :
    HasDerivAt (fun s => (1/2 : ℝ) * X.weights (Real.sqrt 2*s) j)
      ((1/2 : ℝ) * (X.tangent (Real.sqrt 2*t) j * Real.sqrt 2)) t := by
  simpa only [mul_one] using
    (hd.comp t ((hasDerivAt_id t).const_mul (Real.sqrt 2))).const_mul (1/2 : ℝ)

def mixedCurve (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) : DiagonalStateCurve (mixedWeights q p) where
  weights := fun t => mixedWeights q (X.weights (Real.sqrt 2*t))
  tangent := fun t => Sum.elim (fun _ => 0)
    (fun j => (1/2 : ℝ) * (X.tangent (Real.sqrt 2*t) j * Real.sqrt 2))
  at_zero := by
    intro k
    cases k <;> simp only [mixedWeights, Sum.elim_inl, Sum.elim_inr, mul_zero, X.at_zero]
  trace_one := fun t => mixed_weights_normalized q _ hq (X.trace_one _)
  derivative_zero := by
    intro k
    cases k with
    | inl i => exact hasDerivAt_const 0 _
    | inr j =>
      exact dilated_weight_derivative X 0 j
        (by simpa only [mul_zero] using X.derivative_zero j)
  derivative_past := by
    filter_upwards [dilation_tendsto_past.eventually X.derivative_past] with t ht
    intro k
    cases k with
    | inl i => exact hasDerivAt_const t _
    | inr j => exact dilated_weight_derivative X t j (ht j)
  tangent_continuous := by
    intro k
    cases k with
    | inl i => exact continuousAt_const
    | inr j =>
      have h : ContinuousAt (fun t : ℝ => Real.sqrt 2*t) 0 :=
        continuousAt_const.mul continuousAt_id
      have ht : ContinuousAt (fun t => X.tangent t j) (Real.sqrt 2*0) := by
        simpa only [mul_zero] using X.tangent_continuous j
      exact continuousAt_const.mul ((ht.comp h).mul continuousAt_const)

theorem mixed_curve_positive_near (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p)
    (hqp : ∀ i, 0 < q i) (hpp : ∀ j, 0 < p j) :
    ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k, 0 < (mixedCurve q hq X).weights t k :=
  state_curve_positive_near (mixedCurve q hq X) (mixed_weights_positive q p hqp hpp)

theorem mixed_tangent_zero (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) (hz : X.tangent 0 = 0) :
    (mixedCurve q hq X).tangent 0 = 0 := by
  funext k
  cases k <;> simp only [mixedCurve, Sum.elim_inl, Sum.elim_inr, mul_zero, hz,
    Pi.zero_apply, zero_mul]

theorem finite_entropy_scaled {ν : Type} [Fintype ν]
    (r : ν → ℝ) (hr : ∑ j, r j = 1) (a : ℝ) :
    finiteEntropy (fun j => a*r j) = a*finiteEntropy r - a*Real.log a := by
  simp only [finiteEntropy, entropy_atom_scaled, Finset.sum_sub_distrib,
    ← Finset.mul_sum, ← Finset.sum_mul, hr, mul_one]

theorem mixed_entropy (q : ι → ℝ) (r : κ → ℝ)
    (hq : ∑ i, q i = 1) (hr : ∑ j, r j = 1) :
    finiteEntropy (mixedWeights q r) =
      (1/2 : ℝ)*finiteEntropy q + (1/2 : ℝ)*finiteEntropy r - Real.log (1/2 : ℝ) := by
  have he : finiteEntropy (mixedWeights q r) =
      finiteEntropy (fun i => (1/2 : ℝ)*q i) + finiteEntropy (fun j => (1/2 : ℝ)*r j) := by
    simp only [finiteEntropy, mixedWeights, Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr]
  rw [he, finite_entropy_scaled q hq, finite_entropy_scaled r hr]
  ring

theorem mixed_entropy_increment (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) (t : ℝ) :
    finiteEntropy ((mixedCurve q hq X).weights t) - finiteEntropy (mixedWeights q p) =
      (1/2 : ℝ)*(finiteEntropy (X.weights (Real.sqrt 2*t)) - finiteEntropy p) := by
  change finiteEntropy (mixedWeights q (X.weights (Real.sqrt 2*t))) - _ = _
  rw [mixed_entropy q _ hq (X.trace_one _),
    mixed_entropy q p hq (state_curve_base_normalized X)]
  ring

theorem modular_scaled {ν : Type} [Fintype ν]
    (p r : ν → ℝ) (hp : ∀ j, 0 < p j)
    (hnp : ∑ j, p j = 1) (hnr : ∑ j, r j = 1) :
    modularIncrement (fun j => (1/2 : ℝ)*p j) (fun j => (1/2 : ℝ)*r j) =
      (1/2 : ℝ)*modularIncrement p r := by
  have term (j : ν) :
      -((1/2 : ℝ)*r j-(1/2 : ℝ)*p j)*Real.log ((1/2 : ℝ)*p j) =
      (1/2 : ℝ)*(-(r j-p j)*Real.log (p j)) -
        (1/2 : ℝ)*(r j-p j)*Real.log (1/2 : ℝ) := by
    rw [Real.log_mul (by norm_num : (1/2 : ℝ) ≠ 0) (ne_of_gt (hp j))]
    ring
  simp only [modularIncrement, term, Finset.sum_sub_distrib, ← Finset.mul_sum,
    ← Finset.sum_mul, hnr, hnp, sub_self, mul_zero, zero_mul, sub_zero]

theorem mixed_modular_increment (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) (hp : ∀ j, 0 < p j) (t : ℝ) :
    modularIncrement (mixedWeights q p) ((mixedCurve q hq X).weights t) =
      (1/2 : ℝ)*modularIncrement p (X.weights (Real.sqrt 2*t)) := by
  have he : modularIncrement (mixedWeights q p) ((mixedCurve q hq X).weights t) =
      modularIncrement (fun j => (1/2 : ℝ)*p j)
        (fun j => (1/2 : ℝ)*X.weights (Real.sqrt 2*t) j) := by
    simp only [modularIncrement, mixedCurve, mixedWeights, Fintype.sum_sum_type,
      Sum.elim_inl, Sum.elim_inr, sub_self, neg_zero, zero_mul, Finset.sum_const_zero, zero_add]
  rw [he]
  exact modular_scaled p _ hp (state_curve_base_normalized X) (X.trace_one _)

theorem dilated_quadratic_preserved (f : ℝ → ℝ) (c : ℝ)
    (hf : Tendsto (fun t => f t/t^2) (𝓝[<] 0) (𝓝 c)) :
    Tendsto (fun t => ((1/2 : ℝ)*f (Real.sqrt 2*t))/t^2) (𝓝[<] 0) (𝓝 c) := by
  have he : (fun t => ((1/2 : ℝ)*f (Real.sqrt 2*t))/t^2) =
      (fun t => f (Real.sqrt 2*t)/(Real.sqrt 2*t)^2) := by
    funext t
    rw [mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    ring
  rw [he]
  exact hf.comp dilation_tendsto_past

theorem mixed_entropy_quadratic_limit (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) (c : ℝ)
    (h : Tendsto (fun t => (finiteEntropy (X.weights t)-finiteEntropy p)/t^2)
      (𝓝[<] 0) (𝓝 c)) :
    Tendsto (fun t => (finiteEntropy ((mixedCurve q hq X).weights t)-
      finiteEntropy (mixedWeights q p))/t^2) (𝓝[<] 0) (𝓝 c) := by
  simp only [mixed_entropy_increment]
  exact dilated_quadratic_preserved _ c h

theorem mixed_modular_quadratic_limit (q : ι → ℝ) (hq : ∑ i, q i = 1)
    {p : κ → ℝ} (X : DiagonalStateCurve p) (hp : ∀ j, 0 < p j) (c : ℝ)
    (h : Tendsto (fun t => modularIncrement p (X.weights t)/t^2)
      (𝓝[<] 0) (𝓝 c)) :
    Tendsto (fun t => modularIncrement (mixedWeights q p)
      ((mixedCurve q hq X).weights t)/t^2) (𝓝[<] 0) (𝓝 c) := by
  simp only [mixed_modular_increment q hq X hp]
  exact dilated_quadratic_preserved _ c h

theorem mixed_joint_entropy_limit (q : ι → ℝ) (hq : ∑ i, q i = 1)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) :
    Tendsto (fun t => (finiteEntropy ((mixedCurve q hq
      (jointUnitaryCurve C frequency)).weights t)-finiteEntropy (mixedWeights q (jointBase C)))/t^2)
      (𝓝[<] 0) (𝓝 (jointResponse C frequency)) :=
  mixed_entropy_quadratic_limit q hq (jointUnitaryCurve C frequency) (jointResponse C frequency)
    (joint_entropy_quadratic_limit C frequency)

theorem mixed_joint_modular_limit (q : ι → ℝ) (hq : ∑ i, q i = 1)
    (C : UnitaryLabelData κ) (frequency : κ → ℝ) :
    Tendsto (fun t => modularIncrement (mixedWeights q (jointBase C))
      ((mixedCurve q hq (jointUnitaryCurve C frequency)).weights t)/t^2)
      (𝓝[<] 0) (𝓝 (jointResponse C frequency)) :=
  mixed_modular_quadratic_limit q hq (jointUnitaryCurve C frequency) (joint_base_positive C)
    (jointResponse C frequency) (joint_modular_quadratic_limit C frequency)

#print axioms mixedWeights
#print axioms mixed_weights_normalized
#print axioms mixed_weights_positive
#print axioms mixed_static_readout
#print axioms mixed_dynamic_readout
#print axioms dilation_tendsto_past
#print axioms dilated_weight_derivative
#print axioms mixedCurve
#print axioms mixed_curve_positive_near
#print axioms mixed_tangent_zero
#print axioms finite_entropy_scaled
#print axioms mixed_entropy
#print axioms mixed_entropy_increment
#print axioms modular_scaled
#print axioms mixed_modular_increment
#print axioms dilated_quadratic_preserved
#print axioms mixed_entropy_quadratic_limit
#print axioms mixed_modular_quadratic_limit
#print axioms mixed_joint_entropy_limit
#print axioms mixed_joint_modular_limit
end
end ChatgptAudit.StaticDynamic
