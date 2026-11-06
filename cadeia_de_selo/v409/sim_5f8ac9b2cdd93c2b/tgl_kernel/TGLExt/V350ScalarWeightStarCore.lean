import TGLExt.V350ScalarWeightSandwich
import TGLExt.V350ScalarClosedTomita

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

/-- The algebraic full scalar-weight star core, n_ν ∩ n_ν*. -/
def scalarWeightStarCore (P : SiteProfile) :
    NonUnitalStarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare P A.val ∧ HasFiniteScalarSquare P (star A.val)}
  zero_mem' := by
    constructor <;> simpa using HasFiniteScalarSquare.zero P
  add_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare P (A.val+B.val) ∧
      HasFiniteScalarSquare P (star (A.val+B.val))
    exact ⟨HasFiniteScalarSquare.add P _ _ hA.1 hB.1,
      by simpa only [star_add] using HasFiniteScalarSquare.add P _ _ hA.2 hB.2⟩
  mul_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare P (A.val*B.val) ∧
      HasFiniteScalarSquare P (star (A.val*B.val))
    exact ⟨HasFiniteScalarSquare.left_mul P _ _ hB.1,
      by simpa only [star_mul] using
        HasFiniteScalarSquare.left_mul P (star B.val) (star A.val) hA.2⟩
  smul_mem' := by
    intro c A hA
    change HasFiniteScalarSquare P (c • A.val) ∧
      HasFiniteScalarSquare P (star (c • A.val))
    exact ⟨HasFiniteScalarSquare.smul P c _ hA.1,
      by simpa only [star_smul] using HasFiniteScalarSquare.smul P (star c) _ hA.2⟩
  star_mem' := by
    intro A hA
    change HasFiniteScalarSquare P (star A.val) ∧ HasFiniteScalarSquare P (star (star A.val))
    exact ⟨hA.2,by simpa only [star_star] using hA.1⟩

def scalarWeightStarEmbedding (P : SiteProfile) (A : scalarWeightStarCore P) : ScalarGNSHilbert P :=
  scalarWeightGNSEmbedding P ⟨A.val,A.property.1⟩

def scalarUniformToWeightStar (P : SiteProfile) (A : finiteDualStarCore P) : scalarWeightStarCore P :=
  ⟨A.val,HasFiniteDualSquare.scalar_finite P _ A.property.1,
    HasFiniteDualSquare.scalar_finite P _ A.property.2⟩

theorem scalarUniformToWeightStar_star (P : SiteProfile) (A : finiteDualStarCore P) :
    scalarUniformToWeightStar P (star A) = star (scalarUniformToWeightStar P A) := rfl

theorem scalarWeightStarEmbedding_uniform (P : SiteProfile) (A : finiteDualStarCore P) :
    scalarWeightStarEmbedding P (scalarUniformToWeightStar P A) = scalarGNSStarEmbedding P A :=
  scalarWeightGNSEmbedding_uniform P ⟨A.val,A.property.1⟩

def scalarWeightTomitaGraph (P : SiteProfile) : Set (ScalarGNSHilbert P × ScalarGNSHilbert P) :=
  Set.range fun A : scalarWeightStarCore P =>
    (scalarWeightStarEmbedding P A,scalarWeightStarEmbedding P (star A))

theorem scalarTomitaGraph_subset_weight (P : SiteProfile) :
    scalarTomitaGraph P ⊆ scalarWeightTomitaGraph P := by
  rintro _ ⟨A,rfl⟩
  refine ⟨scalarUniformToWeightStar P A,?_⟩
  simp only [← scalarUniformToWeightStar_star,scalarWeightStarEmbedding_uniform]

#print axioms scalarWeightStarCore
#print axioms scalarWeightStarEmbedding
#print axioms scalarUniformToWeightStar
#print axioms scalarUniformToWeightStar_star
#print axioms scalarWeightStarEmbedding_uniform
#print axioms scalarWeightTomitaGraph
#print axioms scalarTomitaGraph_subset_weight
end
end TGLV350.Regular
