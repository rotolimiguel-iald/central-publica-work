import MaxwellNullSchwartzCoreTransportR3
import NullFrequencyAETransportR2
import NullSchwartzCoreSeedR1

/-! Candidate assembly S5-S6 on the same orbital H1.
The existing dense axis-cutoff profiles supply the smooth compact representative.
The explicit null-coordinate construction supplies its Schwartz transform, and
the measure transport supplies the almost-everywhere relation. None of the
fields of NullSchwartzData is imposed as an extra analytic assumption.

This establishes domain inhabitation, density, and a nonzero H1 witness only.
The strong boost derivative, real charge identity, nonzero modular energy,
and complete Maxwell/source certificate are separate remaining obligations.
No build or independent acceptance is claimed by this source comment.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory SchwartzMap
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency
open scoped ContDiff

/-- All regularity and representative fields are constructed from the existing
axis-compact core; the existential output does not hide a domain assumption. -/
theorem axisCompactProfile_has_nullSchwartzData (h : H1)
    (hh : AxisCompactProfile h) (a : Fin 2) : Nonempty (NullSchwartzData h a) := by
  obtain ⟨g, he, hc, hg, ε, hε, hcut⟩ := hh
  have hcut' : ∀ y : MomentumCoordinates, ‖y.1‖ ≤ ε → g y = 0 := hcut
  refine ⟨{
    profile := nullCoreSchwartzProfile g hg hc ε hε hcut' a
    zero_nonpositive := nullCoreSchwartzProfile_nonpositive g hg hc ε hε hcut' a
    null_ae := ?_
    orbital_ae := ?_ }⟩
  · have hn := orbital_ae_nullMomentum (fun y => h y = g y) he
    filter_upwards [hn] with q hq
    filter_upwards [hq, ae_restrict_mem measurableSet_Ioi] with u hu hupos
    rw [nullCoreSchwartzProfile_null g hg hc ε hε hcut' a q u hupos]
    simp only [nullProfileAmplitude, screenAmplitudeOf, hu]
  · filter_upwards [he, transverseProjection_ne_zero_ae] with y hy hyaxis
    have hyaxis' : y.1 ≠ 0 := hyaxis
    rw [nullCoreSchwartzProfile_orbital g hg hc ε hε hcut' a y hyaxis']
    simp only [nullProfileAmplitude, screenAmplitudeOf, hy]

/-- The common domain is dense in the original H1, with its physical-smearing
membership and strong regularity retained rather than replaced by a new space. -/
theorem nullSchwartz_physical_regular_dense :
    Dense {h : H1 | AxisCompactProfile h ∧ StrongRegularProfile h ∧
      h ∈ Set.range physicalSmearCLM ∧ ∀ a : Fin 2, Nonempty (NullSchwartzData h a)} := by
  exact axisCompact_physical_regular_dense.mono (fun h hh =>
    ⟨hh.1, hh.2.1, hh.2.2, fun a => axisCompactProfile_has_nullSchwartzData h hh.1 a⟩)

/-- Non-vacuity in the actual H1. This asserts no nonzero energy expectation. -/
theorem exists_nonzero_nullSchwartz_physical_regular :
    ∃ h : H1, h ≠ 0 ∧ AxisCompactProfile h ∧ StrongRegularProfile h ∧
      h ∈ Set.range physicalSmearCLM ∧ ∀ a : Fin 2, Nonempty (NullSchwartzData h a) := by
  obtain ⟨h, hn, ha, hr, hp⟩ := exists_nonzero_axisCompact_physical_regular
  exact ⟨h, hn, ha, hr, hp, fun a => axisCompactProfile_has_nullSchwartzData h ha a⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_has_nullSchwartzData
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_physical_regular_dense
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_nullSchwartz_physical_regular
