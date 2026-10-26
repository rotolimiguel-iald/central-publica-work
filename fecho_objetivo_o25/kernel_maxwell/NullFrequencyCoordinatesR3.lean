import NullFrequencyMeasureR3

/-! Inverse null-frequency coordinate and exact fiber change of invariant
measure. The hypotheses exclude the zero transverse-mass axis explicitly. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.NullFrequency
open Set MeasureTheory
open ChatgptAudit.WignerRapidityMeasure016
open scoped ENNReal

def inverseLongitudinal (r u : ℝ) : ℝ := (r^2-u^2)/(2*u)
def inverseEnergy (r u : ℝ) : ℝ := (r^2+u^2)/(2*u)

theorem inverseEnergy_pos (r u : ℝ) (hu : 0<u) : 0 < inverseEnergy r u := by
  unfold inverseEnergy
  positivity

theorem energy_inverseLongitudinal (r u : ℝ) (hu : 0<u) :
    energy r (inverseLongitudinal r u)=inverseEnergy r u := by
  have he : r^2+(inverseLongitudinal r u)^2=(inverseEnergy r u)^2 := by
    unfold inverseLongitudinal inverseEnergy
    field_simp [hu.ne']
    ring
  unfold energy
  rw [he,Real.sqrt_sq (inverseEnergy_pos r u hu).le]

theorem null_inverseLongitudinal (r u : ℝ) (hu : 0<u) :
    energy r (inverseLongitudinal r u)-inverseLongitudinal r u=u := by
  rw [energy_inverseLongitudinal r u hu]
  unfold inverseEnergy inverseLongitudinal
  field_simp [hu.ne']
  ring

theorem shell_null_positive (r p : ℝ) (hr : 0<r) : 0<energy r p-p := by
  have hs : (energy r p)^2=r^2+p^2 := by
    exact Real.sq_sqrt (by positivity)
  have hn : 0≤energy r p := Real.sqrt_nonneg _
  nlinarith [sq_pos_of_pos hr]

theorem inverseLongitudinal_null (r p : ℝ) (hr : 0<r) :
    inverseLongitudinal r (energy r p-p)=p := by
  have hp:=(shell_null_positive r p hr).ne'
  have hs : (energy r p)^2=r^2+p^2 := Real.sq_sqrt (by positivity)
  unfold inverseLongitudinal
  field_simp [hp]
  nlinarith

theorem longitudinal_null_lintegral (r : ℝ) (hr : 0<r) (g : ℝ→ℝ≥0∞) :
    (∫⁻p,ENNReal.ofReal (1/energy r p)*g (energy r p-p))=
      ∫⁻u in Ioi 0,ENNReal.ofReal (1/u)*g u := by
  rw [longitudinal_lintegral r hr]
  simp_rw [frequency_is_shell_null r hr]
  exact (frequency_lintegral r hr g).symm

end F1Fecho.NullFrequency
#print axioms F1Fecho.NullFrequency.energy_inverseLongitudinal
#print axioms F1Fecho.NullFrequency.null_inverseLongitudinal
#print axioms F1Fecho.NullFrequency.inverseLongitudinal_null
#print axioms F1Fecho.NullFrequency.longitudinal_null_lintegral

#print axioms F1Fecho.NullFrequency.inverseEnergy_pos
#print axioms F1Fecho.NullFrequency.shell_null_positive
