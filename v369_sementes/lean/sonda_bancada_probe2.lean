import Mathlib
import TGL.GravitonShadow
import TGLExt.FiniteTomita

open Matrix
open scoped Kronecker ComplexOrder MatrixOrder

namespace Probe
open TGL.GravitonShadow

/-! (1) troca das faces -/

theorem bell_swap_invariant :
    bellProjector.submatrix Prod.swap Prod.swap = bellProjector := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [bellProjector]

theorem bell_reindex_invariant :
    Matrix.reindex (Equiv.prodComm (Fin 2) (Fin 2)) (Equiv.prodComm (Fin 2) (Fin 2))
      bellProjector = bellProjector := by
  rw [Matrix.reindex_apply, Equiv.prodComm_symm, Equiv.coe_prodComm]
  exact bell_swap_invariant

/-- o controle v29 TAMBEM e' invariante pela troca (medida: a troca nao discrimina) -/
theorem product_swap_invariant :
    productProjector.submatrix Prod.swap Prod.swap = productProjector := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [productProjector]

/-- a troca e' multiplicativa e respeita star (automorfismo-* por equivalencia) -/
theorem swap_mul (X Y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    (X * Y).submatrix Prod.swap Prod.swap =
      X.submatrix Prod.swap Prod.swap * Y.submatrix Prod.swap Prod.swap := by
  have := Matrix.submatrix_mul_equiv X Y Prod.swap (Equiv.prodComm (Fin 2) (Fin 2)) Prod.swap
  rw [Equiv.coe_prodComm] at this
  exact this.symm

theorem swap_star (X : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    (X.submatrix Prod.swap Prod.swap)ᴴ = Xᴴ.submatrix Prod.swap Prod.swap :=
  Matrix.conjTranspose_submatrix X _ _

/-- J do traco sob a vetorizacao da mathlib: vec(zᴴ) = star(vec z) ∘ swap -/
theorem vec_Jconj (z : Matrix (Fin 2) (Fin 2) ℂ) :
    (TGLExt.Jconj z).vec = star z.vec ∘ Prod.swap := by
  funext ⟨a, b⟩
  rfl

/-! (2) o vacuo de Tomita do estado traco -/

noncomputable def rhoTr : Matrix (Fin 2) (Fin 2) ℂ := (2⁻¹ : ℂ) • 1

noncomputable def cHalf : ℂ := (((Real.sqrt 2)⁻¹ : ℝ) : ℂ)

theorem cHalf_sq : cHalf * cHalf = (2⁻¹ : ℂ) := by
  unfold cHalf
  rw [← Complex.ofReal_mul, ← mul_inv, Real.mul_self_sqrt (by norm_num)]
  push_cast
  ring

theorem cHalf_star : star cHalf = cHalf := by
  unfold cHalf
  exact Complex.conj_ofReal _

theorem cHalf_nonneg : (0 : ℂ) ≤ cHalf := by
  unfold cHalf
  exact Complex.zero_le_real.mpr (by positivity)

theorem omega_trace_state :
    TGLExt.Omega rhoTr = cHalf • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  unfold TGLExt.Omega rhoTr
  apply CFC.sqrt_unique
  · rw [smul_mul_smul_comm, one_mul, cHalf_sq]
  · exact Matrix.nonneg_iff_posSemidef.mpr (Matrix.PosSemidef.one.smul cHalf_nonneg)

theorem bell_is_vacuum_projector :
    vecMulVec (TGLExt.Omega rhoTr).vec (star (TGLExt.Omega rhoTr).vec) = bellProjector := by
  rw [omega_trace_state]
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [vecMulVec_apply, bellProjector, cHalf_star, cHalf_sq]

theorem ptr_bell_is_trace_state : ptr bellProjector = rhoTr := bell_reduced_half

theorem rhoTr_posDef : rhoTr.PosDef := by
  unfold rhoTr
  exact Matrix.PosDef.one.smul (by norm_num)

theorem vacuum_unit : star (TGLExt.Omega rhoTr).vec ⬝ᵥ (TGLExt.Omega rhoTr).vec = 1 := by
  rw [Matrix.star_vec_dotProduct_vec, TGLExt.omega_conjTranspose,
    TGLExt.omega_mul_self _ rhoTr_posDef]
  simp [rhoTr]

/-! (4) a familia: imagens por U ⊗ 1 -/

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

variable (U : Matrix (Fin 2) (Fin 2) ℂ) (hU : U ∈ Matrix.unitaryGroup (Fin 2) ℂ)
include hU

theorem face_unitary : (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) ∈
    unitary (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :=
  Matrix.kronecker_mem_unitary hU (one_mem _)

theorem faceImage_idem : faceImage U * faceImage U = faceImage U := by
  have hW := (Unitary.mem_iff.mp (face_unitary U hU)).1
  rw [Matrix.star_eq_conjTranspose] at hW
  unfold faceImage
  calc _ = (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) * bellProjector *
        ((U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))ᴴ * (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))) *
        bellProjector * (U ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))ᴴ := by simp only [mul_assoc]
    _ = _ := by rw [hW, mul_one, mul_assoc _ bellProjector bellProjector, bell_idem]

omit hU in
theorem faceImage_star : star (faceImage U) = faceImage U := by
  unfold faceImage
  rw [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_mul, Matrix.conjTranspose_mul,
    Matrix.conjTranspose_conjTranspose, ← Matrix.star_eq_conjTranspose bellProjector, bell_star,
    mul_assoc]

theorem faceImage_trace : Matrix.trace (faceImage U) = 1 := by
  have hW := (Unitary.mem_iff.mp (face_unitary U hU)).1
  rw [Matrix.star_eq_conjTranspose] at hW
  unfold faceImage
  rw [Matrix.trace_mul_comm, ← mul_assoc, hW, one_mul, bell_trace_one]

theorem faceImage_reduced_half : ptr (faceImage U) = (2⁻¹ : ℂ) • 1 := by
  have hU' := (Unitary.mem_iff.mp hU).2
  rw [Matrix.star_eq_conjTranspose] at hU'
  unfold faceImage
  rw [ptr_conj, bell_reduced_half, Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, hU']

omit hU in
theorem cci_of_reduced_half (X : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ)
    (h : ptr X = (2⁻¹ : ℂ) • 1) : 1 - Matrix.trace (ptr X * ptr X) = 2⁻¹ := by
  rw [h, smul_mul_smul_comm, one_mul, Matrix.trace_smul, Matrix.trace_one]
  norm_num

noncomputable def faceWitness : GravitonShadowWitness where
  PG := faceImage U
  idem := faceImage_idem U hU
  selfadj := faceImage_star U
  trace_one := faceImage_trace U hU
  reduced_half := faceImage_reduced_half U hU
  cci_half := cci_of_reduced_half _ (faceImage_reduced_half U hU)

end Probe

#print axioms Probe.bell_swap_invariant
#print axioms Probe.bell_is_vacuum_projector
#print axioms Probe.omega_trace_state
#print axioms Probe.vacuum_unit
#print axioms Probe.faceWitness
#print axioms Probe.product_swap_invariant
#print axioms Probe.vec_Jconj
