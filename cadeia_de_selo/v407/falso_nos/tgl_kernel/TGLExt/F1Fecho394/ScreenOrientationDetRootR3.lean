import TGLExt.F1Fecho394.NullFrameDetRootR4
import Mathlib.LinearAlgebra.Matrix.ToLin

/-! Proper metric-preserving momentum transport induces an oriented screen.
The determinant hypothesis is on the actual four-dimensional linear map;
the two-dimensional orientation is a consequence, not an extra input. -/
set_option autoImplicit false
set_option maxHeartbeats 3000000
noncomputable section
open Matrix
open ChatgptAudit.WignerOrbit016 TGLExt TGLExt.ContratoQGv31
open ChatgptAudit.WignerRapidityMeasure016
namespace F1Fecho.ScreenOrientation

def nullCoordinates (y : MomentumCoordinates) (v : Fin 4 → ℝ) : Fin 4 → ℝ :=
  ![orbitPairing v (nullCompanion y),
    orbitPairing v (shellMomentum 0 (rapidityChart 0 y)),
    -orbitPairing v (screenOne y), -orbitPairing v (screenTwo y)]

theorem nullFrame_coordinates (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (v : Fin 4 → ℝ) : nullFrame y *ᵥ nullCoordinates y v = v := by
  have hd := null_frame_decomposition y hy v
  ext i
  have h := congrFun hd i
  simpa [nullFrame, nullCoordinates, Matrix.mulVec, dotProduct,
    Fin.sum_univ_four, sub_eq_add_neg, mul_comm, mul_left_comm, mul_assoc] using h.symm

theorem nullCoordinates_momentum (y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    nullCoordinates y (shellMomentum 0 (rapidityChart 0 y)) = ![1,0,0,0] := by
  have hr := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hsq := transverseMass_sq 0 y.1
  simp only [zero_pow (by decide : 2 ≠ 0), zero_add] at hsq
  have htr := Real.cosh_sq_sub_sinh_sq y.2
  unfold nullCoordinates
  rw [shellMomentum_chart 0 y (transverseMass_pos_of_ne_zero 0 y.1 hy)]
  ext i
  fin_cases i <;>
    simp [orbitPairing, nullCompanion, screenOne, screenTwo] <;> field_simp <;>
    first | (solve | ring)
          | (solve | linear_combination hsq + (transverseMass 0 y.1)^2 * htr)
          | (solve | linear_combination -hsq + (transverseMass 0 y.1)^2 * htr)

theorem momentum_pairing_frame (y : MomentumCoordinates) (hy : y.1 ≠ 0)
    (j : Fin 4) :
    orbitPairing (fun i => nullFrame y i j)
      (shellMomentum 0 (rapidityChart 0 y)) = (![0,1,0,0] : Fin 4 → ℝ) j := by
  have hc := nullCoordinates_momentum y hy
  fin_cases j
  · exact congrFun hc 1
  · simpa [nullCoordinates, nullFrame, orbitPairing_symm] using congrFun hc 0
  · simpa [nullCoordinates, nullFrame, orbitPairing_symm] using neg_eq_zero.mp (congrFun hc 2)
  · simpa [nullCoordinates, nullFrame, orbitPairing_symm] using neg_eq_zero.mp (congrFun hc 3)

def frameTransport (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun i j => nullCoordinates y (g (fun k => nullFrame x k j)) i

theorem frameTransport_factorization (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (hy : y.1 ≠ 0) :
    LinearMap.toMatrix' g * nullFrame x = nullFrame y * frameTransport g x y := by
  ext i j
  have h := congrFun (nullFrame_coordinates y hy (g (fun k => nullFrame x k j))) i
  have hg := congrFun (LinearMap.toMatrix'_mulVec g (fun k => nullFrame x k j)) i
  change (∑ k, LinearMap.toMatrix' g i k * nullFrame x k j) =
    ∑ k, nullFrame y i k * frameTransport g x y k j
  simpa [Matrix.mulVec, dotProduct, frameTransport] using hg.trans h.symm

theorem screen_orientation_of_proper_transport
    (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ))
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x)) = shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b, orbitPairing (g a) (g b) = orbitPairing a b)
    (gd : (LinearMap.toMatrix' g).det = 1) :
    ORDEM016.D1prime.ScreenOrientationMeasured g x y := by
  let C := frameTransport g x y
  have hc0 (i : Fin 4) : C i 0 = (![1,0,0,0] : Fin 4 → ℝ) i := by
    simpa [C, frameTransport, nullFrame, gp] using congrFun (nullCoordinates_momentum y hy) i
  have hc1 (j : Fin 4) : C 1 j = (![0,1,0,0] : Fin 4 → ℝ) j := by
    change orbitPairing (g (fun i => nullFrame x i j))
      (shellMomentum 0 (rapidityChart 0 y)) = _
    rw [← gp, gm]
    exact momentum_pairing_frame x hx j
  have hd : C.det = 1 := by
    have h := congrArg Matrix.det (frameTransport_factorization g x y hy)
    simpa [Matrix.det_mul, nullFrame_det x hx, nullFrame_det y hy, gd, C] using h.symm
  have hexp : C.det = C 2 2 * C 3 3 - C 2 3 * C 3 2 := by
    rw [Matrix.det_succ_column_zero]
    simp [Fin.sum_univ_four, hc0, Matrix.det_fin_three, Fin.succAbove, hc1]
  rw [hexp] at hd
  simpa [ORDEM016.D1prime.ScreenOrientationMeasured, C, frameTransport,
    nullCoordinates, nullFrame, screenCoefficient, screen, orbitPairing_symm] using hd

end F1Fecho.ScreenOrientation
#print axioms F1Fecho.ScreenOrientation.nullFrame_coordinates
#print axioms F1Fecho.ScreenOrientation.nullCoordinates_momentum
#print axioms F1Fecho.ScreenOrientation.momentum_pairing_frame
#print axioms F1Fecho.ScreenOrientation.frameTransport_factorization
#print axioms F1Fecho.ScreenOrientation.screen_orientation_of_proper_transport
