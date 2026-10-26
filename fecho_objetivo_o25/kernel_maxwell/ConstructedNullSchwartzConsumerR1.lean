import NullSchwartzDomainConstructionR2

/-! Consume the constructed null Schwartz profile on the existing axis-compact
core in the actual H1. The Fourier, mixed first-moment and B0 identities below
no longer take NullSchwartzData as a separate analytic premise: its fields are
constructed by the domain theorem. Choice selects that proved representative.

These statements concern the complex contracted Maxwell wave. They do not
assert the real stress charge, a strong H1 derivative, nonzero modular energy,
or an inhabitant of MaxwellCertificate. The full R8 criterion stays open.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency F1Fecho.WeightedPlancherel
open scoped LineDeriv

def axisCompactNullData (h : H1) (hh : AxisCompactProfile h) (a : Fin 2) :
    NullSchwartzData h a :=
  Classical.choice (axisCompactProfile_has_nullSchwartzData h hh a)

theorem axisCompact_nullContractedWave (h : H1) (hh : AxisCompactProfile h)
    (a : Fin 2) (x : NullFourierSpace) :
    nullContractedWave h a x = angularForward (axisCompactNullData h hh a).profile x :=
  nullContractedWave_eq_angularForward h (axisCompactProfile_strongRegular h hh).1
    a (axisCompactNullData h hh a) x

theorem axisCompact_nullWeightedParseval (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) (a b : Fin 2) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) *
      inner ℂ (nullContractedWave h a x) (nullContractedWave k b x)) =
      (-Complex.I * (2 * Real.pi : ℝ)^3) *
        ∫ p, inner ℂ ((axisCompactNullData h hh a).profile p)
          ((∂_{nullFrequencyDirection} (axisCompactNullData k hk b).profile) p) :=
  nullContractedWave_weighted_parseval h k
    (axisCompactProfile_strongRegular h hh).1 (axisCompactProfile_strongRegular k hk).1
    a b (axisCompactNullData h hh a) (axisCompactNullData k hk b)

theorem axisCompact_nullB0 (s : ℝ) (h : H1) (hh : AxisCompactProfile h) (a : Fin 2) :
    (fun y => nullProfileAmplitude (B0 s h) a y) =ᵐ[orbitalMeasure 0]
      fun y => (axisCompactNullData h hh a).profile
        (nullFrequencyDilation s (nullFourierProfilePoint y)) :=
  nullSchwartz_B0_ae s h a (axisCompactNullData h hh a)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompactNullData
#print axioms F1Fecho.MaxwellGlobal.axisCompact_nullContractedWave
#print axioms F1Fecho.MaxwellGlobal.axisCompact_nullWeightedParseval
#print axioms F1Fecho.MaxwellGlobal.axisCompact_nullB0
