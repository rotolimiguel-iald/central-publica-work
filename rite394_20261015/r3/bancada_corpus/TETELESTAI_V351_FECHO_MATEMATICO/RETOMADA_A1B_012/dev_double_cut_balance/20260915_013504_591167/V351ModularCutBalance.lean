import TGLExt.V351ModularImplementation
import TGLExt.PhaseFrequencySeparation
import Mathlib.Analysis.CStarAlgebra.GelfandDuality

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit
noncomputable section

/-- Endpoint-safe scalar consumer of the previously proved frequency separation.
This private calculation alone does not assert the original operator balance. -/
private theorem damped_phase_scalar_balance (r a b : ℝ)
    (hr : r ∈ Set.Icc 0 1) (ha : a ∈ Set.Icc 0 1) (hb : b ∈ Set.Icc 0 1)
    (hphase : ∀ t : ℝ,
      resolventPhaseFunction t r * (resolventDamping a : ℂ) * (resolventDamping b : ℂ) =
      (resolventDamping r : ℂ) * resolventPhaseFunction t a * resolventPhaseFunction (-t) b) :
    (resolventDamping r * resolventDamping a * resolventDamping b) *
      ((1-r)*a*(1-b)-r*(1-a)*b) = 0 := by
  by_cases hz : resolventDamping r * resolventDamping a * resolventDamping b = 0
  · rw [hz, zero_mul]
  have hdr : resolventDamping r ≠ 0 := fun h => hz (by rw [h, zero_mul, zero_mul])
  have hda : resolventDamping a ≠ 0 := fun h => hz (by rw [h, mul_zero, zero_mul])
  have hdb : resolventDamping b ≠ 0 := fun h => hz (by rw [h, mul_zero])
  have hs (x : ℝ) (hx : x ∈ Set.Icc 0 1) (hd : resolventDamping x ≠ 0) :
      0 < x ∧ 0 < 1-x := by
    have h0 : x ≠ 0 := fun h => hd (by simp [resolventDamping,h])
    have h1 : x ≠ 1 := fun h => hd (by simp [resolventDamping,h])
    exact ⟨lt_of_le_of_ne hx.1 h0.symm, sub_pos.mpr (lt_of_le_of_ne hx.2 h1)⟩
  obtain ⟨hr0, hr1⟩ := hs r hr hdr
  obtain ⟨ha0, ha1⟩ := hs a ha hda
  obtain ⟨hb0, hb1⟩ := hs b hb hdb
  have hc : ((resolventDamping r * resolventDamping a * resolventDamping b : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast hz
  have hfreq : Real.log ((1-r)/r) = Real.log ((1-a)/a) - Real.log ((1-b)/b) := by
    apply Commutation032.modular_phase_frequency_separation _ _ _ hc
    intro t
    have hp : modularPhase t (Real.log ((1-a)/a) - Real.log ((1-b)/b)) =
        modularPhase t (Real.log ((1-a)/a)) * modularPhase (-t) (Real.log ((1-b)/b)) := by
      unfold modularPhase
      rw [← Complex.exp_add]
      congr 1
      push_cast
      ring
    rw [hp]
    have ht := hphase t
    simp only [resolventPhaseFunction] at ht
    push_cast
    calc
      _ = (resolventDamping r : ℂ) * modularPhase t (Real.log ((1-r)/r)) *
          (resolventDamping a : ℂ) * (resolventDamping b : ℂ) := by ring
      _ = _ := ht
      _ = _ := by ring
  have he : (1-r)/r = ((1-a)/a) / ((1-b)/b) := by
    calc
      _ = Real.exp (Real.log ((1-r)/r)) := (Real.exp_log (div_pos hr1 hr0)).symm
      _ = Real.exp (Real.log ((1-a)/a) - Real.log ((1-b)/b)) := congrArg Real.exp hfreq
      _ = _ := by rw [Real.exp_sub, Real.exp_log (div_pos ha1 ha0), Real.exp_log (div_pos hb1 hb0)]
  have he' : (1-r)*a*(1-b) = r*(1-a)*b := by
    field_simp [ne_of_gt hr0, ne_of_gt ha0, ne_of_gt hb0, ne_of_gt hb1] at he
    nlinarith [he]
  rw [he', sub_self, mul_zero]

#print axioms damped_phase_scalar_balance
end
end TGLV350.Regular
