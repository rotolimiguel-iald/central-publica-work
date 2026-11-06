import TGLExt.F1Fecho394.RegularScalarGNSR3
import TGLExt.V350FiniteDualStarCore

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarWeightDomain
open TGLV350.Regular F1Fecho.RegularScalarGNS
open scoped ENNReal NNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)

/-- Finiteness of the scalar weight, without a uniform bound on every vector. -/
def HasFiniteScalarSquare 
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) : Prop :=
  dualQuadraticIntegral (star A * A) D.vacuum < ⊤

theorem HasFiniteScalarSquare.zero  :
    HasFiniteScalarSquare D 0 := by
  simp [HasFiniteScalarSquare,dualQuadraticIntegral_zero]

theorem HasFiniteScalarSquare.left_mul 
    (B A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteScalarSquare D A) : HasFiniteScalarSquare D (B*A) :=
  (dualQuadraticIntegral_left_square_le B A D.vacuum).trans_lt
    (ENNReal.mul_lt_top ENNReal.ofReal_lt_top hA)

theorem HasFiniteScalarSquare.add 
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteScalarSquare D A) (hB : HasFiniteScalarSquare D B) :
    HasFiniteScalarSquare D (A+B) := by
  have hb := dualQuadraticIntegral_mono _ _ (dualSquare_add_le A B) D.vacuum
  rw [dualQuadraticIntegral_smul_operator 2 (by norm_num),
    dualQuadraticIntegral_add _ _ (star_mul_self_nonneg A) (star_mul_self_nonneg B)] at hb
  exact hb.trans_lt (ENNReal.mul_lt_top ENNReal.ofReal_lt_top (ENNReal.add_lt_top.mpr ⟨hA,hB⟩))

theorem HasFiniteScalarSquare.smul  (c : ℂ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteScalarSquare D A) : HasFiniteScalarSquare D (c • A) := by
  simpa using HasFiniteScalarSquare.left_mul D (c • 1) A hA

/-- The actual n_ν domain inside the same regular core. -/
def scalarWeightLeftIdeal  :
    Submodule ℂ D.algebra.toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare D A.val}
  zero_mem' := HasFiniteScalarSquare.zero D 
  add_mem' := fun hA hB => HasFiniteScalarSquare.add D _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteScalarSquare.smul D c _ hA

theorem finiteDualLeftIdeal_le_scalarWeight  :
    finiteIdeal D ≤ scalarWeightLeftIdeal D :=
  fun A hA => scalar_finite D A.val hA

theorem scalarWeightLeftIdeal_left_mul 
    (B A : D.algebra.toStarSubalgebra) (hA : A ∈ scalarWeightLeftIdeal D ) :
    B*A ∈ scalarWeightLeftIdeal D := HasFiniteScalarSquare.left_mul D B.val A.val hA

end
end F1Fecho.RegularScalarWeightDomain
#print axioms F1Fecho.RegularScalarWeightDomain.HasFiniteScalarSquare.zero
#print axioms F1Fecho.RegularScalarWeightDomain.HasFiniteScalarSquare.left_mul
#print axioms F1Fecho.RegularScalarWeightDomain.HasFiniteScalarSquare.add
#print axioms F1Fecho.RegularScalarWeightDomain.HasFiniteScalarSquare.smul
#print axioms F1Fecho.RegularScalarWeightDomain.finiteDualLeftIdeal_le_scalarWeight
#print axioms F1Fecho.RegularScalarWeightDomain.scalarWeightLeftIdeal_left_mul
#print axioms F1Fecho.RegularScalarWeightDomain.scalarWeightLeftIdeal
#print axioms F1Fecho.RegularScalarWeightDomain.HasFiniteScalarSquare
