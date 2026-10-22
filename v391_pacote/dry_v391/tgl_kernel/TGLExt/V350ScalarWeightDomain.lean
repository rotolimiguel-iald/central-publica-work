import TGLExt.V350ScalarDualWeight
import TGLExt.V350FiniteDualStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
open scoped ENNReal NNReal
noncomputable section

/-- Finiteness of the scalar weight, without a uniform bound on every vector. -/
def HasFiniteScalarSquare (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) : Prop :=
  dualQuadraticIntegral (star A * A) (regularVacuum P) < ⊤

theorem HasFiniteScalarSquare.zero (P : SiteProfile) :
    HasFiniteScalarSquare P 0 := by
  simp [HasFiniteScalarSquare,dualQuadraticIntegral_zero]

theorem HasFiniteScalarSquare.left_mul (P : SiteProfile)
    (B A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteScalarSquare P A) : HasFiniteScalarSquare P (B*A) :=
  (dualQuadraticIntegral_left_square_le B A (regularVacuum P)).trans_lt
    (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hA)

theorem HasFiniteScalarSquare.add (P : SiteProfile)
    (A B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteScalarSquare P A) (hB : HasFiniteScalarSquare P B) :
    HasFiniteScalarSquare P (A+B) := by
  have hb := dualQuadraticIntegral_mono _ _ (dualSquare_add_le A B) (regularVacuum P)
  rw [dualQuadraticIntegral_smul_operator 2 (by norm_num),
    dualQuadraticIntegral_add _ _ (star_mul_self_nonneg A) (star_mul_self_nonneg B)] at hb
  exact hb.trans_lt (ENNReal.mul_lt_top ENNReal.ofReal_lt_top (ENNReal.add_lt_top.mpr ⟨hA,hB⟩))

theorem HasFiniteScalarSquare.smul (P : SiteProfile) (c : ℂ)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteScalarSquare P A) : HasFiniteScalarSquare P (c • A) := by
  simpa using HasFiniteScalarSquare.left_mul P (c • 1) A hA

/-- The actual n_ν domain inside the same regular core. -/
def scalarWeightLeftIdeal (P : SiteProfile) :
    Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare P A.val}
  zero_mem' := HasFiniteScalarSquare.zero P
  add_mem' := fun hA hB => HasFiniteScalarSquare.add P _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteScalarSquare.smul P c _ hA

theorem finiteDualLeftIdeal_le_scalarWeight (P : SiteProfile) :
    finiteDualLeftIdeal P ≤ scalarWeightLeftIdeal P :=
  fun A hA => HasFiniteDualSquare.scalar_finite P A.val hA

theorem scalarWeightLeftIdeal_left_mul (P : SiteProfile)
    (B A : (regularCoreAlgebra P).toStarSubalgebra) (hA : A ∈ scalarWeightLeftIdeal P) :
    B*A ∈ scalarWeightLeftIdeal P := HasFiniteScalarSquare.left_mul P B.val A.val hA

#print axioms HasFiniteScalarSquare
#print axioms HasFiniteScalarSquare.zero
#print axioms HasFiniteScalarSquare.left_mul
#print axioms HasFiniteScalarSquare.add
#print axioms HasFiniteScalarSquare.smul
#print axioms scalarWeightLeftIdeal
#print axioms finiteDualLeftIdeal_le_scalarWeight
#print axioms scalarWeightLeftIdeal_left_mul
end
end TGLV350.Regular
