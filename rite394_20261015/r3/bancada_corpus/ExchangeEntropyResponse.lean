import UnitaryEntropyResponse

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Exchange055
open TGLExt Matrix Filter Topology Set
open ChatgptAudit ChatgptAudit.Micro021 ChatgptAudit.Unitary022
noncomputable section

/-- The zero-level weight after the two-site exchange protocol. -/
def exchangeWeight (p q t : ℝ) : ℝ := p + (q-p)*Real.sin t^2

/-- The change of the mean energy with levels zero and one. -/
def exchangeHeat (p q t : ℝ) : ℝ := (p-q)*Real.sin t^2

/-- The dimensionless modular energy gap of the faithful Bernoulli reference. -/
def exchangeModularGap (p : ℝ) : ℝ := Real.log p-Real.log (1-p)

/-- The sum of the two regional modular response coefficients. -/
def exchangeCostCoefficient (p q : ℝ) : ℝ :=
  (p-q)*(exchangeModularGap p-exchangeModularGap q)

theorem exchange_weight_zero (p q : ℝ) : exchangeWeight p q 0=p := by
  simp [exchangeWeight]

theorem exchange_weight_convex (p q t : ℝ) :
    exchangeWeight p q t=p*Real.cos t^2+q*Real.sin t^2 := by
  have hc : Real.cos t^2=1-Real.sin t^2 := by
    nlinarith only [Real.sin_sq_add_cos_sq t]
  rw [hc]
  unfold exchangeWeight
  ring

theorem exchange_weight_complement (p q t : ℝ) :
    1-exchangeWeight p q t=exchangeWeight (1-p) (1-q) t := by
  unfold exchangeWeight
  ring

theorem exchange_weight_min_le (p q t : ℝ) : min p q≤exchangeWeight p q t := by
  rcases le_total p q with hpq|hqp
  · rw [min_eq_left hpq]
    exact le_add_of_nonneg_right (mul_nonneg (sub_nonneg.mpr hpq) (sq_nonneg _))
  · rw [min_eq_right hqp]
    have hs : Real.sin t^2≤1 := by
      nlinarith only [Real.sin_sq_add_cos_sq t, sq_nonneg (Real.cos t)]
    have h := mul_nonneg (sub_nonneg.mpr hqp) (sub_nonneg.mpr hs)
    unfold exchangeWeight
    nlinarith only [h]

theorem exchange_weight_pos (p q : ℝ) (hp : 0<p) (hq : 0<q) (t : ℝ) :
    0<exchangeWeight p q t :=
  lt_of_lt_of_le (lt_min hp hq) (exchange_weight_min_le p q t)

theorem exchange_weight_lt_one (p q : ℝ) (hp : p<1) (hq : q<1) (t : ℝ) :
    exchangeWeight p q t<1 := by
  have h := exchange_weight_pos (1-p) (1-q) (by linarith) (by linarith) t
  rw [←exchange_weight_complement] at h
  linarith

theorem exchange_weights_positive (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) (t : ℝ) :
    ∀ i, 0<siteW (exchangeWeight p q t) i :=
  siteW_pos (exchange_weight_pos p q hp0 hq0 t)
    (exchange_weight_lt_one p q hp1 hq1 t)

theorem exchange_weights_normalized (p q t : ℝ) :
    ∑ i, siteW (exchangeWeight p q t) i=1 := siteW_sum _

theorem exchange_heat_eq_displacement (p q t : ℝ) :
    exchangeHeat p q t=p-exchangeWeight p q t := by
  unfold exchangeHeat exchangeWeight
  ring

theorem exchange_heat_antisymmetric (p q t : ℝ) :
    exchangeHeat q p t= -exchangeHeat p q t := by
  unfold exchangeHeat
  ring

theorem exchange_heat_conserved (p q t : ℝ) :
    exchangeHeat p q t+exchangeHeat q p t=0 := by
  rw [exchange_heat_antisymmetric]
  ring

theorem exchange_weight_derivative (p q t : ℝ) :
    HasDerivAt (exchangeWeight p q) (2*(q-p)*Real.sin t*Real.cos t) t := by
  have h := (((Real.hasDerivAt_sin t).pow 2).const_mul (q-p)).const_add p
  convert h using 1 <;> first | rfl | ring

theorem exchange_heat_derivative (p q t : ℝ) :
    HasDerivAt (exchangeHeat p q) (2*(p-q)*Real.sin t*Real.cos t) t := by
  have h := ((Real.hasDerivAt_sin t).pow 2).const_mul (p-q)
  convert h using 1 <;> first | rfl | ring

/-- Both coordinates of the derivative of the Bernoulli distribution. -/
def exchangeTangent (p q t : ℝ) (i : Fin 2) : ℝ :=
  if i=0 then 2*(q-p)*Real.sin t*Real.cos t else -(2*(q-p)*Real.sin t*Real.cos t)

theorem exchange_weights_derivative (p q t : ℝ) (i : Fin 2) :
    HasDerivAt (fun s => siteW (exchangeWeight p q s) i) (exchangeTangent p q t i) t := by
  fin_cases i
  · simpa [siteW, exchangeTangent] using exchange_weight_derivative p q t
  · simpa [siteW, exchangeTangent] using (exchange_weight_derivative p q t).const_sub 1

theorem exchange_tangent_zero (p q : ℝ) : exchangeTangent p q 0=0 := by
  ext i
  simp [exchangeTangent]

/-- The existing finite-state curve contract, instantiated by the exchange weights. -/
def exchangeStateCurve (p q : ℝ) : DiagonalStateCurve (siteW p) where
  weights t := siteW (exchangeWeight p q t)
  tangent := exchangeTangent p q
  at_zero i := by rw [exchange_weight_zero]
  trace_one t := exchange_weights_normalized p q t
  derivative_zero i := exchange_weights_derivative p q 0 i
  derivative_past := Filter.Eventually.of_forall (fun t i => exchange_weights_derivative p q t i)
  tangent_continuous i := by
    unfold exchangeTangent
    split_ifs <;> fun_prop

theorem exchange_modular_increment (p q t : ℝ) :
    modularIncrement (siteW p) (siteW (exchangeWeight p q t))=
      exchangeModularGap p*exchangeHeat p q t := by
  norm_num [modularIncrement, Fin.sum_univ_two, siteW, exchangeWeight,
    exchangeHeat, exchangeModularGap]
  ring

/-- Exact regional entropy identity; faithfulness is needed for its state interpretation. -/
theorem exchange_first_law (p q t : ℝ) :
    finiteEntropy (siteW (exchangeWeight p q t))-finiteEntropy (siteW p)=
      exchangeModularGap p*exchangeHeat p q t-
        diagonalRelativeEntropy (siteW (exchangeWeight p q t)) (siteW p) := by
  have h := relative_entropy_identity (siteW (exchangeWeight p q t)) (siteW p)
  rw [exchange_modular_increment] at h
  linarith

theorem exchange_relative_quadratic_zero (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) :
    Tendsto (fun t => diagonalRelativeEntropy (siteW (exchangeWeight p q t)) (siteW p)/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  have hp : ∀ i, 0<siteW p i := by
    simpa only [exchange_weight_zero] using exchange_weights_positive p q hp0 hp1 hq0 hq1 0
  apply (relative_entropy_quadratic_zero_iff (exchangeStateCurve p q) hp).mpr
  exact exchange_tangent_zero p q

theorem exchange_sin_square_limit :
    Tendsto (fun t : ℝ => Real.sin t^2/t^2) (𝓝[<] 0) (𝓝 1) := by
  simpa only [one_mul, one_pow] using frequency_sin_square_limit 1

theorem exchange_heat_quadratic_limit (p q : ℝ) :
    Tendsto (fun t => exchangeHeat p q t/t^2) (𝓝[<] 0) (𝓝 (p-q)) := by
  simpa only [exchangeHeat, mul_div_assoc, mul_one] using
    exchange_sin_square_limit.const_mul (p-q)

theorem exchange_modular_quadratic_limit (p q : ℝ) :
    Tendsto (fun t => modularIncrement (siteW p) (siteW (exchangeWeight p q t))/t^2)
      (𝓝[<] 0) (𝓝 (exchangeModularGap p*(p-q))) := by
  have h := (exchange_heat_quadratic_limit p q).const_mul (exchangeModularGap p)
  have he : (fun t => modularIncrement (siteW p) (siteW (exchangeWeight p q t))/t^2)=
      (fun t => exchangeModularGap p*(exchangeHeat p q t/t^2)) := by
    funext t
    rw [exchange_modular_increment]
    ring
  rw [he]
  exact h

theorem exchange_entropy_quadratic_limit (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) :
    Tendsto (fun t => (finiteEntropy (siteW (exchangeWeight p q t))-finiteEntropy (siteW p))/t^2)
      (𝓝[<] 0) (𝓝 (exchangeModularGap p*(p-q))) := by
  have h := ((exchange_heat_quadratic_limit p q).const_mul (exchangeModularGap p)).sub
    (exchange_relative_quadratic_zero p q hp0 hp1 hq0 hq1)
  have he :
      (fun t => (finiteEntropy (siteW (exchangeWeight p q t))-finiteEntropy (siteW p))/t^2)=
      (fun t => exchangeModularGap p*(exchangeHeat p q t/t^2)-
        diagonalRelativeEntropy (siteW (exchangeWeight p q t)) (siteW p)/t^2) := by
    funext t
    rw [exchange_first_law]
    ring
  rw [he]
  simpa only [sub_zero] using h

theorem exchange_total_modular_transfer (p q t : ℝ) :
    exchangeModularGap p*exchangeHeat p q t+exchangeModularGap q*exchangeHeat q p t=
      exchangeCostCoefficient p q*Real.sin t^2 := by
  unfold exchangeCostCoefficient exchangeHeat
  ring

theorem exchange_gap_mono {p q : ℝ} (hp0 : 0<p) (hq1 : q<1) (hpq : p≤q) :
    exchangeModularGap p≤exchangeModularGap q := by
  have h1 := Real.log_le_log hp0 hpq
  have h2 := Real.log_le_log (show 0<1-q by linarith) (show 1-q≤1-p by linarith)
  unfold exchangeModularGap
  linarith

theorem exchange_gap_strict_mono {p q : ℝ} (hp0 : 0<p) (hq1 : q<1) (hpq : p<q) :
    exchangeModularGap p<exchangeModularGap q := by
  have h1 := Real.log_lt_log hp0 hpq
  have h2 := Real.log_lt_log (show 0<1-q by linarith) (show 1-q<1-p by linarith)
  unfold exchangeModularGap
  linarith

theorem exchange_coefficient_nonneg (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) :
    0≤exchangeCostCoefficient p q := by
  unfold exchangeCostCoefficient
  rcases le_total p q with hpq|hqp
  · exact mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr hpq)
      (sub_nonpos.mpr (exchange_gap_mono hp0 hq1 hpq))
  · exact mul_nonneg (sub_nonneg.mpr hqp)
      (sub_nonneg.mpr (exchange_gap_mono hq0 hp1 hqp))

theorem exchange_coefficient_pos (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) (hne : p≠q) :
    0<exchangeCostCoefficient p q := by
  unfold exchangeCostCoefficient
  rcases lt_or_gt_of_ne hne with hpq|hqp
  · exact mul_pos_of_neg_of_neg (sub_neg.mpr hpq)
      (sub_neg.mpr (exchange_gap_strict_mono hp0 hq1 hpq))
  · exact mul_pos (sub_pos.mpr hqp)
      (sub_pos.mpr (exchange_gap_strict_mono hq0 hp1 hqp))

theorem exchange_coefficient_zero_iff (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) :
    exchangeCostCoefficient p q=0 ↔ p=q := by
  constructor
  · intro h
    by_contra hne
    have hpos := exchange_coefficient_pos p q hp0 hp1 hq0 hq1 hne
    linarith
  · intro h
    subst q
    simp [exchangeCostCoefficient]

theorem exchange_total_modular_nonneg (p q : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) (t : ℝ) :
    0≤exchangeModularGap p*exchangeHeat p q t+exchangeModularGap q*exchangeHeat q p t := by
  rw [exchange_total_modular_transfer]
  exact mul_nonneg (exchange_coefficient_nonneg p q hp0 hp1 hq0 hq1) (sq_nonneg _)

theorem exchange_equal_weight_control (p t : ℝ) :
    exchangeWeight p p t=p ∧ exchangeHeat p p t=0 ∧ exchangeCostCoefficient p p=0 := by
  simp [exchangeWeight, exchangeHeat, exchangeCostCoefficient]

theorem exchange_coefficient_reference :
    exchangeCostCoefficient (2/3) (3/4)=(Real.log 3-Real.log 2)/12 := by
  have hp : exchangeModularGap (2/3)=Real.log 2 := by
    unfold exchangeModularGap
    rw [←Real.log_div (by norm_num) (by norm_num)]
    norm_num
  have hq : exchangeModularGap (3/4)=Real.log 3 := by
    unfold exchangeModularGap
    rw [←Real.log_div (by norm_num) (by norm_num)]
    norm_num
  unfold exchangeCostCoefficient
  rw [hp, hq]
  ring

theorem exchange_coefficient_reference_pos :
    0<exchangeCostCoefficient (2/3) (3/4) :=
  exchange_coefficient_pos (2/3) (3/4) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num)

#print axioms exchangeWeight
#print axioms exchangeHeat
#print axioms exchangeModularGap
#print axioms exchangeCostCoefficient
#print axioms exchange_weight_zero
#print axioms exchange_weight_convex
#print axioms exchange_weight_complement
#print axioms exchange_weight_min_le
#print axioms exchange_weight_pos
#print axioms exchange_weight_lt_one
#print axioms exchange_weights_positive
#print axioms exchange_weights_normalized
#print axioms exchange_heat_eq_displacement
#print axioms exchange_heat_antisymmetric
#print axioms exchange_heat_conserved
#print axioms exchange_weight_derivative
#print axioms exchange_heat_derivative
#print axioms exchangeTangent
#print axioms exchange_weights_derivative
#print axioms exchange_tangent_zero
#print axioms exchangeStateCurve
#print axioms exchange_modular_increment
#print axioms exchange_first_law
#print axioms exchange_relative_quadratic_zero
#print axioms exchange_sin_square_limit
#print axioms exchange_heat_quadratic_limit
#print axioms exchange_modular_quadratic_limit
#print axioms exchange_entropy_quadratic_limit
#print axioms exchange_total_modular_transfer
#print axioms exchange_gap_mono
#print axioms exchange_gap_strict_mono
#print axioms exchange_coefficient_nonneg
#print axioms exchange_coefficient_pos
#print axioms exchange_coefficient_zero_iff
#print axioms exchange_total_modular_nonneg
#print axioms exchange_equal_weight_control
#print axioms exchange_coefficient_reference
#print axioms exchange_coefficient_reference_pos
end
end ChatgptAudit.Exchange055
