import TGLExt.F1Fecho394.OrbitalSpatialLorentzR2
import TGLExt.F1Fecho394.SpacelikeOpenClosureR5
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection

/-! A spacelike vector can be sent into the right wedge by an actual spatial
orthogonal map. This may include parity; no proper-rotation claim is made. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.SpacelikeGeometry
open TGL.SpecificAQFT F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

theorem spatial_axis_norm (r:ℝ) : ‖spatialChart (![0,0],r)‖=|r| := by
  change ‖WithLp.toLp 2 ((WithLp.toLp 2 ![0,0]:EuclideanSpace ℝ (Fin 2)),r)‖=|r|
  have hz:(WithLp.toLp 2 ![(0:ℝ),0]:EuclideanSpace ℝ (Fin 2))=0 := by ext i; fin_cases i <;> rfl
  rw [hz]
  apply (sq_eq_sq₀ (norm_nonneg _) (abs_nonneg _)).mp
  simp [WithLp.prod_norm_sq_eq_of_L2]

theorem spatial_axis_rotation (z:V) :
    ∃Q:Spatial≃ₗᵢ[ℝ]Spatial,
      spatialSpacetime Q z=![z 0,‖spacetimeSpatial z‖,0,0] := by
  let v:=spacetimeSpatial z
  let w:=spatialChart (![0,0],‖v‖)
  have hn:‖v‖=‖w‖ := by simp [w,spatial_axis_norm]
  let Q:Spatial≃ₗᵢ[ℝ]Spatial:=Submodule.reflection (ℝ ∙ (v-w))ᗮ
  have hQ:Q v=w := Submodule.reflection_sub hn
  have hp:spatialAction Q (![z 2,z 3],z 1)=(![0,0],‖v‖) := by
    apply spatialChart.injective
    rw [spatialAction_chart]
    exact hQ
  refine ⟨Q,?_⟩
  unfold spatialSpacetime
  rw [hp]
  rfl

theorem spacelike_spatial_norm (z:V) (hz:minkowskiSq z<0) :
    |z 0|<‖spacetimeSpatial z‖ := by
  have he:minkowskiSq z=(z 0)^2-‖spacetimeSpatial z‖^2 := by
    calc
      minkowskiSq z=orbitPairing z z := by simp [minkowskiSq,orbitPairing]; ring
      _ = _ := by rw [orbitPairing_spatial,real_inner_self_eq_norm_sq]; ring
  rw [he] at hz
  nlinarith [sq_abs (z 0),abs_nonneg (z 0),norm_nonneg (spacetimeSpatial z)]

theorem spacelike_rotates_into_rightWedge (z:V) (hz:minkowskiSq z<0) :
    ∃Q:Spatial≃ₗᵢ[ℝ]Spatial,spatialSpacetime Q z∈rightWedge := by
  obtain ⟨Q,hQ⟩:=spatial_axis_rotation z
  refine ⟨Q,?_⟩
  rw [hQ]
  exact spacelike_spatial_norm z hz

end F1Fecho.SpacelikeGeometry
#print axioms F1Fecho.SpacelikeGeometry.spatial_axis_rotation
#print axioms F1Fecho.SpacelikeGeometry.spacelike_rotates_into_rightWedge
