import TGLExt.O16.PhotonCharacterCocycle
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-! The actual O16 null frame has fixed orientation. This auxiliary lemma
does not postulate a Lorentz screen orientation. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
open Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
open ChatgptAudit.WignerRapidityMeasure016
namespace F1Fecho.ScreenOrientation

def nullFrame (y : MomentumCoordinates) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun i j => ![shellMomentum 0 (rapidityChart 0 y), nullCompanion y,
    screenOne y, screenTwo y] j i

theorem nullFrame_det (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    (nullFrame y).det = 1 := by
  have hr := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hsq := transverseMass_sq 0 y.1
  simp only [zero_pow (by decide : 2 ≠ 0), zero_add] at hsq
  have htr := Real.cosh_sq_sub_sinh_sq y.2
  unfold nullFrame
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  rw [Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_four, Matrix.det_fin_three, nullCompanion, screenOne, screenTwo, Fin.succAbove]
  field_simp
  linear_combination
    -2 * (Real.cosh y.2)^2 * hsq + 2 * (Real.sinh y.2)^2 * hsq +
    2 * (transverseMass 0 y.1)^2 * htr

end F1Fecho.ScreenOrientation
#print axioms F1Fecho.ScreenOrientation.nullFrame_det
