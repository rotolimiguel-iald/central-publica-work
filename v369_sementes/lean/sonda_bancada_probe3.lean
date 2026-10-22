import Mathlib
import TGL.GravitonShadow
import TGLExt.FiniteTomita

open Matrix
open scoped Kronecker ComplexOrder MatrixOrder

namespace Probe3
open TGL.GravitonShadow

noncomputable def rhoTr : Matrix (Fin 2) (Fin 2) ℂ := (2⁻¹ : ℂ) • 1

theorem rhoTr_posDef : rhoTr.PosDef := by
  unfold rhoTr
  exact Matrix.PosDef.one.smul (by norm_num)

theorem vacuum_unit : star (TGLExt.Omega rhoTr).vec ⬝ᵥ (TGLExt.Omega rhoTr).vec = 1 := by
  rw [Matrix.star_vec_dotProduct_vec, TGLExt.omega_conjTranspose,
    TGLExt.omega_mul_self _ rhoTr_posDef]
  simp [rhoTr]

/-- o estado vetorial do vacuo = o estado de Gibbs do traco (GNS), via vec_mul_eq_mulVec -/
theorem vacuum_state (a : Matrix (Fin 2) (Fin 2) ℂ) :
    star (TGLExt.Omega rhoTr).vec ⬝ᵥ
      ((1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ a) *ᵥ (TGLExt.Omega rhoTr).vec =
      TGLExt.gibbs rhoTr a := by
  rw [← Matrix.vec_mul_eq_mulVec, Matrix.star_vec_dotProduct_vec,
    TGLExt.gibbs_eq_frob_omega _ rhoTr_posDef]
  rfl

/-- o traco contra P_G reproduz o estado traco na face onde a age -/
theorem bell_reads_trace_state (a : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.trace (bellProjector * ((1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ a)) =
      TGLExt.gibbs rhoTr a := by
  simp only [TGLExt.gibbs, rhoTr, Matrix.trace, Matrix.diag, Matrix.mul_apply,
    Fintype.sum_prod_type, Fin.sum_univ_two, bellProjector, Matrix.of_apply,
    Matrix.kronecker_apply, Matrix.one_apply, Matrix.smul_apply]
  simp

/-- J antiunitario (conj ∘ troca) fixa P_G: a acao de J sobre |v⟩⟨v| e' (P ∘ swap).map star -/
theorem bell_J_fixed :
    (bellProjector.submatrix Prod.swap Prod.swap).map star = bellProjector := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [bellProjector, map_ofNat]

/-- a outra reducao: ptr apos a troca = traco sobre o PRIMEIRO fator -/
theorem ptr_swap (X : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) (i j : Fin 2) :
    ptr (X.submatrix Prod.swap Prod.swap) i j = ∑ k : Fin 2, X (k, i) (k, j) := rfl

end Probe3

#print axioms Probe3.vacuum_unit
#print axioms Probe3.vacuum_state
#print axioms Probe3.bell_reads_trace_state
#print axioms Probe3.bell_J_fixed
#print axioms Probe3.ptr_swap
