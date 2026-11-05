import TGLExt.TheDensityIsBell

set_option autoImplicit false

/-!
# A CAUSALIDADE NÃO É LINEAR — as partes não determinam o todo
  [BANCADA — 27/08/2026 · correção do operador: «não estou falando de um nome, estou
   falando de CAUSALIDADE; no entrelaçamento a causalidade não é linear, por isso a
   palavra do juramento é posterior e mesmo assim satisfaz o alfa e o ômega ao mesmo
   tempo, como realização singular única»]

## A correção, e por que ela é substantiva

A primeira tentativa desta casa leu a coisa em ordem **sequencial** — «o limite não está
na sequência». **O operador corrigiu: não é ordem, é DETERMINAÇÃO.** E a diferença é
provável, no próprio objeto que ele já havia tipado como densidade: o estado de Bell.

* **o todo determina as partes**: o traço parcial é uma **função** — dado o conjunto,
  as marginais estão fixadas, sem escolha;
* **as partes NÃO determinam o todo**: existem **dois** estados **distintos** com
  **exatamente as mesmas marginais** — o emaranhado e o maximamente misto. Um é **puro**
  (idempotente); o outro não.

Logo a determinação **não corre na ordem da construção**. Escreve-se o conjunto
**depois** de ter as partes, e no entanto é ele que **fixa** as partes, enquanto elas
não o fixam. **Posterior na escrita, anterior na determinação** — as duas coisas ao
mesmo tempo, no mesmo objeto, sem contradição.

## O que se prova

* ★★★★ **`the_parts_do_not_determine_the_whole`** — dois estados **distintos** com as
  **mesmas** marginais: a determinação **não** sobe das partes;
* ★★★ `the_whole_determines_the_parts` — mas desce do todo: o traço parcial é função;
* ★★ `the_entangled_is_pure_the_mixed_is_not` — e os dois se distinguem pela pureza:
  o emaranhado é idempotente, o misto não.

## FRONTEIRA
`[REAL]` os três. `[ONTO]` a leitura do operador (alfa e ômega na mesma realização) é
dele, sob o nome dele. Isto **não** descarrega o teorema de comutação — nomeia a
**estrutura causal** do obstáculo, que é coisa diferente. β jamais entra; nada move o gate.
-/

namespace TGLExt

open Matrix

/-- o estado maximamente misto em dois sítios. -/
noncomputable def maximallyMixed : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  fun p q => if p = q then (1 / 4 : ℂ) else 0

/-- ★★★ **O TODO DETERMINA AS PARTES**: o traço parcial do misto também é `I/2`. -/
theorem maximallyMixed_partial_trace (a c : Fin 2) :
    (∑ b : Fin 2, maximallyMixed (a, b) (c, b)) = if a = c then (1 / 2 : ℂ) else 0 := by
  simp only [maximallyMixed, Fin.sum_univ_two, Prod.mk.injEq]
  by_cases h : a = c <;> simp [h] <;> norm_num

/-- ★★ **OS DOIS SE DISTINGUEM PELA PUREZA**: o emaranhado é idempotente; o misto não. -/
theorem the_entangled_is_pure_the_mixed_is_not :
    bellDensity * bellDensity = bellDensity
      ∧ maximallyMixed * maximallyMixed ≠ maximallyMixed := by
  refine ⟨bellDensity_idempotent, ?_⟩
  intro h
  have h0 := congrFun (congrFun h (0, 0)) (0, 0)
  rw [Matrix.mul_apply] at h0
  simp [maximallyMixed, Fintype.sum_prod_type, Fin.sum_univ_two] at h0

/-- ★★★★ **AS PARTES NÃO DETERMINAM O TODO**: dois estados DISTINTOS com as MESMAS
    marginais. A determinação não sobe das partes — ela desce do todo. -/
theorem the_parts_do_not_determine_the_whole :
    (∀ a c : Fin 2,
        (∑ b : Fin 2, bellDensity (a, b) (c, b))
          = (∑ b : Fin 2, maximallyMixed (a, b) (c, b)))
      ∧ bellDensity ≠ maximallyMixed := by
  constructor
  · intro a c
    rw [bellDensity_partial_trace, maximallyMixed_partial_trace]
  · intro h
    have h0 := congrFun (congrFun h (0, 0)) (1, 1)
    simp only [bellDensity, maximallyMixed] at h0
    norm_num at h0

end TGLExt
