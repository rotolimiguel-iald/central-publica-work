import TGLExt.UnitaryEntropyResponse
import TGLExt.DirectionalUnitaryFamily
import Mathlib.Data.Matrix.Block

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ChatgptAudit.JointUnitary
open Matrix Filter Topology Set ChatgptAudit.Micro021 ChatgptAudit.Unitary022
  ChatgptAudit.Coherent023
noncomputable section
variable {ι : Type} [Fintype ι]

structure UnitaryLabelData (ι : Type) [Fintype ι] where
  weight : ι → ℝ
  weight_pos : ∀ j, 0 < weight j
  weight_sum : ∑ j, weight j = 1
  axisA : ι → ℝ
  axisB : ι → ℝ
  initialU : ι → ℝ
  initialV : ι → ℝ
  axis_normalized : ∀ j, (axisA j)^2 + (axisB j)^2 = 1
  initial_normalized : ∀ j, (initialU j)^2 + (initialV j)^2 = 1
  positive_u : ∀ j, 0 < initialU j
  positive_v : ∀ j, 0 < initialV j

def labelledWeights (weight : ι → ℝ) (p : ι → Fin 2 → ℝ) :
    ι × Fin 2 → ℝ := fun k => weight k.1 * p k.1 k.2

def jointBase (C : UnitaryLabelData ι) : ι × Fin 2 → ℝ :=
  labelledWeights C.weight (fun j => baseWeights (C.initialU j) (C.initialV j))

def jointWeights (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ) :
    ι × Fin 2 → ℝ :=
  labelledWeights C.weight (fun j => pairWeights (C.axisA j) (C.axisB j)
    (frequency j) (C.initialU j) (C.initialV j) t)

theorem joint_weights_normalized (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) : ∑ k, jointWeights C frequency t k = 1 := by
  unfold jointWeights labelledWeights
  rw [Fintype.sum_prod_type]
  simp only [← Finset.mul_sum, pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized _),
    mul_one]
  exact C.weight_sum

theorem joint_weights_nonnegative (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) : ∀ k, 0 ≤ jointWeights C frequency t k := by
  intro k
  exact mul_nonneg (C.weight_pos k.1).le
    (pair_weights_nonnegative _ _ _ _ _ _ (C.axis_normalized k.1) k.2)

theorem joint_base_positive (C : UnitaryLabelData ι) : ∀ k, 0 < jointBase C k := by
  intro k
  exact mul_pos (C.weight_pos k.1)
    (base_weights_positive _ _ (C.positive_u k.1) (C.positive_v k.1) k.2)

def jointUnitaryCurve (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    DiagonalStateCurve (jointBase C) where
  weights := jointWeights C frequency
  tangent := fun t k => C.weight k.1 * pairTangent (C.axisA k.1) (C.axisB k.1)
    (frequency k.1) (C.initialU k.1) (C.initialV k.1) t k.2
  at_zero := by
    intro k
    unfold jointWeights jointBase labelledWeights
    rw [pair_weights_at_zero]
  trace_one := joint_weights_normalized C frequency
  derivative_zero := fun k => (pair_weights_derivative _ _ _ _ _ 0 k.2).const_mul (C.weight k.1)
  derivative_past := by
    filter_upwards [] with t
    intro k
    exact (pair_weights_derivative _ _ _ _ _ t k.2).const_mul (C.weight k.1)
  tangent_continuous := by
    intro k
    exact continuousAt_const.mul
      ((unitaryStateCurve (C.axisA k.1) (C.axisB k.1) (frequency k.1)
        (C.initialU k.1) (C.initialV k.1) (C.initial_normalized k.1)).tangent_continuous k.2)

theorem joint_curve_tangent_zero (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    (jointUnitaryCurve C frequency).tangent 0 = 0 := by
  funext k
  simp only [jointUnitaryCurve, pair_tangent_at_zero, Pi.zero_apply, mul_zero]

theorem joint_weights_positive_near (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k, 0 < jointWeights C frequency t k :=
  state_curve_positive_near (jointUnitaryCurve C frequency) (joint_base_positive C)

theorem entropy_atom_scaled (weight q : ℝ) :
    entropyAtom (weight*q) = weight * entropyAtom q - weight*q*Real.log weight := by
  by_cases hw : weight = 0
  · simp [hw, entropyAtom]
  by_cases hq : q = 0
  · simp [hq, entropyAtom]
  unfold entropyAtom
  rw [Real.log_mul hw hq]
  ring

theorem entropy_labelled_decomposition (weight : ι → ℝ) (p : ι → Fin 2 → ℝ)
    (hn : ∀ j, ∑ b, p j b = 1) :
    finiteEntropy (labelledWeights weight p) =
      finiteEntropy weight + ∑ j, weight j * finiteEntropy (p j) := by
  unfold finiteEntropy
  rw [Fintype.sum_prod_type, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  simp only [labelledWeights, Fin.sum_univ_two, entropy_atom_scaled]
  have hp : p j 1 = 1 - p j 0 := by
    have h := hn j
    simp only [Fin.sum_univ_two] at h
    linarith
  rw [hp]
  unfold entropyAtom
  ring

theorem modular_labelled_decomposition (weight : ι → ℝ)
    (hw : ∀ j, 0 < weight j) (p r : ι → Fin 2 → ℝ)
    (hp : ∀ j b, 0 < p j b) (hnp : ∀ j, ∑ b, p j b = 1)
    (hnr : ∀ j, ∑ b, r j b = 1) :
    modularIncrement (labelledWeights weight p) (labelledWeights weight r) =
      ∑ j, weight j * modularIncrement (p j) (r j) := by
  unfold modularIncrement
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro j _
  simp only [labelledWeights, Fin.sum_univ_two]
  rw [Real.log_mul (ne_of_gt (hw j)) (ne_of_gt (hp j 0)),
    Real.log_mul (ne_of_gt (hw j)) (ne_of_gt (hp j 1))]
  have hp1 : p j 1 = 1 - p j 0 := by
    have h := hnp j
    simp only [Fin.sum_univ_two] at h
    linarith
  have hr1 : r j 1 = 1 - r j 0 := by
    have h := hnr j
    simp only [Fin.sum_univ_two] at h
    linarith
  rw [hp1, hr1]
  ring

theorem joint_entropy_decomposition (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    finiteEntropy (jointWeights C frequency t) = finiteEntropy C.weight +
      ∑ j, C.weight j * finiteEntropy
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) := by
  apply entropy_labelled_decomposition
  intro j
  exact pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized j)

theorem joint_base_entropy_decomposition (C : UnitaryLabelData ι) :
    finiteEntropy (jointBase C) = finiteEntropy C.weight +
      ∑ j, C.weight j * finiteEntropy (baseWeights (C.initialU j) (C.initialV j)) := by
  apply entropy_labelled_decomposition
  intro j
  simpa only [baseWeights, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
    using C.initial_normalized j

theorem joint_entropy_increment (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C) =
      ∑ j, C.weight j * (finiteEntropy
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) -
          finiteEntropy (baseWeights (C.initialU j) (C.initialV j))) := by
  rw [joint_entropy_decomposition, joint_base_entropy_decomposition]
  simp only [mul_sub, Finset.sum_sub_distrib]
  ring

theorem joint_modular_increment (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    modularIncrement (jointBase C) (jointWeights C frequency t) =
      ∑ j, C.weight j * modularIncrement (baseWeights (C.initialU j) (C.initialV j))
        (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) := by
  apply modular_labelled_decomposition _ C.weight_pos
  · intro j
    exact base_weights_positive _ _ (C.positive_u j) (C.positive_v j)
  · intro j
    simpa only [baseWeights, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
      using C.initial_normalized j
  · intro j
    exact pair_weights_normalized _ _ _ _ _ _ (C.initial_normalized j)

def jointResponse (C : UnitaryLabelData ι) (frequency : ι → ℝ) : ℝ :=
  ∑ j, C.weight j * unitaryResponse (C.axisA j) (C.axisB j)
    (frequency j) (C.initialU j) (C.initialV j)

theorem joint_modular_quadratic_limit (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => modularIncrement (jointBase C) (jointWeights C frequency t) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (jointResponse C frequency)) := by
  have hl := tendsto_finsetSum Finset.univ (fun j _ =>
    (unitary_modular_quadratic_limit (C.axisA j) (C.axisB j) (frequency j)
      (C.initialU j) (C.initialV j) (C.positive_u j) (C.positive_v j)).const_mul (C.weight j))
  have he : (fun t => modularIncrement (jointBase C) (jointWeights C frequency t) / t^2) =
      (fun t => ∑ j, C.weight j *
        (modularIncrement (baseWeights (C.initialU j) (C.initialV j))
          (pairWeights (C.axisA j) (C.axisB j) (frequency j) (C.initialU j) (C.initialV j) t) / t^2)) := by
    funext t
    rw [joint_modular_increment, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [he]
  exact hl

theorem joint_entropy_quadratic_limit (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => (finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C)) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (jointResponse C frequency)) := by
  have hl := tendsto_finsetSum Finset.univ (fun j _ =>
    (unitary_entropy_quadratic_limit (C.axisA j) (C.axisB j) (frequency j)
      (C.initialU j) (C.initialV j) (C.initial_normalized j)
      (C.positive_u j) (C.positive_v j)).const_mul (C.weight j))
  have he : (fun t => (finiteEntropy (jointWeights C frequency t) - finiteEntropy (jointBase C)) / t^2) =
      (fun t => ∑ j, C.weight j *
        ((finiteEntropy (pairWeights (C.axisA j) (C.axisB j) (frequency j)
          (C.initialU j) (C.initialV j) t) -
          finiteEntropy (baseWeights (C.initialU j) (C.initialV j))) / t^2)) := by
    funext t
    rw [joint_entropy_increment, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [he]
  exact hl

theorem joint_relative_entropy_quadratic_zero (C : UnitaryLabelData ι) (frequency : ι → ℝ) :
    Tendsto (fun t => diagonalRelativeEntropy (jointWeights C frequency t) (jointBase C) / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0) := by
  apply (relative_entropy_quadratic_zero_iff (jointUnitaryCurve C frequency)
    (joint_base_positive C)).mpr
  exact joint_curve_tangent_zero C frequency

def jointCovectorCurve (C : UnitaryLabelData ι) (w : ι → Coordinate4) (direction : Coordinate4) :
    DiagonalStateCurve (jointBase C) :=
  jointUnitaryCurve C (fun j => covectorRead (w j) direction)

theorem joint_covector_response (C : UnitaryLabelData ι)
    (w : ι → Coordinate4) (direction : Coordinate4) :
    jointResponse C (fun j => covectorRead (w j) direction) =
      ∑ j, C.weight j * unitaryResponse (C.axisA j) (C.axisB j)
        1 (C.initialU j) (C.initialV j) * (covectorRead (w j) direction)^2 := by
  unfold jointResponse
  apply Finset.sum_congr rfl
  intro j _
  unfold unitaryResponse
  ring

/-- Matrix.blockDiagonal uses (branch,label); probabilities explicitly use (label,branch). -/
def jointBlockFlow [DecidableEq ι] (C : UnitaryLabelData ι) (frequency : ι → ℝ) (t : ℝ) :
    Matrix (Fin 2 × ι) (Fin 2 × ι) ℂ :=
  Matrix.blockDiagonal (fun j => pairFlow (C.axisA j) (C.axisB j) (frequency j) t)

theorem joint_block_flow_unitary [DecidableEq ι] (C : UnitaryLabelData ι)
    (frequency : ι → ℝ) (t : ℝ) :
    (jointBlockFlow C frequency t)ᴴ * jointBlockFlow C frequency t = 1 ∧
      jointBlockFlow C frequency t * (jointBlockFlow C frequency t)ᴴ = 1 := by
  unfold jointBlockFlow
  constructor
  · rw [Matrix.blockDiagonal_conjTranspose, ← Matrix.blockDiagonal_mul]
    simp only [pair_flow_adjoint_mul _ _ _ _ (C.axis_normalized _)]
    exact Matrix.blockDiagonal_one
  · rw [Matrix.blockDiagonal_conjTranspose, ← Matrix.blockDiagonal_mul]
    simp only [pair_flow_mul_adjoint _ _ _ _ (C.axis_normalized _)]
    exact Matrix.blockDiagonal_one

#print axioms UnitaryLabelData
#print axioms labelledWeights
#print axioms jointBase
#print axioms jointWeights
#print axioms joint_weights_normalized
#print axioms joint_weights_nonnegative
#print axioms joint_base_positive
#print axioms jointUnitaryCurve
#print axioms joint_curve_tangent_zero
#print axioms joint_weights_positive_near
#print axioms entropy_atom_scaled
#print axioms entropy_labelled_decomposition
#print axioms modular_labelled_decomposition
#print axioms joint_entropy_decomposition
#print axioms joint_base_entropy_decomposition
#print axioms joint_entropy_increment
#print axioms joint_modular_increment
#print axioms jointResponse
#print axioms joint_modular_quadratic_limit
#print axioms joint_entropy_quadratic_limit
#print axioms joint_relative_entropy_quadratic_zero
#print axioms jointCovectorCurve
#print axioms joint_covector_response
#print axioms jointBlockFlow
#print axioms joint_block_flow_unitary

end
end ChatgptAudit.JointUnitary
