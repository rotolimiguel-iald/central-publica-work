import TGLExt.FiniteTomita

set_option autoImplicit false

/-!
# O fluxo modular σₜ = Ad(ρ^{it})   [TGLExt — fecho do Degrau 0]

O grupo unitário a um parâmetro do Tomita–Takesaki finito:
`ρ^{it} := exp(it·log ρ)` com `log ρ = cfc Real.log ρ`. Provamos:

* lei de grupo `ρ^{i(s+t)} = ρ^{is}·ρ^{it}` e `ρ^{i0} = 1`;
* unitariedade `(ρ^{it})ᴴ = ρ^{-it}` (pertence a `unitary`);
* `σₜ(a) = ρ^{it} a ρ^{-it}` é *-automorfismo com lei de grupo;
* invariância do estado de Gibbs `ω(σₜ(a)) = ω(a)` — KMS dinâmico;
* ancoragem `exp(log ρ) = ρ` (ρ positiva-definida);
* `σₜ` fixa o vetor GNS: `σₜ(Ω) = Ω`.

Com isto o Degrau 0 fecha por inteiro: S, Δ, J, S=J∘Δ^{1/2}, KMS-Gibbs
(FiniteTomita.lean) + o fluxo σₜ (aqui). β NÃO entra: ρ genérico.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n] (ρ : Matrix n n ℂ)

/-- O gerador modular: `log ρ` via cálculo funcional real. -/
def logRho : Matrix n n ℂ := cfc Real.log ρ

/-- `ρ^{it} := exp(it · log ρ)` — o unitário do fluxo modular. -/
def modPow (t : ℝ) : Matrix n n ℂ := exp (((t : ℂ) * Complex.I) • logRho ρ)

/-- O fluxo modular `σₜ(a) = ρ^{it} a ρ^{-it}`. -/
def sigma (t : ℝ) (a : Matrix n n ℂ) : Matrix n n ℂ :=
  modPow ρ t * a * modPow ρ (-t)

/-! ## O gerador é autoadjunto -/

theorem logRho_isSelfAdjoint : IsSelfAdjoint (logRho ρ) := cfc_predicate Real.log ρ

theorem logRho_conjTranspose : (logRho ρ)ᴴ = logRho ρ := logRho_isSelfAdjoint ρ

/-! ## F1–F2: identidade e lei de grupo -/

@[simp] theorem modPow_zero : modPow ρ 0 = 1 := by
  simp [modPow]

/-- [KERNEL] LEI DE GRUPO: `ρ^{i(s+t)} = ρ^{is}·ρ^{it}`. -/
theorem modPow_add (s t : ℝ) : modPow ρ (s + t) = modPow ρ s * modPow ρ t := by
  unfold modPow
  rw [Complex.ofReal_add, add_mul, add_smul]
  exact Matrix.exp_add_of_commute _ _
    (((Commute.refl (logRho ρ)).smul_left _).smul_right _)

theorem modPow_mul_neg (t : ℝ) : modPow ρ t * modPow ρ (-t) = 1 := by
  rw [← modPow_add, add_neg_cancel, modPow_zero]

theorem modPow_neg_mul (t : ℝ) : modPow ρ (-t) * modPow ρ t = 1 := by
  rw [← modPow_add, neg_add_cancel, modPow_zero]

/-! ## F3: unitariedade -/

/-- [KERNEL] `(ρ^{it})ᴴ = ρ^{-it}`: a adjunta do fluxo é o fluxo reverso. -/
theorem modPow_conjTranspose (t : ℝ) : (modPow ρ t)ᴴ = modPow ρ (-t) := by
  have hstar : star ((t : ℂ) * Complex.I) = -((t : ℂ) * Complex.I) := by
    simp
  have hneg : ((-t : ℝ) : ℂ) * Complex.I = -((t : ℂ) * Complex.I) := by
    push_cast; ring
  unfold modPow
  rw [← Matrix.exp_conjTranspose, Matrix.conjTranspose_smul,
      logRho_conjTranspose, hstar, hneg]

/-- [KERNEL] `ρ^{it}` é UNITÁRIO. -/
theorem modPow_mem_unitary (t : ℝ) : modPow ρ t ∈ unitary (Matrix n n ℂ) := by
  rw [Unitary.mem_iff]
  constructor <;> rw [Matrix.star_eq_conjTranspose, modPow_conjTranspose]
  · exact modPow_neg_mul ρ t
  · exact modPow_mul_neg ρ t

/-! ## F4: σₜ é *-automorfismo com lei de grupo -/

theorem sigma_one (t : ℝ) : sigma ρ t 1 = 1 := by
  simp only [sigma, mul_one]; exact modPow_mul_neg ρ t

/-- [KERNEL] `σₜ` é multiplicativo. -/
theorem sigma_mul (t : ℝ) (a b : Matrix n n ℂ) :
    sigma ρ t (a * b) = sigma ρ t a * sigma ρ t b := by
  simp only [sigma]
  calc modPow ρ t * (a * b) * modPow ρ (-t)
      = modPow ρ t * a * ((modPow ρ (-t) * modPow ρ t) * (b * modPow ρ (-t))) := by
        rw [modPow_neg_mul, one_mul]; simp only [mul_assoc]
    _ = modPow ρ t * a * modPow ρ (-t) * (modPow ρ t * b * modPow ρ (-t)) := by
        simp only [mul_assoc]

/-- [KERNEL] `σₜ` respeita a estrela: *-automorfismo. -/
theorem sigma_conjTranspose (t : ℝ) (a : Matrix n n ℂ) :
    sigma ρ t aᴴ = (sigma ρ t a)ᴴ := by
  simp only [sigma, conjTranspose_mul, modPow_conjTranspose, neg_neg, mul_assoc]

/-- [KERNEL] LEI DE GRUPO DO FLUXO: `σₛ∘σₜ = σ_{s+t}`. -/
theorem sigma_sigma (s t : ℝ) (a : Matrix n n ℂ) :
    sigma ρ s (sigma ρ t a) = sigma ρ (s + t) a := by
  simp only [sigma]
  rw [modPow_add, neg_add_rev, modPow_add]
  simp only [mul_assoc]

/-! ## F5: invariância do estado (KMS dinâmico) -/

theorem rho_comm_logRho : Commute ρ (logRho ρ) := by
  unfold logRho
  exact ((Commute.refl ρ).cfc_real Real.log).symm

theorem rho_comm_modPow (t : ℝ) : Commute ρ (modPow ρ t) := by
  unfold modPow
  exact ((rho_comm_logRho ρ).smul_right _).exp_right

/-- [KERNEL] INVARIÂNCIA DO ESTADO: `ω(σₜ(a)) = ω(a)` — o estado de Gibbs
    é estacionário sob seu próprio fluxo modular (a face dinâmica do KMS
    algébrico `gibbs_kms` de FiniteTomita.lean). -/
theorem gibbs_sigma (t : ℝ) (a : Matrix n n ℂ) :
    gibbs ρ (sigma ρ t a) = gibbs ρ a := by
  have hc : ρ * modPow ρ t = modPow ρ t * ρ := (rho_comm_modPow ρ t).eq
  simp only [gibbs, sigma]
  rw [← mul_assoc, ← mul_assoc, hc, mul_assoc (modPow ρ t) ρ a,
      Matrix.trace_mul_cycle, modPow_neg_mul, one_mul]

/-! ## F6: ancoragem exp(log ρ) = ρ -/

section Anchor
open scoped Matrix.Norms.L2Operator

/-- [KERNEL] ANCORAGEM: `exp(log ρ) = ρ` para ρ positiva-definida —
    o gerador logRho é DE FATO o logaritmo de ρ. -/
theorem exp_logRho (hρ : ρ.PosDef) : exp (logRho ρ) = ρ := by
  have h : logRho ρ = CFC.log ρ := rfl
  rw [h]
  exact CFC.exp_log ρ hρ.isStrictlyPositive

end Anchor

/-! ## F7: o fluxo fixa o vetor GNS -/

theorem omega_comm_modPow (t : ℝ) : Commute (Omega ρ) (modPow ρ t) := by
  have h1 : Commute ρ (Omega ρ) := by
    unfold Omega
    rw [CFC.sqrt_eq_cfc]
    exact ((Commute.refl ρ).cfc_nnreal NNReal.sqrt).symm
  have h2 : Commute (logRho ρ) (Omega ρ) := by
    unfold logRho
    exact h1.cfc_real Real.log
  unfold modPow
  exact (h2.symm.smul_right _).exp_right

/-- [KERNEL] O FLUXO FIXA Ω: `σₜ(Ω) = Ω` — o vetor GNS é o ponto
    estacionário do movimento modular (com ΔΩ=Ω e JΩ=Ω, o tripé completo). -/
theorem sigma_omega (t : ℝ) :
    modPow ρ t * Omega ρ * modPow ρ (-t) = Omega ρ := by
  rw [← (omega_comm_modPow ρ t).eq, mul_assoc, modPow_mul_neg, mul_one]

end

end TGLExt
