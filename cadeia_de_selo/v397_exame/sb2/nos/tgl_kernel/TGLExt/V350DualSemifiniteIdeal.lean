import TGLExt.V350RegularFiniteWeight
import TGLExt.V350DualFixedWeightLaws
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2400000

namespace TGLV350.Regular
open MeasureTheory Filter
open scoped ENNReal NNReal Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A single bound for all vectors: the output is a uniformly bounded
quadratic form, not just finite on a chosen vector domain. Realization by
a bounded operator in the fixed algebra is a separate obligation. -/
def HasFiniteDualSquare (A : RegularHilbert H →L[ℂ] RegularHilbert H) : Prop :=
  ∃ C : ℝ≥0, ∀ v, dualQuadraticIntegral (star A * A) v ≤
    (C : ℝ≥0∞) * ENNReal.ofReal (‖v‖ ^ 2)

theorem dualQuadraticIntegral_left_square_le
    (B A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (star (B*A) * (B*A)) v ≤
      ENNReal.ofReal (‖B‖ ^ 2) * dualQuadraticIntegral (star A * A) v := by
  have hp : ∀ s, dualQuadraticIntegrand (star (B*A) * (B*A)) v s ≤
      ENNReal.ofReal (‖B‖ ^ 2) * dualQuadraticIntegrand (star A * A) v s := by
    intro s
    rw [dualQuadraticIntegrand_star_mul, dualQuadraticIntegrand_star_mul, map_mul,
      ← ENNReal.ofReal_mul (sq_nonneg _)]
    apply ENNReal.ofReal_le_ofReal
    change ‖dualAmbient s B (dualAmbient s A v)‖ ^ 2 ≤ ‖B‖ ^ 2 * ‖dualAmbient s A v‖ ^ 2
    rw [← mul_pow]
    apply pow_le_pow_left₀ (norm_nonneg _)
    exact (ContinuousLinearMap.le_opNorm _ _).trans
      (mul_le_mul_of_nonneg_right ((dualIntegralFamily B).norm_bound s) (norm_nonneg _))
  unfold dualQuadraticIntegral
  calc
    _ ≤ ENNReal.ofReal dualHaarFactor * ∫⁻ s : ℝ,
      ENNReal.ofReal (‖B‖ ^ 2) * dualQuadraticIntegrand (star A * A) v s :=
      mul_le_mul_right (lintegral_mono hp) _
    _ = _ := by
      rw [lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ v)]
      ac_rfl

theorem HasFiniteDualSquare.zero :
    HasFiniteDualSquare (0 : RegularHilbert H →L[ℂ] RegularHilbert H) := by
  refine ⟨0, fun v => ?_⟩
  simp [dualQuadraticIntegral_zero]

theorem HasFiniteDualSquare.left_mul
    (B A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : HasFiniteDualSquare A) :
    HasFiniteDualSquare (B*A) := by
  obtain ⟨C,hC⟩ := hA
  refine ⟨‖B‖₊ ^ 2 * C, fun v => ?_⟩
  calc
    _ ≤ ENNReal.ofReal (‖B‖ ^ 2) * dualQuadraticIntegral (star A * A) v :=
      dualQuadraticIntegral_left_square_le B A v
    _ ≤ ENNReal.ofReal (‖B‖ ^ 2) * ((C : ℝ≥0∞) * ENNReal.ofReal (‖v‖ ^ 2)) :=
      mul_le_mul_right (hC v) _
    _ = _ := by simp [ENNReal.ofReal_pow, ofReal_norm, enorm_eq_nnnorm, mul_assoc]

theorem dualSquare_add_le (A B : RegularHilbert H →L[ℂ] RegularHilbert H) :
    star (A+B) * (A+B) ≤ (2 : ℝ) • (star A * A + star B * B) := by
  apply sub_nonneg.mp
  have he : (2 : ℝ) • (star A * A + star B * B) - star (A+B) * (A+B) =
      star (A-B) * (A-B) := by
    simp only [two_smul, star_add, star_sub]
    noncomm_ring
  rw [he]
  exact star_mul_self_nonneg _

theorem HasFiniteDualSquare.add
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteDualSquare A) (hB : HasFiniteDualSquare B) :
    HasFiniteDualSquare (A+B) := by
  obtain ⟨CA,hCA⟩ := hA
  obtain ⟨CB,hCB⟩ := hB
  refine ⟨2 * (CA+CB), fun v => ?_⟩
  calc
    _ ≤ dualQuadraticIntegral ((2 : ℝ) • (star A * A + star B * B)) v :=
      dualQuadraticIntegral_mono _ _ (dualSquare_add_le A B) v
    _ = 2 * (dualQuadraticIntegral (star A * A) v + dualQuadraticIntegral (star B * B) v) := by
      rw [dualQuadraticIntegral_smul_operator 2 (by norm_num),
        dualQuadraticIntegral_add _ _ (star_mul_self_nonneg A) (star_mul_self_nonneg B)]
      norm_num
    _ ≤ 2 * ((CA : ℝ≥0∞) * ENNReal.ofReal (‖v‖^2) +
      (CB : ℝ≥0∞) * ENNReal.ofReal (‖v‖^2)) := mul_le_mul_right (add_le_add (hCA v) (hCB v)) _
    _ = _ := by simp [← add_mul, mul_assoc]

theorem HasFiniteDualSquare.smul (c : ℂ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : HasFiniteDualSquare A) :
    HasFiniteDualSquare (c • A) := by
  simpa using HasFiniteDualSquare.left_mul (c • 1) A hA

/-- Linear finite-square domain inside the same regular core. -/
def finiteDualLeftIdeal (P : TGLExt.SiteProfile) :
    Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val}
  zero_mem' := HasFiniteDualSquare.zero
  add_mem' := fun hA hB => HasFiniteDualSquare.add _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteDualSquare.smul c _ hA

theorem finiteDualLeftIdeal_left_mul (P : TGLExt.SiteProfile)
    (B A : (regularCoreAlgebra P).toStarSubalgebra) (hA : A ∈ finiteDualLeftIdeal P) :
    B*A ∈ finiteDualLeftIdeal P := HasFiniteDualSquare.left_mul B.val A.val hA

theorem regularAverage_hasFiniteDualSquare (P : TGLExt.SiteProfile)
    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage P h) := by
  let C : ℝ≥0 := ⟨h⁻¹, (inv_pos.mpr hh).le⟩
  have hC : ENNReal.ofReal h⁻¹ = (C : ℝ≥0∞) := ENNReal.ofReal_coe_nnreal (p := C)
  refine ⟨C, fun v => ?_⟩
  rw [regularAverage_dualQuadraticIntegral P h hh v,
    ENNReal.ofReal_mul (inv_pos.mpr hh).le]
  rw [hC]

/-- Every core operator is approached strongly, from h>0, by elements of the
finite-square left ideal. This is the density part of semifiniteness for the
constructed fixed-algebra form-valued weight; identifying that algebra with
the original base algebra and constructing the scalar trace remain separate. -/
theorem finiteDualLeftIdeal_strong_approximation (P : TGLExt.SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → HasFiniteDualSquare (A.val * regularAverage P h)) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
  refine ⟨fun h hh => HasFiniteDualSquare.left_mul _ _
    (regularAverage_hasFiniteDualSquare P h hh),
    fun h => (regularCoreAlgebra P).toStarSubalgebra.mul_mem A.property (regularAverage_mem P h),
    fun v => (regularAverage_mul_tendsto P A.val v).mono_left ?_⟩
  exact nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh)

#print axioms HasFiniteDualSquare
#print axioms dualQuadraticIntegral_left_square_le
#print axioms HasFiniteDualSquare.zero
#print axioms HasFiniteDualSquare.left_mul
#print axioms dualSquare_add_le
#print axioms HasFiniteDualSquare.add
#print axioms HasFiniteDualSquare.smul
#print axioms finiteDualLeftIdeal
#print axioms finiteDualLeftIdeal_left_mul
#print axioms regularAverage_hasFiniteDualSquare
#print axioms finiteDualLeftIdeal_strong_approximation
end
end TGLV350.Regular
