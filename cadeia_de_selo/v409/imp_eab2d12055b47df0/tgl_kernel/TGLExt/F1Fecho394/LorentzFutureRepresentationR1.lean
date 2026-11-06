import TGLExt.F1Fecho394.LorentzFutureGenerationR6
/-! Strong continuity and the actual product law of the scalar representation
on every Lorentz matrix with future time column. This has no helicity phase. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.OrbitalSpatial
open TGLExt TGLExt.ImportedSQ

abbrev FutureLorentz := {L : LorentzGrp // 0 < lorentzLinear L timeBasis 0}

def futureToGenerated (L : FutureLorentz) : generatedLorentz :=
  ⟨L.val,future_lorentz_mem_generated L.val L.property⟩

theorem futureToGenerated_continuous : Continuous futureToGenerated := by
  exact continuous_subtype_val.subtype_mk _

theorem futureLorentzUnitary_strongly_continuous (f : H1) :
    Continuous (fun L : FutureLorentz => futureLorentzUnitary L.val L.property f) :=
  (generatedUnitary_strongly_continuous f).comp futureToGenerated_continuous

theorem futureLorentzUnitary_mul (L M : LorentzGrp)
    (hL : 0 < lorentzLinear L timeBasis 0) (hM : 0 < lorentzLinear M timeBasis 0)
    (hLM : 0 < lorentzLinear (L*M) timeBasis 0) (f : H1) :
    futureLorentzUnitary (L*M) hLM f=
      futureLorentzUnitary L hL (futureLorentzUnitary M hM f) := by
  change generatedPullback (⟨L,future_lorentz_mem_generated L hL⟩ *
    ⟨M,future_lorentz_mem_generated M hM⟩) f=_
  exact generatedPullback_mul _ _ _

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.futureToGenerated_continuous
#print axioms F1Fecho.OrbitalSpatial.futureLorentzUnitary_strongly_continuous
#print axioms F1Fecho.OrbitalSpatial.futureLorentzUnitary_mul
