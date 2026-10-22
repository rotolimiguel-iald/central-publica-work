import ExchangeMicroscopicDynamics
import ExchangeEntropyResponse
import ModularCostDerivative

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace ChatgptAudit.Exchange055
open TGLExt Matrix Filter Topology Set
open ChatgptAudit.Micro021
open ChatgptAudit ChatgptAudit.Cost054 ChatgptAudit.Observable035
  ChatgptAudit.Angular034 ChatgptAudit.Cocycle030 ChatgptAudit.Density033
open scoped Kronecker
noncomputable section

/-- The same two-site modular observable splits into the two chosen energy levels. -/
theorem exchange_modular_matrix_split (P : SiteProfile) :
    localModularMatrix P 1 =
      (((-(Real.log (P.w 0) + Real.log (P.w 1)) : ℝ) : ℂ) •
        (1 : Matrix (chainIdx 1) (chainIdx 1) ℂ)) +
      (exchangeModularGap (P.w 0) : ℂ) • exchangeEnergy0Matrix +
      (exchangeModularGap (P.w 1) : ℂ) • exchangeEnergy1Matrix := by
  have hp : P.w 0 ≠ 0 := ne_of_gt (P.pos 0)
  have hq : P.w 1 ≠ 0 := ne_of_gt (P.pos 1)
  have hp' : 1 - P.w 0 ≠ 0 := ne_of_gt (sub_pos.mpr (P.lt_one 0))
  have hq' : 1 - P.w 1 ≠ 0 := ne_of_gt (sub_pos.mpr (P.lt_one 1))
  ext ⟨i0,i1⟩ ⟨j0,j1⟩
  fin_cases i0 <;> fin_cases i1 <;> fin_cases j0 <;> fin_cases j1 <;>
    norm_num [localModularMatrix, towerW, siteW, exchangeEnergy0Matrix,
      exchangeEnergy1Matrix, exchangeNumberMatrix, Matrix.kroneckerMap_apply,
      Matrix.one_apply, exchangeModularGap, Real.log_mul hp hq,
      Real.log_mul hp hq', Real.log_mul hp' hq, Real.log_mul hp' hq']
  all_goals push_cast
  all_goals ring

theorem exchange_modular_observable_split (P : SiteProfile) :
    localModularObservable P 1 =
      (((-(Real.log (P.w 0) + Real.log (P.w 1)) : ℝ) : ℂ) •
        (1 : TowerHilbert P →L[ℂ] TowerHilbert P)) +
      (exchangeModularGap (P.w 0) : ℂ) • exchangeEnergy0 P +
      (exchangeModularGap (P.w 1) : ℂ) • exchangeEnergy1 P := by
  change (towerPiAlgHom P 1) (localModularMatrix P 1) = _
  rw [exchange_modular_matrix_split]
  simp only [map_add, map_smul, map_one]
  rfl

/-- Only the 01-10 transition contributes to the symmetric formula of 054. -/
theorem exchange_generator_local_cost (P : SiteProfile) :
    localModularCost P 1 exchangeGeneratorMatrix =
      exchangeCostCoefficient (P.w 0) (P.w 1) := by
  rw [local_modular_cost_symmetric P 1 exchangeGeneratorMatrix
    exchange_generator_matrix_hermitian]
  have hp : P.w 0 ≠ 0 := ne_of_gt (P.pos 0)
  have hq : P.w 1 ≠ 0 := ne_of_gt (P.pos 1)
  have hp' : 1 - P.w 0 ≠ 0 := ne_of_gt (sub_pos.mpr (P.lt_one 0))
  have hq' : 1 - P.w 1 ≠ 0 := ne_of_gt (sub_pos.mpr (P.lt_one 1))
  norm_num [Fintype.sum_prod_type, Fin.sum_univ_two, exchangeGeneratorMatrix,
    pauliXMatrix, pauliYMatrix, Matrix.kroneckerMap_apply, towerW, siteW,
    exchangeCostCoefficient, exchangeModularGap,
    Real.log_mul hp hq', Real.log_mul hp' hq]
  ring

/-- No new polarizer or replacement state is introduced. -/
theorem exchange_generator_global_cost (P : SiteProfile) :
    towerModularCost P (exchangeGenerator P (hOmega P)) =
      ENNReal.ofReal (exchangeCostCoefficient (P.w 0) (P.w 1)) := by
  change towerModularCost P (towerPi P exchangeGeneratorMatrix (hOmega P)) = _
  rw [tower_local_cost_formula P 1 exchangeGeneratorMatrix
    exchange_generator_matrix_hermitian, exchange_generator_local_cost]

theorem exchange_state_add (P : SiteProfile) (t : ℝ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    exchangeState P t (A+B) = exchangeState P t A + exchangeState P t B := by
  simp only [exchangeState, mul_add, add_mul, omega_state_add]

theorem exchange_state_smul (P : SiteProfile) (t : ℝ) (c : ℂ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    exchangeState P t (c • A) = c * exchangeState P t A := by
  simp only [exchangeState, mul_smul_comm, smul_mul_assoc, omega_state_smul]

theorem exchange_state_one (P : SiteProfile) (t : ℝ) :
    exchangeState P t 1 = 1 := by
  rw [exchangeState, mul_one,
    (Unitary.mem_iff.mp (exchange_unitary_unitary P t)).1]
  exact hOmega_inner_self

theorem exchange_state_at_zero (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    exchangeState P 0 A = omegaState P A := by
  simp [exchangeState, exchange_unitary_zero]

/-- The finite modular curve is the actual exchange state evaluated on K, not a new curve. -/
theorem exchange_finite_modular_reading (P : SiteProfile) (t : ℝ) :
    finiteModularEnergy P 1 exchangeGeneratorMatrix t =
      (exchangeState P t (localModularObservable P 1)).re := by
  change (omegaState P (star (boundedPhase P (exchangeGenerator P) t) *
    localModularObservable P 1 * boundedPhase P (exchangeGenerator P) t)).re = _
  simp only [← exchange_unitary_eq_boundedPhase, exchangeState]

theorem exchange_finite_modular_split (P : SiteProfile) (t : ℝ) :
    finiteModularEnergy P 1 exchangeGeneratorMatrix t =
      -(Real.log (P.w 0)+Real.log (P.w 1)) +
      exchangeModularGap (P.w 0) * (exchangeState P t (exchangeEnergy0 P)).re +
      exchangeModularGap (P.w 1) * (exchangeState P t (exchangeEnergy1 P)).re := by
  rw [exchange_finite_modular_reading, exchange_modular_observable_split]
  simp only [exchange_state_add, exchange_state_smul, exchange_state_one,
    mul_one, Complex.add_re, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero]

/-- Conserved bare energies are weighted by the independently fixed modular gaps. -/
theorem exchange_modular_increment_is_weighted_heat (P : SiteProfile) (t : ℝ) :
    finiteModularEnergy P 1 exchangeGeneratorMatrix t -
      finiteModularEnergy P 1 exchangeGeneratorMatrix 0 =
      exchangeModularGap (P.w 0) * exchangeHeat0 P t +
      exchangeModularGap (P.w 1) * exchangeHeat1 P t := by
  rw [exchange_finite_modular_split, exchange_finite_modular_split]
  simp only [exchange_state_at_zero, exchangeHeat0, exchangeHeat1]
  ring

theorem exchange_weighted_heat_formula (P : SiteProfile) (t : ℝ) :
    exchangeModularGap (P.w 0) * exchangeHeat0 P t +
      exchangeModularGap (P.w 1) * exchangeHeat1 P t =
      exchangeCostCoefficient (P.w 0) (P.w 1) * Real.sin t ^ 2 := by
  rw [exchange_heat0_formula, exchange_heat1_formula]
  simp only [exchangeHeat, exchangeCostCoefficient]
  ring

/-- Exact finite-time identity for the same boundedPhase orbit used in 054. -/
theorem exchange_modular_energy_increment (P : SiteProfile) (t : ℝ) :
    finiteModularEnergy P 1 exchangeGeneratorMatrix t -
      finiteModularEnergy P 1 exchangeGeneratorMatrix 0 =
      exchangeCostCoefficient (P.w 0) (P.w 1) * Real.sin t ^ 2 := by
  rw [exchange_modular_increment_is_weighted_heat, exchange_weighted_heat_formula]

theorem exchange_modular_energy_quadratic_limit (P : SiteProfile) :
    Tendsto (fun t => (finiteModularEnergy P 1 exchangeGeneratorMatrix t -
      finiteModularEnergy P 1 exchangeGeneratorMatrix 0) / t ^ 2)
      (𝓝[≠] (0:ℝ)) (𝓝 (exchangeCostCoefficient (P.w 0) (P.w 1))) := by
  simpa only [exchange_generator_local_cost] using
    finite_modular_energy_quadratic_limit P 1 exchangeGeneratorMatrix
      exchange_generator_matrix_hermitian


/-- Sum of the regional entropies for the two exchange marginals. -/
def exchangePairEntropy (P : SiteProfile) (t : ℝ) : ℝ :=
  finiteEntropy (siteW (exchangeWeight (P.w 0) (P.w 1) t)) +
    finiteEntropy (siteW (exchangeWeight (P.w 1) (P.w 0) t))

theorem exchange_pair_entropy_cost_limit (P : SiteProfile) :
    Tendsto (fun t => (exchangePairEntropy P t - exchangePairEntropy P 0) / t ^ 2)
      (𝓝[<] (0:ℝ)) (𝓝 (localModularCost P 1 exchangeGeneratorMatrix)) := by
  have h := (exchange_entropy_quadratic_limit (P.w 0) (P.w 1)
    (P.pos 0) (P.lt_one 0) (P.pos 1) (P.lt_one 1)).add
      (exchange_entropy_quadratic_limit (P.w 1) (P.w 0)
        (P.pos 1) (P.lt_one 1) (P.pos 0) (P.lt_one 0))
  have he : (fun t => (exchangePairEntropy P t - exchangePairEntropy P 0) / t ^ 2) =
      (fun t => (finiteEntropy (siteW (exchangeWeight (P.w 0) (P.w 1) t)) -
        finiteEntropy (siteW (P.w 0))) / t^2 +
        (finiteEntropy (siteW (exchangeWeight (P.w 1) (P.w 0) t)) -
        finiteEntropy (siteW (P.w 1))) / t^2) := by
    funext t
    simp only [exchangePairEntropy, exchange_weight_zero]
    ring
  rw [he, exchange_generator_local_cost]
  convert h using 1
  unfold exchangeCostCoefficient
  ring

theorem exchange_global_cost_nonzero_iff (P : SiteProfile) :
    towerModularCost P (exchangeGenerator P (hOmega P)) ≠ 0 ↔ P.w 0 ≠ P.w 1 := by
  rw [exchange_generator_global_cost, ne_eq, ENNReal.ofReal_eq_zero]
  have hn := exchange_coefficient_nonneg (P.w 0) (P.w 1)
    (P.pos 0) (P.lt_one 0) (P.pos 1) (P.lt_one 1)
  have hz := exchange_coefficient_zero_iff (P.w 0) (P.w 1)
    (P.pos 0) (P.lt_one 0) (P.pos 1) (P.lt_one 1)
  constructor
  · intro h he
    exact h (le_of_eq (hz.mpr he))
  · intro h he
    exact h (hz.mp (le_antisymm he hn))

/-- The existing microscopic heat contract exposes its normalization explicitly. -/
theorem exchange_heat_error_formula (p q rate t : ℝ) :
    microscopicHeatError (exchangeStateCurve p q) rate (exchangeHeat p q) t =
      (1-rate/(2*Real.pi)*exchangeModularGap p)*exchangeHeat p q t := by
  simp only [microscopicHeatError, exchangeStateCurve, exchange_modular_increment]
  ring

theorem exchange_heat_error_quadratic_limit (p q rate : ℝ) :
    Tendsto (fun t => microscopicHeatError (exchangeStateCurve p q) rate
      (exchangeHeat p q) t / t^2) (𝓝[<] (0:ℝ))
      (𝓝 ((1-rate/(2*Real.pi)*exchangeModularGap p)*(p-q))) := by
  simpa only [exchange_heat_error_formula, mul_div_assoc] using
    (exchange_heat_quadratic_limit p q).const_mul
      (1-rate/(2*Real.pi)*exchangeModularGap p)

/-- This condition is required by the proposed energy/time identification; it is not supplied by it. -/
theorem exchange_heat_matching_iff (p q rate : ℝ) (hne : p ≠ q) :
    Tendsto (fun t => microscopicHeatError (exchangeStateCurve p q) rate
      (exchangeHeat p q) t / t^2) (𝓝[<] (0:ℝ)) (𝓝 0) ↔
      rate*exchangeModularGap p=2*Real.pi := by
  have hpi : 2*Real.pi ≠ 0 := mul_ne_zero (by norm_num) Real.pi_ne_zero
  constructor
  · intro h
    have hz := tendsto_nhds_unique (exchange_heat_error_quadratic_limit p q rate) h
    have hc := (mul_eq_zero.mp hz).resolve_right (sub_ne_zero.mpr hne)
    have hv : rate/(2*Real.pi)*exchangeModularGap p=1 := by linarith
    have hd : (rate*exchangeModularGap p)/(2*Real.pi)=1 := by
      convert hv using 1
      ring
    simpa only [one_mul] using (div_eq_iff hpi).mp hd
  · intro h
    have hv : rate/(2*Real.pi)*exchangeModularGap p=1 := by
      calc
        rate/(2*Real.pi)*exchangeModularGap p =
            (rate*exchangeModularGap p)/(2*Real.pi) := by ring
        _ = 1 := by rw [h, div_self hpi]
    simpa only [hv, sub_self, zero_mul] using exchange_heat_error_quadratic_limit p q rate

/-- Two different faithful marginals cannot share one heat normalization in this exchange protocol. -/
theorem exchange_no_common_heat_rate (p q rate : ℝ)
    (hp0 : 0<p) (hp1 : p<1) (hq0 : 0<q) (hq1 : q<1) (hne : p≠q) :
    ¬ (Tendsto (fun t => microscopicHeatError (exchangeStateCurve p q) rate
        (exchangeHeat p q) t/t^2) (𝓝[<] (0:ℝ)) (𝓝 0) ∧
      Tendsto (fun t => microscopicHeatError (exchangeStateCurve q p) rate
        (exchangeHeat q p) t/t^2) (𝓝[<] (0:ℝ)) (𝓝 0)) := by
  intro h
  have h0 := (exchange_heat_matching_iff p q rate hne).mp h.1
  have h1 := (exchange_heat_matching_iff q p rate (Ne.symm hne)).mp h.2
  have hg : exchangeModularGap p-exchangeModularGap q≠0 := by
    intro hz
    have hc : exchangeCostCoefficient p q=0 := by
      simp only [exchangeCostCoefficient, hz, mul_zero]
    exact hne ((exchange_coefficient_zero_iff p q hp0 hp1 hq0 hq1).mp hc)
  have hr : rate*(exchangeModularGap p-exchangeModularGap q)=0 := by nlinarith
  have hr0 := (mul_eq_zero.mp hr).resolve_right hg
  rw [hr0, zero_mul] at h0
  nlinarith only [Real.pi_pos, h0]


/-- Entropies of the actual restrictions, using measured zero-level expectations. -/
theorem exchange_pair_entropy_is_restriction_sum (P : SiteProfile) (t : ℝ) :
    exchangePairEntropy P t =
      finiteEntropy (siteW (exchangeWeight0 P t)) +
      finiteEntropy (siteW (exchangeWeight1 P t)) := by
  simp only [exchangePairEntropy, exchange_weight0_formula, exchange_weight1_formula]

theorem exchange_measured_pair_entropy_cost_limit (P : SiteProfile) :
    Tendsto (fun t => ((finiteEntropy (siteW (exchangeWeight0 P t)) +
      finiteEntropy (siteW (exchangeWeight1 P t))) -
      (finiteEntropy (siteW (exchangeWeight0 P 0)) +
      finiteEntropy (siteW (exchangeWeight1 P 0)))) / t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (localModularCost P 1 exchangeGeneratorMatrix)) := by
  simpa only [exchange_pair_entropy_is_restriction_sum] using
    exchange_pair_entropy_cost_limit P

theorem exchange_actual_first_law (P : SiteProfile) (t : ℝ) :
    finiteEntropy (siteW (exchangeWeight0 P t)) - finiteEntropy (siteW (P.w 0)) =
      exchangeModularGap (P.w 0) * exchangeHeat0 P t -
        diagonalRelativeEntropy (siteW (exchangeWeight0 P t)) (siteW (P.w 0)) := by
  rw [exchange_weight0_formula, exchange_heat0_formula]
  exact exchange_first_law (P.w 0) (P.w 1) t

/-- A concrete factor observable witnesses failure of state invariance. -/
theorem exchange_state_not_preserved (P : SiteProfile) (t : ℝ)
    (hne : P.w 0 ≠ P.w 1) (ht : Real.sin t ≠ 0) :
    ∃ B ∈ theFactorObject P, exchangeState P t B ≠ omegaState P B := by
  refine ⟨exchangeEnergy0 P, towerPi_mem_factor _, ?_⟩
  intro h
  have hz : exchangeHeat0 P t=0 := by simp only [exchangeHeat0, h, sub_self]
  rw [exchange_heat0_formula, exchangeHeat] at hz
  exact (mul_ne_zero (sub_ne_zero.mpr hne) (pow_ne_zero 2 ht)) hz

#print axioms exchange_modular_matrix_split
#print axioms exchange_modular_observable_split
#print axioms exchange_generator_local_cost
#print axioms exchange_generator_global_cost
#print axioms exchange_state_add
#print axioms exchange_state_smul
#print axioms exchange_state_one
#print axioms exchange_state_at_zero
#print axioms exchange_finite_modular_reading
#print axioms exchange_finite_modular_split
#print axioms exchange_modular_increment_is_weighted_heat
#print axioms exchange_weighted_heat_formula
#print axioms exchange_modular_energy_increment
#print axioms exchange_modular_energy_quadratic_limit

#print axioms exchangePairEntropy
#print axioms exchange_pair_entropy_cost_limit
#print axioms exchange_global_cost_nonzero_iff
#print axioms exchange_heat_error_formula
#print axioms exchange_heat_error_quadratic_limit
#print axioms exchange_heat_matching_iff
#print axioms exchange_no_common_heat_rate
#print axioms exchange_pair_entropy_is_restriction_sum
#print axioms exchange_measured_pair_entropy_cost_limit
#print axioms exchange_actual_first_law
#print axioms exchange_state_not_preserved
end
end ChatgptAudit.Exchange055
