import Mathlib
import TGLExt.LocalBreuerGap
import TGLExt.ModularFlow
import TGLExt.FiniteTomita
import TGLExt.Ergodicity
import TGLExt.IALDJones

/-! Sonda de PESO (rodada 2, F1.TEMPO): o `hd` de T10.d é semanticamente necessário?
    Tentativa: `logRho (rhoD d) = diag(log dᵢ)` para TODO `d` real (o espectro é finito). -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLExt.ProbePesoR2

open scoped Matrix ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- `diagonal` como homomorfismo de *-álgebras `(n → ℂ) → Mₙ(ℂ)`. -/
def diagStar : (n → ℂ) →⋆ₐ[ℂ] Matrix n n ℂ :=
  { Matrix.diagonalAlgHom ℂ with
    map_star' := fun v => by
      ext i j
      by_cases h : i = j
      · subst h; simp [Matrix.diagonalAlgHom, Matrix.diagonal_apply_eq]
      · simp [Matrix.diagonalAlgHom, Matrix.diagonal_apply_ne _ h, Matrix.diagonal_apply_ne _ (Ne.symm h)] }

theorem diagStar_apply (v : n → ℂ) : diagStar v = Matrix.diagonal v := rfl

theorem cfc_log_pi (d : n → ℝ) :
    cfc Real.log (fun i => (d i : ℂ)) = fun i => ((Real.log (d i) : ℝ) : ℂ) := by
  rw [cfc_map_pi (S := ℂ) Real.log (fun i => (d i : ℂ))]
  funext i
  have h := cfc_algebraMap (A := ℂ) (R := ℝ) (d i) Real.log
  simpa using h

theorem logRho_rhoD_general (d : n → ℝ) :
    logRho (rhoD d) = Matrix.diagonal fun i => ((Real.log (d i) : ℝ) : ℂ) := by
  have hsa : IsSelfAdjoint (fun i => (d i : ℂ)) := by
    rw [isSelfAdjoint_iff]; funext i; simp
  have h := (diagStar (n := n)).map_cfc Real.log (fun i => (d i : ℂ))
  rw [cfc_log_pi, diagStar_apply, diagStar_apply] at h
  unfold logRho rhoD
  exact h.symm

end

end TGLExt.ProbePesoR2
