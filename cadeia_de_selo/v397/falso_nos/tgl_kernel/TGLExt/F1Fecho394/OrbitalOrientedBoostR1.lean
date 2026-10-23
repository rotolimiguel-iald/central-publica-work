import TGLExt.F1Fecho394.OrbitalSpatialPoincareR2
/-! Conjugate the paid longitudinal boost by every scalar spatial rotation.
Each resulting one-parameter group acts on the same H1 and has the actual
conjugate Lorentz action on translations. This is not yet a representation
of every Lorentz element, and has no photon Wigner phase. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.OrbitalSpatial
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31
open ChatgptAudit.WignerRapidityMeasure016

theorem scalarSpatialH1_symm (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (f : H1) :
    (scalarSpatialH1 Q).symm f=scalarSpatialH1 Q.symm f := rfl

theorem scalarSpatialH1_U1 (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) (f : H1) :
    scalarSpatialH1 Q (U1 a f)=U1 (spatialSpacetime Q a) (scalarSpatialH1 Q f) :=
  spatialUnitary_translation_covariance Q 0 a f

theorem B0_U1 (s : ℝ) (a : Fin 4 → ℝ) (f : H1) :
    B0 s (U1 a f)=U1 (wedgeBoostMap s a) (B0 s f) :=
  orbitalScalarBoost_translations 0 s a f

def orientedBoost (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (s : ℝ) : H1≃ₗᵢ[ℂ]H1 :=
  ((scalarSpatialH1 Q).symm.trans (B0 s)).trans (scalarSpatialH1 Q)

theorem orientedBoost_apply (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (s : ℝ) (f : H1) :
    orientedBoost Q s f=scalarSpatialH1 Q (B0 s ((scalarSpatialH1 Q).symm f)) := rfl

theorem orientedBoost_zero (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (f : H1) :
    orientedBoost Q 0 f=f := by
  rw [orientedBoost_apply,B0_zero]
  exact (scalarSpatialH1 Q).apply_symm_apply f

theorem orientedBoost_add (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (s t : ℝ) (f : H1) :
    orientedBoost Q (s+t) f=orientedBoost Q s (orientedBoost Q t f) := by
  simp only [orientedBoost_apply,LinearIsometryEquiv.symm_apply_apply,B0_add,
    LinearIsometryEquiv.trans_apply]

theorem orientedBoost_continuous (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (f : H1) :
    Continuous (fun s => orientedBoost Q s f) :=
  (scalarSpatialH1 Q).continuous.comp (B0_continuous ((scalarSpatialH1 Q).symm f))

theorem orientedBoost_U1 (Q : Spatial ≃ₗᵢ[ℝ] Spatial) (s : ℝ)
    (a : Fin 4 → ℝ) (f : H1) :
    orientedBoost Q s (U1 a f)=
      U1 (spatialSpacetime Q (wedgeBoostMap s (spatialSpacetime Q.symm a)))
        (orientedBoost Q s f) := by
  simp only [orientedBoost_apply,scalarSpatialH1_symm]
  rw [scalarSpatialH1_U1,B0_U1,scalarSpatialH1_U1]

def orientedLorentz (q : SpatialOrthogonal) (s : ℝ) : LorentzGrp :=
  orthogonalLorentzHom q * theBoost s * (orthogonalLorentzHom q)⁻¹

theorem orientedLorentz_apply (q : SpatialOrthogonal) (s : ℝ) (a : Fin 4 → ℝ) :
    (orientedLorentz q s).val.mulVec a=
      spatialSpacetime (Unitary.linearIsometryEquiv q)
        (wedgeBoostMap s (spatialSpacetime (Unitary.linearIsometryEquiv q).symm a)) := by
  have hi : (orthogonalLorentzHom q)⁻¹=orthogonalLorentzHom q⁻¹ := (map_inv _ _).symm
  unfold orientedLorentz
  rw [hi]
  change (spatialMatrix (Unitary.linearIsometryEquiv q)*boostMat s*
    spatialMatrix (Unitary.linearIsometryEquiv q⁻¹)).mulVec a= _
  rw [←Matrix.mulVec_mulVec,←Matrix.mulVec_mulVec,spatialMatrix_mulVec,spatialMatrix_mulVec]
  rfl

theorem orientedBoost_U1_actualLorentz (q : SpatialOrthogonal) (s : ℝ)
    (a : Fin 4 → ℝ) (f : H1) :
    orientedBoost (Unitary.linearIsometryEquiv q) s (U1 a f)=
      U1 ((orientedLorentz q s).val.mulVec a)
        (orientedBoost (Unitary.linearIsometryEquiv q) s f) := by
  rw [orientedLorentz_apply]
  exact orientedBoost_U1 _ s a f

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.orientedBoost_zero
#print axioms F1Fecho.OrbitalSpatial.orientedBoost_add
#print axioms F1Fecho.OrbitalSpatial.orientedBoost_continuous
#print axioms F1Fecho.OrbitalSpatial.orientedBoost_U1_actualLorentz
