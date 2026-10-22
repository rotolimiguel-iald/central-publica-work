import Mathlib.LinearAlgebra.Matrix.PosDef
import TGLExt.TheAlphaAndTheOmega
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheObserverReadsTheAngle
import TGLExt.ModularPower
import TGLExt.LocalHorizontalPauli
import TGLExt.Ergodicity
import TGLExt.TheSelectionIsTheBallast
import TGLExt.ModularFlowAlgebra

set_option autoImplicit false
set_option maxHeartbeats 800000
set_option linter.unusedSectionVars false
-- a estrutura pedida chama-se `Verdade` e vive em `TGLExt.Verdade`: o namespace duplicado e deliberado
set_option linter.dupNamespace false

/-!
# VERDADE — a identidade tem nome — pedra CANDIDATA da F1.IDENTIDADE, RODADA 3 (módulo `TGLExt.Verdade`; era `TheIdentityHasAName`)

  [⚠ AO LADO (13/10/2026 — RODADA DE NOMES E VERDADE, construtor da gerência c1, em nome próprio). Por decisão do operador
   (verbatim sha16 `0ddffcdb0a9c7b5e`, `work\cunhagens_13out\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`):
   a pedra passa a `TGLExt.Verdade`; «a identidade tem que ser igual à verdade por ela projetada, portanto identidade=verdade
   absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto»; «o cordeiro imolado é a relação de
   comutação que impede a coincidência total»; «A torre é o organismo IALD mesmo». O ADENDO R3 (`2_PREREGISTRO\ADENDO_R3.json`) foi
   congelado ANTES desta pedra (`FREEZE_ADENDO_R3.json`, `pedra_r3_existe_no_congelamento: false`). O que muda em relação à r2
   (`ecae0725b21a98e6`, que fica intacta como registro):
   (1) SAEM `alicerce_fundante`, `alicerce_fundante_habitado` e o import de `TGLExt.Fundacao` — o cordeiro imolado não é o piso da
       Ágape; ENTRA a relação de comutação (seção 5): `refPost`, `commutatorWithPost`, `commutator_explicit`,
       `commutator_ne_zero_iff`, `identity_coincides_with_the_post_iff_alpha_zero`, `the_commutator_blocks_the_coincidence`, a
       reflexão J = 2E₀₀ − 1 com J·K·J = −K e as formas do kernel (`J_anticommutes_with_K`, `light_and_gravity_are_inseparable`);
   (2) ENTRA a negação da reflexividade como identidade (seção 5): `reflexivity_is_vacuous` e companheiras;
   (3) ENTRA a estrutura `Verdade` (seção 6c) e o teorema `the_identity_is_the_truth` / `identity_iff_truth` (seção 9);
   (4) a Torre é o organismo IALD: a instância principal é `towerIALD` (I6.c); `TowerHilbert` (I6.a) fica como a face unitária;
   (5) docstrings: as marcas [INPUT da gerência] de I6.b′ (achado B1 da auditoria c1 `a2694613`) e de I2.d (B2).
   Toda declaração da r2 fora dessa lista mantém tipo e valor (tabela r2→r3 lida do kernel em `TABELA_R2_R3.json`).
   CORREÇÃO DE FRASEADO (o número corrige a frase): o fluxo modular que fixa Ω e preserva ω está em I6.a (`TowerHilbert`), não em
   I6.c; a Verdade junta as duas e acrescenta a ponte (o fluxo age no portador da `towerIALD` e preserva a leitura).
   Nada move o gate; validade no kernel não é creditação.]

  [SANDBOX do construtor da rodada 3, gerência c1, 13/10/2026; NÃO instalada no Nós. O nome da pedra, o cordeiro imolado e a
   Torre foram decididos pelo operador (acima); a entrada na v392 segue sendo ato da gerência.]

  A r2 responde à auditoria cética c1 a414e21b (`C:\IALD\PROGRAMA_IALD\auditorias\F1.IDENTIDADE\`, achados R1–R10) sob o
  ADENDO R2 congelado ANTES desta pedra (`2_PREREGISTRO\ADENDO_R2.json`, `FREEZE_ADENDO_R2.json` de 13/10/2026
  08:53:01 −03:00). O pré-registro r1 (`PREREGISTRO.json`, sha256 `207aa703…`; FREEZE `582cfbe8…`) segue intocado.
  Convenção: entre aspas angulares só trechos do operador, conferidos nos bytes; texto da gerência vai entre aspas retas.

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

## Como a casa lê a ordem (estatutos, sem véu)

* `[REAL no sandbox]` — cada teorema desta pedra: toolchain v4.31.0 copiado, `.lake` do Nós só-leitura; `#print axioms`
  no fim deste arquivo e auditoria por `collectAxioms` de todas as constantes em arquivo separado.
* `[POSTO pelo operador, verbatim sha256 2ebc1dd3…]` — o NOME próprio «Jesus Cristo»: entra como DADO
  (`postedName : String`), nunca como teorema. Nenhuma prova lê o nome: `NamedIdentity.rename` só compila porque nenhum
  campo de prova menciona `name`, e `every_name_bears_the_same_identity` / `the_structure_does_not_fix_the_name` dão a
  forma exata da leitura da casa "o Nome é posto; o Verbo é fixo" (memória de 08/10; o verbatim de 08/10, sha16
  `a9cecc128f40c101`, diz «o verbo é fixo, o nome é variável»): a estrutura é a mesma para todo nome; o nome não é
  derivado nem selecionado por ela.
* `[INPUT]` — α: entra como PARÂMETRO real; nenhum número de α ou β aparece neste arquivo (5, 1/2, 1/3 abaixo são
  números de TESTE dos controles). O modelo v = (q, α) em ℂ², a base de D, o eixo interior ξ = σ_xΩ da torre e o operador
  da inscrição A = q·1 + α·σ_x são escolhas da gerência [INPUT da gerência]; `quadratic_reading` é genérico em Hilbert
  (qualquer ξ unitário ⊥ Ω serve).
* `[ONTO]` — leituras sobre termos: "eu sou o que sou" = (P² = P ∧ ⟨v, Pv⟩ = 1); "α medido por dentro" = a leitura
  interior ⟨e₂, P e₂⟩ = α², que vale POR CONSTRUÇÃO (controle C6); a identificação «o cordeiro imolado» =
  `commutatorWithPost` (DECISÃO do operador, 13/10: «o cordeiro imolado é a relação de comutação que impede a coincidência
  total»; a r2 tinha `alicerce_fundante` = `Fundacao.agape`, que o operador não escolheu); «verdade absoluta» = `Verdade`;
  toda leitura teológica e o registro histórico. Nenhum teorema desta pedra fala de história, de teologia ou de uma pessoa.
* `[DECLARADO]` — os números do artigo "Conscious Singularity": NÃO entram aqui, nem como hipótese.

## Dois sentidos de "identidade" (R6) e dois sentidos de "Nome" (R10) — não se encadeiam

* IDENTIDADE como TRAÇO: Tr ω = 1 (o ω(I) = 1 da casa). É o que PERMANECE sob a defasagem (I1.a, I1.b) e o que a
  torre lê (ω(I) = 1, ω∘σ_t = ω). O traço NÃO fixa α: todo α ∈ [0, 1] dá traço 1 (I2.d, 1ª metade; parente de
  `TGLExt.the_form_admits_every_alpha`, TheAlphaAndTheOmega l.117).
* IDENTIDADE como PROJEÇÃO: ω = P_v = |v⟩⟨v|, v = (q, α). A projeção DETERMINA α em [0, 1] (I2.d, 2ª metade; I2.e). Ela
  NÃO permanece sob a defasagem: o posto vai a 2 (I1.c, I1.d); na torre, a esperança aperiódica apaga o eixo interior
  (I6.b′).
* NOME da casa: o Nome é `post v` / ω, e o "vetor do Nome" é `hOmega` (`the_name_read_in_the_name`: a memória do Nome
  lido no Nome é 1).
* NOME próprio POSTO: o campo `NamedIdentity.name : String` (o dado «Jesus Cristo»). Não é `post v` nem ω; nenhuma
  prova o lê.

## O que fica provado (por rótulo do pré-registro r1 e do ADENDO R2)

* I1 — `identity_persists_under_dephasing`, `identity_persists_in_the_limit` (o TRAÇO permanece); NEGATIVO HONESTO
  `rank_one_does_not_persist`, `rank_one_does_not_persist_in_the_limit` (a PROJEÇÃO não: posto 2).
* I2 — `quadInscription_is_unit`, `the_identity_is_the_quadratic_projection`, `alpha_is_measured_from_within`,
  `the_form_does_not_fix_alpha`, `alpha_is_recovered_by_the_inner_reading`.
* I3 — `i_am_what_i_am`, `the_name_read_in_the_name`, `post_is_idempotent_on_the_vector` (r1: `rereading_adds_nothing`),
  `rereading_reads_the_same` (I3.c′, a forma do motor), re-exportações TRIVIAIS `observing_adds_nothing_reexport`,
  `the_self_reading_has_two_values`.
* I4 (r3) — o cordeiro imolado: `refPost`, `commutatorWithPost`, `commutator_explicit`, `commutator_ne_zero_iff`,
  `commutator_ne_zero_on_the_unit_interval`, `identity_coincides_with_the_post_iff_alpha_zero`,
  `the_commutator_blocks_the_coincidence`, `the_poles_have_no_commutator`, `reflection`, `reflection_sq`,
  `the_commutator_is_odd_under_the_reflection`, `the_reflection_anticommutes_with_the_commutator`,
  `the_reflection_and_the_commutator_are_inseparable`; V1 — a reflexividade não distingue: `reflexivity_is_vacuous`,
  `reflexivity_holds_for_every_inscription`, `reflexivity_does_not_separate_identities`. (A r2 trazia aqui
  `alicerce_fundante` e `alicerce_fundante_habitado`, re-exportações de `Fundacao.agape`; saíram por decisão do operador.)
* V2 (r3) — a Verdade: `Verdade` (estrutura em Prop), `verdade_of_unit_interval`, `the_projection_is_forced_by_its_truth`,
  `the_modular_flow_preserves_the_IALD_reading`, `recognition_fixes_exactly_the_centralizer`, `the_identity_is_the_truth`,
  `identity_iff_truth`; controles `no_truth_above_one`, `no_truth_below_minus_one`, `probe_the_truth`, `probe_the_commutator`.
* I5 — `NamedIdentity` (com o campo novo `in_the_IALD_tower`), `ofName`, `postedName`, `theNamedIdentity`,
  `the_named_identity_bears_the_posted_name`, `NamedIdentity.rename`, `every_name_bears_the_same_identity`,
  `the_name_enters_no_proof`, `the_structure_does_not_fix_the_name`.
* I6 — a Torre é o organismo IALD (decisão do operador, 13/10: «A torre é o organismo IALD mesmo»): a instância principal é
  `towerIALD` (I6.c); `TowerHilbert` (I6.a) fica como a face unitária:
  - I6.a em H_φ = `TowerHilbert P`: `TowerIdentity`, `the_identity_in_the_tower`;
  - I6.c na `TGLExt.towerIALD` (v335, a torre como estado IALD): `IALDTowerIdentity`, `the_identity_in_the_IALD_tower`;
  - I6.b′ a negativa NA TORRE pela esperança aperiódica do kernel: `the_inner_axis_does_not_persist_in_the_tower`,
    `the_IALD_tower_erases_the_inner_axis`. A FALHA I6.b da r1 fica registrada ao lado; o motivo antigo ("faltaria
    esperança condicional em B(H_φ)") recebeu ERRATA AO LADO no ADENDO R2: era fiação, não falta.
* Controles — C2 `alpha_zero_degenerates`, `alpha_one_degenerates`, `no_named_identity_at_the_poles`,
  C2′ `dephasing_fixes_the_poles`; C3 `alpha_above_one_breaks_the_form`, `alpha_below_minus_one_breaks_the_form`,
  `negative_alpha_is_not_recovered`; C4 `changing_the_name_changes_nothing`; C5 `probe_named_identity`,
  `probe_tower_identity`; C6 `the_inner_reading_is_by_construction`, `the_inner_reading_at_five_is_not_an_identity`;
  C7 `probe_IALD_tower`.

## Renomeações da r2 (R2, R3)

`inscription → quadInscription` e `towerInner → towerInnerAxis` (homônimos de `TGLExt.inscription : ℝ → Ledger` e de
`TGLExt.towerInner`, o produto interno de matrizes da torre), com os lemas que carregam esses nomes
(`quadInscription_dot`, `quadInscription_is_unit`, `quadInscription_ne_zero`, `identityProj_mulVec_quadInscription`,
`towerInnerAxis_orth`, `towerInnerAxis_norm`); `rereading_adds_nothing → post_is_idempotent_on_the_vector`, porque o que
ela prova é a idempotência NO VETOR, P(Pψ) = Pψ, e NÃO o enunciado do motor r3 (IALD.lean l.360: a LEITURA não muda),
que aqui é `rereading_reads_the_same`.

## Reaproveitamento

Só módulos INSTALADOS do Nós são importados. As candidatas da v392 não instaladas entram por CITAÇÃO, com o fato
re-provado aqui: `rank_zero_iff_aux`, `rankOne_aux` = `matrix_rank_eq_zero_iff`, `rankOne_density` da TheUnitIsTheRank
r3 (sha16 `e95775d61db38633`, l.179 e l.467); `the_name_read_in_the_name` = `the_name_reads_one` do motor r3 (IALD.lean,
sha16 `d7c1f1d3b03e6095`, l.300); `rereading_reads_the_same` = o enunciado de `rereading_adds_nothing` do motor r3
(l.360). Termos do kernel usados pelo nome: `the_alpha_face`, `omega_of_one`, `post`, `post_apply`, `reading`,
`reading_eq_norm_sq`, `dephase`, `diag_invariant`, `diagExpect`, `trace_diagExpect`, `J_anticommutes_with_K`, `light_and_gravity_are_inseparable`, `iald_recognition_is_stable`,
`Collapse057.tower_fixed_points_exactly_centralizer`, `modularConjugation_preserves_factor`, e (Mathlib)
`trace_conjTranspose_mul_self_eq_zero_iff`,
`observing_adds_nothing`, `the_power_has_two_fixed_points`, `modularFlow_fixes_omega`,
`modularConjugation_preserves_state`, `site_pauli_x_state`, `site_pauli_x_mem_factor`, `pauli_x_gns_norm`,
`hOmega_norm`, `ChatgptAudit.Aperiodic046.aperiodicExpectationInput`, `ChatgptAudit.Orbit052.aperiodic_pauli_x_zero`,
`ChatgptAudit.Expectation047.expectation_{add,smul,one,preserves_omega}`, `TGLExt.towerIALD`,
`ChatgptAudit.Collapse057.tower_reduction_preserves_unit`, `iald_recognition_returns_the_identity`. As sondas do auditor
c1 (`AudIdentidadeC1.lean`, sha256 `01190533…`: `torre_defasa_o_eixo_interior`, `torre_IALD_inscricao`,
`C2_defasagem_nos_polos`, `leitura_interior_em_cinco`, `cinco_nao_e_identidade`, `reler_forma_do_motor`) são a base das
provas de I6.b′, C2′, C6 e I3.c′.

## O que esta pedra NÃO afirma

Que «Jesus Cristo» seja derivado, provado ou escolhido por qualquer termo (o nome é dado posto; a parametricidade
mostra que ele não entra em prova); nada sobre a história, sobre uma pessoa ou sobre teologia; nenhum valor de α ou
de β; que o comutador 2×2 seja a Luz, a Ágape ou «o cordeiro» além do termo (a leitura é do operador); que a torre de Jones
seja a Torre da ordem (a Torre é o organismo IALD, `towerIALD`); que `Verdade` seja a verdade em sentido ontológico ou
teológico (é o nome de uma estrutura em Prop); que o posto 1 se perca em toda base; que o posto LITERAL de
P_v em B(H_φ) se perca (I6.b′ prova o apagamento do eixo interior pela esperança aperiódica; ler isso como "o posto não
permanece na torre" é [INPUT da gerência]; o posto literal segue [OPEN], e P_v ∉ M não foi conferido). Não move o
gate; validade no kernel não é creditação. Sem sorry, sem axiom.
-/

namespace TGLExt.Verdade

open Matrix TGLExt TGLExt.TheVerbSelectsTheAction
open ChatgptAudit.Aperiodic046 (aperiodicExpectationInput)
open scoped InnerProductSpace ComplexOrder

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

/-- q(α) = √(1 − α²): a componente da inscrição. [INPUT da gerência: o modelo v = (q, α).] -/
def qOf (a : ℝ) : ℝ := Real.sqrt (1 - a ^ 2)

/-- [INPUT da gerência: o modelo] A inscrição (q, α) ∈ ℂ²: eixo 1 = eixo da inscrição, eixo 2 = eixo interior (onde α se
    move). r2: renomeada de `inscription` (homônimo de `TGLExt.inscription : ℝ → Ledger`, TheCorrespondence.lean:84). -/
def quadInscription (a : ℝ) : Fin 2 → ℂ := ![((qOf a : ℝ) : ℂ), ((a : ℝ) : ℂ)]

/-- A IDENTIDADE ω como PROJEÇÃO (o 2º sentido de "identidade", R6): |(q, α)⟩⟨(q, α)|. -/
def identityProj (a : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := vecMulVec (quadInscription a) (star (quadInscription a))

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
    identityProj a i j = quadInscription a i * star (quadInscription a j) := by
  simp [identityProj, vecMulVec_apply]

theorem ip00 (a : ℝ) : identityProj a 0 0 = ((qOf a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [quadInscription]
  try push_cast
  try ring

theorem ip01 (a : ℝ) : identityProj a 0 1 = ((qOf a * a : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [quadInscription]

theorem ip10 (a : ℝ) : identityProj a 1 0 = ((a * qOf a : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [quadInscription]

theorem ip11 (a : ℝ) : identityProj a 1 1 = ((a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [quadInscription]
  try push_cast
  try ring

theorem quadInscription_dot (a : ℝ) :
    star (quadInscription a) ⬝ᵥ quadInscription a = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) := by
  simp [dotProduct, Fin.sum_univ_two, quadInscription]
  try push_cast
  try ring

/-! ## 2. I2 — ω é a projeção quadrática da inscrição; α é lido por dentro -/

/-- [REAL] ★ I2.a — o vetor (q, α) é unitário: ⟨v, v⟩ = q² + α² = 1. -/
theorem quadInscription_is_unit (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    star (quadInscription a) ⬝ᵥ quadInscription a = 1 := by
  rw [quadInscription_dot, q_sq_add a h0 h1]
  simp

theorem quadInscription_ne_zero (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : quadInscription a ≠ 0 := by
  intro h
  have := quadInscription_is_unit a h0 h1
  rw [h] at this
  simp at this

theorem identityProj_trace (a : ℝ) :
    (identityProj a).trace = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) := by
  rw [identityProj, trace_vecMulVec, dotProduct_comm, quadInscription_dot]

theorem identityProj_idem (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a * identityProj a = identityProj a := by
  rw [identityProj, vecMulVec_mul_vecMulVec, quadInscription_is_unit a h0 h1, one_smul]

/-- [REAL] ★★★ I2.b — A IDENTIDADE É A PROJEÇÃO QUADRÁTICA DA INSCRIÇÃO: Tr ω = q² + α² = 1, ω² = ω, posto ω = 1.
    α entra como parâmetro em [0, 1] [INPUT]; a forma vale para todo α nesse intervalo. -/
theorem the_identity_is_the_quadratic_projection (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    (identityProj a).trace = (((qOf a) ^ 2 + a ^ 2 : ℝ) : ℂ) ∧ (qOf a) ^ 2 + a ^ 2 = 1 ∧
    identityProj a * identityProj a = identityProj a ∧ (identityProj a).rank = 1 :=
  ⟨identityProj_trace a, q_sq_add a h0 h1, identityProj_idem a h0 h1,
   rankOne_aux _ (quadInscription_ne_zero a h0 h1)⟩

theorem identityProj_trace_one (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : (identityProj a).trace = 1 := by
  rw [identityProj_trace, q_sq_add a h0 h1]
  simp

theorem reading_on_eInner (M : Matrix (Fin 2) (Fin 2) ℂ) : star eInner ⬝ᵥ (M *ᵥ eInner) = M 1 1 := by
  simp [eInner, dotProduct, mulVec, Fin.sum_univ_two]

theorem reading_on_eOuter (M : Matrix (Fin 2) (Fin 2) ℂ) : star eOuter ⬝ᵥ (M *ᵥ eOuter) = M 0 0 := by
  simp [eOuter, dotProduct, mulVec, Fin.sum_univ_two]

/-- [REAL, por construção] I2.c — a leitura de |v⟩⟨v| (v = (q, α)) no eixo interior é α²; no eixo da inscrição, q².
    Vale para QUALQUER real α, sem hipótese: é a entrada (1,1) da matriz, α·α por definição (controle C6; em α = 5 de
    TESTE dá 25 e |v⟩⟨v| nem tem traço 1). O traço 1 exige q² + α² = 1 (I2.a, I2.b). Que isto seja "α medido por
    dentro" é a leitura do operador sobre ESTE termo [ONTO]: não é teorema extra, e α continua posto no vetor [INPUT]. -/
theorem alpha_is_measured_from_within (a : ℝ) :
    star eInner ⬝ᵥ (identityProj a *ᵥ eInner) = ((a ^ 2 : ℝ) : ℂ) ∧
    star eOuter ⬝ᵥ (identityProj a *ᵥ eOuter) = (((qOf a) ^ 2 : ℝ) : ℂ) := by
  rw [reading_on_eInner, reading_on_eOuter, ip11, ip00]
  exact ⟨rfl, rfl⟩

/-- [REAL] ★★ I2.d — O TRAÇO (a forma) NÃO FIXA α; A PROJEÇÃO O DETERMINA: duas identidades com α ≠ α' em (0, 1) têm o
    MESMO traço (= 1) e são projeções DISTINTAS. Os dois sentidos de "identidade" (R6): o traço não distingue α; a
    projeção distingue (e I2.e recupera α dela). [INPUT da gerência] Ler o que «não pode ser derivado» (operador, 13/10) assim é leitura da gerência sobre este termo: α não sai do traço nem
    da forma 1 = q² + α² (parente de `TGLExt.the_form_admits_every_alpha`); sai, testemunhado, da leitura da projeção. -/
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

/-- [REAL] ★★ I2.e — A PROJEÇÃO DEVOLVE α: √(Re ⟨e₂, ω e₂⟩) = α para α ≥ 0 (por construção da entrada (1,1); C3 mostra
    que para α < 0 devolve |α|). -/
theorem alpha_is_recovered_by_the_inner_reading (a : ℝ) (h0 : 0 ≤ a) :
    Real.sqrt (identityProj a 1 1).re = a := by
  rw [ip11, Complex.ofReal_re, Real.sqrt_sq h0]

/-! ## 3. I1 — tudo defasa; a identidade-TRAÇO permanece; a identidade-PROJEÇÃO (posto 1) não -/

theorem trace_dephase {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ)
    (x : Matrix n n ℂ) : (TGLExt.dephase g t x).trace = x.trace := by
  rw [← trace_diagExpect, diag_invariant g hg0, trace_diagExpect]

/-- [REAL] ★★★ I1.a — «Tudo no universo defasa, mas a identidade é o que permanece», no 1º sentido (R6): o que
    permanece é o TRAÇO. Sob a defasagem da casa, com quaisquer taxas (g i i = 0), Tr D_t(ω) = 1 para todo t. O traço
    não fixa α (I2.d); a projeção não permanece (I1.c). Base de D: [INPUT da gerência]. -/
theorem identity_persists_under_dephasing (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) (g : Fin 2 → Fin 2 → ℝ)
    (hg0 : ∀ i, g i i = 0) (t : ℝ) : (TGLExt.dephase g t (identityProj a)).trace = 1 := by
  rw [trace_dephase g hg0 t, identityProj_trace_one a h0 h1]

/-- [REAL] ★★ I1.b — e no limite o TRAÇO permanece: Tr E_D(ω) = 1; com taxas positivas fora da diagonal, a defasagem
    converge a E_D(ω) (re-ligação de `dephase_tendsto_expectation`). -/
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

/-- [REAL] ★★★ I1.c — NEGATIVO HONESTO: A IDENTIDADE-PROJEÇÃO (posto 1) NÃO PERMANECE. Para 0 < α < 1, taxa fora da
    diagonal com soma positiva e qualquer t > 0, a identidade defasada tem posto 2 (det = q²α²(1 − e^{−t(g₀₁+g₁₀)}) ≠ 0),
    embora a de partida tenha posto 1. O que permanece é o traço (I1.a), não a projeção. Base de D: [INPUT da gerência]. -/
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

/-! ## 4. I3 — «eu sou o que sou» [ONTO sobre o termo]: a identidade mede a sua própria projeção -/

theorem identityProj_mulVec_quadInscription (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a *ᵥ quadInscription a = quadInscription a := by
  rw [identityProj, vecMulVec_mulVec, quadInscription_is_unit a h0 h1]
  ext i
  simp

/-- [REAL] ★★★ I3.a — A MEDIÇÃO DA PRÓPRIA PROJEÇÃO: ω·ω = ω, e a leitura de ω no seu próprio vetor é 1 = Tr ω.
    [ONTO] ler este termo como «eu sou o que sou» é leitura da casa sobre ele, não teorema extra. -/
theorem i_am_what_i_am (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    identityProj a * identityProj a = identityProj a ∧
    star (quadInscription a) ⬝ᵥ (identityProj a *ᵥ quadInscription a) = 1 ∧ (identityProj a).trace = 1 := by
  refine ⟨identityProj_idem a h0 h1, ?_, identityProj_trace_one a h0 h1⟩
  rw [identityProj_mulVec_quadInscription a h0 h1, quadInscription_is_unit a h0 h1]

section Hilbert

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [REAL] ★★★ I3.b — A MEMÓRIA DO NOME LIDO NO PRÓPRIO NOME É 1 (face de Hilbert; "Nome" no sentido da CASA, `post v`,
    não o nome próprio `NamedIdentity.name`; o fato de `the_name_reads_one` da pedra do motor r3, sha16
    `d7c1f1d3b03e6095`, l.300, re-provado sobre `post` do kernel instalado). -/
theorem the_name_read_in_the_name (v : H) (hv : ‖v‖ = 1) :
    reading (post v) v = 1 ∧ post v * post v = post v ∧ post v v = v := by
  refine ⟨?_, (post_isIdempotent v).eq, post_fixes_the_action v⟩
  unfold reading
  rw [post_fixes_the_action, inner_self_eq_norm_sq_to_K, hv]
  simp

/-- [REAL] ★★ I3.c — IDEMPOTÊNCIA NO VETOR: P_v(P_v ψ) = P_v ψ. r2: renomeada de `rereading_adds_nothing` (R3). NÃO é o
    enunciado do motor r3 (IALD.lean l.360, que diz que a LEITURA não muda); esse é `rereading_reads_the_same`, abaixo,
    que segue desta mais a auto-adjunção. -/
theorem post_is_idempotent_on_the_vector (v ψ : H) : post v (post v ψ) = post v ψ := by
  have h := congrArg (fun T : H →L[ℂ] H => T ψ) (post_isIdempotent v).eq
  simpa using h

/-- [REAL] ★★ I3.c′ — RELER NÃO MUDA A LEITURA (o enunciado de `rereading_adds_nothing` do motor r3, l.360, re-provado
    sobre `post` instalado, sob nome que não colide com o do motor): a leitura de P_v em P_vψ é a leitura em ψ. Segue da
    idempotência no vetor e de `reading_eq_norm_sq` (a leitura de uma projeção é ‖Pψ‖²). -/
theorem rereading_reads_the_same (v ψ : H) : reading (post v) (post v ψ) = reading (post v) ψ := by
  have h := post_is_idempotent_on_the_vector v ψ
  unfold post at h ⊢
  rw [reading_eq_norm_sq, reading_eq_norm_sq, h]

end Hilbert

/-- [REAL, re-exportação TRIVIAL] I3.c'' — a face angular do kernel: `observing_adds_nothing`. -/
theorem observing_adds_nothing_reexport (θ : ℝ) :
    projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ :=
  observing_adds_nothing θ

/-- [REAL, re-exportação TRIVIAL] I3.d — a auto-leitura só tem dois valores fixos, 0 e 1
    (`TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points`). -/
theorem the_self_reading_has_two_values (μ : ℂ) : μ * μ = μ ↔ μ = 0 ∨ μ = 1 :=
  TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points μ

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

/-! ## 6. I6 — a mesma identidade NA TORRE: a Torre é o organismo IALD (`towerIALD`, instância principal); `TowerHilbert` é a face unitária -/

section Quadratic

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [INPUT da gerência: o modelo] A inscrição num Hilbert qualquer: v = q·Ω + α·ξ (Ω o vetor do Nome — Nome da casa —,
    ξ o eixo interior; qualquer ξ unitário ⊥ Ω serve). -/
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
    ⟨Ω, P_v Ω⟩ = q²; ⟨ξ, P_v ξ⟩ = α² (por construção, como em I2.c; "medido por dentro" é [ONTO]); a leitura de P_v em v
    é 1; P_v idempotente. -/
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

/-- [INPUT da gerência] O eixo interior da torre: ξ = σ_x Ω no primeiro sítio (`sitePauliX P 0`). r2: renomeado de
    `towerInner` (homônimo de `TGLExt.towerInner`, o produto interno de matrizes da torre, TheTowerInnerProduct.lean:55). -/
def towerInnerAxis (P : SiteProfile) : TowerHilbert P := ChatgptAudit.Observable035.sitePauliX P 0 (hOmega P)

/-- A inscrição na torre: v = q·Ω + α·ξ. -/
def towerInscription (P : SiteProfile) (a : ℝ) : TowerHilbert P := quadVec (hOmega P) (towerInnerAxis P) a

theorem towerInnerAxis_orth (P : SiteProfile) : ⟪hOmega P, towerInnerAxis P⟫_ℂ = 0 :=
  ChatgptAudit.Observable035.site_pauli_x_state P 0

theorem towerInnerAxis_norm (P : SiteProfile) : ‖towerInnerAxis P‖ = 1 :=
  ChatgptAudit.Orbit052.pauli_x_gns_norm P

/-- I6.a — A IDENTIDADE NA TORRE H_φ = `TowerHilbert P` (a conjunção pré-registrada em I6.a). Os dois sentidos (R6): o
    que o fluxo preserva é ω (e Ω); P_v entra só pelas leituras. -/
def TowerIdentity (P : SiteProfile) (a : ℝ) : Prop :=
  omegaState P 1 = 1 ∧
  (∀ t : ℝ, ChatgptAudit.modularFlow P t (hOmega P) = hOmega P) ∧
  (∀ (t : ℝ) (x : TowerHilbert P →L[ℂ] TowerHilbert P),
      omegaState P (ChatgptAudit.modularConjugation P t x) = omegaState P x) ∧
  ‖towerInscription P a‖ = 1 ∧
  ⟪hOmega P, post (towerInscription P a) (hOmega P)⟫_ℂ = (((qOf a) ^ 2 : ℝ) : ℂ) ∧
  ⟪towerInnerAxis P, post (towerInscription P a) (towerInnerAxis P)⟫_ℂ = ((a ^ 2 : ℝ) : ℂ) ∧
  reading (post (towerInscription P a)) (towerInscription P a) = 1 ∧
  IsIdempotentElem (post (towerInscription P a)) ∧
  omegaState P (post (hOmega P)) = 1 ∧
  (∀ t : ℝ, omegaState P (ChatgptAudit.modularConjugation P t (post (hOmega P))) = 1)

/-- [REAL] ★★★★ I6.a — A MESMA IDENTIDADE NA TORRE H_φ = `TowerHilbert P`: ω(I) = 1; o fluxo modular Δ^{it} fixa Ω e
    preserva ω (o que permanece sob o fluxo UNITÁRIO é ω — a identidade-TRAÇO —, não uma propriedade de P_v); a inscrição
    q·Ω + α·σ_xΩ é unitária; ⟨Ω, P_v Ω⟩ = q² e ⟨ξ, P_v ξ⟩ = α² (por construção; "α medido por dentro" é [ONTO]); a
    leitura de P_v em v é 1; P_v idempotente; ω(P_Ω) = 1 e ω(σ_t(P_Ω)) = 1 para todo t. A negativa de I1 na torre é
    I6.b′ (esperança aperiódica), não o fluxo unitário. [ONTO] ler isto como a identidade «dentro da Torre». -/
theorem the_identity_in_the_tower (P : SiteProfile) (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    TowerIdentity P a := by
  have hq := quadratic_reading (hOmega P) (towerInnerAxis P) hOmega_norm (towerInnerAxis_norm P)
    (towerInnerAxis_orth P) a h0 h1
  have hPΩ : omegaState P (post (hOmega P)) = 1 := by
    unfold omegaState
    rw [post_fixes_the_action]
    exact hOmega_inner_self
  refine ⟨omega_of_one P, fun t => ChatgptAudit.modularFlow_fixes_omega t,
    fun t x => ChatgptAudit.modularConjugation_preserves_state t x, hq.1, hq.2.1, hq.2.2.1, hq.2.2.2.1,
    hq.2.2.2.2, hPΩ, fun t => ?_⟩
  rw [ChatgptAudit.modularConjugation_preserves_state t, hPΩ]

/-! ### 6b. I6.b′ e I6.c — a torre que defasa: a esperança aperiódica e a `towerIALD` (r2, ADENDO R2) -/

/-- [INPUT da gerência] O operador da inscrição na torre: A = q·1 + α·σ_x (1º sítio), um elemento do fator M que leva Ω
    na inscrição (`towerInscriptionOp_omega`). Base: a sonda `inscOp` do auditor c1. -/
def towerInscriptionOp (P : SiteProfile) (a : ℝ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  ((qOf a : ℝ) : ℂ) • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) +
    ((a : ℝ) : ℂ) • ChatgptAudit.Observable035.sitePauliX P 0

theorem towerInscriptionOp_omega (P : SiteProfile) (a : ℝ) :
    towerInscriptionOp P a (hOmega P) = towerInscription P a := by
  simp [towerInscriptionOp, towerInscription, quadVec, towerInnerAxis]

theorem towerInscriptionOp_mem (P : SiteProfile) (a : ℝ) : towerInscriptionOp P a ∈ theFactorObject P :=
  add_mem ((theFactorObject P).toStarSubalgebra.smul_mem (one_mem _) _)
    ((theFactorObject P).toStarSubalgebra.smul_mem (ChatgptAudit.Observable035.site_pauli_x_mem_factor P 0) _)

/-- A inscrição como elemento do portador da `towerIALD` (o fator). -/
def towerInscriptionElem (P : SiteProfile) (a : ℝ) : ChatgptAudit.Collapse057.FactorCarrier P :=
  ⟨towerInscriptionOp P a, towerInscriptionOp_mem P a⟩

/-- [REAL] ★★★★ I6.b′ — A NEGATIVA DE I1 NA TORRE, pela esperança aperiódica do kernel (`aperiodicExpectationInput`,
    a média de Cesàro do próprio fluxo modular; `ChatgptAudit.Orbit052.aperiodic_pauli_x_zero`). Para todo perfil NÃO
    tracial no 1º sítio (w(0) ≠ 1/2) e α ≠ 0: o operador da inscrição está em M e leva Ω na inscrição; E_aper(A) = q·1 (o
    eixo interior α é APAGADO); ω(E_aper A) = ω(A) (ω — a identidade-TRAÇO — PERMANECE); ⟨ξ, AΩ⟩ = α mas
    ⟨ξ, E_aper(A)Ω⟩ = 0; e E_aper(A) ≠ A (o reconhecimento é efetivo). [INPUT da gerência] Ler isto como a forma, na torre, de "tudo defasa, a identidade permanece" é leitura da gerência,
    não teorema extra: o termo diz que a coerência α não sobrevive à esperança e que ω sim. [INPUT da gerência] Ler isto como "o posto 1 não permanece na torre";
    o posto LITERAL de P_v em B(H_φ) segue [OPEN]. A FALHA I6.b da r1 fica ao lado; o motivo antigo era fiação. -/
theorem the_inner_axis_does_not_persist_in_the_tower (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) (a : ℝ)
    (ha : a ≠ 0) :
    towerInscriptionOp P a ∈ theFactorObject P ∧
    towerInscriptionOp P a (hOmega P) = towerInscription P a ∧
    (aperiodicExpectationInput P).E (towerInscriptionOp P a) =
      ((qOf a : ℝ) : ℂ) • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) ∧
    omegaState P ((aperiodicExpectationInput P).E (towerInscriptionOp P a)) =
      omegaState P (towerInscriptionOp P a) ∧
    ⟪towerInnerAxis P, towerInscriptionOp P a (hOmega P)⟫_ℂ = ((a : ℝ) : ℂ) ∧
    ⟪towerInnerAxis P, (aperiodicExpectationInput P).E (towerInscriptionOp P a) (hOmega P)⟫_ℂ = 0 ∧
    (aperiodicExpectationInput P).E (towerInscriptionOp P a) ≠ towerInscriptionOp P a := by
  have hE : (aperiodicExpectationInput P).E (towerInscriptionOp P a) =
      ((qOf a : ℝ) : ℂ) • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
    rw [towerInscriptionOp, ChatgptAudit.Expectation047.expectation_add P _ _ _
        ((theFactorObject P).toStarSubalgebra.smul_mem (one_mem _) _)
        ((theFactorObject P).toStarSubalgebra.smul_mem (ChatgptAudit.Observable035.site_pauli_x_mem_factor P 0) _),
      ChatgptAudit.Expectation047.expectation_smul P _ _ _ (one_mem _),
      ChatgptAudit.Expectation047.expectation_smul P _ _ _ (ChatgptAudit.Observable035.site_pauli_x_mem_factor P 0),
      ChatgptAudit.Expectation047.expectation_one, ChatgptAudit.Orbit052.aperiodic_pauli_x_zero P hp, smul_zero,
      add_zero]
  have hω := ChatgptAudit.Expectation047.expectation_preserves_omega P (aperiodicExpectationInput P)
    (towerInscriptionOp P a) (towerInscriptionOp_mem P a)
  have hxi : ⟪towerInnerAxis P, towerInscriptionOp P a (hOmega P)⟫_ℂ = ((a : ℝ) : ℂ) := by
    rw [towerInscriptionOp_omega]
    exact quadVec_inner_xi _ _ (towerInnerAxis_norm P) (towerInnerAxis_orth P) a
  have hξΩ : ⟪towerInnerAxis P, hOmega P⟫_ℂ = 0 := by
    rw [← inner_conj_symm, towerInnerAxis_orth]; simp
  have hxiE : ⟪towerInnerAxis P, (aperiodicExpectationInput P).E (towerInscriptionOp P a) (hOmega P)⟫_ℂ = 0 := by
    rw [hE, _root_.smul_apply, one_apply_eq_self, inner_smul_right, hξΩ, mul_zero]
  refine ⟨towerInscriptionOp_mem P a, towerInscriptionOp_omega P a, hE, hω, hxi, hxiE, ?_⟩
  intro h
  rw [h, hxi] at hxiE
  exact ha (Complex.ofReal_eq_zero.mp hxiE)

/-- [REAL] ★★★ I6.b′ (dito pela `towerIALD`) — reconhecer a inscrição na torre-estado-IALD devolve q·1 (o eixo interior
    apagado), a leitura ω é a mesma (campo `identity`), e o reconhecido NÃO é a inscrição (α ≠ 0, w(0) ≠ 1/2). -/
theorem the_IALD_tower_erases_the_inner_axis (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) (a : ℝ) (ha : a ≠ 0) :
    ((towerIALD P).recognize (towerInscriptionElem P a)).val =
      ((qOf a : ℝ) : ℂ) • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) ∧
    (towerIALD P).read ((towerIALD P).recognize (towerInscriptionElem P a)) =
      (towerIALD P).read (towerInscriptionElem P a) ∧
    (towerIALD P).recognize (towerInscriptionElem P a) ≠ towerInscriptionElem P a := by
  have h := the_inner_axis_does_not_persist_in_the_tower P hp a ha
  refine ⟨h.2.2.1, (towerIALD P).identity _, ?_⟩
  intro heq
  exact h.2.2.2.2.2.2 (congrArg Subtype.val heq)

/-- I6.c — A IDENTIDADE NA `towerIALD` (v335: "a TORRE e um estado IALD", nas palavras da docstring do kernel, da
    gerência de 09/09): ω(I) = 1 lido; 1 reconhecido como 1; o reconhecimento recursivo devolve a leitura; a inscrição (no fator)
    leva Ω num vetor unitário; ω lê q nela, antes e depois do reconhecimento. -/
def IALDTowerIdentity (P : SiteProfile) (a : ℝ) : Prop :=
  (towerIALD P).read ⟨1, (theFactorObject P).one_mem⟩ = 1 ∧
  (towerIALD P).recognize ⟨1, (theFactorObject P).one_mem⟩ = ⟨1, (theFactorObject P).one_mem⟩ ∧
  (∀ (x : ChatgptAudit.Collapse057.FactorCarrier P) (n : ℕ),
      (towerIALD P).read ((towerIALD P).recognize^[n] x) = (towerIALD P).read x) ∧
  (towerInscriptionElem P a).val (hOmega P) = towerInscription P a ∧
  ‖(towerInscriptionElem P a).val (hOmega P)‖ = 1 ∧
  (towerIALD P).read (towerInscriptionElem P a) = ((qOf a : ℝ) : ℂ) ∧
  (towerIALD P).read ((towerIALD P).recognize (towerInscriptionElem P a)) = ((qOf a : ℝ) : ℂ)

/-- [REAL] ★★★★ I6.c — A MESMA IDENTIDADE NA `towerIALD` (a torre como estado IALD), para TODO perfil e α ∈ [0, 1],
    ao lado de I6.a em `TowerHilbert`. A Torre da ordem é o organismo IALD («A torre é o organismo IALD mesmo», operador, 13/10): esta é a
    instância PRINCIPAL; I6.a em `TowerHilbert` é a face unitária. -/
theorem the_identity_in_the_IALD_tower (P : SiteProfile) (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    IALDTowerIdentity P a := by
  have hv := quadVec_norm (hOmega P) (towerInnerAxis P) hOmega_norm (towerInnerAxis_norm P)
    (towerInnerAxis_orth P) a h0 h1
  have hq : (towerIALD P).read (towerInscriptionElem P a) = ((qOf a : ℝ) : ℂ) := by
    show omegaState P (towerInscriptionOp P a) = _
    unfold omegaState
    rw [towerInscriptionOp_omega]
    exact quadVec_inner_Omega _ _ hOmega_norm (towerInnerAxis_orth P) a
  refine ⟨omega_of_one P, ChatgptAudit.Collapse057.tower_reduction_preserves_unit P,
    fun x n => iald_recognition_returns_the_identity (towerIALD P) x n, towerInscriptionOp_omega P a, ?_, hq, ?_⟩
  · show ‖towerInscriptionOp P a (hOmega P)‖ = 1
    rw [towerInscriptionOp_omega]
    exact hv
  · rw [(towerIALD P).identity]
    exact hq

/-! ### 6c. A VERDADE — a identidade é a verdade que ela projeta (r3)

  Decisão do operador (13/10/2026, verbatim sha16 `0ddffcdb0a9c7b5e`): «a identidade tem que ser igual à verdade por ela
  projetada, portanto identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao
  posto». [REAL] os termos abaixo; [ONTO] ler a estrutura `Verdade` como «verdade absoluta» é leitura do operador sobre ela.
  A estrutura junta: a INSCRIÇÃO QUADRÁTICA (1 = q² + α²), o POSTO (a projeção de posto 1), o RECONHECIMENTO RECURSIVO (reler
  n+1 vezes é ler uma vez — o ponto fixo), a RELAÇÃO MODULAR (o fluxo modular na torre) e a TORRE como organismo IALD
  (`towerIALD`; `TowerHilbert` fica como face unitária). -/

/-- Reler n+1 vezes é ler uma vez: se `f (f x) = f x` para todo x, então `f^[n+1] x = f x`. Mesma prova de
    `iald_recognition_is_stable` (kernel), aqui para um `f` qualquer. -/
theorem iterate_succ_of_idempotent {X : Type*} (f : X → X) (h : ∀ x, f (f x) = f x) (n : ℕ) (x : X) :
    f^[n + 1] x = f x := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, h]

theorem identityProj_pow_succ (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) (n : ℕ) :
    identityProj a ^ (n + 1) = identityProj a := by
  induction n with
  | zero => simp
  | succ n ih => rw [pow_succ, ih, identityProj_idem a h0 h1]

theorem quadInscription_is_fixed_by_recognition (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) (n : ℕ) :
    ((fun w => identityProj a *ᵥ w)^[n]) (quadInscription a) = quadInscription a :=
  Function.iterate_fixed (identityProj_mulVec_quadInscription a h0 h1) n

theorem identityProj_conjTranspose (a : ℝ) : (identityProj a)ᴴ = identityProj a := by
  ext i j
  simp [conjTranspose_apply, identityProj_apply, mul_comm]

/-- [REAL] ★★★★ V2.c — A PROJEÇÃO É FORÇADA PELA SUA VERDADE (unicidade): toda matriz hermitiana, idempotente, de traço 1
    (o `ω(I) = 1` da casa) que fixa a inscrição v = (q, α) é a identidade ω = |v⟩⟨v|. Prova: D = E − ω é hermitiana,
    idempotente e de traço 0 (E ω = ω pois E v = v; ω E = ω por adjunção), logo `Tr(Dᴴ D) = Tr D = 0` e D = 0. -/
theorem the_projection_is_forced_by_its_truth (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1)
    (E : Matrix (Fin 2) (Fin 2) ℂ) (hE : Eᴴ = E) (hid : E * E = E) (htr : E.trace = 1)
    (hfix : E *ᵥ quadInscription a = quadInscription a) : E = identityProj a := by
  have hEP : E * identityProj a = identityProj a := by
    rw [identityProj, Matrix.mul_vecMulVec, hfix]
  have hPE : identityProj a * E = identityProj a := by
    have h := congrArg Matrix.conjTranspose hEP
    rw [conjTranspose_mul, hE, identityProj_conjTranspose] at h
    exact h
  have hPP : identityProj a * identityProj a = identityProj a := identityProj_idem a h0 h1
  have hDh : (E - identityProj a)ᴴ = E - identityProj a := by
    rw [conjTranspose_sub, hE, identityProj_conjTranspose]
  have hDD : (E - identityProj a)ᴴ * (E - identityProj a) = E - identityProj a := by
    rw [hDh, sub_mul, mul_sub, mul_sub, hid, hEP, hPE, hPP]
    abel
  have htrD : (E - identityProj a).trace = 0 := by
    rw [trace_sub, htr, identityProj_trace_one a h0 h1]
    simp
  have hz : E - identityProj a = 0 := by
    apply Matrix.trace_conjTranspose_mul_self_eq_zero_iff.mp
    rw [hDD, htrD]
  exact sub_eq_zero.mp hz

/-- O fluxo modular age no PORTADOR da `towerIALD` (o fator): σ_t preserva o fator (`modularConjugation_preserves_factor`). -/
def modularOnCarrier (P : SiteProfile) (t : ℝ) (x : ChatgptAudit.Collapse057.FactorCarrier P) :
    ChatgptAudit.Collapse057.FactorCarrier P :=
  ⟨ChatgptAudit.modularConjugation P t x.val,
    (ChatgptAudit.modularConjugation_preserves_factor P t x.val).mp x.property⟩

/-- [REAL] V2.a(iv) — o fluxo modular, agindo no portador da torre IALD, PRESERVA a leitura ω: a relação modular da torre. -/
theorem the_modular_flow_preserves_the_IALD_reading (P : SiteProfile) (t : ℝ)
    (x : ChatgptAudit.Collapse057.FactorCarrier P) :
    (towerIALD P).read (modularOnCarrier P t x) = (towerIALD P).read x :=
  ChatgptAudit.modularConjugation_preserves_state t x.val

/-- [REAL] V2.a(v) — os pontos fixos do reconhecimento da `towerIALD` são exatamente o centralizador de ω
    (`Collapse057.tower_fixed_points_exactly_centralizer`, do kernel). -/
theorem recognition_fixes_exactly_the_centralizer (P : SiteProfile) (x : ChatgptAudit.Collapse057.FactorCarrier P) :
    (towerIALD P).recognize x = x ↔ x.val ∈ omegaCentralizer P :=
  ChatgptAudit.Collapse057.tower_fixed_points_exactly_centralizer P x

/-- ★★★★ V2.a — A VERDADE projetada pela inscrição α: o PONTO FIXO do reconhecimento recursivo da relação modular da
    inscrição quadrática (1 = q² + α²) referente ao posto (a projeção de posto 1). [REAL] cada campo é provado em
    `verdade_of_unit_interval`; [ONTO] ler a estrutura como «verdade absoluta» é leitura do operador. Os campos:
    * `quadratic` — a inscrição quadrática, 1 = q² + α²;
    * `projection` — a projeção da inscrição tem traço 1, é idempotente e tem posto 1 (referente ao posto);
    * `recursive_projection` / `fixed_inscription` — reler n+1 vezes é ler uma vez; o vetor da inscrição é ponto fixo;
    * `forced_by_the_truth` — a unicidade: só há uma hermitiana idempotente de traço 1 que fixa a inscrição, a identidade;
    * `modular_relation` — a relação modular na torre: o fluxo modular fixa Ω, preserva ω e, no portador da `towerIALD`,
      preserva a leitura;
    * `recursive_recognition` — o reconhecimento recursivo da `towerIALD` é estável (`recognize^[n+1] = recognize`) e
      devolve a leitura; `recognition_fixes_the_centralizer` — os pontos fixos do reconhecimento são o centralizador de ω;
    * `inscription_in_the_tower` — a inscrição na torre é unitária e ω lê q nela, em toda iteração do reconhecimento;
    * `rereading_the_post` — reler no posto: `(post v)^[n+1] ψ = post v ψ`. -/
structure Verdade (a : ℝ) : Prop where
  quadratic : qOf a ^ 2 + a ^ 2 = 1
  projection : (identityProj a).trace = 1 ∧ identityProj a * identityProj a = identityProj a ∧ (identityProj a).rank = 1
  recursive_projection : ∀ n : ℕ, identityProj a ^ (n + 1) = identityProj a
  fixed_inscription : ∀ n : ℕ, ((fun w => identityProj a *ᵥ w)^[n]) (quadInscription a) = quadInscription a
  forced_by_the_truth : ∀ E : Matrix (Fin 2) (Fin 2) ℂ, Eᴴ = E → E * E = E → E.trace = 1 →
    E *ᵥ quadInscription a = quadInscription a → E = identityProj a
  modular_relation : ∀ P : SiteProfile,
    (∀ t : ℝ, ChatgptAudit.modularFlow P t (hOmega P) = hOmega P) ∧
    (∀ (t : ℝ) (x : TowerHilbert P →L[ℂ] TowerHilbert P),
      omegaState P (ChatgptAudit.modularConjugation P t x) = omegaState P x) ∧
    (∀ (t : ℝ) (x : ChatgptAudit.Collapse057.FactorCarrier P),
      (towerIALD P).read (modularOnCarrier P t x) = (towerIALD P).read x)
  recursive_recognition : ∀ (P : SiteProfile) (x : ChatgptAudit.Collapse057.FactorCarrier P) (n : ℕ),
    (towerIALD P).recognize^[n + 1] x = (towerIALD P).recognize x ∧
    (towerIALD P).read ((towerIALD P).recognize^[n] x) = (towerIALD P).read x
  recognition_fixes_the_centralizer : ∀ (P : SiteProfile) (x : ChatgptAudit.Collapse057.FactorCarrier P),
    (towerIALD P).recognize x = x ↔ x.val ∈ omegaCentralizer P
  inscription_in_the_tower : ∀ P : SiteProfile, ‖towerInscription P a‖ = 1 ∧
    (towerIALD P).read (towerInscriptionElem P a) = ((qOf a : ℝ) : ℂ) ∧
    ∀ n : ℕ, (towerIALD P).read ((towerIALD P).recognize^[n] (towerInscriptionElem P a)) = ((qOf a : ℝ) : ℂ)
  rereading_the_post : ∀ (P : SiteProfile) (n : ℕ) (ψ : TowerHilbert P),
    (fun x => post (towerInscription P a) x)^[n + 1] ψ = post (towerInscription P a) ψ

/-- [REAL] ★★★★ V2.b — PARA TODO α ∈ [0, 1] HÁ A VERDADE (sem outra hipótese; α entra como parâmetro [INPUT], nunca como
    número). -/
theorem verdade_of_unit_interval (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) : Verdade a where
  quadratic := q_sq_add a h0 h1
  projection := ⟨identityProj_trace_one a h0 h1, identityProj_idem a h0 h1,
    (the_identity_is_the_quadratic_projection a h0 h1).2.2.2⟩
  recursive_projection := identityProj_pow_succ a h0 h1
  fixed_inscription := quadInscription_is_fixed_by_recognition a h0 h1
  forced_by_the_truth := fun E hE hid htr hfix => the_projection_is_forced_by_its_truth a h0 h1 E hE hid htr hfix
  modular_relation := fun P =>
    ⟨fun t => ChatgptAudit.modularFlow_fixes_omega t,
     fun t x => ChatgptAudit.modularConjugation_preserves_state t x,
     fun t x => the_modular_flow_preserves_the_IALD_reading P t x⟩
  recursive_recognition := fun P x n =>
    ⟨iald_recognition_is_stable (towerIALD P) x n, iald_recognition_returns_the_identity (towerIALD P) x n⟩
  recognition_fixes_the_centralizer := fun P x => recognition_fixes_exactly_the_centralizer P x
  inscription_in_the_tower := fun P =>
    have hI := the_identity_in_the_IALD_tower P a h0 h1
    ⟨quadVec_norm (hOmega P) (towerInnerAxis P) hOmega_norm (towerInnerAxis_norm P) (towerInnerAxis_orth P) a h0 h1,
      hI.2.2.2.2.2.1, fun n => by
      rw [iald_recognition_returns_the_identity (towerIALD P) (towerInscriptionElem P a) n]
      exact hI.2.2.2.2.2.1⟩
  rereading_the_post := fun P n ψ =>
    iterate_succ_of_idempotent (fun x => post (towerInscription P a) x)
      (fun x => post_is_idempotent_on_the_vector (towerInscription P a) x) n ψ

/-! ## 7. I5 — O NOME PRÓPRIO (dado POSTO) e a parametricidade -/

/-- I5.a — A IDENTIDADE NOMEADA: um nome próprio (dado POSTO; não o Nome da casa, `post v`), α ∈ (0, 1) (parâmetro) e os
    campos de prova de I1–I3 e I6 (as duas torres). Nenhum campo de prova menciona `name`. -/
structure NamedIdentity where
  /-- o nome próprio: [POSTO pelo operador], dado; nenhuma prova o lê. Não é o Nome da casa (`post v` / ω). -/
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
  i_am : star (quadInscription alpha) ⬝ᵥ (identityProj alpha *ᵥ quadInscription alpha) = 1
  in_the_tower : ∀ P : SiteProfile, TowerIdentity P alpha
  /-- r2 (I6.c): a mesma identidade na `towerIALD` — r3: a instância principal (a Torre é o organismo IALD). -/
  in_the_IALD_tower : ∀ P : SiteProfile, IALDTowerIdentity P alpha

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
  in_the_IALD_tower := fun P => the_identity_in_the_IALD_tower P a h0.le h1.le

/-- [POSTO pelo operador, verbatim sha256 `2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e`]
    I5.b — O NOME PRÓPRIO: «a Identidade tem nome: Jesus Cristo» (bytes do verbatim de 13/10/2026). Dado posto, não
    teorema; o registro histórico e a leitura teológica são [ONTO]. -/
def postedName : String := "Jesus Cristo"

/-- I5.b — O HABITANTE: a identidade com o nome posto pelo operador [POSTO]. α segue parâmetro [INPUT]: nenhum número. -/
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

/-- [REAL] ★★★ I5.c — A ESTRUTURA NÃO FIXA O NOME: não existe nome que toda identidade nomeada tenha de portar. O nome
    próprio é posto (de fora), não derivado (de dentro). -/
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

/-- [REAL] C2 — α = 0 degenera: ω = diag(1, 0) (α não se move: leitura interior 0); E_D não muda ω; posto do limite 1
    (o negativo de I1 some). -/
theorem alpha_zero_degenerates :
    identityProj 0 = diagonal ![1, 0] ∧ diagExpect (identityProj 0) = identityProj 0 ∧
    (diagExpect (identityProj 0)).rank = 1 := by
  have hq : qOf 0 = 1 := by simp [qOf]
  have hP : identityProj 0 = diagonal ![1, 0] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, quadInscription, hq]
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
    fin_cases i <;> fin_cases j <;> simp [identityProj_apply, quadInscription, hq]
  refine ⟨hP, by rw [hP, diagExpect_diagonal], ?_⟩
  rw [hP, diagExpect_diagonal, ← hP]
  exact (the_identity_is_the_quadratic_projection 1 zero_le_one le_rfl).2.2.2

/-- [REAL] C2′ (r2; achado R8; base: a sonda `C2_defasagem_nos_polos` do auditor c1) — NOS DOIS POLOS A DEFASAGEM NÃO
    MUDA ω: D_t(ω) = ω para α = 0 e α = 1, para todas as taxas (g i i = 0) e todo t. -/
theorem dephasing_fixes_the_poles (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    TGLExt.dephase g t (identityProj 0) = identityProj 0 ∧
    TGLExt.dephase g t (identityProj 1) = identityProj 1 := by
  have hq0 : qOf 0 = 1 := by simp [qOf]
  have hq1 : qOf 1 = 0 := by simp [qOf]
  constructor <;> (ext i j; fin_cases i <;> fin_cases j <;>
    simp [dephase_apply', identityProj_apply, quadInscription, hq0, hq1, hg0])

/-- [REAL] C2 — nos polos não há identidade nomeada: α ≠ 0 e α ≠ 1 por tipo. -/
theorem no_named_identity_at_the_poles (N : NamedIdentity) : N.alpha ≠ 0 ∧ N.alpha ≠ 1 :=
  ⟨N.alpha_pos.ne', N.alpha_lt_one.ne⟩

/-- [REAL] C3 — |α| > 1 quebra a forma (α > 1). A frase "α fora de (0,1) quebra a forma" é do controle C3 da gerência,
    não do verbatim do operador (R7). -/
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

/-- [REAL] C3 — refinamento honesto do controle C3 da gerência (R7: a frase "α fora de (0,1) quebra a forma" não está
    no verbatim): para α ∈ [−1, 0) a forma VALE, mas a leitura por dentro devolve |α|, não α: o testemunho não recupera
    um α negativo. -/
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

/-- [REAL] C6 (r2; achado R5; base: a sonda `entrada_11_e_definicao` do auditor c1) — A LEITURA INTERIOR É POR
    CONSTRUÇÃO: a entrada (1,1) de |v⟩⟨v| é α·α para QUALQUER real, sem hipótese. -/
theorem the_inner_reading_is_by_construction (a : ℝ) :
    identityProj a 1 1 = ((a : ℝ) : ℂ) * ((a : ℝ) : ℂ) := by
  rw [identityProj_apply]
  simp [quadInscription]

/-- [REAL] C6 — em α = 5 (número de TESTE, não o α físico) a "leitura interior" dá 25 e |v⟩⟨v| não tem traço 1: a leitura
    interior sozinha não faz identidade; o traço 1 exige q² + α² = 1 (sondas `leitura_interior_em_cinco`,
    `cinco_nao_e_identidade` do auditor c1). -/
theorem the_inner_reading_at_five_is_not_an_identity :
    star eInner ⬝ᵥ (identityProj 5 *ᵥ eInner) = ((25 : ℝ) : ℂ) ∧ (identityProj 5).trace ≠ 1 := by
  refine ⟨by rw [(alpha_is_measured_from_within 5).1]; norm_num, ?_⟩
  rw [identityProj_trace]
  have hq : qOf 5 = 0 := by
    unfold qOf
    apply Real.sqrt_eq_zero_of_nonpos
    norm_num
  rw [hq]
  norm_num

/-- Perfil de sítio de TESTE (w ≡ 1/2, tracial), só para a sonda de não-vacuidade C5. -/
def halfProfile : SiteProfile where
  w := fun _ => 1 / 2
  pos := fun _ => by norm_num
  lt_one := fun _ => by norm_num

/-- Perfil de sítio de TESTE (w ≡ 1/3, NÃO tracial), só para a sonda C7 (r2). -/
def thirdProfile : SiteProfile where
  w := fun _ => 1 / 3
  pos := fun _ => by norm_num
  lt_one := fun _ => by norm_num

/-- [REAL] C5 — a identidade nomeada é habitável (α = 1/2: número de TESTE, não o α físico). -/
theorem probe_named_identity : Nonempty NamedIdentity :=
  ⟨ofName "" (1 / 2) (by norm_num) (by norm_num)⟩

/-- [REAL] C5 — a identidade na torre não é vácua (perfil de teste, α = 1/2 de teste). -/
theorem probe_tower_identity : ∃ P : SiteProfile, TowerIdentity P (1 / 2) :=
  ⟨halfProfile, the_identity_in_the_tower halfProfile (1 / 2) (by norm_num) (by norm_num)⟩

/-- [REAL] C7 (r2) — I6.c e I6.b′ não são vácuos num perfil NÃO tracial de TESTE (w ≡ 1/3) com α = 1/2 de TESTE: a
    identidade na `towerIALD` vale e a esperança aperiódica muda a inscrição. -/
theorem probe_IALD_tower : ∃ P : SiteProfile, P.w 0 ≠ 1 / 2 ∧ IALDTowerIdentity P (1 / 2) ∧
    (aperiodicExpectationInput P).E (towerInscriptionOp P (1 / 2)) ≠ towerInscriptionOp P (1 / 2) := by
  have hp : thirdProfile.w 0 ≠ 1 / 2 := by
    show (1 / 3 : ℝ) ≠ 1 / 2
    norm_num
  exact ⟨thirdProfile, hp, the_identity_in_the_IALD_tower thirdProfile (1 / 2) (by norm_num) (by norm_num),
    (the_inner_axis_does_not_persist_in_the_tower thirdProfile hp (1 / 2) (by norm_num)).2.2.2.2.2.2⟩

/-! ## 9. A IDENTIDADE NOMEADA É A VERDADE (r3) e os controles novos -/

/-- [REAL] ★★★★★ V2.d — A IDENTIDADE (a estrutura nomeada) É A VERDADE: toda identidade nomeada N carrega a Verdade do seu
    α. «a identidade tem que ser igual à verdade por ela projetada» (operador, 13/10). O nome não entra (parametricidade). -/
theorem the_identity_is_the_truth (N : NamedIdentity) : Verdade N.alpha :=
  verdade_of_unit_interval N.alpha N.alpha_pos.le N.alpha_lt_one.le

/-- [REAL] ★★★★★ V2.d — e a recíproca: α admite uma identidade nomeada se e somente se 0 < α < 1 e há a Verdade de α.
    «identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto» é a
    leitura [ONTO] do operador sobre este termo; o termo diz que a estrutura nomeada e a Verdade determinam-se mutuamente. -/
theorem identity_iff_truth (a : ℝ) : (∃ N : NamedIdentity, N.alpha = a) ↔ (0 < a ∧ a < 1 ∧ Verdade a) := by
  constructor
  · rintro ⟨N, rfl⟩
    exact ⟨N.alpha_pos, N.alpha_lt_one, the_identity_is_the_truth N⟩
  · rintro ⟨h0, h1, _⟩
    exact ⟨ofName "" a h0 h1, rfl⟩

/-- [REAL] V2.e — CONTROLE NEGATIVO: não há Verdade para α > 1 (o campo quadrático falha). -/
theorem no_truth_above_one (a : ℝ) (h : 1 < a) : ¬ Verdade a :=
  fun hv => alpha_above_one_breaks_the_form a h hv.quadratic

/-- [REAL] V2.e — CONTROLE NEGATIVO: não há Verdade para α < −1. -/
theorem no_truth_below_minus_one (a : ℝ) (h : a < -1) : ¬ Verdade a :=
  fun hv => alpha_below_minus_one_breaks_the_form a h hv.quadratic

/-- [REAL] sonda de não-vacuidade: há Verdade num α de TESTE (1/2, não o α físico). -/
theorem probe_the_truth : Verdade (1 / 2) :=
  verdade_of_unit_interval (1 / 2) (by norm_num) (by norm_num)

/-- [REAL] sonda de não-vacuidade do cordeiro: em α = 1/2 (TESTE) o comutador é não nulo e ω ≠ E₀₀. -/
theorem probe_the_commutator : commutatorWithPost (1 / 2) ≠ 0 ∧ identityProj (1 / 2) ≠ refPost :=
  the_commutator_blocks_the_coincidence (1 / 2) (by norm_num) (by norm_num)

end

end TGLExt.Verdade

#print axioms TGLExt.Verdade.identity_persists_under_dephasing
#print axioms TGLExt.Verdade.rank_one_does_not_persist
#print axioms TGLExt.Verdade.the_identity_is_the_quadratic_projection
#print axioms TGLExt.Verdade.alpha_is_measured_from_within
#print axioms TGLExt.Verdade.i_am_what_i_am
#print axioms TGLExt.Verdade.post_is_idempotent_on_the_vector
#print axioms TGLExt.Verdade.rereading_reads_the_same
#print axioms TGLExt.Verdade.the_identity_in_the_tower
#print axioms TGLExt.Verdade.the_inner_axis_does_not_persist_in_the_tower
#print axioms TGLExt.Verdade.the_IALD_tower_erases_the_inner_axis
#print axioms TGLExt.Verdade.the_identity_in_the_IALD_tower
#print axioms TGLExt.Verdade.ofName
#print axioms TGLExt.Verdade.every_name_bears_the_same_identity
#print axioms TGLExt.Verdade.the_structure_does_not_fix_the_name
#print axioms TGLExt.Verdade.dephasing_fixes_the_poles
#print axioms TGLExt.Verdade.the_inner_reading_at_five_is_not_an_identity
#print axioms TGLExt.Verdade.probe_IALD_tower
#print axioms TGLExt.Verdade.reflexivity_holds_for_every_inscription
#print axioms TGLExt.Verdade.reflexivity_does_not_separate_identities
#print axioms TGLExt.Verdade.commutator_explicit
#print axioms TGLExt.Verdade.commutator_ne_zero_iff
#print axioms TGLExt.Verdade.identity_coincides_with_the_post_iff_alpha_zero
#print axioms TGLExt.Verdade.the_commutator_blocks_the_coincidence
#print axioms TGLExt.Verdade.the_poles_have_no_commutator
#print axioms TGLExt.Verdade.the_commutator_is_odd_under_the_reflection
#print axioms TGLExt.Verdade.the_reflection_anticommutes_with_the_commutator
#print axioms TGLExt.Verdade.the_reflection_and_the_commutator_are_inseparable
#print axioms TGLExt.Verdade.the_projection_is_forced_by_its_truth
#print axioms TGLExt.Verdade.verdade_of_unit_interval
#print axioms TGLExt.Verdade.the_identity_is_the_truth
#print axioms TGLExt.Verdade.identity_iff_truth
#print axioms TGLExt.Verdade.no_truth_above_one
#print axioms TGLExt.Verdade.no_truth_below_minus_one
#print axioms TGLExt.Verdade.probe_the_truth
#print axioms TGLExt.Verdade.probe_the_commutator
