import TGLExt.F1Fecho394.OrbitalLocalFinitenessR2
import TGLExt.F1Fecho394.OrbitalSpatialUnitaryR3
import Mathlib.MeasureTheory.Function.LpSpace.ContinuousCompMeasurePreserving
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
/-! Strong continuity of the scalar orbital orthogonal-group action on the
original massless H1. The group carries its existing operator-norm topology.
This supplies no Wigner helicity phase. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016

theorem spatialChart_continuous : Continuous spatialChart := by
  change Continuous (fun p : MomentumCoordinates =>
    WithLp.toLp 2 (WithLp.toLp 2 p.1, p.2))
  fun_prop

theorem spatialChart_symm_continuous : Continuous spatialChart.symm := by
  change Continuous (fun p : Spatial => (WithLp.ofLp (WithLp.ofLp p).1, (WithLp.ofLp p).2))
  fun_prop

abbrev SpatialOrthogonal := unitary (Spatial →L[ℝ] Spatial)

def rotationPullbackMap (q : SpatialOrthogonal) : C(MomentumCoordinates,MomentumCoordinates) :=
  ⟨spatialAction (Unitary.linearIsometryEquiv q).symm, by
    change Continuous (fun p => spatialChart.symm ((star (q : Spatial →L[ℝ] Spatial)) (spatialChart p)))
    exact spatialChart_symm_continuous.comp
      ((star (q : Spatial →L[ℝ] Spatial)).continuous.comp spatialChart_continuous)⟩

theorem rotationPullbackMap_continuous : Continuous rotationPullbackMap := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  change Continuous (fun qp : SpatialOrthogonal × MomentumCoordinates =>
    spatialChart.symm ((star (qp.1 : Spatial →L[ℝ] Spatial)) (spatialChart qp.2)))
  exact spatialChart_symm_continuous.comp
    (((continuous_subtype_val.comp continuous_fst).star).clm_apply
      (spatialChart_continuous.comp continuous_snd))

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

theorem spatialUnitary_strongly_continuous (f : Lp E 2 (orbitalMeasure 0)) :
    Continuous (fun q : SpatialOrthogonal => spatialUnitary 0 (Unitary.linearIsometryEquiv q) f) := by
  exact (continuous_const : Continuous (fun _ : SpatialOrthogonal => f)).compMeasurePreservingLp
    rotationPullbackMap_continuous
    (fun q => spatialAction_orbital (Unitary.linearIsometryEquiv q).symm 0) (by norm_num)

def scalarOrthogonalH1 (q : SpatialOrthogonal) :
    TGLExt.ImportedSQ.H1 ≃ₗᵢ[ℂ] TGLExt.ImportedSQ.H1 :=
  scalarSpatialH1 (Unitary.linearIsometryEquiv q)

theorem scalarOrthogonalH1_strongly_continuous (f : TGLExt.ImportedSQ.H1) :
    Continuous (fun q => scalarOrthogonalH1 q f) := spatialUnitary_strongly_continuous f

theorem scalarOrthogonalH1_one (f : TGLExt.ImportedSQ.H1) : scalarOrthogonalH1 1 f=f := by
  have h : Unitary.linearIsometryEquiv (1 : SpatialOrthogonal)=LinearIsometryEquiv.refl ℝ Spatial := by
    ext x
    rfl
  change spatialUnitary 0 (Unitary.linearIsometryEquiv 1) f=f
  rw [h,spatialUnitary_refl]
  rfl

theorem scalarOrthogonalH1_mul (q r : SpatialOrthogonal) (f : TGLExt.ImportedSQ.H1) :
    scalarOrthogonalH1 (q*r) f=scalarOrthogonalH1 q (scalarOrthogonalH1 r f) := by
  have h : Unitary.linearIsometryEquiv (q*r)=
      (Unitary.linearIsometryEquiv r).trans (Unitary.linearIsometryEquiv q) := by
    ext x
    rfl
  change spatialUnitary 0 (Unitary.linearIsometryEquiv (q*r)) f=
    spatialUnitary 0 (Unitary.linearIsometryEquiv q) (spatialUnitary 0 (Unitary.linearIsometryEquiv r) f)
  rw [h,spatialUnitary_trans]
  rfl

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.rotationPullbackMap_continuous
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary_strongly_continuous
#print axioms F1Fecho.OrbitalSpatial.scalarOrthogonalH1_strongly_continuous
#print axioms F1Fecho.OrbitalSpatial.scalarOrthogonalH1_one
#print axioms F1Fecho.OrbitalSpatial.scalarOrthogonalH1_mul
