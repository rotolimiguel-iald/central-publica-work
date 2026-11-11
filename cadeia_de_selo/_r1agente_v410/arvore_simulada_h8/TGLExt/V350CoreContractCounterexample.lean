import TGL.ModularRealization

set_option autoImplicit false
set_option linter.unusedSectionVars false

namespace TGLV350.ContractAudit
open TGL.ModularRealization
noncomputable section

/-- Adversarial model of the LEGACY contract only. This is not a continuous
crossed product or a proposed canonical trace. It exhibits missing obligations. -/
def zeroTraceLegacyCore (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (D : WedgeModularData W) : ContinuousCoreData W D where
  Core := D.wedgeAlgebra.toStarSubalgebra
  instCoreRing := inferInstance
  instCoreStarRing := inferInstance
  instCoreAlgebra := inferInstance
  embedding := StarAlgHom.id ℂ D.wedgeAlgebra.toStarSubalgebra
  embedding_injective := Function.injective_id
  dualAction := fun _ => StarAlgEquiv.refl
  dualAction_zero := rfl
  dualAction_add := fun _ _ => rfl
  canonicalTrace := fun _ => 0
  trace_zero := rfl
  trace_tracial := fun _ _ => rfl
  trace_star := fun _ => rfl
  trace_dual_scaling := by intro s x; simp

/-- The purported canonical trace may vanish on every element under the
legacy signature, even though the algebra embedding is injective. -/
theorem legacy_contract_accepts_zero_trace
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (D : WedgeModularData W) :
    ∃ C : ContinuousCoreData W D, ∀ x : C.Core, C.canonicalTrace x = 0 :=
  ⟨zeroTraceLegacyCore W D, fun _ => rfl⟩

/-- This countermodel cannot supply a positive-trace Three-Locks corner.
It diagnoses the core contract without claiming to bypass the full witness. -/
theorem zeroTraceLegacyCore_has_no_threeLocks
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (D : WedgeModularData W) :
    ¬ Nonempty (ThreeLocksCoreData W D (zeroTraceLegacyCore W D)) := by
  rintro ⟨T⟩
  exact (lt_irrefl (0 : ENNReal)) T.PF_trace_pos

#print axioms zeroTraceLegacyCore
#print axioms legacy_contract_accepts_zero_trace
#print axioms zeroTraceLegacyCore_has_no_threeLocks
end
end TGLV350.ContractAudit
