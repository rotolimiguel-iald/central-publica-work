import TGLExt.V350FixedCoreBaseIdentification
import TGLExt.V350L2Order

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 600000

namespace TGLV350.Regular
open TGLExt
noncomputable section

def fixedBaseEmbedding (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra →⋆ₐ[ℂ] (dualFixedCore P).toStarSubalgebra :=
  (factorAmplification P).codRestrict (dualFixedCore P).toStarSubalgebra
    (fun A => amplified_factor_mem_dualFixedCore P A A.property)

theorem fixedBaseEmbedding_bijective (P : SiteProfile) :
    Function.Bijective (fixedBaseEmbedding P) := by
  constructor
  · intro A B h
    apply Subtype.ext
    apply fibre_injective
    exact congrArg Subtype.val h
  · intro B
    obtain ⟨C,hC,he⟩ := (dualFixedCore_eq_amplified_base P B.val).mp B.property
    exact ⟨⟨C,hC⟩,Subtype.ext he.symm⟩

/-- A concrete algebra equivalence, not merely existence of an isomorphism. -/
def fixedBaseEquiv (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃⋆ₐ[ℂ] (dualFixedCore P).toStarSubalgebra :=
  StarAlgEquiv.ofBijective (fixedBaseEmbedding P) (fixedBaseEmbedding_bijective P)

theorem fixedBaseEquiv_apply (P : SiteProfile) (A : (theFactorObject P).toStarSubalgebra) :
    (fixedBaseEquiv P A).val = fibre A.val := rfl

theorem fixedBaseEquiv_symm_apply (P : SiteProfile) (B : (dualFixedCore P).toStarSubalgebra) :
    ((fixedBaseEquiv P).symm B).val = fibreCandidate B.val := by
  apply fibre_injective
  have he := congrArg Subtype.val ((fixedBaseEquiv P).apply_symm_apply B)
  rw [fixedBaseEquiv_apply] at he
  exact he.trans (dualFixedCore_eq_fibre_candidate P B.val B.property)

/-- The same map preserves and reflects the inherited positive order. -/
def fixedBaseOrderIso (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃o (dualFixedCore P).toStarSubalgebra where
  toEquiv := (fixedBaseEquiv P).toEquiv
  map_rel_iff' := by
    intro A B
    change fibre A.val ≤ fibre B.val ↔ A.val ≤ B.val
    exact fibre_le_iff A.val B.val

#print axioms fixedBaseEmbedding_bijective
#print axioms fixedBaseEquiv
#print axioms fixedBaseEquiv_apply
#print axioms fixedBaseEquiv_symm_apply
#print axioms fixedBaseOrderIso
end
end TGLV350.Regular
