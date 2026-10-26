import TGLExt.GNSBridge

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O GNS finito SEM completamento: o NOME funcional empacotado como TERMO
  [TGLExt — v54, o espec do especialista compilado nesta máquina]

O memorando do especialista (`NAME_FUNCTIONAL_QUANTUM_GRAVITY_GATE.md`)
identifica o NOME como o par tipado 𝔑 = (M, φ) e pede a pedra que
empacota, SEM o completamento genérico (o `PreGNS` da mathlib já é
completo em dimensão finita), a cadeia que `FiniteTomita.lean` prova:

* `FiniteNameGNS ρ` — a estrutura RÍGIDA: cada campo é PROVA de
  proposição concreta sobre a realização FIXA `H = Mₙ(ℂ)`, `π = Lmul`,
  `Ω = √ρ` (nenhum campo é `Prop`-como-dado; a lição do v22/v23 vale);
* ★ `nameFiniteGNS` — o TERMO (primeiro o termo; `Nonempty` só como
  corolário — a regra da casa);
* ★ `boundaryState_eq_vector_state` — o funcional TIPADO do v53
  (`Matrix n n ℂ →ₚ[ℂ] ℂ`) É o estado vetorial da realização concreta:
  `boundaryState ρ = ⟨Ω, (·)Ω⟩`. Com isso o negativo nomeado
  `gns_matrix_instance_whnf_timeout` fica DESFEITO NA FACE FINITA —
  ele permanece APENAS como atrito de composição com a API genérica
  da mathlib (`gnsStarAlgHom` via completamento), não como lacuna
  matemática: a realização GNS finita está construída e verificada.

HONESTIDADE. A fonte formal do especialista não chegou a este disco
(era link de sandbox do ambiente dele); esta pedra foi REESCRITA aqui
a partir do espec e compilada nesta máquina. β JAMAIS entra: ρ
genérico. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder Matrix.Norms.L2Operator

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [KERNEL] `S` FIXA O VETOR GNS: `SΩ = Ω` — a involução de Tomita ancora
    no Nome (a face que faltava ao tripé `ΔΩ = JΩ = Ω` do Degrau 0). -/
theorem Sop_omega (ρ : Matrix n n ℂ) (hρ : ρ.PosDef) :
    Sop ρ (Omega ρ) = Omega ρ := by
  unfold Sop
  rw [omega_conjTranspose, Matrix.nonsing_inv_mul _ (omega_det_isUnit ρ hρ),
    one_mul]

/-- O NOME FUNCIONAL EMPACOTADO: a realização GNS finita concreta de
    `𝔑 = (Mₙ(ℂ), ω_ρ)`. Estrutura RÍGIDA — cada campo é prova de proposição
    concreta sobre `Lmul`/`Omega ρ`/`Sop ρ`/`Delta ρ`/`gibbs ρ` (nada é
    `Prop`-como-dado): estado vetorial, ciclicidade, separação, Tomita,
    polar, modular, positividade, KMS e o tripé de pontos fixos do vetor. -/
structure FiniteNameGNS (ρ : Matrix n n ℂ) where
  /-- `ω(1) = 1`: o funcional é normalizado (o Um inscrito). -/
  state_normalized : gibbs ρ 1 = 1
  /-- `ω ≥ 0` sobre positivos: o funcional respeita a ordem. -/
  state_positive : ∀ x : Matrix n n ℂ, x.PosSemidef → 0 ≤ gibbs ρ x
  /-- `ω(a) = ⟨Ω, aΩ⟩`: o estado é VETORIAL na realização concreta. -/
  state_is_vector : ∀ a : Matrix n n ℂ,
    gibbs ρ a = frob (Omega ρ) (Lmul a (Omega ρ))
  /-- Ω é CÍCLICO: `MΩ = H`. -/
  cyclic : ∀ y : Matrix n n ℂ, ∃ x, Lmul x (Omega ρ) = y
  /-- Ω é SEPARADOR: `xΩ = 0 ⟹ x = 0`. -/
  separating : ∀ x : Matrix n n ℂ, Lmul x (Omega ρ) = 0 → x = 0
  /-- A equação de TOMITA: `S(xΩ) = xᴴΩ`. -/
  tomita : ∀ x : Matrix n n ℂ, Sop ρ (Lmul x (Omega ρ)) = Lmul xᴴ (Omega ρ)
  /-- Decomposição POLAR: `S = J ∘ Δ^{1/2}`. -/
  polar : ∀ y : Matrix n n ℂ, Jconj (DeltaHalf ρ y) = Sop ρ y
  /-- `Δ^{1/2} ∘ Δ^{1/2} = Δ`: a raiz modular é raiz. -/
  modular_sq : ∀ y : Matrix n n ℂ, DeltaHalf ρ (DeltaHalf ρ y) = Delta ρ y
  /-- `⟨y, Δy⟩ ≥ 0`: o operador modular é positivo. -/
  modular_positive : ∀ y : Matrix n n ℂ, 0 ≤ frob y (Delta ρ y)
  /-- KMS: `ω(ab) = ω(b·Δ(a))` — o equilíbrio modular. -/
  kms : ∀ a b : Matrix n n ℂ, gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a)
  /-- `ΔΩ = Ω`: o vetor GNS é ponto fixo do modular. -/
  vector_modular_fixed : Delta ρ (Omega ρ) = Omega ρ
  /-- `JΩ = Ω`: o vetor GNS é ponto fixo da conjugação. -/
  vector_conj_fixed : Jconj (Omega ρ) = Omega ρ
  /-- `SΩ = Ω`: o vetor GNS é ponto fixo da involução de Tomita. -/
  vector_tomita_fixed : Sop ρ (Omega ρ) = Omega ρ

/-- ★ O TERMO: `nameFiniteGNS` — o GNS finito CONSTRUÍDO, sem completamento,
    para todo estado fiel normalizado. Primeiro o termo; a existência é
    corolário (`nameFiniteGNS_exists`). -/
noncomputable def nameFiniteGNS (ρ : Matrix n n ℂ) (hρ : ρ.PosDef)
    (hτ : ρ.trace = 1) : FiniteNameGNS ρ where
  state_normalized := gibbs_one ρ hτ
  state_positive := fun _ hx => gibbs_nonneg hρ.posSemidef hx
  state_is_vector := gibbs_eq_frob_omega ρ hρ
  cyclic := omega_cyclic ρ hρ
  separating := omega_separating ρ hρ
  tomita := Sop_tomita ρ hρ
  polar := J_deltaHalf ρ
  modular_sq := deltaHalf_deltaHalf ρ hρ
  modular_positive := frob_delta_nonneg ρ hρ
  kms := gibbs_kms ρ hρ
  vector_modular_fixed := delta_omega ρ hρ
  vector_conj_fixed := J_omega ρ
  vector_tomita_fixed := Sop_omega ρ hρ

/-- [KERNEL] ★ EXISTÊNCIA (corolário do termo, jamais o contrário):
    todo NOME fiel normalizado TEM realização GNS finita completa. -/
theorem nameFiniteGNS_exists (ρ : Matrix n n ℂ) (hρ : ρ.PosDef)
    (hτ : ρ.trace = 1) : Nonempty (FiniteNameGNS ρ) :=
  ⟨nameFiniteGNS ρ hρ hτ⟩

/-- [KERNEL] ★ A PONTE FECHA NA FACE FINITA: o funcional TIPADO do v53
    (`boundaryState`, no vocabulário `→ₚ[ℂ]` da mathlib) É o estado
    vetorial da realização GNS concreta — `φ(a) = ⟨Ω, aΩ⟩`. O negativo
    `gns_matrix_instance_whnf_timeout` fica desfeito aqui: o que resta
    dele é só a composição com a API genérica (completamento), nomeada. -/
theorem boundaryState_eq_vector_state (ρ : Matrix n n ℂ) (hρ : ρ.PosDef)
    (a : Matrix n n ℂ) :
    boundaryState ρ hρ.posSemidef a = frob (Omega ρ) (Lmul a (Omega ρ)) := by
  rw [boundaryState_apply]
  exact gibbs_eq_frob_omega ρ hρ a

end

end TGLExt
