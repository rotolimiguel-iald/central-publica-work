import MaxwellRealProjectionR1

/-! Strict positivity for an actual real classical Maxwell field when one
component is nonzero. This makes no quantum normal-ordering positivity claim. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open F1Fecho.MaxwellStress

theorem realWaveProjection_energy_pos_of_component (F : Fin 4→Fin 4→ℂ)
    (ha : ∀μ ν,F ν μ= -F μ ν) (hp : (F 0 1).re≠0) :
    0<(stress metricSignC (fun μ ν=>realWaveProjection (F μ ν)) 0 0).re := by
  have hc : ∀μ ν,realWaveProjection (F ν μ)= -realWaveProjection (F μ ν) := by
    intro μ ν
    rw [ha μ ν,map_neg]
  change 0<(stress (fun μ=>if μ=0 then 1 else -1)
    (fun μ ν=>realWaveProjection (F μ ν)) 0 0).re
  rw [stress_energy_identity _ hc]
  simp only [realWaveProjection_apply]
  have he : (1/2:ℂ)*
      ((Complex.ofReal (Real.sqrt 2*(F 0 1).re))^2+
       (Complex.ofReal (Real.sqrt 2*(F 0 2).re))^2+
       (Complex.ofReal (Real.sqrt 2*(F 0 3).re))^2+
       (Complex.ofReal (Real.sqrt 2*(F 1 2).re))^2+
       (Complex.ofReal (Real.sqrt 2*(F 1 3).re))^2+
       (Complex.ofReal (Real.sqrt 2*(F 2 3).re))^2)=
      Complex.ofReal ((1/2:ℝ)*
       ((Real.sqrt 2*(F 0 1).re)^2+(Real.sqrt 2*(F 0 2).re)^2+
        (Real.sqrt 2*(F 0 3).re)^2+(Real.sqrt 2*(F 1 2).re)^2+
        (Real.sqrt 2*(F 1 3).re)^2+(Real.sqrt 2*(F 2 3).re)^2)) := by
    push_cast
    rfl
  rw [he,Complex.ofReal_re]
  have hs : 0<(Real.sqrt 2*(F 0 1).re)^2 := sq_pos_of_ne_zero
    (mul_ne_zero (Real.sqrt_ne_zero'.mpr (by norm_num)) hp)
  nlinarith [sq_nonneg (Real.sqrt 2*(F 0 2).re),sq_nonneg (Real.sqrt 2*(F 0 3).re),
    sq_nonneg (Real.sqrt 2*(F 1 2).re),sq_nonneg (Real.sqrt 2*(F 1 3).re),
    sq_nonneg (Real.sqrt 2*(F 2 3).re)]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.realWaveProjection_energy_pos_of_component
