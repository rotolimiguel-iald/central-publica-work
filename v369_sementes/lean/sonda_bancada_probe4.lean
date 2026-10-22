import Mathlib
import TGL.GravitonShadow

open Matrix
open scoped Kronecker

namespace Probe4
open TGL.GravitonShadow

noncomputable def faceImage (U : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) * bellProjector * (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))ᴴ

theorem ptr_conj (U : Matrix (Fin 2) (Fin 2) ℂ) (X : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    ptr ((U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) * X * (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))ᴴ) =
      U * ptr X * Uᴴ := by
  ext i j
  simp only [ptr, Matrix.of_apply, Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two,
    Matrix.conjTranspose_apply, Matrix.kronecker_apply, Matrix.one_apply]
  simp
  ring

/-- Pauli X -/
def sx : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

theorem sx_unitary : sx ∈ Matrix.unitaryGroup (Fin 2) ℂ := by
  rw [Matrix.mem_unitaryGroup_iff]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [sx, Matrix.mul_apply, Fin.sum_univ_two, Matrix.star_apply]

/-- a familia nao e' trivial: a face por sx e' OUTRA singularidade (|01>+|10>) -/
theorem faceImage_sx_ne : faceImage sx ≠ bellProjector := by
  intro h
  have := congrFun (congrFun h (0, 1)) (0, 1)
  simp [faceImage, sx, bellProjector, Matrix.mul_apply, Fintype.sum_prod_type,
    Fin.sum_univ_two, Matrix.conjTranspose_apply] at this

/-- o controle (produto) NAO esta na familia de nenhuma U unitaria -/
theorem product_not_in_family (U : Matrix (Fin 2) (Fin 2) ℂ)
    (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ) : faceImage U ≠ productProjector := by
  intro h
  have hU' := (Unitary.mem_iff.mp hU).2
  rw [Matrix.star_eq_conjTranspose] at hU'
  have h1 : ptr (faceImage U) = (2⁻¹ : ℂ) • 1 := by
    unfold faceImage
    rw [ptr_conj, bell_reduced_half, Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, hU']
  rw [h, product_reduced_pure] at h1
  have := congrFun (congrFun h1 1) 1
  simp [e00] at this

end Probe4

#print axioms Probe4.faceImage_sx_ne
#print axioms Probe4.product_not_in_family
#print axioms Probe4.sx_unitary
