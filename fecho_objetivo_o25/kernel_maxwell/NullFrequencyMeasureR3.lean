import TGLExt.O16.RapidityJacobian_v2

/-! Exact positive null-frequency coordinate on each regular massless
rapidity fiber. The invariant measure is du/u, proved by change of variables.
This is a measure identity, not a modular-charge assertion. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.NullFrequency
open Set MeasureTheory
open ChatgptAudit.WignerRapidityMeasure016
open scoped ENNReal

def frequency (r x : ℝ) : ℝ := r*Real.exp (-x)

theorem frequency_pos (r : ℝ) (hr : 0<r) (x : ℝ) : 0<frequency r x :=
  mul_pos hr (Real.exp_pos _)

theorem frequency_hasDerivAt (r x : ℝ) :
    HasDerivAt (frequency r) (-frequency r x) x := by
  unfold frequency
  convert! (((Real.hasDerivAt_exp (-x)).comp x (hasDerivAt_id x).neg).const_mul r) using 1 <;> simp

theorem frequency_injective (r : ℝ) (hr : 0<r) : Function.Injective (frequency r) := by
  intro x y h
  have he:Real.exp (-x)=Real.exp (-y):=mul_left_cancel₀ hr.ne' h
  exact neg_injective (Real.exp_injective he)

theorem frequency_image (r : ℝ) (hr : 0<r) : frequency r '' (univ:Set ℝ)=Ioi 0 := by
  ext u
  constructor
  · rintro ⟨x,_,rfl⟩
    exact frequency_pos r hr x
  · intro hu
    refine ⟨-Real.log (u/r),mem_univ _,?_⟩
    simp only [frequency,neg_neg,Real.exp_log (div_pos hu hr)]
    field_simp

theorem frequency_is_shell_null (r : ℝ) (hr : 0<r) (x : ℝ) :
    energy r (longitudinal r x)-longitudinal r x=frequency r x := by
  rw [energy_longitudinal r hr x]
  unfold longitudinal frequency
  rw [←mul_sub,Real.cosh_sub_sinh]

theorem frequency_lintegral (r : ℝ) (hr : 0<r) (g : ℝ→ℝ≥0∞) :
    (∫⁻u in Ioi 0,ENNReal.ofReal (1/u)*g u)=∫⁻x,g (frequency r x) := by
  have hc:=lintegral_image_eq_lintegral_abs_deriv_mul
    (s:=(univ:Set ℝ)) MeasurableSet.univ
    (fun x _=>(frequency_hasDerivAt r x).hasDerivWithinAt)
    (frequency_injective r hr).injOn (fun u=>ENNReal.ofReal (1/u)*g u)
  rw [frequency_image r hr,Measure.restrict_univ] at hc
  rw [hc]
  apply lintegral_congr_ae
  apply ae_of_all
  intro x
  change ENNReal.ofReal (|-frequency r x|)*(ENNReal.ofReal (1/frequency r x)*g (frequency r x))=g (frequency r x)
  rw [←mul_assoc,abs_neg,abs_of_pos (frequency_pos r hr x),
    ←ENNReal.ofReal_mul (frequency_pos r hr x).le]
  have he:frequency r x*(1/frequency r x)=1:=by field_simp [(frequency_pos r hr x).ne']
  rw [he,ENNReal.ofReal_one,one_mul]

end F1Fecho.NullFrequency
#print axioms F1Fecho.NullFrequency.frequency_hasDerivAt
#print axioms F1Fecho.NullFrequency.frequency_is_shell_null
#print axioms F1Fecho.NullFrequency.frequency_lintegral
