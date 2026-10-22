import TGLExt.V350RegularCoreCommutant
import TGLExt.V350ConstantFibreIdentification

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 600000

namespace TGLV350.Regular
open TGLExt
noncomputable section

theorem dualFixedCore_fibreCandidate_mem (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ dualFixedCore P) : fibreCandidate B ∈ theFactorObject P := by
  apply (fibre_mem_regularCore_iff P (fibreCandidate B)).mp
  rw [← dualFixedCore_eq_fibre_candidate P B hB]
  exact ((dualFixedCore_mem_iff P B).mp hB).1

/-- The dual-fixed algebra of this concrete regular representation is
exactly the amplified original base, on the same tower and real L² space. -/
theorem dualFixedCore_eq_amplified_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    B ∈ dualFixedCore P ↔ ∃ C ∈ theFactorObject P, B = fibre C := by
  constructor
  · intro hB
    exact ⟨fibreCandidate B, dualFixedCore_fibreCandidate_mem P B hB,
      dualFixedCore_eq_fibre_candidate P B hB⟩
  · rintro ⟨C,hC,rfl⟩
    exact amplified_factor_mem_dualFixedCore P C hC

theorem dualFixedCore_existsUnique_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ dualFixedCore P) :
    ∃! C : theFactorObject P, B = fibre (C : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  obtain ⟨C,hC,he⟩ := (dualFixedCore_eq_amplified_base P B).mp hB
  refine ⟨⟨C,hC⟩,he,?_⟩
  intro D hD
  apply Subtype.ext
  exact fibre_injective (hD.symm.trans he)

#print axioms dualFixedCore_fibreCandidate_mem
#print axioms dualFixedCore_eq_amplified_base
#print axioms dualFixedCore_existsUnique_base
end
end TGLV350.Regular
