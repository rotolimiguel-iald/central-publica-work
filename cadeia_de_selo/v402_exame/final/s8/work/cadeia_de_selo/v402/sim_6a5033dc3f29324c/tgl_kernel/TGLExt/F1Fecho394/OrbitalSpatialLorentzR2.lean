import TGLExt.F1Fecho394.OrbitalSpatialCovarianceR2
import TGLExt.PoincareGroup
/-! The scalar spatial transformations are actual elements of the existing
LorentzGrp. This does not extend them to arbitrary Lorentz transformations. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open Matrix
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016 TGLExt

theorem spatialChart_add (p r : MomentumCoordinates) :
    spatialChart (p+r)=spatialChart p+spatialChart r := rfl
theorem spatialChart_smul (c : ℝ) (p : MomentumCoordinates) :
    spatialChart (c • p)=c • spatialChart p := rfl
theorem spatialAction_add (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (p r : MomentumCoordinates) :
    spatialAction Q (p+r)=spatialAction Q p+spatialAction Q r := by
  apply spatialChart.injective
  rw [spatialAction_chart,spatialChart_add,spatialChart_add,map_add,
    spatialAction_chart,spatialAction_chart]
theorem spatialAction_smul (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (c : ℝ) (p : MomentumCoordinates) :
    spatialAction Q (c • p)=c • spatialAction Q p := by
  apply spatialChart.injective
  rw [spatialAction_chart,spatialChart_smul,spatialChart_smul,map_smul,
    spatialAction_chart]

def spatialSpacetimeLinear (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ) where
  toFun := spatialSpacetime Q
  map_add' a b := by
    have hp : (![(a+b) 2,(a+b) 3],(a+b) 1)=
        (![a 2,a 3],a 1)+(![b 2,b 3],b 1) := by
      apply Prod.ext
      · funext i; fin_cases i <;> rfl
      · rfl
    unfold spatialSpacetime
    rw [hp,spatialAction_add]
    funext i
    fin_cases i <;> rfl
  map_smul' c a := by
    have hp : (![(c • a) 2,(c • a) 3],(c • a) 1)=c • (![a 2,a 3],a 1) := by
      apply Prod.ext
      · funext i; fin_cases i <;> rfl
      · rfl
    unfold spatialSpacetime
    rw [hp,spatialAction_smul]
    funext i
    fin_cases i <;> rfl

theorem orbitPairing_spatial (a b : Fin 4 → ℝ) :
    orbitPairing a b=a 0*b 0-inner ℝ (spacetimeSpatial a) (spacetimeSpatial b) := by
  change a 0*b 0-a 1*b 1-a 2*b 2-a 3*b 3=
    a 0*b 0-(inner ℝ (WithLp.toLp 2 ![a 2,a 3] : EuclideanSpace ℝ (Fin 2))
      (WithLp.toLp 2 ![b 2,b 3])+inner ℝ (a 1) (b 1))
  simp [EuclideanSpace.inner_toLp_toLp,dotProduct,Fin.sum_univ_two]
  ring

theorem spatialSpacetime_pairing (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a b : Fin 4 → ℝ) :
    orbitPairing (spatialSpacetime Q a) (spatialSpacetime Q b)=orbitPairing a b := by
  rw [orbitPairing_spatial,orbitPairing_spatial,spacetimeSpatial_rotation,
    spacetimeSpatial_rotation,Q.inner_map_map]
  rfl

theorem orbitPairing_eq_eta (a b : Fin 4 → ℝ) :
    orbitPairing a b=dotProduct a (eta4.mulVec b) := by
  simp [orbitPairing,eta4,Matrix.mulVec,Matrix.diagonal_apply,dotProduct,Fin.sum_univ_four]
  ring

def spatialMatrix (Q : Spatial ≃ₗᵢ[ℝ] Spatial) : Matrix (Fin 4) (Fin 4) ℝ :=
  LinearMap.toMatrix' (spatialSpacetimeLinear Q)

theorem spatialMatrix_mulVec (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) :
    (spatialMatrix Q).mulVec a=spatialSpacetime Q a :=
  LinearMap.toMatrix'_mulVec _ _

theorem spatialMatrix_isLorentz (Q : Spatial ≃ₗᵢ[ℝ] Spatial) : IsLorentz (spatialMatrix Q) := by
  have h (a b : Fin 4 → ℝ) :
      dotProduct a (((spatialMatrix Q)ᵀ*eta4*spatialMatrix Q).mulVec b)=
        dotProduct a (eta4.mulVec b) := by
    rw [←Matrix.mulVec_mulVec,←Matrix.mulVec_mulVec,Matrix.dotProduct_transpose_mulVec,
      dotProduct_comm,spatialMatrix_mulVec,spatialMatrix_mulVec,
      ←orbitPairing_eq_eta,←orbitPairing_eq_eta,spatialSpacetime_pairing]
  ext i j
  have hij:=h (Pi.single i 1) (Pi.single j 1)
  simpa only [Matrix.mulVec_single_one,single_one_dotProduct,Matrix.col_apply] using hij

def spatialLorentz (Q : Spatial ≃ₗᵢ[ℝ] Spatial) : LorentzGrp :=
  ⟨spatialMatrix Q,spatialMatrix_isLorentz Q⟩

theorem spatialLorentz_time (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) :
    ((spatialLorentz Q).val.mulVec a) 0=a 0 := by
  rw [show (spatialLorentz Q).val=spatialMatrix Q from rfl,spatialMatrix_mulVec]
  rfl

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.spatialSpacetimeLinear
#print axioms F1Fecho.OrbitalSpatial.spatialSpacetime_pairing
#print axioms F1Fecho.OrbitalSpatial.spatialMatrix_isLorentz
#print axioms F1Fecho.OrbitalSpatial.spatialLorentz_time
