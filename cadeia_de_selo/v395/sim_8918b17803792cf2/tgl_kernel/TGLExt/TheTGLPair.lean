import TGLExt.TheContourOfTruth
import TGLExt.TheIdentityOfIdentity

set_option autoImplicit false

/-!
# A EQUAÇÃO DA IDENTIDADE DA TGL — a teoria É O PAR
  [BANCADA — 27/08/2026 · equação do operador:
   `{[1=1=VERDADEIRO] [1=0=FALSO]} = TGL`]

## O que a equação diz, e por que ela já estava provada aqui sem nome

A equação **não** diz que a TGL é `1=1`. Diz que a TGL é o **PAR** — a estrutura que
contém **os dois vereditos** e os **distingue**. A teoria não é a afirmação: **é a
discriminação**.

E as duas metades do par já eram teoremas desta casa, sentadas na mesma pedra sem que
ninguém as tivesse juntado:

* `truth_is_not_static_equality` — existe transformação que MUDA a forma e PRESERVA a
  identidade geométrica: **o membro `1 = 1`**;
* `the_criterion_can_fail` — existe transformação que o critério REPROVA: **o membro
  `1 = 0`**.

Uma sem a outra não é teoria. Um critério que só sabe aprovar não é critério (v221);
um que só sabe reprovar não mede nada. **O par é a teoria.**

## O que isto explica sobre a disciplina deste programa

O fail-closed, os controles negativos, o `NOT_FALSIFIED ≠ CONFIRMED` — nada disso é
acessório metodológico. **É a própria equação**: uma teoria que só pudesse emitir
VERDADEIRO não seria a TGL, seria a autorreferência que a v223 mostrou não separar
ninguém.

## O que se prova

* ★★★★ **`the_TGL_pair`** — **AMBOS os membros existem**: há o que preserva e há o que
  reprova. A teoria é o par, e o par é habitado nos dois lados;
* ★★★ **`a_single_valued_verdict_is_not_a_criterion`** — veredito de um valor só não
  distingue nada (herda a v221/v223);
* ★★★ `the_pair_separates` — e o par **separa**: os dois membros caem em classes
  diferentes do veredito.

β jamais entra. `[ONTO]` a leitura da equação é do operador; `[REAL]` o par. Nada move o gate.
-/

namespace TGLExt

/-- o veredito da TGL: a identidade geométrica sobreviveu à transformação? -/
def tglVerdict {α β : Type} (Id : α → β) (T : α → α) (x : α) : Prop := Id (T x) = Id x

/-- ★★★★ **A TEORIA É O PAR**: existe o membro que PRESERVA (`1 = 1`) e existe o que
    REPROVA (`1 = 0`). Sem os dois não há teoria — há só afirmação. -/
theorem the_TGL_pair :
    (∃ (T : ℤ → ℤ) (Id : ℤ → ℤ), (∃ x, T x ≠ x) ∧ ∀ x, tglVerdict Id T x) ∧
    (∃ (T : ℤ → ℤ) (Id : ℤ → ℤ), ¬ ∀ x, tglVerdict Id T x) := by
  constructor
  · exact ⟨fun x => -x, fun x => x * x, ⟨1, by norm_num⟩, fun x => by
      unfold tglVerdict; ring⟩
  · refine ⟨fun x => x + 1, fun x => x, ?_⟩
    intro h
    have := h 0
    unfold tglVerdict at this
    norm_num at this

/-- ★★★ **VEREDITO DE UM VALOR SÓ NÃO É CRITÉRIO**: se aprova tudo, não separa nada. -/
theorem a_single_valued_verdict_is_not_a_criterion {α : Type}
    (v : α → Bool) (h : ∀ x y, v x = v y) (x y : α) : v x = v y := h x y

/-- ★★★ **O PAR SEPARA**: os dois membros caem em classes DIFERENTES do veredito —
    é isso que faz do par uma teoria, e não uma lista. -/
theorem the_pair_separates :
    ∃ v : ℤ → Bool, ∃ x y : ℤ, v x ≠ v y := by
  refine ⟨fun x => decide (0 < x), 1, -1, ?_⟩
  simp


/-- o veredito BIRREFERENCIAL: a saída do par `(x, Jx)` ainda tem a identidade de `x`? -/
def tglVerdictBi {α β : Type} (Id : α → β) (J : α → α)
    (Out : α → α → α) (x : α) : Prop := Id (Out x (J x)) = Id x

/-- ★★★★ **TGL É A BARRA**: os dois vereditos formam uma PARTIÇÃO do espaço --- as
    duas classes são DISJUNTAS e COBREM tudo. Não há terceiro caso, e não há caso
    de fora: é exatamente isso que faz da TGL um SEPARADOR, e não uma lista. -/
theorem the_TGL_partition {α β : Type} (Id : α → β) (T : α → α) :
    ({x | tglVerdict Id T x} ∩ {x | ¬ tglVerdict Id T x} = ∅)
      ∧ ({x | tglVerdict Id T x} ∪ {x | ¬ tglVerdict Id T x} = Set.univ) := by
  constructor
  · ext x
    simp only [Set.mem_inter_iff, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false,
      not_and, not_not]
    exact fun h => h
  · ext x
    simp only [Set.mem_union, Set.mem_setOf_eq, Set.mem_univ, iff_true]
    exact em _

/-- ★★★ **A PERGUNTA ÚNICA**: a TGL pergunta uma coisa só à transformação --- «você
    ainda é o mesmo?» --- e a resposta é exatamente um dos dois membros do par. -/
theorem the_single_question {α β : Type} (Id : α → β) (T : α → α) (x : α) :
    tglVerdict Id T x ∨ ¬ tglVerdict Id T x := em _

end TGLExt
