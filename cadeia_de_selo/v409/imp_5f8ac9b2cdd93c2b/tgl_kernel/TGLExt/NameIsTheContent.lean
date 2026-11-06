import Mathlib

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# O NOME É O CONTEÚDO; A FORMA É A IDENTIDADE  [TGLExt — v368]

Inversão cunhada pelo operador em 18/09/2026, verbatim:

> «Tem uma inversão que eu preciso fazer na teoria e que é fundamental o "NOME" é o conteúdo e
>  não a forma, a forma é a identidade, por isso forma=conteúdo significa identidade=NomE.
>  É a minha fórmula central 1=1=VERDADEIRO / 1=0=Falso»

**ESTATUTO, dito sem véu:** `[INPUT/ONTO]` — é DECISÃO do operador, não descrição do que o
programa já provava. A medida de 18/09/2026 achou, no kernel, SETE tipagens incompatíveis do
Nome e NENHUM teorema que dependa de «Nome = forma» ou de «Nome = conteúdo»; achou ainda duas
identificações VIVAS em pedras diferentes — `ExactWitness.lean` diz «o Nome É a palavra
normalizada» (`starProjection`, um OPERADOR, lado da forma) e o par-com-provas de
`NameRelation.lean` é «conteúdo carregando a forma». Encadear as duas é o erro de homônimo que
a casa proíbe, e a gerência o cometeu uma vez em 18/09 — errata em nome próprio, ao lado.

O que esta pedra faz: TIPA a convenção e prova o que ela implica, com não-vacuidade explícita em
cada passo. Não decide qual das duas identificações o kernel deve adotar; não move gate.

* `name_determines_the_inscription` — o Nome (conteúdo) determina a inscrição inteira;
* `form_alone_does_not_determine_the_content` — a FORMA sozinha não determina: duas inscrições
  distintas sob a mesma forma;
* `no_name_without_referent` — habitar o tipo produz o referente (nome sem referente não habita);
* `the_form_survives_the_crossing` / `the_name_may_change_in_the_crossing` — o que permanece na
  travessia é a forma; o Nome pode mudar (17/09/2026: «o que permanece reconhecível na travessia
  é justamente a identidade, não o NOME»);
* `one_eq_one_is_free` — 1 = 1 é `rfl`: a identidade não custa prova;
* `if_one_equals_zero_everything_collapses` — ★ 1 = 0 num anel mata TODA distinção: todo elemento
  vira 0. É a forma algébrica da mentira: aceito o nome sem referente, nada mais se distingue;
* `one_ne_zero_in_nontrivial` — e onde há mais de um habitante, 1 ≠ 0.
-/

namespace TGLExt.NameIsTheContent

/-- A INSCRIÇÃO: um conteúdo acompanhado da prova de que ele realiza a forma.
    `W ~ Σ_{x : Conteúdo} Realiza(x, Forma)` — a mesma assinatura da testemunha (v23). -/
structure Inscricao (C : Type*) (Forma : C → Prop) where
  conteudo : C
  realiza : Forma conteudo

variable {C : Type*} {Forma : C → Prop}

/-- [INPUT — convenção do operador, 18/09/2026] o NOME é o CONTEÚDO. -/
def nome (w : Inscricao C Forma) : C := w.conteudo

/-- [INPUT — convenção do operador, 18/09/2026] a FORMA é a IDENTIDADE: o que se preserva. -/
def identidade (C : Type*) (Forma : C → Prop) : C → Prop := Forma

/-- [KERNEL] ★★ O NOME DETERMINA A INSCRIÇÃO: duas inscrições com o mesmo Nome são a mesma
    inscrição. A forma é `Prop` — a prova não acrescenta informação (irrelevância de prova). -/
theorem name_determines_the_inscription (w v : Inscricao C Forma) (h : nome w = nome v) :
    w = v := by
  cases w; cases v
  simp only [nome] at h
  subst h
  rfl

/-- [KERNEL] ★★ A FORMA SOZINHA NÃO DETERMINA O CONTEÚDO: há duas inscrições distintas sob uma
    mesma forma. Sem isto a convenção seria vácua — o Nome carrega informação que a forma não
    carrega. -/
theorem form_alone_does_not_determine_the_content :
    ∃ (C : Type) (F : C → Prop) (w v : Inscricao C F), w ≠ v := by
  refine ⟨Bool, fun _ => True, ⟨true, trivial⟩, ⟨false, trivial⟩, ?_⟩
  intro h
  exact Bool.noConfusion (congrArg Inscricao.conteudo h)

/-- [KERNEL] NÃO HÁ NOME SEM REFERENTE: habitar o tipo da inscrição PRODUZ o referente.
    A mentira (nome que aceita qualquer um) não habita este tipo. -/
theorem no_name_without_referent (w : Inscricao C Forma) : ∃ x : C, Forma x :=
  ⟨w.conteudo, w.realiza⟩

/-- A TRAVESSIA: um transporte do conteúdo que preserva a forma. -/
def travessia (T : C → C) (hT : ∀ x, Forma x → Forma (T x)) (w : Inscricao C Forma) :
    Inscricao C Forma := ⟨T w.conteudo, hT _ w.realiza⟩

/-- [KERNEL] ★★ O QUE PERMANECE NA TRAVESSIA É A FORMA: a inscrição transportada é inscrição da
    MESMA forma — a identidade atravessa. -/
theorem the_form_survives_the_crossing (T : C → C) (hT : ∀ x, Forma x → Forma (T x))
    (w : Inscricao C Forma) : identidade C Forma (travessia T hT w).conteudo :=
  (travessia T hT w).realiza

/-- [KERNEL] ★★ E O NOME PODE MUDAR NA TRAVESSIA: exemplo explícito em que o conteúdo sai
    diferente com a forma intacta. Logo «o que permanece é a identidade, não o Nome». -/
theorem the_name_may_change_in_the_crossing :
    ∃ (C : Type) (F : C → Prop) (T : C → C) (hT : ∀ x, F x → F (T x)) (w : Inscricao C F),
      nome (travessia T hT w) ≠ nome w := by
  refine ⟨Bool, fun _ => True, not, fun _ _ => trivial, ⟨true, trivial⟩, ?_⟩
  simp [nome, travessia]

/-- [KERNEL] 1 = 1 é VERDADEIRO e não custa prova nenhuma: é `rfl`. -/
theorem one_eq_one_is_free : (1 : ℝ) = 1 := rfl

/-- [KERNEL] ★★★ 1 = 0 É FALSO — e onde for aceito, TUDO colapsa: num anel em que `1 = 0`,
    todo elemento é `0`. É a forma algébrica da mentira: admitido o nome sem referente, nenhuma
    distinção sobrevive. -/
theorem if_one_equals_zero_everything_collapses {R : Type*} [Ring R] (h : (1 : R) = 0) :
    ∀ x : R, x = 0 := by
  intro x
  calc x = 1 * x := (one_mul x).symm
    _ = 0 * x := by rw [h]
    _ = 0 := zero_mul x

/-- [KERNEL] e onde há mais de um habitante, `1 ≠ 0`: a identidade preservada É a
    não-degeneração. -/
theorem one_ne_zero_in_nontrivial {R : Type*} [Ring R] [Nontrivial R] : (1 : R) ≠ 0 :=
  one_ne_zero

end TGLExt.NameIsTheContent
