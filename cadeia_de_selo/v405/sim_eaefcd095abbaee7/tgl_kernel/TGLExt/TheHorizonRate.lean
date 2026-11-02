import TGLExt.ThePhysicalHorizon

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# κ É TESTEMUNHA ESTRUTURAL, NUNCA INCÓGNITA — FP-5 como regra de tipos
  [BANCADA — 24/08/2026 · frente 6 da derivação do operador]

## A regra do operador

> *"κ é testemunha de uma condição estrutural, não alvo de uma equação de inversão…
> `∃κ, IsHorizonRate(κ, U_phys, K_W)` é permitido; `IsHorizonRate(κ,…) ⟹ δQ = κδA/8πG`
> é permitido; **fica proibido `κ = F(α, β, θ_M, …)` como objetivo de busca**.
> Não remover κ das equações; remover κ da função objetivo."*

FP-5 do catálogo de falsos positivos (a busca por expressão está PROIBIDA — a lição paga:
o T10 com 536.884 expressões mostrou que κ* pontua como alvos falsos). Aqui a proibição
vira TIPO: κ é um CAMPO da estrutura — dado carregado, jamais derivado. O construtor
aceita QUALQUER κ real: é exatamente o ponto — a estrutura pina o PAPEL de κ (a taxa do
gerador do fluxo do horizonte), não o seu valor.

## O que se prova

O gerador entra pela BASE PRÓPRIA (`K = diag(spec)` — todo hermitiano diagonaliza,
teorema espectral [KNOWN]; a testemunha é apresentada na base própria, que é o formato
honesto): `flow τ = diag(exp(−i·κ·τ·specᵢ))` — **a taxa vive NA DEFINIÇÃO do fluxo**.

* ★★ `flow_zero` — `U(0) = 1`;
* ★★★ `flow_group` — `U(τ+σ) = U(τ)·U(σ)` — a condição estrutural INTEIRA de que κ é taxa;
* ★★ `flow_unitary_diag` — cada entrada tem módulo 1: o fluxo é unitário;
* ★ `mkHorizonRate` — construtor EXPLÍCITO para qualquer `(κ, spec)` (termo, jamais
  `Nonempty`): *todo κ é testemunhável; nenhum κ é derivável.*

Sem sorry, sem axiom. β jamais entra. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- **O TIPO DE FP-5**: κ como testemunha estrutural — a taxa do gerador do fluxo do
    horizonte, na base própria do gerador. κ é DADO (campo); o fluxo o carrega por
    definição; NENHUM campo o deriva de coisa alguma. -/
structure HorizonRateWitness (n : Type) [Fintype n] [DecidableEq n] where
  /-- a taxa — testemunha, nunca incógnita. -/
  kappa : ℝ
  /-- o espectro real do gerador hermitiano (a base própria do `K` da cunha). -/
  spec : n → ℝ
  /-- o fluxo do horizonte, com a taxa NA definição:
      `U(τ) = diag(exp(−i·κ·τ·specᵢ))`. -/
  flow : ℝ → Matrix n n ℂ
  flow_def : ∀ τ : ℝ, flow τ
    = Matrix.diagonal (fun i => Complex.exp ((-Complex.I) * kappa * τ * (spec i)))

/-- ★★ `U(0) = 1`: o fluxo parte da identidade. -/
theorem flow_zero (W : HorizonRateWitness n) : W.flow 0 = 1 := by
  rw [W.flow_def]
  simp

/-- ★★★ **A LEI DE GRUPO**: `U(τ+σ) = U(τ)·U(σ)` — a condição estrutural que FAZ de κ
    uma taxa (fases do MESMO gerador somam). -/
theorem flow_group (W : HorizonRateWitness n) (τ σ : ℝ) :
    W.flow (τ + σ) = W.flow τ * W.flow σ := by
  rw [W.flow_def, W.flow_def, W.flow_def, Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- ★★ **O FLUXO É UNITÁRIO** (na diagonal): cada fase tem módulo 1 —
    `‖exp(−iκτ·specᵢ)‖ = 1`. O horizonte gira, não dissipa. -/
theorem flow_unitary_diag (W : HorizonRateWitness n) (τ : ℝ) (i : n) :
    ‖Complex.exp ((-Complex.I) * W.kappa * τ * (W.spec i))‖ = 1 := by
  have h : ((-Complex.I) * W.kappa * τ * (W.spec i))
      = Complex.I * ((-(W.kappa * τ * W.spec i) : ℝ) : ℂ) := by
    push_cast
    ring
  rw [h, Complex.norm_exp]
  simp

/-- ★ **TODO κ É TESTEMUNHÁVEL** — construtor explícito (termo, jamais `Nonempty`):
    a estrutura aceita qualquer taxa real; o que ela pina é o PAPEL, não o valor.
    *A proibição FP-5 lida ao contrário: se κ fosse derivável, este construtor seria
    parcial.* -/
noncomputable def mkHorizonRate (κ : ℝ) (d : n → ℝ) : HorizonRateWitness n where
  kappa := κ
  spec := d
  flow := fun τ => Matrix.diagonal (fun i => Complex.exp ((-Complex.I) * κ * τ * (d i)))
  flow_def := fun _ => rfl

/-- ★ o fecho: para todo κ e todo espectro, a testemunha existe, parte de 1 e satisfaz
    o grupo — κ está NAS equações e FORA da função objetivo. -/
theorem every_rate_is_witnessable (κ : ℝ) (d : n → ℝ) :
    (mkHorizonRate κ d).kappa = κ
    ∧ (mkHorizonRate (n := n) κ d).flow 0 = 1
    ∧ ∀ τ σ : ℝ, (mkHorizonRate (n := n) κ d).flow (τ + σ)
        = (mkHorizonRate (n := n) κ d).flow τ * (mkHorizonRate (n := n) κ d).flow σ :=
  ⟨rfl, flow_zero _, flow_group _⟩

end TGLExt
