import BondLocalityEstimates
import TGLExt.UnitaryDuhamel
import Mathlib.Analysis.Normed.Operator.Mul
import Mathlib.Topology.Algebra.InfiniteSum.Module

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.FiniteCommutatorSeries
open TGLExt NormedSpace ChatgptAudit.BondLocality ChatgptAudit.UnitaryDuhamel
noncomputable section
open scoped Nat

local instance operatorRationalAlgebra (P : SiteProfile) : NormedAlgebra ℚ (BondOperator P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance operatorRationalTower (P : SiteProfile) : IsScalarTower ℚ ℂ (BondOperator P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

abbrev SuperOperator (P : SiteProfile) := BondOperator P →L[ℂ] BondOperator P

local instance superRationalAlgebra (P : SiteProfile) : NormedAlgebra ℚ (SuperOperator P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance superRationalTower (P : SiteProfile) : IsScalarTower ℚ ℂ (SuperOperator P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def leftMultiplier {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  ContinuousLinearMap.mul ℂ (BondOperator P) H

def rightMultiplier {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  (ContinuousLinearMap.mul ℂ (BondOperator P)).flip H

theorem left_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    leftMultiplier H A = H * A := rfl

theorem right_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    rightMultiplier H A = A * H := rfl

theorem left_multiplier_power_apply {P : SiteProfile} (H A : BondOperator P) (k : ℕ) :
    (leftMultiplier H ^ k) A = H ^ k * A := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [pow_succ',ContinuousLinearMap.mul_apply,left_multiplier_apply,ih,pow_succ']
      exact (mul_assoc _ _ _).symm

theorem right_multiplier_power_apply {P : SiteProfile} (H A : BondOperator P) (k : ℕ) :
    (rightMultiplier H ^ k) A = A * H ^ k := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [pow_succ',ContinuousLinearMap.mul_apply,right_multiplier_apply,ih,pow_succ]
      exact mul_assoc _ _ _

theorem multipliers_commute {P : SiteProfile} (H K : BondOperator P) :
    Commute (leftMultiplier H) (rightMultiplier K) := by
  ext A
  exact mul_assoc H A K

theorem exp_left_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    (NormedSpace.exp (leftMultiplier H)) A = NormedSpace.exp H * A := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) (leftMultiplier H)).mapL
    (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  have ht := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) H).mapL (rightMultiplier A)
  simp only [ContinuousLinearMap.apply_apply,ContinuousLinearMap.smul_apply,
    left_multiplier_power_apply] at hs
  simp only [map_smul,right_multiplier_apply] at ht
  exact hs.unique ht

theorem exp_right_multiplier_apply {P : SiteProfile} (H A : BondOperator P) :
    (NormedSpace.exp (rightMultiplier H)) A = A * NormedSpace.exp H := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) (rightMultiplier H)).mapL
    (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  have ht := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) H).mapL (leftMultiplier A)
  simp only [ContinuousLinearMap.apply_apply,ContinuousLinearMap.smul_apply,
    right_multiplier_power_apply] at hs
  simp only [map_smul,left_multiplier_apply] at ht
  exact hs.unique ht

def bracketOperator {P : SiteProfile} (H : BondOperator P) : SuperOperator P :=
  leftMultiplier H - rightMultiplier H

theorem bracket_operator_apply {P : SiteProfile} (H A : BondOperator P) :
    bracketOperator H A = operatorBracket H A := rfl

theorem scaled_bracket_split {P : SiteProfile} (H : BondOperator P) (z : ℂ) :
    z • bracketOperator H = leftMultiplier (z • H) + rightMultiplier ((-z) • H) := by
  ext A
  simp only [ContinuousLinearMap.smul_apply,ContinuousLinearMap.add_apply,bracket_operator_apply,
    operatorBracket,left_multiplier_apply,right_multiplier_apply,smul_sub,
    smul_mul_assoc,mul_smul_comm,neg_smul]
  exact sub_eq_add_neg _ _

theorem exp_scaled_bracket_apply {P : SiteProfile} (H A : BondOperator P) (z : ℂ) :
    (NormedSpace.exp (z • bracketOperator H)) A =
      NormedSpace.exp (z • H) * A * NormedSpace.exp ((-z) • H) := by
  rw [scaled_bracket_split,NormedSpace.exp_add_of_commute (multipliers_commute _ _),
    ContinuousLinearMap.mul_apply,exp_right_multiplier_apply,exp_left_multiplier_apply]
  exact (mul_assoc _ _ _).symm

theorem cutoff_scaled_bracket_power {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (z : ℂ) (k : ℕ) :
    ((z • bracketOperator (cutoffHamiltonian D N)) ^ k) A =
      z ^ k • iteratedCutoffBracket D N A k := by
  induction k with
  | zero => simp [iteratedCutoffBracket]
  | succ k ih =>
      rw [pow_succ',ContinuousLinearMap.mul_apply,ContinuousLinearMap.smul_apply,ih,
        map_smul,bracket_operator_apply,cutoff_hamiltonian_bracket,smul_smul]
      rw [pow_succ',iteratedCutoffBracket]

theorem cutoff_conjugation_hasSum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (z : ℂ) :
    HasSum (fun k => (z ^ k / (k.factorial : ℂ)) • iteratedCutoffBracket D N A k)
      (NormedSpace.exp (z • cutoffHamiltonian D N) * A *
        NormedSpace.exp ((-z) • cutoffHamiltonian D N)) := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ)
      (z • bracketOperator (cutoffHamiltonian D N))).mapL
        (ContinuousLinearMap.apply ℂ (BondOperator P) A)
  simpa only [ContinuousLinearMap.apply_apply,ContinuousLinearMap.smul_apply,
    cutoff_scaled_bracket_power,exp_scaled_bracket_apply,smul_smul,div_eq_mul_inv,mul_comm] using hs

def finiteEvolution {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (t : ℝ) (A : BondOperator P) : BondOperator P :=
  evolution (cutoffHamiltonian D N) t * A * evolution (cutoffHamiltonian D N) (-t)

theorem finite_evolution_hasSum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    HasSum (fun k => (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
      iteratedCutoffBracket D N A k) (finiteEvolution D N t A) := by
  simpa only [finiteEvolution,evolution,Complex.ofReal_neg,neg_mul] using
    cutoff_conjugation_hasSum D N A ((t : ℂ) * Complex.I)

theorem finite_evolution_eq_tsum {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    finiteEvolution D N t A =
      ∑' k, (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
        iteratedCutoffBracket D N A k :=
  (finite_evolution_hasSum D N A t).tsum_eq.symm

theorem finite_evolution_series_summable {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) (t : ℝ) :
    Summable (fun k => (((t : ℂ) * Complex.I) ^ k / (k.factorial : ℂ)) •
      iteratedCutoffBracket D N A k) :=
  (finite_evolution_hasSum D N A t).summable

theorem finite_evolution_isometry {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (t : ℝ) (A : BondOperator P) :
    ‖finiteEvolution D N t A‖ = ‖A‖ := by
  unfold finiteEvolution
  rw [CStarRing.norm_mul_mem_unitary _
      (evolution_unitary _ (cutoff_hamiltonian_selfadjoint D N) (-t)),
    CStarRing.norm_mem_unitary_mul _
      (evolution_unitary _ (cutoff_hamiltonian_selfadjoint D N) t)]

#print axioms operatorRationalAlgebra
#print axioms operatorRationalTower
#print axioms SuperOperator
#print axioms superRationalAlgebra
#print axioms superRationalTower
#print axioms leftMultiplier
#print axioms rightMultiplier
#print axioms left_multiplier_apply
#print axioms right_multiplier_apply
#print axioms left_multiplier_power_apply
#print axioms right_multiplier_power_apply
#print axioms multipliers_commute
#print axioms exp_left_multiplier_apply
#print axioms exp_right_multiplier_apply
#print axioms bracketOperator
#print axioms bracket_operator_apply
#print axioms scaled_bracket_split
#print axioms exp_scaled_bracket_apply
#print axioms cutoff_scaled_bracket_power
#print axioms cutoff_conjugation_hasSum
#print axioms finiteEvolution
#print axioms finite_evolution_hasSum
#print axioms finite_evolution_eq_tsum
#print axioms finite_evolution_series_summable
#print axioms finite_evolution_isometry
end
end ChatgptAudit.FiniteCommutatorSeries
