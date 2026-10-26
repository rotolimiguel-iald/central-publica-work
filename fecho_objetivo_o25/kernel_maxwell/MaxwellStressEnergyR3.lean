import MaxwellStressCalculusR3

/-! Reality and nonnegative classical energy of the Maxwell stress.
This is not a positivity statement for a renormalized quantum stress on all states. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellStress

theorem stress_zero (s : Fin 4→ℂ) (μ ν : Fin 4) : stress s (fun _ _=>0) μ ν=0 := by
  simp [stress]

theorem stress_real (s : Fin 4→ℝ) (F : Fin 4→Fin 4→ℝ) (μ ν : Fin 4) :
    star (stress (fun α=>(s α:ℂ)) (fun α β=>(F α β:ℂ)) μ ν)=
      stress (fun α=>(s α:ℂ)) (fun α β=>(F α β:ℂ)) μ ν := by
  by_cases h : μ=ν <;> simp [stress,h]

theorem stress_energy_identity (F : Fin 4→Fin 4→ℂ)
    (ha : ∀μ ν,F ν μ= -F μ ν) :
    stress (fun μ=>if μ=0 then 1 else -1) F 0 0=
      (1/2:ℂ)*(F 0 1^2+F 0 2^2+F 0 3^2+F 1 2^2+F 1 3^2+F 2 3^2) := by
  have hd (μ : Fin 4) : F μ μ=0 := by
    have h:=ha μ μ
    linear_combination (1/2:ℂ)*h
  have h10:=ha 0 1
  have h20:=ha 0 2
  have h30:=ha 0 3
  have h21:=ha 1 2
  have h31:=ha 1 3
  have h32:=ha 2 3
  have hn20 : (2:Fin 4)≠0 := by decide
  have hn30 : (3:Fin 4)≠0 := by decide
  norm_num [stress,Fin.sum_univ_four,hd,h10,h20,h30,h21,h31,h32,hn20,hn30]
  ring

theorem stress_classical_energy_nonneg (F : Fin 4→Fin 4→ℝ)
    (ha : ∀μ ν,F ν μ= -F μ ν) :
    0≤(stress (fun μ=>if μ=0 then 1 else -1) (fun μ ν=>(F μ ν:ℂ)) 0 0).re := by
  have hc : ∀μ ν,(F ν μ:ℂ)= -(F μ ν:ℂ) := by
    intro μ ν
    rw [ha μ ν]
    push_cast
    rfl
  rw [stress_energy_identity _ hc]
  have he : (1/2:ℂ)*((F 0 1:ℂ)^2+(F 0 2:ℂ)^2+(F 0 3:ℂ)^2+
      (F 1 2:ℂ)^2+(F 1 3:ℂ)^2+(F 2 3:ℂ)^2)=
      Complex.ofReal ((1/2:ℝ)*(F 0 1^2+F 0 2^2+F 0 3^2+F 1 2^2+F 1 3^2+F 2 3^2)) := by push_cast; rfl
  rw [he,Complex.ofReal_re]
  positivity

end F1Fecho.MaxwellStress
#print axioms F1Fecho.MaxwellStress.stress_zero
#print axioms F1Fecho.MaxwellStress.stress_real
#print axioms F1Fecho.MaxwellStress.stress_energy_identity
#print axioms F1Fecho.MaxwellStress.stress_classical_energy_nonneg
