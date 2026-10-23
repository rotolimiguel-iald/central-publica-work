import TGLExt.V350StrongBoundedApplication
import TGLExt.V350ContractionAdjointLimit
import TGLExt.F1Fecho394.RegularCoreFiniteWeightR3
import TGLExt.V350RegularFiniteWeight
import Mathlib.Algebra.Star.NonUnitalSubalgebra
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace F1Fecho.RegularFiniteStarCore
open TGLExt TGLV350.Regular Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem regularAverage_star_tendsto_identity (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (v : RegularHilbert H) :
    Tendsto (fun h : ℝ => star (F1Fecho.RegularCoreAverage.regularAverage B h) v) (𝓝[≠] 0) (𝓝 v) :=
  contraction_adjoint_tendsto_identity _ _ (F1Fecho.RegularCoreAverage.regularAverage_norm_le_one B)
    (F1Fecho.RegularCoreAverage.regularAverage_tendsto_identity B) v

/-- The actual finite-square left ideal intersected with its adjoint.
No unit is asserted to have finite weight. -/
def finiteDualStarCore (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) :
    NonUnitalStarSubalgebra ℂ (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val ∧ HasFiniteDualSquare (star A.val)}
  zero_mem' := by
    constructor <;> simpa using (HasFiniteDualSquare.zero
      (H := H))
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
def regularSandwich (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra)
    (h : ℝ) : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra :=
  ⟨star (F1Fecho.RegularCoreAverage.regularAverage B h) * A.val * F1Fecho.RegularCoreAverage.regularAverage B h,
    (F1Fecho.RegularCovariantCore.core B M).mul_mem
      ((F1Fecho.RegularCovariantCore.core B M).mul_mem
        ((F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem B M h)) A.property)
      (F1Fecho.RegularCoreAverage.regularAverage_mem B M h)⟩

theorem regularSandwich_star (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (h : ℝ) :
    star (regularSandwich B M A h) = regularSandwich B M (star A) h := by
  apply Subtype.ext
  change star (star (F1Fecho.RegularCoreAverage.regularAverage B h) * A.val * F1Fecho.RegularCoreAverage.regularAverage B h) =
    star (F1Fecho.RegularCoreAverage.regularAverage B h) * star A.val * F1Fecho.RegularCoreAverage.regularAverage B h
  simp only [star_mul, star_star, mul_assoc]

theorem regularSandwich_mem_finiteDualStarCore (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (h : ℝ) (hh : 0 < h) :
    regularSandwich B M A h ∈ finiteDualStarCore B M := by
  have hf (X : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) :
      HasFiniteDualSquare (regularSandwich B M X h).val :=
    HasFiniteDualSquare.left_mul _ _ (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare B h hh)
  refine ⟨hf A,?_⟩
  change HasFiniteDualSquare (star (regularSandwich B M A h)).val
  rw [regularSandwich_star]
  exact hf (star A)

theorem regularSandwich_norm_le (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) (h : ℝ) :
    ‖(regularSandwich B M A h).val‖ ≤ ‖A.val‖ := by
  have hx := F1Fecho.RegularCoreAverage.regularAverage_norm_le_one B h
  have hxstar : ‖star (F1Fecho.RegularCoreAverage.regularAverage B h)‖ ≤ (1 : ℝ) := by
    have hn : ‖star (F1Fecho.RegularCoreAverage.regularAverage B h)‖ = ‖F1Fecho.RegularCoreAverage.regularAverage B h‖ :=
      _root_.norm_star (F1Fecho.RegularCoreAverage.regularAverage B h)
    exact hn.le.trans hx
  change ‖star (F1Fecho.RegularCoreAverage.regularAverage B h) * A.val * F1Fecho.RegularCoreAverage.regularAverage B h‖ ≤ _
  calc
    _ ≤ (‖star (F1Fecho.RegularCoreAverage.regularAverage B h)‖ * ‖A.val‖) * ‖F1Fecho.RegularCoreAverage.regularAverage B h‖ :=
      (norm_mul_le _ _).trans (mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _))
    _ ≤ (1 * ‖A.val‖) * 1 := by
      apply mul_le_mul
      · exact mul_le_mul_of_nonneg_right hxstar (norm_nonneg _)
      · exact hx
      · exact norm_nonneg _
      · exact mul_nonneg zero_le_one (norm_nonneg _)
    _ = _ := by ring

theorem regularSandwich_tendsto (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra)
    (v : RegularHilbert (H)) :
    Tendsto (fun h : ℝ => (regularSandwich B M A h).val v) (𝓝[>] 0) (𝓝 (A.val v)) := by
  have ht := bounded_application_tendsto (𝓝[≠] (0 : ℝ))
    (fun h => star (F1Fecho.RegularCoreAverage.regularAverage B h)) 1
    (fun h => by simpa only [_root_.norm_star] using F1Fecho.RegularCoreAverage.regularAverage_norm_le_one B h)
    (fun h => A.val (F1Fecho.RegularCoreAverage.regularAverage B h v)) (A.val v) (A.val v)
    (F1Fecho.RegularCoreAverage.regularAverage_mul_tendsto B A.val v)
    (regularAverage_star_tendsto_identity B (A.val v))
  exact ht.mono_left (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))

/-- Every core element has uniformly bounded approximants in the algebraic
star core, converging strongly together with their adjoints. -/
theorem finiteDualStarCore_strongStar_approximation (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (F1Fecho.RegularCovariantCore.core B M).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → regularSandwich B M A h ∈ finiteDualStarCore B M) ∧
    (∀ h : ℝ, ‖(regularSandwich B M A h).val‖ ≤ ‖A.val‖) ∧
    (∀ v, Tendsto (fun h : ℝ => (regularSandwich B M A h).val v) (𝓝[>] 0) (𝓝 (A.val v))) ∧
    (∀ v, Tendsto (fun h : ℝ => star (regularSandwich B M A h).val v) (𝓝[>] 0)
      (𝓝 (star A.val v))) := by
  refine ⟨regularSandwich_mem_finiteDualStarCore B M A,regularSandwich_norm_le B M A,
    regularSandwich_tendsto B M A,?_⟩
  intro v
  change Tendsto (fun h : ℝ => (star (regularSandwich B M A h)).val v)
    (𝓝[>] 0) (𝓝 ((star A).val v))
  simp_rw [regularSandwich_star]
  exact regularSandwich_tendsto B M (star A) v

#print axioms regularAverage_star_tendsto_identity
#print axioms finiteDualStarCore
#print axioms regularSandwich
#print axioms regularSandwich_star
#print axioms regularSandwich_mem_finiteDualStarCore
#print axioms regularSandwich_norm_le
#print axioms regularSandwich_tendsto
#print axioms finiteDualStarCore_strongStar_approximation
end
end F1Fecho.RegularFiniteStarCore
