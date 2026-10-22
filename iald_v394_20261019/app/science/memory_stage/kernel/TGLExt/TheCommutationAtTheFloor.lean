import TGLExt.TheProfileDuality

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O TEOREMA DE COMUTAÇÃO NO ANDAR — e onde EXATAMENTE o limite pede mais
  [BANCADA — 27/08/2026 · marco M4 · tarefa (c), atacada]

## O achado

A tarefa (c) — o teorema de comutação — foi registrada como **pesquisa**. E é, **no
limite**. Mas **no andar finito ela é ELEMENTAR**, e a prova cabe em três linhas:

> se `T` comuta com toda multiplicação à esquerda, então `T x = T(x·1) = x·T(1)` —
> isto é, `T` **É** a multiplicação à direita por `T(1)`.

O vetor `1` faz todo o trabalho: ele é o **vetor cíclico**. E é exatamente por isso que
o passo ao limite não é gratuito — o argumento inteiro depende de `T(1)` **ser um
elemento da torre**, e no completamento `T(Ω)` pode não ser.

## O que se prova

* ★★★★ **`commutant_of_left_is_right`** — no andar: comutar com toda esquerda ⟹ **ser**
  uma multiplicação à direita, com o fator `T(1)` **explícito**;
* ★★★ `the_right_factor_is_the_image_of_the_unit` — o fator direito É a imagem do
  vetor cíclico: o Nome dá o fator;
* ★★ `right_multiplications_do_commute` — a recíproca (associatividade), fechando o iff.

## ⚠ ONDE O LIMITE PEDE MAIS (dito com precisão, porque é a dívida)
No completamento, `T(Ω)` **é um vetor de `WH`, não necessariamente um elemento da
torre**. O argumento acima produziria uma multiplicação à direita por algo que pode
não estar na álgebra — o fenômeno clássico dos operadores **afiliados**. É AÍ, e só aí,
que o teorema de comutação deixa de ser elementar. A dívida fica com o seu nome exato:
**mostrar que `T(Ω)` é aproximável pela torre**, ou tratar o afiliado. β jamais entra;
nada move o gate.
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- ★★★★ **COMUTAR COM TODA ESQUERDA É SER UMA DIREITA** — no andar, e com o fator
    explícito: `T = R_{T(1)}`. O vetor cíclico faz todo o trabalho. -/
theorem commutant_of_left_is_right (T : Matrix n n ℂ → Matrix n n ℂ)
    (hT : ∀ a x : Matrix n n ℂ, T (a * x) = a * T x) (x : Matrix n n ℂ) :
    T x = x * T 1 := by
  have h := hT x 1
  rwa [mul_one] at h

/-- ★★★ **O FATOR DIREITO É A IMAGEM DO VETOR CÍCLICO**: o Nome dá o fator. -/
theorem the_right_factor_is_the_image_of_the_unit
    (T : Matrix n n ℂ → Matrix n n ℂ)
    (hT : ∀ a x : Matrix n n ℂ, T (a * x) = a * T x) :
    ∃ b : Matrix n n ℂ, (∀ x, T x = x * b) ∧ b = T 1 :=
  ⟨T 1, fun x => commutant_of_left_is_right T hT x, rfl⟩

/-- ★★ **E AS DIREITAS COMUTAM MESMO** (associatividade) — fechando a equivalência. -/
theorem right_multiplications_do_commute (b : Matrix n n ℂ) :
    ∀ a x : Matrix n n ℂ, (a * x) * b = a * (x * b) :=
  fun a x => mul_assoc a x b

end TGLExt
