import TGLExt.V350DualSupportOperator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Radial stationarity at a finite-energy minimizer. This does not identify
the entire form domain with the domain of a square root. -/
theorem ClosedPositiveForm.minimizer_energy_identity
    (Q : ClosedPositiveForm H) (v r : H) (hr : Q.value r ≠ ⊤)
    (hmin : ∀ w : H, ENNReal.ofReal (‖r-v‖^2) + Q.value r ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w) :
    (Q.value r).toReal = (inner ℂ r v).re - ‖r‖^2 := by
  have hpoly : ∀ t : ℝ,
      0 ≤ (‖r‖^2 + (Q.value r).toReal)*t^2 -
        2*((inner ℂ r v).re - (‖r‖^2 + (Q.value r).toReal))*t := by
    intro t
    have he : Q.value (((t+1 : ℝ) : ℂ) • r) =
        ENNReal.ofReal ((t+1)^2) * Q.value r := by
      simpa only [Complex.norm_real, Real.norm_eq_abs, sq_abs] using
        Q.map_smul ((t+1 : ℝ) : ℂ) r
    have hi := hmin (((t+1 : ℝ) : ℂ) • r)
    rw [he] at hi
    have hf : ENNReal.ofReal (‖((t+1 : ℝ) : ℂ) • r-v‖^2) +
        ENNReal.ofReal ((t+1)^2) * Q.value r ≠ ⊤ :=
      ENNReal.add_ne_top.mpr ⟨ENNReal.ofReal_ne_top,
        ENNReal.mul_ne_top ENNReal.ofReal_ne_top hr⟩
    have hir := ENNReal.toReal_mono hf hi
    rw [ENNReal.toReal_add ENNReal.ofReal_ne_top hr,
      ENNReal.toReal_add ENNReal.ofReal_ne_top
        (ENNReal.mul_ne_top ENNReal.ofReal_ne_top hr), ENNReal.toReal_mul] at hir
    simp only [ENNReal.toReal_ofReal (sq_nonneg _)] at hir
    simp only [norm_sub_sq (𝕜 := ℂ)] at hir
    have hnorm : ‖((t+1 : ℝ) : ℂ) • r‖^2 = (t+1)^2 * ‖r‖^2 := by
      simp only [norm_smul, mul_pow, Complex.norm_real, Real.norm_eq_abs, sq_abs]
    have hinner : (inner ℂ (((t+1 : ℝ) : ℂ) • r) v).re =
        (t+1) * (inner ℂ r v).re := by
      simp only [inner_smul_left, Complex.conj_ofReal, Complex.mul_re,
        Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    change ‖r‖^2 - 2*(inner ℂ r v).re + ‖v‖^2 + (Q.value r).toReal ≤
      ‖((t+1 : ℝ) : ℂ) • r‖^2 -
        2*(inner ℂ (((t+1 : ℝ) : ℂ) • r) v).re + ‖v‖^2 +
        (t+1)^2*(Q.value r).toReal at hir
    rw [hnorm, hinner] at hir
    nlinarith
  have hc := linear_coefficient_zero_of_nonnegative_quadratic _ _
    (add_nonneg (sq_nonneg _) ENNReal.toReal_nonneg) hpoly
  linarith

theorem dualResolvent_limit_energy_identity
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    (dualQuadraticIntegral A (R v)).toReal = (inner ℂ (R v) (v-R v)).re := by
  have hr : (dualClosedPositiveForm A hA).value (R v) ≠ ⊤ :=
    ne_of_lt (dualResolvent_limit_range_finite A R hA hlim v)
  have hid := ClosedPositiveForm.minimizer_energy_identity
    (dualClosedPositiveForm A hA) v (R v) hr
    (dualResolvent_limit_minimizes_energy A R hA hlim v)
  change (dualQuadraticIntegral A (R v)).toReal =
    (inner ℂ (R v) v).re - ‖R v‖^2 at hid
  have hself : (inner ℂ (R v) (R v)).re = ‖R v‖^2 :=
    inner_self_eq_norm_sq (𝕜 := ℂ) (R v)
  rw [inner_sub_right, Complex.sub_re, hself]
  exact hid

theorem dualSupportOperator_inverse_parameter
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    R (((x : dualFormSupport A hA) + dualSupportOperator A R hA hR hlim x :
      dualFormSupport A hA) : RegularHilbert H) = (x : dualFormSupport A hA) := by
  let T := dualSupportOperator A R hA hR hlim
  let B := dualSupportResolvent A R hA hlim
  have hg := (resolvent_graph_equation B
    (dualSupportResolvent_injective A R hA hR hlim)
    (x : dualFormSupport A hA) (T x)).mp (T.mem_graph x)
  change (x : dualFormSupport A hA) - B x = B (T x) at hg
  have hp : B ((x : dualFormSupport A hA) + T x) = (x : dualFormSupport A hA) := by
    rw [map_add, ← hg]
    abel
  exact congrArg Subtype.val hp

/-- Finitude is explicit, before applying ENNReal.toReal. -/
theorem dualSupportOperator_domain_finite
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    dualQuadraticIntegral A (x : dualFormSupport A hA) < ⊤ := by
  have hf := dualResolvent_limit_range_finite A R hA hlim
    (((x : dualFormSupport A hA) + dualSupportOperator A R hA hR hlim x :
      dualFormSupport A hA) : RegularHilbert H)
  change dualQuadraticIntegral A _ < ⊤ at hf
  rw [dualSupportOperator_inverse_parameter A R hA hR hlim x] at hf
  exact hf

/-- The original form and the constructed operator agree on the operator
domain. This is still not the full square-root form-domain equality. -/
theorem dualSupportOperator_energy_identity
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    (dualQuadraticIntegral A (x : dualFormSupport A hA)).toReal =
      (inner ℂ (x : dualFormSupport A hA) (dualSupportOperator A R hA hR hlim x)).re := by
  let T := dualSupportOperator A R hA hR hlim
  let u : dualFormSupport A hA := (x : dualFormSupport A hA) + T x
  have hpu : R (u : RegularHilbert H) = (x : dualFormSupport A hA) :=
    dualSupportOperator_inverse_parameter A R hA hR hlim x
  have he := dualResolvent_limit_energy_identity A R hA hlim (u : RegularHilbert H)
  rw [hpu] at he
  have hdiff : (u : RegularHilbert H) - (x : dualFormSupport A hA) =
      (T x : RegularHilbert H) := by
    change (x : RegularHilbert H) + (T x : RegularHilbert H) -
      (x : RegularHilbert H) = (T x : RegularHilbert H)
    abel
  rw [hdiff] at he
  exact he

theorem dualSupportOperator_energy_ennreal
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    dualQuadraticIntegral A (x : dualFormSupport A hA) = ENNReal.ofReal
      (inner ℂ (x : dualFormSupport A hA) (dualSupportOperator A R hA hR hlim x)).re := by
  rw [← dualSupportOperator_energy_identity A R hA hR hlim x]
  exact (ENNReal.ofReal_toReal
    (ne_of_lt (dualSupportOperator_domain_finite A R hA hR hlim x))).symm

#print axioms ClosedPositiveForm.minimizer_energy_identity
#print axioms dualResolvent_limit_energy_identity
#print axioms dualSupportOperator_inverse_parameter
#print axioms dualSupportOperator_domain_finite
#print axioms dualSupportOperator_energy_identity
#print axioms dualSupportOperator_energy_ennreal
end
end TGLV350.Regular
