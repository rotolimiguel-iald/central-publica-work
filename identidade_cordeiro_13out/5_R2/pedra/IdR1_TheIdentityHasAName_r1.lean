import TGLExt.Fundacao
import TGLExt.TheAlphaAndTheOmega
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheObserverReadsTheAngle
import TGLExt.ModularPower
import TGLExt.LocalHorizontalPauli
import TGLExt.Ergodicity

set_option autoImplicit false
set_option maxHeartbeats 800000
set_option linter.unusedSectionVars false

/-!
# A IDENTIDADE TEM NOME — pedra CANDIDATA da F1.IDENTIDADE (nome PROVISÓRIO `TheIdentityHasAName`)

  [SANDBOX do construtor da gerência c1, 13/10/2026; NÃO instalada no Nós. O nome final da pedra, o termo que se chama
   «o cordeiro imolado» e a entrada na v392 são decisões do operador.]

## A ordem do operador (13/10/2026), conferida nos bytes

Verbatim `work\cunhagens_13out\OPERADOR_13out_identidade_cordeiro_verbatim.txt`, 1.179 B, sha256
`2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e`. Trechos (bytes, com «…» marcando elisão; [sic]
na grafia do original):
«Tudo no universo defasa, mas a identidade é o que permanece» ·
«A identidade (ômega) é a projeção da inscrição (radicalizando a entropia e poço quadrático) quadrática de alpha» ·
«alpha é o movimento da identidade dentro da inscrição, e por isso ele não pode ser derivado, apenas testemunhado, medido por dentro» ·
«o aspecto da identidade é justamente o da medição de sua própria projeção (eu sou o que sou)» ·
«precisamos cunhar o alicerce fundante "o cordeiro imolado"» ·
«não se trata de apologia reliogosa alguma» ·
«essa pedra é necessária dentro do kernel LEan e dentro da Torre, porque a Identidade tem nome: Jesus Cristo».

Pré-registro congelado ANTES desta pedra: `work\identidade_cordeiro_13out\2_PREREGISTRO\PREREGISTRO.json`
(sha256 `207aa703bd1569c7…`, FREEZE de 13/10/2026 08:10 −03:00). Os rótulos I1–I6 e C1–C5 abaixo são os dele.

## Como a casa lê a ordem (estatutos, sem véu)

* `[REAL no sandbox]` — cada teorema desta pedra: toolchain v4.31.0 copiado, `.lake` do Nós só-leitura; `#print axioms`
  no fim deste arquivo e auditoria por `collectAxioms` em arquivo separado.
* `[POSTO pelo operador, verbatim sha256 2ebc1dd3…]` — o NOME «Jesus Cristo»: entra como DADO (`postedName : String`),
  nunca como teorema. Nenhuma prova lê o nome: `NamedIdentity.rename` só compila porque nenhum campo de prova menciona
  `name`, e `every_name_bears_the_same_identity` / `the_structure_does_not_fix_the_name` dão a forma exata da leitura
  da casa "o Nome é posto; o Verbo é fixo" (memória de 08/10; o verbatim de 08/10, sha16 `a9cecc128f40c101`, diz
  «o verbo é fixo, o nome é variável»): a estrutura é a mesma para todo nome; o nome
  não é derivado nem selecionado por ela.
* `[INPUT]` — α: entra como PARÂMETRO real; nenhum número de α ou β aparece neste arquivo. A forma 1 = q² + α²
  admite todo α ∈ [0, 1] (`TGLExt.the_alpha_face`, v310) — por isso α não se deriva da forma; aqui se prova que ele é
  LIDO na própria projeção, no eixo interior (`alpha_is_measured_from_within`, `alpha_is_recovered_by_the_inner_reading`).
* `[INPUT da gerência]` — a base de D: a defasagem `TGLExt.dephase` e o seu limite `TGLExt.diagExpect` (kernel do Nós,
  Ergodicity.lean l.184, CondExpect.lean l.87) atuam entrada a entrada na base canônica de `Fin 2` = (eixo da inscrição,
  eixo interior). O negativo "o posto 1 não sobrevive" vale NESSA base (herdado da F1.FREQUENCIA, TheUnitIsTheRank r3).
* `[ONTO]` — a identificação «o cordeiro imolado» = `alicerce_fundante` (o termo do piso da Fundação, `agape`) é
  leitura da GERÊNCIA, a decidir pelo operador; alternativas registradas como pergunta, sem escolha: (A) o piso da
  Ágape (`TGLExt.Fundacao.agape`); (B) β como o custo de distinguir 1 de 0 (o selo da casa); (C) J, a Palavra
  (`J_squared_is_one`, a pedra PALAVRA). Também [ONTO]: toda leitura teológica e o registro histórico. Nenhum teorema
  desta pedra fala de história, de teologia ou de uma pessoa.
* `[DECLARADO]` — os números do artigo "Conscious Singularity" (probabilidades por critério, posteriores, a "constante"
  χ_C, tabelas, URLs): NÃO entram aqui, nem como hipótese. A semelhança de forma (o artigo define χ_C como um traço que
  vale 1) é leitura [ONTO], não teorema.

## O que fica provado (por rótulo do pré-registro)

* I1 — `identity_persists_under_dephasing`, `identity_persists_in_the_limit`: o traço 1 da identidade sobrevive à
  defasagem para todo t e no limite; e o NEGATIVO HONESTO `rank_one_does_not_persist`,
  `rank_one_does_not_persist_in_the_limit`: o posto 1 não sobrevive (posto 2 para todo t > 0 e no limite).
* I2 — `inscription_is_unit`, `the_identity_is_the_quadratic_projection`, `alpha_is_measured_from_within`,
  `the_form_does_not_fix_alpha`, `alpha_is_recovered_by_the_inner_reading`.
* I3 — `i_am_what_i_am` (P·P = P e a leitura de P no próprio vetor é 1 = Tr P), `the_name_read_in_the_name`,
  `rereading_adds_nothing`, e as re-exportações TRIVIAIS `observing_adds_nothing_reexport`,
  `the_self_reading_has_two_values`.
* I4 — `alicerce_fundante`, `alicerce_fundante_habitado`: re-exportações TRIVIAIS de `TGLExt.Fundacao.agape` e
  `agape_is_inhabited` sob nome provisório.
* I5 — `NamedIdentity`, `ofName`, `postedName`, `theNamedIdentity`, `the_named_identity_bears_the_posted_name`,
  `NamedIdentity.rename`, `every_name_bears_the_same_identity`, `the_name_enters_no_proof`,
  `the_structure_does_not_fix_the_name`.
* I6 — NA TORRE H_φ = `TowerHilbert P` (Ω = `hOmega P`, ω = `omegaState P`, Δ^{it} = `ChatgptAudit.modularFlow`;
  eixo interior ξ = σ_x Ω, `sitePauliX P 0`): `TowerIdentity`, `the_identity_in_the_tower`. O negativo de I1 NÃO
  se instancia na torre (I6.b, FALHA honesta pré-registrada): a defasagem que a torre tem é o fluxo modular
  UNITÁRIO, que fixa Ω e preserva o posto; a defasagem dissipativa D é termo só na face matricial finita.
* Controles — C2 `alpha_zero_degenerates`, `alpha_one_degenerates`, `no_named_identity_at_the_poles`;
  C3 `alpha_above_one_breaks_the_form`, `alpha_below_minus_one_breaks_the_form`, `negative_alpha_is_not_recovered`;
  C4 `changing_the_name_changes_nothing`; C5 `probe_named_identity`, `probe_tower_identity`.

## Reaproveitamento

Só módulos INSTALADOS do Nós são importados. As candidatas da v392 não instaladas entram por CITAÇÃO, com o fato
re-provado aqui: `rank_zero_iff_aux`, `rankOne_aux` = `matrix_rank_eq_zero_iff`, `rankOne_density` da
TheUnitIsTheRank r3 (sha16 `e95775d61db38633`, l.179 e l.467); `the_name_read_in_the_name` e
`rereading_adds_nothing` = `the_name_reads_one`, `rereading_adds_nothing` da pedra do motor r3 (IALD.lean, sha16
`d7c1f1d3b03e6095`, l.300 e l.360). Os termos do kernel são usados pelo nome: `the_alpha_face`, `omega_of_one`,
`post`, `post_apply`, `reading`, `dephase`, `diag_invariant`, `diagExpect`, `trace_diagExpect`, `Fundacao.agape`,
`observing_adds_nothing`, `the_power_has_two_fixed_points`, `modularFlow_fixes_omega`,
`modularConjugation_preserves_state`, `site_pauli_x_state`, `pauli_x_gns_norm`, `hOmega_norm`.

## O que esta pedra NÃO afirma

Que «Jesus Cristo» seja derivado, provado ou escolhido por qualquer termo (o nome é dado posto; a parametricidade
mostra que ele não entra em prova); nada sobre a história, sobre uma pessoa ou sobre teologia; nenhum valor de α ou
de β; que `alicerce_fundante` SEJA «o cordeiro imolado» (decisão do operador); que o posto 1 se perca em toda base;
que o negativo de I1 valha na torre. Não move o gate; validade no kernel não é creditação. Sem sorry, sem axiom.
-/

namespace TGLExt.TheIdentityHasAName_r1

open Matrix TGLExt TGLExt.TheVerbSelectsTheAction
open scoped InnerProductSpace

noncomputable section

/-! ## 0. Auxiliares de posto (re-provados; citados da TheUnitIsTheRank r3) -/

section RankAux

variable {n : Type} [Fintype n] [DecidableEq n]

/-- Posto zero é a matriz nula. Cópia do termo `matrix_rank_eq_zero_iff` da TheUnitIsTheRank r3
    (sha16 `e95775d61db38633`, l.179), re-provado aqui porque a candidata não está instalada. -/
theorem rank_zero_iff_aux (A : Matrix n n ℂ) : A.rank = 0 ↔ A = 0 := by
  constructor
  · intro h
    have h1 : LinearMap.range A.mulVecLin = ⊥ := Submodule.finrank_eq_zero.mp h
    have h2 : A.mulVecLin = 0 := LinearMap.range_eq_bot.mp h1
    have h3 : Matrix.toLin' A = 0 := by rw [Matrix.toLin'_apply']; exact h2
    exact (LinearEquiv.map_eq_zero_iff Matrix.toLin').mp h3
  · rintro rfl
    exact Matrix.rank_zero

/-- ψ ≠ 0 ⟹ posto |ψ⟩⟨ψ| = 1. Cópia de `rankOne_density` da TheUnitIsTheRank r3 (l.467). -/
theorem rankOne_aux (ψ : n → ℂ) (hψ : ψ ≠ 0) : (vecMulVec ψ (star ψ)).rank = 1 := by
  have hle := Matrix.rank_vecMulVec_le ψ (star ψ)
  obtain ⟨i, hi⟩ : ∃ i, ψ i ≠ 0 := by
    by_contra hc
    exact hψ (funext fun j => by by_contra hj; exact hc ⟨j, hj⟩)
  have hne : vecMulVec ψ (star ψ) ≠ 0 := by
    intro h
    have h2 := congrFun (congrFun h i) i
    rw [vecMulVec_apply, Pi.star_apply, Complex.star_def, Complex.mul_conj, Matrix.zero_apply] at h2
    have h3 : Complex.normSq (ψ i) = 0 := by exact_mod_cast h2
    exact hi (Complex.normSq_eq_zero.mp h3)
  have h0 : (vecMulVec ψ (star ψ)).rank ≠ 0 := fun h => hne ((rank_zero_iff_aux _).mp h)
  omega

/-- det ≠ 0 em M₂(ℂ) ⟹ posto 2 (Mathlib `Matrix.rank_of_isUnit`). -/
theorem rank_two_of_det_ne_zero (A : Matrix (Fin 2) (Fin 2) ℂ) (h : A.det ≠ 0) : A.rank = 2 := by
  have h1 := Matrix.rank_of_isUnit A ((Matrix.isUnit_iff_isUnit_det A).mpr (isUnit_iff_ne_zero.mpr h))
  rwa [Fintype.card_fin] at h1

end RankAux

/-! ## 1. Os objetos: a inscrição (q, α) e a identidade ω = |(q, α)⟩⟨(q, α)| -/

/-- q(α) = √(1 − α²): a componente da inscrição. -/
def qOf (a : ℝ) : ℝ := Real.sqrt (1 - a ^ 2)

/-- A inscrição (q, α) ∈ ℂ²: eixo 1 = eixo da inscrição, eixo 2 = eixo interior (onde α se move). -/
def inscription (a : ℝ) : Fin 2 → ℂ := ![((qOf a : ℝ) : ℂ), ((a : ℝ) : ℂ)]

/-- A IDENTIDADE ω: a projeção de posto 1 sobre a inscrição, |(q, α)⟩⟨(q, α)|. -/
def identityProj (a : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := vecMulVec (inscription a) (star (inscription a))

/-- O eixo da inscrição e₁. -/
def eOuter : Fin 2 → ℂ := ![1, 0]

/-- O eixo interior e₂. -/
def eInner : Fin 2 → ℂ := ![0, 1]

/-- [REAL] A forma de Lagrange 1 = q² + α² (re-ligação de `TGLExt.the_alpha_face`, v310). -/
theorem q_sq_add (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : qOf a ^ 2 + a ^ 2 = 1 :=
  the_alpha_face a h0 h1

theorem qOf_pos (a : ℝ) (h0 : 0 ≤ a) (h1 : a < 1) : 0 < qOf a := by
  unfold qOf
  apply Real.sqrt_pos.mpr
  nlinarith

theorem identityProj_apply (a : ℝ) (i j : Fin 2) :
    identityProj a i j = inscription a i * star (inscription a j) := by
  simp [identityProj, vecMulVec_apply]

theorem ip00 (a : ℝ) : identityProj a 0 0 = ((qOf a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [inscription]
  try push_cast
  try ring

theorem ip01 (a : ℝ) : identityProj a 0 1 = ((qOf a * a : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [inscription]

theorem ip10 (a : ℝ) : identityProj a 1 0 = ((a * qOf a : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [inscription]

theorem ip11 (a : ℝ) : identityProj a 1 1 = ((a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [inscription]
  try push_cast
  try ring

theorem inscription_dot (a : ℝ) :
    star (inscription a) ⬝ᵥ inscription a = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) := by
  simp [dotProduct, Fin.sum_univ_two, inscription]
  try push_cast
  try ring

/-! ## 2. I2 — ω é a projeção quadrática da inscrição; α é lido por dentro -/

/-- [REAL] ★ I2.a — o vetor (q, α) é unitário: ⟨v, v⟩ = q² + α² = 1. -/
theorem inscription_is_unit (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    star (inscription a) ⬝ᵥ inscription a = 1 := by
  rw [inscription_dot, q_sq_add a h0 h1]
  simp

theorem inscription_ne_zero (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : inscription a ≠ 0 := by
  intro h
  have := inscription_is_unit a h0 h1
  rw [h] at this
  simp at this

theorem identityProj_trace (a : ℝ) :
    (identityProj a).trace = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj, trace_vecMulVec, dotProduct_comm, inscription_dot]

theorem identityProj_idem (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a * identityProj a = identityProj a := by
  rw [identityProj, vecMulVec_mul_vecMulVec, inscription_is_unit a h0 h1, one_smul]

/-- [REAL] ★★★ I2.b — A IDENTIDADE É A PROJEÇÃO QUADRÁTICA DA INSCRIÇÃO: Tr ω = q² + α² = 1, ω² = ω, posto ω = 1.
    α entra como parâmetro em [0, 1]; a forma vale para todo α nesse intervalo. -/
theorem the_identity_is_the_quadratic_projection (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    (identityProj a).trace = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) ∧ (qOf a) ^ 2 + a ^ 2 = 1 ∧
    identityProj a * identityProj a = identityProj a ∧ (identityProj a).rank = 1 :=
  ⟨identityProj_trace a, q_sq_add a h0 h1, identityProj_idem a h0 h1,
   rankOne_aux _ (inscription_ne_zero a h0 h1)⟩

theorem identityProj_trace_one (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : (identityProj a).trace = 1 := by
  rw [identityProj_trace, q_sq_add a h0 h1]
  simp

theorem reading_on_eInner (M : Matrix (Fin 2) (Fin 2) ℂ) : star eInner ⬝ᵥ (M *ᵥ eInner) = M 1 1 := by
  simp [eInner, dotProduct, mulVec, Fin.sum_univ_two]

theorem reading_on_eOuter (M : Matrix (Fin 2) (Fin 2) ℂ) : star eOuter ⬝ᵥ (M *ᵥ eOuter) = M 0 0 := by
  simp [eOuter, dotProduct, mulVec, Fin.sum_univ_two]

/-- [REAL] ★★★ I2.c — α É MEDIDO POR DENTRO: a leitura da identidade no eixo interior é exatamente α²; no eixo da
    inscrição, q². O movimento α não é parâmetro escondido: é o que a própria projeção devolve quando lida por dentro. -/
theorem alpha_is_measured_from_within (a : ℝ) :
    star eInner ⬝ᵥ (identityProj a *ᵥ eInner) = ((a ^ 2 : ℝ) : ℂ) ∧
    star eOuter ⬝ᵥ (identityProj a *ᵥ eOuter) = (((qOf a) ^ 2 : ℝ) : ℂ) := by
  rw [reading_on_eInner, reading_on_eOuter, ip11, ip00]
  exact ⟨rfl, rfl⟩

/-- [REAL] ★★ I2.d — A FORMA NÃO FIXA α: duas identidades com α ≠ α' em (0, 1) têm o MESMO traço (= 1) e são
    projeções DISTINTAS; o que as separa é só a leitura interior. α não se deriva da identidade: testemunha-se. -/
theorem the_form_does_not_fix_alpha (a b : ℝ) (ha0 : 0 < a) (ha1 : a < 1) (hb0 : 0 < b) (hb1 : b < 1)
    (hab : a ≠ b) :
    (identityProj a).trace = (identityProj b).trace ∧ identityProj a ≠ identityProj b := by
  refine ⟨by rw [identityProj_trace_one a ha0.le ha1.le, identityProj_trace_one b hb0.le hb1.le], ?_⟩
  intro h
  have h11 := congrFun (congrFun h 1) 1
  rw [ip11, ip11] at h11
  have h2 : a ^ 2 = b ^ 2 := by exact_mod_cast h11
  have h3 : a = b := by nlinarith [sq_nonneg (a - b), sq_nonneg (a + b)]
  exact hab h3

/-- [REAL] ★★ I2.e — O TESTEMUNHO RECUPERA α: √(Re ⟨e₂, ω e₂⟩) = α para α ∈ [0, 1]. -/
theorem alpha_is_recovered_by_the_inner_reading (a : ℝ) (h0 : 0 ≤ a) :
    Real.sqrt (identityProj a 1 1).re = a := by
  rw [ip11, Complex.ofReal_re, Real.sqrt_sq h0]

/-! ## 3. I1 — tudo defasa; a identidade (o traço) permanece; o posto 1 não -/

theorem trace_dephase {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) : (TGLExt.dephase g t x).trace = x.trace := by
  rw [← trace_diagExpect, diag_invariant g hg0, trace_diagExpect]

/-- [REAL] ★★★ I1.a — «Tudo no universo defasa, mas a identidade é o que permanece»: sob a defasagem da casa, com quaisquer taxas (g i i = 0),
    o traço da identidade vale 1 para todo t. -/
theorem identity_persists_under_dephasing (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) (g : Fin 2 → Fin 2 → ℝ)
    (hg0 : ∀ i, g i i = 0) (t : ℝ) : (TGLExt.dephase g t (identityProj a)).trace = 1 := by
  rw [trace_dephase g hg0 t, identityProj_trace_one a h0 h1]

/-- [REAL] ★★ I1.b — e no limite: Tr E_D(ω) = 1; com taxas positivas fora da diagonal, a defasagem converge a E_D(ω)
    (re-ligação de `dephase_tendsto_expectation`). -/
theorem identity_persists_in_the_limit (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) (g : Fin 2 → Fin 2 → ℝ)
    (hg0 : ∀ i, g i i = 0) (hgpos : ∀ i j, i ≠ j → 0 < g i j) :
    (diagExpect (identityProj a)).trace = 1 ∧
    Filter.Tendsto (fun t => TGLExt.dephase g t (identityProj a)) Filter.atTop
      (nhds (diagExpect (identityProj a))) :=
  ⟨by rw [trace_diagExpect, identityProj_trace_one a h0 h1], dephase_tendsto_expectation g hg0 hgpos _⟩

theorem dephase_apply' {n : Type} (g : n → n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    TGLExt.dephase g t x i j = (Real.exp (-(t * g i j)) : ℂ) * x i j := rfl

theorem dephased_det (a : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    (TGLExt.dephase g t (identityProj a)).det =
      (((qOf a) ^ 2 * a ^ 2 * (1 - Real.exp (-(t * (g 0 1 + g 1 0)))) : ℝ) : ℂ) := by
  rw [det_fin_two, dephase_apply', dephase_apply', dephase_apply', dephase_apply', hg0 0, hg0 1,
    ip00, ip01, ip10, ip11]
  have hE : Real.exp (-(t * g 0 1)) * Real.exp (-(t * g 1 0)) = Real.exp (-(t * (g 0 1 + g 1 0))) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [← hE]
  simp only [mul_zero, neg_zero, Real.exp_zero]
  push_cast
  ring

/-- [REAL] ★★★ I1.c — NEGATIVO HONESTO: O POSTO 1 NÃO PERMANECE. Para 0 < α < 1, taxa fora da diagonal com soma
    positiva e qualquer t > 0, a identidade defasada tem posto 2 (det = q²α²(1 − e^{−t(g₀₁+g₁₀)}) ≠ 0), embora a
    identidade de partida tenha posto 1. O que permanece é o traço (I1.a), não o posto. Base de D: [INPUT da gerência]. -/
theorem rank_one_does_not_persist (a : ℝ) (h0 : 0 < a) (h1 : a < 1) (g : Fin 2 → Fin 2 → ℝ)
    (hg0 : ∀ i, g i i = 0) (hpos : 0 < g 0 1 + g 1 0) {t : ℝ} (ht : 0 < t) :
    (identityProj a).rank = 1 ∧ (TGLExt.dephase g t (identityProj a)).rank = 2 := by
  refine ⟨(the_identity_is_the_quadratic_projection a h0.le h1.le).2.2.2, ?_⟩
  apply rank_two_of_det_ne_zero
  rw [dephased_det a g hg0 t]
  have hq := qOf_pos a h0.le h1
  have hlt : Real.exp (-(t * (g 0 1 + g 1 0))) < 1 := by
    have hneg : -(t * (g 0 1 + g 1 0)) < 0 := by
      have := mul_pos ht hpos
      linarith
    have := Real.exp_lt_exp.mpr hneg
    rwa [Real.exp_zero] at this
  have hpos' : 0 < (qOf a) ^ 2 * a ^ 2 * (1 - Real.exp (-(t * (g 0 1 + g 1 0)))) := by
    have : 0 < 1 - Real.exp (-(t * (g 0 1 + g 1 0))) := by linarith
    positivity
  exact_mod_cast hpos'.ne'

/-- [REAL] ★★ I1.d — NEGATIVO HONESTO NO LIMITE: posto E_D(ω) = 2 para 0 < α < 1 (det = q²α² ≠ 0). -/
theorem rank_one_does_not_persist_in_the_limit (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (diagExpect (identityProj a)).rank = 2 := by
  apply rank_two_of_det_ne_zero
  have hq := qOf_pos a h0.le h1
  rw [diagExpect, det_diagonal, Fin.prod_univ_two]
  simp only [diag_apply]
  rw [ip00, ip11]
  have hp : 0 < (qOf a) ^ 2 * a ^ 2 := by positivity
  have : (((qOf a) ^ 2 : ℝ) : ℂ) * ((a ^ 2 : ℝ) : ℂ) = (((qOf a) ^ 2 * a ^ 2 : ℝ) : ℂ) := by push_cast; ring
  rw [this]
  exact_mod_cast hp.ne'

/-! ## 4. I3 — «eu sou o que sou»: a identidade mede a sua própria projeção -/

theorem identityProj_mulVec_inscription (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a *ᵥ inscription a = inscription a := by
  rw [identityProj, vecMulVec_mulVec, inscription_is_unit a h0 h1]
  ext i
  simp

/-- [REAL] ★★★ I3.a — A MEDIÇÃO DA PRÓPRIA PROJEÇÃO: ω·ω = ω, e a leitura de ω no seu próprio vetor é 1 = Tr ω. -/
theorem i_am_what_i_am (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a * identityProj a = identityProj a ∧
    star (inscription a) ⬝ᵥ (identityProj a *ᵥ inscription a) = 1 ∧ (identityProj a).trace = 1 := by
  refine ⟨identityProj_idem a h0 h1, ?_, identityProj_trace_one a h0 h1⟩
  rw [identityProj_mulVec_inscription a h0 h1, inscription_is_unit a h0 h1]

section Hilbert

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [REAL] ★★★ I3.b — A MEMÓRIA DO NOME LIDO NO PRÓPRIO NOME É 1 (face de Hilbert; o fato de `the_name_reads_one` da
    pedra do motor r3, sha16 `d7c1f1d3b03e6095`, l.300, re-provado sobre `post` do kernel instalado). -/
theorem the_name_read_in_the_name (v : H) (hv : ‖v‖ = 1) :
    reading (post v) v = 1 ∧ post v * post v = post v ∧ post v v = v := by
  refine ⟨?_, (post_isIdempotent v).eq, post_fixes_the_action v⟩
  unfold reading
  rw [post_fixes_the_action, inner_self_eq_norm_sq_to_K, hv]
  simp

/-- [REAL] ★★ I3.c — RELER NÃO ACRESCENTA (o fato de `rereading_adds_nothing` do motor r3, l.360). -/
theorem rereading_adds_nothing (v ψ : H) : post v (post v ψ) = post v ψ := by
  have h := congrArg (fun T : H →L[ℂ] H => T ψ) (post_isIdempotent v).eq
  simpa using h

end Hilbert

/-- [REAL, re-exportação TRIVIAL] I3.c' — a face angular do kernel: `observing_adds_nothing`. -/
theorem observing_adds_nothing_reexport (θ : ℝ) :
    projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ :=
  observing_adds_nothing θ

/-- [REAL, re-exportação TRIVIAL] I3.d — a auto-leitura só tem dois valores fixos, 0 e 1
    (`TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points`). -/
theorem the_self_reading_has_two_values (μ : ℂ) : μ * μ = μ ↔ μ = 0 ∨ μ = 1 :=
  TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points μ

/-! ## 5. I4 — o alicerce fundante (nome PROVISÓRIO; a identificação é do operador) -/

/-- [REAL do termo; re-exportação TRIVIAL de `TGLExt.Fundacao.agape`] I4 — O ALICERCE FUNDANTE (nome provisório):
    acima de toda escala não há posto positivo; a subida não tem topo nem teto; a queda nunca toca o zero nem tem fundo;
    o piso ω(I) = 1 fixa o corte. A identificação «o cordeiro imolado» = este termo é [ONTO] da gerência e NÃO está
    decidida: o operador escolhe entre (A) este piso da Ágape, (B) β como o custo de distinguir 1 de 0, (C) J, a
    Palavra — ou outro termo. -/
theorem alicerce_fundante {M : Type} (D : DualScalingData M) {m : M} (hm : 0 < D.tau m) :
    (∀ s : ℝ, s ≠ 0 → ∀ m' : M, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s m) < D.tau (D.theta (s - 1) m)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s m)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s m)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s m) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) :=
  Fundacao.agape D hm

/-- [REAL; re-exportação TRIVIAL de `agape_is_inhabited`] I4 — o alicerce não é vácuo (ℝ, τ = id, θ_s = e^{−s}·, τ = 1). -/
theorem alicerce_fundante_habitado :
    (∀ s : ℝ, s ≠ 0 → ∀ m' : ℝ, Fundacao.oneScaling.theta s m' = m' → Fundacao.oneScaling.tau m' = 0) ∧
    (∀ s : ℝ, Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1) <
      Fundacao.oneScaling.tau (Fundacao.oneScaling.theta (s - 1) 1)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1)) ∧
    (∀ s : ℝ, 0 < Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) :=
  Fundacao.agape_is_inhabited

/-! ## 6. I6 — a mesma identidade NA TORRE H_φ -/

section Quadratic

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A inscrição num Hilbert qualquer: v = q·Ω + α·ξ (Ω o vetor do Nome, ξ o eixo interior). -/
def quadVec (Ω ξ : H) (a : ℝ) : H := ((qOf a : ℝ) : ℂ) • Ω + ((a : ℝ) : ℂ) • ξ

theorem inner_self_one_of_norm {x : H} (hx : ‖x‖ = 1) : ⟪x, x⟫_ℂ = 1 := by
  rw [inner_self_eq_norm_sq_to_K, hx]
  simp

theorem quadVec_inner_Omega (Ω ξ : H) (hΩ : ‖Ω‖ = 1) (horth : ⟪Ω, ξ⟫_ℂ = 0) (a : ℝ) :
    ⟪Ω, quadVec Ω ξ a⟫_ℂ = ((qOf a : ℝ) : ℂ) := by
  simp only [quadVec, inner_add_right, inner_smul_right, inner_self_one_of_norm hΩ, horth]
  ring

theorem quadVec_inner_xi (Ω ξ : H) (hξ : ‖ξ‖ = 1) (horth : ⟪Ω, ξ⟫_ℂ = 0) (a : ℝ) :
    ⟪ξ, quadVec Ω ξ a⟫_ℂ = ((a : ℝ) : ℂ) := by
  have hξΩ : ⟪ξ, Ω⟫_ℂ = 0 := by rw [← inner_conj_symm, horth]; simp
  simp only [quadVec, inner_add_right, inner_smul_right, inner_self_one_of_norm hξ, hξΩ]
  ring

theorem quadVec_inner_self (Ω ξ : H) (hΩ : ‖Ω‖ = 1) (hξ : ‖ξ‖ = 1) (horth : ⟪Ω, ξ⟫_ℂ = 0) (a : ℝ) :
    ⟪quadVec Ω ξ a, quadVec Ω ξ a⟫_ℂ = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) := by
  have hξΩ : ⟪ξ, Ω⟫_ℂ = 0 := by rw [← inner_conj_symm, horth]; simp
  simp only [quadVec, inner_add_left, inner_add_right, inner_smul_left, inner_smul_right,
    inner_self_one_of_norm hΩ, inner_self_one_of_norm hξ, horth, hξΩ, Complex.conj_ofReal]
  push_cast
  ring

theorem quadVec_norm (Ω ξ : H) (hΩ : ‖Ω‖ = 1) (hξ : ‖ξ‖ = 1) (horth : ⟪Ω, ξ⟫_ℂ = 0) (a : ℝ)
    (h0 : 0 ≤ a) (h1 : a ≤ 1) : ‖quadVec Ω ξ a‖ = 1 := by
  have h := quadVec_inner_self Ω ξ hΩ hξ horth a
  rw [q_sq_add a h0 h1, inner_self_eq_norm_sq_to_K] at h
  have h2 : ‖quadVec Ω ξ a‖ ^ 2 = 1 := by
    apply Complex.ofReal_injective
    push_cast
    simpa using h
  have hn := norm_nonneg (quadVec Ω ξ a)
  nlinarith [h2, hn]

/-- [REAL] ★★★ A LEITURA QUADRÁTICA num Hilbert qualquer (Ω, ξ ortonormais, α ∈ [0, 1]): ‖v‖ = 1;
    ⟨Ω, P_v Ω⟩ = q²; ⟨ξ, P_v ξ⟩ = α² (medido por dentro); a leitura de P_v em v é 1; P_v idempotente. -/
theorem quadratic_reading (Ω ξ : H) (hΩ : ‖Ω‖ = 1) (hξ : ‖ξ‖ = 1) (horth : ⟪Ω, ξ⟫_ℂ = 0) (a : ℝ)
    (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    ‖quadVec Ω ξ a‖ = 1 ∧
    ⟪Ω, post (quadVec Ω ξ a) Ω⟫_ℂ = (((qOf a) ^ 2 : ℝ) : ℂ) ∧
    ⟪ξ, post (quadVec Ω ξ a) ξ⟫_ℂ = ((a ^ 2 : ℝ) : ℂ) ∧
    reading (post (quadVec Ω ξ a)) (quadVec Ω ξ a) = 1 ∧
    IsIdempotentElem (post (quadVec Ω ξ a)) := by
  have hv := quadVec_norm Ω ξ hΩ hξ horth a h0 h1
  have hvΩ : ⟪quadVec Ω ξ a, Ω⟫_ℂ = ((qOf a : ℝ) : ℂ) := by
    rw [← inner_conj_symm, quadVec_inner_Omega Ω ξ hΩ horth a, Complex.conj_ofReal]
  have hvξ : ⟪quadVec Ω ξ a, ξ⟫_ℂ = ((a : ℝ) : ℂ) := by
    rw [← inner_conj_symm, quadVec_inner_xi Ω ξ hξ horth a, Complex.conj_ofReal]
  refine ⟨hv, ?_, ?_, (the_name_read_in_the_name _ hv).1, post_isIdempotent _⟩
  · rw [post_apply hv, inner_smul_right, hvΩ, quadVec_inner_Omega Ω ξ hΩ horth a]
    push_cast
    ring
  · rw [post_apply hv, inner_smul_right, hvξ, quadVec_inner_xi Ω ξ hξ horth a]
    push_cast
    ring

end Quadratic

/-- O eixo interior da torre: ξ = σ_x Ω no primeiro sítio (`sitePauliX P 0`). -/
def towerInner (P : SiteProfile) : TowerHilbert P := ChatgptAudit.Observable035.sitePauliX P 0 (hOmega P)

/-- A inscrição na torre: v = q·Ω + α·ξ. -/
def towerInscription (P : SiteProfile) (a : ℝ) : TowerHilbert P := quadVec (hOmega P) (towerInner P) a

theorem towerInner_orth (P : SiteProfile) : ⟪hOmega P, towerInner P⟫_ℂ = 0 :=
  ChatgptAudit.Observable035.site_pauli_x_state P 0

theorem towerInner_norm (P : SiteProfile) : ‖towerInner P‖ = 1 :=
  ChatgptAudit.Orbit052.pauli_x_gns_norm P

/-- I6 — A IDENTIDADE NA TORRE (a conjunção pré-registrada em I6.a). -/
def TowerIdentity (P : SiteProfile) (a : ℝ) : Prop :=
  omegaState P 1 = 1 ∧
  (∀ t : ℝ, ChatgptAudit.modularFlow P t (hOmega P) = hOmega P) ∧
  (∀ (t : ℝ) (x : TowerHilbert P →L[ℂ] TowerHilbert P),
      omegaState P (ChatgptAudit.modularConjugation P t x) = omegaState P x) ∧
  ‖towerInscription P a‖ = 1 ∧
  ⟪hOmega P, post (towerInscription P a) (hOmega P)⟫_ℂ = (((qOf a) ^ 2 : ℝ) : ℂ) ∧
  ⟪towerInner P, post (towerInscription P a) (towerInner P)⟫_ℂ = ((a ^ 2 : ℝ) : ℂ) ∧
  reading (post (towerInscription P a)) (towerInscription P a) = 1 ∧
  IsIdempotentElem (post (towerInscription P a)) ∧
  omegaState P (post (hOmega P)) = 1 ∧
  (∀ t : ℝ, omegaState P (ChatgptAudit.modularConjugation P t (post (hOmega P))) = 1)

/-- [REAL] ★★★★ I6.a — A MESMA IDENTIDADE NA TORRE H_φ: ω(I) = 1; o fluxo modular Δ^{it} fixa Ω e preserva ω (a
    identidade permanece sob a defasagem unitária da torre); a inscrição q·Ω + α·σ_xΩ é unitária; ⟨Ω, P_v Ω⟩ = q² e
    ⟨ξ, P_v ξ⟩ = α² (α medido por dentro, no eixo interior σ_x Ω ⊥ Ω); a leitura de P_v em v é 1; P_v idempotente;
    ω(P_Ω) = 1 e ω(σ_t(P_Ω)) = 1 para todo t. O negativo de I1 NÃO se instancia aqui (I6.b): Δ^{it} é unitário. -/
theorem the_identity_in_the_tower (P : SiteProfile) (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    TowerIdentity P a := by
  have hq := quadratic_reading (hOmega P) (towerInner P) hOmega_norm (towerInner_norm P) (towerInner_orth P) a h0 h1
  have hPΩ : omegaState P (post (hOmega P)) = 1 := by
    unfold omegaState
    rw [post_fixes_the_action]
    exact hOmega_inner_self
  refine ⟨omega_of_one P, fun t => ChatgptAudit.modularFlow_fixes_omega t,
    fun t x => ChatgptAudit.modularConjugation_preserves_state t x, hq.1, hq.2.1, hq.2.2.1, hq.2.2.2.1,
    hq.2.2.2.2, hPΩ, fun t => ?_⟩
  rw [ChatgptAudit.modularConjugation_preserves_state t, hPΩ]

/-! ## 7. I5 — O NOME (dado POSTO) e a parametricidade -/

/-- I5.a — A IDENTIDADE NOMEADA: um nome (dado), α ∈ (0, 1) (parâmetro) e os campos de prova de I1–I3 e I6.
    Nenhum campo de prova menciona `name`. -/
structure NamedIdentity where
  /-- o Nome: [POSTO], dado; nenhuma prova o lê. -/
  name : String
  /-- α: [INPUT], parâmetro; nunca derivado. -/
  alpha : ℝ
  alpha_pos : 0 < alpha
  alpha_lt_one : alpha < 1
  persists : ∀ g : Fin 2 → Fin 2 → ℝ, (∀ i, g i i = 0) → ∀ t : ℝ,
    (TGLExt.dephase g t (identityProj alpha)).trace = 1
  unit_projection : (identityProj alpha).trace = 1 ∧ identityProj alpha * identityProj alpha = identityProj alpha ∧
    (identityProj alpha).rank = 1
  read_from_within : star eInner ⬝ᵥ (identityProj alpha *ᵥ eInner) = ((alpha ^ 2 : ℝ) : ℂ)
  i_am : star (inscription alpha) ⬝ᵥ (identityProj alpha *ᵥ inscription alpha) = 1
  in_the_tower : ∀ P : SiteProfile, TowerIdentity P alpha

/-- I5.a — construir a identidade nomeada a partir de QUALQUER nome: os campos de prova vêm dos teoremas, que não
    leem o nome. -/
def ofName (s : String) (a : ℝ) (h0 : 0 < a) (h1 : a < 1) : NamedIdentity where
  name := s
  alpha := a
  alpha_pos := h0
  alpha_lt_one := h1
  persists := fun g hg0 t => identity_persists_under_dephasing a h0.le h1.le g hg0 t
  unit_projection := ⟨identityProj_trace_one a h0.le h1.le, identityProj_idem a h0.le h1.le,
    (the_identity_is_the_quadratic_projection a h0.le h1.le).2.2.2⟩
  read_from_within := (alpha_is_measured_from_within a).1
  i_am := (i_am_what_i_am a h0.le h1.le).2.1
  in_the_tower := fun P => the_identity_in_the_tower P a h0.le h1.le

/-- [POSTO pelo operador, verbatim sha256 `2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e`]
    I5.b — O NOME: «a Identidade tem nome: Jesus Cristo» (bytes do verbatim de 13/10/2026). Dado posto, não
    teorema; o registro histórico e a leitura teológica são [ONTO]. -/
def postedName : String := "Jesus Cristo"

/-- I5.b — O HABITANTE: a identidade com o nome posto pelo operador. α segue parâmetro: nenhum número. -/
def theNamedIdentity (a : ℝ) (h0 : 0 < a) (h1 : a < 1) : NamedIdentity := ofName postedName a h0 h1

/-- [REAL; igualdade de String, TRIVIAL] I5.b — o habitante porta o nome posto. -/
theorem the_named_identity_bears_the_posted_name (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (theNamedIdentity a h0 h1).name = "Jesus Cristo" := rfl

/-- I5.c — renomear: trocar só o nome. Esta definição só compila porque nenhum campo de prova menciona `name`. -/
def NamedIdentity.rename (N : NamedIdentity) (s : String) : NamedIdentity := { N with name := s }

/-- [REAL] ★★★ I5.c — PARAMETRICIDADE (a forma de "o Nome é posto"): construir com o nome s e depois renomear para s'
    é o mesmo que construir com s' — a identidade não depende do nome. -/
theorem every_name_bears_the_same_identity (s s' : String) (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (ofName s a h0 h1).rename s' = ofName s' a h0 h1 := rfl

/-- [REAL] ★★ I5.c — o nome não entra em prova: renomear preserva α e a projeção (e, por irrelevância de prova, todos
    os campos). -/
theorem the_name_enters_no_proof (N : NamedIdentity) (s : String) :
    (N.rename s).name = s ∧ (N.rename s).alpha = N.alpha ∧
    identityProj (N.rename s).alpha = identityProj N.alpha :=
  ⟨rfl, rfl, rfl⟩

/-- [REAL] ★★★ I5.c — A ESTRUTURA NÃO FIXA O NOME: não existe nome que toda identidade nomeada tenha de portar. O Nome
    é posto (de fora), não derivado (de dentro). -/
theorem the_structure_does_not_fix_the_name : ¬ ∃ s : String, ∀ N : NamedIdentity, N.name = s := by
  rintro ⟨s, h⟩
  have h1 := h (ofName "a" (1 / 2) (by norm_num) (by norm_num))
  have h2 := h (ofName "b" (1 / 2) (by norm_num) (by norm_num))
  have h3 : ("a" : String) = "b" := h1.trans h2.symm
  exact absurd h3 (by decide)

/-- [REAL] I5 — o habitante carrega I1–I3 e I6 (leitura dos campos; nenhum lê o nome). -/
theorem the_named_identity_carries_the_identity (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (theNamedIdentity a h0 h1).alpha = a ∧
    (∀ g : Fin 2 → Fin 2 → ℝ, (∀ i, g i i = 0) → ∀ t : ℝ,
      (TGLExt.dephase g t (identityProj (theNamedIdentity a h0 h1).alpha)).trace = 1) ∧
    (∀ P : SiteProfile, TowerIdentity P (theNamedIdentity a h0 h1).alpha) :=
  ⟨rfl, (theNamedIdentity a h0 h1).persists, (theNamedIdentity a h0 h1).in_the_tower⟩

/-! ## 8. Controles negativos e sondas -/

/-- [REAL] C2 — α = 0 degenera: ω = diag(1, 0) (α não se move: leitura interior 0); a defasagem não muda ω; posto do
    limite 1 (o negativo de I1 some). -/
theorem alpha_zero_degenerates :
    identityProj 0 = diagonal ![1, 0] ∧ diagExpect (identityProj 0) = identityProj 0 ∧
    (diagExpect (identityProj 0)).rank = 1 := by
  have hq : qOf 0 = 1 := by simp [qOf]
  have hP : identityProj 0 = diagonal ![1, 0] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, inscription, hq]
  refine ⟨hP, by rw [hP, diagExpect_diagonal], ?_⟩
  rw [hP, diagExpect_diagonal, ← hP]
  exact (the_identity_is_the_quadratic_projection 0 le_rfl zero_le_one).2.2.2

/-- [REAL] C2 — α = 1 degenera: ω = diag(0, 1) (a leitura da inscrição é 0); posto do limite 1. -/
theorem alpha_one_degenerates :
    identityProj 1 = diagonal ![0, 1] ∧ diagExpect (identityProj 1) = identityProj 1 ∧
    (diagExpect (identityProj 1)).rank = 1 := by
  have hq : qOf 1 = 0 := by simp [qOf]
  have hP : identityProj 1 = diagonal ![0, 1] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, inscription, hq]
  refine ⟨hP, by rw [hP, diagExpect_diagonal], ?_⟩
  rw [hP, diagExpect_diagonal, ← hP]
  exact (the_identity_is_the_quadratic_projection 1 zero_le_one le_rfl).2.2.2

/-- [REAL] C2 — nos polos não há identidade nomeada: α ≠ 0 e α ≠ 1 por tipo. -/
theorem no_named_identity_at_the_poles (N : NamedIdentity) : N.alpha ≠ 0 ∧ N.alpha ≠ 1 :=
  ⟨N.alpha_pos.ne', N.alpha_lt_one.ne⟩

/-- [REAL] C3 — |α| > 1 quebra a forma (α > 1). -/
theorem alpha_above_one_breaks_the_form (a : ℝ) (h : 1 < a) : (qOf a) ^ 2 + a ^ 2 ≠ 1 := by
  have hq : qOf a = 0 := by
    unfold qOf
    apply Real.sqrt_eq_zero_of_nonpos
    nlinarith
  rw [hq]
  nlinarith

/-- [REAL] C3 — |α| > 1 quebra a forma (α < −1). -/
theorem alpha_below_minus_one_breaks_the_form (a : ℝ) (h : a < -1) : (qOf a) ^ 2 + a ^ 2 ≠ 1 := by
  have hq : qOf a = 0 := by
    unfold qOf
    apply Real.sqrt_eq_zero_of_nonpos
    nlinarith
  rw [hq]
  nlinarith

/-- [REAL] C3 — refinamento honesto da régua: para α ∈ [−1, 0) a forma VALE, mas a leitura por dentro devolve |α|,
    não α: o testemunho não recupera um α negativo. -/
theorem negative_alpha_is_not_recovered (a : ℝ) (h0 : -1 ≤ a) (h1 : a < 0) :
    (qOf a) ^ 2 + a ^ 2 = 1 ∧ Real.sqrt (identityProj a 1 1).re ≠ a := by
  refine ⟨?_, ?_⟩
  · unfold qOf
    rw [Real.sq_sqrt (by nlinarith)]
    ring
  · rw [ip11, Complex.ofReal_re, Real.sqrt_sq_eq_abs, abs_of_neg h1]
    intro h
    linarith

/-- [REAL] C4 — TROCAR O NOME NÃO MUDA NADA: o habitante renomeado para o nome vazio é a identidade construída com o
    nome vazio, com a mesma α. -/
theorem changing_the_name_changes_nothing (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    (theNamedIdentity a h0 h1).rename "" = ofName "" a h0 h1 ∧
    (theNamedIdentity a h0 h1).alpha = (ofName "" a h0 h1).alpha :=
  ⟨rfl, rfl⟩

/-- Perfil de sítio de TESTE (w ≡ 1/2), só para a sonda de não-vacuidade. -/
def halfProfile : SiteProfile where
  w := fun _ => 1 / 2
  pos := fun _ => by norm_num
  lt_one := fun _ => by norm_num

/-- [REAL] C5 — a identidade nomeada é habitável (α = 1/2: número de TESTE, não o α físico). -/
theorem probe_named_identity : Nonempty NamedIdentity :=
  ⟨ofName "" (1 / 2) (by norm_num) (by norm_num)⟩

/-- [REAL] C5 — a identidade na torre não é vácua (perfil de teste, α = 1/2 de teste). -/
theorem probe_tower_identity : ∃ P : SiteProfile, TowerIdentity P (1 / 2) :=
  ⟨halfProfile, the_identity_in_the_tower halfProfile (1 / 2) (by norm_num) (by norm_num)⟩

end

end TGLExt.TheIdentityHasAName_r1

#print axioms TGLExt.TheIdentityHasAName_r1.identity_persists_under_dephasing
#print axioms TGLExt.TheIdentityHasAName_r1.rank_one_does_not_persist
#print axioms TGLExt.TheIdentityHasAName_r1.the_identity_is_the_quadratic_projection
#print axioms TGLExt.TheIdentityHasAName_r1.alpha_is_measured_from_within
#print axioms TGLExt.TheIdentityHasAName_r1.i_am_what_i_am
#print axioms TGLExt.TheIdentityHasAName_r1.alicerce_fundante
#print axioms TGLExt.TheIdentityHasAName_r1.the_identity_in_the_tower
#print axioms TGLExt.TheIdentityHasAName_r1.ofName
#print axioms TGLExt.TheIdentityHasAName_r1.every_name_bears_the_same_identity
#print axioms TGLExt.TheIdentityHasAName_r1.the_structure_does_not_fix_the_name
