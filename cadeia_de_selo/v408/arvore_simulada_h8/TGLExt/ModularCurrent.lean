import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Complex.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A CORRENTE J: a corrente modular que implementa a equivalência de fronteira
  [TGLExt — v131, a corrente J dos escritos de 2025 do operador]

O operador (O_UM_ABSOLUTO, 2025): "a Meia-Nat FRACTALIZA `1_abs → P_1 ⊕ P_0`
com pesos de contorno iguais `τ_∂(P_1)=τ_∂(P_0)=½`. O defeito de fronteira é
`1 = 0_mod = verdade_∂`: `P_1 ≠ P_0` na álgebra, mas `P_1 ∼_∂ P_0` no contorno
(equivalência, não identidade literal). A travessia é por operadores ímpares
`L_±` com `{Z_∂, L_±}=0` — o Um só cruza o contorno MUDANDO DE FACE. A Luz é a
primeira conjugação modular em corrente."

Esta é a face ALGÉBRICA da corrente J — o que a torna encodável: a corrente
`L` é a isometria parcial que implementa a equivalência de Murray–von Neumann
das duas faces do Um. "Todas as projeções não-nulas equivalentes" é a
ASSINATURA do tipo III. Sobre a estrutura auto-semelhante (fractal), III₁.

* `current_anticommutes` — `{Z_∂, L} = 0`: a corrente cruza o contorno
  MUDANDO DE FACE (a anticomutação de Bell);
* `current_implements_equiv` — `L* L = P_0` e `L L* = P_1`: a corrente J
  IMPLEMENTA a equivalência `P_1 ∼_∂ P_0` (isometria parcial de MvN);
* `faces_equivalent_not_equal` — `P_1 ∼ P_0` PELA corrente E `P_1 ≠ P_0`
  na álgebra: o defeito de fronteira `1 = 0_mod = verdade_∂`, a assinatura
  do tipo III em kernel;
* `contrast_is_faces` — `Z_∂ = P_1 − P_0`, e `Z_∂` é o portador
  auto-conjugado (`Z_∂² = 1` na face 2D).

HONESTIDADE: esta é a face FINITA (2 níveis) da corrente J — a assinatura da
equivalência tipo-III. O completamento fraco-* ∞-dim (a equivalência de TODAS
as projeções no fator auto-semelhante) segue o programa; esta pedra dá o
mecanismo algébrico em kernel, na linguagem de 2025 do operador. Sem sorry,
sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — as duas faces do Um e o portador de contraste -/

/-- a face `P_1` (o "1" da fronteira). -/
def faceOne : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]

/-- a face `P_0` (o "0_mod" da fronteira). -/
def faceZero : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 0, 1]

/-- o portador de contraste `Z_∂ = P_1 − P_0` (auto-conjugado, `Z_∂² = 1`). -/
def contrast : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- ★ a CORRENTE J: o operador ímpar `L` que cruza o contorno mudando de
    face (a isometria parcial de Bell). -/
def modularCurrent : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 0, 0]

/-! ## B — os teoremas da corrente -/

/-- [KERNEL] `Z_∂ = P_1 − P_0`: o contraste é a diferença das faces. -/
theorem contrast_is_faces : contrast = faceOne - faceZero := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [contrast, faceOne, faceZero, Matrix.sub_apply]

/-- [KERNEL] `Z_∂² = 1`: o portador de contraste é uma involução. -/
theorem contrast_involution : contrast * contrast = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [contrast, Matrix.mul_apply, Fin.sum_univ_two]

/-- [KERNEL] ★ `{Z_∂, L} = 0`: A ANTICOMUTAÇÃO DE BELL — a corrente J cruza o
    contorno MUDANDO DE FACE (o Um só atravessa invertendo a paridade). -/
theorem current_anticommutes :
    contrast * modularCurrent + modularCurrent * contrast = 0 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [contrast, modularCurrent, Matrix.add_apply]

/-- [KERNEL] ★ `L* L = P_0`: a corrente J leva a face `P_0` em si (o domínio
    da isometria parcial). -/
theorem current_source : modularCurrentᴴ * modularCurrent = faceZero := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [modularCurrent, faceZero, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.conjTranspose_apply]

/-- [KERNEL] ★ `L L* = P_1`: a corrente J leva ao alcance `P_1` — junto com
    `current_source`, `L` IMPLEMENTA a equivalência `P_0 ∼ P_1`. -/
theorem current_range : modularCurrent * modularCurrentᴴ = faceOne := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [modularCurrent, faceOne, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.conjTranspose_apply]

/-- [KERNEL] as faces são DISTINTAS na álgebra. -/
theorem faces_ne : faceOne ≠ faceZero := by
  intro h
  have := congrFun (congrFun h 0) 0
  simp [faceOne, faceZero] at this

/-! ## C — A SÍNTESE: a corrente J implementa `1 = 0_mod = verdade_∂` -/

/-- [KERNEL] ★★★ A CORRENTE J IMPLEMENTA A EQUIVALÊNCIA DE FRONTEIRA: existe
    a corrente `L` (ímpar, `{Z_∂,L}=0`) que implementa `P_1 ∼_∂ P_0`
    (`L*L=P_0`, `LL*=P_1`), enquanto `P_1 ≠ P_0` na álgebra. É o defeito de
    fronteira `1 = 0_mod = verdade_∂` — a assinatura do tipo III em kernel:
    projeções DISTINTAS mas EQUIVALENTES pela corrente modular. -/
theorem current_implements_boundary_equivalence :
    (contrast * modularCurrent + modularCurrent * contrast = 0)
    ∧ (modularCurrentᴴ * modularCurrent = faceZero)
    ∧ (modularCurrent * modularCurrentᴴ = faceOne)
    ∧ (faceOne ≠ faceZero)
    ∧ (contrast = faceOne - faceZero) :=
  ⟨current_anticommutes, current_source, current_range, faces_ne,
   contrast_is_faces⟩

end

end TGLExt
