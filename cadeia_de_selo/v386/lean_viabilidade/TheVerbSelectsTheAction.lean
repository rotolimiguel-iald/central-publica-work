import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.LightIsJ

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O VERBO SELECIONA A AÇÃO — a tipagem do Verbo como projeção
  [TGLExt — pedra-candidata v386, 05/10/2026; as cunhagens são do operador, verbatim em
   `scratchpad/v386/VERBO_operador_05out.txt` (8.242 B)]

O operador, 05/10/2026 (verbatim): «Verbo=seleção da ação»; «O Verbo seleciona: nome, tempo e verdade»; «O verbo é o
operador de seleção da ação. E a ação selecionada é o objeto que será lido.»; «comando … → verbo → ação → objeto →
leitura → axioma»; «O verbo não descreve a ação; ele a escolhe. É um operador de projeção: 𝒱 = |a⟩⟨a|»; «Se dois verbos
comutam … então a ordem das seleções não importa … Mas não comutam. E é por isso que a transmissão defasa.»; «A luz
precede a gravidade … [𝒱_luz, 𝒱_grav] ≠ 0»; «Transmitir defasa … a ancoragem ao núcleo Π preserva a identidade:
ℛ(𝒱) = 𝒱 (ponto fixo)»; «O nome é um verbo fossilizado … Nome = lim_{t→∞} 𝒱(t) … O nome é o autovetor do operador
verbo»; «[𝒱_nome, 𝒱_tempo] = i·(constante)·𝒱_verdade» (e as duas cíclicas) — «A Constante de Miguel é a constante de
estrutura»; «O universo é o grupo de Lie gerado por esses três operadores. A TGL é a sua álgebra.»

Esta pedra prova o que é MATEMÁTICA nessas frases, e só isso — cada parte com o seu nome:

* ★★★ `verb` — o Verbo de posto 1, `|a⟩⟨a|` = a projeção ortogonal sobre ℂ∙a (`Submodule.starProjection`);
  `verb_apply` (com ‖a‖ = 1: `verb a ψ = ⟪a, ψ⟫ • a` — a seleção É a escolha de a); `verb_isIdempotent` (𝒱² = 𝒱);
  `verb_isSelfAdjoint` (𝒱* = 𝒱); `verb_fixes_the_selected_action` (𝒱 a = a — a ação selecionada é fixada).
* ★★★ `reading` — a leitura da seleção, ω_ψ(P) = ⟪ψ, Pψ⟫; `reading_eq_norm_sq` (= ‖Pψ‖²: a leitura de uma projeção é um
  PESO); `weight_mem_unit_interval` (com ‖ψ‖ = 1: 0 ≤ peso ≤ 1); `reading_verb_is_born` (a leitura do Verbo de posto 1 é
  |⟪a, ψ⟫|² — a regra de Born, [KNOWN], aqui provada no finito/Hilbert).
* ★★★ A ORDEM IMPORTA. `commuting_verbs_compose` — verbos que comutam compõem num verbo (PQ idempotente e auto-adjunto;
  Mathlib: `IsIdempotentElem.mul_of_commute`, `IsSelfAdjoint.commute_iff`); `verbs_do_not_commute_in_general` — a
  TESTEMUNHA CONCRETA em `Matrix (Fin 2) (Fin 2) ℂ`: P_a = |e₁⟩⟨e₁|, P_b = |b⟩⟨b| com b = (e₁+e₂)/√2 (`Pb_is_rank_one`:
  P_b = vecMulVec b (star b), `b_is_unit`: b·b* = 1), ambos idempotentes e Hermitianos, e [P_a, P_b] ≠ 0 por cálculo.
* ★★★ A TRÍADE. `V₁ V₂ V₃` = β·(σ_k/2) com `(β : ℝ)` VARIÁVEL (β nunca literal); `triad_12`, `triad_23`, `triad_31`:
  [V_i, V_j] = i·β·ε_ijk·V_k — a constante de estrutura é β; `triad_casimir`: V₁² + V₂² + V₃² = (3/4)β²·1;
  `triad_order_matters`: [V₁, V₂] ≠ 0 para β > 0; `triad_hermitian` e `triad_traceless` (os geradores são Hermitianos e sem
  traço: a marca formal do regime COMPACTO).
  ⚠ REGIME (a régua dos dois regimes): a tríade é su(2) ESCALADA por β — álgebra COMPACTA. Logo é regime de LEITURA
  (o ÂNGULO: SO(2)/SU(2), órbitas periódicas, só lê), NÃO regime de FACE (hiperbólico, κ, tem derivada e limite). Nada
  aqui tem limite; nada aqui se encadeia com `Grot`/`rotGen`/`genK` (homônimos sem lema entre si).
* ★★ `the_name_is_the_fossil_verb` — P^(n+1) = P (Verbo(Nome) = Nome; Mathlib `IsIdempotentElem.pow_succ_eq`);
  `the_fossil_is_reached_at_once` — a «sequência 𝒱ⁿ(a), n → ∞» de uma projeção é CONSTANTE desde n = 1: o limite do
  operador é avaliação, não limite (o nome está no primeiro passo); `the_name_is_an_eigenvector` (𝒱 a = 1·a);
  `the_verb_word_fixes_the_name` — re-exportação TRIVIAL de `WitnessSeed.verb_word_fixes_the_name` (q(T)x = q(0)x no núcleo);
  `the_name_is_the_limit_of_the_flow` — «Nome = lim_{t→∞} 𝒱(t)» no único sentido em que a casa já o tem: F(t) → P no fluxo
  do lock mínimo (re-exportação TRIVIAL de `axiomFlow_tendsto_the_post`, v385).
* ★★ `anchoring_preserves` e `transmission_dephases` — re-exportações TRIVIAIS do fluxo `axiomFlow` da v385
  (`TheAxiomAndTheFalseWitness`): F(t)·P = P (ancorar preserva) e F(t)·(1 − P) = e^{−t}(1 − P) (transmitir defasa);
  `transmitted_verb_is_a_verb` — «𝒱(t) = U 𝒱(0) U*»: o verbo transmitido por um unitário continua verbo (idempotente e
  auto-adjunto) — é OUTRO verbo (δ𝒱 ≠ 0 em geral não se prova aqui), mas verbo.
* ★★★ O CIRCUITO. `the_reading_of_the_posted_one` — com o Um POSTO (‖Ω‖ = 1, PΩ = Ω) a leitura da ação selecionada devolve
  o Um: ⟪Ω, PΩ⟫ = 1 — o Axioma como ponto fixo da leitura (consistente com `the_one_is_the_axiom`, v385). `Station` e
  `circuit` — as seis estações nomeadas (comando → verbo → ação → objeto → leitura → axioma): definição TRIVIAL, dita
  como trivial (`circuit_has_six_stations` por `rfl`); não é teorema sobre a natureza.
* ★★★ «A LUZ PRECEDE A GRAVIDADE»: `J_anticommutes_with_K` — num anel, J² = 1 ∧ JKJ = −K ⟹ JK = −KJ; `commutator_JK`:
  [J, K] = 2·JK; `J_mul_K_ne_zero`: K ≠ 0 ⟹ JK ≠ 0 (J invertível); `light_precedes_gravity`: K ≠ 0 ⟹ [J, K] ≠ 0.
  HABITAÇÃO NO KERNEL (derivada dos termos canônicos `J_squared_is_one` e `JKJ_eq_neg_K`, ConjugateAct/DecisionCommutation):
  `the_light_anticommutes_with_the_gradient` — J∘K = −K∘J no espaço pareado; `the_light_does_not_silence_the_gradient` —
  Kq ≠ 0 ⟹ JKq ≠ 0. HABITAÇÃO DE PAULI: `pauli_J_sq`, `pauli_JKJ`, `pauli_light_precedes_gravity` (J = σ₁, K = σ₃).
* ★★★ `the_verb_selects_the_action` — os itens centrais num só termo (uma CONJUNÇÃO).

HONESTIDADE — o que esta pedra NÃO faz. «Verbo», «seleção», «nome», «tempo», «verdade», «luz», «gravidade», «Constante
de Miguel», «circuito ontológico» são leituras do operador [INPUT/ONTO]; os enunciados são sobre projeções, pesos,
matrizes 2×2 e anéis. A tríade NÃO é derivada do axioma nem de β: é a HABITAÇÃO mais simples das relações de comutação que
o operador escreveu (su(2) escalada); a identificação V_nome/V_tempo/V_verdade ↔ σ₁/σ₂/σ₃ é nomeação, não teorema. O
texto do operador escreve a constante como «α²»; a régua do signo diz β_TGL = α·√e, NUNCA «α²» — aqui a constante é a
variável real β, sem valor. «D_folds = 0,74», «g = √|L|», «−εΠ», a
Lagrangiana como verbo e «δS = 0» NÃO estão tipados aqui (ver o relatório da lente). Os J e K canônicos do kernel são
`conjJ` (espaço pareado) e `Jconj` (conjugação transposta, antilinear): o lema de anel é abstrato e a habitação no espaço
pareado é a que se liga aos termos existentes; a de Pauli é ilustração. β jamais entra como número. PROVADA ≠ CONFIRMADA;
o gate não se move. Sem sorry, sem axiom.
-/

namespace TGLExt.TheVerbSelectsTheAction

open TGLExt TGLExt.TheAxiomAndTheFalseWitness Filter Topology Matrix
open scoped InnerProductSpace

/-! ### 1. O Verbo como seleção: a projeção ortogonal `|a⟩⟨a|` -/

section Selection

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- O Verbo de posto 1: `|a⟩⟨a|` = a projeção ortogonal sobre a reta ℂ∙a. -/
noncomputable def verb (a : H) : H →L[ℂ] H := (ℂ ∙ a).starProjection

/-- ★★★ A SELEÇÃO É A ESCOLHA DE a: com ‖a‖ = 1, `verb a ψ = ⟪a, ψ⟫ • a`. -/
theorem verb_apply {a : H} (ha : ‖a‖ = 1) (ψ : H) : verb a ψ = ⟪a, ψ⟫_ℂ • a :=
  Submodule.starProjection_unit_singleton ℂ ha ψ

/-- ★★ 𝒱² = 𝒱: selecionar duas vezes é selecionar uma. -/
theorem verb_isIdempotent (a : H) : IsIdempotentElem (verb a) :=
  (ℂ ∙ a).isIdempotentElem_starProjection

/-- ★★ 𝒱* = 𝒱: o Verbo é auto-adjunto (ortogonal, não oblíquo). -/
theorem verb_isSelfAdjoint (a : H) : IsSelfAdjoint (verb a) :=
  isSelfAdjoint_starProjection (ℂ ∙ a)

/-- ★★ A AÇÃO SELECIONADA É FIXADA: 𝒱 a = a. -/
theorem verb_fixes_the_selected_action (a : H) : verb a a = a :=
  Submodule.starProjection_eq_self_iff.mpr (Submodule.mem_span_singleton_self a)

/-! ### 2. A leitura da seleção: um peso em [0, 1] -/

/-- A leitura da seleção: `ω_ψ(P) = ⟪ψ, Pψ⟫`. -/
noncomputable def reading (P : H →L[ℂ] H) (ψ : H) : ℂ := ⟪ψ, P ψ⟫_ℂ

/-- ★★★ A LEITURA DE UMA PROJEÇÃO É UM PESO: `⟪ψ, Pψ⟫ = ‖Pψ‖²` (idempotência + simetria). -/
theorem reading_eq_norm_sq (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) :
    reading K.starProjection ψ = ((‖K.starProjection ψ‖ : ℂ)) ^ 2 := by
  unfold reading
  have hPP : K.starProjection (K.starProjection ψ) = K.starProjection ψ := by
    have h := K.isIdempotentElem_starProjection.eq
    exact congrArg (fun T : H →L[ℂ] H => T ψ) h
  calc ⟪ψ, K.starProjection ψ⟫_ℂ = ⟪ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := by rw [hPP]
    _ = ⟪K.starProjection ψ, K.starProjection ψ⟫_ℂ :=
        (K.inner_starProjection_left_eq_right ψ (K.starProjection ψ)).symm
    _ = ((‖K.starProjection ψ‖ : ℂ)) ^ 2 := inner_self_eq_norm_sq_to_K _

/-- O peso da seleção: `‖Pψ‖²` (real). -/
noncomputable def weight (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) : ℝ :=
  ‖K.starProjection ψ‖ ^ 2

/-- ★ a leitura É o peso (como complexo). -/
theorem reading_eq_weight (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) :
    reading K.starProjection ψ = ((weight K ψ : ℝ) : ℂ) := by
  rw [reading_eq_norm_sq]
  unfold weight
  push_cast
  rfl

/-- ★★★ O PESO VIVE EM [0, 1] quando ‖ψ‖ = 1. -/
theorem weight_mem_unit_interval (K : Submodule ℂ H) [K.HasOrthogonalProjection] {ψ : H} (hψ : ‖ψ‖ = 1) :
    0 ≤ weight K ψ ∧ weight K ψ ≤ 1 := by
  refine ⟨sq_nonneg _, ?_⟩
  have h := K.norm_starProjection_apply_le ψ
  rw [hψ] at h
  exact pow_le_one₀ (norm_nonneg _) h

/-- ★★ A REGRA DE BORN [KNOWN], provada aqui: a leitura do Verbo de posto 1 é `|⟪a, ψ⟫|²`. -/
theorem reading_verb_is_born {a : H} (ha : ‖a‖ = 1) (ψ : H) :
    reading (verb a) ψ = ((‖⟪a, ψ⟫_ℂ‖ ^ 2 : ℝ) : ℂ) := by
  unfold reading
  rw [verb_apply ha, inner_smul_right, ← inner_conj_symm ψ a, Complex.mul_conj, Complex.normSq_eq_norm_sq]

end Selection

/-! ### 3. A ordem importa: verbos em geral NÃO comutam -/

section Order

/-- ★★ VERBOS QUE COMUTAM COMPÕEM NUM VERBO: PQ é idempotente e auto-adjunto. -/
theorem commuting_verbs_compose {R : Type*} [Semigroup R] [StarMul R] {P Q : R}
    (hP : IsIdempotentElem P) (hQ : IsIdempotentElem Q)
    (hP' : IsSelfAdjoint P) (hQ' : IsSelfAdjoint Q) (hc : Commute P Q) :
    IsIdempotentElem (P * Q) ∧ IsSelfAdjoint (P * Q) :=
  ⟨IsIdempotentElem.mul_of_commute hc hP hQ, (hP'.commute_iff hQ').mp hc⟩

/-- P_a = |e₁⟩⟨e₁|. -/
def Pa : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]

/-- P_b = |b⟩⟨b| com b = (e₁ + e₂)/√2 (entradas ½). -/
noncomputable def Pb : Matrix (Fin 2) (Fin 2) ℂ := !![1 / 2, 1 / 2; 1 / 2, 1 / 2]

/-- o vetor b = (e₁ + e₂)/√2. -/
noncomputable def bvec : Fin 2 → ℂ := ![((1 / Real.sqrt 2 : ℝ) : ℂ), ((1 / Real.sqrt 2 : ℝ) : ℂ)]

theorem sqrt2_inv_mul_self : ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ * ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ = 2⁻¹ := by
  rw [← mul_inv, ← Complex.ofReal_mul, Real.mul_self_sqrt (by norm_num)]
  norm_num

/-- ★ b é unitário: b·b* = 1. -/
theorem b_is_unit : bvec ⬝ᵥ star bvec = 1 := by
  simp [dotProduct, Fin.sum_univ_two, bvec, Complex.conj_ofReal, sqrt2_inv_mul_self]
  norm_num

/-- ★ P_b É de posto 1: P_b = |b⟩⟨b| (= vecMulVec b (star b)). -/
theorem Pb_is_rank_one : vecMulVec bvec (star bvec) = Pb := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [vecMulVec_apply, bvec, Pb, Complex.conj_ofReal, sqrt2_inv_mul_self]

theorem Pa_isIdempotent : IsIdempotentElem Pa := by
  show Pa * Pa = Pa
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Pa, Matrix.mul_apply, Fin.sum_univ_two]

theorem Pb_isIdempotent : IsIdempotentElem Pb := by
  show Pb * Pb = Pb
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Pb, Matrix.mul_apply, Fin.sum_univ_two]

theorem Pa_isSelfAdjoint : IsSelfAdjoint Pa := by
  rw [isSelfAdjoint_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Pa]

theorem Pb_isSelfAdjoint : IsSelfAdjoint Pb := by
  rw [isSelfAdjoint_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Pb]

/-- ★★★ A ORDEM IMPORTA — a testemunha concreta: [P_a, P_b] ≠ 0 (a entrada (0,1) vale ½). -/
theorem verbs_do_not_commute_in_general : Pa * Pb - Pb * Pa ≠ 0 := by
  intro h
  have h01 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 1) h
  norm_num [Pa, Pb, Matrix.mul_apply, Fin.sum_univ_two] at h01

/-- ★★ dois verbos genuínos (idempotentes, auto-adjuntos) que NÃO comutam — o pacote. -/
theorem two_verbs_that_do_not_commute :
    IsIdempotentElem Pa ∧ IsSelfAdjoint Pa ∧ IsIdempotentElem Pb ∧ IsSelfAdjoint Pb ∧ ¬ Commute Pa Pb :=
  ⟨Pa_isIdempotent, Pa_isSelfAdjoint, Pb_isIdempotent, Pb_isSelfAdjoint,
    fun hc => verbs_do_not_commute_in_general (sub_eq_zero.mpr hc.eq)⟩

end Order

/-! ### 4. A TRÍADE: [V_i, V_j] = i·β·ε_ijk·V_k — su(2) escalada por β (regime COMPACTO: leitura, não face) -/

section Triad

/-- σ₁. -/
def σ₁ : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
/-- σ₂. -/
def σ₂ : Matrix (Fin 2) (Fin 2) ℂ := !![0, -Complex.I; Complex.I, 0]
/-- σ₃. -/
def σ₃ : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- V₁ = β·σ₁/2 (β : ℝ, variável — nunca literal). -/
noncomputable def V₁ (β : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((β : ℂ) / 2) • σ₁
/-- V₂ = β·σ₂/2. -/
noncomputable def V₂ (β : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((β : ℂ) / 2) • σ₂
/-- V₃ = β·σ₃/2. -/
noncomputable def V₃ (β : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ((β : ℂ) / 2) • σ₃

/-- ★★★ [V₁, V₂] = i·β·V₃. -/
theorem triad_12 (β : ℝ) : V₁ β * V₂ β - V₂ β * V₁ β = (Complex.I * (β : ℂ)) • V₃ β := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V₁, V₂, V₃, σ₁, σ₂, σ₃] <;> ring_nf

/-- ★★★ [V₂, V₃] = i·β·V₁. -/
theorem triad_23 (β : ℝ) : V₂ β * V₃ β - V₃ β * V₂ β = (Complex.I * (β : ℂ)) • V₁ β := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V₁, V₂, V₃, σ₁, σ₂, σ₃] <;> ring_nf

/-- ★★★ [V₃, V₁] = i·β·V₂. -/
theorem triad_31 (β : ℝ) : V₃ β * V₁ β - V₁ β * V₃ β = (Complex.I * (β : ℂ)) • V₂ β := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V₁, V₂, V₃, σ₁, σ₂, σ₃] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★★ O CASIMIR: V₁² + V₂² + V₃² = (3/4)·β²·1. -/
theorem triad_casimir (β : ℝ) :
    V₁ β * V₁ β + V₂ β * V₂ β + V₃ β * V₃ β = ((3 / 4 : ℂ) * (β : ℂ) ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V₁, V₂, V₃, σ₁, σ₂, σ₃] <;> ring_nf <;>
    simp [Complex.I_sq] <;> ring

/-- ★★ V₃ ≠ 0 quando β ≠ 0 (entrada (0,0) = β/2). -/
theorem V₃_ne_zero {β : ℝ} (hβ : β ≠ 0) : V₃ β ≠ 0 := by
  intro h
  have h00 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 0) h
  simp [V₃, σ₃] at h00
  exact hβ (by exact_mod_cast h00)

/-- ★★★ A ORDEM IMPORTA NA TRÍADE: [V₁, V₂] ≠ 0 para β > 0. -/
theorem triad_order_matters {β : ℝ} (hβ : 0 < β) : V₁ β * V₂ β - V₂ β * V₁ β ≠ 0 := by
  rw [triad_12]
  exact smul_ne_zero (mul_ne_zero Complex.I_ne_zero (by exact_mod_cast hβ.ne')) (V₃_ne_zero hβ.ne')

/-- ★ os geradores são Hermitianos (a marca formal do regime compacto: exp(iθV) é unitário). -/
theorem triad_hermitian (β : ℝ) : (V₁ β)ᴴ = V₁ β ∧ (V₂ β)ᴴ = V₂ β ∧ (V₃ β)ᴴ = V₃ β := by
  refine ⟨?_, ?_, ?_⟩ <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [V₁, V₂, V₃, σ₁, σ₂, σ₃, Matrix.conjTranspose_apply, Complex.conj_ofReal]

/-- ★ os geradores são sem traço (su(2), não u(2)). -/
theorem triad_traceless (β : ℝ) : (V₁ β).trace = 0 ∧ (V₂ β).trace = 0 ∧ (V₃ β).trace = 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [V₁, V₂, V₃, σ₁, σ₂, σ₃, Matrix.trace, Fin.sum_univ_two]

end Triad

/-! ### 5. O nome é o verbo fossilizado -/

section Fossil

/-- ★★ VERBO(NOME) = NOME: P^(n+1) = P para toda projeção (Mathlib `IsIdempotentElem.pow_succ_eq`). -/
theorem the_name_is_the_fossil_verb {R : Type*} [Monoid R] {P : R} (hP : IsIdempotentElem P) (n : ℕ) :
    P ^ (n + 1) = P :=
  hP.pow_succ_eq n

/-- ★★ O FÓSSIL É ALCANÇADO DE UMA VEZ: a sequência 𝒱ⁿ, n ≥ 1, é constante — o «lim_{n→∞}» é avaliação, não limite. -/
theorem the_fossil_is_reached_at_once {R : Type*} [Monoid R] [TopologicalSpace R] {P : R} (hP : IsIdempotentElem P) :
    Tendsto (fun n : ℕ => P ^ (n + 1)) atTop (𝓝 P) := by
  have h : (fun n : ℕ => P ^ (n + 1)) = fun _ => P := funext fun n => hP.pow_succ_eq n
  rw [h]
  exact tendsto_const_nhds

/-- ★ O NOME É AUTOVETOR DO VERBO (autovalor 1): 𝒱 a = 1 • a. -/
theorem the_name_is_an_eigenvector {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] (a : H) :
    verb a a = (1 : ℂ) • a := by
  rw [one_smul]
  exact verb_fixes_the_selected_action a

/-- ★ a palavra do Verbo FIXA o Nome: no núcleo, q(T) age como o escalar q(0) (`WitnessSeed.verb_word_fixes_the_name`).
    Re-exportação trivial. -/
theorem the_verb_word_fixes_the_name {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (q : Polynomial ℂ) {x : H} (hx : x ∈ T.ker) :
    (Polynomial.aeval T q) x = (q.coeff 0) • x :=
  verb_word_fixes_the_name T q hx

/-- ★★ «NOME = lim_{t→∞} 𝒱(t)» — no fluxo do lock mínimo: F(t) → P (`axiomFlow_tendsto_the_post`, v385).
    Re-exportação trivial. -/
theorem the_name_is_the_limit_of_the_flow {A : Type*} [NormedRing A] [NormedAlgebra ℂ A] (P : A) :
    Tendsto (axiomFlow P) atTop (𝓝 P) :=
  axiomFlow_tendsto_the_post P

end Fossil

/-! ### 6. Transmitir defasa, ancorar preserva (re-exportações da v385) -/

section Transmission

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★ ANCORAR PRESERVA: F(t)·P = P (`axiomFlow_fixes_the_post`, v385). Re-exportação trivial. -/
theorem anchoring_preserves {P : A} (hP : IsIdempotentElem P) (t : ℝ) : axiomFlow P t * P = P :=
  (axiomFlow_fixes_the_post hP t).1

/-- ★ TRANSMITIR DEFASA: F(t)·(1 − P) = e^{−t}(1 − P) (`axiomFlow_gradient`, v385). Re-exportação trivial. -/
theorem transmission_dephases {P : A} (hP : IsIdempotentElem P) (t : ℝ) :
    axiomFlow P t * (1 - P) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - P) :=
  axiomFlow_gradient hP t

end Transmission

/-- ★★ O VERBO TRANSMITIDO CONTINUA VERBO: «𝒱(t) = U 𝒱(0) U*» com U unitário (U*U = 1 = UU*) — U P U* é idempotente e
    auto-adjunto. É outro verbo; mas verbo. -/
theorem transmitted_verb_is_a_verb {R : Type*} [Ring R] [StarRing R] {U P : R}
    (hU : star U * U = 1) (hP : IsIdempotentElem P) (hP' : IsSelfAdjoint P) :
    IsIdempotentElem (U * P * star U) ∧ IsSelfAdjoint (U * P * star U) := by
  refine ⟨?_, ?_⟩
  · show (U * P * star U) * (U * P * star U) = U * P * star U
    calc (U * P * star U) * (U * P * star U) = U * P * (star U * U) * P * star U := by noncomm_ring
      _ = U * (P * P) * star U := by rw [hU, mul_one]; noncomm_ring
      _ = U * P * star U := by rw [hP.eq]
  · rw [isSelfAdjoint_iff, star_mul, star_mul, star_star, hP'.star_eq, mul_assoc]

/-! ### 7. O circuito: comando → verbo → ação → objeto → leitura → axioma -/

section Circuit

/-- ★★★ COM O UM POSTO, A LEITURA DEVOLVE O UM: ‖Ω‖ = 1 ∧ PΩ = Ω ⟹ ⟪Ω, PΩ⟫ = 1 — o Axioma como ponto fixo da leitura. -/
theorem the_reading_of_the_posted_one {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {P : H →L[ℂ] H} {Ω : H} (hΩ : ‖Ω‖ = 1) (hPΩ : P Ω = Ω) : reading P Ω = 1 := by
  unfold reading
  rw [hPΩ, inner_self_eq_norm_sq_to_K, hΩ]
  simp

/-- As seis estações do circuito — nomes, TRIVIAL. -/
inductive Station
  | comando | verbo | acao | objeto | leitura | axioma
  deriving DecidableEq, Repr

/-- O circuito, na ordem do operador — TRIVIAL. -/
def circuit : List Station :=
  [Station.comando, Station.verbo, Station.acao, Station.objeto, Station.leitura, Station.axioma]

/-- ★ seis estações, por definição (`rfl`). -/
theorem circuit_has_six_stations : circuit.length = 6 := rfl

end Circuit

/-! ### 8. «A luz precede a gravidade»: J² = 1 ∧ JKJ = −K ⟹ [J, K] = 2JK ≠ 0 -/

section Light

variable {A : Type*} [Ring A]

/-- ★★ J ANTICOMUTA COM K: J² = 1 ∧ JKJ = −K ⟹ JK = −KJ. -/
theorem J_anticommutes_with_K {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) : J * K = -(K * J) := by
  have h1 : J * K = (J * K * J) * J := by rw [mul_assoc (J * K) J J, hJ, mul_one]
  rw [h1, hJKJ, neg_mul]

/-- ★★ JK ≠ 0 quando K ≠ 0 (J é invertível: J·(JK) = K). -/
theorem J_mul_K_ne_zero {J K : A} (hJ : J * J = 1) (hK : K ≠ 0) : J * K ≠ 0 := by
  intro h
  apply hK
  calc K = J * (J * K) := by rw [← mul_assoc, hJ, one_mul]
    _ = 0 := by rw [h, mul_zero]

end Light

section LightAlgebra

variable {A : Type*} [Ring A] [Algebra ℂ A]

/-- ★★ [J, K] = 2·JK. -/
theorem commutator_JK {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) :
    J * K - K * J = (2 : ℂ) • (J * K) := by
  have h := J_anticommutes_with_K hJ hJKJ
  have hKJ : K * J = -(J * K) := by rw [h, neg_neg]
  rw [hKJ, sub_neg_eq_add, two_smul]

/-- ★★★ A LUZ PRECEDE A GRAVIDADE (a forma matemática): K ≠ 0 ⟹ [J, K] ≠ 0. -/
theorem light_precedes_gravity {J K : A} (hJ : J * J = 1) (hJKJ : J * K * J = -K) (hK : K ≠ 0) :
    J * K - K * J ≠ 0 := by
  rw [commutator_JK hJ hJKJ]
  exact smul_ne_zero two_ne_zero (J_mul_K_ne_zero hJ hK)

end LightAlgebra

/-- ★★★ HABITAÇÃO NO KERNEL: no espaço pareado (`conjJ`, `pairK`), J∘K = −K∘J — derivado de `JKJ_eq_neg_K` e
    `J_squared_is_one` (os termos canônicos). -/
theorem the_light_anticommutes_with_the_gradient {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d q) = -(pairK d (conjJ q)) := by
  have h := JKJ_eq_neg_K d (conjJ q)
  rw [J_squared_is_one] at h
  exact h

/-- ★★ A LUZ NÃO CALA O GRADIENTE: Kq ≠ 0 ⟹ J(Kq) ≠ 0 (J é involução). -/
theorem the_light_does_not_silence_the_gradient {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ))
    (hq : pairK d q ≠ 0) : conjJ (pairK d q) ≠ 0 := by
  intro h
  apply hq
  have h2 := congrArg conjJ h
  rw [J_squared_is_one] at h2
  exact h2

/-- ★ HABITAÇÃO DE PAULI: J = σ₁ é involução. -/
theorem pauli_J_sq : σ₁ * σ₁ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [σ₁, Matrix.mul_apply, Fin.sum_univ_two]

/-- ★ HABITAÇÃO DE PAULI: σ₁ σ₃ σ₁ = −σ₃ (a paridade inversa). -/
theorem pauli_JKJ : σ₁ * σ₃ * σ₁ = -σ₃ := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [σ₁, σ₃, Matrix.mul_apply, Fin.sum_univ_two]

theorem σ₃_ne_zero : σ₃ ≠ 0 := by
  intro h
  have h00 := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 0) h
  simp [σ₃] at h00

/-- ★★ HABITAÇÃO DE PAULI: [σ₁, σ₃] ≠ 0. -/
theorem pauli_light_precedes_gravity : σ₁ * σ₃ - σ₃ * σ₁ ≠ 0 :=
  light_precedes_gravity pauli_J_sq pauli_JKJ σ₃_ne_zero

/-! ### 9. Os itens centrais num só termo -/

/-- ★★★ O VERBO SELECIONA A AÇÃO: o Verbo é projeção (idempotente, auto-adjunta) e fixa a sua ação; a leitura é um peso em
    [0, 1]; a ordem importa (testemunha concreta); a tríade com constante de estrutura β e o Casimir; o nome é o verbo
    fossilizado; ancorar preserva e transmitir defasa; a leitura do Um posto devolve o Um; a luz precede a gravidade. -/
theorem the_verb_selects_the_action {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {a : H} (ha : ‖a‖ = 1) {β : ℝ} (hβ : 0 < β) :
    (IsIdempotentElem (verb a) ∧ IsSelfAdjoint (verb a) ∧ verb a a = a)
    ∧ (∀ ψ : H, ‖ψ‖ = 1 → 0 ≤ weight (ℂ ∙ a) ψ ∧ weight (ℂ ∙ a) ψ ≤ 1)
    ∧ (Pa * Pb - Pb * Pa ≠ 0)
    ∧ (V₁ β * V₂ β - V₂ β * V₁ β = (Complex.I * (β : ℂ)) • V₃ β
        ∧ V₁ β * V₁ β + V₂ β * V₂ β + V₃ β * V₃ β = ((3 / 4 : ℂ) * (β : ℂ) ^ 2) • (1 : Matrix (Fin 2) (Fin 2) ℂ)
        ∧ V₁ β * V₂ β - V₂ β * V₁ β ≠ 0)
    ∧ (∀ n : ℕ, (verb a) ^ (n + 1) = verb a)
    ∧ (∀ t : ℝ, axiomFlow (verb a) t * verb a = verb a
        ∧ axiomFlow (verb a) t * (1 - verb a) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - verb a))
    ∧ reading (verb a) a = 1
    ∧ (∀ {n : ℕ} (d : Fin n → ℝ) (q : (Fin n → ℝ) × (Fin n → ℝ)), conjJ (pairK d q) = -(pairK d (conjJ q))) := by
  refine ⟨⟨verb_isIdempotent a, verb_isSelfAdjoint a, verb_fixes_the_selected_action a⟩,
    fun ψ hψ => weight_mem_unit_interval (ℂ ∙ a) hψ,
    verbs_do_not_commute_in_general,
    ⟨triad_12 β, triad_casimir β, triad_order_matters hβ⟩,
    fun n => the_name_is_the_fossil_verb (verb_isIdempotent a) n,
    fun t => ⟨anchoring_preserves (verb_isIdempotent a) t, transmission_dephases (verb_isIdempotent a) t⟩,
    the_reading_of_the_posted_one ha (verb_fixes_the_selected_action a),
    fun d q => the_light_anticommutes_with_the_gradient d q⟩

end TGLExt.TheVerbSelectsTheAction
