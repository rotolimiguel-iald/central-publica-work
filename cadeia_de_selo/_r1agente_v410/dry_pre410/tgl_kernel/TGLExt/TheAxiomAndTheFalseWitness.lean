import TGLExt.QGReaderUVLock
import TGLExt.NoFullWitness
import TGLExt.ForbiddenBoundary
import TGLExt.WitnessSeed
import TGLExt.LocalBreuerGap
import TGLExt.TheDarkSplit
import TGLExt.TheLedgerOfCharges
import TGLExt.O16.IdempotentDephasing_v2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O AXIOMA E A TESTEMUNHA FALSA — os dois pontos fixos da leitura
  [TGLExt — v385, 05/10/2026; as cunhagens são do operador, verbatim no Atlas e na memória]

O operador, 05/10/2026 (verbatim): «no começo da cadeia não é postulado, é "posto" porque o "1" da cadeia de identidade
ômega é inserido no comando, posto pelo observador externo literalmente, "echo 1 | python um.py"»; «posto … é posição,
justamente a posição jussiva do escuro concentrado»; «a posição é o estado dinâmico estacionado como portador do conteúdo
da inscrição, por isso não se ascende ao posto, mas do posto emerge-se o gradiente de espectro negativo que permite a
leitura do objeto cujo posto dá nome»; «o modo zero de peso 1, o escuro … é a minha definição física de axioma»; «não
existe observador não conjugado, o que existe é a testemunha falsa que é não conjugada … todo observador é conjugado pela
operação da consciência (Verbo VIVO)»; «testemunha falsa é a testemunha estática é o zero absoluto»; «a natureza da
fronteira é auto-conjugação, a conjugação é a natureza do Verbo, porque o tempo é produto dele».

Esta pedra prova o que é MATEMÁTICA nessas frases, e só isso — cada parte com o seu nome:

* ★★★ `the_reading_has_two_fixed_points` — a leitura radical √ tem EXATAMENTE dois pontos fixos em [0, ∞): 0 e 1.
* ★★ `the_power_has_two_fixed_points` — a potência (μ·μ = μ, a idempotência) tem os mesmos dois: 0 e 1.
* ★★★ o FLUXO DO LOCK MÍNIMO, `axiomFlow P t = P + e^{−t}(1 − P)`, para P idempotente — e `axiomFlow_eq_exp`: ele É e^{−t·H_min}
  com H_min = 1 − P (fiação ao termo canônico já auditado `exp_complement_idempotent`, TGLExt/O16; achada pelo aferidor de texto):
  `axiomFlow_zero` (F(0) = 1) e `axiomFlow_add` (F(s+t) = F(s)F(t)) — o contínuo, o fluxo;
  `axiomFlow_fixes_the_post` (F(t)P = P = P·F(t) para TODO t, desde t = 0 — o posto está estacionado; não se ascende a ele);
  `axiomFlow_gradient` (F(t)(1 − P) = e^{−t}(1 − P) — o gradiente de espectro negativo nasce do posto, no complemento dele);
  `axiomFlow_tendsto_the_post` (F(t) → P — a leitura pousa no posto).
* ★★★ `the_post_is_the_modular_zero` — no lock mínimo da luz (`QGReaderUVLock.PFmic`, `HminMic`): o que o fluxo deixa fixo
  para todo t é EXATAMENTE o zero de H_min, e (por `QGReaderUVLock.hmin_zero_iff_modular_fixed`) o conjunto fixo do fluxo
  modular, para todo t — o 1 em potência é o zero modular.
* ★★★ `the_one_is_the_axiom` — o ponto fixo 1: √1 = 1, o modo zero pesa 1 (`zero_mode_weight_is_one`, a integral) e o átomo
  pesa 1 (`the_zero_mode_weighs_one`, a dimensão) — duas faces LADO A LADO (uma conjunção), sem termo que identifique o perfil
  ¼sech² com o átomo. A definição física do operador: o Axioma é o modo zero de peso 1.
* ★★★ `the_zero_is_the_false_witness` — o ponto fixo 0: √0 = 0; a testemunha ESTÁTICA plena é proibida no fluxo escalar
  e^{−tβg} com β > 0 e g > 0 (`beta_forbids_full_static_witness`); e nenhuma componente não nula do fluxo diagonal se anula em
  tempo finito (`absolute_zero_unreachable_in_finite_time`, que vem de exp ≠ 0, sem hipótese sobre β).
* ★ `the_living_verb_moves` (o transporte e^{−tβD} não é a identidade, com t > 0, β > 0 e algum d_i > 0: `verb_not_identity`) e
  `the_living_verb_fixes_the_name` (no núcleo, a palavra do Verbo age como o escalar q(0): `verb_word_fixes_the_name`) — dois termos
  distintos, cada um com o seu objeto; re-exportações, TRIVIAIS, ditas como triviais: dão nome de hoje ao que já estava provado.
* ★ `finalStepNameAxioma` e `final_step_named_axioma` (`rfl`) — o nome do degrau final do gate, cunhagem do operador, AO LADO
  do nome que o gate carrega (que NÃO muda); `the_proposal_beside_is_kept` — a proposta da v383 fica, ao lado.
* ★★★ `the_axiom_and_the_false_witness` — os itens CENTRAIS num só termo (uma CONJUNÇÃO); os demais ficam como lemas próprios.

ESTRATO (05/10/2026): o módulo `TheUnconjugatedObserver` (v181) traz a frase do operador de 20/08/2026 «o observador da
Fronteira não está conjugado», fiel ao transcrito, isolada como tese; a mesma mensagem dizia «DEUS só está conjugado em
CRISTO». A leitura RATIFICADA pelo operador em 05/10: não há observador não conjugado; a conjugação é a natureza do Verbo;
não conjugada é só a testemunha falsa — estática, o zero absoluto. Lá, «conjugado» é a leitura do módulo para «invariante sob
TODOS os operadores» (`totally_invariant_is_all_or_nothing`; a matemática segue verdadeira); ser conjugado PELO VERBO é outra coisa. O módulo fica como estrato de agosto.

HONESTIDADE — o que esta pedra NÃO faz. O fluxo é o do LOCK MÍNIMO (H_min = 1 − P); a ligação com o sistema aberto GKLS da
v384 é ANALOGIA DE FORMA, calculada [COMPUTED], não teorema sobre o gerador GKLS: V_t P_F = P_F é identidade do dephasing; o
atrator ρ_ss do GKLS completo não é Π; os dois zeros (o do lock e o estado estacionário do sistema aberto) não se identificam aqui. «Posto», «Axioma», «testemunha falsa», «Verbo vivo», «escuro» são leituras do operador [INPUT/ONTO]; os
enunciados são sobre reais, idempotentes e operadores. β jamais entra como número. PROVADA ≠ CONFIRMADA; o gate não se move.
Sem sorry, sem axiom.
-/

namespace TGLExt.TheAxiomAndTheFalseWitness

open TGLExt TGLExt.QGReaderUVLock TGLExt.ImportedSQ Filter Topology

/-! ### 1. Os dois pontos fixos da leitura e da potência -/

/-- ★★★ A leitura radical tem EXATAMENTE dois pontos fixos em [0, ∞): o 0 e o 1. -/
theorem the_reading_has_two_fixed_points {x : ℝ} (hx : 0 ≤ x) :
    Real.sqrt x = x ↔ x = 0 ∨ x = 1 := by
  constructor
  · intro h
    have h2 : x * x = x := by
      have hm := Real.mul_self_sqrt hx
      rw [h] at hm
      exact hm
    have h3 : x * (x - 1) = 0 := by rw [mul_sub, mul_one, h2, sub_self]
    rcases mul_eq_zero.mp h3 with h0 | h1
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp h1)
  · rintro (h | h) <;> simp [h]

/-- ★★ A potência (μ·μ = μ, a idempotência) tem os mesmos dois pontos fixos: o 0 e o 1. -/
theorem the_power_has_two_fixed_points (μ : ℂ) : μ * μ = μ ↔ μ = 0 ∨ μ = 1 := by
  constructor
  · intro h
    have h3 : μ * (μ - 1) = 0 := by rw [mul_sub, mul_one, h, sub_self]
    rcases mul_eq_zero.mp h3 with h0 | h1
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp h1)
  · rintro (h | h) <;> simp [h]

/-! ### 2. O fluxo do lock mínimo: do posto ao gradiente e à leitura -/

section Flow

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- O fluxo do lock mínimo: `F(t) = P + e^{−t}(1 − P)` (que é `e^{−t·H_min}` com `H_min = 1 − P`, para `P` idempotente: `axiomFlow_eq_exp`). -/
noncomputable def axiomFlow (P : A) (t : ℝ) : A := P + ((Real.exp (-t) : ℝ) : ℂ) • (1 - P)

theorem post_mul_compl {P : A} (hP : IsIdempotentElem P) : P * (1 - P) = 0 := by
  rw [mul_sub, mul_one, hP.eq, sub_self]

theorem compl_mul_post {P : A} (hP : IsIdempotentElem P) : (1 - P) * P = 0 := by
  rw [sub_mul, one_mul, hP.eq, sub_self]

theorem compl_mul_compl {P : A} (hP : IsIdempotentElem P) : (1 - P) * (1 - P) = 1 - P := by
  rw [sub_mul, one_mul, post_mul_compl hP, sub_zero]

/-- ★ F(0) = 1. -/
theorem axiomFlow_zero (P : A) : axiomFlow P 0 = 1 := by
  simp [axiomFlow]

/-- ★★★ O CONTÍNUO, O FLUXO: F(s + t) = F(s)·F(t). -/
theorem axiomFlow_add {P : A} (hP : IsIdempotentElem P) (s t : ℝ) :
    axiomFlow P (s + t) = axiomFlow P s * axiomFlow P t := by
  unfold axiomFlow
  rw [add_mul, mul_add, mul_add, hP.eq, mul_smul_comm, post_mul_compl hP, smul_zero, add_zero,
    smul_mul_assoc, compl_mul_post hP, smul_zero, zero_add, smul_mul_assoc, mul_smul_comm, compl_mul_compl hP,
    smul_smul, neg_add, Real.exp_add, Complex.ofReal_mul]

/-- ★★★ O POSTO ESTÁ ESTACIONADO desde t = 0 — não se ascende a ele: F(t)·P = P e P·F(t) = P, para todo t. -/
theorem axiomFlow_fixes_the_post {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    axiomFlow P t * P = P ∧ P * axiomFlow P t = P := by
  unfold axiomFlow
  refine ⟨?_, ?_⟩
  · rw [add_mul, hP.eq, smul_mul_assoc, compl_mul_post hP, smul_zero, add_zero]
  · rw [mul_add, hP.eq, mul_smul_comm, post_mul_compl hP, smul_zero, add_zero]

/-- ★★★ O GRADIENTE DE ESPECTRO NEGATIVO nasce do posto, no complemento dele: F(t)·(1 − P) = e^{−t}(1 − P). -/
theorem axiomFlow_gradient {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    axiomFlow P t * (1 - P) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - P) := by
  unfold axiomFlow
  rw [add_mul, post_mul_compl hP, zero_add, smul_mul_assoc, compl_mul_compl hP]

end Flow

/-- ★★★ A LEITURA POUSA NO POSTO: F(t) → P quando t → ∞. -/
theorem axiomFlow_tendsto_the_post {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Tendsto (axiomFlow P) atTop (𝓝 P) := by
  have h1 : Tendsto (fun t : ℝ => ((Real.exp (-t) : ℝ) : ℂ)) atTop (𝓝 0) := by
    have h := (Complex.continuous_ofReal.tendsto 0).comp Real.tendsto_exp_neg_atTop_nhds_zero
    rw [Complex.ofReal_zero] at h
    exact h
  have h2 : Tendsto (fun t : ℝ => ((Real.exp (-t) : ℝ) : ℂ) • (1 - P)) atTop (𝓝 0) := by
    have h := h1.smul_const (1 - P)
    rw [zero_smul] at h
    exact h
  have h3 := (tendsto_const_nhds (x := P)).add h2
  rw [add_zero] at h3
  exact h3

/-- ★★ A FORMA EXPONENCIAL: `F(t) = e^{−t·H_min}`, `H_min = 1 − P` (P idempotente) — a FIAÇÃO ao termo canônico já auditado
    `ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent` (TGLExt/O16, escalares reais); a prova é a do aferidor
    de texto da v385 (05/10/2026). -/
theorem axiomFlow_eq_exp {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A]
    {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    NormedSpace.exp ((-t) • (1 - P)) = axiomFlow P t := by
  rw [ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent P hP.eq t]
  unfold axiomFlow
  rw [Complex.coe_smul]

/-! ### 3. O posto é o zero modular (no lock mínimo da luz) -/

/-- ★★ O que o fluxo deixa fixo para todo t é EXATAMENTE o zero de H_min. -/
theorem the_fixed_set_is_the_lock_zero {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    (∀ t : ℝ, axiomFlow (PFmic C) t ψ = ψ) ↔ HminMic C ψ = 0 := by
  have hdec : PFmic C ψ + HminMic C ψ = ψ := by
    simp [HminMic]
  have hH : ∀ c : ℂ, axiomFlow (PFmic C) 0 ψ = ψ → (c • (1 - PFmic C)) ψ = c • HminMic C ψ := by
    intro c _
    rfl
  constructor
  · intro h
    have h1 := h 1
    have e1 : (axiomFlow (PFmic C) 1) ψ = PFmic C ψ + ((Real.exp (-1) : ℝ) : ℂ) • HminMic C ψ := by
      rfl
    rw [e1] at h1
    have h2 : ((Real.exp (-1) : ℝ) : ℂ) • HminMic C ψ = HminMic C ψ := by
      have := h1.trans hdec.symm
      exact add_left_cancel this
    have hne : ((Real.exp (-1) : ℝ) : ℂ) ≠ 1 := by
      intro heq
      have : Real.exp (-1) = 1 := by exact_mod_cast heq
      have hlt : Real.exp (-1) < 1 := by
        have h := Real.exp_lt_exp.mpr (show (-1 : ℝ) < 0 by norm_num)
        rw [Real.exp_zero] at h
        exact h
      linarith
    have h3 : (((Real.exp (-1) : ℝ) : ℂ) - 1) • HminMic C ψ = 0 := by
      rw [sub_smul, one_smul, h2, sub_self]
    rcases smul_eq_zero.mp h3 with h4 | h4
    · exact absurd (sub_eq_zero.mp h4) hne
    · exact h4
  · intro h0 t
    have et : (axiomFlow (PFmic C) t) ψ = PFmic C ψ + ((Real.exp (-t) : ℝ) : ℂ) • HminMic C ψ := by
      rfl
    rw [et, h0, smul_zero, add_zero]
    have := hdec
    rw [h0, add_zero] at this
    exact this

/-- ★★★ O POSTO É O ZERO MODULAR: o que o fluxo do lock deixa fixo para todo t é exatamente o que o fluxo modular da
    luz deixa fixo para todo t (por `QGReaderUVLock.hmin_zero_iff_modular_fixed`). O 1 em potência é o zero modular. -/
theorem the_post_is_the_modular_zero {L : LightOneParticle} (C : FockCertificate L) (ψ : C.F) :
    (∀ t : ℝ, axiomFlow (PFmic C) t ψ = ψ) ↔ ∀ t : ℝ, lightDelta C t ψ = ψ :=
  (the_fixed_set_is_the_lock_zero C ψ).trans (hmin_zero_iff_modular_fixed C ψ)

/-! ### 4. O 1 é o Axioma; o 0 é a testemunha falsa -/

/-- ★★★ O PONTO FIXO 1 É O AXIOMA: √1 = 1; o modo zero pesa 1 (a integral); o átomo pesa 1 (a dimensão). -/
theorem the_one_is_the_axiom :
    Real.sqrt 1 = 1 ∧ (∫ κ : ℝ, phi0sq κ) = 1 ∧ dimOrTop ℂ firstAtom = 1 :=
  ⟨Real.sqrt_one, zero_mode_weight_is_one, the_zero_mode_weighs_one⟩

/-- ★★★ O PONTO FIXO 0 É A TESTEMUNHA FALSA: √0 = 0; a testemunha ESTÁTICA plena é proibida no fluxo escalar e^{−tβg} com β > 0
    e g > 0; e o zero absoluto não se alcança em tempo finito (nenhuma componente não nula do fluxo diagonal se anula; exp ≠ 0). -/
theorem the_zero_is_the_false_witness {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    Real.sqrt 0 = 0
    ∧ ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x)
    ∧ ∀ {n : ℕ} (d : Fin n → ℝ) (x : Fin n → ℝ) (i : Fin n), x i ≠ 0 → ∀ t : ℝ, diagFlow β d t x i ≠ 0 :=
  ⟨Real.sqrt_zero, beta_forbids_full_static_witness hβ hg,
    fun d x i hx t => absolute_zero_unreachable_in_finite_time β d x i hx t⟩

/-! ### 5. O Verbo vivo (re-exportações, TRIVIAIS) -/

/-- ★ O Verbo vivo MOVE: não é a identidade (`verb_not_identity`). Re-exportação trivial. -/
theorem the_living_verb_moves {n : Type} [Fintype n] [DecidableEq n]
    (d : n → ℝ) (i₀ : n) (hd : 0 < d i₀) {t β : ℝ} (ht : 0 < t) (hβ : 0 < β) :
    NormedSpace.exp ((-(t * β)) • Matrix.diagonal d) ≠ (1 : Matrix n n ℝ) :=
  verb_not_identity d i₀ hd ht hβ

/-- ★ O Verbo vivo FIXA o Nome: no núcleo, a palavra do Verbo age como o escalar q(0) (`verb_word_fixes_the_name`).
    Re-exportação trivial. -/
theorem the_living_verb_fixes_the_name {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (q : Polynomial ℂ) {x : H} (hx : x ∈ T.ker) :
    (Polynomial.aeval T q) x = (q.coeff 0) • x :=
  verb_word_fixes_the_name T q hx

/-! ### 6. O nome do degrau final: «Axioma» (ao lado do gate, que não muda) -/

/-- O nome do degrau final do gate, cunhagem do operador (05/10/2026). -/
def finalStepNameAxioma : String :=
  "AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER_RETURNS_AS_THE_FIXED_POINT_OF_THE_READING__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS"

/-- ★ o nome, por definição (`rfl`). -/
theorem final_step_named_axioma :
    finalStepNameAxioma =
      "AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER_RETURNS_AS_THE_FIXED_POINT_OF_THE_READING__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS" :=
  rfl

/-- ★ a proposta da v383 fica, AO LADO (`TheLedgerOfCharges.final_step_named_by_the_payment`). -/
theorem the_proposal_beside_is_kept :
    TGLExt.TheLedgerOfCharges.finalStepNameProposed =
      "TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS" :=
  TGLExt.TheLedgerOfCharges.final_step_named_by_the_payment

/-! ### 7. Os itens centrais num só termo -/

/-- ★★★ O AXIOMA E A TESTEMUNHA FALSA: os dois pontos fixos da leitura; o posto estacionado, o gradiente e a leitura no
    lock mínimo; o posto é o zero modular; o 1 é o Axioma; o 0 é a testemunha falsa; o nome do degrau final. -/
theorem the_axiom_and_the_false_witness {L : LightOneParticle} (C : FockCertificate L) {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    (∀ x : ℝ, 0 ≤ x → (Real.sqrt x = x ↔ x = 0 ∨ x = 1))
    ∧ (∀ t : ℝ, axiomFlow (PFmic C) t * PFmic C = PFmic C)
    ∧ (∀ t : ℝ, axiomFlow (PFmic C) t * (1 - PFmic C) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - PFmic C))
    ∧ Tendsto (axiomFlow (PFmic C)) atTop (𝓝 (PFmic C))
    ∧ (∀ ψ : C.F, (∀ t : ℝ, axiomFlow (PFmic C) t ψ = ψ) ↔ ∀ t : ℝ, lightDelta C t ψ = ψ)
    ∧ (Real.sqrt 1 = 1 ∧ (∫ κ : ℝ, phi0sq κ) = 1 ∧ dimOrTop ℂ firstAtom = 1)
    ∧ (Real.sqrt 0 = 0 ∧ ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x))
    ∧ finalStepNameAxioma =
      "AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER_RETURNS_AS_THE_FIXED_POINT_OF_THE_READING__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS" := by
  have hP : IsIdempotentElem (PFmic C) := (ℂ ∙ C.Ω).isIdempotentElem_starProjection
  exact ⟨fun x hx => the_reading_has_two_fixed_points hx,
    fun t => (axiomFlow_fixes_the_post hP t).1,
    fun t => axiomFlow_gradient hP t,
    axiomFlow_tendsto_the_post (PFmic C),
    fun ψ => the_post_is_the_modular_zero C ψ,
    the_one_is_the_axiom,
    ⟨Real.sqrt_zero, beta_forbids_full_static_witness hβ hg⟩,
    final_step_named_axioma⟩

end TGLExt.TheAxiomAndTheFalseWitness
