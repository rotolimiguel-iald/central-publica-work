import ExpectationBlockPositive
import OperatorBlockRepresentation
import SummableLikelihoodGenerator
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt
open scoped ComplexOrder

noncomputable section

/-- Norm closure supplies the actual C-star structure on the factor subtype. -/
instance factor_subalgebra_closed (P : SiteProfile) :
    IsClosed ((theFactorObject P).toStarSubalgebra :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
  ChatgptAudit.Cocycle030.factor_norm_closed P

/-- The ambient positive square root remains in the norm-closed factor. -/
theorem factor_positive_sqrt_mem (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (hA : 0 ≤ A) :
    CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P) ∈
      (theFactorObject P).toStarSubalgebra := by
  have hAop : 0 ≤ (A : TowerHilbert P →L[ℂ] TowerHilbert P) := hA
  rw [CFC.sqrt_eq_real_sqrt _ hAop]
  exact cfcₙ_mem (𝕜' := ℂ) Real.sqrt A.property

/-- The inherited operator order is exactly the star-square order on the factor. -/
theorem factor_nonnegative_iff_star_square (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) :
    0 ≤ A ↔ ∃ B : (theFactorObject P).toStarSubalgebra, A = star B * B := by
  constructor
  · intro hA
    have hAop : 0 ≤ (A : TowerHilbert P →L[ℂ] TowerHilbert P) := hA
    let B : (theFactorObject P).toStarSubalgebra :=
      ⟨CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P),
        factor_positive_sqrt_mem P A hA⟩
    refine ⟨B, Subtype.ext ?_⟩
    change (A : TowerHilbert P →L[ℂ] TowerHilbert P) =
      star (CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P)) *
        CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    rw [(CFC.sqrt_nonneg (A : TowerHilbert P →L[ℂ] TowerHilbert P)).isSelfAdjoint.star_eq,
      CFC.sqrt_mul_sqrt_self _ hAop]
  · rintro ⟨B, rfl⟩
    change 0 ≤ star (B : TowerHilbert P →L[ℂ] TowerHilbert P) *
      (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    exact star_mul_self_nonneg _

/-- This instance keeps the subtype order inherited from bounded operators. -/
instance factor_subalgebra_star_ordered (P : SiteProfile) :
    StarOrderedRing (theFactorObject P).toStarSubalgebra :=
  StarOrderedRing.of_nonneg_iff'
    (fun {x y} h z => by
      change (z : TowerHilbert P →L[ℂ] TowerHilbert P) +
          (x : TowerHilbert P →L[ℂ] TowerHilbert P) ≤
        (z : TowerHilbert P →L[ℂ] TowerHilbert P) +
          (y : TowerHilbert P →L[ℂ] TowerHilbert P)
      have hxy : (x : TowerHilbert P →L[ℂ] TowerHilbert P) ≤
          (y : TowerHilbert P →L[ℂ] TowerHilbert P) := h
      simpa only [add_comm] using
        add_le_add_left hxy (z : TowerHilbert P →L[ℂ] TowerHilbert P))
    (factor_nonnegative_iff_star_square P)

/-- Genuine C-star matrix positivity follows from the represented block form. -/
theorem expectation_cstarMatrix_nonnegative (P : SiteProfile) (I : ExpectationInput P)
    (k : ℕ)
    (M : CStarMatrix (Fin k) (Fin k) (theFactorObject P).toStarSubalgebra)
    (hM : 0 ≤ M) :
    0 ≤ M.map (expectationLinearMap P I) := by
  have hinc :
      0 ≤ M.map (theFactorObject P).toStarSubalgebra.subtype :=
    CompletelyPositiveMapClass.map_cstarMatrix_nonneg'
      (theFactorObject P).toStarSubalgebra.subtype k M hM
  have hblock :
      BlockPositive P k
        (fun i j => (M i j : TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    (operator_block_nonneg_iff (TowerHilbert P) k _).mp hinc
  apply (operator_block_nonneg_iff (TowerHilbert P) k _).mpr
  exact general_expectation_block_positive P I k
    (fun i j => (M i j : TowerHilbert P →L[ℂ] TowerHilbert P))
    (fun i j => (M i j).property) hblock

/-- The constructed expectation, restricted to its actual algebra, as a genuine CP map. -/
def generalExpectationCompletelyPositiveMap (P : SiteProfile) (I : ExpectationInput P) :
    CompletelyPositiveMap (theFactorObject P).toStarSubalgebra
      (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toLinearMap := expectationLinearMap P I
  map_cstarMatrix_nonneg' := expectation_cstarMatrix_nonnegative P I

theorem general_expectation_cp_apply (P : SiteProfile) (I : ExpectationInput P)
    (A : (theFactorObject P).toStarSubalgebra) :
    generalExpectationCompletelyPositiveMap P I A = I.E A := rfl

theorem general_expectation_cp_toLinearMap (P : SiteProfile) (I : ExpectationInput P) :
    (generalExpectationCompletelyPositiveMap P I).toLinearMap =
      expectationLinearMap P I := rfl

#print axioms factor_subalgebra_closed
#print axioms factor_positive_sqrt_mem
#print axioms factor_nonnegative_iff_star_square
#print axioms factor_subalgebra_star_ordered
#print axioms expectation_cstarMatrix_nonnegative
#print axioms generalExpectationCompletelyPositiveMap
#print axioms general_expectation_cp_apply
#print axioms general_expectation_cp_toLinearMap

end

end ChatgptAudit.Expectation047
