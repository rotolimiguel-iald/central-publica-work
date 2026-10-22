import TGLExt.TheScaleHasNoFixedPoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O FATOR DE COMPRESSÃO NÃO É IDENTIFICÁVEL DE DENTRO
  [BANCADA — 22/08/2026; a prova pedida, na formulação exata do operador]

## A formulação do operador, verbatim

> *"o mapa de compressão `𝒞_α : X_origem → X_inscrita` com `x_inscrito = α·x_origem`. O
> observador interno só dispõe da representação já comprimida… razões internas como
> `x'_i/x'_j = x_i/x_j` **eliminam α**. Para recuperar o fator global é necessária uma
> referência que **não tenha sido submetida à mesma transformação**. Esse é exatamente o
> problema de **identificabilidade**."*
>
> *"nenhuma derivação de `α` é válida se algum de seus inputs já contiver `α`, explícita ou
> implicitamente."*

**Está tudo certo, e tudo se prova.** O que segue é isso, e a delimitação do alcance.

## O que fica provado

* ★★★ `every_alpha_fits_every_observation` — **toda `α` é compatível com toda observação
  inscrita**: dado `y`, existe origem `x = y/α` que a produz, para **qualquer** `α ≠ 0`.
  *É a falha de identificabilidade na sua forma nua;*
* ★★★ `internal_ratios_are_alpha_blind` — **`(αxᵢ)/(αxⱼ) = xᵢ/xⱼ`**: as razões internas
  **eliminam `α` exatamente**. O observador que só dispõe de razões **não tem acesso a ele**;
* ★★★ `no_scale_invariant_functional_yields_alpha` — **um funcional invariante de escala NÃO
  pode devolver `α`.** Se `F(c·x) = F(x)` para todo `c`, então `F` é constante ao longo da
  família comprimida, enquanto `α` varia: contradição. *É a regra metodológica do operador,
  como teorema;*
* ★★★ `alpha_free_inputs_give_alpha_free_output` — **entradas invariantes de escala produzem
  saída invariante de escala.** Logo **nenhuma composição de quantidades `α`-livres pode
  produzir `α`**;
* ★★ `two_worlds_indistinguishable` — a forma mais forte: **dois mundos com fatores de
  compressão diferentes geram dados inscritos idênticos.** Não é ignorância do observador —
  **é ausência de informação no dado**.

## O ALCANCE — o que isto prova e o que NÃO prova

**PROVA:** que `α` **não é identificável a partir do dado inscrito sozinho**, quando o acesso
se dá por razões / funcionais invariantes de escala. **Isso sustenta a leitura do operador de
que `α_obs` é condição de calibração e não defeito da teoria** — e é a mesma situação de
qualquer régua que só pode ser lida com objetos já redimensionados por ela.

**NÃO PROVA:** que `α` seja *inderivável em absoluto*. A hipótese que faz o teorema funcionar é
**`F` invariante de escala**. Um princípio numa **face que QUEBRA a escala** — uma face finita,
com dimensão, traço e gap — **não satisfaz essa hipótese**, e o teorema **não o alcança**.

> **A dicotomia fica exata:** ou o acesso é por quantidade invariante de escala — e aí `α` é
> **provadamente** inacessível —, ou existe uma face que quebra a escala, e aí **essa face tem
> de ser exibida**, e o que dela sair é sobredeterminado ou é ajuste.

E o contra-indicador registrado em `TheScaleHasNoFixedPoint` permanece: **ângulo é invariante
de escala**, logo uma condição de comutação **pode** fixar `θ_M` sem violar nada aqui — e
`sin²θ_M = β`. **As duas coisas convivem porque atuam em faces diferentes.**

## A consequência que o operador tirou, e que fica provada como REGRA

> **Nenhuma derivação de `α` é válida se algum input já contiver `α`.**

É `alpha_free_inputs_give_alpha_free_output` lido ao contrário. E tem aplicação imediata e
concreta: **`β_TGL = α_obs·√e` deriva `β` a partir de `α`, e NÃO pode ser invertida e
apresentada como derivação independente de `α`** se `β` foi calibrado com a própria `α`.
*Isto é exatamente o que o T10 mediu por fora e o que este teorema fecha por dentro.*

## Estatutos

`[REAL]` os cinco teoremas · `[ONTO]` do operador, fora de todo enunciado: `1_abs` como posição
que conhece o mapa antes da compressão, e `IALD` como observador interno · **`[NÃO PROVADO]`**
que `α` seja inderivável fora da hipótese de invariância de escala. **Provou-se o que se
formulou, e não mais.**

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-- O MAPA DE COMPRESSÃO: `x_inscrito = α · x_origem`. -/
def compress (a x : ℝ) : ℝ := a * x

/-! ### A falha de identificabilidade, nua -/

/-- ★★★ **TODA `α` É COMPATÍVEL COM TODA OBSERVAÇÃO.** Dado um dado inscrito `y` e **qualquer**
    fator `a ≠ 0`, existe uma origem que o produz — a saber `x = y/a`.

    *O dado inscrito não restringe o fator: é a falha de identificabilidade na forma nua.* -/
theorem every_alpha_fits_every_observation (y a : ℝ) (ha : a ≠ 0) :
    ∃ x : ℝ, compress a x = y := by
  refine ⟨y / a, ?_⟩
  unfold compress
  field_simp

/-- ★★ **DOIS MUNDOS INDISTINGUÍVEIS.** Para quaisquer dois fatores não-nulos existem origens
    que produzem **o mesmo** dado inscrito.

    *Não é ignorância do observador — é ausência de informação no dado.* -/
theorem two_worlds_indistinguishable (y a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    ∃ x₁ x₂ : ℝ, compress a x₁ = y ∧ compress b x₂ = y := by
  refine ⟨y / a, y / b, ?_, ?_⟩ <;> unfold compress <;> field_simp

/-- ★★★ **AS RAZÕES INTERNAS SÃO CEGAS A `α`.** `(a·xᵢ)/(a·xⱼ) = xᵢ/xⱼ`.

    O observador que só dispõe de razões **não tem acesso ao fator**: ele cancela exatamente. -/
theorem internal_ratios_are_alpha_blind (a xi xj : ℝ) (ha : a ≠ 0) :
    (compress a xi) / (compress a xj) = xi / xj := by
  unfold compress
  rcases eq_or_ne xj 0 with hj | hj
  · simp [hj]
  · field_simp

/-! ### A regra metodológica do operador, como teorema -/

/-- ★★★ **NENHUM FUNCIONAL INVARIANTE DE ESCALA DEVOLVE `α`.**

    Se `F(c·x) = F(x)` para todo `c > 0`, então `F` não pode valer `a` sobre `compress a x`
    para todo `a > 0` — porque o lado esquerdo é constante e o direito varia.

    *É a regra do operador — "nenhuma derivação de α é válida se os inputs já a contiverem" —
    na sua forma contrapositiva e provada.* -/
theorem no_scale_invariant_functional_yields_alpha
    (F : ℝ → ℝ) (hF : ∀ c x : ℝ, 0 < c → F (c * x) = F x) (x : ℝ) :
    ¬ (∀ a : ℝ, 0 < a → F (compress a x) = a) := by
  intro h
  have h1 : F x = 1 := by
    have := h 1 (by norm_num)
    simpa [compress] using this
  have h2 : F x = 2 := by
    have hc := hF 2 x (by norm_num)
    have := h 2 (by norm_num)
    rw [compress] at this
    rw [hc] at this
    exact this
  rw [h1] at h2
  norm_num at h2

/-- ★★★ **ENTRADAS `α`-LIVRES DÃO SAÍDA `α`-LIVRE.** Se `u` e `v` são invariantes de escala,
    qualquer combinação `g(u,v)` também é.

    **Logo nenhuma composição de quantidades `α`-livres pode produzir `α`** — que é a regra
    metodológica do operador, dita na direção construtiva. -/
theorem alpha_free_inputs_give_alpha_free_output
    (u v : ℝ → ℝ) (g : ℝ → ℝ → ℝ)
    (hu : ∀ c x : ℝ, 0 < c → u (c * x) = u x)
    (hv : ∀ c x : ℝ, 0 < c → v (c * x) = v x) :
    ∀ c x : ℝ, 0 < c → g (u (c * x)) (v (c * x)) = g (u x) (v x) := by
  intro c x hc
  rw [hu c x hc, hv c x hc]

/-- ★★ o fecho: **o dado não restringe o fator**, **as razões cancelam-no**, e **funcional
    invariante de escala não o devolve** — os três num enunciado. O alcance está no cabeçalho,
    e ele para exatamente onde a invariância de escala para. -/
theorem the_compression_is_not_identifiable (y : ℝ) (x : ℝ) :
    (∀ a : ℝ, a ≠ 0 → ∃ x' : ℝ, compress a x' = y)
    ∧ (∀ a xi xj : ℝ, a ≠ 0 → (compress a xi) / (compress a xj) = xi / xj)
    ∧ (∀ F : ℝ → ℝ, (∀ c z : ℝ, 0 < c → F (c * z) = F z) →
        ¬ (∀ a : ℝ, 0 < a → F (compress a x) = a)) :=
  ⟨fun a ha => every_alpha_fits_every_observation y a ha,
   fun a xi xj ha => internal_ratios_are_alpha_blind a xi xj ha,
   fun F hF => no_scale_invariant_functional_yields_alpha F hF x⟩

end

end TGLExt
