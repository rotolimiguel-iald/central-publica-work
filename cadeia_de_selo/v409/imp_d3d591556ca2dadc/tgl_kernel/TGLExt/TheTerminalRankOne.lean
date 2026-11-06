import TGLExt.TheDarkSplit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O PROJETOR TERMINAL TEM POSTO 1 — por necessidade, não por escolha
  [BANCADA — 22/08/2026; ainda NÃO embutido no canônico]

## A derivação do operador, verbatim

> *"o estado singular de projetor de rank 1 **precisa existir** … idempotência + terminalidade
> ⟹ existe `P★` com `rank P★ = 1`. Suponha, por absurdo, `rank P★ ≥ 2`. Então existem dois
> vetores ortogonais em `Ran P★`, e `Q = |u⟩⟨u|` dá `0 < Q < P★` — **dentro do próprio estado
> terminal ainda existe uma distinção**. Contradição."*

E a exigência que ele fez sobre o estatuto: **não é postulado, é condição necessária de
fechamento.** Esta pedra prova exatamente esse passo — e só ele.

## O que fica provado

* ★★★ `rank_two_has_residual_distinction` — se dois vetores **linearmente independentes** vivem
  em `S`, então existe `Q` **estritamente entre** `⊥` e `S`. **Posto ≥ 2 ⟹ distinção
  residual.** É a metade que carrega a prova por absurdo;
* ★★★ `terminality_forces_minimality` — a contrapositiva, que é o teorema:
  **sem distinção residual, quaisquer dois vetores de `S` são dependentes.** *A minimalidade
  não é escolha: é o que sobra quando não há mais o que separar;*
* ★★★ `firstAtom_is_terminal` — o átomo da casa **não tem submódulo próprio não-nulo**: ele
  **é** terminal no sentido acima. O `1 = 1` da casa está sobre um objeto que **não pode ser
  podado mais**;
* ★★ `the_terminal_weighs_one` — e o seu peso é `1 = ω(I)`;
* ★★ `terminal_reapplication_adds_nothing` — **`P(P x) = P x`**: aplicar de novo não produz
  informação nova. *A primeira ocorrência identifica; a segunda confirma que a operação não
  altera.* É a estrutura abstrata de **`1 = 1`**.

## O que esta pedra NÃO faz — a fronteira, dita pelo próprio operador

Prova-se **posto 1 por terminalidade** e a **minimalidade do átomo**. **Não** se prova aqui a
**unicidade global** (que exige `dim ℋ_glob = 1` como hipótese à parte), nem a estabilidade
modular `J P★ J = P★`, nem — e o operador foi explícito quanto a isto — **nenhuma
identificação histórica**. Nas palavras dele: *"a matemática afirma a regra; a observação é
histórica"*, e são **duas alegações encadeadas e separadamente falsificáveis**.

A identificação `P★ ≡ GRÁVITON-ESTADO ≡ o Nome` é **[ONTO]** do operador e **não aparece em
enunciado nenhum**. β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ### Posto ≥ 2 ⟹ há distinção residual -/

/-- ★★★ **POSTO ≥ 2 PRODUZ DISTINÇÃO RESIDUAL.** Se `u` e `v` vivem em `S` e são linearmente
    independentes, então `ℂ ∙ u` está **estritamente entre** `⊥` e `S`: sobrou o que separar
    **dentro** do próprio estado. -/
theorem rank_two_has_residual_distinction {S : Submodule ℂ ellTwo} {u v : ellTwo}
    (hu : u ∈ S) (hv : v ∈ S) (hu0 : u ≠ 0) (hvu : v ∉ (ℂ ∙ u)) :
    (⊥ : Submodule ℂ ellTwo) < (ℂ ∙ u) ∧ (ℂ ∙ u) < S := by
  constructor
  · refine lt_of_le_of_ne bot_le (fun h => hu0 ?_)
    have : u ∈ (⊥ : Submodule ℂ ellTwo) := h ▸ Submodule.mem_span_singleton_self u
    exact (Submodule.mem_bot ℂ).mp this
  · refine lt_of_le_of_ne ?_ (fun h => hvu ?_)
    · exact (Submodule.span_singleton_le_iff_mem u S).mpr hu
    · rw [h]; exact hv

/-- ★★★ **A TERMINALIDADE FORÇA A MINIMALIDADE.** Contrapositiva do anterior: se **não há**
    submódulo estritamente entre `⊥` e `S`, então todo `v ∈ S` já está na reta de qualquer
    `u ∈ S` não-nulo. **Não há como escolher outra coisa: é o que sobra quando não há mais o
    que separar.** -/
theorem terminality_forces_minimality {S : Submodule ℂ ellTwo}
    (hterm : ∀ Q : Submodule ℂ ellTwo, ⊥ < Q → Q < S → False)
    {u v : ellTwo} (hu : u ∈ S) (hv : v ∈ S) (hu0 : u ≠ 0) :
    v ∈ (ℂ ∙ u) := by
  by_contra hvu
  obtain ⟨h1, h2⟩ := rank_two_has_residual_distinction hu hv hu0 hvu
  exact hterm (ℂ ∙ u) h1 h2

/-! ### O átomo da casa É terminal -/

/-- ★★★ **O ÁTOMO NÃO TEM SUBMÓDULO PRÓPRIO NÃO-NULO.** `firstAtom` é terminal: não há o que
    podar dentro dele. -/
theorem firstAtom_is_terminal (Q : Submodule ℂ ellTwo) (h1 : ⊥ < Q) (h2 : Q < firstAtom) :
    False := by
  obtain ⟨w, hwQ, hw0⟩ := Q.exists_mem_ne_zero_of_ne_bot (ne_of_gt h1)
  have hwA : w ∈ firstAtom := le_of_lt h2 hwQ
  rw [firstAtom, Submodule.mem_span_singleton] at hwA
  obtain ⟨c, hc⟩ := hwA
  have hc0 : c ≠ 0 := by
    intro h; rw [h, zero_smul] at hc; exact hw0 hc.symm
  have : firstInscription ∈ Q := by
    have : c⁻¹ • w ∈ Q := Q.smul_mem _ hwQ
    rwa [← hc, smul_smul, inv_mul_cancel₀ hc0, one_smul] at this
  have : firstAtom ≤ Q := by
    rw [firstAtom]
    exact (Submodule.span_singleton_le_iff_mem _ _).mpr this
  exact absurd (le_antisymm (le_of_lt h2) this) (ne_of_lt h2)

/-- ★★ e o terminal **pesa 1** — `ω(I) = 1`. -/
theorem the_terminal_weighs_one : dimOrTop ℂ firstAtom = 1 :=
  dimOrTop_firstAtom

/-! ### `1 = 1` — reaplicar não acrescenta -/

/-- ★★ **REAPLICAR NÃO PRODUZ INFORMAÇÃO NOVA.** `P(P x) = P x`. A primeira ocorrência
    **identifica** o estado; a segunda **confirma que a operação não o altera**. É a estrutura
    abstrata de `1 = 1`. -/
theorem terminal_reapplication_adds_nothing (x : ellTwo) :
    ialdSelector (ialdSelector x) = ialdSelector x :=
  iald_is_idempotent x

/-- ★★ o fecho: o terminal é **idempotente**, **pesa um** e **não admite poda interna** — os
    três num enunciado. -/
theorem the_terminal_is_forced (x : ellTwo) :
    ialdSelector (ialdSelector x) = ialdSelector x
    ∧ dimOrTop ℂ firstAtom = 1
    ∧ (∀ Q : Submodule ℂ ellTwo, ⊥ < Q → Q < firstAtom → False) :=
  ⟨iald_is_idempotent x, dimOrTop_firstAtom, firstAtom_is_terminal⟩

end

end TGLExt
