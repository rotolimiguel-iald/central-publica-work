import Mathlib

set_option autoImplicit false

/-! Exact algebraic bridge for the preregistered incoherent population channel.
S itself remains unitary; passing to T assumes complete dephasing between scatterings.
No literal beta, observed data, canonical boost identification or ontological claim.
The sum/difference basis is deliberately unnormalized; its inverse is supplied explicitly.
-/
namespace F1Atrator.OpticalPopulation

abbrev M := Matrix (Fin 2) (Fin 2) ℝ

def T (b : ℝ) : M := !![1-b,b;b,1-b]
noncomputable def R : M := !![(1/2:ℝ),1/2;1/2,1/2]
def A (b : ℝ) : M := 1-T b
def basis : M := !![(1:ℝ),1;1,-1]
noncomputable def basisInv : M := (1/2:ℝ) • basis

theorem population_decomposition (b : ℝ) :
    T b = R + (1-2*b) • ((1:M)-R) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [T,R] <;> ring

theorem reading_after_step (b : ℝ) : R * T b = R := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,T,R] <;> ring

theorem step_after_reading (b : ℝ) : T b * R = R := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,T,R] <;> ring

theorem rereading_adds_nothing : R * R = R := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,R]

theorem reading_symmetric : R.transpose = R := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [R]

theorem basis_inverse_left : basisInv * basis = (1:M) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,basisInv,basis]

theorem basis_inverse_right : basis * basisInv = (1:M) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,basisInv,basis]

theorem sum_difference_conjugacy (b : ℝ) :
    basisInv * T b * basis = !![(1:ℝ),0;0,1-2*b] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,basisInv,basis,T] <;> ring

theorem reading_in_sum_difference_basis :
    basisInv * R * basis = !![(1:ℝ),0;0,0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Fin.sum_univ_two,basisInv,basis,R]

theorem letter_before_normalization (b : ℝ) :
    A b - (2*b) • (1:M) = (-(2*b)) • R := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [A,T,R] <;> ring

theorem normalized_letter (b : ℝ) (hb : b ≠ 0) :
    (-(2*b))⁻¹ • (A b - (2*b) • (1:M)) = R := by
  rw [letter_before_normalization, smul_smul]
  have h : -(2*b) ≠ 0 := neg_ne_zero.mpr (mul_ne_zero (by norm_num) hb)
  rw [inv_mul_cancel₀ h, one_smul]

theorem annihilating_polynomial (b : ℝ) :
    A b * (A b - (2*b) • (1:M)) = 0 := by
  rw [letter_before_normalization, Matrix.mul_smul]
  have h : A b * R = 0 := by
    rw [A, sub_mul, one_mul, step_after_reading, sub_self]
  rw [h, smul_zero]

theorem strict_transient_factor {b : ℝ} (hb : 0 < b) (hbhalf : b < 1/2) :
    -1 < 1-2*b ∧ 1-2*b < 1 ∧ 0 < 1-2*b := by
  constructor
  · linarith
  constructor <;> linarith

theorem zero_beta_control : T 0 = (1:M) := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [T]

theorem affine_no_fixed (x : ℝ) : x+1 ≠ x := by
  intro h
  linarith

end F1Atrator.OpticalPopulation

#print axioms F1Atrator.OpticalPopulation.population_decomposition
#print axioms F1Atrator.OpticalPopulation.reading_after_step
#print axioms F1Atrator.OpticalPopulation.step_after_reading
#print axioms F1Atrator.OpticalPopulation.rereading_adds_nothing
#print axioms F1Atrator.OpticalPopulation.reading_symmetric
#print axioms F1Atrator.OpticalPopulation.basis_inverse_left
#print axioms F1Atrator.OpticalPopulation.basis_inverse_right
#print axioms F1Atrator.OpticalPopulation.sum_difference_conjugacy
#print axioms F1Atrator.OpticalPopulation.reading_in_sum_difference_basis
#print axioms F1Atrator.OpticalPopulation.letter_before_normalization
#print axioms F1Atrator.OpticalPopulation.normalized_letter
#print axioms F1Atrator.OpticalPopulation.annihilating_polynomial
#print axioms F1Atrator.OpticalPopulation.strict_transient_factor
#print axioms F1Atrator.OpticalPopulation.zero_beta_control

#print axioms F1Atrator.OpticalPopulation.affine_no_fixed
