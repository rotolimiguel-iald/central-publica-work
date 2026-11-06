import TGLExt.V350RegularGeneratedAlgebra

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem centralizer_wot_preimage (S : Set (H →L[ℂ] H)) :
    {A : H →WOT[ℂ] H | A.toCLM ∈ Set.centralizer S} =
      Set.centralizer (ContinuousLinearMapWOT.ofCLM '' S) := by
  ext A
  simp only [Set.mem_setOf_eq, Set.mem_centralizer_iff]
  constructor
  · intro h B hB
    rcases hB with ⟨C, hC, rfl⟩
    apply ContinuousLinearMapWOT.toCLM_injective
    exact h C hC
  · intro h B hB
    exact congrArg ContinuousLinearMapWOT.toCLM (h (.ofCLM B) ⟨B, hB, rfl⟩)

/-- The bicommutant definition implies WOT closure. This is only this direction
of the bicommutant theorem; no converse, predual, or normal trace is asserted. -/
theorem vonNeumann_wot_closed (N : VonNeumannAlgebra H) :
    IsClosed {A : H →WOT[ℂ] H | A.toCLM ∈ N} := by
  have heq : {A : H →WOT[ℂ] H | A.toCLM ∈ N} =
      Set.centralizer (ContinuousLinearMapWOT.ofCLM ''
        Set.centralizer (N : Set (H →L[ℂ] H))) := by
    rw [← centralizer_wot_preimage]
    ext A
    change A.toCLM ∈ (N : Set (H →L[ℂ] H)) ↔
      A.toCLM ∈ Set.centralizer (Set.centralizer (N : Set (H →L[ℂ] H)))
    rw [VonNeumannAlgebra.centralizer_centralizer]
  rw [heq]
  exact Set.isClosed_centralizer _

theorem regularCore_wot_closed (P : TGLExt.SiteProfile) :
    IsClosed {A : RegularHilbert (TGLExt.TowerHilbert P) →WOT[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P} :=
  vonNeumann_wot_closed (regularCoreAlgebra P)

#print axioms vonNeumann_wot_closed
#print axioms regularCore_wot_closed
end
end TGLV350.Regular
