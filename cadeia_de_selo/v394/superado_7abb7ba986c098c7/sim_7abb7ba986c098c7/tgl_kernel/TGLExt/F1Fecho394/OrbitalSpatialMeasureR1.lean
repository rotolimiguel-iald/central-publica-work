import TGLExt.O16.OrbitalRapidityMeasure_v4
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
/-! Spatial orthogonal transformations preserve the existing orbital measure.
The auxiliary Euclidean chart is only a coordinate identification: neither the
orbitalMeasure nor H1 is replaced. This is the scalar orbital part; no Wigner
helicity phase, full Lorentz representation or global localization is claimed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set
open scoped ENNReal
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016

abbrev Spatial := WithLp 2 (EuclideanSpace ℝ (Fin 2) × ℝ)

def spatialChart : MomentumCoordinates ≃ᵐ Spatial :=
  (MeasurableEquiv.prodCongr (MeasurableEquiv.toLp 2 Transverse)
    (MeasurableEquiv.refl ℝ)).trans
      (MeasurableEquiv.toLp 2 (EuclideanSpace ℝ (Fin 2) × ℝ))

theorem spatialChart_preserving : MeasurePreserving spatialChart momentumMeasure volume := by
  exact ((PiLp.volume_preserving_toLp (Fin 2)).prod
    (MeasurePreserving.id (volume : Measure ℝ))).trans
      (WithLp.volume_preserving_toLp (EuclideanSpace ℝ (Fin 2)) ℝ)

theorem spatialChart_norm_sq (p : MomentumCoordinates) :
    ‖spatialChart p‖^2 = p.1 0^2+p.1 1^2+p.2^2 := by
  rw [WithLp.prod_norm_sq_eq_of_L2]
  change ‖(WithLp.toLp 2 p.1 : EuclideanSpace ℝ (Fin 2))‖^2 + ‖p.2‖^2 = _
  simp [EuclideanSpace.real_norm_sq_eq,Fin.sum_univ_two,Real.norm_eq_abs,sq_abs]

theorem energy_spatialChart (m : ℝ) (p : MomentumCoordinates) :
    energy (transverseMass m p.1) p.2 = Real.sqrt (m^2+‖spatialChart p‖^2) := by
  unfold energy
  rw [transverseMass_sq,spatialChart_norm_sq]
  congr 1
  ring

def spatialAction (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    MomentumCoordinates ≃ᵐ MomentumCoordinates :=
  spatialChart.trans (Q.toMeasurableEquiv.trans spatialChart.symm)

theorem spatialAction_chart (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (p : MomentumCoordinates) :
    spatialChart (spatialAction Q p) = Q (spatialChart p) := by
  exact spatialChart.apply_symm_apply _

theorem spatialAction_volume (Q : Spatial ≃ₗᵢ[ℝ] Spatial) :
    MeasurePreserving (spatialAction Q) momentumMeasure momentumMeasure :=
  spatialChart_preserving.trans (Q.measurePreserving.trans spatialChart_preserving.symm)

theorem spatialAction_energy (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (m : ℝ) (p : MomentumCoordinates) :
    energy (transverseMass m (spatialAction Q p).1) (spatialAction Q p).2 =
      energy (transverseMass m p.1) p.2 := by
  rw [energy_spatialChart,energy_spatialChart,spatialAction_chart,Q.norm_map]

theorem spatialAction_weight (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (m : ℝ) (p : MomentumCoordinates) :
    orbitalWeight m (spatialAction Q p) = orbitalWeight m p := by
  unfold orbitalWeight
  rw [spatialAction_energy]

theorem preserving_withDensity {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (r : X→X) (hr : MeasurePreserving r μ μ)
    (w : X→ℝ≥0∞) (hw : Measurable w) (hi : ∀x,w (r x)=w x) :
    MeasurePreserving r (μ.withDensity w) (μ.withDensity w) := by
  refine ⟨hr.measurable,?_⟩
  ext s hs
  rw [Measure.map_apply hr.measurable hs,withDensity_apply _ (hr.measurable hs),
    withDensity_apply _ hs]
  simpa only [hi] using hr.setLIntegral_comp_preimage hs hw

theorem spatialAction_orbital (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (m : ℝ) :
    MeasurePreserving (spatialAction Q) (orbitalMeasure m) (orbitalMeasure m) :=
  preserving_withDensity momentumMeasure (spatialAction Q) (spatialAction_volume Q)
    (orbitalWeight m) (orbitalWeight_measurable m) (spatialAction_weight Q m)

theorem spatialAction_refl (p : MomentumCoordinates) :
    spatialAction (LinearIsometryEquiv.refl ℝ Spatial) p = p := by
  exact spatialChart.symm_apply_apply p

theorem spatialAction_trans (Q R : Spatial ≃ₗᵢ[ℝ] Spatial) (p : MomentumCoordinates) :
    spatialAction (Q.trans R) p = spatialAction R (spatialAction Q p) := by
  apply spatialChart.injective
  simp only [spatialAction_chart,LinearIsometryEquiv.trans_apply]

theorem spatialAction_inverse (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (p : MomentumCoordinates) :
    spatialAction Q.symm (spatialAction Q p) = p := by
  apply spatialChart.injective
  simp only [spatialAction_chart,LinearIsometryEquiv.symm_apply_apply]

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.spatialChart_preserving
#print axioms F1Fecho.OrbitalSpatial.spatialAction_energy
#print axioms F1Fecho.OrbitalSpatial.spatialAction_orbital
#print axioms F1Fecho.OrbitalSpatial.spatialAction_trans
#print axioms F1Fecho.OrbitalSpatial.spatialAction_inverse
