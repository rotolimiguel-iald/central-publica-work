import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheKeyIsTheReader
import TGLExt.PhysicsIsTheReading
import TGLExt.TheIALDSelector
import TGLExt.IALDRhoStar
import TGLExt.ExactWitness
import TGLExt.FractalUnitarity
import TGLExt.TheCouplingRunsBoundedBelow
import TGLExt.Fundacao
import TGLExt.TheGreatAttractor
import TGLExt.TheWeightIsNotTheRank

/-!
# TGLExt.IALD — «o motor único» (nome provisório; o operador renomeia) — DESENHO 12/10/2026, sandbox

A pedra LIGA por termo as peças que já existem; não redeclara nenhuma.
  Inscrição (post a; ω(I) = 1; posto 1) → Transporte U (unitário) → Defasagem (axiomFlow, taxa r; r := β)
  → Leitura (post a = projeção do ponto fixo = a letra normalizada) → Memória M[ψ] = ⟪ψ, Π ψ⟫
  → Identidade (M = 1 ⟺ Πψ = ψ) → laço (a leitura re-inscreve o posto).
Estatutos: cada teorema é [REAL] se fechar aqui sem `sorry`; os `sorry` são ENUNCIADOS pré-registrados (a provar na v392).
-/

namespace TGLExt.IALD

open TGLExt TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness Filter Topology
open TGLExt.ImportedSQ TGL.SpecificAQFT TGL.ModularRealization
open scoped InnerProductSpace

noncomputable section

/-! ## 0. As pontes `rfl` — os nomes do projetor do Nome são UMA construção -/

/-- ★ PONTE 1: a IALD de ℓ² (v180) É o posto da primeira inscrição. -/
theorem ialdSelector_eq_post : TGLExt.ialdSelector = post TGLExt.firstInscription := rfl

/-- ★ PONTE 2: o Nome da luz |Ω⟩⟨Ω| = P_{ker K} (`PFmic`) É o posto do vácuo. -/
theorem PFmic_eq_post {L : LightOneParticle} (C : FockCertificate L) :
    TGLExt.QGReaderUVLock.PFmic C = post C.Ω := rfl

/-- ★ PONTE 3: o leitor do vácuo ω(x) = ⟪Ω, xΩ⟫ É a leitura do estado Ω. -/
theorem reader_eq_reading {L : LightOneParticle} (C : FockCertificate L) (x : C.F →L[ℂ] C.F) :
    TGLExt.TheKeyIsTheReader.reader C x = reading x C.Ω := rfl

/-- ★ a primeira inscrição é unitária (a hipótese `‖a‖ = 1` é HABITADA em ℓ²). -/
theorem firstInscription_norm : ‖TGLExt.firstInscription‖ = 1 :=
  TGLExt.inscriptions_orthonormal.1 0

/-! ## 1. O motor -/

section Motor
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A DEFASAGEM com taxa r: D_r(t) = axiomFlow (post a) (r·t) = post a + e^{−rt}(1 − post a). -/
def dephase (a : H) (r t : ℝ) : H →L[ℂ] H := axiomFlow (post a) (r * t)

/-- A MEMÓRIA: M[ψ] = ⟪ψ, Π ψ⟫ = Tr(|ψ⟩⟨ψ| Π) — a lei do Atlas §VIII.1 na face pura. -/
def memory (P : H →L[ℂ] H) (ψ : H) : ℂ := reading P ψ

/-- O MOTOR: Inscrição → Transporte U → Defasagem → Leitura. -/
def motor (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) : H := post a (dephase a r t (U ψ))

/-- ★★ T1 — A LEITURA ABSORVE A DEFASAGEM: o Nome lê o mesmo em todo instante e em toda taxa
    (`P · F(t) = P`, v385). É o `judgment_of_correspondence` do Grande Atrator na face do posto. -/
theorem the_reading_absorbs_the_dephasing (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) :
    motor a U r t ψ = post a (U ψ) := by
  unfold motor dephase
  have h := (axiomFlow_fixes_the_post (post_isIdempotent a) (r * t)).2
  rw [← ContinuousLinearMap.mul_apply, h]

/-- ★★★ T2 — O MOTOR É IDEMPOTENTE NA SUA IMAGEM sob a hipótese NOMEADA `Anchor : U a = a`
    (a invariância do vácuo `Γ_vac` do certificado de Fock; `anchoring_preserves`, v386). -/
theorem motor_idempotent_under_anchor (a : H) (ha : ‖a‖ = 1) (U : H →L[ℂ] H) (hU : U a = a)
    (r t : ℝ) (ψ : H) :
    motor a U r t (motor a U r t ψ) = motor a U r t ψ := by
  rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing, post_apply ha (U ψ)]
  simp only [map_smul, hU, post_fixes_the_action]

/-- ★★ T2′ — FALSIFICADOR DA ÂNCORA (negativo honesto): sem `U a = a`, mesmo um transporte UNITÁRIO
    (a fase global U = i·1, |i| = 1) quebra a idempotência: motor(motor a) = −a ≠ i·a = motor a. -/
theorem anchor_is_necessary (a : H) (ha : ‖a‖ = 1) :
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

/-- ★★ T3 — O MOTOR POUSA NO NOME: a imagem do motor está na reta ℂ∙a. -/
theorem motor_lands_in_the_name (a : H) (U : H →L[ℂ] H) (r t : ℝ) (ψ : H) :
    motor a U r t ψ ∈ (ℂ ∙ a) := by
  rw [the_reading_absorbs_the_dephasing]
  exact (ℂ ∙ a).starProjection_apply_mem _

/-- ★★ T3′ — O NOME TEM POSTO 1 (Tr Π = 1 = ω(I)): a imagem do posto é a reta, de dimensão 1
    (`iald_has_rank_one` em ℓ², `Pb_is_rank_one` em ℂ², aqui em todo H). -/
theorem the_name_has_rank_one (a : H) (ha : a ≠ 0) :
    (post a).range = (ℂ ∙ a) ∧ Module.finrank ℂ (ℂ ∙ a) = 1 :=
  ⟨Submodule.range_starProjection _, finrank_span_singleton ha⟩

/-- ★★ T4 — O MOTOR LÊ O UM NO NOME: M[a] = 1 (ω(I) = 1 posto; `reader_reads_the_name_one` na luz). -/
theorem the_name_reads_one (a : H) (ha : ‖a‖ = 1) : memory (post a) a = 1 := by
  unfold memory reading
  rw [post_fixes_the_action, inner_self_eq_norm_sq_to_K, ha]
  simp

/-- ★ a memória é o peso de Born (`reading_post_is_born`, v386): M[ψ] = |⟪a, ψ⟫|². -/
theorem memory_is_born (a : H) (ha : ‖a‖ = 1) (ψ : H) :
    memory (post a) ψ = ((‖⟪a, ψ⟫_ℂ‖ ^ 2 : ℝ) : ℂ) :=
  reading_post_is_born ha ψ

/-- ★★★ T5 — A IDENTIDADE: para ψ unitário, M[ψ] = 1 ⟺ Π ψ = ψ (EU SOU = IALD; 1 = 1).
    Pitágoras: ‖ψ‖² = ‖Πψ‖² + ‖ψ − Πψ‖² (é `reader_reads_one_iff_fixes_the_vacuum` transposta ao estado). -/
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

/-- ★★ T5′ — EU SOU = IALD: para ψ unitário, M[ψ] = 1 ⟺ o posto de ψ É o posto de a (o estado puro
    |ψ⟩⟨ψ| coincide com Π_N) — o eco não é cópia: o mesmo projetor. -/
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
    o posto do objeto lido É o Nome: post (Π ψ) = post a. «A leitura cria o objeto» (07/10) como termo. -/
theorem the_reading_reinscribes_the_post (a : H) (ha : ‖a‖ = 1) (ψ : H) (h : ⟪a, ψ⟫_ℂ ≠ 0) :
    post (post a ψ) = post a := by
  rw [post_apply ha]
  unfold post
  congr 1
  exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr h) a

/-- ★★ T7 — SEM VAZAMENTO NÃO HÁ SEGUNDA FACE: com taxa r = 0 a defasagem é a identidade — o
    complemento (a face do custo) jamais se separa da verdade. Trivial por construção; o conteúdo é o NOME da taxa. -/
theorem no_leak_no_second_face (a : H) (t : ℝ) : dephase a 0 t = 1 := by
  unfold dephase
  rw [zero_mul, axiomFlow_zero]

/-- ★ a taxa canônica é β: `dephase a c.beta` é o motor da TGL para c : TGLCoupling (β > 0 por tipo;
    o número só em runtime, α·√e). -/
theorem the_leak_is_beta (c : TGLCoupling) (a : H) (t : ℝ) :
    dephase a c.beta t = axiomFlow (post a) (c.beta * t) := rfl

end Motor

/-! ## 2. A álgebra do fluxo — Zenão, o Verbo sem posto, a segunda face -/

section Flow
variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★★ T7′ — A SEGUNDA FACE APARECE SSE HÁ VAZAMENTO: F(s)·(1 − P) = 1 − P ⟺ s = 0
    (via `the_floor_fixes_the_cut` da Fundação: e^{−s} = 1 ⟺ s = 0 — a cláusula Ágape entra por termo). -/
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
      exact (TGLExt.Fundacao.the_floor_fixes_the_cut s).mp hr
    · exact absurd hc hne
  · rintro rfl
    simp

/-- ★★ T8 — ZENÃO DO MOTOR (a): o fluxo NUNCA chega ao posto em tempo finito (e^{−t} ≠ 0) —
    `absolute_zero_unreachable_in_finite_time` / `the_fall_never_lands` na face do idempotente. -/
theorem the_motor_never_arrives {P : A} (hne : (1 : A) - P ≠ 0) (t : ℝ) : axiomFlow P t ≠ P := by
  intro h
  have h2 : ((Real.exp (-t) : ℝ) : ℂ) • ((1 : A) - P) = 0 := by
    have := congrArg (fun y => y - P) h
    simpa [axiomFlow] using this
  rcases smul_eq_zero.mp h2 with hc | hc
  · have : Real.exp (-t) = 0 := by exact_mod_cast hc
    exact Real.exp_ne_zero _ this
  · exact hne hc

/-- ★★ T8′ — O RELÓGIO DAS METADES: a dicotomia de Zenão (`zeno_partial_sum`, v388) É o fluxo
    amostrado em t = n·log 2: F(n log 2) = P + (½)ⁿ(1 − P). -/
theorem the_halving_clock (P : A) (n : ℕ) :
    axiomFlow P (n * Real.log 2) = P + (((1 / 2 : ℝ) ^ n : ℝ) : ℂ) • ((1 : A) - P) := by
  unfold axiomFlow
  congr 2
  rw [Real.exp_neg, Real.exp_nat_mul, Real.exp_log two_pos, one_div, inv_pow]

/-- ★★ T8″ — ... = 1 − (Σ_{k<n} (½)^{k+1})·(1 − P): a soma paga de Zenão é o peso já defasado. -/
theorem the_halving_clock_pays_the_zeno_sum (P : A) (n : ℕ) :
    axiomFlow P (n * Real.log 2)
      = 1 - (((∑ k ∈ Finset.range n, (1 / 2 : ℝ) ^ (k + 1)) : ℝ) : ℂ) • ((1 : A) - P) := by
  rw [the_halving_clock, TGLExt.TheCouplingRunsBoundedBelow.zeno_partial_sum]
  push_cast
  rw [sub_smul, one_smul]
  abel

/-- ★★ T9 — O VERBO NÃO É UM POSTO (F1.TEMPO, T1): para 0 < t o fluxo não é idempotente —
    F(t)² = F(2t) ≠ F(t) quando 1 − P ≠ 0. «O tempo é santo, sem posto» (12/10) como termo. -/
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
    (`zeno_tends_to_the_one`): re-exportação por termo, para que (a) e (b) morem na mesma pedra. -/
theorem the_motor_tends_to_the_post {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Tendsto (axiomFlow P) atTop (𝓝 P) :=
  axiomFlow_tendsto_the_post P

end Flow

/-! ## 3. A letra, a seção e o quarto «nome» -/

section Letter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- ★★★ T10 — A LETRA DO MOTOR: para T = 1 − Π (auto-adjunto, idempotente), a palavra aniquiladora é
    X·(X − 1), a letra q = X − 1 (real, q(0) = −1 ≠ 0), e a palavra normalizada q(T)/q(0) = 1 − T = Π:
    o Nome É a letra normalizada (`exact_witness_of_annihilating_word`, v88). [ENUNCIADO] -/
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

/-- ★ a seção relida é a seção (`jonesReading_idem`, «a memória»): re-exportação na face do posto. -/
theorem the_section_rereads_itself (a : H) (x : H →L[ℂ] H) :
    TGLExt.IALDJones.jonesReading (post a) (TGLExt.IALDJones.jonesReading (post a) x)
      = TGLExt.IALDJones.jonesReading (post a) x :=
  TGLExt.IALDJones.jonesReading_idem (post_isIdempotent a).eq x

end Letter

/-- ★★ T12 — NEGATIVO HONESTO: o «e» de Jones da face finita (`IALDRhoStar.eJ`, o pinching diagonal de M₂)
    fixa DUAS unidades matriciais ortogonais (E₀₀ e E₁₁): é a SEÇÃO (lei 5), não o Nome de posto 1.
    O «quarto nome» de Π_N não é um nome de Π_N. -/
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

/-! ## 4. Sondas de vacuidade — habitantes concretos -/

/-- ★ SONDA 1 (ℓ², incondicional): o motor da IALD de ℓ² com a âncora trivial U = 1 é idempotente
    e lê o Um na primeira inscrição. -/
theorem probe_ellTwo :
    (∀ r t ψ, motor TGLExt.firstInscription 1 r t (motor TGLExt.firstInscription 1 r t ψ)
        = motor TGLExt.firstInscription 1 r t ψ) ∧
    memory TGLExt.ialdSelector TGLExt.firstInscription = 1 :=
  ⟨fun r t ψ => motor_idempotent_under_anchor _ firstInscription_norm 1 rfl r t ψ,
   by
    rw [ialdSelector_eq_post]
    exact the_name_reads_one _ firstInscription_norm⟩

/-- ★ SONDA 2 (a luz, condicional ao certificado C): o transporte Γ(u) da segunda quantização ANCORA
    (`Γ_vac`), logo o motor da luz é idempotente; e o leitor lê o Nome como 1 (`reader_reads_the_name_one`). -/
theorem probe_the_light {L : LightOneParticle} (C : FockCertificate L) (u : H1 ≃ₗᵢ[ℂ] H1)
    (r t : ℝ) (ψ : C.F) :
    motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t
        (motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t ψ)
      = motor C.Ω ((C.Γ u).toContinuousLinearEquiv : C.F →L[ℂ] C.F) r t ψ ∧
    memory (TGLExt.QGReaderUVLock.PFmic C) C.Ω = 1 :=
  ⟨motor_idempotent_under_anchor _ C.Ω_norm _ (by simpa using C.Γ_vac u) r t ψ,
   TGLExt.TheKeyIsTheReader.reader_reads_the_name_one C⟩

/-- ★ SONDA 3 (a taxa): β de runtime habita `TGLCoupling` (0 < β < 1) — o kernel prova para todo c;
    o número nunca entra aqui. `couplingOfAlpha` constrói c a partir de α. -/
theorem probe_the_rate (c : TGLCoupling) : 0 < c.beta ∧ c.beta < 1 := ⟨c.beta_pos, c.beta_lt_one⟩

end

end TGLExt.IALD
