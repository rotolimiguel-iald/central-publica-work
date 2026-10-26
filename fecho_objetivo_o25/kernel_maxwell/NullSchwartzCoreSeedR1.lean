import PhysicalSmearDensityR6
import RegularMaxwellDensityR2

/-! Candidate seed for the null Schwartz domain.
This reuses the existing dense axis-cutoff class in the actual H1, its
strong regularity, and the existing physical spacetime smearing map.
The nonzero witness is selected from this dense class using the already
constructed nonzero physical smear. No new analytic hypothesis is added.

This file does NOT yet inhabit NullSchwartzData: the smooth compact
null-coordinate transport and the a.e. representative transport remain
explicit obligations. It does not claim a nonzero boost/modular energy.
No compilation was run by the author.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016

 theorem axisCompactProfile_strongRegular (h : H1) (hh : AxisCompactProfile h) :
    StrongRegularProfile h := by
  obtain ⟨g, he, hc, hd, _⟩ := hh
  exact smoothCompactProfile_strongRegular h ⟨g, he, hc, hd⟩

 theorem axisCompact_physical_regular_dense :
    Dense {h : H1 | AxisCompactProfile h ∧ StrongRegularProfile h ∧
      h ∈ Set.range physicalSmearCLM} := by
  exact axisCompactProfile_dense.mono (fun h hh =>
    ⟨hh, axisCompactProfile_strongRegular h hh,
      axisCompactProfile_mem_range_physicalSmear h hh⟩)

/-- A nonzero actual H1 seed, with regularity and membership in the existing
physical smearing range. Its null-coordinate Schwartz representation is
not asserted here. -/
 theorem exists_nonzero_axisCompact_physical_regular :
    ∃ h : H1, h ≠ 0 ∧ AxisCompactProfile h ∧ StrongRegularProfile h ∧
      h ∈ Set.range physicalSmearCLM := by
  obtain ⟨f, hf⟩ := exists_nonzero_real_physicalSmear
  have hne : ({0}ᶜ : Set H1).Nonempty := by
    refine ⟨physicalSmearCLM f.val, ?_⟩
    simpa only [mem_compl_iff, mem_singleton_iff] using hf
  obtain ⟨h, hh, hz⟩ := axisCompact_physical_regular_dense.exists_mem_open
    isClosed_singleton.isOpen_compl hne
  exact ⟨h, by simpa only [mem_compl_iff, mem_singleton_iff] using hz, hh⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompactProfile_strongRegular
#print axioms F1Fecho.MaxwellGlobal.axisCompact_physical_regular_dense
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_axisCompact_physical_regular
