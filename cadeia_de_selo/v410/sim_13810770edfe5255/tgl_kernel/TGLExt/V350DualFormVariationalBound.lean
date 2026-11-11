import TGLExt.V350DualSquareRoot
import Mathlib.Algebra.QuadraticDiscriminant
import Mathlib.Analysis.Normed.Operator.Extend

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter ChatgptAudit.Continuous049
open scoped Topology ENNReal ComplexConjugate
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The complex phase is tested as well as the real scaling; a bound on the
real part alone is not silently substituted for the modulus. -/
theorem inner_norm_bound_of_variational_bound (B : H →L[ℂ] H) (w : H)
    (c : ℝ) (hc : 0 ≤ c)
    (h : ∀ v : H, 2*(inner ℂ w v).re ≤ ‖B v‖^2 + c) (v : H) :
    ‖inner ℂ w v‖ ≤ Real.sqrt c * ‖B v‖ := by
  have hreal (u : H) : (inner ℂ w u).re^2 ≤ c*‖B u‖^2 := by
    have hp : ∀ t : ℝ, 0 ≤ ‖B u‖^2*(t*t) + (-2*(inner ℂ w u).re)*t+c := by
      intro t
      have ht := h ((t : ℂ) • u)
      simp only [map_smul, norm_smul, mul_pow, Complex.norm_real,
        Real.norm_eq_abs, sq_abs, inner_smul_right, Complex.mul_re,
        Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero] at ht
      nlinarith only [ht]
    have hd := discrim_le_zero hp
    unfold discrim at hd
    nlinarith only [hd]
  let z := inner ℂ w v
  have hphase : (inner ℂ w (star z • v)).re = ‖z‖^2 := by
    simp only [inner_smul_right, Complex.mul_re, Complex.star_def,
      Complex.conj_re, Complex.conj_im, Complex.sq_norm, Complex.normSq_apply]
    dsimp [z]
    ring
  have hp := hreal (star z • v)
  rw [hphase] at hp
  simp only [map_smul, norm_smul, norm_star, mul_pow] at hp
  have hs : ‖z‖^2 ≤ c * ‖B v‖^2 := by
    by_cases hz : ‖z‖ = 0
    · rw [hz, zero_pow (by omega : 2 ≠ 0)]
      exact mul_nonneg hc (sq_nonneg _)
    · have hm : ‖z‖^2 * ‖z‖^2 ≤ ‖z‖^2 * (c * ‖B v‖^2) := by
        nlinarith only [hp]
      exact le_of_mul_le_mul_left hm (sq_pos_of_ne_zero hz)
  have ht : (Real.sqrt c * ‖B v‖)^2 = c * ‖B v‖^2 := by
    rw [mul_pow, Real.sq_sqrt hc]
  have hn := mul_nonneg (Real.sqrt_nonneg c) (norm_nonneg (B v))
  change ‖z‖ ≤ _
  nlinarith only [hs, ht, hn, norm_nonneg z]

/-- Construct the preimage via a bounded extension and Riesz. The dense range,
self-adjointness, and optimal bound are explicit inputs. -/
theorem exists_preimage_of_inner_bound (B : H →L[ℂ] H) (hB : IsSelfAdjoint B)
    (hd : DenseRange B) (w : H) (c : ℝ) (hc : 0 ≤ c)
    (hb : ∀ v : H, ‖inner ℂ w v‖ ≤ c * ‖B v‖) :
    ∃ z : H, B z = w ∧ ‖z‖ ≤ c := by
  let f : H →ₗ[ℂ] ℂ := (innerSL ℂ w).toLinearMap
  let F : H →L[ℂ] ℂ := f.extendOfNorm B.toLinearMap
  let z : H := (InnerProductSpace.toDual ℂ H).symm F
  have he (v : H) : F (B v) = inner ℂ w v :=
    LinearMap.extendOfNorm_eq hd ⟨c,hb⟩ v
  refine ⟨z,?_,?_⟩
  · apply ext_inner_right ℂ
    intro v
    rw [bounded_graph_selfadjoint_inner B hB]
    exact (InnerProductSpace.toDual_symm_apply).trans (he v)
  · change ‖(InnerProductSpace.toDual ℂ H).symm F‖ ≤ c
    rw [(InnerProductSpace.toDual ℂ H).symm.norm_map]
    exact LinearMap.opNorm_extendOfNorm_le hd hc hb

/-- A finite-energy vector bounds the dual quadratic expression. Both
energies are proved finite before applying ENNReal.toReal. -/
theorem dualResolvent_variational_dual_bound
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (w : RegularHilbert H) (hw : dualQuadraticIntegral A w < ⊤)
    (v : RegularHilbert H) :
    2*(inner ℂ w v).re ≤ (inner ℂ (R v) v).re +
      ‖w‖^2 + (dualQuadraticIntegral A w).toReal := by
  have hr : dualQuadraticIntegral A (R v) ≠ ⊤ :=
    ne_of_lt (dualResolvent_limit_range_finite A R hA hlim v)
  have hm := dualResolvent_limit_minimizes_energy A R hA hlim v w
  have ht := ENNReal.toReal_mono
    (ENNReal.add_ne_top.mpr ⟨ENNReal.ofReal_ne_top, ne_of_lt hw⟩) hm
  change (ENNReal.ofReal (‖R v-v‖^2) + dualQuadraticIntegral A (R v)).toReal ≤
    (ENNReal.ofReal (‖w-v‖^2) + dualQuadraticIntegral A w).toReal at ht
  rw [ENNReal.toReal_add ENNReal.ofReal_ne_top hr,
    ENNReal.toReal_add ENNReal.ofReal_ne_top (ne_of_lt hw),
    ENNReal.toReal_ofReal (sq_nonneg _), ENNReal.toReal_ofReal (sq_nonneg _),
    dualResolvent_limit_energy_identity A R hA hlim v] at ht
  simp only [norm_sub_sq (𝕜 := ℂ), inner_sub_right, Complex.sub_re] at ht
  have hself : (inner ℂ (R v) (R v)).re = ‖R v‖^2 :=
    inner_self_eq_norm_sq (𝕜 := ℂ) (R v)
  rw [hself] at ht
  change ‖R v‖^2 - 2*(inner ℂ (R v) v).re + ‖v‖^2 +
    ((inner ℂ (R v) v).re - ‖R v‖^2) ≤
    ‖w‖^2 - 2*(inner ℂ w v).re + ‖v‖^2 +
      (dualQuadraticIntegral A w).toReal at ht
  linarith

#print axioms inner_norm_bound_of_variational_bound
#print axioms exists_preimage_of_inner_bound
#print axioms dualResolvent_variational_dual_bound
end
end TGLV350.Regular
