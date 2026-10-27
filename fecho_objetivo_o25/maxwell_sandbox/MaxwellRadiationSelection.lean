import MaxwellRadiationWitness

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! The general Maxwell radiation closure cannot be a perfect-fluid screen closure. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen

/-- Universal TGL-L screen form: every regular radiation profile has zero 1--2 pressure contrast. -/
def UniversalPerfectFluidScreenClosure : Prop :=
  ∀ h : H1, RegularProfile h →
    (realProfileStress h 2 2 0 - realProfileStress h 1 1 0).re = 0

/-- The general Maxwell radiation dynamics refutes a universal perfect-fluid screen closure. -/
theorem universalPerfectFluidScreenClosure_impossible : ¬ UniversalPerfectFluidScreenClosure := by
  intro H
  obtain ⟨f, b, hf, hpos⟩ := exists_tensor01_radiation_witness
  let h : H1 := fullySymmetrizedProfile (momentumSmearCLM f)
  have hh : RegularProfile h := fullySymmetrizedProfile_regular (momentumSmearCLM f)
    (momentumSmear_regular f)
  have hp : 0 < (realProfileStress h 2 2 0 - realProfileStress h 1 1 0).re :=
    tensor01_fullySymmetric_pressure_contrast_pos f b hf hpos
  exact (ne_of_gt hp) (H h hh)

/-- The explicit witness is not a TGL-L perfect-fluid screen configuration. -/
theorem tensor01_not_perfectFluidScreen (f : SchwartzTensor) (b : Spacetime → ℂ)
    (hf : ∀ p, f p = b p • tensorUnit01) (hpos : 0 < (regularWave f 0 1 0).re) :
    (realProfileStress (fullySymmetrizedProfile (momentumSmearCLM f)) 2 2 0 -
      realProfileStress (fullySymmetrizedProfile (momentumSmearCLM f)) 1 1 0).re ≠ 0 :=
  ne_of_gt (tensor01_fullySymmetric_pressure_contrast_pos f b hf hpos)

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.universalPerfectFluidScreenClosure_impossible
#print axioms F1Fecho.MaxwellGlobal.tensor01_not_perfectFluidScreen
