import TGLExt.F1Fecho394.ScreenCocycleMatrixR4

/-! The existing circular screen polarizations are explicit eigenvectors of
the orientation-preserving transverse cocycle. Orientation is not erased. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Matrix Complex
namespace F1Fecho.OrbitalScreen
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open ORDEM016.D1prime

def circularCoefficients (h : ℝ) : Fin 2 → ℂ := ![1,(h : ℂ)*I]

def screenReconstruction (x : MomentumCoordinates) (v : Fin 2 → ℂ) : Fin 4 → ℂ :=
  fun i => v 0*(screenOne x i : ℂ)+v 1*(screenTwo x i : ℂ)

theorem circularCoefficients_reconstruct (h : ℝ) (x : MomentumCoordinates) :
    screenReconstruction x (circularCoefficients h)=circularScreen h x := by
  funext i
  simp [screenReconstruction,circularCoefficients,circularScreen]

theorem circularCoefficient_plus (g : Vec4 →ₗ[ℝ] Vec4)
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (hp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (hm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b)
    (ho : ScreenOrientationMeasured g x y) :
    (coefficientMatrix g x y).mulVec (circularCoefficients 1)=
      screenPhase g x y • circularCoefficients 1 := by
  obtain ⟨h11,h10,_⟩ := oriented_screen_entries g x y hx hy hp hm ho
  funext i
  fin_cases i <;>
    simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,coefficientMatrix,circularCoefficients,
      screenPhase,photonPhase,h11,h10] <;> ring_nf <;> simp [Complex.I_sq]

theorem circularCoefficient_minus (g : Vec4 →ₗ[ℝ] Vec4)
    (x y : MomentumCoordinates) (hx : x.1 ≠ 0) (hy : y.1 ≠ 0)
    (hp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (hm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b)
    (ho : ScreenOrientationMeasured g x y) :
    (coefficientMatrix g x y).mulVec (circularCoefficients (-1))=
      star (screenPhase g x y) • circularCoefficients (-1) := by
  obtain ⟨h11,h10,_⟩ := oriented_screen_entries g x y hx hy hp hm ho
  funext i
  fin_cases i <;>
    simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,coefficientMatrix,circularCoefficients,
      screenPhase,photonPhase,h11,h10] <;> ring_nf <;> simp [Complex.I_sq]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.circularCoefficients_reconstruct
#print axioms F1Fecho.OrbitalScreen.circularCoefficient_plus
#print axioms F1Fecho.OrbitalScreen.circularCoefficient_minus
