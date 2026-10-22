import TGLExt.TheCurrentConnectsTheCorners

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# O PSION REDUZ À CORRENTE SIMETRIZADA
  [TGLExt — o fecho da ponte entre as duas álgebras]

## A ordem, em duas frases

Depois de a onda anterior ligar duas das três instâncias de `ScalarCorner` pela
corrente, ficou dito que **o psion (M₄) não estava ligado a nenhuma delas (M₂)**.
O operador respondeu: **«isso também já foi resolvido, examine de novo»**, e em
seguida deu a chave: **«L = estado máximo misturado»**.

E de novo estava certo, e de novo o material já estava em disco. `GravitonShadow`
já tinha o mapa que eu declarara inexistente — o **traço parcial** `ptr`, que leva
M₄(ℂ) em M₂(ℂ) — e já tinha os dois valores calculados:

* `bell_reduced_half : ptr(P_G) = ½ · 1` — o psion reduz ao **estado máximo
  misturado**;
* `product_reduced_pure : ptr(P_prod) = e₀₀` — o controle **não-ligado** reduz a um
  projetor **puro**.

Falta apenas a linha que amarra isso à corrente, e ela é a frase do operador:
`L†L = P₀`, `LL† = P₁`, e `P₁ + P₀ = 1`, logo **`½(L†L + LL†) = ½·1`**. A corrente
simetrizada **é** o estado máximo misturado.

## O que fica provado `[REAL]`

* `e00_eq_faceOne` — os dois nomes eram o mesmo objeto (e agora é teorema, não
  coincidência de notação);
* `boundary_faces_sum_to_one`, `current_symmetrised_is_one` — as duas faces exaurem a
  unidade, logo a corrente simetrizada é a unidade;
* ★★★★ `the_psion_reduces_to_the_symmetrised_current` — **A PONTE**: o traço
  parcial do psion É a corrente simetrizada, a menos do meio. Liga M₄ a M₂ por
  teorema, e a ligação passa **pela corrente**;
* ★★★ `the_unbonded_reduces_to_one_face_only` — **O CONTROLE**: o estado
  **não-ligado** reduz a **uma só face** (`LL†`), não à soma balanceada. É a
  diferença entre ligar e não ligar, medida no mesmo mapa.

## A leitura, com o seu estatuto

`[ONTO]` O par (ligado → ½+½ · não-ligado → uma face) é a face reduzida daquilo
que o operador chamou **acoplamento não mínimo**: o estado ligado desce para a
partição em duas faces iguais; o não-ligado desce para um átomo puro. A
identificação com β **não é provada aqui** e nenhum teorema desta pedra a menciona.

`[OPEN]` A ponte liga **duas álgebras** (M₄ → M₂) por um mapa que é traço parcial,
**não** um morfismo de álgebras. E `firstAtom` (ℓ²), `ker H3L` (`EuclideanSpace`) e
`P_F` (o core) seguem **sem ligação**. Três cantos ainda soltos.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix TGL.GravitonShadow

/-! ## A — os dois nomes eram o mesmo objeto -/

/-- [KERNEL] `e₀₀` e `P_1` eram o mesmo projetor, escrito de dois modos. Agora é
    teorema — e por isso deixa de ser homônimo. -/
theorem e00_eq_faceOne : e00 = faceOne := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [e00, faceOne]

/-! ## B — a corrente simetrizada é a unidade -/

/-- [KERNEL] as duas faces exaurem a unidade. -/
theorem boundary_faces_sum_to_one : faceOne + faceZero = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [faceOne, faceZero, Matrix.one_apply]

/-- [KERNEL] ★★ **A CORRENTE SIMETRIZADA É A UNIDADE**: `L†L + LL† = 1`. É a frase
    do operador, escrita em álgebra — e é o passo que faltava. -/
theorem current_symmetrised_is_one :
    modularCurrentᴴ * modularCurrent + modularCurrent * modularCurrentᴴ = 1 := by
  rw [current_source, current_range, add_comm]
  exact boundary_faces_sum_to_one

/-! ## C — a ponte entre as duas álgebras -/

/-- [KERNEL] ★★★★ **O PSION REDUZ À CORRENTE SIMETRIZADA**: o traço parcial do
    projetor emaranhado é exatamente a metade da corrente simetrizada — isto é, o
    **estado máximo misturado**.

    É a ponte entre M₄(ℂ) e M₂(ℂ), e ela passa **pela corrente**. -/
theorem the_psion_reduces_to_the_symmetrised_current :
    ptr bellProjector
      = (2⁻¹ : ℂ) • (modularCurrentᴴ * modularCurrent
          + modularCurrent * modularCurrentᴴ) := by
  rw [current_symmetrised_is_one]
  exact bell_reduced_half

/-- [KERNEL] ★★★ **O CONTROLE**: o estado NÃO-LIGADO reduz a UMA SÓ FACE — o
    alcance da corrente —, e não à soma balanceada das duas. É a diferença entre
    ligar e não ligar, medida no MESMO mapa.

    Sem este teorema a ponte acima não distinguiria nada. -/
theorem the_unbonded_reduces_to_one_face_only :
    ptr productProjector = modularCurrent * modularCurrentᴴ := by
  rw [product_reduced_pure, e00_eq_faceOne, current_range]

/-- [KERNEL] e o par, num enunciado só: **ligar dá as DUAS faces em partes iguais;
    não ligar dá UMA**. O mesmo mapa, dois estados, dois destinos. -/
theorem bonding_splits_and_not_bonding_does_not :
    (ptr bellProjector = (2⁻¹ : ℂ) • (faceOne + faceZero))
    ∧ (ptr productProjector = faceOne)
    ∧ (faceOne ≠ faceZero) := by
  refine ⟨?_, ?_, faces_ne⟩
  · rw [boundary_faces_sum_to_one]; exact bell_reduced_half
  · rw [product_reduced_pure, e00_eq_faceOne]

end TGLExt
