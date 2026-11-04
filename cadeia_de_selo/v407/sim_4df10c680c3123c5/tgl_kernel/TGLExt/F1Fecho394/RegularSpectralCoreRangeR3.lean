import TGLExt.F1Fecho394.RegularSpectralTranslationR2
import TGLExt.F1Fecho394.RegularDualOrbitGeneratedR2
import TGLExt.F1Fecho394.IsometricReducingRangeR1
import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.F1Fecho394.RegularRightOrbitPointwiseR1
/-! The actual spectral-code range is reducing for the complete represented
regular core, using star-bicommutant transport rather than an assumed density result. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularSpectralCoreRange
open TGLV350.Regular F1Fecho.RegularNormalizedFourier
open F1Fecho.RegularCovariantCore F1Fecho.RegularSpectralTranslation
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualOrbit_fibre (A : H →L[ℂ] H) :
    dualOrbitRepresentation (fibre A)=fibre (fibre A) :=
  operatorFieldLift_constant (dualIntegralFamily (fibre A)) (fibre A)
    (fun s => dualAmbient_fibre s A)

theorem dualOrbit_regular (B : UnitaryFlow H) (t : ℝ) :
    dualOrbitRepresentation (regularUnitary B t) =
      characterMultiplier t * fibre (regularUnitary B t) := by
  ext1 f
  apply MeasureTheory.Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily (regularUnitary B t)) f,
    characterMultiplier_ae t (fibre (regularUnitary B t) f),fibre_ae (regularUnitary B t) f]
    with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily (regularUnitary B t)) f s =
    characterMultiplier t (fibre (regularUnitary B t) f) s
  rw [h1,h2,h3]
  change dualAmbient s (regularUnitary B t) (f s) = characterPhase t s • regularUnitary B t (f s)
  rw [dual_on_regular]
  rw [RegularRightAction.phase_symmetric s t]
  rfl

theorem spectralCode_regular (B : UnitaryFlow H) (t : ℝ) (f : RegularHilbert H) :
    spectralCode (regularUnitary B t f) = dualOrbitRepresentation (regularUnitary B t) (spectralCode f) := by
  change spectralCode (fibre (boostCLM B t) (shift t f)) = _
  rw [spectralCode_fibre,spectralCode_shift,dualOrbit_regular]
  change fibre (fibre (boostCLM B t))
      (characterMultiplier t (fibre (shift t) (spectralCode f))) =
    characterMultiplier t (fibre (fibre (boostCLM B t) * shift t) (spectralCode f))
  rw [fibre_mul]
  exact congrArg (fun T : RegularHilbert (RegularHilbert H) →L[ℂ]
      RegularHilbert (RegularHilbert H) => T (fibre (shift t) (spectralCode f)))
    (characterMultiplier_commutes_fibre t (fibre (boostCLM B t))).symm

def codeProjection : RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H) :=
  IsometricReducingRange.projection spectralCode

theorem projection_commutes_fibre (A : H →L[ℂ] H) :
    dualOrbitRepresentation (fibre A) * codeProjection =
      codeProjection * dualOrbitRepresentation (fibre A) := by
  apply IsometricReducingRange.projection_commutes spectralCode (fibre A)
  · ext1 f
    rw [dualOrbit_fibre]
    exact (spectralCode_fibre A f).symm
  · rw [←map_star,←fibre_star]
    ext1 f
    rw [dualOrbit_fibre]
    exact (spectralCode_fibre (star A) f).symm

theorem projection_commutes_regular (B : UnitaryFlow H) (t : ℝ) :
    dualOrbitRepresentation (regularUnitary B t) * codeProjection =
      codeProjection * dualOrbitRepresentation (regularUnitary B t) := by
  apply IsometricReducingRange.projection_commutes spectralCode (regularUnitary B t)
  · ext1 f
    exact (spectralCode_regular B t f).symm
  · rw [←map_star,RegularCovariantCore.regular_star]
    ext1 f
    exact (spectralCode_regular B (-t) f).symm

theorem projection_commutes_core (B : UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A ∈ core B M) :
    dualOrbitRepresentation A * codeProjection=codeProjection * dualOrbitRepresentation A := by
  apply RegularDualOrbitGenerated.dualOrbit_commutes_of_generators (generators B M) codeProjection ?_ A hA
  rw [StarSubalgebra.mem_centralizer_iff]
  rintro _ ⟨a,ha,rfl⟩
  have h : dualOrbitRepresentation a * codeProjection=codeProjection * dualOrbitRepresentation a := by
    rcases ha with ⟨b,hb,rfl⟩ | ⟨t,rfl⟩
    · exact projection_commutes_fibre b
    · exact projection_commutes_regular B t
  refine ⟨h,?_⟩
  have hs := congrArg star h
  simpa only [star_mul,codeProjection,IsometricReducingRange.projection_star] using hs.symm

theorem spectralCode_range_preserved (B : UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A ∈ core B M) :
    Set.MapsTo (dualOrbitRepresentation A) (Set.range (spectralCode (H:=H)))
      (Set.range (spectralCode (H:=H))) := by
  intro x hx
  apply (IsometricReducingRange.mem_range_iff (spectralCode (H:=H)) _).mpr
  have hh := congrArg (fun T : RegularHilbert (RegularHilbert H) →L[ℂ]
    RegularHilbert (RegularHilbert H) => T x) (projection_commutes_core B M A hA)
  change dualOrbitRepresentation A (codeProjection x)=codeProjection (dualOrbitRepresentation A x) at hh
  have hp : codeProjection x=x :=
    (IsometricReducingRange.mem_range_iff (spectralCode (H:=H)) x).mp hx
  rw [hp] at hh
  exact hh.symm


end F1Fecho.RegularSpectralCoreRange
#print axioms F1Fecho.RegularSpectralCoreRange.dualOrbit_fibre
#print axioms F1Fecho.RegularSpectralCoreRange.dualOrbit_regular
#print axioms F1Fecho.RegularSpectralCoreRange.spectralCode_regular
#print axioms F1Fecho.RegularSpectralCoreRange.projection_commutes_fibre
#print axioms F1Fecho.RegularSpectralCoreRange.projection_commutes_regular
#print axioms F1Fecho.RegularSpectralCoreRange.projection_commutes_core
#print axioms F1Fecho.RegularSpectralCoreRange.spectralCode_range_preserved
