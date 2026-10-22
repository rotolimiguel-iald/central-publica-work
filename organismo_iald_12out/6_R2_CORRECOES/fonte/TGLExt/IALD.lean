import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheKeyIsTheReader
import TGLExt.PhysicsIsTheReading
import TGLExt.TheIALDSelector
import TGLExt.IALDRhoStar
import TGLExt.ExactWitness
import TGLExt.FractalUnitarity
import TGLExt.TheCouplingRunsBoundedBelow
import TGLExt.TheGreatAttractor
import TGLExt.TheWeightIsNotTheRank
import TGLExt.Palavra
import TGLExt.TheSingularityReadsTheAttractorAdendo1
import TGLExt.TheUnitIsTheRank
import TGLExt.TheTimeIsNotAPost

set_option autoImplicit false

/-!
# TGLExt.IALD — o motor único (nome provisório; o nome é do operador) — RODADA 2 (13/10/2026), sandbox

R2 = a pedra r1 (`2_CONSTRUCAO\sandbox\TGLExt\IALD.lean`, sha256 `a267bc6d2aedf2fa…`) corrigida SÓ pelas oito
correções C1–C8 do relatório `4_RELATORIO\O_ORGANISMO_E_A_PROVA_DISTINTIVA.md` §5.2, que somam as duas auditorias
(`3_AUD_REPRO`, `3_AUD_ESTATUTO`). Nada está instalado. A tabela r1→r2 por declaração está em
`6_R2_CORRECOES\TABELA_R1_R2.md`. Toda declaração que já PASSAVA mantém o tipo, exceto `motor_idempotent_under_anchor`
(C2: perdeu a hipótese `‖a‖ = 1`, que era decorativa ali) e `anchor_is_necessary`, RENOMEADA para
`unitarity_is_not_enough` (C1: mesmo tipo; o nome antigo dizia mais do que o termo prova).

Pinos (C7) — as candidatas vigentes da v392, compiladas na sobreposição do sandbox, NÃO instaladas:
PALAVRA `33184b49a8bba7e7`; F1.ATRATOR ADENDO1 `433d13c223b03971`; F1.FREQUENCIA `TheUnitIsTheRank` r3
`e95775d61db38633`; F1.TEMPO R2 `TheTimeIsNotAPost` `4d8a82591badd010`.

A pedra LIGA por termo peças que já existem; não redeclara nenhuma.
  Inscrição (post a; posto 1) → Transporte U → Defasagem D_r(t) = axiomFlow (post a) (r·t) → Leitura (post a)
  → Memória M[ψ] = ⟪ψ, Π ψ⟫ → Identidade (M = 1 ⟺ Πψ = ψ) → laço (a leitura re-inscreve o posto).

O QUE A PEDRA NÃO EXIGE E NÃO DIZ (correções):
* C1 — A pedra NÃO exige U unitário: `U : H →L[ℂ] H` é qualquer operador contínuo. A âncora `U a = a` é SUFICIENTE
  (T2), não necessária (`anchor_not_necessary`). A condição exata da idempotência é a âncora fraca
  `post a (U a) = a` OU o motor nulo (`motor_idempotent_iff_weak_anchor_or_null`); fora do motor nulo, é exatamente a
  âncora fraca (`motor_idempotent_iff_weak_anchor`); o motor nulo tem peso (`null_transport_is_idempotent_without_weak_anchor`).
  Se U deve ser unitário por tipo é pergunta do operador; esta pedra não decide.
* C3 — A Fundação NÃO é importada diretamente: a r1 só usava `Fundacao.the_floor_fixes_the_cut`, invólucro de
  `Real.exp_eq_one_iff`; T7′ cita agora a injetividade da exponencial real. A cláusula Ágape NÃO entra por termo
  (`agape`, `abismo`, `DualScalingData`: 0 usos aqui) e a Q15 NÃO está resolvida. O arquivo `TGLExt.Fundacao` continua
  no fecho de importação só de forma transitiva, porque `TheTimeIsNotAPost` o importa; nenhum termo dele é usado aqui.
  Construir o `DualScalingData` do motor é pergunta do operador; esta pedra não o constrói.
* C4 — Há quatro objetos chamados defasagem/pinching ao redor desta pedra, e só o primeiro é a defasagem do motor:
  (1) `IALD.dephase a r t = axiomFlow (post a) (r·t)`, operador sobre vetores de H, invertível em todo (r, t)
      (`the_motor_dephasing_is_invertible`): leva vetor a vetor, logo estado puro a estado puro;
  (2) `TGLExt.diagExpect` (`CondExpect.lean:87`), a esperança diagonal (pinching) de matrizes, usada em B8(iii);
  (3) `TGLExt.IALDRhoStar.eJ`, o pinching de M₂ do T12 — o MESMO que (2) em M₂ (`the_jones_pinching_is_diagExpect`, rfl);
  (4) `TGLExt.dephase` (`Ergodicity.lean:184`), o amortecimento de Schur das entradas; não aparece nesta pedra.
  Nenhum lema desta pedra liga (1) a (2), (3) ou (4). B8(iii) e T12 NÃO são a defasagem do motor.
* C6 — A SAÍDA DO MOTOR NÃO DEPENDE DE β NEM DE t (T1; `the_motor_ignores_rate_and_time`). `the_leak_is_beta` é um `rfl`
  de NOME; a defasagem vale para QUALQUER taxa real (`the_leak_is_any_rate`). β só vive na face D, antes da leitura.
  Esta pedra é VALIDADE (fecho lógico na face do posto), não prova distintiva: nenhum observável dela discrimina a natureza.
* C5 — As leituras ontológicas nas docstrings vão marcadas [ONTO] (EU SOU = IALD, santo, Zenão, a singularidade);
  o termo é sempre o enunciado Lean. T5′ é um fato geral de espaço de Hilbert.
* C8 — As pontes P1–P3 são `rfl`: desfazem um homônimo aparente (três nomes da MESMA forma `(ℂ ∙ v).starProjection`);
  unem a forma, não o referente (`post_is_not_constant`). Não suprem um lema que faltasse. O organismo segue sendo uma
  lista auditada fora desta pedra (0 referências aqui a `QGSolutionComplete`, Tetelestai, `the_whole_is_one`,
  `the_matrix_rule`, ao livro de cobranças, a `agape` e a `DualScalingData`).

Régua: cada teorema é [REAL] se fechar aqui sem lacuna de prova contra o kernel v391 do Nós (só leitura). PROVADA = validade;
a confirmação recusada é creditação; o único elo pendente da QG é β_TGL na natureza a 5σ; o gate não se move aqui;
β nunca literal (na pedra a taxa é `r`, ou `c.beta` com `c : TGLCoupling`; o número só em runtime, α·√e).
Regra dos dois regimes: a FACE é o objeto (hiperbólico; `axiomFlow`, tem limite); o ÂNGULO é a leitura (compacto;
`projPlus`, `angFamily` da PALAVRA, só lê). Nenhuma equação desta pedra iguala um objeto de um regime a um do outro.
-/

namespace TGLExt.IALD

open TGLExt TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness Filter Topology
open TGLExt.ImportedSQ TGL.SpecificAQFT TGL.ModularRealization
open scoped InnerProductSpace

noncomputable section

/-! ## 0. As pontes `rfl` — os nomes do projetor do Nome são UMA forma (homônimo aparente, não lema ausente) -/

/-- ★ PONTE 1: a IALD de ℓ² (v180) tem a forma do posto da primeira inscrição. `rfl` une a FORMA, não o referente. -/
theorem ialdSelector_eq_post : TGLExt.ialdSelector = post TGLExt.firstInscription := rfl

/-- ★ PONTE 2: o Nome da luz |Ω⟩⟨Ω| = P_{ker K} (`PFmic`) tem a forma do posto do vácuo (no espaço de Fock; `rfl`). -/
theorem PFmic_eq_post {L : LightOneParticle} (C : FockCertificate L) :
    TGLExt.QGReaderUVLock.PFmic C = post C.Ω := rfl

/-- ★ PONTE 3: o leitor do vácuo ω(x) = ⟪Ω, xΩ⟫ É a leitura do estado Ω (`rfl`). -/
theorem reader_eq_reading {L : LightOneParticle} (C : FockCertificate L) (x : C.F →L[ℂ] C.F) :
    TGLExt.TheKeyIsTheReader.reader C x = reading x C.Ω := rfl

/-- ★ a primeira inscrição é unitária (a hipótese `‖a‖ = 1` é HABITADA em ℓ²). -/
theorem firstInscription_norm : ‖TGLExt.firstInscription‖ = 1 :=
  TGLExt.inscriptions_orthonormal.1 0

/-! ## 1. O motor -/

section Motor
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A DEFASAGEM DO MOTOR com taxa r: D_r(t) = axiomFlow (post a) (r·t) = post a + e^{−rt}(1 − post a).
    Objeto (1) do cabeçalho: operador sobre vetores; NÃO é `diagExpect`, nem `IALDRhoStar.eJ`, nem `TGLExt.dephase`. -/
def dephase (a : H) (r t : ℝ) : H →L[ℂ] H := axiomFlow (post a) (r * t)

/-- A MEMÓRIA: M[ψ] = ⟪ψ, Π ψ⟫ = Tr(|ψ⟩⟨ψ| Π) — a lei do Atlas §VIII.1 na face pura. -/
def memory (P : H →L[ℂ] H) (ψ : H) : ℂ := reading P ψ

/-- O MOTOR: Inscrição → Transporte U → Defasagem → Leitura. -/
def motor (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) : H := post a (IALD.dephase a r t (U ψ))

/-- ★★ T1 — A LEITURA ABSORVE A DEFASAGEM: motor a U r t ψ = post a (U ψ) (`P · F(t) = P`, v385).
    A SAÍDA DO MOTOR NÃO DEPENDE DA TAXA r (β só por nome) NEM DO TEMPO t: β atua só na face D, antes da leitura,
    e nenhum observável do motor depende de β (C6). -/
theorem the_reading_absorbs_the_dephasing (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) :
    motor a U r t ψ = post a (U ψ) := by
  unfold motor IALD.dephase
  have h := (axiomFlow_fixes_the_post (post_isIdempotent a) (r * t)).2
  rw [← ContinuousLinearMap.mul_apply, h]

/-- ★★ C6 — O MOTOR IGNORA A TAXA E O TEMPO: para quaisquer (r, t) e (r′, t′), a saída é a mesma.
    É a forma explícita de que esta pedra é validade, não prova distintiva. -/
theorem the_motor_ignores_rate_and_time (a : H) (U : H →L[ℂ] H) (r t r' t' : ℝ) (ψ : H) :
    motor a U r t ψ = motor a U r' t' ψ := by
  rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing]

/-- ★★ T3 — O MOTOR POUSA NO NOME: a imagem do motor está na reta ℂ∙a. -/
theorem motor_lands_in_the_name (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) :
    motor a U r t ψ ∈ (ℂ ∙ a) := by
  rw [the_reading_absorbs_the_dephasing]
  exact (ℂ ∙ a).starProjection_apply_mem _

/-- ★★★ C1 — A ÂNCORA FRACA BASTA: se `post a (U a) = a`, o motor é idempotente (U qualquer, a qualquer, sem norma).
    Reaproveitada da sonda C1 do auditor de reprodução (`AuditorRepro.motor_idempotent_under_weak_anchor`). -/
theorem motor_idempotent_under_weak_anchor (a : H) (U : H →L[ℂ] H) (hU : post a (U a) = a)
    (r t : ℝ) (ψ : H) :
    motor a U r t (motor a U r t ψ) = motor a U r t ψ := by
  rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing]
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp ((ℂ ∙ a).starProjection_apply_mem (U ψ))
  change post a (U ((ℂ ∙ a).starProjection (U ψ))) = (ℂ ∙ a).starProjection (U ψ)
  rw [← hc, map_smul, map_smul, hU]

/-- ★★★ T2 — O MOTOR É IDEMPOTENTE NA SUA IMAGEM sob a hipótese NOMEADA `Anchor : U a = a`
    (a invariância do vácuo `Γ_vac` do certificado de Fock; `anchoring_preserves`, v386).
    R2 (C2): sem a hipótese `‖a‖ = 1`, que era decorativa aqui (a âncora forte implica a fraca para todo a). -/
theorem motor_idempotent_under_anchor (a : H) (U : H →L[ℂ] H) (hU : U a = a)
    (r t : ℝ) (ψ : H) :
    motor a U r t (motor a U r t ψ) = motor a U r t ψ :=
  motor_idempotent_under_weak_anchor a U (by rw [hU, post_fixes_the_action]) r t ψ

/-- ★★★ C1 — A CONDIÇÃO EXATA: o motor é idempotente em todo ψ ⟺ vale a âncora fraca `post a (U a) = a`
    OU o motor é nulo. Sem hipótese de norma nem de unitariedade. -/
theorem motor_idempotent_iff_weak_anchor_or_null (a : H) (U : H →L[ℂ] H) (r t : ℝ) :
    (∀ ψ, motor a U r t (motor a U r t ψ) = motor a U r t ψ) ↔
      (post a (U a) = a ∨ ∀ ψ, motor a U r t ψ = 0) := by
  constructor
  · intro hid
    by_cases hnull : ∀ ψ, motor a U r t ψ = 0
    · exact Or.inr hnull
    · left
      obtain ⟨ψ, hψ⟩ := not_forall.mp hnull
      obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp (motor_lands_in_the_name a U r t ψ)
      have hc0 : c ≠ 0 := by
        rintro rfl
        apply hψ
        rw [← hc, zero_smul]
      have h := hid ψ
      rw [← hc, the_reading_absorbs_the_dephasing, map_smul, map_smul] at h
      exact smul_right_injective H hc0 h
  · rintro (hU | hnull) ψ
    · exact motor_idempotent_under_weak_anchor a U hU r t ψ
    · rw [hnull ψ]
      exact hnull 0

/-- ★★ C1 — FORA DO MOTOR NULO, A ÂNCORA FRACA É EXATA: se algum ψ tem saída não nula, idempotência ⟺ `post a (U a) = a`. -/
theorem motor_idempotent_iff_weak_anchor (a : H) (U : H →L[ℂ] H) (r t : ℝ)
    (h : ∃ ψ, motor a U r t ψ ≠ 0) :
    (∀ ψ, motor a U r t (motor a U r t ψ) = motor a U r t ψ) ↔ post a (U a) = a := by
  rw [motor_idempotent_iff_weak_anchor_or_null]
  constructor
  · rintro (hU | hnull)
    · exact hU
    · obtain ⟨ψ, hψ⟩ := h
      exact absurd (hnull ψ) hψ
  · intro hU
    exact Or.inl hU

/-- ★ C1 — O MOTOR NULO TEM PESO: com U = 0 e a ≠ 0 a âncora fraca falha e, ainda assim, o motor é idempotente
    (é o disjunto nulo da condição exata). -/
theorem null_transport_is_idempotent_without_weak_anchor (a : H) (ha : a ≠ 0) (r t : ℝ) :
    post a ((0 : H →L[ℂ] H) a) ≠ a ∧
      ∀ ψ, motor a 0 r t (motor a 0 r t ψ) = motor a 0 r t ψ := by
  refine ⟨?_, ?_⟩
  · rw [ContinuousLinearMap.zero_apply, map_zero]
    exact fun h => ha h.symm
  · intro ψ
    rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing]
    simp

/-- ★★ C1 — A ÂNCORA NÃO É NECESSÁRIA: com ‖a‖ = 1, b ⊥ a e b ≠ 0, o transporte U = 1 + |b⟩⟨a| NÃO ancora
    (U a = a + b ≠ a) e o motor é idempotente. Reaproveitada da sonda A1 do auditor (`AuditorRepro.anchor_not_necessary`). -/
theorem anchor_not_necessary (a b : H) (ha : ‖a‖ = 1) (hab : ⟪a, b⟫_ℂ = 0) (hb : b ≠ 0) :
    let U : H →L[ℂ] H := 1 + (innerSL ℂ a).smulRight b
    U a ≠ a ∧ ∀ r t ψ, motor a U r t (motor a U r t ψ) = motor a U r t ψ := by
  intro U
  have haa : ⟪a, a⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, ha]; simp
  have hUa : U a = a + b := by
    simp only [U, ContinuousLinearMap.add_apply, ContinuousLinearMap.one_apply,
      ContinuousLinearMap.smulRight_apply, innerSL_apply_apply, haa, one_smul]
  have hpb : post a b = 0 := by
    rw [post_apply ha, hab, zero_smul]
  refine ⟨?_, ?_⟩
  · rw [hUa]
    intro h
    exact hb (by simpa using h)
  · intro r t ψ
    apply motor_idempotent_under_weak_anchor
    rw [hUa, map_add, post_fixes_the_action, hpb, add_zero]

/-- ★★ T2′ — A UNITARIEDADE NÃO BASTA (negativo honesto; r1: `anchor_is_necessary`, renomeada em C1 — mesmo tipo):
    a fase global U = i·1 é unitária e quebra a idempotência: motor(motor a) = −a ≠ i·a = motor a.
    Prova só isto; NÃO prova que a âncora é necessária (ver `anchor_not_necessary`). -/
theorem unitarity_is_not_enough (a : H) (ha : ‖a‖ = 1) :
    motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 (motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a)
      ≠ motor a (Complex.I • (1 : H →L[ℂ] H)) 0 0 a := by
  have ha0 : a ≠ 0 := by
    intro h
    rw [h, norm_zero] at ha
    exact zero_ne_one ha
  rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing]
  simp only [ContinuousLinearMap.smul_apply, ContinuousLinearMap.one_apply, map_smul,
    post_fixes_the_action, smul_smul, Complex.I_mul_I]
  intro h
  have h2 : ((-1 : ℂ) - Complex.I) • a = 0 := by rw [sub_smul, h, sub_self]
  rcases smul_eq_zero.mp h2 with hc | hc
  · have := congrArg Complex.im hc
    simp at this
  · exact ha0 hc

/-- ★ a fase global É unitária: star(i·1)·(i·1) = 1 — logo a âncora não é consequência da unitariedade. -/
theorem phase_is_unitary :
    star (Complex.I • (1 : H →L[ℂ] H)) * (Complex.I • (1 : H →L[ℂ] H)) = 1 := by
  rw [star_smul, star_one, smul_mul_smul_comm, one_mul, Complex.star_def, Complex.conj_I,
    neg_mul, Complex.I_mul_I, neg_neg, one_smul]

omit [CompleteSpace H] in
/-- ★★ T3′ — O NOME TEM POSTO 1 (Tr Π = 1 = ω(I)): a imagem do posto é a reta, de dimensão 1
    (`iald_has_rank_one` em ℓ², `Pb_is_rank_one` em ℂ², aqui em todo H). POSTO = RANK no átomo. -/
theorem the_name_has_rank_one (a : H) (ha : a ≠ 0) :
    (post a).range = (ℂ ∙ a) ∧ Module.finrank ℂ (ℂ ∙ a) = 1 :=
  ⟨Submodule.range_starProjection _, finrank_span_singleton ha⟩

/-- ★★ T4 — O MOTOR LÊ O UM NO NOME: M[a] = 1 (`reader_reads_the_name_one` na luz). A hipótese ‖a‖ = 1 tem peso aqui. -/
theorem the_name_reads_one (a : H) (ha : ‖a‖ = 1) : memory (post a) a = 1 := by
  unfold memory reading
  rw [post_fixes_the_action, inner_self_eq_norm_sq_to_K, ha]
  simp

/-- ★ a memória é o peso de Born (`reading_post_is_born`, v386): M[ψ] = |⟪a, ψ⟫|². -/
theorem memory_is_born (a : H) (ha : ‖a‖ = 1) (ψ : H) :
    memory (post a) ψ = ((‖⟪a, ψ⟫_ℂ‖ ^ 2 : ℝ) : ℂ) :=
  reading_post_is_born ha ψ

/-- ★★★ T5 — para ψ unitário, M[ψ] = 1 ⟺ Π ψ = ψ (Pitágoras: ‖ψ‖² = ‖Πψ‖² + ‖ψ − Πψ‖²; é
    `reader_reads_one_iff_fixes_the_vacuum` transposta ao estado). [ONTO] a leitura EU SOU = IALD; 1 = 1. -/
theorem memory_one_iff_identity (a : H) (ψ : H) (hψ : ‖ψ‖ = 1) :
    memory (post a) ψ = 1 ↔ post a ψ = ψ := by
  unfold memory
  change reading (ℂ ∙ a).starProjection ψ = 1 ↔ (ℂ ∙ a).starProjection ψ = ψ
  rw [reading_eq_norm_sq (ℂ ∙ a) ψ]
  constructor
  · intro h
    have h1 : ‖(ℂ ∙ a).starProjection ψ‖ = 1 := by
      have h' : ((‖(ℂ ∙ a).starProjection ψ‖ : ℝ) : ℂ) ^ 2 = ((1 : ℝ) : ℂ) ^ 2 := by simpa using h
      have h'' : ‖(ℂ ∙ a).starProjection ψ‖ ^ 2 = (1 : ℝ) ^ 2 := by exact_mod_cast h'
      nlinarith [norm_nonneg ((ℂ ∙ a).starProjection ψ),
        sq_nonneg (‖(ℂ ∙ a).starProjection ψ‖ - 1), sq_nonneg (‖(ℂ ∙ a).starProjection ψ‖ + 1)]
    have hpyth := Submodule.norm_sq_eq_add_norm_sq_starProjection ψ (ℂ ∙ a)
    rw [hψ, h1] at hpyth
    have h0 : ‖(ℂ ∙ a)ᗮ.starProjection ψ‖ ^ 2 = 0 := by nlinarith
    have hz : (ℂ ∙ a)ᗮ.starProjection ψ = 0 := by
      rw [sq_eq_zero_iff, norm_eq_zero] at h0
      exact h0
    have hsum := Submodule.starProjection_add_starProjection_orthogonal (K := ℂ ∙ a) ψ
    rw [hz, add_zero] at hsum
    exact hsum
  · intro h
    rw [h, hψ]
    simp

/-- ★★ T5′ — para ψ unitário, M[ψ] = 1 ⟺ post ψ = post a: FATO GERAL DE ESPAÇO DE HILBERT (dois vetores unitários
    com |⟪a, ψ⟫| = 1 geram a mesma reta, logo o mesmo projetor; o estado puro |ψ⟩⟨ψ| coincide com Π_N).
    [ONTO] a leitura EU SOU = IALD e o eco que não é cópia; o termo é só a igualdade dos projetores. -/
theorem memory_one_iff_same_post (a : H) (ψ : H) (hψ : ‖ψ‖ = 1) :
    memory (post a) ψ = 1 ↔ post ψ = post a := by
  rw [memory_one_iff_identity a ψ hψ]
  constructor
  · intro h
    have hmem : ψ ∈ (ℂ ∙ a) := (ℂ ∙ a).starProjection_eq_self_iff.mp h
    obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.mp hmem
    have hc : c ≠ 0 := by
      rintro rfl
      simp at hψ
    unfold post
    congr 1
    exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr hc) a
  · intro h
    have : post ψ ψ = ψ := post_fixes_the_action ψ
    rw [h] at this
    exact this

/-- ★★ T6 — RELER NÃO ACRESCENTA (lei 9, E² = E): M[Πψ] = M[ψ] — a idempotência da memória
    (`observing_adds_nothing`, `jonesReading_idem`, `iald_is_idempotent`, em UMA face). -/
theorem rereading_adds_nothing (a : H) (ψ : H) :
    memory (post a) (post a ψ) = memory (post a) ψ := by
  unfold memory
  change reading (ℂ ∙ a).starProjection ((ℂ ∙ a).starProjection ψ) = reading (ℂ ∙ a).starProjection ψ
  rw [reading_eq_norm_sq (ℂ ∙ a), reading_eq_norm_sq (ℂ ∙ a)]
  have hPP : (ℂ ∙ a).starProjection ((ℂ ∙ a).starProjection ψ) = (ℂ ∙ a).starProjection ψ :=
    (ℂ ∙ a).starProjection_eq_self_iff.mpr ((ℂ ∙ a).starProjection_apply_mem ψ)
  show ((‖(ℂ ∙ a).starProjection ((ℂ ∙ a).starProjection ψ)‖ : ℝ) : ℂ) ^ 2 = _
  rw [hPP]

/-- ★★★ T6′ — O LAÇO: A LEITURA RE-INSCREVE O POSTO. Se o estado tem memória não nula do Nome,
    o posto do objeto lido É o Nome: post (Π ψ) = post a. [ONTO] a cunhagem do operador de 07/10 sobre a leitura
    que cria o objeto (a PALAVRA); o termo é só a igualdade dos projetores. -/
theorem the_reading_reinscribes_the_post (a : H) (ha : ‖a‖ = 1) (ψ : H) (h : ⟪a, ψ⟫_ℂ ≠ 0) :
    post (post a ψ) = post a := by
  rw [post_apply ha]
  unfold post
  congr 1
  exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr h) a

omit [CompleteSpace H] in
/-- ★★ T7 — SEM VAZAMENTO NÃO HÁ SEGUNDA FACE: com taxa r = 0 a defasagem é a identidade.
    Trivial por construção; o conteúdo é o NOME da taxa. -/
theorem no_leak_no_second_face (a : H) (t : ℝ) : IALD.dephase a 0 t = 1 := by
  unfold IALD.dephase
  rw [zero_mul, axiomFlow_zero]

omit [CompleteSpace H] in
/-- ★ a taxa como β: `dephase a c.beta` para c : TGLCoupling. É um `rfl` DE NOME (C6): instancia a taxa r com
    `c.beta`; nada nesta pedra depende de r ser β (`the_leak_is_any_rate`). O número só em runtime, α·√e. -/
theorem the_leak_is_beta (c : TGLCoupling) (a : H) (t : ℝ) :
    IALD.dephase a c.beta t = axiomFlow (post a) (c.beta * t) := rfl

omit [CompleteSpace H] in
/-- ★ C6 — A DEFASAGEM VALE PARA QUALQUER TAXA REAL (reaproveitada da sonda C2 do auditor): β entra só como nome. -/
theorem the_leak_is_any_rate (a : H) (r t : ℝ) :
    IALD.dephase a r t = axiomFlow (post a) (r * t) := rfl

/-- ★★ C4 — A DEFASAGEM DO MOTOR É INVERTÍVEL em todo (r, t), com inverso D_r(−t) (via `TheTimeIsNotAPost.flow_isUnit`):
    leva vetor a vetor, logo não apaga posto de estado puro. É o que a separa do pinching de B8(iii)/T12. -/
theorem the_motor_dephasing_is_invertible (a : H) (r t : ℝ) : IsUnit (IALD.dephase a r t) :=
  TGLExt.TheTimeIsNotAPost.flow_isUnit (post_isIdempotent a) (r * t)

end Motor

/-! ## 2. A álgebra do fluxo — o tempo finito, o Verbo sem posto, a segunda face -/

section Flow
variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★★ T7′ — A SEGUNDA FACE APARECE SSE HÁ VAZAMENTO: F(s)·(1 − P) = 1 − P ⟺ s = 0.
    R2 (C3): pela injetividade da exponencial real (`Real.exp_eq_one_iff`, Mathlib), sem a Fundação.
    A cláusula Ágape NÃO entra nesta pedra. -/
theorem second_face_iff_leak {P : A} (hP : IsIdempotentElem P) (hne : (1 : A) - P ≠ 0) (s : ℝ) :
    axiomFlow P s * (1 - P) = 1 - P ↔ s = 0 := by
  rw [axiomFlow_gradient hP]
  constructor
  · intro h
    have h2 : (((Real.exp (-s) : ℝ) : ℂ) - 1) • ((1 : A) - P) = 0 := by
      rw [sub_smul, one_smul, h, sub_self]
    rcases smul_eq_zero.mp h2 with hc | hc
    · have hc' : ((Real.exp (-s) : ℝ) : ℂ) = 1 := sub_eq_zero.mp hc
      have hr : Real.exp (-s) = 1 := by exact_mod_cast hc'
      rw [Real.exp_eq_one_iff] at hr
      linarith
    · exact absurd hc hne
  · rintro rfl
    simp

/-- ★★ T8 — o fluxo NUNCA chega ao posto em tempo finito (e^{−t} ≠ 0) — `absolute_zero_unreachable_in_finite_time`
    na face do idempotente. [ONTO] a leitura como Zenão do motor; o termo é só e^{−t} ≠ 0. -/
theorem the_motor_never_arrives {P : A} (hne : (1 : A) - P ≠ 0) (t : ℝ) : axiomFlow P t ≠ P := by
  intro h
  have h2 : ((Real.exp (-t) : ℝ) : ℂ) • ((1 : A) - P) = 0 := by
    have := congrArg (fun y => y - P) h
    simpa [axiomFlow] using this
  rcases smul_eq_zero.mp h2 with hc | hc
  · have : Real.exp (-t) = 0 := by exact_mod_cast hc
    exact Real.exp_ne_zero _ this
  · exact hne hc

/-- ★★ T8′ — O RELÓGIO DAS METADES: o fluxo amostrado em t = n·log 2 é F(n log 2) = P + (½)ⁿ(1 − P).
    [ONTO] a leitura como a dicotomia de Zenão (`zeno_partial_sum`, v388). -/
theorem the_halving_clock (P : A) (n : ℕ) :
    axiomFlow P (n * Real.log 2) = P + (((1 / 2 : ℝ) ^ n : ℝ) : ℂ) • ((1 : A) - P) := by
  unfold axiomFlow
  congr 2
  rw [Real.exp_neg, Real.exp_nat_mul, Real.exp_log two_pos, one_div, inv_pow]

/-- ★★ T8″ — ... = 1 − (Σ_{k<n} (½)^{k+1})·(1 − P): a soma parcial (`zeno_partial_sum`) é o peso já defasado. -/
theorem the_halving_clock_pays_the_zeno_sum (P : A) (n : ℕ) :
    axiomFlow P (n * Real.log 2)
      = 1 - (((∑ k ∈ Finset.range n, (1 / 2 : ℝ) ^ (k + 1)) : ℝ) : ℂ) • ((1 : A) - P) := by
  rw [the_halving_clock, TGLExt.TheCouplingRunsBoundedBelow.zeno_partial_sum]
  push_cast
  rw [sub_smul, one_smul]
  abel

/-- ★★ T9 — O VERBO NÃO É UM POSTO (F1.TEMPO, T9): para 0 < t o fluxo não é idempotente —
    F(t)² = F(2t) ≠ F(t) quando 1 − P ≠ 0. [ONTO] o tempo que o operador nomeia «santo» (12/10) entra aqui só como
    sem posto; o termo não diz o que o tempo é. -/
theorem the_verb_is_not_a_post {P : A} (hP : IsIdempotentElem P) (hne : (1 : A) - P ≠ 0)
    {t : ℝ} (ht : 0 < t) : ¬ IsIdempotentElem (axiomFlow P t) := by
  intro hid
  have h2 : axiomFlow P (t + t) = axiomFlow P t := by
    rw [axiomFlow_add hP]
    exact hid.eq
  unfold axiomFlow at h2
  have h3 : ((((Real.exp (-(t + t)) : ℝ) : ℂ) - ((Real.exp (-t) : ℝ) : ℂ))) • ((1 : A) - P) = 0 := by
    rw [sub_smul]
    have := congrArg (fun y => y - P) h2
    simp only [add_sub_cancel_left] at this
    rw [this, sub_self]
  rcases smul_eq_zero.mp h3 with hc | hc
  · have hc' : Real.exp (-(t + t)) = Real.exp (-t) := by exact_mod_cast sub_eq_zero.mp hc
    have := Real.exp_injective hc'
    linarith
  · exact hne hc

/-- ★ a convergência: F(t) → P (`axiomFlow_tendsto_the_post`, v385) — o limite É o posto
    (`zeno_tends_to_the_one`): re-exportação por termo, para que T8 e o limite morem na mesma pedra. -/
theorem the_motor_tends_to_the_post {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Tendsto (axiomFlow P) atTop (𝓝 P) :=
  axiomFlow_tendsto_the_post P

end Flow

/-! ## 3. A letra, a seção e o quarto nome -/

section Letter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- ★★★ T10 — A LETRA DO MOTOR: para T = 1 − Π (auto-adjunto, idempotente), a palavra aniquiladora é
    X·(X − 1), a letra q = X − 1 (real, q(0) = −1 ≠ 0), e a palavra normalizada q(T)/q(0) = 1 − T = Π:
    o Nome É a letra normalizada (`exact_witness_of_annihilating_word`, v88). -/
theorem the_letter_of_the_motor (a : H) :
    ((1 : H →L[ℂ] H) - post a).ker.starProjection = post a := by
  set T : H →L[ℂ] H := 1 - post a with hT
  have hsa : ContinuousLinearMap.adjoint T = T := by
    rw [← ContinuousLinearMap.star_eq_adjoint]
    exact ((IsSelfAdjoint.one (R := H →L[ℂ] H)).sub (post_isSelfAdjoint a)).star_eq
  have hidem : T * T = T := by
    have hP := (post_isIdempotent a).eq
    rw [hT, sub_mul, mul_sub, mul_sub, one_mul, one_mul, mul_one, hP]
    abel
  have hann : Polynomial.aeval T (Polynomial.X * (Polynomial.X - 1 : Polynomial ℂ)) = 0 := by
    simp only [map_mul, map_sub, Polynomial.aeval_X, map_one]
    rw [mul_sub, mul_one, hidem, sub_self]
  have hc : (Polynomial.X - 1 : Polynomial ℂ).coeff 0 ≠ 0 := by
    simp [Polynomial.coeff_X_zero, Polynomial.coeff_one_zero]
  have hq : ∀ n, starRingEnd ℂ ((Polynomial.X - 1 : Polynomial ℂ).coeff n)
      = (Polynomial.X - 1 : Polynomial ℂ).coeff n := by
    intro n
    simp only [Polynomial.coeff_sub, Polynomial.coeff_X, Polynomial.coeff_one]
    split_ifs <;> simp
  have h := TGLExt.exact_witness_of_annihilating_word T hsa (Polynomial.X - 1) hann hc hq
  rw [h]
  simp only [map_sub, Polynomial.aeval_X, map_one, Polynomial.coeff_sub, Polynomial.coeff_X_zero,
    Polynomial.coeff_one_zero, hT, sub_sub_cancel_left]
  simp

/-- ★★ T11 — A SEÇÃO É O NÚMERO VEZES O NOME (lei 5 ↔ lei 1): Π·x·Π = ⟪a, x a⟫ • Π
    (`the_shadow_is_the_reader_weighted_by_the_reading` na luz; aqui em todo H) — `jonesReading (post a) x`. -/
theorem the_section_is_the_number_times_the_name (a : H) (ha : ‖a‖ = 1) (x : H →L[ℂ] H) :
    TGLExt.IALDJones.jonesReading (post a) x = ⟪a, x a⟫_ℂ • post a := by
  ext ψ
  simp only [TGLExt.IALDJones.jonesReading, ContinuousLinearMap.mul_apply,
    ContinuousLinearMap.smul_apply, post_apply ha, map_smul, smul_smul, mul_comm]

/-- ★ a seção relida é a seção (`jonesReading_idem`): re-exportação na face do posto. -/
theorem the_section_rereads_itself (a : H) (x : H →L[ℂ] H) :
    TGLExt.IALDJones.jonesReading (post a) (TGLExt.IALDJones.jonesReading (post a) x)
      = TGLExt.IALDJones.jonesReading (post a) x :=
  TGLExt.IALDJones.jonesReading_idem (post_isIdempotent a).eq x

end Letter

/-- ★★ T12 — NEGATIVO HONESTO: o pinching diagonal da face finita `TGLExt.IALDRhoStar.eJ` (M₂ → M₂; objeto (3) do
    cabeçalho) fixa DUAS unidades matriciais ortogonais (E₀₀ e E₁₁): é a SEÇÃO (lei 5), não o Nome de posto 1.
    O quarto nome de Π_N não é um nome de Π_N. NÃO É A DEFASAGEM DO MOTOR (`IALD.dephase`, objeto (1)). -/
theorem the_jones_pinching_is_not_the_name :
    TGLExt.IALDRhoStar.eJ (Matrix.of fun a b => if a = (0 : Fin 2) ∧ b = (0 : Fin 2) then (1 : ℂ) else 0)
      = (Matrix.of fun a b => if a = (0 : Fin 2) ∧ b = (0 : Fin 2) then (1 : ℂ) else 0) ∧
    TGLExt.IALDRhoStar.eJ (Matrix.of fun a b => if a = (1 : Fin 2) ∧ b = (1 : Fin 2) then (1 : ℂ) else 0)
      = (Matrix.of fun a b => if a = (1 : Fin 2) ∧ b = (1 : Fin 2) then (1 : ℂ) else 0) := by
  constructor
  · have := TGLExt.IALDRhoStar.eJ_on_units 0 0
    simpa using this
  · have := TGLExt.IALDRhoStar.eJ_on_units 1 1
    simpa using this

/-- ★★ C4 — PONTE VERDADEIRA E CURTA ENTRE DOIS HOMÔNIMOS: o pinching `eJ` do T12 e a esperança diagonal `diagExpect`
    do B8(iii) são o MESMO pinching em M₂ (`rfl`). Ambos ficam fora da defasagem do motor. -/
theorem the_jones_pinching_is_diagExpect (ξ : TGLExt.IALDRhoStar.V) :
    TGLExt.IALDRhoStar.eJ ξ = diagExpect ξ := rfl

/-- ★ C4 — O PINCHING APAGA UMA COERÊNCIA: `diagExpect E₀₁ = 0` com E₀₁ ≠ 0 — não é injetivo, ao contrário da
    defasagem do motor (`the_motor_dephasing_is_invertible`). -/
theorem the_pinching_kills_a_coherence :
    diagExpect (Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ)) = 0 ∧
      Matrix.single (0 : Fin 2) (1 : Fin 2) (1 : ℂ) ≠ 0 := by
  refine ⟨?_, ?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [diagExpect]
  · intro h
    have := congrFun (congrFun h 0) 1
    simp at this

/-! ## 4. Sondas de vacuidade — habitantes concretos -/

/-- ★ SONDA 1 (ℓ², incondicional): o motor da IALD de ℓ² com a âncora trivial U = 1 é idempotente
    e lê o Um na primeira inscrição. -/
theorem probe_ellTwo :
    (∀ r t ψ, motor TGLExt.firstInscription 1 r t (motor TGLExt.firstInscription 1 r t ψ)
        = motor TGLExt.firstInscription 1 r t ψ) ∧
    memory TGLExt.ialdSelector TGLExt.firstInscription = 1 :=
  ⟨fun r t ψ => motor_idempotent_under_anchor _ 1 rfl r t ψ,
   by
    rw [ialdSelector_eq_post]
    exact the_name_reads_one _ firstInscription_norm⟩

/-- ★ SONDA 2 (a luz, condicional ao certificado C, sem habitante no kernel): o transporte Γ(u) da segunda
    quantização ANCORA (`Γ_vac`), logo o motor da luz é idempotente; e o leitor lê o Nome como 1. -/
theorem probe_the_light {L : LightOneParticle} (C : FockCertificate L) (u : H1 ≃ₗᵢ[ℂ] H1)
    (r t : ℝ) (ψ : C.F) :
    motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t
        (motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t ψ)
      = motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t ψ ∧
    memory (TGLExt.QGReaderUVLock.PFmic C) C.Ω = 1 :=
  ⟨motor_idempotent_under_anchor _ _ (by simpa using C.Γ_vac u) r t ψ,
   TGLExt.TheKeyIsTheReader.reader_reads_the_name_one C⟩

/-- ★ SONDA 3 (a taxa): o kernel prova 0 < c.beta < 1 para TODO c : TGLCoupling. Que o β de runtime habite
    `TGLCoupling` é fato de runtime (`couplingOfAlpha`), não termo desta pedra; o número nunca entra aqui. -/
theorem probe_the_rate (c : TGLCoupling) : 0 < c.beta ∧ c.beta < 1 := ⟨c.beta_pos, c.beta_lt_one⟩

/-! ## 5. PONTES POR TERMO às pedras candidatas da v392 (compiladas na sobreposição deste sandbox; NÃO instaladas)

Regra dos dois regimes: as pontes B1–B6 e B9–B11 ficam na FACE (o fluxo `axiomFlow`, hiperbólico, com limite);
B7 (PALAVRA) e B8 (F1.FREQUENCIA, face matricial) são CITAÇÕES POR TERMO em conjunção, nunca uma equação que
identifique o ângulo com a face ou a matriz com o operador de Hilbert. -/

section Candidatas
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

omit [CompleteSpace H] in
/-- ★★★ B1 — A DEFASAGEM DO MOTOR É A FAMÍLIA DO ATRATOR (F1.ATRATOR, ADENDO1): `dephase a r t = faceFamily a e^{−rt}`
    (`rfl`). Na face do posto o homônimo da Q9 do levantamento é aparente; `diagFlow` sobre ℝⁿ segue sem termo. -/
theorem dephase_eq_faceFamily (a : H) (r t : ℝ) :
    IALD.dephase a r t
      = TGLExt.TheSingularityReadsTheAttractor.faceFamily a (((Real.exp (-(r * t)) : ℝ) : ℂ)) := rfl

/-- ★★ B2 — COM VAZAMENTO (r·t > 0) A DEFASAGEM CONTRAI ESTRITAMENTE O COMPLEMENTO DO NOME
    (`StrictComplementContraction`, a hipótese A4 do atrator, aqui HABITADA pelo motor: c = e^{−rt} < 1). -/
theorem dephase_is_a_strict_complement_contraction (a : H) (ha : a ≠ 0) {r t : ℝ} (hrt : 0 < r * t) :
    TGLExt.TheSingularityReadsTheAttractor.StrictComplementContraction (IALD.dephase a r t) a := by
  rw [dephase_eq_faceFamily]
  apply TGLExt.TheSingularityReadsTheAttractor.faceFamily_hypothesis a ha
  rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  have h : Real.exp (-(r * t)) < Real.exp 0 := Real.exp_lt_exp.mpr (by linarith)
  simpa using h

/-- ★★★ B3 — dim Fix = 1: o espaço fixo da defasagem com vazamento É a reta do Nome, de dimensão 1
    (A4 do atrator aplicado ao motor; POSTO = RANK no ponto fixo). -/
theorem dephase_fixed_dimension_one (a : H) (ha : a ≠ 0) {r t : ℝ} (hrt : 0 < r * t) :
    Module.finrank ℂ (TGLExt.TheSingularityReadsTheAttractor.fixedSpace (IALD.dephase a r t)) = 1 :=
  TGLExt.TheSingularityReadsTheAttractor.A4_dimension_one _ _
    (dephase_is_a_strict_complement_contraction a ha hrt)

/-- ★★★ B4 — a leitura do atrator (`reading T` = projeção do espaço fixo, ADENDO1) aplicada à defasagem com
    vazamento É o posto `post a`: a leitura R do motor é a projeção do ponto fixo de D.
    [ONTO] «a singularidade é a leitura do atrator» (operador, 10/10, verbatim sha256 `1d9dd9a65fdacf68…`). -/
theorem the_singularity_reads_the_name (a : H) (ha : a ≠ 0) {r t : ℝ} (hrt : 0 < r * t) :
    TGLExt.TheSingularityReadsTheAttractor.reading (IALD.dephase a r t) = post a := by
  unfold TGLExt.TheSingularityReadsTheAttractor.reading post
  congr 1
  exact TGLExt.TheSingularityReadsTheAttractor.A4_fixedSpace_eq_span _ _
    (dephase_is_a_strict_complement_contraction a ha hrt)

/-- ★★ B5 — O MOTOR É A LEITURA DO ATRATOR APLICADA AO TRANSPORTE: motor a U r t ψ = reading (D_r(t)) (U ψ). -/
theorem motor_is_the_reading_of_the_attractor (a : H) (ha : a ≠ 0) (U : H →L[ℂ] H) {r t : ℝ}
    (hrt : 0 < r * t) (ψ : H) :
    motor a U r t ψ = TGLExt.TheSingularityReadsTheAttractor.reading (IALD.dephase a r t) (U ψ) := by
  rw [the_reading_absorbs_the_dephasing, the_singularity_reads_the_name a ha hrt]

/-- ★★ B6 — A ÓRBITA ITERADA: D_r(t)ⁿ ψ → post a ψ (A1 do atrator na face do motor): iterar a defasagem com
    vazamento converge ao Nome lido (não se pede limite ao ângulo). [ONTO] a leitura como Zenão. -/
theorem the_iterated_motor_tends_to_the_name (a : H) {r t : ℝ} (hrt : 0 < r * t) (ψ : H) :
    Tendsto (fun n : ℕ => (IALD.dephase a r t)^[n] ψ) atTop (𝓝 (post a ψ)) := by
  rw [dephase_eq_faceFamily]
  have hlam : ‖(((Real.exp (-(r * t)) : ℝ) : ℂ))‖ < 1 := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    have h : Real.exp (-(r * t)) < Real.exp 0 := Real.exp_lt_exp.mpr (by linarith)
    simpa using h
  exact TGLExt.TheSingularityReadsTheAttractor.A1_face_orbit a _ hlam ψ

/-- ★ B7 — RELER NÃO ACRESCENTA NOS DOIS REGIMES, em CONJUNÇÃO (não em equação): na FACE do motor (T6) e no
    ÂNGULO da PALAVRA (`Palavra.rereading_adds_nothing` = `observing_adds_nothing`). A PALAVRA lê o plano do
    boost; o motor lê o posto. São duas leituras; a pedra não as iguala (regra dos dois regimes). -/
theorem rereading_adds_nothing_in_both_regimes (a : H) :
    (∀ ψ : H, memory (post a) (post a ψ) = memory (post a) ψ) ∧
    (∀ θ : ℝ, TGLExt.projPlus * (TGLExt.projPlus * TGLExt.angFamily θ)
        = TGLExt.projPlus * TGLExt.angFamily θ) :=
  ⟨rereading_adds_nothing a, TGLExt.Palavra.rereading_adds_nothing⟩

end Candidatas

/-! B8 — POSTO = RANK NA FACE MATRICIAL (F1.FREQUENCIA, `TheUnitIsTheRank` r3 `e95775d61db38633`), por termo, em quatro
re-exportações: (i) Tr P = posto P para todo idempotente; (ii) a unidade ρ* tem traço 1 e posto 1; (iii) NEGATIVO
HONESTO: o PINCHING `diagExpect` sozinho não guarda o posto (D_∞F_θ(1) tem posto 2 em θ_M) — sobrevive o traço;
(iv) a LEITURA seletiva por posto 1 devolve o posto (Lüders [KNOWN]).
RÓTULO (C4): o `diagExpect` de B8(iii) (objeto (2) do cabeçalho; `CondExpect.lean:87`) NÃO É A DEFASAGEM DO MOTOR
(`IALD.dephase`, objeto (1), invertível). Nenhum lema desta pedra liga um ao outro; o nome inglês `dephasing` de B8(iii)
vem da F1.FREQUENCIA e designa o pinching. T3′ (o motor devolve posto 1) é provado na face de Hilbert sem B8. -/

/-- ★ B8(i) — o traço de um posto é o seu posto: Tr P = rank P (P² = P). -/
theorem the_trace_is_the_rank_of_a_post {n : Type} [Fintype n] [DecidableEq n] (P : Matrix n n ℂ)
    (hP : P * P = P) : P.trace = (P.rank : ℂ) :=
  TGLExt.TheUnitIsTheRank.trace_eq_rank_of_projection P hP

/-- ★ B8(ii) — a unidade ρ* da face finita: traço 1 e posto 1 (POSTO = RANK no átomo). -/
theorem the_unit_has_trace_one_and_rank_one :
    TGLExt.TheUnitIsTheRank.rhoStar.trace = 1 ∧ TGLExt.TheUnitIsTheRank.rhoStar.rank = 1 :=
  ⟨TGLExt.TheUnitIsTheRank.rhoStar_unit.1, TGLExt.TheUnitIsTheRank.rhoStar_unit.2.1⟩

/-- ★ B8(iii) — NEGATIVO HONESTO (F1.FREQUENCIA B5.e(ii)): o pinching `diagExpect` sozinho NÃO preserva o posto.
    NÃO É A DEFASAGEM DO MOTOR: aqui `diagExpect` (esperança diagonal de matrizes, `CondExpect.lean:87`) age sobre
    `rhoOut θ`; a defasagem do motor é `IALD.dephase` (invertível; `the_motor_dephasing_is_invertible`). -/
theorem dephasing_alone_does_not_keep_the_rank (c : TGLCoupling) :
    ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank :=
  TGLExt.TheUnitIsTheRank.rank_not_preserved_by_dephasing c

open Matrix in
/-- ★ B8(iv) — a leitura seletiva por posto 1 devolve o posto (Lüders [KNOWN]), na face matricial. -/
theorem the_reading_restores_the_post_in_the_matrix_face {n : Type} [Fintype n] [DecidableEq n]
    (a : n → ℂ) (X : Matrix n n ℂ) (h : star a ⬝ᵥ (X *ᵥ a) ≠ 0) :
    (star a ⬝ᵥ (X *ᵥ a))⁻¹ • (vecMulVec a (star a) * X * vecMulVec a (star a)) = vecMulVec a (star a) :=
  TGLExt.TheUnitIsTheRank.reading_returns_the_post a X h

section TempoSanto
variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★ B9 — O VERBO É POSTO SSE t = 0 (F1.TEMPO R2, `TheTimeIsNotAPost.flow_isIdempotentElem_iff`): a forma sse de T9. -/
theorem the_verb_is_a_post_iff {P : A} (hP : IsIdempotentElem P) (hne : (1 : A) - P ≠ 0) (t : ℝ) :
    IsIdempotentElem (axiomFlow P t) ↔ t = 0 :=
  TGLExt.TheTimeIsNotAPost.flow_isIdempotentElem_iff hP hne t

end TempoSanto

section TempoSantoHilbert
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- ★★★ B10 — O POSTO DO MOTOR É SÓ O LIMITE (F1.TEMPO R2 `the_time_is_not_a_post` na face do posto `post a`, sob H-C):
    o fluxo é idempotente sse t = 0, é invertível em todo t, o posto não é invertível, e F(t) → post a. -/
theorem the_motor_post_is_only_the_limit (a : H) (hne : (1 : H →L[ℂ] H) - post a ≠ 0) :
    (∀ t : ℝ, IsIdempotentElem (axiomFlow (post a) t) ↔ t = 0) ∧
    (∀ t : ℝ, IsUnit (axiomFlow (post a) t)) ∧
    ¬ IsUnit (post a) ∧
    Tendsto (axiomFlow (post a)) atTop (𝓝 (post a)) := by
  have hP1 : post a ≠ 1 := fun h1 => hne (by rw [h1, sub_self])
  have h := TGLExt.TheTimeIsNotAPost.the_time_is_not_a_post (post_isIdempotent a) hP1
  exact ⟨h.2.1, h.2.2.1, h.2.2.2.1, h.2.2.2.2⟩

end TempoSantoHilbert

/-- ★ B11 — O TEMPO DO MOTOR É PARÂMETRO, NÃO OPERADOR (F1.TEMPO R2, `no_time_matrix_fin`): em dimensão finita
    não há T com [T, H] = i·1. O t de `dephase` é um real. -/
theorem the_time_of_the_motor_is_a_parameter :
    ∀ (m : ℕ), 0 < m → ∀ T H : Matrix (Fin m) (Fin m) ℂ,
      T * H - H * T ≠ Complex.I • (1 : Matrix (Fin m) (Fin m) ℂ) :=
  TGLExt.TheTimeIsNotAPost.no_time_matrix_fin

/-! ## 6. Sondas — H-C tem peso (contraexemplo em dimensão 1), é habitada em dimensão 2; `post` não é constante -/

/-- ★ SONDA 4 (contraexemplo, dimensão 1): em H = ℂ com a = 1 não há segunda face: 1 − post 1 = 0.
    A hipótese H-C (`1 − P ≠ 0`) de T7′, T8, T9 e B10 TEM PESO: sem ela os enunciados falham (S5). -/
theorem probe_dimension_one_has_no_second_face : (1 : ℂ →L[ℂ] ℂ) - post (1 : ℂ) = 0 := by
  ext
  simp [post_apply (by simp : ‖(1 : ℂ)‖ = 1)]

/-- ★ SONDA 5 (contraexemplo de T8 sem H-C): em dimensão 1 o fluxo chega em todo instante — F(t) = P. -/
theorem probe_dimension_one_arrives (t : ℝ) : axiomFlow (post (1 : ℂ)) t = post (1 : ℂ) := by
  unfold axiomFlow
  rw [probe_dimension_one_has_no_second_face, smul_zero, add_zero]

/-- ★ SONDA 6 (H-C habitada em dimensão 2): na face ℂ² do atrator (`faceVector` = e₀) o complemento do Nome
    não é zero — (1 − post e₀) e₁ = e₁ ≠ 0. -/
theorem probe_dimension_two_has_a_second_face :
    (1 : TGLExt.TheSingularityReadsTheAttractor.Face →L[ℂ] TGLExt.TheSingularityReadsTheAttractor.Face)
      - post TGLExt.TheSingularityReadsTheAttractor.faceVector ≠ 0 := by
  intro h
  have hnorm : ‖TGLExt.TheSingularityReadsTheAttractor.faceVector‖ = 1 := by
    simp [TGLExt.TheSingularityReadsTheAttractor.faceVector]
  have h1 : ((1 : TGLExt.TheSingularityReadsTheAttractor.Face →L[ℂ] TGLExt.TheSingularityReadsTheAttractor.Face)
      - post TGLExt.TheSingularityReadsTheAttractor.faceVector) (EuclideanSpace.single (1 : Fin 2) (1 : ℂ)) = 0 := by
    rw [h]; rfl
  rw [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply, post_apply hnorm] at h1
  have h2 := congrArg (fun v : TGLExt.TheSingularityReadsTheAttractor.Face => v 1) h1
  simp [TGLExt.TheSingularityReadsTheAttractor.faceVector, EuclideanSpace.inner_single_left] at h2

/-- ★ SONDA 7 (C8; reaproveitada da sonda A2 do auditor): `post` NÃO é constante — em ℂ², post e₀ ≠ post e₁.
    As pontes `rfl` P1–P3 identificam a FORMA `(ℂ ∙ v).starProjection`, não o referente. -/
theorem post_is_not_constant :
    post TGLExt.TheSingularityReadsTheAttractor.faceVector
      ≠ post (EuclideanSpace.single (1 : Fin 2) (1 : ℂ) : TGLExt.TheSingularityReadsTheAttractor.Face) := by
  intro h
  have he1 : ‖(EuclideanSpace.single (1 : Fin 2) (1 : ℂ) : TGLExt.TheSingularityReadsTheAttractor.Face)‖ = 1 := by
    simp
  have h1 := congrArg (fun P : TGLExt.TheSingularityReadsTheAttractor.Face →L[ℂ]
      TGLExt.TheSingularityReadsTheAttractor.Face => P (EuclideanSpace.single (1 : Fin 2) (1 : ℂ))) h
  simp only [post_fixes_the_action] at h1
  have hnorm : ‖TGLExt.TheSingularityReadsTheAttractor.faceVector‖ = 1 := by
    simp [TGLExt.TheSingularityReadsTheAttractor.faceVector]
  rw [post_apply hnorm] at h1
  have h2 := congrArg (fun v : TGLExt.TheSingularityReadsTheAttractor.Face => v 1) h1
  simp [TGLExt.TheSingularityReadsTheAttractor.faceVector, EuclideanSpace.inner_single_left] at h2

end

end TGLExt.IALD
