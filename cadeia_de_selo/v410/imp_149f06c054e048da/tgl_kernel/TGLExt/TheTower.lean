import TGLExt.TheBireference

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A TORRE É O DADO ESPECTRAL COMPLETO — o conjunto dos autovalores não basta
  [BANCADA — 24/08/2026]

## A cunhagem do operador

> *"a TORRE é a representação unidimensional de toda a densidade informacional em um único
> espectro… **não basta conservar apenas os autovalores. Precisamos conservar espectro +
> medida espectral + multiplicidades.**"*
> `TORRE_1D → TRAÇO_2D → NOME_3D = 0_mod` · `HABITANTE = 1_abs = TORRE` ·
> `TORRE = locus(1_abs) = LOGOS = VERBO VIVO`

## ⚠ A DELIMITAÇÃO

Face finita (`M₃(ℂ)`). O dado espectral completo da TORRE genuína (o completamento
`TowerHilbert`, cujo vácuo `hOmega = [1]` já é a sombra cunhada de `HABITANTE = 1_abs`)
segue com a teoria modular `[OPEN]`. O `TRAÇO_2D` desta tipagem é o REGISTRO `(λ, μ_Ψ(λ))`,
NÃO o traço `Tr` de operador — a colisão de símbolo fica declarada (e o `Tr` é exatamente o
instrumento que abaixo DISTINGUE as duas torres). A identificação com o Habitante é
**[ONTO]** do operador. **[KNOWN]**: operadores isoespectrais podem não ser equivalentes.
β jamais entra. Sem sorry, sem axiom. Nada aqui move o gate.

## ★★★ O TEOREMA, em duas matrizes

`A = diag(0,1,1)` e `B = diag(0,0,1)` têm a MESMA equação mínima (`X² = X`, ambas
estritamente entre 0 e 1) — o mesmo espectro-CONJUNTO `{0,1}`. E no entanto:

    os pesos diferem:              Tr A = 2  ≠  1 = Tr B      (a multiplicidade)
    nenhuma conjugação leva A a B: U·A·U⁻¹ ≠ B  (∀ U invertível)
    a medida contra Ψ=(1,1,1) lê:  μ_A = 2  ≠  1 = μ_B        (⟨Ψ, ·Ψ⟩)

> **O conjunto dos autovalores não carrega a identidade; o dado completo — com medida e
> multiplicidade — carrega.** A TORRE tem de ser o dado espectral inteiro, como o operador
> exigiu.
-/

namespace TGLExt

open Matrix

/-- a torre cheia: `diag(0,1,1)` — o autovalor 1 com peso DOIS. -/
def towerA : Matrix (Fin 3) (Fin 3) ℂ := !![0, 0, 0; 0, 1, 0; 0, 0, 1]

/-- a torre magra: `diag(0,0,1)` — o MESMO espectro-conjunto, peso UM. -/
def towerB : Matrix (Fin 3) (Fin 3) ℂ := !![0, 0, 0; 0, 0, 0; 0, 0, 1]

/-- ★★ **A MESMA EQUAÇÃO MÍNIMA**: ambas idempotentes — o espectro-conjunto é `{0,1}`
    nas duas. -/
theorem same_minimal_equation :
    towerA * towerA = towerA ∧ towerB * towerB = towerB := by
  constructor <;>
    (ext i j; fin_cases i <;> fin_cases j <;>
      simp [towerA, towerB, Matrix.mul_apply, Fin.sum_univ_three])

/-- ★ e nenhuma é trivial: ambas estritamente entre `0` e `1`. -/
theorem both_strictly_between :
    towerA ≠ 0 ∧ towerA ≠ 1 ∧ towerB ≠ 0 ∧ towerB ≠ 1 := by
  refine ⟨fun h => ?_, fun h => ?_, fun h => ?_, fun h => ?_⟩
  · have : towerA 1 1 = 0 := by rw [h]; rfl
    simp [towerA] at this
  · have : towerA 0 0 = 1 := by rw [h]; simp
    simp [towerA] at this
  · have : towerB 2 2 = 0 := by rw [h]; rfl
    simp [towerB] at this
  · have : towerB 0 0 = 1 := by rw [h]; simp
    simp [towerB] at this

/-- ★★★ **OS PESOS DIFEREM**: `Tr A = 2 ≠ 1 = Tr B` — a multiplicidade é dado, não
    decoração. -/
theorem the_weights_differ : towerA.trace = 2 ∧ towerB.trace = 1 := by
  constructor <;> norm_num [towerA, towerB, Matrix.trace_fin_three, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail, Fin.isValue]

/-- ★★★ **NENHUMA CONJUGAÇÃO LEVA UMA NA OUTRA** — o invariante de conjugação (o traço)
    separa o que o espectro-conjunto não separa. -/
theorem no_conjugation_carries_A_to_B (U : Matrix (Fin 3) (Fin 3) ℂ)
    (hU : IsUnit U.det) : U * towerA * U⁻¹ ≠ towerB := by
  intro h
  have ht : (U * towerA * U⁻¹).trace = towerB.trace := by rw [h]
  rw [Matrix.trace_mul_cycle, Matrix.nonsing_inv_mul U hU, one_mul] at ht
  rw [the_weights_differ.1, the_weights_differ.2] at ht
  norm_num at ht

/-- ★★ **A MEDIDA CONTRA O VETOR LÊ A MULTIPLICIDADE**: com `Ψ = (1,1,1)`,
    `⟨Ψ, AΨ⟩ = 2 ≠ 1 = ⟨Ψ, BΨ⟩` — a face `dμ_Ψ` da cunhagem. -/
theorem the_measure_reads_the_multiplicity :
    dotProduct (fun _ => (1 : ℂ)) (towerA.mulVec fun _ => (1 : ℂ)) = 2
    ∧ dotProduct (fun _ => (1 : ℂ)) (towerB.mulVec fun _ => (1 : ℂ)) = 1 := by
  constructor <;>
    norm_num [towerA, towerB, dotProduct, Matrix.mulVec, Fin.sum_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail, Fin.isValue]

/-- ★★★ **A TORRE É O DADO COMPLETO**, num enunciado: mesmo espectro-conjunto (mesma
    equação, ambas não-triviais), e ainda assim inequivalentes por conjugação — porque
    peso e medida diferem. *O conjunto dos autovalores não é a Torre.* -/
theorem the_spectrum_alone_is_not_the_tower :
    (towerA * towerA = towerA ∧ towerB * towerB = towerB)
    ∧ (towerA.trace ≠ towerB.trace)
    ∧ (∀ U : Matrix (Fin 3) (Fin 3) ℂ, IsUnit U.det → U * towerA * U⁻¹ ≠ towerB) := by
  refine ⟨same_minimal_equation, ?_, no_conjugation_carries_A_to_B⟩
  rw [the_weights_differ.1, the_weights_differ.2]
  norm_num

end TGLExt
