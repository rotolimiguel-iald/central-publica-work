import TGLExt.V351BaseFunctionalEvaluation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV351
open TGLExt TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal NNReal ComplexOrder
noncomputable section

/-- The net index is arbitrary, not silently replaced by a sequence. -/
theorem ennreal_tsum_iSup_directed {ι : Type*}
    [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (f : ι → ℕ → ℝ≥0∞) (hf : ∀ k, Monotone (fun i => f i k)) :
    (∑' k, ⨆ i, f i k) = ⨆ i, ∑' k, f i k := by
  have hfin : ∀ n : ℕ,
      (∑ k ∈ Finset.range n, ⨆ i, f i k) = ⨆ i, ∑ k ∈ Finset.range n, f i k := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      simp only [Finset.sum_range_succ, ih]
      exact ENNReal.iSup_add_iSup_of_monotone
        (fun i j hij => Finset.sum_le_sum (fun k _ => hf k hij)) (hf n)
  simp_rw [ENNReal.tsum_eq_iSup_nat, hfin]
  exact iSup_comm

variable (P : SiteProfile)
variable (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ)
variable (v : ℕ → TowerHilbert P)
variable (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
  HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D))
include hrep

theorem baseDualEvaluation_input_zero :
    baseDualEvaluation P (PositiveCoreInput.zero P) ψ = 0 := by
  rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep, baseDualWeight_zero]
  simp [AffiliatedPositiveForm.zeroForm, ClosedPositiveForm.zeroForm]

theorem baseDualEvaluation_input_add (A B : PositiveCoreInput P) :
    baseDualEvaluation P (A.add B) ψ =
      baseDualEvaluation P A ψ + baseDualEvaluation P B ψ := by
  simp_rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep]
  rw [baseDualWeight_add]
  exact ENNReal.tsum_add

theorem baseDualEvaluation_input_scale (r : ℝ≥0) (A : PositiveCoreInput P) :
    baseDualEvaluation P (A.scale r) ψ = (r : ℝ≥0∞) * baseDualEvaluation P A ψ := by
  simp_rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep]
  rw [baseDualWeight_scale]
  exact ENNReal.tsum_mul_left

theorem baseDualEvaluation_input_mono (A B : PositiveCoreInput P) (hAB : A ≤ B) :
    baseDualEvaluation P A ψ ≤ baseDualEvaluation P B ψ := by
  simp_rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep]
  exact ENNReal.tsum_le_tsum (fun k => baseDualWeight_mono P A B hAB (v k))

/-- Supremum preservation in the core input for every represented functional.
The internal supremum is the only limit hypothesis. -/
theorem baseDualEvaluation_input_normal {ι : Type*}
    [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    baseDualEvaluation P
        ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩ ψ =
      ⨆ i, baseDualEvaluation P ⟨(A i).val, (A i).property, hpos i⟩ ψ := by
  simp_rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep, baseDualWeight_value]
  simp_rw [regularDualForm_preserves_internal_isLUB P A S hpos hmono hS]
  exact ennreal_tsum_iSup_directed _
    (fun k i j hij => dualQuadraticIntegral_mono (A i).val (A j).val (hmono hij)
      (testVector (v k)))

/-- This is the same dual action and Haar constant. Only the averaged value
descends from a vector-series representation, including infinite outputs. -/
theorem baseDualEvaluation_eq_dual_integral (A : PositiveCoreInput P) :
    baseDualEvaluation P A ψ = ENNReal.ofReal dualHaarFactor *
      ∫⁻ s : ℝ, ∑' k, dualQuadraticIntegrand A.val (testVector (v k)) s := by
  rw [baseDualEvaluation_eq_hasSum_series P A ψ v hrep]
  simp only [baseDualWeight_value, dualQuadraticIntegral]
  rw [lintegral_tsum (fun k =>
    (dualQuadraticIntegrand_measurable A.val (testVector (v k))).aemeasurable)]
  exact ENNReal.tsum_mul_left

/-- A bounded output is read as evaluation of that very base operator. -/
theorem baseDualEvaluation_bounded_output (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra) (hD : 0 ≤ D)
    (hbounded : ∀ w, dualQuadraticIntegral A.val w =
      ENNReal.ofReal (inner ℂ w (fibre D.val w)).re) :
    baseDualEvaluation P A ψ = ENNReal.ofReal (ψ D).re := by
  rw [baseDualEvaluation_eq_hasSum_series P A ψ v hrep]
  simp_rw [baseDualWeight_bounded_value P A D hbounded]
  exact (baseFunctional_hasSum_positive_evaluation P ψ v hrep D hD).symm

/-- Bimodularity is inherited from the same fixed-base equivalence. The
second functional is explicitly represented by the transported vectors. -/
theorem baseDualEvaluation_bimodule (A : PositiveCoreInput P)
    (B : (theFactorObject P).toStarSubalgebra)
    (χ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ)
    (hχ : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (B.val (v k)) (D.val (B.val (v k)))) (χ D)) :
    baseDualEvaluation P (A.conjugate (fixedBaseEquiv P B)) ψ =
      baseDualEvaluation P A χ := by
  rw [baseDualEvaluation_eq_hasSum_series P _ ψ v hrep,
    baseDualEvaluation_eq_hasSum_series P _ χ (fun k => B.val (v k)) hχ,
    baseDualWeight_bimodule]
  rfl

omit hrep

/-- The zero test concerns the whole family of evaluations, not faithfulness
of each arbitrary positive functional. The vacuum alone already witnesses it. -/
theorem baseDualEvaluation_family_faithful (A : PositiveCoreInput P) :
    (∀ w : TowerHilbert P, baseDualEvaluation P A (baseVectorFunctional P w) = 0) ↔
      A = PositiveCoreInput.zero P := by
  constructor
  · intro hz
    apply (scalarDualWeight_faithful P A).mp
    rw [← baseDualEvaluation_vacuum]
    exact hz (hOmega P)
  · rintro rfl w
    rw [baseDualEvaluation_vector, baseDualWeight_zero]
    rfl

/-- The same finite and infinite controls continue to be actual outputs. -/
theorem baseDualEvaluation_averageSquare :
    baseDualEvaluation P (positiveAverageSquare P) (baseVectorFunctional P (hOmega P)) = 1 := by
  rw [baseDualEvaluation_vacuum, scalarDualWeight_averageSquare]

theorem baseDualEvaluation_unit_infinite (w : TowerHilbert P) (hw : w ≠ 0) :
    baseDualEvaluation P (positiveUnit P) (baseVectorFunctional P w) = ⊤ := by
  rw [baseDualEvaluation_vector, baseDualWeight_unit_infinite P w hw]

#print axioms ennreal_tsum_iSup_directed
#print axioms baseDualEvaluation_input_zero
#print axioms baseDualEvaluation_input_add
#print axioms baseDualEvaluation_input_scale
#print axioms baseDualEvaluation_input_mono
#print axioms baseDualEvaluation_input_normal
#print axioms baseDualEvaluation_eq_dual_integral
#print axioms baseDualEvaluation_bounded_output
#print axioms baseDualEvaluation_bimodule
#print axioms baseDualEvaluation_family_faithful
#print axioms baseDualEvaluation_averageSquare
#print axioms baseDualEvaluation_unit_infinite
end
end TGLV351
