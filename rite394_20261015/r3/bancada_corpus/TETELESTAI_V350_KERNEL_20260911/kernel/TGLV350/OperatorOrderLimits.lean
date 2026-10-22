/-!
RETIRED PROTOTYPE — NOT COMPILED, NOT INTEGRATED, NOT PROOF EVIDENCE.
The failed attempts are retained under logs/. TGLExt.MonotoneOperatorLimit
already supplies the needed results; L2Order imports that verified module.
This prototype is intentionally absent from the embedded monolith and Audit.
-/
import Mathlib

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.OperatorOrder
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def quadratic (A : H →L[ℂ] H) (v : H) : ℝ := (inner ℂ (A v) v).re

theorem quadratic_mono {A B : H →L[ℂ] H} (h : A ≤ B) (v : H) :
    quadratic A v ≤ quadratic B v := by
  have hv := (ContinuousLinearMap.le_def A B).mp h |>.re_inner_nonneg_left v
  change 0 ≤ (inner ℂ ((B-A) v) v).re at hv
  simpa only [sub_apply, inner_sub_left, Complex.sub_re, sub_nonneg, quadratic] using hv

/-- Positive quadratic energy controls the norm of an operator applied to a vector. -/
theorem positive_norm_sq_le {A : H →L[ℂ] H} (hA : 0 ≤ A) (v : H) :
    ‖A v‖ ^ 2 ≤ ‖A‖ * quadratic A v := by
  let B := CFC.sqrt A
  have hB : B.IsPositive := (ContinuousLinearMap.nonneg_iff_isPositive B).mp (CFC.sqrt_nonneg A)
  have hBB : B * B = A := CFC.sqrt_mul_sqrt_self A hA
  have hq : quadratic A v = ‖B v‖ ^ 2 := by
    unfold quadratic
    rw [← hBB, mul_apply_eq_comp, hB.inner_left_eq_inner_right]
    exact real_inner_self_eq_norm_sq (𝕜 := ℂ) (B v)
  have hn : ‖A v‖ ≤ ‖B‖ * ‖B v‖ := by
    rw [← hBB, mul_apply_eq_comp]
    exact B.le_opNorm (B v)
  calc
    ‖A v‖ ^ 2 ≤ (‖B‖ * ‖B v‖) ^ 2 :=
      (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr hn
    _ = ‖A‖ * quadratic A v := by
      rw [mul_pow, show ‖B‖ = Real.sqrt ‖A‖ from CFC.norm_sqrt A hA,
        Real.sq_sqrt (norm_nonneg A), hq]

/-- Positivity is closed under strong limits along a nontrivial filter. -/
theorem nonneg_of_strong_limit {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → (H →L[ℂ] H)) (A : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (A v)))
    (hpos : ∀ᶠ i in l, 0 ≤ T i) : 0 ≤ A := by
  rw [ContinuousLinearMap.nonneg_iff_isPositive, ContinuousLinearMap.isPositive_def]
  constructor
  · intro x y
    have hleft : Tendsto (fun i => inner ℂ (T i x) y) l (𝓝 (inner ℂ (A x) y)) :=
      (hT x).inner (tendsto_const_nhds (x := y))
    have hright : Tendsto (fun i => inner ℂ x (T i y)) l (𝓝 (inner ℂ x (A y))) :=
      (tendsto_const_nhds (x := x)).inner (hT y)
    have heq : (fun i => inner ℂ (T i x) y) =ᶠ[l] (fun i => inner ℂ x (T i y)) := by
      filter_upwards [hpos] with i hi
      exact ((ContinuousLinearMap.nonneg_iff_isPositive (T i)).mp hi).inner_left_eq_inner_right x y
    exact tendsto_nhds_unique hleft (hright.congr' heq.symm)
  · intro v
    change 0 ≤ (inner ℂ (A v) v).re
    have hq : Tendsto (fun i => (inner ℂ (T i v) v).re) l (𝓝 (inner ℂ (A v) v).re) :=
      Complex.continuous_re.continuousAt.tendsto.comp
        ((hT v).inner (tendsto_const_nhds (x := v)))
    exact ge_of_tendsto hq (hpos.mono fun i hi =>
      ((ContinuousLinearMap.nonneg_iff_isPositive (T i)).mp hi).re_inner_nonneg_left v)

theorem le_strong_limit {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → (H →L[ℂ] H)) (A B : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (A v)))
    (hle : ∀ᶠ i in l, B ≤ T i) : B ≤ A := by
  rw [← sub_nonneg]
  exact nonneg_of_strong_limit (fun i => T i - B) (A-B)
    (fun v => (hT v).sub tendsto_const_nhds) (hle.mono fun _ h => sub_nonneg.mpr h)

theorem strong_limit_le {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → (H →L[ℂ] H)) (A B : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (A v)))
    (hle : ∀ᶠ i in l, T i ≤ B) : A ≤ B := by
  rw [← sub_nonneg]
  exact nonneg_of_strong_limit (fun i => B - T i) (B-A)
    (fun v => tendsto_const_nhds.sub (hT v)) (hle.mono fun _ h => sub_nonneg.mpr h)

/-- A strong limit of an increasing net is its least upper bound in Loewner order. -/
theorem isLUB_of_monotone_strong_limit {ι : Type*} [Preorder ι]
    [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → (H →L[ℂ] H)) (A : H →L[ℂ] H) (hmono : Monotone T)
    (hT : ∀ v, Tendsto (fun i => T i v) atTop (𝓝 (A v))) :
    IsLUB (Set.range T) A := by
  constructor
  · rintro _ ⟨i, rfl⟩
    exact le_strong_limit T A (T i) hT ((eventually_ge_atTop i).mono fun _ hij => hmono hij)
  · intro B hB
    exact strong_limit_le T A B hT (Eventually.of_forall fun i => hB ⟨i, rfl⟩)

#print axioms positive_norm_sq_le
#print axioms nonneg_of_strong_limit
#print axioms isLUB_of_monotone_strong_limit
end
end TGLV350.OperatorOrder
