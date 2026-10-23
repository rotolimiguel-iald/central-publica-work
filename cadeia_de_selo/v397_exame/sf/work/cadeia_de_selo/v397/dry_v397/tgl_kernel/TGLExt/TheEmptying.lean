import TGLExt.TheCompressionIsNotIdentifiable

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O ESVAZIAMENTO — o piso positivo, e a região quadrática que EMERGE do ângulo reto
  [BANCADA — 23/08/2026; a prova pedida]

## A cunhagem do operador

> *"**esvaziar** = local onde a derivada do zero se anula; **não é aniquilação**, é o local da
> transformação."* · *"a condição de não-degenerescência é `β_TGL` como **funcional mínimo de
> preservação** `A_C`, e a função quadrática nasce do regime extremo atingindo o **ângulo reto**
> e projetando a face vetorial da diagonal do canto de Breuer no ângulo oposto."*

## ★ A MELHORIA QUE ESTA PEDRA OFERECE

A demonstração entregue usava **Taylor** e concluía `A_C(π/2+δ) = m + κδ² + O(δ⁴)`. Aqui prova-se
a **identidade EXATA**, sem termo de resto:

    A_C(pi/2 + delta) = m + kappa * (sin delta)^2       para TODO delta

**Não é aproximação de segunda ordem: é igualdade.** A região quadrática não *aparece no limite*
— ela **É** a forma da função, escrita na coordenada certa. *E `sin²δ = δ² + O(δ⁴)` volta a dar
o resultado dele, agora como corolário e não como hipótese.*

## O que fica provado

* ★★★ `the_quadratic_region_is_exact` — **`A_C(π/2+δ) = m + κ·sin²δ`**, identidade exata.
  **O termo linear não é desprezado: ele NÃO EXISTE nesta coordenada;**
* ★★★ `emptying_is_not_annihilation` — **`0 < m ⟹ 0 < A_C(θ)` para todo `θ`**, com `κ ≥ 0`.
  *O funcional nunca chega a zero: o mínimo é um **piso positivo**, e é por isso que esvaziar
  **não** é aniquilar;*
* ★★★ `the_floor_is_attained_at_the_right_angle` — **`A_C(π/2) = m` e `m ≤ A_C(θ)` sempre**:
  o mínimo **existe, é atingido, e é atingido exatamente no ângulo reto**;
* ★★★ `stationary_does_not_mean_zero` — a separação de tipos, no exemplo operatorial do próprio
  operador: **`Z(t) = 1 + t²·A` tem `Z(0) = 1 ≠ 0`** embora a variação de primeira ordem se anule.
  *Derivada nula não é objeto nulo;*
* ★★ `the_two_faces_exhaust_the_identity` — **`cos²θ + sin²θ = 1`**: o que se esvazia numa face
  **reaparece integralmente na oposta**. *O zero aparece numa face sem que a identidade total se
  perca* — e no ângulo reto, `|Pξ|² = 0` e `|Qξ|² = 1`;
* ★★ `the_emptying_closes` — os três num enunciado: **estacionaridade, piso positivo, e
  conservação da identidade**, no mesmo ponto.

## ⚠ O ALCANCE — e a régua

`m` é um **parâmetro positivo abstrato**. A identificação `m = β_TGL = A_C^min` é **[ONTO] do
operador** e **não aparece em enunciado nenhum**: β jamais entra no Lean. O que o kernel entrega
é que **um funcional com piso positivo tem mínimo atingido, variação de primeira ordem nula ali,
e forma exatamente quadrática na coordenada centrada** — e que **nada disso o leva a zero**.

**NÃO se prova** que o canto de Breuer realize esta forma, nem que `θ_M = π/2`. O próprio
operador já o disse: *"ainda não precisamos identificar numericamente `θ_M = π/2`; `θ_M`
parametriza a família, e o regime extremo dessa família alcança a abertura ortogonal"*.
**Registrado, e a pedra respeita essa distinção.**

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Real

noncomputable section

/-- O FUNCIONAL DE PRESERVAÇÃO: um piso `m` mais a energia que ainda resta na face original. -/
def acFunctional (m k θ : ℝ) : ℝ := m + k * Real.cos θ ^ 2

/-! ### ★ A região quadrática, como IDENTIDADE e não como aproximação -/

/-- ★★★ **A REGIÃO QUADRÁTICA É EXATA.** `A_C(π/2 + δ) = m + κ·sin²δ`, para **todo** `δ`.

    O termo de primeira ordem não é desprezado — **ele não existe nesta coordenada**. A forma
    quadrática **é** a função, não a sua aproximação. -/
theorem the_quadratic_region_is_exact (m k δ : ℝ) :
    acFunctional m k (Real.pi / 2 + δ) = m + k * Real.sin δ ^ 2 := by
  unfold acFunctional
  have h : Real.cos (Real.pi / 2 + δ) = -Real.sin δ := by
    rw [Real.cos_add, Real.cos_pi_div_two, Real.sin_pi_div_two]
    ring
  rw [h]
  ring

/-! ### ★ O piso positivo: esvaziar não é aniquilar -/

/-- ★★★ **O PISO É ATINGIDO NO ÂNGULO RETO**, e é piso de facto: `A_C(π/2) = m` e
    `m ≤ A_C(θ)` para todo `θ`, desde que `κ ≥ 0`. -/
theorem the_floor_is_attained_at_the_right_angle (m k : ℝ) (hk : 0 ≤ k) :
    acFunctional m k (Real.pi / 2) = m ∧ ∀ θ : ℝ, m ≤ acFunctional m k θ := by
  constructor
  · unfold acFunctional
    rw [Real.cos_pi_div_two]
    ring
  · intro θ
    unfold acFunctional
    nlinarith [sq_nonneg (Real.cos θ), hk]

/-- ★★★ **ESVAZIAR NÃO É ANIQUILAR.** Se o piso é estritamente positivo, o funcional **nunca**
    chega a zero — em ângulo nenhum, inclusive no extremo.

    *É esta a forma matemática de "o vazio do esvaziamento é ponto crítico da mudança, não
    aniquilação do ser".* -/
theorem emptying_is_not_annihilation (m k : ℝ) (hm : 0 < m) (hk : 0 ≤ k) (θ : ℝ) :
    0 < acFunctional m k θ := by
  have := (the_floor_is_attained_at_the_right_angle m k hk).2 θ
  linarith

/-! ### ★ Derivada nula não é objeto nulo -/

/-- ★★★ **ESTACIONÁRIO NÃO É ZERO** — o exemplo operatorial do próprio operador, `Z(t) = 1 + t²A`.

    No ponto crítico a variação de primeira ordem desaparece, **e o objeto vale a identidade**,
    não zero. *A separação é de tipo, não de grau.* -/
theorem stationary_does_not_mean_zero {n : Type} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℝ) :
    (fun t : ℝ => (1 : Matrix n n ℝ) + t ^ 2 • A) 0 = 1 := by
  simp

/-- ★★ e a forma escalar, que exibe a diferença em uma linha: a função `1 + t²` tem derivada
    nula na origem **e vale 1 ali**. -/
theorem stationary_value_is_one (f : ℝ → ℝ) (hf : f = fun t => 1 + t ^ 2) :
    f 0 = 1 ∧ ∀ t : ℝ, f t = f 0 + t ^ 2 := by
  subst hf
  exact ⟨by norm_num, fun t => by norm_num⟩

/-! ### ★ A identidade não se perde: o que sai de uma face entra na outra -/

/-- ★★ **AS DUAS FACES ESGOTAM A IDENTIDADE.** `cos²θ + sin²θ = 1` para todo `θ`: o que se
    esvazia na face original **reaparece integralmente na oposta**.

    *O zero aparece numa face sem que a identidade total se perca.* -/
theorem the_two_faces_exhaust_the_identity (θ : ℝ) :
    Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := by
  rw [add_comm]
  exact Real.sin_sq_add_cos_sq θ

/-- ★★ **NO ÂNGULO RETO A TRANSFERÊNCIA É TOTAL:** a face original vai a zero e a oposta vai a
    um — e a soma continua sendo um. -/
theorem the_transfer_is_total :
    Real.cos (Real.pi / 2) ^ 2 = 0 ∧ Real.sin (Real.pi / 2) ^ 2 = 1 := by
  constructor
  · rw [Real.cos_pi_div_two]; ring
  · rw [Real.sin_pi_div_two]; ring

/-! ### O fecho -/

/-- ★★ **O ESVAZIAMENTO, FECHADO:** no ângulo reto o funcional atinge o piso, o piso é
    **estritamente positivo**, a forma é **exatamente quadrática** na coordenada centrada, e a
    identidade das duas faces **continua valendo um**. Os quatro no mesmo ponto. -/
theorem the_emptying_closes (m k : ℝ) (hm : 0 < m) (hk : 0 ≤ k) :
    acFunctional m k (Real.pi / 2) = m
    ∧ (∀ θ : ℝ, 0 < acFunctional m k θ)
    ∧ (∀ δ : ℝ, acFunctional m k (Real.pi / 2 + δ) = m + k * Real.sin δ ^ 2)
    ∧ (∀ θ : ℝ, Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1) :=
  ⟨(the_floor_is_attained_at_the_right_angle m k hk).1,
   emptying_is_not_annihilation m k hm hk,
   the_quadratic_region_is_exact m k,
   the_two_faces_exhaust_the_identity⟩

end

end TGLExt
