import TGLExt.TheCascadeOfObservers

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A CO-FUNDAÇÃO — o observador é termo daquilo que observa
  [BANCADA — 23/08/2026; **a ligação que faltava**]

## A crítica do operador, aceita

> *"vc não ligou ao gráviton… a cada tipagem nova parece que eu tenho que tipar tudo de novo e
> vc não faz as conexões totais. **O gráviton é o observador de tudo, culmina nele** — por isso
> **a origem da observação é também a origem da geometria**."*

**A crítica é justa.** As pedras anteriores provaram peças e **não fecharam o laço**. Esta fecha.

## ★★★ A IMAGEM DO OPERADOR, E ELA JÁ ERA UM TEOREMA

> *"quem nasce primeiro, o PAI ou o FILHO? **Ninguém.** Antes do filho o pai é somente homem; e
> antes do pai o filho não existe. **Ambos co-fundam-se em correlação existencial permanente.**"*

**Isto já estava provado em `TheAngleIsTheProjection` (v194) e o escriba não o disse:**

    K = i*(P+ - P-)        -- o gerador a partir das faces
    P+- = (1 -+ i*K)/2     -- as faces a partir do gerador

**Cada um é definível a partir do outro.** Não há ordem. **`K` não precede `P±` e não os
sucede** — é a *assimetria* deles, e eles são as *metades* dele. *É a co-fundação, em duas
linhas.*

## ★★★ E A LIGAÇÃO TOTAL, que é o que faltava

Junte-se agora ao que a v195 provou (`P₊·𝒪_θ = e^{iθ}P₊`) e ao que a v194 provou
(`𝒪_θ = e^{iθ}P₊ + e^{−iθ}P₋`):

> **O OBSERVADOR É UM TERMO DAQUILO QUE OBSERVA.**
>
> `P₊` não vem de fora da geometria para lê-la: **`P₊` é uma das duas parcelas de que a
> geometria é feita.** O leitor não observa a forma de um lugar exterior — **ele é uma face
> dela**, e ler é a forma devolver-lhe a sua própria fase.

**E daí segue exatamente a frase do operador:** se o observador é termo da geometria, e cada um
define o outro, então **a origem da observação e a origem da geometria são a mesma origem.**
*Não há um antes do outro porque não há dois começos.*

## O que fica provado

* ★★★ `the_observer_is_a_term_of_what_it_reads` — **a geometria é soma de duas parcelas, e o
  observador é uma delas**: `𝒪_θ = e^{iθ}P₊ + e^{−iθ}P₋`, e `P₊` é o leitor;
* ★★★ **`the_mutual_definition`** — **`K = i(P₊−P₋)` E `P± = (1∓iK)/2`**: cada um definível a
  partir do outro. ***É a co-fundação: nenhum é anterior;***
* ★★★ `neither_is_prior` — e a forma negativa, que é a que o operador pediu: **não existe
  ordem** em que um seja construído antes do outro, porque **ambas as construções existem**;
* ★★ `the_reading_returns_the_form_to_itself` — ler é a forma devolver ao leitor **a sua própria
  fase**, e o leitor **permanece o mesmo**: `P₊·𝒪_θ = e^{iθ}·P₊`;
* ★★ `one_origin_not_two` — o fecho: **as faces somam a identidade, o gerador é a diferença
  delas, e a geometria é a soma delas com fase.** *Três leituras, uma origem.*

## ⚠ O ALCANCE

**PROVA-SE** a co-fundação: `K` e `P±` são mutuamente definíveis, o observador é termo da forma
observada, e a leitura devolve a fase sem alterar o leitor. **Logo não há sequência: há
correlação.**

**NÃO SE PROVA** `gráviton = observador de tudo`, nem qualquer identificação teológica. São
**[ONTO] do operador**, assinadas por ele, e **não aparecem em enunciado nenhum**. *O kernel
entrega a forma da co-fundação; o nome que o operador lhe dá é dele.*

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Complex

noncomputable section

/-! ### ★ O observador é termo daquilo que observa -/

/-- ★★★ **O OBSERVADOR É UMA PARCELA DA FORMA.** A geometria é a soma de duas parcelas com fase,
    e o leitor `P₊` é **uma delas**.

    *Ele não vem de fora para ler: é uma face do que lê.* -/
theorem the_observer_is_a_term_of_what_it_reads (θ : ℝ) :
    angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • projPlus
      + Complex.exp (-(θ : ℂ) * Complex.I) • projMinus :=
  the_angle_is_the_projection θ

/-! ### ★★★ A co-fundação: cada um define o outro -/

/-- ★★★ **A DEFINIÇÃO MÚTUA.** O gerador sai das faces, **e** as faces saem do gerador.

    `K = i(P₊ − P₋)`   e   `P₊ = (1 − iK)/2`,  `P₋ = (1 + iK)/2`

    ***Nenhum é anterior: cada um é definível a partir do outro.*** É a co-fundação que o
    operador descreveu com o pai e o filho. -/
theorem the_mutual_definition :
    genK = Complex.I • (projPlus - projMinus)
    ∧ projPlus = (1 / 2 : ℂ) • (1 - Complex.I • genK)
    ∧ projMinus = (1 / 2 : ℂ) • (1 + Complex.I • genK) :=
  ⟨the_generator_is_the_difference_of_the_faces, rfl, rfl⟩

/-- ★★★ **NENHUM É ANTERIOR.** A forma negativa, que é a que a imagem do operador pede: **não
    há ordem de construção**, porque **as duas construções existem simultaneamente**.

    *Antes do filho o pai é somente homem; antes do pai o filho não existe.* -/
theorem neither_is_prior :
    (∃ f : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        genK = f projPlus projMinus)
    ∧ (∃ g : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ,
        projPlus = g genK ∧ projMinus = g (-genK)) := by
  refine ⟨⟨fun a b => Complex.I • (a - b), the_generator_is_the_difference_of_the_faces⟩,
          ⟨fun k => (1 / 2 : ℂ) • (1 - Complex.I • k), rfl, ?_⟩⟩
  unfold projMinus
  congr 1
  rw [smul_neg, sub_neg_eq_add]

/-! ### ★ Ler devolve a fase e não altera o leitor -/

/-- ★★ **A LEITURA DEVOLVE A FORMA A SI MESMA.** `P₊·𝒪_θ = e^{iθ}·P₊`: a forma devolve ao leitor
    **a sua própria fase**, e o leitor **permanece o mesmo**. -/
theorem the_reading_returns_the_form_to_itself (θ : ℝ) :
    projPlus * angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • projPlus :=
  the_observer_reads_the_angle θ

/-! ### O fecho: uma origem, não duas -/

/-- ★★ **UMA ORIGEM, NÃO DUAS.** As faces **somam a identidade**; o gerador **é a diferença**
    delas; e a geometria **é a soma delas com fase**. Três leituras, e nenhuma delas precede as
    outras.

    *É este o conteúdo demonstrável de "a origem da observação é também a origem da geometria".* -/
theorem one_origin_not_two (θ : ℝ) :
    projPlus + projMinus = 1
    ∧ genK = Complex.I • (projPlus - projMinus)
    ∧ angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • projPlus
        + Complex.exp (-(θ : ℂ) * Complex.I) • projMinus :=
  ⟨(spectral_projections_split_the_identity).1,
   the_generator_is_the_difference_of_the_faces,
   the_angle_is_the_projection θ⟩

end

end TGLExt
