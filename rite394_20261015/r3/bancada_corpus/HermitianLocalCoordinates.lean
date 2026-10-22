import Mathlib

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit.Cone039
open Matrix
open scoped ComplexOrder
noncomputable section

def hermitianMatrix (t x y z : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![((t+z : ℝ) : ℂ), (x : ℂ)-Complex.I*(y : ℂ);
    (x : ℂ)+Complex.I*(y : ℂ), ((t-z : ℝ) : ℂ)]

def matrixCoordinates (A : Matrix (Fin 2) (Fin 2) ℂ) : Fin 4 → ℝ :=
  ![((A 0 0).re+(A 1 1).re)/2, (A 0 1).re, -(A 0 1).im,
    ((A 0 0).re-(A 1 1).re)/2]

def rankOneMatrix (v : Fin 2 → ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.vecMulVec v (star v)

theorem hermitian_isHermitian (t x y z : ℝ) :
    (hermitianMatrix t x y z).IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [hermitianMatrix, Matrix.conjTranspose_apply, star_add,
      star_mul, mul_comm, sub_eq_add_neg]

theorem hermitian_det (t x y z : ℝ) :
    (hermitianMatrix t x y z).det = ((t^2-x^2-y^2-z^2 : ℝ) : ℂ) := by
  rw [Matrix.det_fin_two]
  simp only [hermitianMatrix, Matrix.of_apply, Matrix.cons_val_zero,
    Matrix.cons_val_one]
  push_cast
  linear_combination (y : ℂ)^2 * Complex.I_sq

theorem hermitian_trace (t x y z : ℝ) :
    (hermitianMatrix t x y z).trace = ((2*t : ℝ) : ℂ) := by
  simp [Matrix.trace, hermitianMatrix, Fin.sum_univ_two]
  ring

theorem hermitian_identity : hermitianMatrix 1 0 0 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [hermitianMatrix]

theorem coords_of_hermitian (t x y z : ℝ) :
    matrixCoordinates (hermitianMatrix t x y z) = ![t,x,y,z] := by
  ext i
  fin_cases i <;>
    simp [matrixCoordinates, hermitianMatrix, Complex.mul_re, Complex.mul_im]

theorem hermitian_of_coords (A : Matrix (Fin 2) (Fin 2) ℂ) (hA : A.IsHermitian) :
    hermitianMatrix (matrixCoordinates A 0) (matrixCoordinates A 1)
      (matrixCoordinates A 2) (matrixCoordinates A 3) = A := by
  have h00 : (A 0 0).im = 0 := by
    have h := congrArg Complex.im (hA.apply 0 0)
    simp only [Complex.star_def, Complex.conj_im] at h
    linarith
  have h11 : (A 1 1).im = 0 := by
    have h := congrArg Complex.im (hA.apply 1 1)
    simp only [Complex.star_def, Complex.conj_im] at h
    linarith
  have h10 := hA.apply 1 0
  ext i j
  fin_cases i <;> fin_cases j <;>
    apply Complex.ext <;>
    simp [hermitianMatrix, matrixCoordinates, h00, h11, ←h10,
      Complex.mul_re, Complex.mul_im] <;> ring

theorem hermitian_coordinates_unique (t x y z t' x' y' z' : ℝ)
    (h : hermitianMatrix t x y z = hermitianMatrix t' x' y' z') :
    t=t' ∧ x=x' ∧ y=y' ∧ z=z' := by
  have hc := congrArg matrixCoordinates h
  rw [coords_of_hermitian, coords_of_hermitian] at hc
  exact ⟨congrFun hc 0, congrFun hc 1, congrFun hc 2, congrFun hc 3⟩

theorem rank_one_positive (v : Fin 2 → ℂ) :
    (rankOneMatrix v).PosSemidef :=
  Matrix.posSemidef_vecMulVec_self_star v

theorem rank_one_hermitian (v : Fin 2 → ℂ) :
    (rankOneMatrix v).IsHermitian :=
  (rank_one_positive v).isHermitian

theorem rank_one_det (v : Fin 2 → ℂ) : (rankOneMatrix v).det = 0 := by
  simp [rankOneMatrix, Matrix.det_fin_two, Matrix.vecMulVec]
  ring

theorem rank_one_coordinates_null (v : Fin 2 → ℂ) :
    (matrixCoordinates (rankOneMatrix v) 0)^2 =
      (matrixCoordinates (rankOneMatrix v) 1)^2+
      (matrixCoordinates (rankOneMatrix v) 2)^2+
      (matrixCoordinates (rankOneMatrix v) 3)^2 := by
  have h := hermitian_det (matrixCoordinates (rankOneMatrix v) 0)
    (matrixCoordinates (rankOneMatrix v) 1)
    (matrixCoordinates (rankOneMatrix v) 2)
    (matrixCoordinates (rankOneMatrix v) 3)
  rw [hermitian_of_coords _ (rank_one_hermitian v), rank_one_det] at h
  have hr := congrArg Complex.re h
  simp only [Complex.zero_re, Complex.ofReal_re] at hr
  linarith

#print axioms hermitianMatrix
#print axioms matrixCoordinates
#print axioms rankOneMatrix
#print axioms hermitian_isHermitian
#print axioms hermitian_det
#print axioms hermitian_trace
#print axioms hermitian_identity
#print axioms coords_of_hermitian
#print axioms hermitian_of_coords
#print axioms hermitian_coordinates_unique
#print axioms rank_one_positive
#print axioms rank_one_hermitian
#print axioms rank_one_det
#print axioms rank_one_coordinates_null

end
end ChatgptAudit.Cone039
