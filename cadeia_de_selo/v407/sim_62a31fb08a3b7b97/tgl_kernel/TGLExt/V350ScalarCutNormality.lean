import TGLExt.V350ScalarBoundedCuts

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem dualCutFunctional_re_tendsto {ι : Type*} [Preorder ι]
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (B : RegularHilbert H →L[ℂ] RegularHilbert H) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v)))
    (R : ℝ) (v : RegularHilbert H) :
    Tendsto (fun i => (dualCutFunctional R v (A i)).re) atTop
      (𝓝 (dualCutFunctional R v B).re) := by
  simp only [dualCutFunctional_apply,Complex.mul_re,Complex.ofReal_re,
    Complex.ofReal_im,zero_mul,sub_zero]
  exact tendsto_const_nhds.mul (dualWeightCut_tendsto_quadratic A B hmono hlim v R)

/-- Normality criterion on the original N: positive increasing nets converge
in every bounded cut reading to their internal supremum, without a supplied
strong-convergence premise. It applies to nonnegative radii in particular. -/
theorem scalarCut_tendsto_internal_isLUB (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hB : IsLUB (Set.range A) B)
    (R : ℝ) :
    Tendsto (fun i => (dualCutFunctional R (regularVacuum P) (A i).val).re) atTop
      (𝓝 (dualCutFunctional R (regularVacuum P) B.val).re) := by
  have hbound : ∀ i, ‖(A i).val‖ ≤ ‖B.val‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hB.1 (Set.mem_range_self i))
  obtain ⟨D, _, _, hlim, _, hD⟩ := vonNeumann_exists_positive_isLUB
    (regularCoreAlgebra P) A hpos hmono ‖B.val‖ (norm_nonneg _) hbound
  have hDB : D = B := hD.unique hB
  subst D
  exact dualCutFunctional_re_tendsto (fun i => (A i).val) B.val hmono hlim R (regularVacuum P)

#print axioms dualCutFunctional_re_tendsto
#print axioms scalarCut_tendsto_internal_isLUB
end
end TGLV350.Regular
