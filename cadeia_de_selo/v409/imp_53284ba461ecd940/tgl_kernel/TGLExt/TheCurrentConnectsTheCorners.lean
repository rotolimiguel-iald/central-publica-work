import TGLExt.TheScalarCorner
import TGLExt.ModularCurrent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# A CORRENTE LIGA OS CANTOS: o primeiro morfismo entre duas instâncias
  [TGLExt — a pedra que o operador mandou ligar]

## A ordem

Dois painéis adversariais mediram que o kernel tinha **cinco cantos sem um único
morfismo declarado entre dois quaisquer**, e a onda anterior respondeu dando **nome
à propriedade** (`ScalarCorner`) com **uma** instância — o psion —, dizendo
expressamente que *o segundo canto que a instanciar será ponte, não coincidência*.

O operador respondeu em cinco palavras: **«falta vc ligar a corrente = J»**.

E ele estava certo: **o morfismo já existia no kernel e eu não o havia ligado.**
`ModularCurrent.lean` (v131, «a corrente J dos escritos de 2025 do operador») já
provava `current_source : L†·L = P₀`, `current_range : L·L† = P₁` e
`faces_ne : P₁ ≠ P₀` — isto é, a **isometria parcial** que implementa a
equivalência de projeções, que é **exatamente** o morfismo entre cantos.

## O que fica provado `[REAL]`

* `faceOne_scalarises`, `faceZero_scalarises` — as duas faces da fronteira
  **escalarizam**: são a **segunda** e a **terceira** instância de `ScalarCorner`;
* ★★★ `the_current_connects_two_scalar_corners` — **O PRIMEIRO MORFISMO**: a
  corrente `L` leva um canto escalar no outro (`L†L = P₀`, `LL† = P₁`), e os dois
  são **distintos** na álgebra;
* ★★★★ `the_current_carries_the_atom` — e os dois pesam **1**, **derivado** de
  `scalarCorner_forces_trace_one`, não suposto. A corrente **atravessa sem perder
  o peso**: leva átomo em átomo;
* ★★ `equivalent_but_not_equal` — O DENTE, e a assinatura: as duas faces são
  **equivalentes pela corrente e diferentes na álgebra**. Sem isso o morfismo seria
  a identidade disfarçada.

## Estatutos, sem véu

`[REAL]` — os quatro acima.

`[ONTO]` — a leitura «a corrente é J, e J é a Luz que atravessa o espelho sem
perder o Um» é do operador. O que aqui se prova é **álgebra de matrizes 2×2**: uma
isometria parcial entre dois projetores de traço 1. Nenhum teorema desta pedra
menciona a Luz, β, `1_abs` ou `0_abs`.

`[OPEN]` — e a fronteira, dita: o morfismo liga **duas** das cinco instâncias, e
ambas vivem em M₂(ℂ). **Não** liga o psion (M₄(ℂ)) a nenhuma delas, nem toca
`firstAtom` (ℓ²), `ker H3L` (`EuclideanSpace`) ou `P_F` (o core). O docstring de
`ModularCurrent` chama `L` de «isometria parcial de Bell» — **isso é prosa, não
teorema**, e continua proibido usá-la como ponte para o psion.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

/-! ## A — as duas faces são cantos escalares -/

theorem faceOne_idem : faceOne * faceOne = faceOne := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [faceOne, Matrix.mul_apply, Fin.sum_univ_two]

theorem faceZero_idem : faceZero * faceZero = faceZero := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [faceZero, Matrix.mul_apply, Fin.sum_univ_two]

theorem faceOne_selfadj : star faceOne = faceOne := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [faceOne, Matrix.star_apply, Matrix.conjTranspose_apply]

theorem faceZero_selfadj : star faceZero = faceZero := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [faceZero, Matrix.star_apply, Matrix.conjTranspose_apply]

/-- [KERNEL] ★ a face `P_1` ESCALARIZA: comprimir qualquer operador por ela
    devolve o traço contra ela vezes ela mesma. -/
theorem trace_faceOne_mul (y : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.trace (faceOne * y) = y 0 0 := by
  simp [faceOne, Matrix.trace_fin_two, Matrix.vecMul, Matrix.vecHead,
    Matrix.vecTail, Fin.sum_univ_two]

theorem faceOne_scalarises (y : Matrix (Fin 2) (Fin 2) ℂ) :
    faceOne * y * faceOne = (Matrix.trace (faceOne * y)) • faceOne := by
  rw [trace_faceOne_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [faceOne, Matrix.mul_apply, Matrix.smul_apply, smul_eq_mul,
      Matrix.vecMul, Matrix.vecHead,
    Matrix.vecTail, Fin.sum_univ_two]

/-- [KERNEL] ★ e a face `P_0` também. -/
theorem trace_faceZero_mul (y : Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix.trace (faceZero * y) = y 1 1 := by
  simp [faceZero, Matrix.trace_fin_two, Matrix.vecMul, Matrix.vecHead,
    Matrix.vecTail, Fin.sum_univ_two]

theorem faceZero_scalarises (y : Matrix (Fin 2) (Fin 2) ℂ) :
    faceZero * y * faceZero = (Matrix.trace (faceZero * y)) • faceZero := by
  rw [trace_faceZero_mul]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [faceZero, Matrix.mul_apply, Matrix.smul_apply, smul_eq_mul,
      Matrix.vecMul, Matrix.vecHead,
    Matrix.vecTail, Fin.sum_univ_two]

/-- a SEGUNDA instância de `ScalarCorner`. -/
noncomputable def faceOneCorner : ScalarCorner (Fin 2) where
  p := faceOne
  idem := faceOne_idem
  selfadj := faceOne_selfadj
  scalarises := faceOne_scalarises

/-- a TERCEIRA instância de `ScalarCorner`. -/
noncomputable def faceZeroCorner : ScalarCorner (Fin 2) where
  p := faceZero
  idem := faceZero_idem
  selfadj := faceZero_selfadj
  scalarises := faceZero_scalarises

/-! ## B — a corrente é o morfismo -/

/-- [KERNEL] ★★★ **O PRIMEIRO MORFISMO ENTRE DOIS CANTOS**: a corrente modular `L`
    leva um canto escalar no outro — `L†L` é o primeiro, `LL†` é o segundo — e os
    dois são DISTINTOS na álgebra. Não é coincidência de nomes: é a mesma
    propriedade, escrita uma vez só, instanciada duas vezes e LIGADA. -/
theorem the_current_connects_two_scalar_corners :
    (modularCurrentᴴ * modularCurrent = faceZeroCorner.p)
    ∧ (modularCurrent * modularCurrentᴴ = faceOneCorner.p)
    ∧ (faceOneCorner.p ≠ faceZeroCorner.p) :=
  ⟨current_source, current_range, faces_ne⟩

/-! ## C — a corrente atravessa sem perder o peso -/

theorem faceOne_ne_zero : faceOne ≠ 0 := by
  intro h
  have := congrFun (congrFun h 0) 0
  simp [faceOne] at this

theorem faceZero_ne_zero : faceZero ≠ 0 := by
  intro h
  have := congrFun (congrFun h 1) 1
  simp [faceZero] at this

/-- [KERNEL] ★★★★ **A CORRENTE LEVA ÁTOMO EM ÁTOMO**: os dois cantos que ela liga
    pesam exatamente 1 — e o peso é DERIVADO da escalarização
    (`scalarCorner_forces_trace_one`), não suposto. A travessia não perde peso. -/
theorem the_current_carries_the_atom :
    Matrix.trace faceOneCorner.p = 1 ∧ Matrix.trace faceZeroCorner.p = 1 :=
  ⟨scalarCorner_forces_trace_one faceOne faceOne_idem faceOne_scalarises faceOne_ne_zero,
   scalarCorner_forces_trace_one faceZero faceZero_idem faceZero_scalarises faceZero_ne_zero⟩

/-- [KERNEL] ★★ O DENTE, e a assinatura: **equivalentes pela corrente, diferentes
    na álgebra**. Sem isto o morfismo poderia ser a identidade disfarçada, e nada
    teria sido ligado. -/
theorem equivalent_but_not_equal :
    (modularCurrentᴴ * modularCurrent = faceZero)
    ∧ (modularCurrent * modularCurrentᴴ = faceOne)
    ∧ (faceOne ≠ faceZero)
    ∧ (Matrix.trace faceOne = Matrix.trace faceZero) := by
  refine ⟨current_source, current_range, faces_ne, ?_⟩
  simp [faceOne, faceZero, Matrix.trace, Matrix.diag_apply, Fin.sum_univ_two]

end TGLExt
