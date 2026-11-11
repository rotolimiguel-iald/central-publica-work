import TGLExt.F1Fecho394.SpacelikeAxisRotationR2
import TGLExt.F1Fecho394.ScreenLorentzTransportR7
import TGLExt.F1Fecho394.SpacetimeLorentzFourierR3

/-! Pointwise spacelike separation admits a common spatial change of frame
and a midpoint translation into opposite wedges. Arbitrary sets are not
claimed to fit in a single pair of wedges. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.SpacelikeGeometry
open TGL.SpecificAQFT F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen
open ChatgptAudit.WignerOrbit016

def leftWedge : Set V := {z | |z 0| < -z 1}

theorem half_rightWedge (z:V) (hz:z∈rightWedge) : (1/2:ℝ) • z∈rightWedge := by
  change |(1/2:ℝ)*z 0|<(1/2:ℝ)*z 1
  rw [abs_mul]
  norm_num only [abs_of_nonneg (by norm_num : (0:ℝ) ≤ 1/2)]
  change |z 0| < z 1 at hz
  exact mul_lt_mul_of_pos_left hz (by norm_num)

theorem neg_rightWedge (z:V) (hz:z∈rightWedge) : -z∈leftWedge := by
  simpa [leftWedge,rightWedge,Pi.neg_apply] using hz

theorem spacelike_pair_opposite_wedges (x y:V) (hxy:minkowskiSq (x-y)<0) :
    ∃L:generatedLorentz,∃m:V,
      lorentzLinear L.val (x-m)∈rightWedge ∧
      lorentzLinear L.val (y-m)∈leftWedge := by
  obtain ⟨Q,hQ⟩:=spacelike_rotates_into_rightWedge (x-y) hxy
  let L:=generatedSpatial (Unitary.linearIsometryEquiv.symm Q)
  have hL (z:V):lorentzLinear L.val z=spatialSpacetime Q z := by
    change (spatialMatrix (Unitary.linearIsometryEquiv
      (Unitary.linearIsometryEquiv.symm Q))).mulVec z=_
    rw [Unitary.linearIsometryEquiv.apply_symm_apply,spatialMatrix_mulVec]
  let m:V:=(1/2:ℝ) • (x+y)
  have hx:x-m=(1/2:ℝ) • (x-y) := by ext i; simp [m]; ring
  have hy:y-m=-((1/2:ℝ) • (x-y)) := by ext i; simp [m]; ring
  refine ⟨L,m,?_,?_⟩
  · rw [hx,map_smul,hL]
    exact half_rightWedge _ hQ
  · rw [hy,map_neg,map_smul,hL]
    exact neg_rightWedge _ (half_rightWedge _ hQ)

end F1Fecho.SpacelikeGeometry
#print axioms F1Fecho.SpacelikeGeometry.spacelike_pair_opposite_wedges
