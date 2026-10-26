import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.Ext
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace ChatgptAudit.GeometricSector
open Matrix
noncomputable section

abbrev Mat4 := Matrix (Fin 4) (Fin 4) ℂ

def productDensity (p : ℝ) : Mat4 :=
  Matrix.diagonal ![((p : ℂ) ^ 2), (p : ℂ) * (1-p),
    (1-(p : ℂ)) * p, (1-(p : ℂ)) ^ 2]

def localDiagonal (a b : ℂ) : Mat4 :=
  Matrix.diagonal ![a, a, b, b]

def localSeed : Mat4 := localDiagonal 1 0

def blockRotation : Mat4 :=
  !![1, 0, 0, 0;
     0, 3/5, -(4/5), 0;
     0, 4/5, 3/5, 0;
     0, 0, 0, 1]

def rotate (a : Mat4) : Mat4 := blockRotation * a * blockRotationᴴ

def spectralCenterAverage (a : Mat4) : Mat4 :=
  Matrix.diagonal ![a 0 0, (a 1 1 + a 2 2)/2, (a 1 1 + a 2 2)/2, a 3 3]

def weightedState (p : ℝ) (a : Mat4) : ℂ :=
  (p : ℂ)^2 * a 0 0 + (p : ℂ)*(1-p)*a 1 1 +
    (1-(p : ℂ))*p*a 2 2 + (1-(p : ℂ))^2*a 3 3

def PairwiseCommutative (sector : Set Mat4) : Prop :=
  ∀ a ∈ sector, ∀ b ∈ sector, a*b=b*a

def StateUnitaryCovariant (density : Mat4) (sector : Set Mat4) : Prop :=
  ∀ u : Mat4, uᴴ*u=1 → u*uᴴ=1 → u*density*uᴴ=density →
    ∀ a ∈ sector, u*a*uᴴ ∈ sector

theorem block_rotation_left_unitary : blockRotationᴴ * blockRotation = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, blockRotation, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Fin.sum_univ_succ]

theorem block_rotation_right_unitary : blockRotation * blockRotationᴴ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, blockRotation, Matrix.mul_apply, Matrix.conjTranspose_apply,
      Fin.sum_univ_succ]

theorem block_rotation_preserves_product_density (p : ℝ) :
    blockRotation * productDensity p * blockRotationᴴ = productDensity p := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, blockRotation, productDensity, Matrix.mul_apply,
      Matrix.conjTranspose_apply, Fin.sum_univ_succ] <;> ring

theorem local_seed_is_hermitian : localSeedᴴ = localSeed := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, localSeed, localDiagonal, Matrix.conjTranspose_apply]

theorem local_seed_commutes_density (p : ℝ) :
    localSeed * productDensity p = productDensity p * localSeed := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, localSeed, localDiagonal, productDensity, Matrix.mul_apply,
      Fin.sum_univ_succ]

theorem rotated_seed_off_diagonal :
    rotate localSeed 1 2 = (12 : ℂ)/25 := by
  norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, rotate, blockRotation, localSeed, localDiagonal,
    Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ]

theorem local_seed_does_not_commute_with_rotated_seed :
    localSeed * rotate localSeed ≠ rotate localSeed * localSeed := by
  intro h
  have he := congrArg (fun a : Mat4 => a 1 2) h
  norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, rotate, blockRotation, localSeed, localDiagonal,
    Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ] at he

theorem no_state_covariant_commutative_sector_containing_local_seed
    (p : ℝ) (sector : Set Mat4)
    (hseed : localSeed ∈ sector)
    (hcov : StateUnitaryCovariant (productDensity p) sector)
    (hcomm : PairwiseCommutative sector) : False := by
  have hrot : rotate localSeed ∈ sector :=
    hcov blockRotation block_rotation_left_unitary block_rotation_right_unitary
      (block_rotation_preserves_product_density p) localSeed hseed
  exact local_seed_does_not_commute_with_rotated_seed (hcomm localSeed hseed _ hrot)

theorem no_state_covariant_commutative_extension (p : ℝ) :
    ¬ ∃ sector : Set Mat4,
      (∀ a b : ℂ, localDiagonal a b ∈ sector) ∧
      StateUnitaryCovariant (productDensity p) sector ∧ PairwiseCommutative sector := by
  rintro ⟨sector, hlocal, hcov, hcomm⟩
  exact no_state_covariant_commutative_sector_containing_local_seed p sector
    (hlocal 1 0) hcov hcomm

theorem spectral_center_unital : spectralCenterAverage 1 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage]

theorem spectral_center_add (a b : Mat4) :
    spectralCenterAverage (a+b) = spectralCenterAverage a + spectralCenterAverage b := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage] <;> ring

theorem spectral_center_smul (z : ℂ) (a : Mat4) :
    spectralCenterAverage (z • a) = z • spectralCenterAverage a := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage] <;> ring

theorem spectral_center_idempotent (a : Mat4) :
    spectralCenterAverage (spectralCenterAverage a) = spectralCenterAverage a := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage]

theorem spectral_center_outputs_commute (a b : Mat4) :
    spectralCenterAverage a * spectralCenterAverage b =
      spectralCenterAverage b * spectralCenterAverage a := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem spectral_center_preserves_state (p : ℝ) (a : Mat4) :
    weightedState p (spectralCenterAverage a) = weightedState p a := by
  norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, weightedState, spectralCenterAverage]
  ring

theorem spectral_center_covariant_under_block_rotation (a : Mat4) :
    spectralCenterAverage (rotate a) = rotate (spectralCenterAverage a) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage, rotate, blockRotation,
      Matrix.mul_apply, Matrix.conjTranspose_apply, Fin.sum_univ_succ] <;> first | rfl | ring

theorem spectral_center_changes_local_seed :
    spectralCenterAverage localSeed = Matrix.diagonal ![1, (1:ℂ)/2, 1/2, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage, localSeed, localDiagonal]

theorem spectral_center_does_not_fix_local_seed :
    spectralCenterAverage localSeed ≠ localSeed := by
  intro h
  have he := congrArg (fun a : Mat4 => a 1 1) h
  norm_num [Matrix.diagonal_apply, Complex.conj_ofNat, Matrix.vecMul, dotProduct, Matrix.cons_val_two, Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail, spectralCenterAverage, localSeed, localDiagonal] at he

theorem spectral_center_retains_local_diagonal_iff (a b : ℂ) :
    spectralCenterAverage (localDiagonal a b) = localDiagonal a b ↔ a=b := by
  constructor
  · intro h
    have he := congrArg (fun x : Mat4 => x 1 1) h
    have hm : (a+b)/2=a := by simpa [spectralCenterAverage, localDiagonal] using he
    linear_combination -2 * hm
  · intro h
    subst b
    ext i j
    fin_cases i <;> fin_cases j <;> simp [spectralCenterAverage, localDiagonal]

#print axioms Mat4
#print axioms productDensity
#print axioms localDiagonal
#print axioms localSeed
#print axioms blockRotation
#print axioms rotate
#print axioms spectralCenterAverage
#print axioms weightedState
#print axioms PairwiseCommutative
#print axioms StateUnitaryCovariant
#print axioms block_rotation_left_unitary
#print axioms block_rotation_right_unitary
#print axioms block_rotation_preserves_product_density
#print axioms local_seed_is_hermitian
#print axioms local_seed_commutes_density
#print axioms rotated_seed_off_diagonal
#print axioms local_seed_does_not_commute_with_rotated_seed
#print axioms no_state_covariant_commutative_sector_containing_local_seed
#print axioms no_state_covariant_commutative_extension
#print axioms spectral_center_unital
#print axioms spectral_center_add
#print axioms spectral_center_smul
#print axioms spectral_center_idempotent
#print axioms spectral_center_outputs_commute
#print axioms spectral_center_preserves_state
#print axioms spectral_center_covariant_under_block_rotation
#print axioms spectral_center_changes_local_seed
#print axioms spectral_center_does_not_fix_local_seed
#print axioms spectral_center_retains_local_diagonal_iff

end
end ChatgptAudit.GeometricSector
