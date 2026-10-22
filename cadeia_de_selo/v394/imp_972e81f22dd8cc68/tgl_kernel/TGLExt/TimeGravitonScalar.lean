import TGLExt.TheRuleInTheContinuousMotor
import TGLExt.PhaseFrequencySeparation

/-! Exact scalar factors for the finite v394 flow. Phase clocks use an explicit
lift, not a single-valued inverse of a periodic angle. Rate and units remain
parameters; positivity is required only for decay. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace TGLExt.TimeGravitonFlow
open Complex Filter Topology
noncomputable section

def exponent (rate frequency : ℝ) : ℂ := -(rate : ℂ) + (frequency : ℂ)*Complex.I

def mode (rate frequency time : ℝ) : ℂ :=
  Complex.exp (exponent rate frequency * (time : ℂ))

theorem mode_eq_spin (rate frequency time : ℝ) :
    mode rate frequency time = IALDJones.spin rate frequency time := by
  unfold mode exponent IALDJones.spin IALDJones.coeff
  rw [Complex.ofReal_exp, ← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem mode_zero (rate frequency : ℝ) : mode rate frequency 0 = 1 := by
  simp [mode]

theorem mode_add (rate frequency s t : ℝ) :
    mode rate frequency (s+t) = mode rate frequency s * mode rate frequency t := by
  simp only [mode_eq_spin]
  exact IALDJones.spin_add rate frequency s t

theorem mode_ne_zero (rate frequency time : ℝ) : mode rate frequency time ≠ 0 :=
  Complex.exp_ne_zero _

theorem mode_norm (rate frequency time : ℝ) :
    ‖mode rate frequency time‖ = Real.exp (-(rate*time)) := by
  rw [mode_eq_spin]
  exact IALDJones.norm_spin rate frequency time

theorem mode_continuous (rate frequency : ℝ) : Continuous (mode rate frequency) := by
  unfold mode
  fun_prop

theorem mode_hasDerivAt (rate frequency time : ℝ) :
    HasDerivAt (mode rate frequency)
      (exponent rate frequency * mode rate frequency time) time := by
  have h := (((hasDerivAt_id time).ofReal_comp).const_mul (exponent rate frequency)).cexp
  unfold mode
  simpa [mode, mul_comm] using h

theorem mode_tendsto_zero (rate frequency : ℝ) (hr : 0 < rate) :
    Tendsto (mode rate frequency) atTop (nhds 0) := by
  apply tendsto_zero_iff_norm_tendsto_zero.mpr
  simp only [mode_norm]
  simpa only [IALDJones.coeff, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (Real.exp_pos _), abs_zero] using
    (IALDJones.coeff_tendsto_zero hr).norm

theorem module_clock (rate frequency time : ℝ) (hr : rate ≠ 0) :
    -Real.log ‖mode rate frequency time‖ / rate = time := by
  rw [mode_norm, Real.log_exp]
  field_simp

def liftedPhase (frequency time : ℝ) : ℝ := frequency*time

theorem phase_clock (omega s t : ℝ) (hω : omega ≠ 0) :
    (liftedPhase (2*omega) t - liftedPhase (2*omega) s)/(2*omega) = t-s := by
  unfold liftedPhase
  field_simp

theorem module_elapsed_clock (rate frequency s t : ℝ) (hr : rate ≠ 0) :
    -Real.log ‖mode rate frequency (t-s)‖ / rate = t-s :=
  module_clock rate frequency (t-s) hr

theorem phase_frequency_identified (a b : ℝ) (c : ℂ) (hc : c ≠ 0)
    (h : ∀ s : ℝ, Complex.exp ((s : ℂ)*Complex.I*(a : ℂ))*c =
      Complex.exp ((s : ℂ)*Complex.I*(b : ℂ))*c) : a = b :=
  ChatgptAudit.Commutation032.phase_frequency_separation a b c hc h

end
end TGLExt.TimeGravitonFlow
#print axioms TGLExt.TimeGravitonFlow.mode_eq_spin
#print axioms TGLExt.TimeGravitonFlow.mode_zero
#print axioms TGLExt.TimeGravitonFlow.mode_add
#print axioms TGLExt.TimeGravitonFlow.mode_ne_zero
#print axioms TGLExt.TimeGravitonFlow.mode_norm
#print axioms TGLExt.TimeGravitonFlow.mode_continuous
#print axioms TGLExt.TimeGravitonFlow.mode_hasDerivAt
#print axioms TGLExt.TimeGravitonFlow.mode_tendsto_zero
#print axioms TGLExt.TimeGravitonFlow.module_clock
#print axioms TGLExt.TimeGravitonFlow.phase_clock
#print axioms TGLExt.TimeGravitonFlow.module_elapsed_clock
#print axioms TGLExt.TimeGravitonFlow.phase_frequency_identified
