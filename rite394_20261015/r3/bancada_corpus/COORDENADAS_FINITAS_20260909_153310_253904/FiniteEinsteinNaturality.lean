import FiniteRicciContraction
import TGLExt.SelectedGravitationalAtlas

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.FiniteEinsteinNaturality
open Matrix Set TGLExt ChatgptAudit.FiniteCoordinates ChatgptAudit.FiniteLeviCivita
  ChatgptAudit.FiniteCoordinateCurvature ChatgptAudit.FiniteRicciContraction
  ChatgptAudit.GeneralMetric ChatgptAudit.SelectedAtlas
noncomputable section
variable {U W : Set Coordinate4}

theorem ricci_finite_coordinate_transformation (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) :
    coordinateRicci (pullbackConnection C Gamma) x =
      (changeJacobian C x)ᵀ * coordinateRicci Gamma (C.forward x) * changeJacobian C x := by
  unfold coordinateRicci
  simp_rw [coordinate_curvature_finite_transformation C Gamma hGamma x hx]
  exact finite_ricci_contraction _ _ _ (jacobian_mul_inverse_jacobian C x hx)

theorem levi_civita_ricci_finite_transformation (C : SmoothCoordinateChange U W)
    (g : TensorField4) (hg : SmoothMatrixOn W g)
    (hl : ∀ y ∈ W, LorentzByCongruence (g y))
    (x : Coordinate4) (hx : x ∈ U) :
    coordinateRicci (leviCivitaField (pullbackMetric C g)
      (metricInverse (pullbackMetric C g))) x =
        (changeJacobian C x)ᵀ *
          coordinateRicci (leviCivitaField g (metricInverse g)) (C.forward x) *
            changeJacobian C x := by
  have he : EqOn (leviCivitaField (pullbackMetric C g) (metricInverse (pullbackMetric C g)))
      (pullbackConnection C (leviCivitaField g (metricInverse g))) U :=
    fun y hy => levi_civita_finite_coordinate_transformation C g hg hl y hy
  rw [coordinate_ricci_congr_on C.source_open _ _ he hx]
  exact ricci_finite_coordinate_transformation C _ (levi_civita_field_smooth W C.target_open
    g (metricInverse g) hg (constructed_metric_inverse_smooth W g hg hl)) x hx

theorem scalar_curvature_finite_coordinate_transformation (C : SmoothCoordinateChange U W)
    (g : TensorField4) (hg : SmoothMatrixOn W g)
    (hl : ∀ y ∈ W, LorentzByCongruence (g y))
    (x : Coordinate4) (hx : x ∈ U) :
    coordinateScalarCurvature (metricInverse (pullbackMetric C g))
      (leviCivitaField (pullbackMetric C g) (metricInverse (pullbackMetric C g))) x =
        coordinateScalarCurvature (metricInverse g)
          (leviCivitaField g (metricInverse g)) (C.forward x) := by
  have hlor := hl (C.forward x) (C.forward_maps hx)
  have hs := inverse_symmetric_of_symmetric (g (C.forward x)) (metricInverse g (C.forward x))
    (lorentz_metric_symmetric _ hlor) (constructed_metric_inverse_left g _ hlor)
  unfold coordinateScalarCurvature
  rw [constructed_pullback_inverse C g x hx hlor,
    levi_civita_ricci_finite_transformation C g hg hl x hx]
  exact finite_scalar_contraction _ _ _ _ (jacobian_mul_inverse_jacobian C x hx) hs

theorem einstein_finite_coordinate_transformation (C : SmoothCoordinateChange U W)
    (g : TensorField4) (hg : SmoothMatrixOn W g)
    (hl : ∀ y ∈ W, LorentzByCongruence (g y))
    (x : Coordinate4) (hx : x ∈ U) :
    geometricEinsteinTensor (pullbackMetric C g) (metricInverse (pullbackMetric C g))
      (leviCivitaField (pullbackMetric C g) (metricInverse (pullbackMetric C g))) x =
        (changeJacobian C x)ᵀ *
          geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g))
            (C.forward x) * changeJacobian C x := by
  unfold geometricEinsteinTensor
  rw [levi_civita_ricci_finite_transformation C g hg hl x hx,
    scalar_curvature_finite_coordinate_transformation C g hg hl x hx]
  exact finite_einstein_congruence _ _ _ _

/-- Agreement on the open source, rather than agreement at a single point,
is what identifies all the derivatives entering the Einstein tensor. -/
theorem einstein_finite_overlap_transformation (C : SmoothCoordinateChange U W)
    (g h : TensorField4) (hg : SmoothMatrixOn W g)
    (hl : ∀ y ∈ W, LorentzByCongruence (g y))
    (hmetric : EqOn h (pullbackMetric C g) U)
    (x : Coordinate4) (hx : x ∈ U) :
    geometricEinsteinTensor h (metricInverse h) (leviCivitaField h (metricInverse h)) x =
      (changeJacobian C x)ᵀ *
        geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g))
          (C.forward x) * changeJacobian C x := by
  rw [geometric_einstein_congr_on C.source_open h (pullbackMetric C g) hmetric hx]
  exact einstein_finite_coordinate_transformation C g hg hl x hx

#print axioms ricci_finite_coordinate_transformation
#print axioms levi_civita_ricci_finite_transformation
#print axioms scalar_curvature_finite_coordinate_transformation
#print axioms einstein_finite_coordinate_transformation
#print axioms einstein_finite_overlap_transformation
end
end ChatgptAudit.FiniteEinsteinNaturality
