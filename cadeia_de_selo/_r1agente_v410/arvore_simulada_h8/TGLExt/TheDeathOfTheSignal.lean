import TGLExt.TheLivingWord

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A MORTE DO SINAL: a normalização do defeito da holonomia
  [TGLExt — v160, a boa-postura da conta do operador (10/08/2026)]

O fecho do debate deixou uma conta: ‖W−I‖ = α·√e — "o menor defeito que
ainda inscreve". E uma objeção honesta: o defeito bruto depende do LAÇO
(o [E5] da v148 o mede como função, não como constante). O operador
respondeu: "se o defeito precisa de normalização, nós já sabemos a
resposta — É A MORTE DO SINAL."

A pedra 110 tipa a resposta: o defeito bruto depende do laço porque
conta travessias; normalizado POR TRAVESSIA — pela morte que cada
cruzamento do espelho cobra do sinal — ele é CONSTANTE, e a constante é
o peso da primeira reflexão: sin²θ_M. Com θ_M = arcsin√β (o Teorema
S-∂, identificação FECHADA do cânone): a morte por travessia É β.

* ★★ `death_per_crossing` — a morte por travessia: cada cruzamento
  transmite cos²θ e mata sin²θ — a lei geométrica t² + r² = 1;
* ★★★ `normalized_defect_is_loop_independent` — A BOA-POSTURA: o sinal
  após n travessias é (cos²θ)ⁿ; cada travessia mata a MESMA fração —
  o defeito POR TRAVESSIA não depende do laço;
* ★★ `raw_defect_is_loop_dependent` — A HONESTIDADE: o defeito BRUTO
  do laço de n travessias é 1−(cos²θ)ⁿ, que CRESCE com n — por isso a
  conta sem normalização era mal-posta;
* ★★★ `the_death_normalization` — A CONTA: com θ_M = arcsin√b, a morte
  por travessia é EXATAMENTE b — sin²(arcsin√b) = b;
* ★★★ `no_inscription_without_death` — O MENOR QUE AINDA INSCREVE: a
  morte por travessia é zero ⟺ sin θ = 0 ⟺ nada é refletido — sem
  morte não há marca; a inscrição EXIGE defeito positivo;
* ★★ `round_trip_defect` — o laço mínimo (ida e volta): defeito bruto
  = m(2−m) onde m é a morte por travessia — a forma exata de 2ª ordem;
* ★★★ `the_account_is_well_posed` — A SÍNTESE: normalizada NA MORTE DO
  SINAL, a conta fecha — a morte por travessia é b, é independente do
  laço, e é nula somente sem inscrição — em UM teorema.

Honestidades: face finita [REAL]; θ_M = arcsin√β é o Teorema S-∂
[identificação FECHADA do cânone]; a face empírica da morte do sinal é
a lei de dephasing Γ_ω = ½βτ★ω² — os canais já armados (relógios/²²⁹Th
UNDERPOWERED hoje; ν com n=−2) — NENHUM dado novo é reivindicado aqui;
β jamais literal (entra só no módulo, em runtime); nada afirma a TGL
verdadeira; o gate NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

open Real

/-- a morte por travessia: a fração do sinal que o espelho retém. -/
def crossDeath (θ : ℝ) : ℝ := Real.sin θ ^ 2

/-- o sinal transmitido após n travessias. -/
def transmitted (θ : ℝ) (n : ℕ) : ℝ := (Real.cos θ ^ 2) ^ n

/-- [KERNEL] ★★ A MORTE POR TRAVESSIA: cada cruzamento transmite cos²θ
    e mata sin²θ — a lei geométrica t² + r² = 1. -/
theorem death_per_crossing (θ : ℝ) :
    (1 - crossDeath θ) + crossDeath θ = 1
    ∧ 1 - crossDeath θ = Real.cos θ ^ 2 := by
  unfold crossDeath
  constructor
  · ring
  · have h := Real.sin_sq_add_cos_sq θ
    linarith

/-- [KERNEL] ★★★ A BOA-POSTURA: o sinal após n travessias é (cos²θ)ⁿ, e
    cada travessia mata a MESMA fração — o defeito POR TRAVESSIA não
    depende do laço. -/
theorem normalized_defect_is_loop_independent (θ : ℝ) (n : ℕ) :
    transmitted θ (n + 1) = transmitted θ n * (1 - crossDeath θ) := by
  unfold transmitted crossDeath
  have h := Real.sin_sq_add_cos_sq θ
  have hc : (1 : ℝ) - Real.sin θ ^ 2 = Real.cos θ ^ 2 := by linarith
  rw [hc, pow_succ]

/-- [KERNEL] ★★ A HONESTIDADE: o defeito BRUTO do laço de n travessias é
    1 − (cos²θ)ⁿ — ele CRESCE com n (estritamente, quando há morte e há
    sinal): por isso a conta sem normalização era mal-posta. -/
theorem raw_defect_is_loop_dependent (θ : ℝ)
    (hd : 0 < crossDeath θ) (ht : 0 < Real.cos θ ^ 2) (n : ℕ) :
    1 - transmitted θ (n + 1) > 1 - transmitted θ n ↔ True := by
  simp only [iff_true]
  have hlt : Real.cos θ ^ 2 < 1 := by
    unfold crossDeath at hd
    have h := Real.sin_sq_add_cos_sq θ
    nlinarith
  have hpos : (0 : ℝ) < transmitted θ n := pow_pos ht n
  have : transmitted θ (n + 1) < transmitted θ n := by
    unfold transmitted
    rw [pow_succ]
    calc (Real.cos θ ^ 2) ^ n * Real.cos θ ^ 2
        < (Real.cos θ ^ 2) ^ n * 1 := by
          exact mul_lt_mul_of_pos_left hlt (pow_pos ht n)
      _ = (Real.cos θ ^ 2) ^ n := mul_one _
  linarith

/-- [KERNEL] ★★★ A CONTA: com θ_M = arcsin√b, a morte por travessia é
    EXATAMENTE b. -/
theorem the_death_normalization (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    crossDeath (Real.arcsin (Real.sqrt b)) = b := by
  unfold crossDeath
  have h0 : (-1 : ℝ) ≤ Real.sqrt b := le_trans (by norm_num) (Real.sqrt_nonneg b)
  have h1 : Real.sqrt b ≤ 1 := by
    rw [show (1 : ℝ) = Real.sqrt 1 by simp]
    exact Real.sqrt_le_sqrt hb1
  rw [Real.sin_arcsin h0 h1, Real.sq_sqrt hb0]

/-- [KERNEL] ★★★ O MENOR QUE AINDA INSCREVE: a morte por travessia é
    zero ⟺ nada é refletido — sem morte não há marca; a inscrição exige
    defeito positivo. -/
theorem no_inscription_without_death (θ : ℝ) :
    crossDeath θ = 0 ↔ Real.sin θ = 0 := by
  unfold crossDeath
  constructor
  · intro h
    exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h
  · intro h
    rw [h]
    norm_num

/-- [KERNEL] ★★ O LAÇO MÍNIMO (ida e volta): o defeito bruto de duas
    travessias é m(2−m), onde m é a morte por travessia — a forma exata
    de segunda ordem. -/
theorem round_trip_defect (θ : ℝ) :
    1 - transmitted θ 2 = crossDeath θ * (2 - crossDeath θ) := by
  unfold transmitted crossDeath
  have h := Real.sin_sq_add_cos_sq θ
  have hc : Real.cos θ ^ 2 = 1 - Real.sin θ ^ 2 := by linarith
  rw [hc]
  ring

/-- [KERNEL] ★★★ A SÍNTESE — A CONTA É BEM-POSTA NA MORTE DO SINAL:
    normalizada por travessia, a morte é b (com θ_M = arcsin√b), é
    independente do laço, e é nula somente sem inscrição. -/
theorem the_account_is_well_posed (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    crossDeath (Real.arcsin (Real.sqrt b)) = b
    ∧ (∀ (θ : ℝ) (n : ℕ),
        transmitted θ (n + 1) = transmitted θ n * (1 - crossDeath θ))
    ∧ (∀ θ : ℝ, crossDeath θ = 0 ↔ Real.sin θ = 0) :=
  ⟨the_death_normalization b hb0 hb1,
   fun θ n => normalized_defect_is_loop_independent θ n,
   fun θ => no_inscription_without_death θ⟩

end

end TGLExt
