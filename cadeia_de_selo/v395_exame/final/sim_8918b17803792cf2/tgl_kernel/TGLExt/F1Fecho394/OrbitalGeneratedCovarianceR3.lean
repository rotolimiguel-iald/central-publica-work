import TGLExt.F1Fecho394.OrbitalGeneratedUnitaryR3
/-! Strong continuity and exact translation covariance for the generated
scalar Lorentz representation. The matrix-subtype topology is used, not a
topology transported from words. No helicity phase or global net is inferred. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalSpatial
open TGLExt TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

instance lorentzMatrixTopology : TopologicalSpace LorentzGrp := by
  unfold LorentzGrp
  infer_instance

def generatedPullbackMap (L : generatedLorentz) : C(MomentumCoordinates,MomentumCoordinates) :=
  ⟨shellAction (L⁻¹).val,shellAction_continuous _⟩

theorem generatedPullbackMap_continuous : Continuous generatedPullbackMap := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  change Continuous (fun p : generatedLorentz × MomentumCoordinates =>
    momentumOf ((lorentzInv p.1.val.val).mulVec (shellMomentum 0 p.2)))
  unfold momentumOf lorentzInv shellMomentum energy transverseMass
  fun_prop

theorem generatedUnitary_strongly_continuous (f : H1) :
    Continuous (fun L : generatedLorentz => generatedUnitary L f) := by
  exact (continuous_const : Continuous (fun _ : generatedLorentz => f)).compMeasurePreservingLp
    generatedPullbackMap_continuous (fun L => (shellAction_lift L⁻¹).1) (by norm_num)

theorem orbitPairing_lorentz (L : LorentzGrp) (a b : Fin 4 → ℝ) :
    orbitPairing (L.val.mulVec a) (L.val.mulVec b)=orbitPairing a b := by
  rw [orbitPairing_eq_eta,orbitPairing_eq_eta]
  calc
    dotProduct (L.val.mulVec a) (eta4.mulVec (L.val.mulVec b)) =
        dotProduct a ((L.valᵀ*eta4*L.val).mulVec b) := by
          rw [←Matrix.mulVec_mulVec,←Matrix.mulVec_mulVec,Matrix.dotProduct_transpose_mulVec]
          exact dotProduct_comm _ _
    _ = dotProduct a (eta4.mulVec b) := by rw [L.property]

theorem lorentz_mul_inverse_apply (L : LorentzGrp) (a : Fin 4 → ℝ) :
    L.val.mulVec ((L⁻¹).val.mulVec a)=a := by
  rw [Matrix.mulVec_mulVec,←lorentzGrp_mul_val,mul_inv_cancel,lorentzGrp_one_val,Matrix.one_mulVec]

theorem orbitPairing_lorentz_inverse (L : LorentzGrp) (a b : Fin 4 → ℝ) :
    orbitPairing a ((L⁻¹).val.mulVec b)=orbitPairing (L.val.mulVec a) b := by
  have h := orbitPairing_lorentz L a ((L⁻¹).val.mulVec b)
  rw [lorentz_mul_inverse_apply] at h
  exact h.symm

theorem generatedPhase_ae (L : generatedLorentz) (a : Fin 4 → ℝ) :
    (fun p => orbitalPhase 0 a (shellAction (L⁻¹).val p)) =ᵐ[orbitalMeasure 0]
      orbitalPhase 0 (L.val.val.mulVec a) := by
  filter_upwards [(shellAction_lift L⁻¹).2] with p hp
  unfold orbitalPhase
  rw [hp]
  exact congrArg phase (orbitPairing_lorentz_inverse L.val a (shellMomentum 0 p))

theorem generatedUnitary_U1 (L : generatedLorentz) (a : Fin 4 → ℝ) (f : H1) :
    generatedUnitary L (U1 a f)=U1 (L.val.val.mulVec a) (generatedUnitary L f) := by
  change generatedUnitary L (orbitalTranslation 0 a f)=
    orbitalTranslation 0 (L.val.val.mulVec a) (generatedUnitary L f)
  have htr := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (orbitalTranslation_ae 0 a f)
  apply Lp.ext
  filter_upwards [generatedUnitary_ae L (orbitalTranslation 0 a f),htr,
    orbitalTranslation_ae 0 (L.val.val.mulVec a) (generatedUnitary L f),
    generatedUnitary_ae L f,generatedPhase_ae L a] with p h1 h2 h3 h4 h5
  rw [h1,h2,h3,h4,h5]

def generatedPoincare (a : Fin 4 → ℝ) (L : generatedLorentz) : PoincareGroup := ⟨a,L.val⟩

theorem generatedPoincare_mul (a b : Fin 4 → ℝ) (L M : generatedLorentz) :
    generatedPoincare a L*generatedPoincare b M=
      generatedPoincare (a+L.val.val.mulVec b) (L*M) := rfl

def generatedPoincareH1 (a : Fin 4 → ℝ) (L : generatedLorentz) : H1≃ₗᵢ[ℂ]H1 :=
  (generatedUnitary L).trans (U1 a)

theorem generatedPoincareH1_mul (a b : Fin 4 → ℝ) (L M : generatedLorentz) (f : H1) :
    generatedPoincareH1 (a+L.val.val.mulVec b) (L*M) f=
      generatedPoincareH1 a L (generatedPoincareH1 b M f) := by
  change U1 (a+L.val.val.mulVec b) (generatedUnitary (L*M) f)=
    U1 a (generatedUnitary L (U1 b (generatedUnitary M f)))
  rw [generatedUnitary_U1]
  change U1 (a+L.val.val.mulVec b) (generatedPullback (L*M) f)=_
  rw [generatedPullback_mul]
  exact orbitalTranslation_add 0 a _ _

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.generatedUnitary_strongly_continuous
#print axioms F1Fecho.OrbitalSpatial.orbitPairing_lorentz
#print axioms F1Fecho.OrbitalSpatial.generatedUnitary_U1
#print axioms F1Fecho.OrbitalSpatial.generatedPoincareH1_mul
