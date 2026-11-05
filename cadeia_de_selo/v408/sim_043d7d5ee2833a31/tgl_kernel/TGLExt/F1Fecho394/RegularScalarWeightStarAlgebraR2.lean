import TGLExt.F1Fecho394.RegularScalarWeightDomainR1
/-! The full finite-weight star algebra on an arbitrary regular scalar-weight context.
The concrete Fock context is applied by the separate consumer. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarWeightStarAlgebra
open TGLV350.Regular F1Fecho.RegularScalarGNS F1Fecho.RegularScalarWeightDomain
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)
/-- The algebraic full scalar-weight star core, n_ν ∩ n_ν*. -/
def scalarWeightStarCore  :
    NonUnitalStarSubalgebra ℂ D.algebra.toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare D A.val ∧ HasFiniteScalarSquare D (star A.val)}
  zero_mem' := by
    change HasFiniteScalarSquare D (0 : RegularHilbert H →L[ℂ] RegularHilbert H) ∧ HasFiniteScalarSquare D (star (0 : RegularHilbert H →L[ℂ] RegularHilbert H))
    exact ⟨HasFiniteScalarSquare.zero D, by simpa only [star_zero] using HasFiniteScalarSquare.zero D⟩
  add_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare D (A.val+B.val) ∧
      HasFiniteScalarSquare D (star (A.val+B.val))
    exact ⟨HasFiniteScalarSquare.add D _ _ hA.1 hB.1,
      by simpa only [star_add] using HasFiniteScalarSquare.add D _ _ hA.2 hB.2⟩
  mul_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare D (A.val*B.val) ∧
      HasFiniteScalarSquare D (star (A.val*B.val))
    exact ⟨HasFiniteScalarSquare.left_mul D _ _ hB.1,
      by simpa only [star_mul] using
        HasFiniteScalarSquare.left_mul D (star B.val) (star A.val) hA.2⟩
  smul_mem' := by
    intro c A hA
    change HasFiniteScalarSquare D (c • A.val) ∧
      HasFiniteScalarSquare D (star (c • A.val))
    exact ⟨HasFiniteScalarSquare.smul D c _ hA.1,
      by simpa only [star_smul] using HasFiniteScalarSquare.smul D (star c) _ hA.2⟩
  star_mem' := by
    intro A hA
    change HasFiniteScalarSquare D (star A.val) ∧ HasFiniteScalarSquare D (star (star A.val))
    exact ⟨hA.2,by simpa only [star_star] using hA.1⟩


end F1Fecho.RegularScalarWeightStarAlgebra
#print axioms F1Fecho.RegularScalarWeightStarAlgebra.scalarWeightStarCore
