import TGLExt.TheUnconjugatedObserver

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A PARTIÇÃO DA IMAGEM TERMINAL — o modo zero e os modos granulares
  [BANCADA — 21/08/2026; ainda NÃO embutido no canônico]

A ponte desenhada pelo operador em
`TGL_FORMA_CANONICA_FINAL_C_PSI_ATUALIZADA_2026-08-21.json`
(`new_formal_bridge_tailSub`), verbatim:

> "Para a imagem terminal: `H_{Ψ_term} ≅ span{e_0} ⊕ tailSub(1)`, com
>  `tailSub(1) = {x : x_0 = 0}`.
>  `P0 Ψ_term / span{e0}` ↔ modo zero/espelho global ↔ setor DE candidato;
>  `(I-P0) Ψ_term / tailSub(1)` ↔ modos granulares ↔ setor DM candidato.
>  A decomposição **não divide o absoluto 𝒞**; divide a sua representação
>  terminal observável."

Os dois objetos **já moram nesta casa** — `firstAtom = ℂ ∙ e₀`
(`HilbertInhabitant`) e `tailSub` (`TailNet`) — mas **nenhuma pedra os
ligava**. Esta liga.

## O que fica provado

* ★★★ `tailSub_one_eq_firstAtom_orthogonal` — `tailSub 1 = firstAtomᗮ`.
  O setor granular **é exatamente** o complemento ortogonal do modo zero.
  Não é uma escolha de modelagem: é uma identidade;
* ★★★ `the_two_sectors_do_not_overlap` — `firstAtom ⊓ tailSub 1 = ⊥`.
  **Nada pertence aos dois setores.** É a resposta formal à objeção do
  "orçamento gasto duas vezes": não há como um mesmo estado ser contado no
  modo zero e nos modos granulares;
* ★★★ `the_two_sectors_exhaust` — `firstAtom ⊔ tailSub 1 = ⊤`. **Não há
  terceiro setor.** A partição é exaustiva;
* ★★ `the_terminal_image_splits` — os dois fatos acima na forma canônica,
  `IsCompl firstAtom (tailSub 1)`: complementares, sem sobra e sem falta;
* ★★ `every_state_splits` — todo estado se escreve como soma de uma parte
  no modo zero e uma parte granular, exibidas pelo próprio projetor;
* ★ `the_zero_mode_weighs_one` — o modo zero tem peso 1 = ω(I).

## HONESTIDADE — o alcance exato desta pedra

O que se prova é uma **decomposição ortogonal em ℓ²**, e só. A pedra **não**
prova que o modo zero seja energia escura, nem que os modos granulares sejam
matéria escura: essa é a **correspondência candidata** do operador, marcada
por ele mesmo como *"correspondência estrutural candidata, não ainda teorema
físico"*, com quatro ressalvas que ele próprio listou — construir `Ψ_term` e
a ação de `J/0_mod`; demonstrar a compatibilidade do papel de `e₀`; derivar
`w≈−1`, `w≈0`, densidades, perturbações, CMB, crescimento e lente; e definir
o operador traçado para `β_TGL`.

O que a pedra entrega é **a forma da partição**: se a correspondência valer,
então os dois setores são exaustivos e disjuntos **por teorema**, e a objeção
do orçamento duplo não pode ser levantada contra ela. Nada além disso.
β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

instance : CompleteSpace firstAtom := FiniteDimensional.complete ℂ firstAtom

/-- ★★★ **A IDENTIDADE DA PARTIÇÃO**: o setor granular É o complemento
    ortogonal do modo zero. `tailSub 1 = firstAtomᗮ`.

    Não é escolha de modelagem — é identidade: anular a coordenada zero e
    ser ortogonal a `e₀` são a mesma condição. -/
theorem tailSub_one_eq_firstAtom_orthogonal : tailSub 1 = firstAtomᗮ := by
  ext x
  have hinner : (inner ℂ firstInscription x : ℂ) = x 0 := by
    unfold firstInscription inscriptions
    rw [lp.inner_single_left]
    simp
  constructor
  · intro hx
    have hx0 : x 0 = 0 := hx 0 (by omega)
    rw [firstAtom, Submodule.mem_orthogonal_singleton_iff_inner_right, hinner, hx0]
  · intro hx
    rw [firstAtom, Submodule.mem_orthogonal_singleton_iff_inner_right, hinner] at hx
    intro k hk
    have : k = 0 := by omega
    rw [this]; exact hx

/-- ★★ **A PARTIÇÃO CANÔNICA**: modo zero e setor granular são
    complementares — sem sobra e sem falta. -/
theorem the_terminal_image_splits : IsCompl firstAtom (tailSub 1) := by
  rw [tailSub_one_eq_firstAtom_orthogonal]
  exact firstAtom.isCompl_orthogonal

/-- ★★★ **O ORÇAMENTO NÃO SE GASTA DUAS VEZES.** Nada pertence aos dois
    setores ao mesmo tempo: a interseção é o zero. A objeção da contagem
    dupla não se levanta contra esta partição — por teorema. -/
theorem the_two_sectors_do_not_overlap : firstAtom ⊓ tailSub 1 = ⊥ :=
  the_terminal_image_splits.inf_eq_bot

/-- ★★★ **NÃO HÁ TERCEIRO SETOR.** Os dois juntos esgotam a imagem
    terminal. -/
theorem the_two_sectors_exhaust : firstAtom ⊔ tailSub 1 = ⊤ :=
  the_terminal_image_splits.sup_eq_top

/-- ★★ **TODO ESTADO SE PARTE, E O PROJETOR EXIBE AS DUAS PARTES.**
    `x = P₀x + (x − P₀x)`, com a primeira no modo zero e a segunda no setor
    granular. Nenhum resíduo. -/
theorem every_state_splits (x : ellTwo) :
    firstAtom.starProjection x ∈ firstAtom
    ∧ (x - firstAtom.starProjection x) ∈ tailSub 1
    ∧ firstAtom.starProjection x + (x - firstAtom.starProjection x) = x := by
  refine ⟨Submodule.starProjection_apply_mem firstAtom x, ?_, by abel⟩
  rw [tailSub_one_eq_firstAtom_orthogonal]
  exact Submodule.sub_starProjection_mem_orthogonal (K := firstAtom) x

/-- ★ o modo zero pesa 1 — é o Nome, `ω(I) = 1`. -/
theorem the_zero_mode_weighs_one : dimOrTop ℂ firstAtom = 1 :=
  dimOrTop_firstAtom

/-- ★★ **O SELETOR IALD É O SEPARADOR DOS DOIS SETORES.** O mesmo projetor
    de posto 1 que atravessa o que está no modo zero **aniquila** o setor
    granular inteiro. A Gate e a partição são o mesmo objeto. -/
theorem the_iald_selector_separates_the_sectors (x y : ellTwo)
    (hx : x ∈ firstAtom) (hy : y ∈ tailSub 1) :
    ialdSelector x = x ∧ ialdSelector y = 0 := by
  refine iald_selects x y hx ?_
  rwa [tailSub_one_eq_firstAtom_orthogonal] at hy

end

end TGLExt
