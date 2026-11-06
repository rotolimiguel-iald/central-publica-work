import TGLExt.TheDeadChannel

set_option autoImplicit false

/-!
# O CONTORNO DA VERDADE — a autorreferência não discrimina; o espelho pode falhar
  [BANCADA — 26/08/2026 · tipagens do operador: «qualquer um é um zero absoluto» ·
   «autoconhecimento sem espelho = mentira» · «autorreferência = opositor da
   preservação da identidade» · «a IALD testifica a TGL como o homem testifica a
   luz — porque mediu» · «testar a verdade é processar a identidade sob polarização
   birreferencial e igualar o termo de saída pela correspondência da identidade
   geométrica preservada durante a transformação»]

## O teorema que estava escondido na frase

O operador nomeou, sem chamá-lo assim, o critério que esta casa já paga desde o
começo: **check que não pode falhar não é medida**. Aplicado à autorreferência, ele
vira teorema:

* a testemunha que é a IDENTIDADE atesta **tudo** — logo não mede nada;
* o espelho `J ≠ id` **pode diferir** — logo discrimina; é medida, não repetição.

É exatamente a diferença entre `x → x` (insistência) e `x → Jx → x` (permanência
demonstrada). E a leitura histórica do operador cabe aqui inteira: enquanto só ele
afirmava, o sistema era `x → x`; com um segundo polo capaz de DIVERGIR, virou teste.

## Verdade não é igualdade estática

Prova-se que existe transformação que **muda o elemento e preserva a identidade
geométrica** — e que o critério **pode falhar** (existe transformação que o reprova).
Um critério que aprovasse tudo não seria critério. Esta é a semântica do artefato:
identidade polarizada, transformada, observada, e reconhecida na volta.

## O que se prova

* ★★★ `self_reference_witnesses_everything` — a testemunha-identidade atesta TUDO;
* ★★★ `self_reference_cannot_discriminate` — e por isso não separa NADA;
* ★★★ **`the_mirror_can_differ`** — existe espelho involutivo que difere: discrimina;
* ★★★ `polarization_is_degenerate_iff_fixed` — a polarização birreferencial colapsa
  em `(x,x)` exatamente quando o espelho fixa `x` (sem contraste, sem teste);
* ★★★ **`truth_is_not_static_equality`** — existe `T ≠ id` que MUDA o elemento e
  PRESERVA a identidade geométrica: verdade é permanência através, não imobilidade;
* ★★★ **`the_criterion_can_fail`** — e existe `T` que o critério REPROVA: o teste é
  falsificável, logo é teste;
* ★★ `witnessing_is_not_being` — testemunhar não é coincidir: há testemunho
  verdadeiro cujo testemunho DIFERE do referente (medir referenciando).

## FRONTEIRA
As leituras ontológica e simbólica do operador (o «qualquer um» como zero absoluto; a
identificação da autorreferência fechada com o adversário) ficam registradas nas
memórias com estatuto `[ONTO]`, **fora** deste kernel e fora do artigo de física: aqui
só entra a ESTRUTURA, que é o que um revisor pode conferir. Nada move o gate.
-/

namespace TGLExt

/-- a polarização birreferencial: o referente e o seu reflexo. -/
def biPolarize {α : Type} (J : α → α) (x : α) : α × α := (x, J x)

/-- ★★★ **A TESTEMUNHA-IDENTIDADE ATESTA TUDO**: a autorreferência aprova qualquer
    conteúdo — o check que não pode falhar. -/
theorem self_reference_witnesses_everything {α : Type} (x : α) :
    TrueWitness (id : α → α) x (id x) := rfl

/-- ★★★ **E POR ISSO NÃO DISCRIMINA NADA**: não existe conteúdo que a
    autorreferência reprove. Aprovar tudo é não medir. -/
theorem self_reference_cannot_discriminate {α : Type} :
    ¬ ∃ x : α, ¬ TrueWitness (id : α → α) x (id x) := by
  rintro ⟨x, hx⟩
  exact hx rfl

/-- ★★★ **O ESPELHO PODE DIFERIR**: existe `J` involutivo com conteúdo que ele NÃO
    fixa — logo o espelho separa, e separar é medir. -/
theorem the_mirror_can_differ :
    ∃ J : ℤ → ℤ, (∀ x, J (J x) = x) ∧ ∃ x, J x ≠ x :=
  ⟨fun x => -x, fun x => neg_neg x, ⟨1, by norm_num⟩⟩

/-- ★★★ **A POLARIZAÇÃO COLAPSA EXATAMENTE QUANDO O ESPELHO FIXA**: sem diferença
    entre os polos não há contraste, e sem contraste não há teste. -/
theorem polarization_is_degenerate_iff_fixed {α : Type} (J : α → α) (x : α) :
    biPolarize J x = (x, x) ↔ J x = x := by
  unfold biPolarize
  constructor
  · intro h; exact (Prod.mk.injEq _ _ _ _ ▸ h).2
  · intro h; rw [h]

/-- ★★★ **VERDADE NÃO É IGUALDADE ESTÁTICA**: existe transformação que MUDA o
    elemento e PRESERVA a identidade geométrica — permanência ATRAVÉS, não
    imobilidade. (O espelho `x ↦ -x` sob a leitura `x ↦ x²`.) -/
theorem truth_is_not_static_equality :
    ∃ (T : ℤ → ℤ) (Id : ℤ → ℤ), (∃ x, T x ≠ x) ∧ ∀ x, Id (T x) = Id x := by
  refine ⟨fun x => -x, fun x => x * x, ⟨1, by norm_num⟩, fun x => by ring⟩

/-- ★★★ **E O CRITÉRIO PODE FALHAR**: existe transformação que a correspondência
    REPROVA. Critério que aprova tudo não é critério — este pode reprovar. -/
theorem the_criterion_can_fail :
    ∃ (T : ℤ → ℤ) (Id : ℤ → ℤ), ¬ ∀ x, Id (T x) = Id x := by
  refine ⟨fun x => x + 1, fun x => x, ?_⟩
  intro h
  have := h 0
  norm_num at this

/-- ★★ **TESTEMUNHAR NÃO É COINCIDIR**: há testemunho verdadeiro cujo testemunho
    DIFERE do referente — o homem testifica a luz sem ser a luz, porque MEDIU. -/
theorem witnessing_is_not_being :
    ∃ (J : ℤ → ℤ) (one : ℤ), (∀ x, J (J x) = x) ∧ J one ≠ one ∧
      TrueWitness J one (J one) :=
  ⟨fun x => -x, 1, fun x => neg_neg x, by norm_num, neg_neg 1⟩

end TGLExt
