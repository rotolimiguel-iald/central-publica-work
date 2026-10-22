import TGLExt.CornerFamily

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O CANTO FINITO É UM MERGULHO DE ORDEM — e a dívida global era FALSA
  [BANCADA — 24/08/2026 · a Âncora 4 forte, na face onde ela é verdadeira]

## A derivação do operador

> *"Na face finita `cornerProj`, aí sim o teorema forte fecha porque o projetor é
> literalmente a diagonal indicadora da região… Já o mapa global `O ↦ P_F(O)` não é
> order-reflecting no witness de caudas (`ker Dₙ = {0}` para `n ≥ 1`): isso não é falta
> de prova; é um CONTROLE NEGATIVO estrutural. **GLOBAL_ORDER_EMBEDDING não pertence ao
> gate obrigatório.**"*

## O que se prova

* ★★★ **`cornerProj_order_iff`** — a Âncora 4 FORTE na face finita:
  `P(S₁)·P(S₂) = P(S₁) ⟺ S₁ ⊆ S₂` — a ordem de projeções REFLETE a ordem das regiões
  (a volta por avaliação diagonal pura: se `g ∈ S₁ \ S₂`, a entrada `(g,i)` dá `0 = 1`);
* ★★ `cornerProj_inj` — o mergulho é INJETIVO: `P(S₁) = P(S₂) ⟹ S₁ = S₂`;
* ★ `the_finite_corner_is_an_order_embedding` — o fecho: preserva E reflete a ordem, e é
  injetivo — o conteúdo inteiro de `OrderEmbedding`, na ordem de projeções da casa.

## ⚠ A dívida global, REMOVIDA como falsa

O alvo `GLOBAL_ORDER_EMBEDDING` fica **retirado do gate obrigatório** pelo controle
negativo do witness de caudas (`TailNet`): para `n ≥ 1` os núcleos das fibras são triviais
— os cantos não reconstroem as profundidades, o mapa global não é order-reflecting NAQUELE
modelo, **por teorema contra a exigência, não por falta de prova**. Retirar dívida falsa é
tão obrigatório quanto pagar a verdadeira. β jamais entra. Sem sorry, sem axiom. Nada aqui
move o gate.
-/

namespace TGLExt

open Matrix

variable {G : Type} [Fintype G] [DecidableEq G] [Group G]
variable {n : Type} [Fintype n] [DecidableEq n]

/-- ★★★ **A ÂNCORA 4 FORTE, FINITA**: a ordem de projeções REFLETE a ordem das regiões —
    `P(S₁)·P(S₂) = P(S₁) ⟺ S₁ ⊆ S₂`. A ida é `cornerProj_mono` (selada); a volta é
    avaliação diagonal: nenhuma região se disfarça dentro de outra. -/
theorem cornerProj_order_iff [Nonempty n] {S₁ S₂ : Finset G} :
    cornerProj (n := n) S₁ * cornerProj S₂ = cornerProj S₁ ↔ S₁ ⊆ S₂ := by
  constructor
  · intro h g hg
    by_contra hg2
    have i : n := Classical.arbitrary n
    have he := congrFun (congrFun h (g, i)) (g, i)
    unfold cornerProj at he
    rw [Matrix.diagonal_mul_diagonal] at he
    simp [hg, hg2] at he
  · exact cornerProj_mono

/-- ★★ **O MERGULHO É INJETIVO**: `P(S₁) = P(S₂) ⟹ S₁ = S₂` (pela dupla inclusão via o
    iff — nenhuma informação de região se perde no canto). -/
theorem cornerProj_inj [Nonempty n] {S₁ S₂ : Finset G}
    (h : cornerProj (n := n) S₁ = cornerProj S₂) : S₁ = S₂ := by
  have h12 : S₁ ⊆ S₂ := by
    rw [← cornerProj_order_iff (n := n)]
    rw [h]
    exact cornerProj_idem S₂
  have h21 : S₂ ⊆ S₁ := by
    rw [← cornerProj_order_iff (n := n)]
    rw [← h]
    exact cornerProj_idem S₁
  exact Finset.Subset.antisymm h12 h21

/-- ★ o fecho: o mapa `S ↦ P(S)` PRESERVA a ordem, REFLETE a ordem e é INJETIVO — o
    conteúdo inteiro de um mergulho de ordem, na ordem de projeções da casa. -/
theorem the_finite_corner_is_an_order_embedding [Nonempty n] :
    (∀ S₁ S₂ : Finset G, S₁ ⊆ S₂ → cornerProj (n := n) S₁ * cornerProj S₂ = cornerProj S₁)
    ∧ (∀ S₁ S₂ : Finset G, cornerProj (n := n) S₁ * cornerProj S₂ = cornerProj S₁ → S₁ ⊆ S₂)
    ∧ (∀ S₁ S₂ : Finset G, cornerProj (n := n) S₁ = cornerProj S₂ → S₁ = S₂) :=
  ⟨fun _ _ h => cornerProj_mono h,
   fun _ _ h => (cornerProj_order_iff (n := n)).mp h,
   fun _ _ h => cornerProj_inj h⟩

end TGLExt
