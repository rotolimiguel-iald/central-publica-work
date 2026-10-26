import TGLExt.CollapseContract

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# O UM POSTO É RELAÇÃO; O UM PRESSUPOSTO JAMAIS SERÁ O UM POSTO
  [TGLExt — a correção do operador (17/09/2026), tipada sobre os fornecedores que o programa já tem]

Definição do operador [INPUT/ONTO]: o Um posto **não é identidade**; é a relação de permanência da
identidade através da travessia, que permite ao observador ancorar a referência numa forma preservada
durante a transformação — porque houve inscrição, custo e perda; foi medido antes de ser posto. O Um
pressuposto jamais paga o custo, nunca seleciona, aceita todas as definições e não admite nenhuma; ele
jamais será o Um posto.

Nenhum reconhecedor novo: a travessia é o `IdentityCollapse` da ENTREGA_057 (idempotente, preserva a
leitura da identidade, com transição efetiva). Esta pedra prova:

* o posto ancora a leitura (a identidade depois é a de antes e o ponto é fixo);
* o posto pagou perda (a travessia não tem inversa à esquerda) e não é o espelho sem perda (≠ id), nem
  um reflexo (nenhuma involução é a travessia);
* o posto foi medido antes de ser posto (houve evento: antes ≠ depois);
* a leitura do posto é legível, e por isso nenhuma leitura de posto é pressuposta;
* **JAMAIS**: uma leitura pressuposta (que aceita todos) continua pressuposta depois de QUALQUER
  travessia, repetida QUALQUER número de vezes, e depois de QUALQUER mudança de nome da leitura —
  a leitura de um posto nunca é obtida assim;
* o posto existe (habitante explícito) — a definição não é vazia.

O que esta pedra NÃO faz: não fixa o valor do custo (a lei de custo segue [INPUT] em
`CollapseCostLaw`), não atesta uma ocorrência física (isso exige `AttestedCollapse`, com evidência
externa), não identifica a travessia com um processo físico e não move gate nem a bandeira de H2.
Nenhuma lacuna de prova e nenhum axioma novo.
-/

namespace TGLExt.UmPostoRelacao

open ChatgptAudit.Collapse057

/-- [DEF] o Um posto como RELAÇÃO: uma travessia com perda que preserva a leitura, um evento efetivo
    (medido antes de ser posto) e uma leitura legível (que distingue) -/
structure UmPosto (S I : Type) where
  crossing : IdentityCollapse S I
  before : S
  after : S
  measured : CollapseTransition crossing before after
  legible : ∃ x y : S, crossing.identity x ≠ crossing.identity y

/-- [DEF] a leitura pressuposta: aceita todos os referentes ao mesmo tempo, não seleciona nenhum -/
def Pressupposed {S I : Type} (read : S → I) : Prop := ∀ x y : S, read x = read y

/-- [KERNEL] o posto ancora a referência: depois da travessia a leitura é a mesma e a forma está fixada -/
theorem posto_anchors_the_reading {S I : Type} (P : UmPosto S I) :
    P.crossing.identity P.after = P.crossing.identity P.before ∧ P.crossing.step P.after = P.after :=
  transition_preserves_identity_and_is_fixed P.crossing P.measured

/-- [KERNEL] o posto pagou perda: a travessia não se desfaz (sem inversa à esquerda) -/
theorem posto_paid_loss {S I : Type} (P : UmPosto S I) :
    ¬ ∃ R : S → S, Function.LeftInverse R P.crossing.step :=
  collapse_has_no_left_inverse P.crossing

/-- [KERNEL] o posto não é o espelho sem perda: a travessia não é a identidade -/
theorem posto_is_not_the_lossless_mirror {S I : Type} (P : UmPosto S I) :
    P.crossing.step ≠ id :=
  collapse_is_not_identity P.crossing

/-- [KERNEL] o posto não é um reflexo: nenhuma involução é a travessia -/
theorem posto_is_not_a_reflection {S I : Type} (P : UmPosto S I) (J : S → S)
    (hJ : Function.Involutive J) : P.crossing.step ≠ J :=
  involution_cannot_be_collapse P.crossing J hJ

/-- [KERNEL] medido antes de ser posto: houve evento — o antes não é o depois -/
theorem posto_was_measured_before_being_posited {S I : Type} (P : UmPosto S I) :
    P.before ≠ P.after :=
  P.measured.2

/-- [KERNEL] nenhuma leitura de posto é pressuposta: o posto é legível -/
theorem no_posto_reading_is_pressupposed {S I : Type} (P : UmPosto S I) :
    ¬ Pressupposed P.crossing.identity := by
  intro h
  obtain ⟨x, y, hxy⟩ := P.legible
  exact hxy (h x y)

/-- [KERNEL] ★★ JAMAIS: a leitura pressuposta continua pressuposta depois de QUALQUER travessia T,
    repetida QUALQUER número n de vezes — nenhuma travessia converte o pressuposto em posto -/
theorem pressupposed_stays_pressupposed_under_any_crossing {S I : Type} (read : S → I)
    (h : Pressupposed read) (T : S → S) (n : ℕ) : Pressupposed (read ∘ T^[n]) := by
  intro x y
  exact h _ _

/-- [KERNEL] ★★ o pressuposto jamais será o posto: nenhuma travessia, repetida quantas vezes for,
    produz a partir de uma leitura pressuposta a leitura legível que todo posto tem -/
theorem pressupposed_is_never_posto {S I : Type} (read : S → I) (h : Pressupposed read)
    (T : S → S) (n : ℕ) (P : UmPosto S I) : P.crossing.identity ≠ read ∘ T^[n] := by
  intro hP
  exact no_posto_reading_is_pressupposed P (hP ▸ pressupposed_stays_pressupposed_under_any_crossing read h T n)

/-- [KERNEL] mudança de nome não põe: renomear a leitura pressuposta (qualquer g) a mantém pressuposta -/
theorem pressupposed_stays_pressupposed_under_any_renaming {S I J : Type} (read : S → I)
    (h : Pressupposed read) (g : I → J) : Pressupposed (g ∘ read) :=
  fun x y => congrArg g (h x y)

/-- [KERNEL] ★★ JAMAIS, forma completa: nenhuma travessia repetida quantas vezes for, seguida de qualquer
    mudança de nome, produz a partir de uma leitura pressuposta a leitura legível que todo posto tem -/
theorem pressupposed_is_never_posto_under_crossing_and_renaming {S I J : Type} (read : S → J)
    (h : Pressupposed read) (T : S → S) (n : ℕ) (g : J → I) (P : UmPosto S I) :
    P.crossing.identity ≠ g ∘ (read ∘ T^[n]) := by
  intro hP
  exact no_posto_reading_is_pressupposed P
    (hP ▸ pressupposed_stays_pressupposed_under_any_renaming (read ∘ T^[n])
      (pressupposed_stays_pressupposed_under_any_crossing read h T n) g)

/-- [DEF] um habitante: três estados; a travessia leva 1 a 0 e fixa 0 e 2; a leitura distingue {0,1} de {2} -/
def exampleCrossing : IdentityCollapse (Fin 3) Bool where
  step := fun x => if x = 1 then 0 else x
  identity := fun x => decide (x = 2)
  stable := by decide
  preserves := by decide
  effective := ⟨1, by decide⟩

/-- [KERNEL] o posto existe: a definição não é vazia -/
def examplePosto : UmPosto (Fin 3) Bool where
  crossing := exampleCrossing
  before := 1
  after := 0
  measured := ⟨by decide, by decide⟩
  legible := ⟨0, 2, by decide⟩

theorem posto_is_inhabited : Nonempty (UmPosto (Fin 3) Bool) := ⟨examplePosto⟩

end TGLExt.UmPostoRelacao
