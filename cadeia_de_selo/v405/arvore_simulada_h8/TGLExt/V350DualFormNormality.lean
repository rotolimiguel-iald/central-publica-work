import TGLExt.V350DualCutNormality
import TGLExt.V350RegularNormality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory Filter Set
open scoped ENNReal Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

variable {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]

/-- Extended integral evaluations preserve arbitrary positive monotone strong limits.
The proof passes through finite compact cuts, not a countability assumption on the net. -/
theorem dualQuadraticIntegral_of_monotone_strong_limit
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (S v)))
    (v : RegularHilbert H) :
    dualQuadraticIntegral S v = ⨆ i, dualQuadraticIntegral (A i) v := by
  have hS := ChatgptAudit.Expectation047.positive_of_strong_limit
    A S (Eventually.of_forall hpos) hlim
  have hsup := ChatgptAudit.Expectation047.monotone_strong_limit_isLUB A hmono S hlim
  apply le_antisymm
  · rw [dualQuadraticIntegral_eq_iSup_cuts S hS v]
    apply iSup_le
    intro n
    have ht : Tendsto (fun i => ENNReal.ofReal (dualHaarFactor *
        (inner ℂ v (dualWeightCut (n : ℝ) (A i) v)).re)) atTop
        (𝓝 (ENNReal.ofReal (dualHaarFactor *
          (inner ℂ v (dualWeightCut (n : ℝ) S v)).re))) :=
      ENNReal.continuous_ofReal.continuousAt.tendsto.comp
        (tendsto_const_nhds.mul (dualWeightCut_tendsto_quadratic A S hmono hlim v (n : ℝ)))
    have ht' : Tendsto (fun i => ENNReal.ofReal dualHaarFactor *
        ENNReal.ofReal (inner ℂ v (dualWeightCut (n : ℝ) (A i) v)).re) atTop
        (𝓝 (ENNReal.ofReal dualHaarFactor *
          ENNReal.ofReal (inner ℂ v (dualWeightCut (n : ℝ) S v)).re)) := by
      simpa only [ENNReal.ofReal_mul dualHaarFactor_pos.le] using ht
    apply le_of_tendsto ht'
    apply Eventually.of_forall
    intro i
    exact (dualWeightCut_quadratic_le (n : ℝ) (Nat.cast_nonneg n) (A i) (hpos i) v).trans
      (le_iSup (fun j => dualQuadraticIntegral (A j) v) i)
  · exact iSup_le fun i => dualQuadraticIntegral_mono (A i) S
      (hsup.1 (Set.mem_range_self i)) v

/-- No strong convergence hypothesis: the bounded positive operator limit is constructed
and identified with the given least upper bound. -/
theorem dualQuadraticIntegral_preserves_positive_isLUB
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S)
    (v : RegularHilbert H) :
    dualQuadraticIntegral S v = ⨆ i, dualQuadraticIntegral (A i) v := by
  have hbound : ∀ i, ‖A i‖ ≤ ‖S‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hS.1 (Set.mem_range_self i))
  obtain ⟨B, _, _, hlim, hB⟩ := ChatgptAudit.Expectation047.monotone_operator_limit
    A hpos hmono ‖S‖ (norm_nonneg S) hbound
  have hBS : B = S := hB.unique hS
  subst B
  exact dualQuadraticIntegral_of_monotone_strong_limit A S hpos hmono hlim v

/-- Order normality for an internal least upper bound of any concrete von Neumann
subalgebra of the regular representation. No ambient supremum is assumed. -/
theorem dualQuadraticIntegral_preserves_internal_isLUB
    (N : VonNeumannAlgebra (RegularHilbert H))
    (A : ι → N.toStarSubalgebra) (S : N.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S)
    (v : RegularHilbert H) :
    dualQuadraticIntegral S.val v = ⨆ i, dualQuadraticIntegral (A i).val v := by
  exact dualQuadraticIntegral_preserves_positive_isLUB
    (fun i => (A i).val) S.val hpos hmono (vonNeumann_isLUB_coe N A S hpos hmono hS) v

/-- The theorem applies to the same regular core, with the supremum internal to it.
This is normality of the family of extended forms, not yet a base-valued weight. -/
theorem regularDualForm_preserves_internal_isLUB (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral S.val v = ⨆ i, dualQuadraticIntegral (A i).val v :=
  dualQuadraticIntegral_preserves_internal_isLUB (regularCoreAlgebra P) A S hpos hmono hS v

#print axioms dualQuadraticIntegral_of_monotone_strong_limit
#print axioms dualQuadraticIntegral_preserves_positive_isLUB
#print axioms dualQuadraticIntegral_preserves_internal_isLUB
#print axioms regularDualForm_preserves_internal_isLUB
end
end TGLV350.Regular
