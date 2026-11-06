import TGLExt.TheScalarCorner
import Mathlib.LinearAlgebra.Matrix.Kronecker

set_option autoImplicit false

/-!
Reflexão no canto de Bell do kernel e pulso de Pauli coletivo.
Igualdades finitas no modelo. A realização da reflexão na propagação permanece aberta.
-/

noncomputable section
namespace TGLExt.ReflexaoBellTroca
open Matrix TGL.GravitonShadow
open scoped Kronecker

abbrev Bit := Fin 2
abbrev Pair := Bit × Bit
abbrev PairMat := Matrix Pair Pair ℂ

/-- A matriz de Pauli Y nas convenções |0⟩, |1⟩. -/
def pauliY : Matrix Bit Bit ℂ := Matrix.of fun i j =>
  if i = j then 0 else if i = 0 then -Complex.I else Complex.I

/-- Permutação dos dois índices da base de produto. -/
def swap : PairMat := Matrix.of fun i j => if i = (j.2, j.1) then 1 else 0

def collectiveY : PairMat := pauliY ⊗ₖ pauliY

def reflection : PairMat := (2 : ℂ) • psionCorner.p - 1

/-- Igualdade no espaço inteiro de dimensão quatro. -/
theorem reflection_eq_neg_collectiveY_swap : reflection = -(collectiveY * swap) := by
  ext ⟨a, b⟩ ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    norm_num [reflection, psionCorner, bellProjector, collectiveY, pauliY, swap,
      Matrix.mul_apply, Fintype.sum_prod_type, Fin.sum_univ_two, Matrix.one_apply,
      Complex.I_mul_I]

/-- Sur le sous-espace fixé pela troca, as ações diferem por fase global −1. -/
theorem reflection_on_swap_fixed (ψ : Pair → ℂ) (h : swap *ᵥ ψ = ψ) :
    reflection *ᵥ ψ = -(collectiveY *ᵥ ψ) := by
  rw [reflection_eq_neg_collectiveY_swap, Matrix.neg_mulVec, ← Matrix.mulVec_mulVec, h]

/-- Para toda matriz invariante por conjugação pela troca, os dois pulsos induzem
exatamente a mesma matriz de saída. Inclui toda densidade apoiada no triplete. -/
theorem reflection_conjugation_on_swap_invariant (ρ : PairMat)
    (h : swap * ρ * swapᴴ = ρ) :
    reflection * ρ * reflectionᴴ = collectiveY * ρ * collectiveYᴴ := by
  rw [reflection_eq_neg_collectiveY_swap, Matrix.conjTranspose_neg, Matrix.conjTranspose_mul]
  calc
    -(collectiveY * swap) * ρ * -(swapᴴ * collectiveYᴴ) =
        collectiveY * (swap * ρ * swapᴴ) * collectiveYᴴ := by
          simp [Matrix.mul_assoc]
    _ = collectiveY * ρ * collectiveYᴴ := by rw [h]

end TGLExt.ReflexaoBellTroca

#print axioms TGLExt.ReflexaoBellTroca.reflection_eq_neg_collectiveY_swap
#print axioms TGLExt.ReflexaoBellTroca.reflection_on_swap_fixed
#print axioms TGLExt.ReflexaoBellTroca.reflection_conjugation_on_swap_invariant
