import CartesianMaxwellBianchiR3
import MaxwellStressEnergyR3

/-! A real-linear projection onto the actual real Maxwell wave, with the
sqrt(2) Segal coherent normalization. Its stress is real and its classical
energy nonnegative; this is not a statement about arbitrary quantum states. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open F1Fecho.MaxwellStress

def realWaveProjection : ℂ→L[ℝ]ℂ :=
  Real.sqrt 2 • (Complex.ofRealCLM.comp Complex.reCLM)

theorem realWaveProjection_apply (z : ℂ) :
    realWaveProjection z=Complex.ofReal (Real.sqrt 2*z.re) := by
  simp [realWaveProjection,Complex.real_smul]

theorem realWaveProjection_sign (μ : Fin 4) (z : ℂ) :
    realWaveProjection (metricSignC μ*z)=metricSignC μ*realWaveProjection z := by
  unfold metricSignC
  split_ifs <;> simp

theorem realWaveProjection_stress_real (F : Fin 4→Fin 4→ℂ) (μ ν : Fin 4) :
    star (stress metricSignC (fun α β=>realWaveProjection (F α β)) μ ν)=
      stress metricSignC (fun α β=>realWaveProjection (F α β)) μ ν := by
  simp only [realWaveProjection_apply]
  have hs : metricSignC=(fun μ=>Complex.ofReal (if μ=0 then 1 else -1:ℝ)) := by
    funext μ
    by_cases h : μ=0 <;> simp [metricSignC,h]
  rw [hs]
  exact stress_real _ _ μ ν

theorem realWaveProjection_energy_nonneg (F : Fin 4→Fin 4→ℂ)
    (ha : ∀μ ν,F ν μ= -F μ ν) :
    0≤(stress metricSignC (fun μ ν=>realWaveProjection (F μ ν)) 0 0).re := by
  simp only [realWaveProjection_apply]
  have hr : ∀μ ν,Real.sqrt 2*(F ν μ).re= -(Real.sqrt 2*(F μ ν).re) := by
    intro μ ν
    rw [ha μ ν,Complex.neg_re,mul_neg]
  exact stress_classical_energy_nonneg (fun μ ν=>Real.sqrt 2*(F μ ν).re) hr

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.realWaveProjection_apply
#print axioms F1Fecho.MaxwellGlobal.realWaveProjection_sign
#print axioms F1Fecho.MaxwellGlobal.realWaveProjection_stress_real
#print axioms F1Fecho.MaxwellGlobal.realWaveProjection_energy_nonneg
