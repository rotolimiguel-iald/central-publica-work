import ModularFlowSpectrum
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Commutation032
open ChatgptAudit
noncomputable section

theorem phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ,
      Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c=
      Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :
    a=b := by
  have hd (r : ℝ) :
      HasDerivAt
        (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(r : ℂ))*c)
        ((Complex.I*(r : ℂ))*c) 0 := by
    have hr :=
      (((((hasDerivAt_id (0 : ℝ)).ofReal_comp).mul_const Complex.I).mul_const
        (r : ℂ)).cexp).mul_const c
    simpa using hr
  have hf :
      (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c)=
      (fun s : ℝ => Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :=
    funext h
  have ha := hd a
  rw [hf] at ha
  have hfreq := mul_right_cancel₀ hc (ha.unique (hd b))
  exact Complex.ofReal_injective
    (mul_left_cancel₀ Complex.I_ne_zero hfreq)

theorem modular_phase_exponential (s a : ℝ) :
    modularPhase s a=Complex.exp ((s : ℂ)*Complex.I*(a : ℂ)) := by
  unfold modularPhase
  congr 1
  push_cast
  ring

theorem modular_phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    a=b := by
  apply phase_frequency_separation a b c hc
  intro s
  simpa only [modular_phase_exponential] using h s

theorem phase_frequency_zero_or_equal (a b : ℝ) (c : ℂ)
    (h : ∀ s : ℝ,
      Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c=
      Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) :
    c=0 ∨ a=b := by
  by_cases hc : c=0
  · exact Or.inl hc
  · exact Or.inr (phase_frequency_separation a b c hc h)

theorem modular_phase_frequency_zero_or_equal (a b : ℝ) (c : ℂ)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    c=0 ∨ a=b := by
  by_cases hc : c=0
  · exact Or.inl hc
  · exact Or.inr (modular_phase_frequency_separation a b c hc h)

theorem modular_phase_frequency_iff (a b : ℝ) (c : ℂ) :
    (∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) ↔ c=0 ∨ a=b := by
  constructor
  · exact modular_phase_frequency_zero_or_equal a b c
  · rintro (rfl | rfl) s <;> simp

#print axioms phase_frequency_separation
#print axioms modular_phase_exponential
#print axioms modular_phase_frequency_separation
#print axioms phase_frequency_zero_or_equal
#print axioms modular_phase_frequency_zero_or_equal
#print axioms modular_phase_frequency_iff

end
end ChatgptAudit.Commutation032
