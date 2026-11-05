import TGLExt.F1Fecho394.OrbitalSpatialContinuityR1
/-! Translation covariance for every scalar spatial orthogonal transformation
on the unchanged massless H1. Helicity transport is a separate obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

def spacetimeSpatial (a : Fin 4 → ℝ) : Spatial := spatialChart (![a 2,a 3],a 1)

def spatialSpacetime (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) : Fin 4 → ℝ :=
  let p := spatialAction Q (![a 2,a 3],a 1)
  ![a 0,p.2,p.1 0,p.1 1]

theorem spacetimeSpatial_rotation (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) :
    spacetimeSpatial (spatialSpacetime Q a)=Q (spacetimeSpatial a) := by
  change spatialChart (![(spatialAction Q (![a 2,a 3],a 1)).1 0,
    (spatialAction Q (![a 2,a 3],a 1)).1 1],
    (spatialAction Q (![a 2,a 3],a 1)).2)=Q (spatialChart (![a 2,a 3],a 1))
  have hvec (v : Fin 2 → ℝ) : ![v 0,v 1]=v := by
    funext i
    fin_cases i <;> rfl
  rw [hvec]
  exact spatialAction_chart Q _

theorem orbitPairing_shell_spatial (m : ℝ) (a : Fin 4 → ℝ) (p : MomentumCoordinates) :
    orbitPairing a (shellMomentum m p)=
      a 0 * energy (transverseMass m p.1) p.2 - inner ℝ (spacetimeSpatial a) (spatialChart p) := by
  change a 0 * energy (transverseMass m p.1) p.2-a 1*p.2-a 2*p.1 0-a 3*p.1 1=_
  change a 0 * energy (transverseMass m p.1) p.2-a 1*p.2-a 2*p.1 0-a 3*p.1 1 =
    a 0 * energy (transverseMass m p.1) p.2 -
      (inner ℝ (WithLp.toLp 2 ![a 2,a 3] : EuclideanSpace ℝ (Fin 2))
        (WithLp.toLp 2 p.1) + inner ℝ (a 1) p.2)
  simp [EuclideanSpace.inner_toLp_toLp,dotProduct,Fin.sum_univ_two]
  ring

theorem spatial_orbitalPhase (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (m : ℝ)
    (a : Fin 4 → ℝ) (p : MomentumCoordinates) :
    orbitalPhase m a (spatialAction Q.symm p)=orbitalPhase m (spatialSpacetime Q a) p := by
  unfold orbitalPhase
  apply congrArg phase
  rw [orbitPairing_shell_spatial,orbitPairing_shell_spatial,spatialAction_energy,
    spatialAction_chart,spacetimeSpatial_rotation]
  have hi := Q.inner_map_map (spacetimeSpatial a) (Q.symm (spatialChart p))
  rw [Q.apply_symm_apply] at hi
  change a 0 * energy (transverseMass m p.1) p.2 - _ =
    a 0 * energy (transverseMass m p.1) p.2 - _
  rw [hi]

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

theorem spatialUnitary_translation_covariance (Q : Spatial ≃ₗᵢ[ℝ] Spatial)
    (m : ℝ) (a : Fin 4 → ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    spatialUnitary m Q (orbitalTranslation m a f)=
      orbitalTranslation m (spatialSpacetime Q a) (spatialUnitary m Q f) := by
  have htr := (spatialAction_orbital Q.symm m).quasiMeasurePreserving.ae
    (orbitalTranslation_ae m a f)
  apply Lp.ext
  filter_upwards [spatialUnitary_ae m Q (orbitalTranslation m a f),htr,
    orbitalTranslation_ae m (spatialSpacetime Q a) (spatialUnitary m Q f),
    spatialUnitary_ae m Q f] with p h1 h2 h3 h4
  rw [h1,h2,h3,h4,spatial_orbitalPhase]

theorem scalarOrthogonalH1_U1 (q : SpatialOrthogonal) (a : Fin 4 → ℝ)
    (f : TGLExt.ImportedSQ.H1) :
    scalarOrthogonalH1 q (TGLExt.ImportedSQ.U1 a f)=
      TGLExt.ImportedSQ.U1 (spatialSpacetime (Unitary.linearIsometryEquiv q) a)
        (scalarOrthogonalH1 q f) :=
  spatialUnitary_translation_covariance _ 0 a f

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.spacetimeSpatial_rotation
#print axioms F1Fecho.OrbitalSpatial.spatial_orbitalPhase
#print axioms F1Fecho.OrbitalSpatial.spatialUnitary_translation_covariance
#print axioms F1Fecho.OrbitalSpatial.scalarOrthogonalH1_U1
