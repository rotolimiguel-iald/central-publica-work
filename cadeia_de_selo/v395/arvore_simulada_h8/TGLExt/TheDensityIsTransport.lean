import TGLExt.TheFoldIsNotADistance

set_option autoImplicit false

/-!
# DENSIDADE É A GEOMETRIA MEDINDO A LUZ EM TRANSPORTE
  [BANCADA — 26/08/2026 · tipagem do operador: «densidade = transporte da luz»;
   «densidade é a geometria medindo a Luz em transporte = neutrino»]

## A tensão que a tipagem resolve

O corpus do operador dizia o neutrino como «fuga do condensado», **sem modulação
geométrica**. Isso parecia dizer que a geometria não o alcança. A tipagem nova desfaz a
confusão, e a distinção é **estrutural, não retórica**:

    NÃO SER FIXADO pela geometria  ≠  NÃO SER MENSURÁVEL pela geometria.

Ao contrário: **é medido precisamente porque está passando**. E isso é um teorema —
o conjunto do que a forma **mede** contém estritamente o conjunto do que o espelho
**fixa**.

## O que se prova

* ★★★ **`measured_but_not_fixed`** — existe o que é **medido** (norma não-nula) e
  **não é fixado** pelo espelho: medir e fixar são coisas diferentes;
* ★★★ `the_fixed_are_properly_contained` — os fixos estão **propriamente** contidos
  nos mensuráveis: há sempre mais medida do que permanência local;
* ★★ `transport_leaves_a_trace` — se o transporte move, a diferença é **mensurável**:
  o rastro do transporte é o que a geometria lê.

## ESTATUTOS
`[REAL]` os três acima — estrutura pura. `[ONTO]` a identificação da densidade com o
neutrino é leitura do operador, registrada sob o nome dele; ela **integra** as
formulações anteriores (luz sem colapso, fuga do condensado, banho/decoerência) como
regimes do mesmo transporte, em vez de substituí-las. `[OPEN]` qual grandeza padrão
realiza «densidade do transporte» — energia, corrente, ou tensor — é escolha a fazer,
não resultado. β jamais entra; nada move o gate.
-/

namespace TGLExt

/-- ★★★ **MEDIDO E NÃO FIXADO**: existe conteúdo com medida não-nula que o espelho
    NÃO fixa. Medir e fixar são coisas diferentes. -/
theorem measured_but_not_fixed :
    ∃ x : ℝ, |x| ≠ 0 ∧ theFold x ≠ x := by
  refine ⟨1, ?_, ?_⟩
  · norm_num
  · unfold theFold
    norm_num

/-- ★★★ **OS FIXOS ESTÃO PROPRIAMENTE CONTIDOS NOS MENSURÁVEIS**: há sempre mais
    medida do que permanência local. -/
theorem the_fixed_are_properly_contained :
    {x : ℝ | theFold x = x} ⊂ {x : ℝ | |x| = |x|} := by
  constructor
  · intro x _
    exact rfl
  · intro h
    have h1 : (1 : ℝ) ∈ {x : ℝ | |x| = |x|} := rfl
    have h2 := h h1
    simp only [Set.mem_setOf_eq] at h2
    unfold theFold at h2
    norm_num at h2

/-- ★★ **O TRANSPORTE DEIXA RASTRO**: se move, a diferença é mensurável — e é esse
    rastro que a geometria lê. -/
theorem transport_leaves_a_trace (x y : ℝ) (h : x ≠ y) : |x - y| ≠ 0 := by
  intro hc
  exact h (sub_eq_zero.mp (abs_eq_zero.mp hc))

end TGLExt
