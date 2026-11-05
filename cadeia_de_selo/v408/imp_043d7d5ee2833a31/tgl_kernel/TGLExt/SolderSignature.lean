import TGLExt.SolderField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A ASSINATURA PLENA DA SOLDA: (1,3) em todo ponto
  [TGLExt — item A da ordem de fechamento: a condicional «solda»]

O v63 provou `det g = −(det e)²` e NOMEOU o resto: «a assinatura plena
de Sylvester é [KNOWN clássico, kernel OPEN]». O v107 construiu o campo
`theSolderField x = diag((1+x₀²)², −1, −1, −1)`. Esta pedra FECHA a
assinatura plena PARA O CAMPO CONSTRUÍDO — sem teoria de inércia
externa: a solda é diagonal explícita, e a inércia sai entrada a
entrada, em TODO ponto do espaço-tempo:

* ★ `theSolderField_inertia` — o DADO DE INÉRCIA completo, como iff:
  a entrada `i` é positiva ⟺ `i = 0`; negativa ⟺ `i ≠ 0` — exatamente
  UMA direção temporal e TRÊS espaciais, em todo `x`;
* `theSolderField_offdiag` — fora da diagonal é zero (a base do frame
  curvo já diagonaliza a solda: autovalores = entradas);
* ★ `theSolderField_timelike_basis` / `theSolderField_spacelike_basis`
  — a forma quadrática nos eixos: `Q(e₀) > 0` e `Q(eᵢ) < 0` (i ≠ 0) —
  o cone de luz tem interior e exterior em todo ponto;
* `theSolderField_signature_sum` — a soma dos sinais é `1 − 3 = −2`
  (a marca numérica da assinatura lorentziana 4D).

HONESTIDADE: fecha a assinatura PARA O HABITANTE (o campo do v107,
diagonal por construção); a lei de inércia de Sylvester GERAL (base
arbitrária) segue [KNOWN clássico] — nomeada, não usada: aqui nada a
requer, porque a diagonalização é explícita. β JAMAIS entra no Lean.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

/-- Abreviação local: a entrada diagonal da solda no ponto `x`. -/
private theorem solder_diag_entry (x : Fin 4 → ℝ) (i : Fin 4) :
    theSolderField x i i = if i = 0 then profileFn x ^ 2 else -1 := by
  rw [theSolderField_eq]
  exact Matrix.diagonal_apply_eq _ i

/-- ★ O DADO DE INÉRCIA COMPLETO, em todo ponto: positiva ⟺ temporal
    (`i = 0`); negativa ⟺ espacial (`i ≠ 0`). Uma direção de tempo,
    três de espaço — a assinatura (1,3), entrada a entrada. -/
theorem theSolderField_inertia (x : Fin 4 → ℝ) (i : Fin 4) :
    (0 < theSolderField x i i ↔ i = 0)
      ∧ (theSolderField x i i < 0 ↔ i ≠ 0) := by
  rw [solder_diag_entry]
  by_cases hi : i = 0
  · rw [if_pos hi]
    exact ⟨iff_of_true (pow_pos (profileFn_pos x) 2) hi,
           iff_of_false (not_lt.mpr (pow_pos (profileFn_pos x) 2).le)
             (fun h => h hi)⟩
  · rw [if_neg hi]
    exact ⟨iff_of_false (by norm_num) hi,
           iff_of_true (by norm_num) hi⟩

/-- Fora da diagonal a solda é ZERO em todo ponto: a base do frame curvo
    já a diagonaliza — os autovalores são as entradas. -/
theorem theSolderField_offdiag (x : Fin 4 → ℝ) (i j : Fin 4) (hij : i ≠ j) :
    theSolderField x i j = 0 := by
  rw [theSolderField_eq]
  exact Matrix.diagonal_apply_ne _ hij

/-- ★ O EIXO TEMPORAL: `Q(e₀) = g₀₀ > 0` em todo ponto — o interior do
    cone de luz existe em toda parte. -/
theorem theSolderField_timelike_basis (x : Fin 4 → ℝ) :
    0 < theSolderField x 0 0 :=
  ((theSolderField_inertia x 0).1).mpr rfl

/-- ★ OS EIXOS ESPACIAIS: `Q(eᵢ) = gᵢᵢ < 0` para `i ≠ 0` — o exterior
    do cone existe em toda parte. -/
theorem theSolderField_spacelike_basis (x : Fin 4 → ℝ) (i : Fin 4)
    (hi : i ≠ 0) : theSolderField x i i < 0 :=
  ((theSolderField_inertia x i).2).mpr hi

/-- A MARCA NUMÉRICA da assinatura: a soma dos sinais das entradas
    diagonais é `1 − 3 = −2` em todo ponto (uma temporal, três
    espaciais). -/
theorem theSolderField_signature_sum (x : Fin 4 → ℝ) :
    (∑ i : Fin 4, Real.sign (theSolderField x i i)) = -2 := by
  have h0 : Real.sign (theSolderField x 0 0) = 1 :=
    Real.sign_of_pos (theSolderField_timelike_basis x)
  have hs : ∀ i : Fin 4, i ≠ 0 → Real.sign (theSolderField x i i) = -1 :=
    fun i hi => Real.sign_of_neg (theSolderField_spacelike_basis x i hi)
  rw [Fin.sum_univ_four]
  rw [h0, hs 1 (by decide), hs 2 (by decide), hs 3 (by decide)]
  norm_num

end

end TGLExt
