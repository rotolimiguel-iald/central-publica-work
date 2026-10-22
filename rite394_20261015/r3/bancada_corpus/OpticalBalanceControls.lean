import OpticalVolterraBalance
import OpticalRiccatiInvariant
import Mathlib.Analysis.Calculus.Deriv.Pow

set_option autoImplicit false

namespace ChatgptAudit.Optical051
open MeasureTheory Set
noncomputable section

/-- An exactly integrated variable-curvature control. -/
theorem optical_affine_curvature_primitive (r v t : ℝ) :
    opticalPrimitive (fun s => r + v * s) t = r * t + v * t ^ 2 / 2 := by
  have hd : ∀ s ∈ uIcc 0 t,
      HasDerivAt (fun u : ℝ => r * u + v * u ^ 2 / 2) (r + v * s) s := by
    intro s _
    convert ((hasDerivAt_id s).const_mul r).add
      ((((hasDerivAt_id s).pow 2).const_mul v).div_const 2) using 1
    all_goals first | rfl | (simp only [id_eq]; ring)
  have hc : Continuous (fun s : ℝ => r + v * s) :=
    continuous_const.add (continuous_const.mul continuous_id)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd (hc.intervalIntegrable 0 t)
  simpa [opticalPrimitive] using h

theorem optical_affine_curvature_drift (r v t : ℝ) :
    opticalCurvatureDrift (fun s => r + v * s) t = -v * t ^ 2 / 2 := by
  rw [opticalCurvatureDrift, optical_affine_curvature_primitive]
  ring

theorem optical_affine_drift_negative (r v t : ℝ) (hv : 0 < v) (ht : t ≠ 0) :
    opticalCurvatureDrift (fun s => r + v * s) t < 0 := by
  rw [optical_affine_curvature_drift]
  have hp := sq_pos_of_ne_zero ht
  nlinarith [mul_pos hv hp]

theorem optical_affine_drift_positive (r v t : ℝ) (hv : v < 0) (ht : t ≠ 0) :
    0 < opticalCurvatureDrift (fun s => r + v * s) t := by
  rw [optical_affine_curvature_drift]
  have hp := sq_pos_of_ne_zero ht
  nlinarith [mul_pos (neg_pos.mpr hv) hp]

/-- Riccati data feed the exact balance; optical equations and matching remain hypotheses. -/
theorem optical_matrix_constant_balance
    (I : Set ℝ) (ho : IsOpen I) (hI : Convex ℝ I) (h0 : 0 ∈ I)
    (A x z y rxx rxy ryy Q : ℝ → ℝ) (K r : ℝ)
    (hB : ∀ s ∈ I, opticalRiccatiSystem x z y rxx rxy ryy s)
    (hR : ∀ s ∈ I, rxx s + ryy s = r)
    (hA : ∀ s ∈ I, HasDerivAt A (A s * (x s + y s)) s)
    (hzero : x 0 + y 0 = 0)
    (hQ : ∀ s ∈ I, HasDerivAt Q (-K * s * r * A s) s)
    (hQ0 : Q 0 = 0) (t : ℝ) (ht : t ∈ I) :
    Q t - K * (A t - A 0) =
      K * opticalVolterraCorrection A (fun s => opticalScreenNormSq (x s) (z s) (y s)) t := by
  have hx : ContinuousOn x I :=
    fun s hs => (hB s hs).1.continuousAt.continuousWithinAt
  have hz : ContinuousOn z I :=
    fun s hs => (hB s hs).2.1.continuousAt.continuousWithinAt
  have hy : ContinuousOn y I :=
    fun s hs => (hB s hs).2.2.continuousAt.continuousWithinAt
  have hF : ContinuousOn (fun s => opticalScreenNormSq (x s) (z s) (y s)) I := by
    unfold opticalScreenNormSq
    exact ((hx.pow 2).add (continuousOn_const.mul (hz.pow 2))).add (hy.pow 2)
  apply optical_volterra_balance_constant I ho hI h0 A (fun s => x s + y s)
    (fun s => opticalScreenNormSq (x s) (z s) (y s)) Q K r hF hA
    _ hzero hQ hQ0 t ht
  intro s hs
  simpa only [hR s hs] using optical_riccati_trace x z y rxx rxy ryy s (hB s hs)

theorem optical_matrix_correction_nonneg
    (I : Set ℝ) (hI : Convex ℝ I) (h0 : 0 ∈ I)
    (A x z y : ℝ → ℝ) (hA : ∀ s ∈ I, 0 ≤ A s) (t : ℝ) (ht : t ∈ I) :
    0 ≤ opticalVolterraCorrection A (fun s => opticalScreenNormSq (x s) (z s) (y s)) t :=
  optical_volterra_correction_nonneg I hI h0 A _ hA
    (fun s _ => optical_screen_norm_nonneg (x s) (z s) (y s)) t ht

/-- Algebraic orientation for a segment from t to zero, with a nonzero thermal factor. -/
theorem optical_past_entropy_orientation (Q A0 At temperature eta correction : ℝ)
    (hT : temperature ≠ 0)
    (hbalance : Q - temperature * eta * (At - A0) = temperature * eta * correction) :
    eta * (A0 - At) = (-Q) / temperature + eta * correction := by
  field_simp [hT]
  nlinarith [hbalance]

/-- At zero thermal factor, the scalar balance says only that the heat is zero. -/
theorem optical_zero_temperature_control (Q A0 At eta correction : ℝ) :
    (Q - (0 : ℝ) * eta * (At - A0) = (0 : ℝ) * eta * correction) ↔ Q = 0 := by
  simp

theorem optical_entropy_correction_nonneg (eta correction : ℝ)
    (heta : 0 ≤ eta) (hc : 0 ≤ correction) : 0 ≤ eta * correction :=
  mul_nonneg heta hc

#print axioms optical_affine_curvature_primitive
#print axioms optical_affine_curvature_drift
#print axioms optical_affine_drift_negative
#print axioms optical_affine_drift_positive
#print axioms optical_matrix_constant_balance
#print axioms optical_matrix_correction_nonneg
#print axioms optical_past_entropy_orientation
#print axioms optical_zero_temperature_control
#print axioms optical_entropy_correction_nonneg

end
end ChatgptAudit.Optical051
