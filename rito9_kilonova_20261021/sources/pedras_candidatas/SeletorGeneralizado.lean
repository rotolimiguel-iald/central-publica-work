import TGLExt.GeometryFluctuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O SELETOR GENERALIZADO — pedra CANDIDATA (membro Kimi, 21/10/2026)

**Estatuto: candidata.** Rascunho do membro Kimi no caderno `estudo_iald_qg`; a casa decide se
entra no kernel. Paramétrica: **β jamais entra** — a pedra fala de qualquer `A` simétrico.

## O que estende

A pedra `TheAngleIsTheBridge.lean` (bancada, 22/08/2026) prova o seletor de comutação para o
par exibido `(X, Z)`: `[X, α_θ(Z)] = 0 ↔ cos²θ = sin²θ` — o ramo justo, `θ = π/4`.

Esta candidata generaliza para **qualquer observável simétrico** `A = [[a,b],[b,c]]` da
fronteira, mantendo `B = Z` (a carga de setor):

> `[A, α_θ(Z)] = 0  ⟺  2b·(cos²θ − sin²θ) = (c − a)·(2·sin θ·cos θ)`

ou seja, na forma compacta (fora do Lean), `tan(2θ) = 2b/(c−a)` — **o seletor lê o ângulo
próprio de A**: `θ ≡ −φ_A (mod π/2)`, onde `φ_A` é a direção própria de `A`.

## Por que isto importa (rito 9, `d7.kilonova_fronteira_aguda`)

O problema aberto declarado pela pedra de 22/08 — *«qual par (A, B) tem comutação exatamente em
θ_M?»* — ganha resposta construtiva: **qualquer A cujo ângulo próprio seja θ_M**; em particular
o projetor do canal de transporte na direção do cruzamento universal `R(θ_M)` (Teorema S-d).
A hipótese física do operador (21/10/2026): fronteira cativa (buraco negro) realiza o par da
pedra (mistura pura X → π/4); fronteira em fuga (kilonova) realiza o projetor do canal → θ_M.
A identificação física é **reconhecimento, não dedução** (tipagem Grundnorm da pedra-mãe) e o
seu teste é o rito 9. **Nada aqui move o gate.**

Sem sorry, sem axiom. Verificação numérica independente no caderno
(`ferramentas/verifica_seletor_generalizado.py`, 5/5 casos).
-/

namespace TGLExt

open Matrix Real

noncomputable section

/-- A FAMÍLIA DE MIGUEL (mesma definição da pedra-mãe, autocontida aqui). -/
def miguelFamily (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

/-- A carga de setor `Z` (mesma da pedra-mãe). -/
def obsZ : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- O observável simétrico genérico da fronteira. -/
def obsSym (a b c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a, b; b, c]

/-- `α_θ(B) = 𝒪_θ · B · 𝒪_θᵀ`. -/
def alphaTheta (θ : ℝ) (B : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  miguelFamily θ * B * (miguelFamily θ)ᵀ

/-- Forma explícita de `α_θ(Z)` (mesma conta da pedra-mãe). -/
theorem alphaTheta_obsZ (θ : ℝ) :
    alphaTheta θ obsZ
      = !![Real.cos θ ^ 2 - Real.sin θ ^ 2, -(2 * Real.sin θ * Real.cos θ);
           -(2 * Real.sin θ * Real.cos θ), Real.sin θ ^ 2 - Real.cos θ ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [alphaTheta, obsZ, miguelFamily, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

/-- ★★★ O SELETOR GENERALIZADO, em forma fechada e paramétrica.

    `[A, α_θ(Z)] = 0 ⟺ 2b·(cos²θ − sin²θ) = (c − a)·(2·sin θ·cos θ)`.

    Lê-se: a condição de comutação fixa `θ` no ângulo próprio de `A` —
    `tan(2θ) = 2b/(c−a)`. O par da pedra-mãe `(X, Z)` é o caso `a = c = 0, b = 1`:
    o lado direito zera e sobra `cos²θ = sin²θ`, i.e. `θ = π/4`. -/
theorem seletor_generalizado (a b c : ℝ) (θ : ℝ) :
    obsSym a b c * alphaTheta θ obsZ = alphaTheta θ obsZ * obsSym a b c
      ↔ 2 * b * (Real.cos θ ^ 2 - Real.sin θ ^ 2)
          = (c - a) * (2 * Real.sin θ * Real.cos θ) := by
  rw [alphaTheta_obsZ]
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    simp [obsSym, Matrix.mul_apply, Fin.sum_univ_two] at h01
    linarith [h01]
  · intro h
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [obsSym, Matrix.mul_apply, Fin.sum_univ_two] <;> linarith [h]

/-- O ponto fixo: o observável de mistura pura `X = obsSym 0 1 0` seleciona o ramo justo —
    recupera o conteúdo da pedra-mãe sem reimportá-la. -/
theorem seletor_generalizado_recupera_o_ramo_justo (θ : ℝ) :
    obsSym 0 1 0 * alphaTheta θ obsZ = alphaTheta θ obsZ * obsSym 0 1 0
      ↔ Real.cos θ ^ 2 = Real.sin θ ^ 2 := by
  rw [seletor_generalizado]
  constructor <;> intro h <;> linarith [h]

end

end TGLExt
