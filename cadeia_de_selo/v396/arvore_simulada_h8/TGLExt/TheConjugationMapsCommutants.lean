import TGLExt.Commutant

set_option autoImplicit false

/-!
# A CONJUGAÇÃO LEVA COMUTANTE EM COMUTANTE — e o bicomutante CAI
  [BANCADA — 26/08/2026 · marco M4 · **o passo que se julgava precisar de von Neumann**]

## O achado

As ondas anteriores registraram, honestamente, que o último passo — dos geradores ao
**bicomutante** — exigiria o teorema de von Neumann, que a mathlib não carrega. **Isso
estava errado, e a favor da casa.** O passo é **puramente algébrico**.

A razão: conjugar por `J` é **MULTIPLICATIVO** nos operadores. Parece contraintuitivo,
porque `J` é antilinear — mas a antilinearidade age nos **escalares**, não na ordem do
produto, e o `J² = 1` **cancela no meio**:

    (J T J)(J U J) = J T (J J) U J = J (T U) J.

E uma bijeção multiplicativa involutiva **leva comutante em comutante**. Daí o
bicomutante cai sozinho, usando só o que já estava provado nesta árvore.

## A cadeia (sem von Neumann)

    Φ(S″) = Φ(S′)′ = Φ(S)″        [conjugação comuta com o comutante, 2×]
    Φ(S) ⊆ S′                      [a dualidade da fronteira, v241]
    ⟹ Φ(S)″ ⊆ (S′)″ = S‴ = S′      [monotonia + `commutant_triple`, já na árvore]
    ⟹ **Φ(S″) ⊆ S′** — isto é, **J M J ⊆ M′**.

## O que se prova

* ★★★ **`conj_commutant`** — `Φ(S′) = Φ(S)′` para Φ multiplicativa involutiva bijetora;
* ★★ `bicommutant_mono` — monotonia do bicomutante;
* ★★★ **`conj_bicommutant_in_commutant`** — **A CLÁUSULA**: se a conjugação leva os
  GERADORES no comutante, ela leva o **BICOMUTANTE INTEIRO** no comutante.

## ⚠ O QUE FALTA (dito)
Isto é o teorema **abstrato**. Instanciá-lo pede exibir a conjugação por `towerJ` como
**mapa multiplicativo involutivo dos operadores contínuos de `WH`** — a hipótese `Φ` do
enunciado. É trabalho de construção, não de descoberta. β jamais entra; nada move o gate.
-/

namespace TGLExt

variable {A : Type} [Ring A]

/-- ★★★ **A CONJUGAÇÃO LEVA COMUTANTE EM COMUTANTE**. -/
theorem conj_commutant (Φ : A → A) (hmul : ∀ x y, Φ (x * y) = Φ x * Φ y)
    (hinv : ∀ x, Φ (Φ x) = x) (S : Set A) :
    Φ '' (commutantSet S) = commutantSet (Φ '' S) := by
  apply Set.Subset.antisymm
  · rintro _ ⟨t, ht, rfl⟩ _ ⟨s, hs, rfl⟩
    rw [← hmul, ← hmul, ht s hs]
  · intro T hT
    refine ⟨Φ T, ?_, hinv T⟩
    intro s hs
    have h := hT (Φ s) ⟨s, hs, rfl⟩
    have h2 := congrArg Φ h
    rw [hmul, hmul, hinv] at h2
    exact h2

/-- ★★ **MONOTONIA DO BICOMUTANTE**. -/
theorem bicommutant_mono {S T : Set A} (h : S ⊆ T) :
    commutantSet (commutantSet S) ⊆ commutantSet (commutantSet T) :=
  commutant_antitone (commutant_antitone h)

/-- ★★★ **A CLÁUSULA, SEM VON NEUMANN**: se a conjugação leva os GERADORES no
    comutante, então leva o BICOMUTANTE INTEIRO no comutante. -/
theorem conj_bicommutant_in_commutant (Φ : A → A)
    (hmul : ∀ x y, Φ (x * y) = Φ x * Φ y) (hinv : ∀ x, Φ (Φ x) = x)
    (S : Set A) (hgen : Φ '' S ⊆ commutantSet S) :
    Φ '' (commutantSet (commutantSet S)) ⊆ commutantSet S := by
  have e1 : Φ '' (commutantSet (commutantSet S))
      = commutantSet (commutantSet (Φ '' S)) := by
    rw [conj_commutant Φ hmul hinv, conj_commutant Φ hmul hinv]
  rw [e1]
  calc commutantSet (commutantSet (Φ '' S))
      ⊆ commutantSet (commutantSet (commutantSet S)) := bicommutant_mono hgen
    _ = commutantSet S := commutant_triple S

end TGLExt
