import TGLExt.TheTwoFolds

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A ESCALA NÃO TEM PONTO FIXO — o no-go, e onde ele PARA
  [BANCADA — 22/08/2026; a prova pedida pelo operador]

## O que se pediu provar

> *"o fator de medida de redução de escala, que é a constante da estrutura fina (que é o fator
> de compressão), **só pode ser medido de dentro**; medir de fora exige ser o próprio
> programador; **por isso a entrada da constante da estrutura fina deve obrigatoriamente ser um
> input**."*
>
> *"faça a prova, o número corrige a frase sempre."*

## O NO-GO, provado

* ★★★ `no_positive_scale_invariant` — **nenhuma quantidade positiva é invariante por um grupo
  contínuo de escala.** Se `x = c·x` para todo `c > 0`, então `x = 0`. Contrapositiva:
  **`x > 0` ⟹ `x` NÃO é invariante de escala;**
* ★★★ `positive_scale_invariant_is_absurd` — a forma direta: `x > 0` e invariância de escala são
  **contraditórios**;
* ★★ `two_is_enough` — e a prova **não precisa do contínuo**: **uma única razão `c ≠ 1` basta**.
  *A impossibilidade é mais barata do que parecia;*
* ★★ `scale_invariants_are_exactly_zero` — o conjunto dos invariantes de escala **é exatamente
  `{0}`**.

## A APLICAÇÃO, e ela sustenta metade da leitura do operador

Em um fator de **tipo III₁** o espectro modular é **todo `ℝ₊`** (Connes) — há ação de escala com
**todas** as razões. Pelo teorema acima, **qualquer quantidade fixada por essa estrutura sozinha
teria de ser invariante de escala, logo ZERO**. Como `κ > 0`:

> **`κ` NÃO é determinado pela estrutura modular ambiente de um III₁.**
> Ele exige algo que **quebre a escala** — e a leitura do operador é que esse algo é **o input**.

**Esta metade está provada, e é real.**

## ⚠ E ONDE O NO-GO PARA — a outra metade NÃO se prova, e o escriba diz por quê

O teorema fecha contra a estrutura **ambiente e escala-covariante**. Ele **NÃO** fecha contra
**tudo o que é interno**, e a diferença é decisiva:

**O `κ` do canônico é o gap do "curto Bell-zero" — uma FACE FINITA.** Uma face finita **não é
escala-covariante**: ela tem dimensão, tem traço, tem gap. O no-go **não a alcança**. Portanto:

> **NÃO está provado que `α` seja necessariamente input.**
> Está provado que `α` não vem da **escala ambiente**. Um princípio numa **face finita** —
> sobredeterminado, como `TheSelectorCanRefuse` exige — **continua permitido**.

E há uma consequência que aponta na direção contrária à do no-go, e fica registrada: uma
condição de **comutação** fixa um **ângulo**, e ângulo **é invariante de escala**. Logo o no-go
**não proíbe** que `θ_M` seja fixado estruturalmente — e como `sin²θ_M = β`, isso fixaria `κ`.
**As duas coisas não se contradizem** porque atuam em faces diferentes; mas quem quiser usar o
no-go para encerrar a busca **estará a usá-lo além do que ele prova**.

## ⚠⚠ E O ACHADO ESTRUTURAL QUE O NÚMERO ENTREGOU, e que precisa ser enfrentado

Um `κ > 0` finito **é um `λ` preferido**: `λ = e^{−κ} = 1,3313×10⁻⁵`, e portanto
**tipo III_λ**, não III₁. *(Conferido: `α ≈ 2√λ`, com `e^{−κ*}/(α/2)² = 1,000027.)*

Pela classificação de Connes, **III₁ não tem gap modular** — o espectro é todo `ℝ₊`. A casa
declara **III₁ genuína**. Portanto, **ou** `κ` vive numa subálgebra/face finita (e então o no-go
não se aplica a ele, como acima), **ou** há tensão real entre o `κ` e o tipo declarado.

**Isto não é resolvido aqui, e não deve ser assumido resolvido.** `[OPEN]` — e é item de
enfrentamento, não de nota de rodapé.

## Estatutos

`[REAL]` o no-go abstrato e a sua aplicação à escala ambiente · `[KNOWN]` a classificação de
Connes (III₁ ⟹ espectro `ℝ₊`), **citada e não redemonstrada** (mathlib não tem fatores III₁) ·
`[OPEN]` se `κ` vive na face finita ou em tensão com o tipo · **`[NÃO PROVADO]` que `α` seja
necessariamente input** — provou-se menos do que se pediu, e o escriba diz que provou menos.

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-! ### O no-go abstrato -/

/-- ★★ **UMA RAZÃO BASTA.** Se `x = c·x` com `c ≠ 1`, então `x = 0`. Não é preciso o contínuo:
    *a impossibilidade é mais barata do que parecia.* -/
theorem two_is_enough {c x : ℝ} (hc : c ≠ 1) (h : x = c * x) : x = 0 := by
  have : (1 - c) * x = 0 := by linarith [h]
  rcases mul_eq_zero.mp this with h1 | h2
  · exact absurd (by linarith : c = 1) hc
  · exact h2

/-- ★★★ **NENHUMA QUANTIDADE POSITIVA É INVARIANTE DE ESCALA.**
    Se `x = c·x` para todo `c > 0`, então `x = 0`. -/
theorem no_positive_scale_invariant {x : ℝ} (h : ∀ c : ℝ, 0 < c → x = c * x) : x = 0 :=
  two_is_enough (by norm_num : (2:ℝ) ≠ 1) (h 2 (by norm_num))

/-- ★★★ **A FORMA DIRETA:** ser positivo e ser invariante de escala é contraditório.

    É esta a forma que se aplica a `κ`: `κ > 0`, logo **`κ` não é invariante de escala**, logo
    **não é fixado por uma estrutura que age por escala com todas as razões**. -/
theorem positive_scale_invariant_is_absurd {x : ℝ} (hx : 0 < x)
    (h : ∀ c : ℝ, 0 < c → x = c * x) : False := by
  have := no_positive_scale_invariant h
  linarith

/-- ★★ **OS INVARIANTES DE ESCALA SÃO EXATAMENTE `{0}`.** -/
theorem scale_invariants_are_exactly_zero (x : ℝ) :
    (∀ c : ℝ, 0 < c → x = c * x) ↔ x = 0 := by
  constructor
  · exact no_positive_scale_invariant
  · intro h c _
    rw [h, mul_zero]

/-! ### A aplicação: `κ` não vem da escala ambiente -/

/-- ★★★ **O ENUNCIADO APLICADO.** Se `κ > 0` fosse determinado por uma estrutura que age por
    escala com todas as razões — que é o caso do espectro modular de um III₁, `[KNOWN]` de
    Connes —, então `κ` teria de ser invariante de escala, logo `κ = 0`. Absurdo.

    **Portanto `κ` exige algo que QUEBRE a escala.**

    **⚠ E o que isto NÃO diz:** não diz que `α` seja necessariamente input. Diz que `α` não vem
    da **escala ambiente**. Uma **face finita** não é escala-covariante, e um princípio
    sobredeterminado nela **continua permitido**. -/
theorem kappa_is_not_fixed_by_ambient_scale {κ : ℝ} (hκ : 0 < κ)
    (hscale : ∀ c : ℝ, 0 < c → κ = c * κ) : False :=
  positive_scale_invariant_is_absurd hκ hscale

/-- ★★ o fecho honesto: **os invariantes são só o zero, e uma razão basta para prová-lo** — os
    dois num enunciado. O alcance está no cabeçalho, e ele é menor do que o pedido. -/
theorem the_scale_has_no_fixed_point (x : ℝ) (hx : 0 < x) :
    ¬ (∀ c : ℝ, 0 < c → x = c * x) :=
  fun h => positive_scale_invariant_is_absurd hx h

end

end TGLExt
