import TGLExt.LeftRight

set_option autoImplicit false

/-!
# Tomita–Takesaki finito-dimensional   [TGLExt — Degrau 0]

O núcleo algébrico do teorema de Tomita–Takesaki em `H = Mₙ(ℂ)` com a forma
de Frobenius, para um estado de Gibbs `ρ` positivo-definido:

* `Ω := √ρ` (CFC) é cíclico e separador para a multiplicação à esquerda;
* `S(xΩ) = xᴴΩ` com `S y = Ω⁻¹ yᴴ Ω`, e `S² = id`;
* decomposição polar `S = J ∘ Δ^{1/2}` com `J z = zᴴ` (LeftRight.lean) e
  `Δ^{1/2} y = Ω y Ω⁻¹`, `Δ y = ρ y ρ⁻¹`;
* `Δ ≥ 0` na forma de Frobenius; `ΔΩ = Ω`; `JΩ = Ω`;
* KMS na forma de Gibbs: `ω(ab) = ω(b·Δ(a))` — a continuação analítica
  `t = −i` do fluxo modular, SEM potências imaginárias (`ρ^{it}` fica para
  a pedra futura `ModularFlow.lean`).

β NÃO entra aqui: isto é infraestrutura pura, ρ genérico. Sem sorry, sem
axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ)

/-- O vetor GNS do estado de Gibbs: `Ω = √ρ` (raiz psd via cálculo funcional). -/
def Omega : Matrix n n ℂ := CFC.sqrt ρ

/-- O operador de Tomita `S y = Ω⁻¹ yᴴ Ω` (a extensão total de `xΩ ↦ xᴴΩ`). -/
def Sop (y : Matrix n n ℂ) : Matrix n n ℂ := (Omega ρ)⁻¹ * yᴴ * Omega ρ

/-- A raiz do operador modular: `Δ^{1/2} y = Ω y Ω⁻¹`. -/
def DeltaHalf (y : Matrix n n ℂ) : Matrix n n ℂ := Omega ρ * y * (Omega ρ)⁻¹

/-- O operador modular: `Δ y = ρ y ρ⁻¹`. -/
def Delta (y : Matrix n n ℂ) : Matrix n n ℂ := ρ * y * ρ⁻¹

/-- O estado de Gibbs `ω(a) = Tr(ρ a)`. -/
def gibbs (a : Matrix n n ℂ) : ℂ := (ρ * a).trace

/-! ## Bloco 0 — fatos sobre Ω (a régua: cada fato compila antes do seguinte) -/

omit [Fintype n] [DecidableEq n] in
theorem rho_nonneg (hρ : ρ.PosDef) : (0 : Matrix n n ℂ) ≤ ρ :=
  hρ.posSemidef.nonneg

/-- [KERNEL] `Ω · Ω = ρ`: a raiz é raiz. -/
theorem omega_mul_self (hρ : ρ.PosDef) : Omega ρ * Omega ρ = ρ :=
  CFC.sqrt_mul_sqrt_self ρ (rho_nonneg ρ hρ)

/-- [KERNEL] `Ωᴴ = Ω`: a raiz psd é hermitiana. -/
theorem omega_conjTranspose : (Omega ρ)ᴴ = Omega ρ :=
  (CFC.sqrt_nonneg ρ).posSemidef.isHermitian

/-- [KERNEL] `Ω` é positiva-definida quando `ρ` o é. -/
theorem omega_posDef (hρ : ρ.PosDef) : (Omega ρ).PosDef :=
  (CFC.sqrt_nonneg ρ).posSemidef.posDef_iff_isUnit.mpr
    ((CFC.isUnit_sqrt_iff ρ (rho_nonneg ρ hρ)).mpr hρ.isUnit)

theorem omega_det_isUnit (hρ : ρ.PosDef) : IsUnit (Omega ρ).det :=
  (Omega ρ).isUnit_iff_isUnit_det.mp (omega_posDef ρ hρ).isUnit

theorem rho_det_isUnit (hρ : ρ.PosDef) : IsUnit ρ.det :=
  ρ.isUnit_iff_isUnit_det.mp hρ.isUnit

/-- [KERNEL] `ρ` comuta com sua raiz (pura álgebra: `ρΩ = ΩΩΩ = Ωρ`). -/
theorem rho_comm_omega (hρ : ρ.PosDef) : ρ * Omega ρ = Omega ρ * ρ := by
  have h := omega_mul_self ρ hρ
  calc ρ * Omega ρ = Omega ρ * Omega ρ * Omega ρ := by rw [h]
    _ = Omega ρ * (Omega ρ * Omega ρ) := mul_assoc _ _ _
    _ = Omega ρ * ρ := by rw [h]

/-- [KERNEL] `ρ⁻¹ = Ω⁻¹ Ω⁻¹`. -/
theorem rho_inv_eq (hρ : ρ.PosDef) : ρ⁻¹ = (Omega ρ)⁻¹ * (Omega ρ)⁻¹ := by
  have h := omega_mul_self ρ hρ
  calc ρ⁻¹ = (Omega ρ * Omega ρ)⁻¹ := by rw [h]
    _ = (Omega ρ)⁻¹ * (Omega ρ)⁻¹ := Matrix.mul_inv_rev _ _

/-- [KERNEL] `(Ω⁻¹)ᴴ = Ω⁻¹`. -/
theorem omega_inv_conjTranspose : ((Omega ρ)⁻¹)ᴴ = (Omega ρ)⁻¹ := by
  rw [Matrix.conjTranspose_nonsing_inv, omega_conjTranspose]

/-! ## Ω é cíclico e separador -/

/-- [KERNEL] Ω é CÍCLICO: todo vetor de H é `xΩ` (dimensão finita + Ω invertível). -/
theorem omega_cyclic (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    ∃ x, Lmul x (Omega ρ) = y :=
  ⟨y * (Omega ρ)⁻¹, by
    simp only [Lmul_apply]
    rw [mul_assoc, Matrix.nonsing_inv_mul _ (omega_det_isUnit ρ hρ), mul_one]⟩

/-- [KERNEL] Ω é SEPARADOR: `xΩ = 0 ⟹ x = 0`. -/
theorem omega_separating (hρ : ρ.PosDef) (x : Matrix n n ℂ)
    (h : Lmul x (Omega ρ) = 0) : x = 0 := by
  simp only [Lmul_apply] at h
  have h2 : x * Omega ρ * (Omega ρ)⁻¹ = 0 * (Omega ρ)⁻¹ := by rw [h]
  rwa [Matrix.mul_nonsing_inv_cancel_right _ _ (omega_det_isUnit ρ hρ), zero_mul] at h2

/-! ## O operador de Tomita e a decomposição polar -/

/-- [KERNEL] A EQUAÇÃO DE TOMITA: `S(xΩ) = xᴴΩ` — o operador que troca
    a face interna pela externa sobre o vetor GNS. -/
theorem Sop_tomita (hρ : ρ.PosDef) (x : Matrix n n ℂ) :
    Sop ρ (Lmul x (Omega ρ)) = Lmul xᴴ (Omega ρ) := by
  simp only [Sop, Lmul_apply, conjTranspose_mul, omega_conjTranspose]
  rw [Matrix.nonsing_inv_mul_cancel_left _ _ (omega_det_isUnit ρ hρ)]

/-- [KERNEL] `S` é involutivo: `S² = id`. -/
theorem Sop_involutive (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    Sop ρ (Sop ρ y) = y := by
  simp only [Sop, conjTranspose_mul, Matrix.conjTranspose_nonsing_inv,
    omega_conjTranspose, conjTranspose_conjTranspose]
  rw [Matrix.nonsing_inv_mul_cancel_left _ _ (omega_det_isUnit ρ hρ),
    mul_assoc, Matrix.nonsing_inv_mul _ (omega_det_isUnit ρ hρ), mul_one]

/-- [KERNEL] DECOMPOSIÇÃO POLAR: `J ∘ Δ^{1/2} = S` — a conjugação de
    LeftRight.lean composta com a raiz modular É o operador de Tomita. -/
theorem J_deltaHalf (y : Matrix n n ℂ) : Jconj (DeltaHalf ρ y) = Sop ρ y := by
  simp only [Jconj, DeltaHalf, Sop, conjTranspose_mul,
    Matrix.conjTranspose_nonsing_inv, omega_conjTranspose, mul_assoc]

/-- [KERNEL] `Δ^{1/2} ∘ Δ^{1/2} = Δ` (não usa invertibilidade!). -/
theorem deltaHalf_deltaHalf (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    DeltaHalf ρ (DeltaHalf ρ y) = Delta ρ y := by
  calc DeltaHalf ρ (DeltaHalf ρ y)
      = Omega ρ * (Omega ρ * y * (Omega ρ)⁻¹) * (Omega ρ)⁻¹ := rfl
    _ = Omega ρ * Omega ρ * y * ((Omega ρ)⁻¹ * (Omega ρ)⁻¹) := by
        simp only [mul_assoc]
    _ = ρ * y * ρ⁻¹ := by rw [omega_mul_self ρ hρ, ← rho_inv_eq ρ hρ, mul_assoc]

/-- [KERNEL] `ΔΩ = Ω`: o vetor GNS é ponto fixo do operador modular. -/
theorem delta_omega (hρ : ρ.PosDef) : Delta ρ (Omega ρ) = Omega ρ := by
  show ρ * Omega ρ * ρ⁻¹ = Omega ρ
  rw [rho_comm_omega ρ hρ, Matrix.mul_nonsing_inv_cancel_right _ _ (rho_det_isUnit ρ hρ)]

/-- [KERNEL] `JΩ = Ω`: o vetor GNS é ponto fixo da conjugação. -/
theorem J_omega : Jconj (Omega ρ) = Omega ρ :=
  omega_conjTranspose ρ

/-! ## Positividade de Δ -/

/-- [KERNEL] `⟨y, Δy⟩ = ⟨Δ^{1/2}y, Δ^{1/2}y⟩`: Δ é o quadrado da sua raiz
    também na forma de Frobenius. -/
theorem frob_delta_eq (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    frob y (Delta ρ y) = frob (DeltaHalf ρ y) (DeltaHalf ρ y) := by
  have hS : (DeltaHalf ρ y)ᴴ = (Omega ρ)⁻¹ * yᴴ * Omega ρ := J_deltaHalf ρ y
  simp only [frob]
  rw [hS]
  simp only [Delta, DeltaHalf, mul_assoc]
  conv_rhs => rw [Matrix.trace_mul_comm]
  simp only [mul_assoc]
  rw [← mul_assoc (Omega ρ) (Omega ρ), omega_mul_self ρ hρ, ← rho_inv_eq ρ hρ]

/-- [KERNEL] POSITIVIDADE do operador modular: `0 ≤ ⟨y, Δy⟩` (ordem de ℂ). -/
theorem frob_delta_nonneg (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    0 ≤ frob y (Delta ρ y) := by
  rw [frob_delta_eq ρ hρ y]
  exact (Matrix.posSemidef_conjTranspose_mul_self (DeltaHalf ρ y)).trace_nonneg

/-- [KERNEL] A mesma positividade em partes real/imaginária explícitas. -/
theorem frob_delta_re_im (hρ : ρ.PosDef) (y : Matrix n n ℂ) :
    0 ≤ (frob y (Delta ρ y)).re ∧ (frob y (Delta ρ y)).im = 0 := by
  have h := frob_delta_nonneg ρ hρ y
  rw [Complex.nonneg_iff] at h
  exact ⟨h.1, h.2.symm⟩

/-! ## KMS na forma de Gibbs -/

/-- [KERNEL] KMS: `ω(ab) = ω(b·Δ(a))` — a condição de equilíbrio modular
    na forma algébrica (a continuação `t = −i` do fluxo, sem `ρ^{it}`).
    Pura ciclicidade do traço + cancelamento não-singular. -/
theorem gibbs_kms (hρ : ρ.PosDef) (a b : Matrix n n ℂ) :
    gibbs ρ (a * b) = gibbs ρ (b * Delta ρ a) := by
  simp only [gibbs, Delta]
  conv_rhs => rw [Matrix.trace_mul_comm]
  simp only [mul_assoc]
  rw [Matrix.nonsing_inv_mul _ (rho_det_isUnit ρ hρ), mul_one]
  conv_rhs => rw [Matrix.trace_mul_comm]
  simp only [mul_assoc]

/-- `ω(1) = 1` sse `Tr ρ = 1` — a normalização de estado é EXTERNA aos
    teoremas 3–6 (nota honesta: nenhum deles a usa). -/
theorem gibbs_one (hτ : ρ.trace = 1) : gibbs ρ 1 = 1 := by
  simp only [gibbs, mul_one, hτ]

/-- [KERNEL] `ω(a) = ⟨Ω, aΩ⟩`: o estado de Gibbs é o estado vetorial do
    vetor GNS — a ponte entre LeftRight.lean e este arquivo. -/
theorem gibbs_eq_frob_omega (hρ : ρ.PosDef) (a : Matrix n n ℂ) :
    gibbs ρ a = frob (Omega ρ) (Lmul a (Omega ρ)) := by
  simp only [gibbs, frob, Lmul_apply, omega_conjTranspose]
  conv_rhs => rw [Matrix.trace_mul_comm]
  rw [mul_assoc, omega_mul_self ρ hρ, Matrix.trace_mul_comm]

end

end TGLExt
