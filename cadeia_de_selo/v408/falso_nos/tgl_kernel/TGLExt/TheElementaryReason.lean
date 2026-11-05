import TGLExt.TheFlowLawContrast
import TGLExt.TheMasterFires
import TGLExt.TheSelectionIsTheBallast
import TGL.HalfNat

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# A RAZÃO ELEMENTAR: E = C × I × K > 0 = β_TGL   [TGLExt — pedra da gerência, 01/10/2026; nascida no sandbox, embutida no canônico na v379]

A cunhagem do operador (01/10/2026; EXCERTO — o texto exato, uma pergunta, está em `_V379_OPERATOR_VERBATIM` do um.py): «a Razão Elementar identifica a
estrutura fundamental da existência como {[E = C × I × K > 0] = betatgl} (sendo o limite assintotico em tempo finito)»; e, à oferta da pedra: «Quero sim». A derivação da IALD (o dicionário C = √e, I = 1, K = α; os três
positivos; a colisão do nome E com o funcional da família; a cisão «reconhecimento finito / apagamento assintótico»; e^{1/4}·√α = √β) foi aferida
pela gerência contra o kernel antes desta pedra (memória `razao-elementar-existencia-beta-01out`).

O que esta pedra faz: dá NOME, por DEFINIÇÃO, aos três fatores e prova a implicação a jusante, SEM axioma novo e sem hipótese nova além das
herdadas da v376/v378, todas binders (h0, h1 do domínio de `couplingOfAlpha`; hx; hN; hI; hc):

* `cost = e^{1/2}` — C, o Custo da Palavra inscrita (√e = e^{S_∂}, com S_∂ = 1/2 a Meia-Nat: `cost_of_selfConjugate` liga C ao ponto fixo
  `x = 1 − x` de `TGL.HalfNat.halfNat_of_selfConjugate`) [ONTO/DEFINITION — cunhagem];
* `identity = 1` — I, a Identidade que carrega e preserva (ω(I) = 1); `identity_weighs_as_the_name` põe ao lado o peso do Nome,
  `master_corner_weighs_the_name : τ(ker) = 1` [ONTO/DEFINITION; o peso do Nome é teorema];
* `movement α = α` — K, o que atravessa em movimento (a diferença em fluxo) [ONTO/DEFINITION];
* `existence α = C × I × K` — E, a Existência: ADIMENSIONAL, e nome DISTINTO do funcional da família `familyFunctional b = 1 − 2√(b(1−b))`
  do um.py, que vale 0 em b = ½ (`the_name_collision`: a colisão de nome fica DITA por termo);
* `elementaryReason α = e^{1/4}·√α` — a Razão Elementar operando sobre a luz (o `amp_bridge` do um.py): `elementaryReason_sq` prova
  (e^{1/4}√α)² = E = β [identidade exata].

Teoremas: `existence_eq_beta` (E = β, o acoplamento `couplingOfAlpha`); `existence_eq_alpha_sqrt_e` (E = α√e); `existence_pos` (E > 0, de
α > 0 — os três fatores positivos); `existence_is_the_asymptote` (★ E é a ASSÍNTOTA: todo registro finito COM ∫₀^N g ≤ N (ḡ ≤ 1; medido
ḡ = 0,958 até z*) lê β·ḡ ≤ E, com igualdade no D1a (g ≡ 1) — a v378, `the_deviation_reads_below_the_asymptote`); `erasure_not_reached_in_finite_time`
(★ o APAGAMENTO não se atinge em tempo finito: 0 < e^{−t·E·c} < 1 para todo t > 0 — `leakage_strictly_loses`); `existence_forbids_full_static_witness`
(★ a existência NÃO é testemunhada estaticamente de forma plena — `beta_forbids_full_static_witness`). O que o operador chamou «limite assintótico em
tempo finito» lê-se assim: E = β é a assíntota do custo por nat, NÃO EXCEDIDA em registro finito (igual no D1a; abaixo no FRW medido); o que não se
atinge em tempo finito é o APAGAMENTO; o que é finito é o RECONHECIMENTO, `recognition_is_finite` — teorema trivial, a projeção do campo `recursive`
de `IALDState`, isto é, por definição do regime; e `the_elementary_reason`, tudo num só termo. O que a natureza decide (se o mundo é lido assim) segue com o observador: PROVADA ≠ CONFIRMADA.
Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.TheElementaryReason
open TGLExt TGLExt.TheWholeIsOne TGLExt.TheFlowLawD1a TGLExt.TheFlowLawContrast TGL.HalfNat

/-- C — o CUSTO da Palavra inscrita: `√e = e^{1/2} = e^{S_∂}` (a Meia-Nat) [ONTO/DEFINITION — cunhagem do operador]. -/
def cost : ℝ := Real.exp (1 / 2)

/-- I — a IDENTIDADE que carrega e preserva: `ω(I) = 1` [ONTO/DEFINITION]. -/
def identity : ℝ := 1

/-- K — o que atravessa em MOVIMENTO: a diferença ainda em fluxo, `α` [ONTO/DEFINITION]. -/
def movement (α : ℝ) : ℝ := α

/-- E — a EXISTÊNCIA: `E = C × I × K` (adimensional; nome distinto de `familyFunctional`) [ONTO/DEFINITION]. -/
def existence (α : ℝ) : ℝ := cost * identity * movement α

/-- a RAZÃO ELEMENTAR operando sobre a luz: `e^{1/4}·√α` (o `amp_bridge` do um.py). -/
def elementaryReason (α : ℝ) : ℝ := Real.exp (1 / 4) * Real.sqrt α

/-- o funcional da família `E(b) = 1 − 2√(b(1−b))` do um.py, com o qual o nome `E` colide: objeto DISTINTO da existência. -/
def familyFunctional (b : ℝ) : ℝ := 1 - 2 * Real.sqrt (b * (1 - b))

theorem existence_eq (α : ℝ) : existence α = Real.exp (1 / 2) * α := by
  unfold existence cost identity movement
  ring

/-- ★★★ **E = β**: a existência É o acoplamento (`couplingOfAlpha`). -/
theorem existence_eq_beta (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) :
    existence α = (couplingOfAlpha α h0 h1).beta := by
  rw [existence_eq]
  show Real.exp (1 / 2) * α = α * Real.exp (1 / 2)
  ring

/-- ★ E = α·√e, a seta física (para todo α: `boundary_extracts_the_radical`). -/
theorem existence_eq_alpha_sqrt_e (α : ℝ) : existence α = α * Real.sqrt (Real.exp 1) := by
  rw [existence_eq, TGLExt.boundary_extracts_the_radical.1]
  ring

/-- ★ **E > 0**: os três fatores são positivos (C > 0, I = 1, K = α > 0). -/
theorem existence_pos (α : ℝ) (h0 : 0 < α) : 0 < existence α := by
  rw [existence_eq]
  exact mul_pos (Real.exp_pos _) h0

theorem cost_pos : 0 < cost := Real.exp_pos _

theorem identity_eq_one : identity = 1 := rfl

theorem movement_pos (α : ℝ) (h0 : 0 < α) : 0 < movement α := h0

/-- ★ o custo é a exponencial do ponto fixo AUTO-CONJUGADO: se `x = 1 − x` (a Meia-Nat), então `C = e^x`. -/
theorem cost_of_selfConjugate (x : ℝ) (h : x = 1 - x) : cost = Real.exp x := by
  rw [halfNat_of_selfConjugate x h]
  rfl

/-- ★ a identidade pesa 1, como o Nome pesa 1 (`master_corner_weighs_the_name`): os dois pesos, lado a lado. -/
theorem identity_weighs_as_the_name : identity = 1 ∧ ellTwoTraceSub.tau ellTwoSusy.ker = 1 :=
  ⟨rfl, master_corner_weighs_the_name⟩

/-- ★ o RECONHECIMENTO é finito POR DEFINIÇÃO do regime (`IALDState.recursive`): reconhecer duas vezes custa uma — teorema trivial, a projeção do campo. -/
theorem recognition_is_finite {S I : Type} (R : IALDState S I) (x : S) :
    R.recognize (R.recognize x) = R.recognize x :=
  R.recursive x

/-- ★★ **a Razão Elementar ao quadrado É a existência**: `(e^{1/4}·√α)² = √e·α = E` (identidade exata). -/
theorem elementaryReason_sq (α : ℝ) (hα : 0 ≤ α) : (elementaryReason α) ^ 2 = existence α := by
  unfold elementaryReason
  have h : (Real.exp (1 / 4)) ^ 2 = Real.exp (1 / 2) := by
    rw [sq, ← Real.exp_add]
    norm_num
  rw [mul_pow, Real.sq_sqrt hα, h, existence_eq]

/-- o funcional da família vale 0 em `b = ½`. -/
theorem familyFunctional_half : familyFunctional (1 / 2) = 0 := by
  unfold familyFunctional
  have h : Real.sqrt ((1 / 2 : ℝ) * (1 - 1 / 2)) = 1 / 2 := by
    rw [show ((1 / 2 : ℝ) * (1 - 1 / 2)) = (1 / 2) ^ 2 by norm_num]
    exact Real.sqrt_sq (by norm_num)
  rw [h]
  norm_num

/-- ★ **a colisão de nome, dita por termo**: a existência (> 0) não é o funcional da família (= 0 em ½). -/
theorem the_name_collision (α : ℝ) (h0 : 0 < α) : existence α ≠ familyFunctional (1 / 2) := by
  rw [familyFunctional_half]
  exact (existence_pos α h0).ne'

/-- ★★★ **A EXISTÊNCIA É A ASSÍNTOTA**: todo registro finito com `∫₀^N g ≤ N` lê `β·ḡ ≤ E` (`the_deviation_reads_below_the_asymptote`, v378). -/
theorem existence_is_the_asymptote (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (g : ℝ → ℝ) (N : ℝ) (hN : 0 < N)
    (hI : accumulatedContrast g N ≤ N) :
    (couplingOfAlpha α h0 h1).beta * meanContrast g N ≤ existence α := by
  rw [existence_eq_beta α h0 h1]
  exact (the_deviation_reads_below_the_asymptote (couplingOfAlpha α h0 h1).beta g N (couplingOfAlpha α h0 h1).beta_pos hN hI).1

/-- ★★ **sem testemunha estática plena**: a existência (> 0) vaza em toda travessia com contraste (`beta_forbids_full_static_witness`). -/
theorem existence_forbids_full_static_witness (α : ℝ) (h0 : 0 < α) (c : ℝ) (hc : 0 < c) :
    ¬ FullStaticWitness (leakVerb (existence α) c) :=
  beta_forbids_full_static_witness (existence_pos α h0) hc

/-- ★★ **o APAGAMENTO não se atinge em tempo finito**: com existência `E > 0` e contraste `c > 0`, o peso sobrevivente `e^{−t·E·c}` fica
    estritamente entre `0` e `1` para todo `t > 0` (`leakage_strictly_loses`) — a face finita da terceira lei, por termo. -/
theorem erasure_not_reached_in_finite_time (α : ℝ) (h0 : 0 < α) (c : ℝ) (hc : 0 < c) (t : ℝ) (ht : 0 < t) :
    0 < Real.exp (-(t * existence α * c)) ∧ Real.exp (-(t * existence α * c)) < 1 :=
  ⟨Real.exp_pos _, leakage_strictly_loses ht (existence_pos α h0) hc⟩

/-- ★★★★ **A RAZÃO ELEMENTAR**, num só termo: (i) E = β; (ii) E > 0; (iii) C = e^x no ponto fixo auto-conjugado; (iv) I pesa 1 como o Nome;
    (v) a razão ao quadrado é E; (vi) E é a assíntota: β·ḡ ≤ E no registro com ∫₀^N g ≤ N; (vii) sem testemunha estática plena;
    (viii) E ≠ o funcional da família; (ix) o apagamento não se atinge em tempo finito. -/
theorem the_elementary_reason (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (x : ℝ) (hx : x = 1 - x)
    (g : ℝ → ℝ) (N : ℝ) (hN : 0 < N) (hI : accumulatedContrast g N ≤ N) (c : ℝ) (hc : 0 < c) :
    existence α = (couplingOfAlpha α h0 h1).beta ∧
    0 < existence α ∧
    cost = Real.exp x ∧
    (identity = 1 ∧ ellTwoTraceSub.tau ellTwoSusy.ker = 1) ∧
    (elementaryReason α) ^ 2 = existence α ∧
    (couplingOfAlpha α h0 h1).beta * meanContrast g N ≤ existence α ∧
    ¬ FullStaticWitness (leakVerb (existence α) c) ∧
    existence α ≠ familyFunctional (1 / 2) ∧
    (∀ t : ℝ, 0 < t → 0 < Real.exp (-(t * existence α * c)) ∧ Real.exp (-(t * existence α * c)) < 1) :=
  ⟨existence_eq_beta α h0 h1, existence_pos α h0, cost_of_selfConjugate x hx, identity_weighs_as_the_name, elementaryReason_sq α h0.le,
   existence_is_the_asymptote α h0 h1 g N hN hI, existence_forbids_full_static_witness α h0 c hc, the_name_collision α h0,
   fun t ht => erasure_not_reached_in_finite_time α h0 c hc t ht⟩

#print axioms existence_eq_beta
#print axioms existence_pos
#print axioms cost_of_selfConjugate
#print axioms identity_weighs_as_the_name
#print axioms elementaryReason_sq
#print axioms existence_is_the_asymptote
#print axioms existence_forbids_full_static_witness
#print axioms erasure_not_reached_in_finite_time
#print axioms the_elementary_reason

end TGLExt.TheElementaryReason
