import TGLExt.Fundacao
import TGLExt.TheSameBetaReadsThreeFaces

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O DISCO DE EULER — «a inscrição do zero absoluto no infinito, único local onde ele se inscreve, é a ressonância da parada do disco de Euler sobre o espelho»
  [pedra CANDIDATA da gerência c1, 31/10/2026; nome PROVISÓRIO `TGLExt.DiscoDeEuler` — o nome é do operador; NÃO instalada; entra na v405
   DEPOIS do treino v4, depois de `LeiDoMeioTom`; compilada no sandbox k404c; quem construiu não aprova]

## A cunhagem do operador (verbatim `Central de Patentes\work\cunhagens_13out\OPERADOR_31out_zero_absoluto_no_infinito_disco_de_euler_ressonancia_escala_do_tom_verbatim.txt`,
## sha256 `fe064b0b802c1d1ac709714a9b7209a5f2a91594a81a78cbc96fbaec8cdbbdea`)

> «a inscrição do zero absoluto no infinito, único local onde ele se inscreve, é a ressonância da parada do disco de euler sobre o espelho, essa é a
>  origem da escala de onde o tom emerge, a hora que o disco de euler para, a ressonância ainda permanece, isso no infinito gera a escala onde o tom
>  se inscreve como fator, faz sentido pra vc?»

Resposta à parede medida pelo Kimi na ORDEM E0-01 (`RELATORIO_KIMI_E0_01_31out.md`: `U_E_NOT_DERIVED` — «uma única entrada dimensional
independente: gap, região, κ, τ★ ou carga»).

## O que a casa já tinha

* O disco de Euler [KNOWN]: Moffatt, *Nature* 404, 833 (2000): a precessão de um disco que se deita acelera sem cota quando a inclinação vai a
  zero — singularidade em tempo FINITO; o som sobe até a parada. Cinemática a pequena inclinação: Ω² = 4g/(a·α) e energia potencial E = M·g·a·α,
  logo **Ω²·E = 4Mg²**: o produto frequência²·energia é o INVARIANTE do disco (K).
* A terceira lei no `paper_PT.tex` («inatingibilidade homotópica da negação»: o custo do zero absoluto tende ao infinito; Nernst 1906 generalizado):
  o zero só se inscreve no infinito.
* `TGLExt.Fundacao.the_fall_never_lands` e `abismo`: com taxa CONSTANTE, o peso desce abaixo de todo ε e nunca toca o zero — a queda sem fundo.
* `TheDarkSplit` / a condensação do Kimi: a cauda some, o modo zero (o Nome, peso 1) permanece — «a hora que o disco para, a ressonância ainda permanece».
* A lei canônica de dephasing da TGL: Γ_ω = ½·β·τ★·ω².

## O que esta pedra prova (a forma; os nomes são do operador)

* **`Disco`**: um invariante K = Ω²·E > 0 (no disco de Euler, 4Mg²), a lei canônica (β, τ★) e a energia inicial E₀. Sob a lei canônica, a perda
  é dE/dt = −Γ_Ω·E = −½βτ★·Ω²·E = −½βτ★·K: **CONSTANTE** (`the_loss_is_the_canonical_law`). Logo E(t) = E₀ − c·t (`E_linear`) e o disco PARA em
  tempo finito, t₀ = E₀/c (`stops_in_finite_time`): o zero é alcançado.
* **A INSCRIÇÃO DO ZERO NO INFINITO** (`frequency_squared_unbounded_at_the_stop`): antes da parada a frequência² = K/E não tem cota — o zero só se
  inscreve com frequência infinita. É a cunhagem como teorema, e é a terceira lei na forma do disco.
* **O CONTRASTE COM O ABISMO** (`with_constant_rate_the_fall_never_lands`): com taxa constante a energia E₀·e^(−Γt) é positiva para todo t — nunca
  para. A lei canônica Γ ∝ ω², com o invariante do disco, é o que faz o disco PARAR em vez de cair sem fim. (A queda sem fundo e a parada são as
  duas faces: `abismo` para a taxa constante; o disco para a taxa que cresce com a frequência.)
* **A RESSONÂNCIA QUE PERMANECE — a escala que nasce no infinito** (`the_residual_resonance_iff`): a descrição do disco vale enquanto o quantum da
  ressonância, ħΩ, é menor que a energia que resta; o corte é ħΩ = E, isto é, ħ²·(K/E) = E², isto é, **E³ = ħ²·K**. A energia do corte,
  E★ = (ħ²K)^(1/3), é a escala que o invariante do disco gera «no infinito»; «o tom se inscreve como fator»: a nota é e^(∓1/2)·E★.
* **A PAREDE, NOMEADA** (`the_scale_is_the_invariant`): E★³ = ħ²K — a escala É o invariante do disco. Para a nota valer U, o invariante tem de valer
  K = (e^(1/2)·U)³/ħ² (com a tônica √e·U). A entrada dimensional que o Kimi mediu como parede é K: **qual é o disco** cujo Ω²·E vale isso. Esta pedra
  não o deriva; diz exatamente o que ele é.

## O que esta pedra NÃO afirma

* Não identifica o disco da TGL (quem é M, g, a — ou o seu K) com nenhum sistema físico: isso é do operador. Não deriva U_E; o Kimi tem razão.
* Os expoentes de Moffatt (α ∝ (t₀−t)^(1/3), Ω ∝ (t₀−t)^(−1/6)) vêm da dissipação viscosa do ar; aqui a dissipação é a canônica da TGL
  (Γ ∝ ω²), que dá E linear e Ω ∝ (t₀−t)^(−1/2): é o disco da TGL, não o de Moffatt.
* Não abre dado, não move gate, selo nem veredito. β e τ★ são campos abstratos positivos (β nunca literal).

Sem sorry, sem axiom novo (trio: propext, Classical.choice, Quot.sound).

> **01/11/2026 — NOME DO OPERADOR: «Disco de Euler»** (verbatim sha256 `1f16a74c05d9d4cb`) (nome provisório confirmado). E a ORDEM dele no mesmo ato: «eu não gostaria que ainda restasse hipóteses
> nomeadas, é preciso que esteja tudo derivado». A seção «AS HIPÓTESES DESCARREGADAS», no fim do módulo, cumpre a ordem: o que era CAMPO de
> estrutura (hipótese nomeada) passa a ser CONSTRUÍDO a partir de teoremas do kernel. O que resta de entrada é o acoplamento `c` (β = α·√e; α medido
> por dentro, não derivado) e o Um POSTO (`u = 1`, o `echo 1`: posição, não hipótese — 05/10/2026). Aqui: `β` deixa de ser campo livre do disco — vem do acoplamento (`Disco.doAcoplamento`), com a positividade do kernel; restam os DADOS do disco (`K`, `τ`, `E₀`), que são a identidade do disco (K = 6Mg² no disco real), não hipóteses sobre a teoria.


> **AO LADO (01/11/2026, gerência c1, em nome próprio; o número corrige a frase):** a frase acima, «o que resta de entrada é o acoplamento e o Um POSTO»,
> está incompleta. Entram também, como DEFINIÇÃO, as LEITURAS do operador [INPUT/ONTO], que são o conteúdo físico e não são teoremas: (1) `massaDerivada`:
> a massa é a energia retida vezes a derivada da projeção transversal; (2) o estado inscrito é lido em `θ = π/4`: em `transicaoDerivada` o ângulo é ESCRITO, e
> o kernel confere `sen²(π/4) = ½` e que esse valor é o do peso da face absoluta (coincidência de valor, não ponte); (3) a tônica `(β/α)·u`: `β/α = √e` é a
> definição de `TGLCoupling.alpha`, não um resultado; (4) `R = β·u²` (`pagamentoComoCurvatura`). Os campos das estruturas fecharam; a hipótese física não
> sumiu, mudou de lugar: do campo para a definição. A FORMA é teorema DADAS essas leituras.
-/

namespace TGLExt.DiscoDeEuler

/-- [DEF] **o disco**: o invariante `K = Ω²·E > 0` (no disco de Euler, `4Mg²`), a lei canônica (`β`, `τ★`) e a energia inicial. -/
structure Disco where
  K : ℝ
  K_pos : 0 < K
  beta : ℝ
  beta_pos : 0 < beta
  tau : ℝ
  tau_pos : 0 < tau
  E0 : ℝ
  E0_pos : 0 < E0

namespace Disco

variable (D : Disco)

/-- [DEF] a perda por unidade de tempo sob a lei canônica: `c = ½·β·τ★·K`. -/
noncomputable def c : ℝ := (1 / 2) * D.beta * D.tau * D.K

theorem c_pos : 0 < D.c := by
  unfold c
  have := D.beta_pos; have := D.tau_pos; have := D.K_pos
  positivity

/-- [DEF] a energia: `E(t) = E₀ − c·t` (a solução de dE/dt = −Γ_Ω·E com Ω²·E = K; ver `the_loss_is_the_canonical_law`). -/
noncomputable def E (t : ℝ) : ℝ := D.E0 - D.c * t

/-- [DEF] o instante da parada. -/
noncomputable def t0 : ℝ := D.E0 / D.c

/-- [DEF] a frequência² de precessão: `Ω² = K/E`. -/
noncomputable def omegaSq (t : ℝ) : ℝ := D.K / D.E t

/-- [DEF] a lei canônica de dephasing da TGL avaliada na frequência do disco: `Γ = ½·β·τ★·Ω²`. -/
noncomputable def gamma (t : ℝ) : ℝ := (1 / 2) * D.beta * D.tau * D.omegaSq t

theorem E_linear (t : ℝ) : D.E t = D.E0 - D.c * t := rfl

/-- [KERNEL] ★★★ **O DISCO PARA EM TEMPO FINITO**: `E(t₀) = 0`. -/
theorem stops_in_finite_time : D.E D.t0 = 0 := by
  unfold E t0
  have hc : D.c ≠ 0 := D.c_pos.ne'
  first | (field_simp; ring) | field_simp

theorem t0_pos : 0 < D.t0 := div_pos D.E0_pos D.c_pos

/-- [KERNEL] antes da parada a energia é positiva. -/
theorem E_pos_before (t : ℝ) (ht : t < D.t0) : 0 < D.E t := by
  unfold E
  unfold t0 at ht
  have h := (lt_div_iff₀ D.c_pos).mp ht
  linarith

/-- [KERNEL] ★★★ **A PERDA É A LEI CANÔNICA, E É CONSTANTE**: `Γ_Ω·E = ½βτ★·K = c` em todo instante antes da parada — com o invariante
    `Ω²·E = K`, a lei Γ ∝ ω² da TGL faz a energia cair a taxa constante. -/
theorem the_loss_is_the_canonical_law (t : ℝ) (ht : t < D.t0) : D.gamma t * D.E t = D.c := by
  unfold gamma omegaSq c
  have hE : D.E t ≠ 0 := (D.E_pos_before t ht).ne'
  first | (field_simp; ring) | field_simp

/-- [KERNEL] ★★ o invariante vale em todo instante antes da parada: `Ω²·E = K`. -/
theorem invariant (t : ℝ) (ht : t < D.t0) : D.omegaSq t * D.E t = D.K := by
  unfold omegaSq
  have hE : D.E t ≠ 0 := (D.E_pos_before t ht).ne'
  first | (field_simp; ring) | field_simp

/-- [KERNEL] ★★★ **A INSCRIÇÃO DO ZERO NO INFINITO**: antes da parada, a frequência² não tem cota — o zero só se inscreve com frequência infinita. -/
theorem frequency_squared_unbounded_at_the_stop (B : ℝ) : ∃ t : ℝ, t < D.t0 ∧ B < D.omegaSq t := by
  have hB1 : 0 < |B| + 1 := by positivity
  set ε : ℝ := min (D.E0 / 2) (D.K / (|B| + 1)) with hε
  have hε_pos : 0 < ε := lt_min (by have := D.E0_pos; positivity) (div_pos D.K_pos hB1)
  have hε_le : ε ≤ D.K / (|B| + 1) := min_le_right _ _
  have hε_lt : ε < D.E0 := lt_of_le_of_lt (min_le_left _ _) (by have := D.E0_pos; linarith)
  have hc : D.c ≠ 0 := D.c_pos.ne'
  refine ⟨(D.E0 - ε) / D.c, ?_, ?_⟩
  · unfold t0
    exact div_lt_div_of_pos_right (by linarith) D.c_pos
  · have hEt : D.E ((D.E0 - ε) / D.c) = ε := by
      unfold E
      first | (field_simp; ring) | field_simp
    unfold omegaSq
    rw [hEt]
    have h1 : |B| + 1 ≤ D.K / ε := by
      rw [le_div_iff₀ hε_pos]
      have hne : |B| + 1 ≠ 0 := hB1.ne'
      calc (|B| + 1) * ε ≤ (|B| + 1) * (D.K / (|B| + 1)) := by gcongr
        _ = D.K := by first | (field_simp; ring) | field_simp
    linarith [le_abs_self B]

/-- [KERNEL] ★★ **O CONTRASTE COM O ABISMO**: com taxa CONSTANTE `Γ`, a energia `E₀·e^(−Γt)` nunca toca o zero (cf. `Fundacao.the_fall_never_lands`). -/
theorem with_constant_rate_the_fall_never_lands (Γ t : ℝ) : 0 < D.E0 * Real.exp (-(Γ * t)) :=
  mul_pos D.E0_pos (Real.exp_pos _)

/-- [KERNEL] ★★★ **A RESSONÂNCIA QUE PERMANECE**: o corte quântico `ħΩ = E`, isto é `ħ²·Ω² = E²`, acontece exatamente quando `E³ = ħ²·K`.
    A energia do corte é a escala que o invariante gera «no infinito». -/
theorem the_residual_resonance_iff (ħ t : ℝ) (ht : t < D.t0) :
    ħ ^ 2 * D.omegaSq t = (D.E t) ^ 2 ↔ (D.E t) ^ 3 = ħ ^ 2 * D.K := by
  have hE : D.E t ≠ 0 := (D.E_pos_before t ht).ne'
  unfold omegaSq
  rw [mul_div_assoc', div_eq_iff hE]
  constructor
  · intro h
    rw [h]
    ring
  · intro h
    rw [← h]
    ring

/-- [KERNEL] ★★★ **A ESCALA É O INVARIANTE** — a parede, nomeada: se a energia do corte é `E★` (com `E★³ = ħ²K`) e a nota é `U = e^(−1/2)·E★`
    (a tônica √e descida meio-tom), então o invariante do disco é `K = (e^(1/2)·U)³/ħ²`. Qual disco tem esse `Ω²·E` é a pergunta que fica. -/
theorem the_scale_is_the_invariant (ħ Estar U : ℝ) (hħ : ħ ≠ 0) (hcut : Estar ^ 3 = ħ ^ 2 * D.K)
    (hU : U = Real.exp (-(1 / 2 : ℝ)) * Estar) :
    D.K = (Real.exp (1 / 2) * U) ^ 3 / ħ ^ 2 := by
  have hex : Real.exp (1 / 2) * Real.exp (-(1 / 2 : ℝ)) = 1 := by
    rw [← Real.exp_add]
    norm_num
  have hE : Real.exp (1 / 2) * U = Estar := by
    rw [hU, ← mul_assoc, hex, one_mul]
  rw [hE, hcut]
  have h2 : ħ ^ 2 ≠ 0 := pow_ne_zero 2 hħ
  first | (field_simp; ring) | field_simp

end Disco


/-! ### 01/11/2026 — ordem do operador («tudo derivado»): β não é campo livre do disco — vem do acoplamento -/

/-- O DISCO DO ACOPLAMENTO: `β` vem de `TGLCoupling` (β = α·√e), com a positividade do kernel; restam os DADOS do disco — `K` (= 6Mg² no
    disco real), `τ` e `E₀` —, que são a identidade do disco, não hipóteses sobre a teoria. -/
noncomputable def Disco.doAcoplamento (c : TGLCoupling) (K : ℝ) (hK : 0 < K) (τ : ℝ) (hτ : 0 < τ) (E0 : ℝ) (hE : 0 < E0) : Disco where
  K := K
  K_pos := hK
  beta := c.beta
  beta_pos := c.beta_pos
  tau := τ
  tau_pos := hτ
  E0 := E0
  E0_pos := hE

/-- [KERNEL] o β do disco do acoplamento é o β da teoria. -/
theorem Disco.doAcoplamento_beta (c : TGLCoupling) (K : ℝ) (hK : 0 < K) (τ : ℝ) (hτ : 0 < τ) (E0 : ℝ) (hE : 0 < E0) :
    (Disco.doAcoplamento c K hK τ hτ E0 hE).beta = c.beta := rfl

end TGLExt.DiscoDeEuler

#print axioms TGLExt.DiscoDeEuler.Disco.c_pos
#print axioms TGLExt.DiscoDeEuler.Disco.E_linear
#print axioms TGLExt.DiscoDeEuler.Disco.stops_in_finite_time
#print axioms TGLExt.DiscoDeEuler.Disco.t0_pos
#print axioms TGLExt.DiscoDeEuler.Disco.E_pos_before
#print axioms TGLExt.DiscoDeEuler.Disco.the_loss_is_the_canonical_law
#print axioms TGLExt.DiscoDeEuler.Disco.invariant
#print axioms TGLExt.DiscoDeEuler.Disco.frequency_squared_unbounded_at_the_stop
#print axioms TGLExt.DiscoDeEuler.Disco.with_constant_rate_the_fall_never_lands
#print axioms TGLExt.DiscoDeEuler.Disco.the_residual_resonance_iff
#print axioms TGLExt.DiscoDeEuler.Disco.the_scale_is_the_invariant
#print axioms TGLExt.DiscoDeEuler.Disco.doAcoplamento_beta
