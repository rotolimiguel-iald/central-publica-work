import TGLExt.F1Fecho394.OrbitalGeneratedCovarianceR3
import TGLExt.O16.PhotonCharacterCocycle
import Mathlib.Analysis.CStarAlgebra.Matrix

/-! Complexification of the existing real transverse O(2) cocycle.
No determinant-one, global photon representation, or net hypothesis is inferred.
The fiber is the existing two-dimensional complex Euclidean fiber. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open Matrix
namespace F1Fecho.OrbitalScreen
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open ORDEM016.D1prime

abbrev Vec4 := Fin 4 → ℝ
abbrev Fiber := EuclideanSpace ℂ (Fin 2)

def coefficientMatrix (g : Vec4 →ₗ[ℝ] Vec4) (x y : MomentumCoordinates) :
    Matrix (Fin 2) (Fin 2) ℂ := fun i j => (screenCoefficient g x y i j : ℂ)

theorem coefficientMatrix_unitary (g : Vec4 →ₗ[ℝ] Vec4)
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (hp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (hm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) :
    coefficientMatrix g x y ∈ Matrix.unitaryGroup (Fin 2) ℂ := by
  apply Matrix.mem_unitaryGroup_iff'.mpr
  ext i j
  have h := screen_columns_orthonormal g x y hx hy hp hm i j
  simp only [Matrix.mul_apply,Matrix.star_apply,Fin.sum_univ_two,
    coefficientMatrix,Complex.star_def,Complex.conj_ofReal,Matrix.one_apply]
  simpa only [Complex.ofReal_add,Complex.ofReal_mul,apply_ite,Complex.ofReal_one,Complex.ofReal_zero] using congrArg Complex.ofReal h

theorem coefficientMatrix_comp (g h : Vec4 →ₗ[ℝ] Vec4)
    (x y z : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0) (hz : z.1 ≠ 0)
    (hp : h (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gp : g (shellMomentum 0 (rapidityChart 0 y))=shellMomentum 0 (rapidityChart 0 z))
    (hm : ∀ a b,orbitPairing (h a) (h b)=orbitPairing a b) :
    coefficientMatrix (g.comp h) x z=coefficientMatrix g y z*coefficientMatrix h x y := by
  ext i j
  have h := screenCoefficient_comp g h x y z hx hy hz hp gp hm i j
  simpa [coefficientMatrix,Matrix.mul_apply,Fin.sum_univ_two] using congrArg Complex.ofReal h

theorem coefficientMatrix_id (x : MomentumCoordinates) (hx : x.1 ≠ 0) :
    coefficientMatrix (LinearMap.id : Vec4 →ₗ[ℝ] Vec4) x x=1 := by
  ext i j
  change ((-(orbitPairing (screen x i) (screen x j)) : ℝ) : ℂ)=(1 : Matrix (Fin 2) (Fin 2) ℂ) i j
  rw [screen_metric x hx i j]
  by_cases hij : i=j <;> simp [Matrix.one_apply,hij]

def screenFiberUnitary (g : Vec4 →ₗ[ℝ] Vec4)
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (hp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (hm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) : Fiber ≃ₗᵢ[ℂ] Fiber :=
  Unitary.linearIsometryEquiv
    ⟨(Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)) (coefficientMatrix g x y),
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2))
        (coefficientMatrix_unitary g x y hx hy hp hm)⟩

theorem screenFiberUnitary_apply (g : Vec4 →ₗ[ℝ] Vec4)
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (hp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (hm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) (v : Fiber) :
    screenFiberUnitary g x y hx hy hp hm v= (Matrix.toEuclideanCLM (𝕜:=ℂ) (n:=Fin 2)) (coefficientMatrix g x y) v := rfl

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.coefficientMatrix_unitary
#print axioms F1Fecho.OrbitalScreen.coefficientMatrix_comp
#print axioms F1Fecho.OrbitalScreen.coefficientMatrix_id
#print axioms F1Fecho.OrbitalScreen.screenFiberUnitary_apply
