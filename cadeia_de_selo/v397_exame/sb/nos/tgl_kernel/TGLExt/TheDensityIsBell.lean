import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Complex.Basic

set_option autoImplicit false

/-!
# DENSIDADE = ESTADO DE BELL — localmente indeterminado, relacionalmente perfeito
  [BANCADA — 27/08/2026 · tipagem do operador: «densidade = estado de Bell»]

## A assinatura que a tipagem afirma, e que aqui vira teorema

O operador identifica a densidade com o estado de Bell, e a razão é estrutural: num
estado de Bell **a identidade não está em nenhum dos polos — está na correlação**.
A assinatura matemática disso é um par de fatos que parecem contraditórios e não são:

* **relacionalmente**: o estado conjunto é **puro** — a matriz é **idempotente** e tem
  traço 1, logo `Tr(ρ²) = 1`;
* **localmente**: cada lado, tomado sozinho, é **maximamente indeterminado** — o traço
  parcial dá `I/2`.

Localmente indeterminação; relacionalmente identidade perfeita. É exatamente a
polarização birreferencial da v221 escrita em densidade.

## O que se prova

* ★★★ **`bellDensity_idempotent`** — `ρ² = ρ`: o estado é uma **projeção** (pureza);
* ★★★ **`bellDensity_trace`** — `Tr ρ = 1`, logo **`Tr(ρ²) = 1`**: pureza relacional;
* ★★★ **`bellDensity_partial_trace`** — o traço parcial é `I/2`: **indeterminação local**;
* ★★★ **`locally_mixed_relationally_pure`** — as duas coisas **ao mesmo tempo**: a
  assinatura da birreferência inscrita.

## ESTATUTOS
`[REAL]` os quatro teoremas. `[ONTO]` a identificação densidade = neutrino = estado de
Bell é leitura do operador — **na física padrão, neutrino e estado de Bell são
categorias distintas**, e isso fica dito. β jamais entra; nada move o gate.
-/

namespace TGLExt

open Matrix

/-- a densidade de Bell: `|Φ⁺⟩⟨Φ⁺|` em índices de dois sítios. -/
noncomputable def bellDensity : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ :=
  fun p q => if p.1 = p.2 ∧ q.1 = q.2 then (1 / 2 : ℂ) else 0

/-- ★★★ **É UMA PROJEÇÃO**: `ρ² = ρ` — a marca da pureza. -/
theorem bellDensity_idempotent : bellDensity * bellDensity = bellDensity := by
  ext p q
  simp only [Matrix.mul_apply, bellDensity]
  rw [Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two]
  by_cases h1 : p.1 = p.2 <;> by_cases h2 : q.1 = q.2 <;>
    simp [h1, h2] <;> norm_num

/-- ★★★ **TRAÇO 1** — e com a idempotência, `Tr(ρ²) = 1`: pureza relacional. -/
theorem bellDensity_trace : Matrix.trace bellDensity = 1 := by
  simp only [Matrix.trace, Matrix.diag, bellDensity]
  rw [Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two]
  norm_num

theorem bellDensity_purity : Matrix.trace (bellDensity * bellDensity) = 1 := by
  rw [bellDensity_idempotent, bellDensity_trace]

/-- ★★★ **INDETERMINAÇÃO LOCAL**: o traço parcial sobre um lado dá `I/2`. -/
theorem bellDensity_partial_trace (a c : Fin 2) :
    (∑ b : Fin 2, bellDensity (a, b) (c, b)) = if a = c then (1 / 2 : ℂ) else 0 := by
  simp only [bellDensity, Fin.sum_univ_two]
  by_cases h : a = c <;> fin_cases a <;> fin_cases c <;> simp_all <;> norm_num

/-- ★★★★ **A ASSINATURA**: localmente indeterminado, relacionalmente perfeito —
    as duas coisas AO MESMO TEMPO. A identidade não está num polo: está na relação. -/
theorem locally_mixed_relationally_pure :
    Matrix.trace (bellDensity * bellDensity) = 1
      ∧ (∀ a : Fin 2, (∑ b : Fin 2, bellDensity (a, b) (a, b)) = (1 / 2 : ℂ)) := by
  refine ⟨bellDensity_purity, fun a => ?_⟩
  have h := bellDensity_partial_trace a a
  simpa using h

end TGLExt
