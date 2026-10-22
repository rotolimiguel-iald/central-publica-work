import TGLExt.V350StrongBoundedApplication
import TGLExt.V350ScalarDualWeight
import Mathlib.Algebra.Star.NonUnitalSubalgebra

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- The actual finite-square left ideal intersected with its adjoint.
No unit is asserted to have finite weight. -/
def finiteDualStarCore (P : SiteProfile) :
    NonUnitalStarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val ∧ HasFiniteDualSquare (star A.val)}
  zero_mem' := by
    constructor <;> simpa using (HasFiniteDualSquare.zero
      (H := TowerHilbert P))
  add_mem' := by
    intro A B hA hB
    change HasFiniteDualSquare (A.val+B.val) ∧ HasFiniteDualSquare (star (A.val+B.val))
    exact ⟨HasFiniteDualSquare.add _ _ hA.1 hB.1,
      by simpa only [star_add] using
        HasFiniteDualSquare.add _ _ hA.2 hB.2⟩
  mul_mem' := by
    intro A B hA hB
    change HasFiniteDualSquare (A.val*B.val) ∧ HasFiniteDualSquare (star (A.val*B.val))
    exact ⟨HasFiniteDualSquare.left_mul _ _ hB.1,
      by simpa only [star_mul] using
        HasFiniteDualSquare.left_mul (star B.val) (star A.val) hA.2⟩
  smul_mem' := by
    intro c A hA
    change HasFiniteDualSquare (c • A.val) ∧ HasFiniteDualSquare (star (c • A.val))
    exact ⟨HasFiniteDualSquare.smul c _ hA.1,
      by simpa only [star_smul] using
        HasFiniteDualSquare.smul (star c) _ hA.2⟩
  star_mem' := by
    intro A hA
    change HasFiniteDualSquare (star A.val) ∧ HasFiniteDualSquare (star (star A.val))
    exact ⟨hA.2,by simpa only [star_star] using hA.1⟩

/-- A bounded sandwich in the same N, with a finite-square factor on the
right both before and after taking the adjoint. -/
def regularSandwich (P : SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra)
    (h : ℝ) : (regularCoreAlgebra P).toStarSubalgebra :=
  ⟨star (regularAverage P h) * A.val * regularAverage P h,
    (regularCoreAlgebra P).mul_mem
      ((regularCoreAlgebra P).mul_mem
        ((regularCoreAlgebra P).toStarSubalgebra.star_mem' (regularAverage_mem P h)) A.property)
      (regularAverage_mem P h)⟩

theorem regularSandwich_star (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    star (regularSandwich P A h) = regularSandwich P (star A) h := by
  apply Subtype.ext
  change star (star (regularAverage P h) * A.val * regularAverage P h) =
    star (regularAverage P h) * star A.val * regularAverage P h
  simp only [star_mul, star_star, mul_assoc]

theorem regularSandwich_mem_finiteDualStarCore (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) (hh : 0 < h) :
    regularSandwich P A h ∈ finiteDualStarCore P := by
  have hf (B : (regularCoreAlgebra P).toStarSubalgebra) :
      HasFiniteDualSquare (regularSandwich P B h).val :=
    HasFiniteDualSquare.left_mul _ _ (regularAverage_hasFiniteDualSquare P h hh)
  refine ⟨hf A,?_⟩
  change HasFiniteDualSquare (star (regularSandwich P A h)).val
  rw [regularSandwich_star]
  exact hf (star A)

theorem regularSandwich_norm_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    ‖(regularSandwich P A h).val‖ ≤ ‖A.val‖ := by
  have hx := regularAverage_norm_le_one P h
  have hxstar : ‖star (regularAverage P h)‖ ≤ (1 : ℝ) := by
    have hn : ‖star (regularAverage P h)‖ = ‖regularAverage P h‖ :=
      _root_.norm_star (regularAverage P h)
    exact hn.le.trans hx
  change ‖star (regularAverage P h) * A.val * regularAverage P h‖ ≤ _
  calc
    _ ≤ (‖star (regularAverage P h)‖ * ‖A.val‖) * ‖regularAverage P h‖ :=
      (norm_mul_le _ _).trans (mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _))
    _ ≤ (1 * ‖A.val‖) * 1 := by
      apply mul_le_mul
      · exact mul_le_mul_of_nonneg_right hxstar (norm_nonneg _)
      · exact hx
      · exact norm_nonneg _
      · exact mul_nonneg zero_le_one (norm_nonneg _)
    _ = _ := by ring

theorem regularSandwich_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun h : ℝ => (regularSandwich P A h).val v) (𝓝[>] 0) (𝓝 (A.val v)) := by
  have ht := bounded_application_tendsto (𝓝[≠] (0 : ℝ))
    (fun h => star (regularAverage P h)) 1
    (fun h => by simpa only [_root_.norm_star] using regularAverage_norm_le_one P h)
    (fun h => A.val (regularAverage P h v)) (A.val v) (A.val v)
    (regularAverage_mul_tendsto P A.val v)
    (regularAverage_star_tendsto_identity P (A.val v))
  exact ht.mono_left (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))

/-- Every core element has uniformly bounded approximants in the algebraic
star core, converging strongly together with their adjoints. -/
theorem finiteDualStarCore_strongStar_approximation (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → regularSandwich P A h ∈ finiteDualStarCore P) ∧
    (∀ h : ℝ, ‖(regularSandwich P A h).val‖ ≤ ‖A.val‖) ∧
    (∀ v, Tendsto (fun h : ℝ => (regularSandwich P A h).val v) (𝓝[>] 0) (𝓝 (A.val v))) ∧
    (∀ v, Tendsto (fun h : ℝ => star (regularSandwich P A h).val v) (𝓝[>] 0)
      (𝓝 (star A.val v))) := by
  refine ⟨regularSandwich_mem_finiteDualStarCore P A,regularSandwich_norm_le P A,
    regularSandwich_tendsto P A,?_⟩
  intro v
  change Tendsto (fun h : ℝ => (star (regularSandwich P A h)).val v)
    (𝓝[>] 0) (𝓝 ((star A).val v))
  simp_rw [regularSandwich_star]
  exact regularSandwich_tendsto P (star A) v

theorem finiteDualStarCore_scalar_squares_finite (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (hA : A ∈ finiteDualStarCore P) :
    dualQuadraticIntegral (star A.val * A.val) (regularVacuum P) < ⊤ ∧
    dualQuadraticIntegral (A.val * star A.val) (regularVacuum P) < ⊤ :=
  ⟨HasFiniteDualSquare.scalar_finite P _ hA.1,
    by simpa only [star_star] using HasFiniteDualSquare.scalar_finite P _ hA.2⟩

#print axioms finiteDualStarCore
#print axioms regularSandwich
#print axioms regularSandwich_star
#print axioms regularSandwich_mem_finiteDualStarCore
#print axioms regularSandwich_norm_le
#print axioms regularSandwich_tendsto
#print axioms finiteDualStarCore_strongStar_approximation
#print axioms finiteDualStarCore_scalar_squares_finite
end
end TGLV350.Regular
