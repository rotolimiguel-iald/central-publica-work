import Mathlib
import TheTimeHasNoRank

/-!
Sondas adversariais do AUDITOR — arquivo que DEVE FALHAR (EXIT ≠ 0): tentativas DIRETAS de provar o contrário
das pedras e uma prova sem hipóteses. Cada `example` abaixo deve produzir um erro. Se algum compilar, a pedra tem
um buraco.
F1  provar que EXISTE par de Weyl em M₂(ℂ) com (E₀₁, E₁₀);
F2  provar que F(1) do posto diag(1,0) É idempotente (o contrário de T9.a em t = 1);
F3  provar a queda estrita de pureza (T6.c) SEM hipótese alguma (g, t, x genéricos);
F4  provar que o relógio tem período 1 para κ = 1 (período errado; o certo é 2π).
-/

set_option autoImplicit false
open TGLExt TGLExt.TheTimeHasNoRank

noncomputable section

example : ∃ T H : Matrix (Fin 2) (Fin 2) ℂ, T * H - H * T = Complex.I • (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  ⟨E01, E10, by ext i j; fin_cases i <;> fin_cases j <;> simp [E01, E10, Matrix.single]⟩

example : IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1) := by
  unfold IsIdempotentElem TheAxiomAndTheFalseWitness.axiomFlow postDiag
  ext i j
  fin_cases i <;> fin_cases j <;> simp

example (g : Fin 2 → Fin 2 → ℝ) (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    purityR (dephase g t x) < purityR x := by
  simp [purityR_dephase, purityR]

example (t : ℝ) : Circle.exp (1 * (t + 1)) = Circle.exp (1 * t) := by
  simp

end
