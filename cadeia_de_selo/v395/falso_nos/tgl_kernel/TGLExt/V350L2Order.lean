import TGLExt.MonotoneOperatorLimit
import TGLExt.V350L2BoundedStrongContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def testVectorIsometry : H →ₗᵢ[ℂ] RegularHilbert H where
  toFun := testVector
  map_add' v w := by
    unfold testVector
    exact indicatorConstLp_add.symm
  map_smul' c v := by
    have h := fibre_testVector (c • (1 : H →L[ℂ] H)) v
    rw [fibre_smul, fibre_one] at h
    exact h.symm
  norm_map' := testVector_norm

theorem testVector_inner (v w : H) :
    inner ℂ (testVector v) (testVector w) = inner ℂ v w :=
  testVectorIsometry.inner_map_map v w

theorem fibre_nonneg {A : H →L[ℂ] H} (hA : 0 ≤ A) : 0 ≤ fibre A := by
  obtain ⟨B, rfl⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hA
  rw [fibre_mul, fibre_star]
  exact star_mul_self_nonneg _

theorem fibre_nonneg_iff (A : H →L[ℂ] H) : 0 ≤ fibre A ↔ 0 ≤ A := by
  constructor
  · intro hA
    rw [ContinuousLinearMap.nonneg_iff_isPositive, ContinuousLinearMap.isPositive_iff_complex]
    intro v
    have h := (ContinuousLinearMap.isPositive_iff_complex (fibre A)).mp
      ((ContinuousLinearMap.nonneg_iff_isPositive (fibre A)).mp hA) (testVector v)
    simpa only [fibre_testVector, testVector_inner] using h
  · exact fibre_nonneg

theorem fibre_le_iff (A B : H →L[ℂ] H) : fibre A ≤ fibre B ↔ A ≤ B := by
  have hsub : fibre (B-A) = fibre B - fibre A := map_sub fibreRepresentation B A
  rw [← sub_nonneg, ← hsub, fibre_nonneg_iff, sub_nonneg]

theorem fibre_monotone : Monotone (fibre (H := H)) :=
  fun _ _ h => (fibre_le_iff _ _).mpr h

/-- This intermediate lemma keeps strong convergence explicit; it is not yet
the theorem that every increasing bounded positive net has such a limit. -/
theorem isLUB_fibre_of_monotone_strong_limit {ι : Type*} [Preorder ι]
    [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → (H →L[ℂ] H)) (A : H →L[ℂ] H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C) (hmono : Monotone T)
    (hT : ∀ v, Tendsto (fun i => T i v) atTop (𝓝 (A v))) :
    IsLUB (Set.range (fun i => fibre (T i))) (fibre A) :=
  ChatgptAudit.Expectation047.monotone_strong_limit_isLUB _ (fibre_monotone.comp hmono) _
    (fibre_tendsto_of_uniformly_bounded T A C hbound hT)

/-- Normality in order: every positive directed supremum is preserved.
Strong convergence is constructed from positivity, monotonicity and the supremum;
it is not an extra hypothesis. -/
theorem fibre_preserves_positive_isLUB {ι : Type*} [Preorder ι]
    [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => fibre (T i))) (fibre B) := by
  have hbound : ∀ i, ‖T i‖ ≤ ‖B‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hB.1 (Set.mem_range_self i))
  obtain ⟨A, _, _, hstrong, hA⟩ :=
    ChatgptAudit.Expectation047.monotone_operator_limit T hpos hmono
      ‖B‖ (norm_nonneg B) hbound
  have hEq : A = B := hA.unique hB
  subst A
  exact isLUB_fibre_of_monotone_strong_limit T B ‖B‖ hbound hmono hstrong

#print axioms fibre_nonneg_iff
#print axioms fibre_le_iff
#print axioms isLUB_fibre_of_monotone_strong_limit
#print axioms fibre_preserves_positive_isLUB
end
end TGLV350.Regular
