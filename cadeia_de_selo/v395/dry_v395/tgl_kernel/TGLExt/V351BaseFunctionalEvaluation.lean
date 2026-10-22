import TGLExt.V351BaseMoreauApproximants
import Mathlib.MeasureTheory.Integral.Lebesgue.Countable

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV351
open TGLExt TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal NNReal ComplexOrder
noncomputable section

/-- The sequence already constructed by Moreau, retained in the same base. -/
def baseDualApproximant (P : SiteProfile) (A : PositiveCoreInput P) (n : ℕ) :
    (theFactorObject P).toStarSubalgebra :=
  ⟨(exists_monotone_base_dual_approximation P A).choose n,
    (exists_monotone_base_dual_approximation P A).choose_spec.1 n⟩

theorem baseDualApproximant_properties (P : SiteProfile) (A : PositiveCoreInput P) :
    (∀ n, 0 ≤ baseDualApproximant P A n) ∧ Monotone (baseDualApproximant P A) ∧
      ∀ v : TowerHilbert P, (baseDualWeight P A).value v =
        ⨆ n, ENNReal.ofReal (inner ℂ v ((baseDualApproximant P A n).val v)).re := by
  have h := (exists_monotone_base_dual_approximation P A).choose_spec
  refine ⟨h.2.1,h.2.2.1,?_⟩
  intro v
  simpa only [baseDualWeight_value, baseDualApproximant, fibre_testVector, testVector_inner] using h.2.2.2 (testVector v)

/-- An evaluation on bounded functionals on M. Normality is not asserted merely
by this definition; the vector-series compatibility below identifies its domain. -/
def baseDualEvaluation (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) : ℝ≥0∞ :=
  ⨆ n, ENNReal.ofReal (ψ (baseDualApproximant P A n)).re

def baseVectorFunctional (P : SiteProfile) (v : TowerHilbert P) :
    (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ :=
  ((innerSL ℂ v).comp (ContinuousLinearMap.apply ℂ (TowerHilbert P) v)).comp
    (theFactorObject P).toStarSubalgebra.toSubalgebra.toSubmodule.subtypeL

theorem baseVectorFunctional_apply (P : SiteProfile) (v : TowerHilbert P)
    (D : (theFactorObject P).toStarSubalgebra) :
    baseVectorFunctional P v D = inner ℂ v (D.val v) := rfl

theorem baseVectorFunctional_positive (P : SiteProfile) (v : TowerHilbert P)
    (D : (theFactorObject P).toStarSubalgebra) (hD : 0 ≤ D) :
    0 ≤ baseVectorFunctional P v D :=
  ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hD).inner_nonneg_right v

theorem baseDualEvaluation_vector (P : SiteProfile) (A : PositiveCoreInput P)
    (v : TowerHilbert P) :
    baseDualEvaluation P A (baseVectorFunctional P v) = (baseDualWeight P A).value v :=
  ((baseDualApproximant_properties P A).2.2 v).symm

theorem baseDualEvaluation_vacuum (P : SiteProfile) (A : PositiveCoreInput P) :
    baseDualEvaluation P A (baseVectorFunctional P (hOmega P)) = scalarDualWeight P A := by
  rw [baseDualEvaluation_vector, ← scalarDualWeight_eq_base_evaluation]

theorem baseDualEvaluation_zero (P : SiteProfile) (A : PositiveCoreInput P) :
    baseDualEvaluation P A 0 = 0 := by simp [baseDualEvaluation]

theorem baseDualEvaluation_sequence_monotone (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ)
    (hψ : ∀ D, 0 ≤ D → 0 ≤ ψ D) :
    Monotone (fun n => ENNReal.ofReal (ψ (baseDualApproximant P A n)).re) := by
  intro n m hnm
  have hp := hψ (baseDualApproximant P A m-baseDualApproximant P A n)
    (sub_nonneg.mpr ((baseDualApproximant_properties P A).2.1 hnm))
  have hr := (Complex.nonneg_iff.mp hp).1
  rw [map_sub, Complex.sub_re] at hr
  exact ENNReal.ofReal_le_ofReal (sub_nonneg.mp hr)

theorem baseDualEvaluation_add (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ χ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ)
    (hψ : ∀ D, 0 ≤ D → 0 ≤ ψ D) (hχ : ∀ D, 0 ≤ D → 0 ≤ χ D) :
    baseDualEvaluation P A (ψ+χ) = baseDualEvaluation P A ψ + baseDualEvaluation P A χ := by
  unfold baseDualEvaluation
  rw [ENNReal.iSup_add_iSup_of_monotone (baseDualEvaluation_sequence_monotone P A ψ hψ)
    (baseDualEvaluation_sequence_monotone P A χ hχ)]
  congr 1
  funext n
  change ENNReal.ofReal ((ψ (baseDualApproximant P A n)).re +
    (χ (baseDualApproximant P A n)).re) = _
  exact ENNReal.ofReal_add
    (Complex.nonneg_iff.mp (hψ _ ((baseDualApproximant_properties P A).1 n))).1
    (Complex.nonneg_iff.mp (hχ _ ((baseDualApproximant_properties P A).1 n))).1

theorem baseDualEvaluation_scale (P : SiteProfile) (A : PositiveCoreInput P)
    (r : ℝ≥0) (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) :
    baseDualEvaluation P A ((r : ℂ) • ψ) = (r : ℝ≥0∞) * baseDualEvaluation P A ψ := by
  unfold baseDualEvaluation
  rw [ENNReal.mul_iSup]
  congr 1
  funext n
  change ENNReal.ofReal (((r : ℂ) * ψ (baseDualApproximant P A n)).re) = _
  simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  simp

theorem baseDualEvaluation_lowerSemicontinuous (P : SiteProfile) (A : PositiveCoreInput P) :
    LowerSemicontinuous (baseDualEvaluation P A) := by
  apply lowerSemicontinuous_iSup
  intro n
  exact (ENNReal.continuous_ofReal.comp (Complex.continuous_re.comp
    (ContinuousLinearMap.apply ℂ ℂ (baseDualApproximant P A n)).continuous)).lowerSemicontinuous

/-- Monotone convergence for nonnegative series; no finite total is assumed. -/
theorem ennreal_tsum_iSup_monotone (f : ℕ → ℕ → ℝ≥0∞)
    (hf : ∀ k, Monotone (fun n => f n k)) :
    (∑' k, ⨆ n, f n k) = ⨆ n, ∑' k, f n k := by
  simpa only [lintegral_count] using
    (lintegral_iSup (μ := Measure.count) (fun _ => measurable_of_countable _)
      (show Monotone f from fun n m hnm k => hf k hnm))

/-- This hypothesis is an explicit vector-series representation on positive
elements of M. It is not silently supplied for arbitrary functionals. -/
theorem baseDualEvaluation_eq_vector_series (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D →
      ENNReal.ofReal (ψ D).re = ∑' k, ENNReal.ofReal (inner ℂ (v k) (D.val (v k))).re) :
    baseDualEvaluation P A ψ = ∑' k, (baseDualWeight P A).value (v k) := by
  unfold baseDualEvaluation
  simp_rw [hrep _ ((baseDualApproximant_properties P A).1 _)]
  rw [← ennreal_tsum_iSup_monotone]
  · congr 1
    funext k
    exact ((baseDualApproximant_properties P A).2.2 (v k)).symm
  · intro k
    exact baseDualEvaluation_sequence_monotone P A (baseVectorFunctional P (v k))
      (baseVectorFunctional_positive P (v k))

theorem baseDualEvaluation_series_independent (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v w : ℕ → TowerHilbert P)
    (hv : ∀ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D →
      ENNReal.ofReal (ψ D).re = ∑' k, ENNReal.ofReal (inner ℂ (v k) (D.val (v k))).re)
    (hw : ∀ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D →
      ENNReal.ofReal (ψ D).re = ∑' k, ENNReal.ofReal (inner ℂ (w k) (D.val (w k))).re) :
    (∑' k, (baseDualWeight P A).value (v k)) = ∑' k, (baseDualWeight P A).value (w k) :=
  (baseDualEvaluation_eq_vector_series P A ψ v hv).symm.trans
    (baseDualEvaluation_eq_vector_series P A ψ w hw)

/-- A genuine convergent complex vector-series representation supplies the
extended positive representation used above; no convention for divergent tsum. -/
theorem baseFunctional_hasSum_positive_evaluation (P : SiteProfile)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D))
    (D : (theFactorObject P).toStarSubalgebra) (hD : 0 ≤ D) :
    ENNReal.ofReal (ψ D).re = ∑' k, ENNReal.ofReal (inner ℂ (v k) (D.val (v k))).re := by
  have hr := Complex.reCLM.hasSum (hrep D)
  change HasSum (fun k => (inner ℂ (v k) (D.val (v k))).re) (ψ D).re at hr
  rw [← hr.tsum_eq]
  exact ENNReal.ofReal_tsum_of_nonneg
    (fun k => ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hD).re_inner_nonneg_right (v k))
    hr.summable

theorem baseDualEvaluation_eq_hasSum_series (P : SiteProfile) (A : PositiveCoreInput P)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) :
    baseDualEvaluation P A ψ = ∑' k, (baseDualWeight P A).value (v k) :=
  baseDualEvaluation_eq_vector_series P A ψ v (baseFunctional_hasSum_positive_evaluation P ψ v hrep)

/-- The series has finite total square norm, derived by evaluating the unit. -/
theorem baseFunctional_hasSum_square_norm (P : SiteProfile)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) :
    HasSum (fun k => ‖v k‖^2) (ψ 1).re := by
  have hr := Complex.reCLM.hasSum (hrep 1)
  have hs : ∀ k, (inner ℂ (v k) (v k)).re = ‖v k‖^2 :=
    fun k => inner_self_eq_norm_sq (𝕜 := ℂ) (v k)
  change HasSum (fun k => (inner ℂ (v k) (v k)).re) (ψ 1).re at hr
  simpa only [hs] using hr

theorem baseVectorFunctional_norm_le (P : SiteProfile) (v : TowerHilbert P) :
    ‖baseVectorFunctional P v‖ ≤ ‖v‖^2 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (sq_nonneg _)
  intro D
  change ‖inner ℂ v (D.val v)‖ ≤ ‖v‖^2 * ‖D‖
  calc
    _ ≤ ‖v‖ * ‖D.val v‖ := norm_inner_le_norm _ _
    _ ≤ ‖v‖ * (‖D.val‖ * ‖v‖) :=
      mul_le_mul_of_nonneg_left (D.val.le_opNorm v) (norm_nonneg v)
    _ = ‖v‖^2 * ‖D‖ := by change ‖v‖ * (‖D‖ * ‖v‖) = _; ring

/-- A square-summable vector family really constructs a bounded positive
functional on the original base; the representation is not an extra input. -/
theorem exists_base_series_functional (P : SiteProfile) (v : ℕ → TowerHilbert P)
    (hv : Summable (fun k => ‖v k‖^2)) :
    ∃ ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ,
      (∀ D : (theFactorObject P).toStarSubalgebra,
        HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) ∧
      (∀ D, 0 ≤ D → 0 ≤ ψ D) ∧
      ∀ A : PositiveCoreInput P,
        baseDualEvaluation P A ψ = ∑' k, (baseDualWeight P A).value (v k) := by
  have hh : Summable (fun k => baseVectorFunctional P (v k)) :=
    Summable.of_norm_bounded hv (fun k => baseVectorFunctional_norm_le P (v k))
  let ψ := ∑' k, baseVectorFunctional P (v k)
  have hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D) := by
    intro D
    exact (ContinuousLinearMap.apply ℂ ℂ D).hasSum hh.hasSum
  refine ⟨ψ,hrep,?_,fun A => baseDualEvaluation_eq_hasSum_series P A ψ v hrep⟩
  intro D hD
  have hp : 0 ≤ ∑' k, inner ℂ (v k) (D.val (v k)) :=
    tsum_nonneg (fun k => baseVectorFunctional_positive P (v k) D hD)
  rwa [(hrep D).tsum_eq] at hp

#print axioms baseDualApproximant
#print axioms baseDualApproximant_properties
#print axioms baseDualEvaluation
#print axioms baseVectorFunctional
#print axioms baseVectorFunctional_apply
#print axioms baseVectorFunctional_positive
#print axioms baseDualEvaluation_vector
#print axioms baseDualEvaluation_vacuum
#print axioms baseDualEvaluation_zero
#print axioms baseDualEvaluation_sequence_monotone
#print axioms baseDualEvaluation_add
#print axioms baseDualEvaluation_scale
#print axioms baseDualEvaluation_lowerSemicontinuous
#print axioms ennreal_tsum_iSup_monotone
#print axioms baseDualEvaluation_eq_vector_series
#print axioms baseDualEvaluation_series_independent
#print axioms baseFunctional_hasSum_positive_evaluation
#print axioms baseDualEvaluation_eq_hasSum_series
#print axioms baseFunctional_hasSum_square_norm
#print axioms baseVectorFunctional_norm_le
#print axioms exists_base_series_functional
end
end TGLV351
