import TGLExt.F1Fecho394.OrbitalSpatialMeasureR1
import TGLExt.TheImportedSecondQuantization
/-! The scalar spatial action on the very same orbital L2 space. The inverse
map in pullback gives the usual active-action convention. Helicity cocycles
are not supplied by this construction. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

def spatialIsometry (m : ℝ) (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    Lp E 2 (orbitalMeasure m) →ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  Lp.compMeasurePreservingₗᵢ ℂ (spatialAction Q.symm) (spatialAction_orbital Q.symm m)

theorem spatialIsometry_inverse (m : ℝ) (Q : Spatial ≃ₗᵢ[ℝ] Spatial)
    (f : Lp E 2 (orbitalMeasure m)) :
    spatialIsometry m Q.symm (spatialIsometry m Q f) = f := by
  change Lp.compMeasurePreserving (spatialAction Q.symm.symm) _
    (Lp.compMeasurePreserving (spatialAction Q.symm) _ f) = f
  rw [← Lp.compMeasurePreserving_comp_apply]
  have he : (spatialAction Q.symm ∘ spatialAction Q.symm.symm) = id := by
    funext p
    simpa only [Function.comp_apply,LinearIsometryEquiv.symm_symm,id_eq] using spatialAction_inverse Q p
  simp only [he,Lp.compMeasurePreserving_id_apply]

def spatialUnitary (m : ℝ) (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    Lp E 2 (orbitalMeasure m) ≃ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  LinearIsometryEquiv.ofLinearIsometry (spatialIsometry m Q)
    (spatialIsometry m Q.symm).toLinearMap
    (by
      apply LinearMap.ext
      intro f
      change spatialIsometry m Q (spatialIsometry m Q.symm f) = f
      simpa only [LinearIsometryEquiv.symm_symm] using spatialIsometry_inverse m Q.symm f)
    (by apply LinearMap.ext; intro f; exact spatialIsometry_inverse m Q f)

theorem spatialUnitary_ae (m : ℝ) (Q : Spatial ≃ₗᵢ[ℝ] Spatial)
    (f : Lp E 2 (orbitalMeasure m)) :
    (spatialUnitary m Q f : MomentumCoordinates → E) =ᵐ[orbitalMeasure m]
      fun p => f (spatialAction Q.symm p) :=
  Lp.coeFn_compMeasurePreserving f (spatialAction_orbital Q.symm m)

theorem spatialUnitary_refl (m : ℝ) :
    spatialUnitary (E := E) m (LinearIsometryEquiv.refl ℝ Spatial) =
      LinearIsometryEquiv.refl ℂ _ := by
  apply LinearIsometryEquiv.ext
  intro f
  change Lp.compMeasurePreserving (spatialAction (LinearIsometryEquiv.refl ℝ Spatial).symm) _ f = f
  have he : (spatialAction (LinearIsometryEquiv.refl ℝ Spatial).symm : MomentumCoordinates→MomentumCoordinates) = id := by
    funext p
    exact spatialAction_refl p
  simp only [he,Lp.compMeasurePreserving_id_apply]

theorem spatialUnitary_trans (m : ℝ) (Q R : Spatial ≃ₗᵢ[ℝ] Spatial) :
    spatialUnitary (E := E) m (Q.trans R) =
      (spatialUnitary m Q).trans (spatialUnitary m R) := by
  apply LinearIsometryEquiv.ext
  intro f
  change Lp.compMeasurePreserving (spatialAction (Q.trans R).symm) _ f =
    Lp.compMeasurePreserving (spatialAction R.symm) _
      (Lp.compMeasurePreserving (spatialAction Q.symm) _ f)
  rw [← Lp.compMeasurePreserving_comp_apply]
  have he : (spatialAction (Q.trans R).symm : MomentumCoordinates→MomentumCoordinates) =
      spatialAction Q.symm ∘ spatialAction R.symm := by
    funext p
    exact spatialAction_trans R.symm Q.symm p
  simp only [he]

/-- This action is on the unchanged canonical H1, not an isomorphic replacement. -/
def scalarSpatialH1 (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    TGLExt.ImportedSQ.H1 ≃ₗᵢ[ℂ] TGLExt.ImportedSQ.H1 := spatialUnitary 0 Q

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.spatialIsometry_inverse
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary_ae
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary_refl
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary_trans
#print axioms F1Fecho.OrbitalSpatial.scalarSpatialH1
