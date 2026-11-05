import TGLExt.F1Fecho394.MaxwellComplexRapidityR3
import TGLExt.F1Fecho394.RapidityExponentialSpanR2

/-! The actual Maxwell bivector entries have finite exponential dependence
on complex rapidity. This derives the growth class from p and the screens. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellStrip
open F1Fecho.RapidityPolynomial ChatgptAudit.WignerRapidityMeasure016

theorem complexMomentum_mem (q : Fin 2 → ℝ) (i : Fin 4) :
    (fun z => complexMomentum q z i) ∈ span := by
  fin_cases i
  · change ((transverseMass 0 q:ℂ) • Complex.cosh) ∈ span
    exact span.smul_mem _ cosh_mem
  · change ((transverseMass 0 q:ℂ) • Complex.sinh) ∈ span
    exact span.smul_mem _ sinh_mem
  · exact const_mem _
  · exact const_mem _

theorem complexScreen_mem (q : Fin 2 → ℝ) (j : Fin 2) (i : Fin 4) :
    (fun z => complexScreen q j z i) ∈ span := by
  fin_cases j
  · fin_cases i
    · exact sinh_mem
    · exact cosh_mem
    · exact const_mem _
    · exact const_mem _
  · fin_cases i <;> exact const_mem _

theorem analyticStrength_mem (q : Fin 2 → ℝ) (j : Fin 2) (μ ν : Fin 4) :
    analyticStrength q j μ ν ∈ span := by
  change ((fun z => complexMomentum q z μ)*(fun z => complexScreen q j z ν)-
    (fun z => complexMomentum q z ν)*(fun z => complexScreen q j z μ)) ∈ span
  exact span.sub_mem
    (mul_mem _ _ (complexMomentum_mem q μ) (complexScreen_mem q j ν))
    (mul_mem _ _ (complexMomentum_mem q ν) (complexScreen_mem q j μ))

end F1Fecho.MaxwellStrip
#print axioms F1Fecho.MaxwellStrip.complexMomentum_mem
#print axioms F1Fecho.MaxwellStrip.complexScreen_mem
#print axioms F1Fecho.MaxwellStrip.analyticStrength_mem
