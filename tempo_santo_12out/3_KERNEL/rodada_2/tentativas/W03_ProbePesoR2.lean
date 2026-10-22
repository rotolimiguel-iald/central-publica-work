import Mathlib
import TGLExt.LocalBreuerGap
import TGLExt.ModularFlow
import TGLExt.FiniteTomita
import TGLExt.Ergodicity
import TGLExt.IALDJones

/-! Sonda de PESO (rodada 2, F1.TEMPO): o `hd` de T10.d é semanticamente necessário?
    Rota por comutação: `logRho (rhoD d)` comuta com toda diagonal ⟹ é diagonal; é autoadjunto ⟹ entradas
    reais; logo `ρ^{it}` é diagonal de módulo 1 e `|σ_t(x)ᵢⱼ| = |xᵢⱼ|` para TODO `d` real. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLExt.ProbePesoR2

open Matrix NormedSpace
open scoped Matrix ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

theorem logRho_rhoD_commute_diagonal (d : n → ℝ) (v : n → ℂ) :
    Commute (logRho (rhoD d)) (Matrix.diagonal v) := by
  have h : Commute (rhoD d) (Matrix.diagonal v) := by
    unfold rhoD Commute SemiconjBy
    rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
    congr 1
    funext i
    ring
  exact h.cfc_real Real.log

theorem logRho_rhoD_real_diagonal (d : n → ℝ) :
    ∃ ℓ : n → ℝ, logRho (rhoD d) = Matrix.diagonal (fun i => (ℓ i : ℂ)) := by
  refine ⟨fun i => (logRho (rhoD d) i i).re, ?_⟩
  ext i j
  by_cases hij : i = j
  · subst hij
    have hsa := congrFun (congrFun (logRho_conjTranspose (rhoD d)) i) i
    rw [Matrix.conjTranspose_apply] at hsa
    have hsa' : (starRingEnd ℂ) (logRho (rhoD d) i i) = logRho (rhoD d) i i := hsa
    rw [Matrix.diagonal_apply_eq]
    exact (Complex.conj_eq_iff_re.mp hsa').symm
  · rw [Matrix.diagonal_apply_ne _ hij]
    have hc := congrFun (congrFun (logRho_rhoD_commute_diagonal d (Pi.single i 1)).eq i) j
    simp only [Matrix.mul_diagonal, Matrix.diagonal_mul, Pi.single_apply, if_neg (Ne.symm hij),
      mul_zero] at hc
    simpa using hc.symm

theorem modPow_rhoD_general (d : n → ℝ) :
    ∃ ℓ : n → ℝ, ∀ t : ℝ, modPow (rhoD d) t
      = Matrix.diagonal fun i => Complex.exp ((t : ℂ) * Complex.I * (ℓ i : ℂ)) := by
  obtain ⟨ℓ, hℓ⟩ := logRho_rhoD_real_diagonal d
  refine ⟨ℓ, fun t => ?_⟩
  unfold modPow
  rw [hℓ, ← Matrix.diagonal_smul, Matrix.exp_diagonal]
  congr 1
  funext i
  simp only [Pi.coe_exp, Pi.smul_apply, smul_eq_mul, ← Complex.exp_eq_exp_ℂ]

theorem phase_norm_one (t s : ℝ) : ‖Complex.exp ((t : ℂ) * Complex.I * (s : ℂ))‖ = 1 := by
  rw [show (t : ℂ) * Complex.I * (s : ℂ) = ((t * s : ℝ) : ℂ) * Complex.I by push_cast; ring]
  exact Complex.norm_exp_ofReal_mul_I _

/-- T10.d SEM `hd`: para TODO `d` real. -/
theorem modular_clock_rotates_without_shrinking_general (d : n → ℝ) (t : ℝ) (x : Matrix n n ℂ) (i j : n) :
    ‖sigma (rhoD d) t x i j‖ = ‖x i j‖ := by
  obtain ⟨ℓ, hℓ⟩ := modPow_rhoD_general d
  simp only [sigma, hℓ t, hℓ (-t), Matrix.mul_diagonal, Matrix.diagonal_mul]
  rw [norm_mul, norm_mul, phase_norm_one, phase_norm_one, one_mul, mul_one]

/-- sonda: `d = (1, 0)` (viola `hd`) e ainda assim a conclusão vale. -/
example (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    ‖sigma (rhoD ![(1 : ℝ), 0]) t x 0 1‖ = ‖x 0 1‖ :=
  modular_clock_rotates_without_shrinking_general _ t x 0 1

end

end TGLExt.ProbePesoR2

#print axioms TGLExt.ProbePesoR2.logRho_rhoD_commute_diagonal
#print axioms TGLExt.ProbePesoR2.logRho_rhoD_real_diagonal
#print axioms TGLExt.ProbePesoR2.modPow_rhoD_general
#print axioms TGLExt.ProbePesoR2.phase_norm_one
#print axioms TGLExt.ProbePesoR2.modular_clock_rotates_without_shrinking_general
