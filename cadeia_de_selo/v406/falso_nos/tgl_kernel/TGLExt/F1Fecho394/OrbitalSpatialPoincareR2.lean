import TGLExt.F1Fecho394.OrbitalSpatialLorentzR2
/-! A concrete spatial subgroup of the existing PoincareGroup, represented
on the original H1. Arbitrary boosts and helicity phases remain separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Matrix
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016 TGLExt TGLExt.ImportedSQ

theorem spacetime_ext {a b : Fin 4 → ℝ} (h0 : a 0=b 0)
    (hs : spacetimeSpatial a=spacetimeSpatial b) : a=b := by
  have hc : (![a 2,a 3],a 1)=(![b 2,b 3],b 1) := spatialChart.injective hs
  have h1 := congrArg Prod.snd hc
  have h2 := congrArg (fun p : MomentumCoordinates => p.1 0) hc
  have h3 := congrArg (fun p : MomentumCoordinates => p.1 1) hc
  funext i
  fin_cases i
  · exact h0
  · exact h1
  · exact h2
  · exact h3

theorem spatialSpacetime_refl (a : Fin 4 → ℝ) :
    spatialSpacetime (LinearIsometryEquiv.refl ℝ Spatial) a=a := by
  apply spacetime_ext
  · rfl
  · rw [spacetimeSpatial_rotation]
    rfl

theorem spatialSpacetime_trans (Q R : Spatial ≃ₗᵢ[ℝ] Spatial) (a : Fin 4 → ℝ) :
    spatialSpacetime (Q.trans R) a=spatialSpacetime R (spatialSpacetime Q a) := by
  apply spacetime_ext
  · rfl
  · rw [spacetimeSpatial_rotation,spacetimeSpatial_rotation,spacetimeSpatial_rotation]
    rfl

theorem spatialMatrix_refl : spatialMatrix (LinearIsometryEquiv.refl ℝ Spatial)=1 := by
  have h : spatialSpacetimeLinear (LinearIsometryEquiv.refl ℝ Spatial)=LinearMap.id := by
    apply LinearMap.ext
    intro a
    exact spatialSpacetime_refl a
  unfold spatialMatrix
  rw [h,LinearMap.toMatrix'_id]

theorem spatialMatrix_trans (Q R : Spatial ≃ₗᵢ[ℝ] Spatial) :
    spatialMatrix (Q.trans R)=spatialMatrix R*spatialMatrix Q := by
  have h : spatialSpacetimeLinear (Q.trans R)=
      (spatialSpacetimeLinear R).comp (spatialSpacetimeLinear Q) := by
    apply LinearMap.ext
    intro a
    exact spatialSpacetime_trans Q R a
  unfold spatialMatrix
  rw [h,LinearMap.toMatrix'_comp]

def orthogonalLorentzHom : SpatialOrthogonal →* LorentzGrp where
  toFun q := spatialLorentz (Unitary.linearIsometryEquiv q)
  map_one' := by
    apply Subtype.ext
    change spatialMatrix (Unitary.linearIsometryEquiv (1 : SpatialOrthogonal))=1
    have h : Unitary.linearIsometryEquiv (1 : SpatialOrthogonal)=LinearIsometryEquiv.refl ℝ Spatial := by
      ext x; rfl
    rw [h,spatialMatrix_refl]
  map_mul' q r := by
    apply Subtype.ext
    change spatialMatrix (Unitary.linearIsometryEquiv (q*r))=
      spatialMatrix (Unitary.linearIsometryEquiv q)*spatialMatrix (Unitary.linearIsometryEquiv r)
    have h : Unitary.linearIsometryEquiv (q*r)=
        (Unitary.linearIsometryEquiv r).trans (Unitary.linearIsometryEquiv q) := by
      ext x; rfl
    rw [h,spatialMatrix_trans]

def spatialPoincare (a : Fin 4 → ℝ) (q : SpatialOrthogonal) : PoincareGroup :=
  ⟨a,orthogonalLorentzHom q⟩

theorem spatialPoincare_mul (a b : Fin 4 → ℝ) (q r : SpatialOrthogonal) :
    spatialPoincare a q*spatialPoincare b r=
      spatialPoincare (a+spatialSpacetime (Unitary.linearIsometryEquiv q) b) (q*r) := by
  apply poincare_ext
  · change a+(spatialMatrix (Unitary.linearIsometryEquiv q)).mulVec b= _
    rw [spatialMatrix_mulVec]
    rfl
  · exact (orthogonalLorentzHom.map_mul q r).symm

def spatialPoincareH1 (a : Fin 4 → ℝ) (q : SpatialOrthogonal) : H1≃ₗᵢ[ℂ]H1 :=
  (scalarOrthogonalH1 q).trans (U1 a)

theorem spatialPoincareH1_mul (a b : Fin 4 → ℝ) (q r : SpatialOrthogonal) (f : H1) :
    spatialPoincareH1 (a+spatialSpacetime (Unitary.linearIsometryEquiv q) b) (q*r) f=
      spatialPoincareH1 a q (spatialPoincareH1 b r f) := by
  change U1 (a+spatialSpacetime (Unitary.linearIsometryEquiv q) b) (scalarOrthogonalH1 (q*r) f)=
    U1 a (scalarOrthogonalH1 q (U1 b (scalarOrthogonalH1 r f)))
  rw [scalarOrthogonalH1_mul,scalarOrthogonalH1_U1]
  exact orbitalTranslation_add 0 a _ _

theorem spatialPoincareH1_one (f : H1) : spatialPoincareH1 0 1 f=f := by
  change U1 0 (scalarOrthogonalH1 1 f)=f
  rw [scalarOrthogonalH1_one]
  exact orbitalTranslation_zero 0 f

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.orthogonalLorentzHom
#print axioms F1Fecho.OrbitalSpatial.spatialPoincare_mul
#print axioms F1Fecho.OrbitalSpatial.spatialPoincareH1_mul
#print axioms F1Fecho.OrbitalSpatial.spatialPoincareH1_one
