import TGLExt.V350ScalarGNSAction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

/-- Completion of the actual finite-square orbit range, in the ambient L² norm.
No density claim about the maximal scalar-weight domain is built into this definition. -/
def scalarGNSSubspace (P : SiteProfile) :
    Submodule ℂ (RegularHilbert (RegularHilbert (TowerHilbert P))) :=
  (scalarGNSLinear P).range.topologicalClosure

abbrev ScalarGNSHilbert (P : SiteProfile) := scalarGNSSubspace P

instance scalarGNSCompleteSpace (P : SiteProfile) : CompleteSpace (ScalarGNSHilbert P) :=
  Submodule.topologicalClosure.completeSpace (scalarGNSLinear P).range

def scalarGNSEmbedding (P : SiteProfile) : finiteDualLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P :=
  (scalarGNSLinear P).codRestrict (scalarGNSSubspace P)
    (fun A => (scalarGNSLinear P).range.le_topologicalClosure ⟨A,rfl⟩)

theorem scalarGNSEmbedding_injective (P : SiteProfile) :
    Function.Injective (scalarGNSEmbedding P) := by
  intro A B h
  exact scalarGNSLinear_injective P (congrArg Subtype.val h)

theorem scalarGNSAmbientAction_preserves (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ∀ v ∈ scalarGNSSubspace P, scalarGNSAmbientAction P B v ∈ scalarGNSSubspace P := by
  have h : Set.MapsTo (scalarGNSAmbientAction P B)
      ((scalarGNSLinear P).range : Set _) ((scalarGNSLinear P).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarGNSLeftProduct P B A, (scalarGNSAmbientAction_intertwines P B A).symm⟩
  exact h.closure (scalarGNSAmbientAction P B).continuous

def scalarGNSAction (P : SiteProfile) (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  (scalarGNSAmbientAction P B).restrict (scalarGNSAmbientAction_preserves P B)

theorem scalarGNSAction_apply (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    (scalarGNSAction P B v).val = scalarGNSAmbientAction P B v.val := rfl

theorem scalarGNSAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) : ‖scalarGNSAction P B‖ ≤ ‖B.val‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro v
  exact (scalarGNSAmbientAction P B).le_of_opNorm_le
    (scalarGNSAmbientAction_norm_le P B) v.val

theorem scalarGNSAction_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : finiteDualLeftIdeal P) :
    scalarGNSAction P B (scalarGNSEmbedding P A) =
      scalarGNSEmbedding P (scalarGNSLeftProduct P B A) := by
  apply Subtype.ext
  exact scalarGNSAmbientAction_intertwines P B A

#print axioms scalarGNSSubspace
#print axioms scalarGNSCompleteSpace
#print axioms scalarGNSEmbedding
#print axioms scalarGNSEmbedding_injective
#print axioms scalarGNSAmbientAction_preserves
#print axioms scalarGNSAction
#print axioms scalarGNSAction_apply
#print axioms scalarGNSAction_norm_le
#print axioms scalarGNSAction_intertwines
end
end TGLV350.Regular
