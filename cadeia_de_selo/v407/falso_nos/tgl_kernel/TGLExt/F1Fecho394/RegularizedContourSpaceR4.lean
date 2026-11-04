import TGLExt.F1Fecho394.LowerGaussianContourR2
import TGLExt.F1Fecho394.RapidityExponentialSpanR2

/-! Contour integrability and equality form a genuine linear subspace.
The bounded scalar theorem extends to finite exponential coefficients by
linear induction, with integrability tracked at both boundaries. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
namespace F1Fecho.WedgeLaplace

def regSlice (b p y : ℝ) (F : ℂ → ℂ) (x : ℝ) : ℂ :=
  regularized b 0 p F ((x:ℂ)+(y:ℂ)*I)

theorem regSlice_add (b p y : ℝ) (F G : ℂ → ℂ) :
    regSlice b p y (F+G)=regSlice b p y F+regSlice b p y G := by
  funext x
  simp [regSlice,regularized,mul_add]

theorem regSlice_smul (b p y : ℝ) (c : ℂ) (F : ℂ → ℂ) :
    regSlice b p y (c • F)=c • regSlice b p y F := by
  funext x
  simp only [regSlice,regularized,Pi.smul_apply,smul_eq_mul]
  ring

def contourSpace (b p : ℝ) : Submodule ℂ (ℂ → ℂ) where
  carrier := {F | Integrable (regSlice b p 0 F) ∧
    Integrable (regSlice b p (-Real.pi) F) ∧
    (∫ x,regSlice b p (-Real.pi) F x)=∫ x,regSlice b p 0 F x}
  zero_mem' := by
    have he (y : ℝ) : regSlice b p y (0 : ℂ → ℂ) = (0 : ℝ → ℂ) := by
      funext x
      simp [regSlice,regularized]
    change Integrable (regSlice b p 0 0) ∧ Integrable (regSlice b p (-Real.pi) 0) ∧ _
    rw [he,he]
    exact ⟨integrable_zero _ _ _,integrable_zero _ _ _,rfl⟩
  add_mem' := by
    rintro F G ⟨hF0,hFπ,hFe⟩ ⟨hG0,hGπ,hGe⟩
    change Integrable (regSlice b p 0 (F+G)) ∧
      Integrable (regSlice b p (-Real.pi) (F+G)) ∧ _
    rw [regSlice_add,regSlice_add]
    exact ⟨hF0.add hG0,hFπ.add hGπ,by simp only [Pi.add_apply]; rw [integral_add hFπ hGπ,integral_add hF0 hG0,hFe,hGe]⟩
  smul_mem' := by
    rintro c F ⟨hF0,hFπ,hFe⟩
    change Integrable (regSlice b p 0 (c • F)) ∧
      Integrable (regSlice b p (-Real.pi) (c • F)) ∧ _
    rw [regSlice_smul,regSlice_smul]
    exact ⟨hF0.smul c,hFπ.smul c,by simpa only [Pi.smul_apply,integral_smul] using congrArg (fun z : ℂ => c • z) hFe⟩

theorem regularized_mode_mul (b p k : ℝ) (F : ℂ → ℂ) (z : ℂ) :
    regularized b 0 p (F1Fecho.RapidityPolynomial.mode k*F) z=regularized b k p F z := by
  unfold regularized F1Fecho.RapidityPolynomial.mode
  simp only [ofReal_zero,add_zero,Pi.mul_apply,add_mul,exp_add]
  ring

theorem mode_mul_mem_contourSpace (b : ℝ) (hb : 0 < b) (p k C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    F1Fecho.RapidityPolynomial.mode k*F ∈ contourSpace b p := by
  change Integrable (regSlice b p 0 (F1Fecho.RapidityPolynomial.mode k*F)) ∧
    Integrable (regSlice b p (-Real.pi) (F1Fecho.RapidityPolynomial.mode k*F)) ∧ _
  have he (y : ℝ) : regSlice b p y (F1Fecho.RapidityPolynomial.mode k*F) =
      fun x : ℝ => regularized b k p F ((x:ℂ)+(y:ℂ)*I) := by
    funext x
    exact regularized_mode_mul b p k F _
  rw [he,he]
  refine ⟨?_,?_,?_⟩
  · exact regularized_slice_integrable b hb k p C 0 F hC hc hF
      (neg_nonpos.mpr Real.pi_pos.le) le_rfl
  · exact regularized_slice_integrable b hb k p C (-Real.pi) F hC hc hF le_rfl
      (neg_nonpos.mpr Real.pi_pos.le)
  · simpa only [ofReal_zero,zero_mul,add_zero] using
      regularized_contour_shift b hb k p C F hC hc hd hF


theorem polynomial_mul_mem_contourSpace (b : ℝ) (hb : 0 < b) (p C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C)
    (P : ℂ → ℂ) (hP : P ∈ F1Fecho.RapidityPolynomial.span) :
    P*F ∈ contourSpace b p := by
  induction hP using Submodule.span_induction with
  | mem P hP =>
    obtain ⟨k,rfl⟩ := hP
    exact mode_mul_mem_contourSpace b hb p k C F hC hc hd hF
  | zero => simpa only [zero_mul] using (contourSpace b p).zero_mem
  | add P Q hP hQ ihP ihQ =>
    rw [add_mul]
    exact (contourSpace b p).add_mem ihP ihQ
  | smul c P hP ih =>
    rw [smul_mul_assoc]
    exact (contourSpace b p).smul_mem c ih

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.contourSpace
#print axioms F1Fecho.WedgeLaplace.mode_mul_mem_contourSpace
#print axioms F1Fecho.WedgeLaplace.polynomial_mul_mem_contourSpace
