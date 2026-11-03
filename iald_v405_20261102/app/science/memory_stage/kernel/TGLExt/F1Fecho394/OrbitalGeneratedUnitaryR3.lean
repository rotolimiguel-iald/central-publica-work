import TGLExt.F1Fecho394.OrbitalGeneratedMeasureR2
/-! A scalar unitary representation of the actual generated Lorentz subgroup.
The pullback is the explicit spatial projection of L^{-1}p on the mass shell;
it does not depend on a word in generators or on a selected lift witness. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Set Matrix
namespace F1Fecho.OrbitalSpatial
open TGLExt TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016

def shellAction (L : LorentzGrp) (p : MomentumCoordinates) : MomentumCoordinates :=
  momentumOf (L.val.mulVec (shellMomentum 0 p))

theorem shellAction_continuous (L : LorentzGrp) : Continuous (shellAction L) := by
  unfold shellAction momentumOf shellMomentum energy transverseMass
  fun_prop

theorem shellAction_eq_lift {L : LorentzGrp} {r : MomentumCoordinates → MomentumCoordinates}
    (hr : ShellLift L r) : shellAction L=ᵐ[orbitalMeasure 0] r := by
  filter_upwards [hr.2] with p hp
  change momentumOf (L.val.mulVec (shellMomentum 0 p))=r p
  rw [←hp,momentumOf_shell]

theorem shellAction_lift (L : generatedLorentz) : ShellLift L.val (shellAction L.val) := by
  obtain ⟨r,hr⟩ := (generated_admissible L.property).1
  have he := shellAction_eq_lift hr
  refine ⟨⟨(shellAction_continuous _).measurable,?_⟩,?_⟩
  · rw [Measure.map_congr he]
    exact hr.1.map_eq
  · filter_upwards [he,hr.2] with p h1 h2
    rw [h1,h2]

theorem shellAction_one_ae : shellAction 1=ᵐ[orbitalMeasure 0] id :=
  shellAction_eq_lift shellLift_one

theorem shellAction_mul_ae (L M : generatedLorentz) :
    shellAction (L*M).val=ᵐ[orbitalMeasure 0] shellAction L.val ∘ shellAction M.val :=
  shellAction_eq_lift (shellLift_mul (shellAction_lift L) (shellAction_lift M))

def generatedPullback (L : generatedLorentz) : H1 →ₗᵢ[ℂ] H1 :=
  Lp.compMeasurePreservingₗᵢ ℂ (shellAction (L⁻¹).val) (shellAction_lift L⁻¹).1

theorem generatedPullback_ae (L : generatedLorentz) (f : H1) :
    generatedPullback L f=ᵐ[orbitalMeasure 0] fun p => f (shellAction (L⁻¹).val p) :=
  Lp.coeFn_compMeasurePreserving f (shellAction_lift L⁻¹).1

theorem generatedPullback_one (f : H1) : generatedPullback 1 f=f := by
  apply Lp.ext
  filter_upwards [generatedPullback_ae 1 f,shellAction_one_ae] with p h1 h2
  simpa only [inv_one,OneMemClass.coe_one,h2,id_eq] using h1

theorem generatedPullback_mul (L M : generatedLorentz) (f : H1) :
    generatedPullback (L*M) f=generatedPullback L (generatedPullback M f) := by
  have hc := shellAction_mul_ae M⁻¹ L⁻¹
  have hp := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (generatedPullback_ae M f)
  apply Lp.ext
  filter_upwards [generatedPullback_ae (L*M) f,
    generatedPullback_ae L (generatedPullback M f),hp,hc] with p h1 h2 h3 h4
  rw [h1,h2,h3]
  congr 1
  simpa only [_root_.mul_inv_rev,Function.comp_apply] using h4

theorem generatedPullback_inverse (L : generatedLorentz) (f : H1) :
    generatedPullback L (generatedPullback L⁻¹ f)=f := by
  rw [←generatedPullback_mul,mul_inv_cancel,generatedPullback_one]

def generatedUnitary (L : generatedLorentz) : H1≃ₗᵢ[ℂ]H1 :=
  LinearIsometryEquiv.ofLinearIsometry (generatedPullback L)
    (generatedPullback L⁻¹).toLinearMap
    (by apply LinearMap.ext; intro f; exact generatedPullback_inverse L f)
    (by
      apply LinearMap.ext
      intro f
      change generatedPullback L⁻¹ (generatedPullback L f)=f
      simpa only [inv_inv] using generatedPullback_inverse L⁻¹ f)

theorem generatedUnitary_apply (L : generatedLorentz) (f : H1) :
    generatedUnitary L f=generatedPullback L f := rfl

def generatedUnitaryHom : generatedLorentz →* (H1≃ₗᵢ[ℂ]H1) where
  toFun := generatedUnitary
  map_one' := by apply LinearIsometryEquiv.ext; intro f; exact generatedPullback_one f
  map_mul' L M := by apply LinearIsometryEquiv.ext; intro f; exact generatedPullback_mul L M f

theorem generatedUnitary_ae (L : generatedLorentz) (f : H1) :
    generatedUnitary L f=ᵐ[orbitalMeasure 0] fun p => f (shellAction (L⁻¹).val p) :=
  generatedPullback_ae L f

def generatedSpatial (q : SpatialOrthogonal) : generatedLorentz :=
  ⟨orthogonalLorentzHom q,spatial_mem_generated q⟩

def generatedBoost (s : ℝ) : generatedLorentz := ⟨theBoost s,boost_mem_generated s⟩

theorem generatedUnitary_spatial (q : SpatialOrthogonal) (f : H1) :
    generatedUnitary (generatedSpatial q) f=scalarOrthogonalH1 q f := by
  change generatedUnitary (generatedSpatial q) f=spatialUnitary 0 (Unitary.linearIsometryEquiv q) f
  have h := shellAction_eq_lift (shellLift_spatial q⁻¹)
  apply Lp.ext
  filter_upwards [generatedUnitary_ae (generatedSpatial q) f,
    spatialUnitary_ae 0 (Unitary.linearIsometryEquiv q) f,h] with p h1 h2 h3
  rw [h1,h2]
  congr 1
  have hi : ((generatedSpatial q)⁻¹).val=orthogonalLorentzHom q⁻¹ := (map_inv _ _).symm
  rw [hi,h3]
  rfl

theorem generatedUnitary_boost (s : ℝ) (f : H1) :
    generatedUnitary (generatedBoost s) f=B0 s f := by
  change generatedUnitary (generatedBoost s) f=orbitalScalarBoost 0 s f
  have h := shellAction_eq_lift (shellLift_boost (-s))
  apply Lp.ext
  filter_upwards [generatedUnitary_ae (generatedBoost s) f,orbitalScalarBoost_ae 0 s f,h]
    with p h1 h2 h3
  rw [h1,h2]
  congr 1
  change shellAction ((theBoost s)⁻¹) p=coordinateBoost 0 (-s) p
  rw [theBoost_inv_eq,h3]

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.shellAction_lift
#print axioms F1Fecho.OrbitalSpatial.generatedUnitaryHom
#print axioms F1Fecho.OrbitalSpatial.generatedUnitary_spatial
#print axioms F1Fecho.OrbitalSpatial.generatedUnitary_boost
