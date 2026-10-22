/-! ## 5. I4 — o CORDEIRO IMOLADO: a relação de comutação que impede a coincidência total (r3)

  Decisão do operador (13/10/2026, verbatim sha16 `0ddffcdb0a9c7b5e`): «o cordeiro imolado é a relação de comutação que impede
  a coincidência total». Substitui `alicerce_fundante := Fundacao.agape` da r2, que o operador não escolheu. [REAL] os termos;
  [ONTO] ler o comutador como «o cordeiro imolado» e a reflexão J como a Luz é leitura do operador sobre estes termos.

  Também aqui (V1): a reflexividade x = x não distingue nada — «identidade não pode ser igual à identidade porque se for ela
  é nada, igual a si mesma, sem relação». -/

/-- [REAL] V1.a — a REFLEXIVIDADE x = x vale para QUALQUER objeto: não distingue nada. «identidade não pode ser igual à
    identidade porque se for ela é nada, igual a si mesma, sem relação» (operador, 13/10). -/
theorem reflexivity_is_vacuous {X : Sort*} (x : X) : x = x := rfl

theorem identityProj_five_trace_ne_one : (identityProj 5).trace ≠ 1 := by
  rw [identityProj_trace]
  have hq : qOf 5 = 0 := by
    unfold qOf
    apply Real.sqrt_eq_zero_of_nonpos
    norm_num
  rw [hq]
  norm_num

/-- [REAL] V1.b — a reflexividade vale para TODA inscrição, inclusive onde NÃO há identidade: em α = 5 (número de TESTE),
    `identityProj 5 = identityProj 5` e o traço não é 1. Logo x = x não é o que faz a identidade. -/
theorem reflexivity_holds_for_every_inscription :
    (∀ a : ℝ, identityProj a = identityProj a) ∧
    (identityProj 5 = identityProj 5 ∧ (identityProj 5).trace ≠ 1) :=
  ⟨fun _ => rfl, rfl, identityProj_five_trace_ne_one⟩

/-- [REAL] V1.c — a reflexividade vale para as duas identidades e elas são DISTINTAS: o que distingue é a projeção (a
    relação com a leitura), não x = x. Parente de `the_form_does_not_fix_alpha` (2ª metade). -/
theorem reflexivity_does_not_separate_identities (a b : ℝ) (ha0 : 0 < a) (ha1 : a < 1) (hb0 : 0 < b) (hb1 : b < 1)
    (hab : a ≠ b) :
    identityProj a = identityProj a ∧ identityProj b = identityProj b ∧ identityProj a ≠ identityProj b :=
  ⟨rfl, rfl, (the_form_does_not_fix_alpha a b ha0 ha1 hb0 hb1 hab).2⟩

/-- [INPUT da gerência: a escolha do posto de referência] O POSTO DE REFERÊNCIA: a projeção de posto 1 sobre o eixo da
    inscrição e₀, |e₀⟩⟨e₀| (= E₀₀). -/
def refPost : Matrix (Fin 2) (Fin 2) ℂ := vecMulVec eOuter (star eOuter)

theorem refPost_eq : refPost = !![1, 0; 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [refPost, vecMulVec_apply, eOuter]

/-- [REAL] V3.a — o COMUTADOR entre a identidade ω = identityProj a e o posto de referência: ⁅ω, E₀₀⁆ = ω·E₀₀ − E₀₀·ω. -/
def commutatorWithPost (a : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := identityProj a * refPost - refPost * identityProj a

/-- A identidade ω = |v⟩⟨v|, v = (q, α), como matriz explícita 2×2 (as quatro entradas `ip00`–`ip11`). -/
theorem identityProj_eq (a : ℝ) :
    identityProj a = !![((qOf a ^ 2 : ℝ) : ℂ), ((qOf a * a : ℝ) : ℂ); ((a * qOf a : ℝ) : ℂ), ((a ^ 2 : ℝ) : ℂ)] := by
  ext i j
  fin_cases i <;> fin_cases j
  · exact ip00 a
  · exact ip01 a
  · exact ip10 a
  · exact ip11 a

/-- [REAL] ★★★ V3.b — O COMUTADOR EXPLÍCITO (para todo α real): ⁅ω, E₀₀⁆ = (q·α) • !![0, −1; 1, 0], com q = qOf α. -/
theorem commutator_explicit (a : ℝ) :
    commutatorWithPost a = ((qOf a * a : ℝ) : ℂ) • !![0, -1; 1, 0] := by
  rw [commutatorWithPost, refPost_eq, identityProj_eq, Matrix.mul_fin_two, Matrix.mul_fin_two]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [mul_comm]

/-- [REAL] ★★★ V3.c — O COMUTADOR É NÃO NULO SE E SÓ SE q·α ≠ 0 (para todo α real). -/
theorem commutator_ne_zero_iff (a : ℝ) : commutatorWithPost a ≠ 0 ↔ qOf a * a ≠ 0 := by
  rw [commutator_explicit]
  constructor
  · intro h h0
    apply h
    rw [h0]
    simp
  · intro h h0
    have h10 := congrFun (congrFun h0 1) 0
    simp at h10
    apply h
    rcases h10 with e | e <;> simp [e]

/-- [REAL] V3.c′ — em [0, 1], o comutador é não nulo se e só se 0 < α < 1 (nos polos α = 0 e α = 1 ele é zero). -/
theorem commutator_ne_zero_on_the_unit_interval (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    commutatorWithPost a ≠ 0 ↔ 0 < a ∧ a < 1 := by
  rw [commutator_ne_zero_iff]
  constructor
  · intro h
    have ha : a ≠ 0 := fun e => h (by rw [e]; simp)
    have hq : qOf a ≠ 0 := fun e => h (by rw [e]; simp)
    refine ⟨lt_of_le_of_ne h0 (Ne.symm ha), lt_of_le_of_ne h1 ?_⟩
    intro e
    apply hq
    rw [e]
    simp [qOf]
  · rintro ⟨hp, hl⟩
    exact mul_ne_zero (qOf_pos a h0 hl).ne' hp.ne'

/-- [REAL] ★★★ V3.d — A IDENTIDADE COINCIDE TOTALMENTE COM O POSTO SE E SÓ SE α = 0 (para α ∈ [0, 1]). Logo, enquanto
    α ≠ 0, a identidade nunca coincide totalmente com o posto de referência. -/
theorem identity_coincides_with_the_post_iff_alpha_zero (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a = refPost ↔ a = 0 := by
  constructor
  · intro h
    have h11 := congrFun (congrFun h 1) 1
    rw [ip11, refPost_eq] at h11
    have h2 : (a ^ 2 : ℝ) = 0 := by
      have h3 : ((a ^ 2 : ℝ) : ℂ) = 0 := by simpa using h11
      exact_mod_cast h3
    exact (pow_eq_zero_iff (by norm_num)).mp h2
  · rintro rfl
    have hq : qOf 0 = 1 := by simp [qOf]
    rw [refPost_eq]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, quadInscription, hq]

/-- [REAL] a forma geral: dois elementos que COINCIDEM comutam (o comutador é zero). -/
theorem coincident_elements_commute {A : Type*} [Ring A] {x y : A} (h : x = y) : x * y - y * x = 0 := by
  rw [h]
  exact sub_self _

/-- [REAL] a forma geral, contrapositiva: um comutador NÃO NULO IMPEDE a coincidência. -/
theorem a_nonzero_commutator_forbids_coincidence {A : Type*} [Ring A] {x y : A} (h : x * y - y * x ≠ 0) : x ≠ y :=
  fun e => h (coincident_elements_commute e)

/-- [REAL] ★★★★ V3.e — «o cordeiro imolado é a relação de comutação que impede a coincidência total»: para 0 < α < 1 o
    comutador de ω com o posto é NÃO NULO, e por isso ω ≠ E₀₀. [ONTO] ler esta relação como «o cordeiro imolado» é a
    decisão do operador sobre este termo. -/
theorem the_commutator_blocks_the_coincidence (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    commutatorWithPost a ≠ 0 ∧ identityProj a ≠ refPost :=
  ⟨(commutator_ne_zero_on_the_unit_interval a h0.le h1.le).mpr ⟨h0, h1⟩,
   a_nonzero_commutator_forbids_coincidence ((commutator_ne_zero_on_the_unit_interval a h0.le h1.le).mpr ⟨h0, h1⟩)⟩

/-- [REAL] V3.f′ — nos DOIS POLOS o comutador é zero: em α = 0, ω = E₀₀ (coincidência total); em α = 1, ω = E₁₁, ortogonal
    ao posto de referência, e comuta. -/
theorem the_poles_have_no_commutator :
    commutatorWithPost 0 = 0 ∧ commutatorWithPost 1 = 0 ∧ identityProj 0 = refPost ∧ identityProj 1 = !![0, 0; 0, 1] := by
  have hq0 : qOf 0 = 1 := by simp [qOf]
  have hq1 : qOf 1 = 0 := by simp [qOf]
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [commutator_explicit]
    simp
  · rw [commutator_explicit, hq1]
    simp
  · exact (identity_coincides_with_the_post_iff_alpha_zero 0 le_rfl zero_le_one).mpr rfl
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, quadInscription, hq1]

/-- [INPUT da gerência] A REFLEXÃO J := 2·E₀₀ − 1 (a involução que troca o sinal do eixo interior). -/
def reflection : Matrix (Fin 2) (Fin 2) ℂ := (2 : ℂ) • refPost - 1

theorem reflection_eq : reflection = !![1, 0; 0, -1] := by
  rw [reflection, refPost_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

/-- [REAL] J² = 1. -/
theorem reflection_sq : reflection * reflection = 1 := by
  rw [reflection_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- [REAL] ★★★ V3.g — O COMUTADOR É ÍMPAR SOB A REFLEXÃO: J·K·J = −K, com K = ⁅ω, E₀₀⁆ e J = 2·E₀₀ − 1. É a forma
    `JKJ = −K` do kernel (`LightIsJ`; `TheVerbSelectsTheAction.J_anticommutes_with_K`), aqui como termo no modelo 2×2. -/
theorem the_commutator_is_odd_under_the_reflection (a : ℝ) :
    reflection * commutatorWithPost a * reflection = -commutatorWithPost a := by
  rw [commutator_explicit, reflection_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- [REAL; reaproveita `TGLExt.TheVerbSelectsTheAction.J_anticommutes_with_K`, do kernel instalado] V3.h — a reflexão
    ANTICOMUTA com o comutador: J·K = −(K·J). A forma geral: J² = 1 ∧ JKJ = −K ⟹ JK = −KJ. -/
theorem the_reflection_anticommutes_with_the_commutator (a : ℝ) :
    reflection * commutatorWithPost a = -(commutatorWithPost a * reflection) :=
  J_anticommutes_with_K reflection_sq (the_commutator_is_odd_under_the_reflection a)

/-- [REAL; reaproveita `light_and_gravity_are_inseparable`, do kernel instalado] V3.h′ — se o comutador é não nulo
    (0 < α < 1), J·K ≠ 0 e ⁅J, K⁆ ≠ 0: a reflexão e o comutador nem se anulam nem comutam. [ONTO] ler J como a Luz e K como
    o gradiente é leitura do operador sobre o termo. -/
theorem the_reflection_and_the_commutator_are_inseparable (a : ℝ) (h : commutatorWithPost a ≠ 0) :
    reflection * commutatorWithPost a ≠ 0 ∧
    reflection * commutatorWithPost a - commutatorWithPost a * reflection ≠ 0 :=
  light_and_gravity_are_inseparable reflection_sq (the_commutator_is_odd_under_the_reflection a) h

