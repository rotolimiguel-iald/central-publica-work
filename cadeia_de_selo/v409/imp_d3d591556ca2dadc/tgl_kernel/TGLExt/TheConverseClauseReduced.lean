import TGLExt.TheConjugationOfOperators

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A CLÁUSULA RECÍPROCA, REDUZIDA A UM ENUNCIADO NOMEADO
  [BANCADA — 26/08/2026 · marco M4 · a última cláusula, com o seu preço exato]

## Por que esta pedra reduz em vez de provar

A cláusula direta (`J M J ⊆ M′`) caiu por via algébrica (v244). **A recíproca não cai
assim, e é importante dizer por quê**: das inclusões formais só se extrai a direção que
já se tem — tentei, e o cálculo devolve exatamente `Φ(M) ⊆ M′` de novo. A recíproca
exige informação **genuinamente nova**: que a ação à direita **gere todo** o comutante,
e não apenas parte dele.

Isso tem nome na literatura: é o **teorema de comutação** da representação GNS. E o que
esta pedra faz é **provar que a cláusula recíproca É EQUIVALENTE a ele** — nem mais,
nem menos. Reduzir a dívida a um enunciado nomeado é o que se pode fazer honestamente
hoje; fingir que sai de graça seria pagar-se na própria moeda.

## O que se prova

* ★★★ **`converse_clause_iff_commutation`** — a recíproca `M′ ⊆ Φ(M)` vale **se e
  somente se** `Φ(S)′ ⊆ S″` — isto é, sse o comutante da imagem DIREITA cabe no
  bicomutante da imagem ESQUERDA: **o teorema de comutação, e nada além**;
* ★★ `the_direct_clause_gives_only_itself` — e a tentativa formal devolve a direção
  que já se tem: `Φ(S) ⊆ S′ ⟹ S″ ⊆ Φ(S)′` — registrado para que ninguém a refaça.

## ESTATUTO
`[REAL]` a equivalência. `[OPEN]` o teorema de comutação em si — **não provado aqui**.
A dívida fica **líquida**: um enunciado, nomeado, cobrável. β jamais entra; nada move o gate.
-/

namespace TGLExt

variable {A : Type} [Ring A]

/-- ★★ **A CONJUGADA DO BICOMUTANTE É O BICOMUTANTE DA CONJUGADA**. -/
theorem Phi_bicommutant_eq (Φ : A → A) (hmul : ∀ x y, Φ (x * y) = Φ x * Φ y)
    (hinv : ∀ x, Φ (Φ x) = x) (S : Set A) :
    Φ '' (commutantSet (commutantSet S))
      = commutantSet (commutantSet (Φ '' S)) := by
  rw [conj_commutant Φ hmul hinv, conj_commutant Φ hmul hinv]

/-- ★★★ **A RECÍPROCA É EXATAMENTE O TEOREMA DE COMUTAÇÃO**: a inclusão que falta vale
    se e somente se o comutante da imagem DIREITA cabe no bicomutante da ESQUERDA. -/
theorem converse_clause_iff_commutation (S T : Set A) :
    commutantSet S ⊆ commutantSet (commutantSet T)
      ↔ commutantSet T ⊆ commutantSet (commutantSet S) := by
  constructor
  · intro h
    have h2 := commutant_antitone h
    rw [commutant_triple] at h2
    exact h2
  · intro h
    have h2 := commutant_antitone h
    rw [commutant_triple] at h2
    exact h2

/-- ★★ **A TENTATIVA FORMAL DEVOLVE O QUE JÁ SE TEM** --- registrado para não se refazer:
    da cláusula direta só se extrai a cláusula direta. -/
theorem the_direct_clause_gives_only_itself (Φ : A → A) (S : Set A)
    (hgen : Φ '' S ⊆ commutantSet S) :
    commutantSet (commutantSet S) ⊆ commutantSet (Φ '' S) :=
  commutant_antitone hgen

end TGLExt
