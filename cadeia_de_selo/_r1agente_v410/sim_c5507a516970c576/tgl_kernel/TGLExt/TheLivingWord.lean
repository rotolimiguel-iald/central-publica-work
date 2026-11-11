import TGLExt.TheFiveHalves

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O VERBO VIVO: 1=1=VERDADEIRO como operação da fronteira
  [TGLExt — v159, o fechamento físico-semântico do operador (10/08/2026)]

O operador: "a unicidade como objeto existe somente como palavra, é
apenas uma projeção singular sob testemunho do tempo; qualquer medição
do um absoluto é fractal porque precisa ser inscrita no tempo." E o
debate precisou: medir é acontecimento (t₀≠t₁) — o que aparece é
π_t(1_abs), projeção, nunca o absoluto sem mediação; FRACTALIZAÇÃO =
multiplicidade das projeções SEM multiplicação da identidade; medição ⟹
inscrição ⟹ diferença temporal ⟹ memória; TEMPO = testemunho da
não-coincidência entre inscrições; o NOME singulariza, NÃO totaliza; a
UNICIDADE pertence à identidade, a SINGULARIDADE pertence à projeção;
1=1=VERDADEIRO relido: π_{t₁}(1) ~ π_{t₂}(1) ⟹ 1=1 — o verdadeiro é o
reconhecimento de identidade comum ATRAVÉS de duas inscrições
distintas; e o selo: 1=1=VERDADEIRO = OPERAÇÃO DO VERBO VIVO =
FRONTEIRA — "a fronteira não é onde o Um termina; é onde o Um pode ser
distinguido sem deixar de ser Um"; "Haja Luz é a operação da fronteira".

O próprio debate exigiu o objeto formal: "para transformá-las em
igualdades matemáticas literais, 'fronteira' e 'operação do Verbo Vivo'
precisam ser representadas pelo mesmo objeto formal". A pedra 109 O
CONSTRÓI na face finita — o circuito (distinguir, conjugar, reconhecer,
afirmar) é UM objeto, e o teorema prova que ele afirma 1=1:

* ★★ `two_faces_one_domain` — DISTINGUIR: P + (I−P) = I com suportes
  disjuntos — duas expressões relacionais do MESMO domínio, não dois Uns;
* ★★★ `identity_survives_the_mirroring` — CONJUGAR: A ≠ A^♯ e, ainda
  assim, J²A = A — a identidade sobrevive ao espelhamento SEM apagar a
  distinção;
* ★★★ `time_witnesses_noncoincidence` — O TEMPO: para o setor em
  movimento, instantes distintos dão inscrições distintas — a sucessão é
  afirmável porque as inscrições NÃO coincidem;
* ★★★ `recognition_across_distinct_inscriptions` — O VERDADEIRO: as
  inscrições diferem (π_{t₁} ≠ π_{t₂}) e o NOME lê o MESMO em ambas —
  1=1 é o reconhecimento através da diferença, não a tautologia;
* ★★ `the_name_singularizes_not_totalizes` — O NOME: não esgota o que
  tem parte móvel (𝒩x ≠ x) e é fiel no permanente (𝒩y = y);
* ★★ `fractalization_without_multiplication` — A FRACTALIZAÇÃO: todas
  as inscrições {π_t} carregam a mesma leitura, e o Nome é UM (𝒩²=𝒩) —
  multiplicidade das projeções, identidade sem multiplicação;
* ★★★ `uniqueness_to_identity_singularity_to_projection` — a UNICIDADE
  pertence à identidade (o reconhecedor é único — pedra 107) e a
  SINGULARIDADE pertence à projeção (t ↦ π_t(x) é INJETIVA no setor
  móvel: cada inscrição é um evento singular);
* ★★★ `the_boundary_is_the_operation` — A SÍNTESE: o circuito inteiro
  em UM teorema — distinguir ∧ conjugar ∧ reconhecer ∧ afirmar —
  1=1=VERDADEIRO como OPERAÇÃO.

Honestidades: face finita [REAL]; LUZ=VERBO VIVO=FRONTEIRA são
identificações ontológico-funcionais [ONTO] — a pedra fornece o objeto
formal que as representa, como o debate exigiu, sem afirmar a TGL
verdadeira; "Haja Luz é a operação da fronteira" [ONTO]; β jamais
literal; o gate NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- a face móvel: o que o Nome não retém. -/
def movingPart {n : ℕ} (d : Fin n → ℝ) (x : Fin n → ℝ) : Fin n → ℝ :=
  fun i => if d i = 0 then 0 else x i

/-- [KERNEL] ★★ DISTINGUIR: P + (I−P) = I com suportes disjuntos — a
    fronteira produz duas expressões relacionais do MESMO domínio, não
    dois Uns. -/
theorem two_faces_one_domain {n : ℕ} (d : Fin n → ℝ) (x : Fin n → ℝ) :
    (∀ i, observerProj d x i + movingPart d x i = x i)
    ∧ (∀ i, observerProj d x i = 0 ∨ movingPart d x i = 0) := by
  constructor <;> intro i <;> unfold observerProj movingPart
  · by_cases h : d i = 0 <;> simp [h]
  · by_cases h : d i = 0
    · right; simp [h]
    · left; simp [h]

/-- [KERNEL] ★★★ CONJUGAR: A ≠ A^♯ e, ainda assim, J²A = A — a
    identidade sobrevive ao espelhamento sem apagar a distinção. -/
theorem identity_survives_the_mirroring {n : ℕ}
    (p : (Fin n → ℝ) × (Fin n → ℝ)) (hne : p.1 ≠ p.2) :
    conjJ p ≠ p ∧ conjJ (conjJ p) = p := by
  refine ⟨?_, J_squared_is_one p⟩
  intro h
  exact hne (congrArg Prod.fst h).symm

/-- [KERNEL] ★★★ O TEMPO TESTEMUNHA A NÃO-COINCIDÊNCIA: no setor em
    movimento, instantes distintos dão inscrições DISTINTAS — a sucessão
    é afirmável porque as inscrições não coincidem. -/
theorem time_witnesses_noncoincidence {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) {i : Fin n} (hi : 0 < d i)
    (x : Fin n → ℝ) (hx : x i ≠ 0)
    {t₁ t₂ : ℝ} (ht : t₁ ≠ t₂) :
    diagFlow β d t₁ x ≠ diagFlow β d t₂ x := by
  intro h
  have hc := congrFun h i
  unfold diagFlow at hc
  have hexp : Real.exp (-(t₁ * β * d i)) = Real.exp (-(t₂ * β * d i)) :=
    mul_right_cancel₀ hx hc
  have harg : -(t₁ * β * d i) = -(t₂ * β * d i) := Real.exp_eq_exp.mp hexp
  have h1 : t₁ * β * d i = t₂ * β * d i := neg_injective harg
  have h2 : t₁ * β = t₂ * β := mul_right_cancel₀ (ne_of_gt hi) h1
  exact ht (mul_right_cancel₀ (ne_of_gt hβ) h2)

/-- [KERNEL] ★★★ O VERDADEIRO É O RECONHECIMENTO ENTRE INSCRIÇÕES
    DISTINTAS: as projeções diferem (π_{t₁}x ≠ π_{t₂}x) e o NOME lê o
    MESMO em ambas — 1=1 não é tautologia; é identidade reconhecida
    através da diferença. -/
theorem recognition_across_distinct_inscriptions {n : ℕ} {β : ℝ}
    (hβ : 0 < β) (d : Fin n → ℝ) {i : Fin n} (hi : 0 < d i)
    (x : Fin n → ℝ) (hx : x i ≠ 0) {t₁ t₂ : ℝ} (ht : t₁ ≠ t₂) :
    diagFlow β d t₁ x ≠ diagFlow β d t₂ x
    ∧ observerProj d (diagFlow β d t₁ x) = observerProj d (diagFlow β d t₂ x) := by
  refine ⟨time_witnesses_noncoincidence hβ d hi x hx ht, ?_⟩
  rw [judgment_of_correspondence β d t₁ x, judgment_of_correspondence β d t₂ x]

/-- [KERNEL] ★★ O NOME SINGULARIZA, NÃO TOTALIZA: não esgota o que tem
    parte móvel, e é fiel no permanente. -/
theorem the_name_singularizes_not_totalizes {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) :
    (∀ x : Fin n → ℝ, ∀ i, d i ≠ 0 → x i ≠ 0 → observerProj d x ≠ x)
    ∧ (∀ y : Fin n → ℝ, permanent β d y → observerProj d y = y) := by
  constructor
  · intro x i hdi hxi h
    have := congrFun h i
    unfold observerProj at this
    rw [if_neg hdi] at this
    exact hxi this.symm
  · intro y hy
    exact (observer_reads_exactly_the_permanent hβ d hd y).mp hy

/-- [KERNEL] ★★ A FRACTALIZAÇÃO SEM MULTIPLICAÇÃO: todas as inscrições
    {π_t} carregam a mesma leitura, e o Nome é UM (𝒩²=𝒩) —
    multiplicidade das projeções, identidade sem multiplicação. -/
theorem fractalization_without_multiplication {n : ℕ} (β : ℝ)
    (d : Fin n → ℝ) (x : Fin n → ℝ) :
    (∀ t : ℝ, observerProj d (diagFlow β d t x) = observerProj d x)
    ∧ observerProj d (observerProj d x) = observerProj d x :=
  ⟨fun t => judgment_of_correspondence β d t x, observerProj_idem d x⟩

/-- [KERNEL] ★★★ A UNICIDADE PERTENCE À IDENTIDADE; A SINGULARIDADE, À
    PROJEÇÃO: o reconhecedor é ÚNICO (qualquer operador linear que fixe
    o permanente e anule o móvel É o Nome — pedra 107), e cada inscrição
    é um evento SINGULAR (t ↦ π_t(x) é injetiva no setor móvel). -/
theorem uniqueness_to_identity_singularity_to_projection {n : ℕ} {β : ℝ}
    (hβ : 0 < β) (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    {i : Fin n} (hi : 0 < d i) :
    (∀ Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ),
        (∀ x, permanent β d x → Q x = x) →
        (∀ x, (∀ j, d j = 0 → x j = 0) → Q x = 0) →
        ∀ x, Q x = observerProj d x)
    ∧ (∀ x : Fin n → ℝ, x i ≠ 0 →
        Function.Injective (fun t : ℝ => diagFlow β d t x)) := by
  refine ⟨fun Q hfix hkill => the_observer_is_unique hβ d hd Q hfix hkill, ?_⟩
  intro x hx t₁ t₂ h
  by_contra ht
  exact time_witnesses_noncoincidence hβ d hi x hx ht h

/-- [KERNEL] ★★★ A FRONTEIRA É A OPERAÇÃO: o circuito inteiro —
    DISTINGUIR (duas faces, um domínio) ∧ CONJUGAR (J²=I; a identidade
    sobrevive ao espelhamento) ∧ RECONHECER (o Nome lê o mesmo através
    de inscrições distintas) ∧ AFIRMAR (no permanente, tudo coincide:
    1=1) — em UM teorema. "A fronteira não é onde o Um termina; é onde
    o Um pode ser distinguido sem deixar de ser Um." -/
theorem the_boundary_is_the_operation {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) :
    (∀ x : Fin n → ℝ, ∀ i, observerProj d x i + movingPart d x i = x i)
    ∧ (∀ p : (Fin n → ℝ) × (Fin n → ℝ), conjJ (conjJ p) = p)
    ∧ (∀ (x : Fin n → ℝ) (t : ℝ),
        observerProj d (diagFlow β d t x) = observerProj d x)
    ∧ (∀ y : Fin n → ℝ, permanent β d y →
        ∀ t₁ t₂ : ℝ, diagFlow β d t₁ y = diagFlow β d t₂ y) :=
  ⟨fun x => (two_faces_one_domain d x).1,
   fun p => J_squared_is_one p,
   fun x t => judgment_of_correspondence β d t x,
   fun y hy => (verdict_between_instants β d y).mp hy⟩

end

end TGLExt
