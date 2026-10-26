import TGLExt.V350DualVariational
import Mathlib.Analysis.InnerProductSpace.Adjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal ComplexConjugate
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem linear_coefficient_zero_of_nonnegative_quadratic (a b : ℝ) (ha : 0 ≤ a)
    (h : ∀ t : ℝ, 0 ≤ a*t^2 - 2*b*t) : b = 0 := by
  let t := b / (a+1)
  have ht : (a+1)*t = b := mul_div_cancel₀ b (by linarith)
  have ht' := congrArg (fun x : ℝ => x*t) ht
  have h0 := h t
  have hsq := sq_nonneg t
  have hprod := mul_nonneg ha hsq
  have htzero : t = 0 := by nlinarith
  simpa only [htzero, mul_zero] using ht.symm

/-- A zero minimizer is orthogonal to every finite-energy direction. This lemma
uses arbitrary closed positive forms and does not assume a dense finite domain. -/
theorem ClosedPositiveForm.zero_minimizer_orthogonal (Q : ClosedPositiveForm H) (v : H)
    (hmin : ∀ w : H, ENNReal.ofReal (‖v‖^2) ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w) : v ∈ Q.finiteDomainᗮ := by
  have hreal : ∀ w ∈ Q.finiteDomain, (inner ℂ w v).re = 0 := by
    intro w hw
    have hwfin : Q.value w ≠ ⊤ := ne_of_lt hw
    have hpoly : ∀ t : ℝ, 0 ≤ (‖w‖^2 + (Q.value w).toReal)*t^2 -
        2*(inner ℂ w v).re*t := by
      intro t
      have he : Q.value ((t : ℂ) • w) = ENNReal.ofReal (t^2) * Q.value w := by
        simpa only [Complex.norm_real, Real.norm_eq_abs, sq_abs] using Q.map_smul (t : ℂ) w
      have hi := hmin ((t : ℂ) • w)
      rw [he] at hi
      have hright : ENNReal.ofReal (‖(t : ℂ) • w-v‖^2) +
          ENNReal.ofReal (t^2) * Q.value w ≠ ⊤ :=
        ENNReal.add_ne_top.mpr ⟨ENNReal.ofReal_ne_top,
          ENNReal.mul_ne_top ENNReal.ofReal_ne_top hwfin⟩
      have hir := ENNReal.toReal_mono hright hi
      rw [ENNReal.toReal_add ENNReal.ofReal_ne_top
        (ENNReal.mul_ne_top ENNReal.ofReal_ne_top hwfin),
        ENNReal.toReal_mul] at hir
      simp only [ENNReal.toReal_ofReal (sq_nonneg _)] at hir
      rw [norm_sub_sq (𝕜 := ℂ)] at hir
      have hnorm : ‖(t : ℂ) • w‖^2 = t^2 * ‖w‖^2 := by
        simp only [norm_smul, mul_pow, Complex.norm_real, Real.norm_eq_abs, sq_abs]
      have hinner : (inner ℂ ((t : ℂ) • w) v).re = t * (inner ℂ w v).re := by
        simp only [inner_smul_left, Complex.conj_ofReal, Complex.mul_re,
          Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
      change ‖v‖^2 ≤ ‖(t : ℂ) • w‖^2 -
        2*(inner ℂ ((t : ℂ) • w) v).re + ‖v‖^2 + t^2*(Q.value w).toReal at hir
      rw [hnorm, hinner] at hir
      nlinarith
    exact linear_coefficient_zero_of_nonnegative_quadratic _ _
      (add_nonneg (sq_nonneg _) ENNReal.toReal_nonneg) hpoly
  rw [Submodule.mem_orthogonal]
  intro w hw
  apply Complex.ext
  · exact hreal w hw
  · have hi := hreal (Complex.I • w) (Q.finiteDomain.smul_mem Complex.I hw)
    change (inner ℂ w v).im = 0
    simpa only [inner_smul_left, Complex.conj_I, Complex.mul_re, Complex.neg_re,
      Complex.I_re, neg_zero, zero_mul, Complex.neg_im, Complex.I_im,
      neg_mul, one_mul, zero_sub, neg_neg] using hi

/-- The kernel of the constructed strong limit is exactly the infinite-domain
orthogonal part. Strong convergence is supplied by exists_dualResolvent_limit. -/
theorem dualResolvent_kernel_eq_finiteDomain_orthogonal
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    R.ker = (dualClosedPositiveForm A hA).finiteDomainᗮ := by
  ext v
  constructor
  · intro hv
    have hvzero : R v = 0 := hv
    apply ClosedPositiveForm.zero_minimizer_orthogonal
    intro w
    change ENNReal.ofReal (‖v‖^2) ≤ ENNReal.ofReal (‖w-v‖^2) + dualQuadraticIntegral A w
    have hm := dualResolvent_limit_minimizes_energy A R hA hlim v w
    simpa only [dualEnergy, hvzero, zero_sub, norm_neg,
      dualQuadraticIntegral_zero_vector, add_zero] using hm
  · intro hv
    change R v = 0
    apply ext_inner_left ℂ
    intro u
    have hp := (ContinuousLinearMap.nonneg_iff_isPositive R).mp hR
    rw [inner_zero_right, ← hp.inner_left_eq_inner_right]
    exact ((dualClosedPositiveForm A hA).finiteDomain.mem_orthogonal v).mp hv
      (R u) (dualResolvent_limit_range_finite A R hA hlim u)

theorem dualResolvent_range_closure_eq_finiteDomain_closure
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    R.range.topologicalClosure = (dualClosedPositiveForm A hA).finiteDomain.topologicalClosure := by
  have hself : R.adjoint = R := (IsSelfAdjoint.of_nonneg hR).adjoint_eq
  calc
    R.range.topologicalClosure = R.kerᗮ := by
      simpa only [hself] using R.orthogonal_ker.symm
    _ = (dualClosedPositiveForm A hA).finiteDomainᗮᗮ := by
      rw [dualResolvent_kernel_eq_finiteDomain_orthogonal A R hA hR hlim]
    _ = _ := Submodule.orthogonal_orthogonal_eq_closure _

#print axioms linear_coefficient_zero_of_nonnegative_quadratic
#print axioms ClosedPositiveForm.zero_minimizer_orthogonal
#print axioms dualResolvent_kernel_eq_finiteDomain_orthogonal
#print axioms dualResolvent_range_closure_eq_finiteDomain_closure
end
end TGLV350.Regular
