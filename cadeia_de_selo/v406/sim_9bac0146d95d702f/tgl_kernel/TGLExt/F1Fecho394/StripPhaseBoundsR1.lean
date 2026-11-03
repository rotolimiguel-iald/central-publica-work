import TGLExt.O16.PositiveEnergyIntegral_v4
import Mathlib.Analysis.Calculus.DiffContOnCl
/-! Scalar estimates for the actual modular strip. The frequency h is signed;
the exponential moment is exp(h), so no positivity of log(Delta) is assumed.
This is analytic infrastructure, not a KMS certificate or a new physical input. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.StripPhase
open ChatgptAudit.PositiveEnergy016

def phase (z : ℂ) (h : ℝ) : ℂ := spectralPhase z (-h)

theorem norm_phase (z : ℂ) (h : ℝ) : ‖phase z h‖ = Real.exp (z.im*h) := by
  simp [phase,spectralPhase_norm]

theorem phase_derivative (z : ℂ) (h : ℝ) :
    HasDerivAt (fun w => phase w h) (((-h : ℝ) : ℂ)*Complex.I*phase z h) z :=
  spectralPhase_hasDerivAt z (-h)

theorem phase_bound (z : ℂ) (h : ℝ) (hz0 : 0≤z.im) (hz1 : z.im≤1) :
    ‖phase z h‖ ≤ 1+Real.exp h := by
  rw [norm_phase]
  by_cases hh : 0≤h
  · have he : Real.exp (z.im*h) ≤ Real.exp h :=
      Real.exp_le_exp.mpr (by nlinarith)
    linarith
  · have he : Real.exp (z.im*h) ≤ 1 :=
      Real.exp_le_one_iff.mpr (by nlinarith)
    linarith [Real.exp_pos h]

theorem derivative_bound (z : ℂ) (h δ : ℝ) (hd : 0<δ)
    (hz0 : δ≤z.im) (hz1 : z.im≤1-δ) :
    ‖((-h : ℝ) : ℂ)*Complex.I*phase z h‖ ≤ (1/δ)*(1+Real.exp h) := by
  have hd0 : 0≤1/δ := le_of_lt (one_div_pos.mpr hd)
  by_cases hh : 0≤h
  · have hx := spectralPhase_derivative_bound (⟨0,1-z.im⟩ : ℂ) h δ hh hd
      (show δ≤1-z.im by linarith)
    have hx' : h*Real.exp (-(1-z.im)*h) ≤ 1/δ := by
      simpa only [norm_mul,Complex.norm_real,Real.norm_eq_abs,abs_of_nonneg hh,
        Complex.norm_I,mul_one,spectralPhase_norm] using hx
    have he : Real.exp (z.im*h)=Real.exp h*Real.exp (-(1-z.im)*h) := by
      rw [← Real.exp_add]
      congr 1
      ring
    have hn : ‖((-h : ℝ) : ℂ)*Complex.I*phase z h‖ = h*Real.exp (z.im*h) := by
      simp [norm_mul,norm_phase,Real.norm_eq_abs,abs_of_nonneg hh]
    rw [hn,he]
    calc
      h*(Real.exp h*Real.exp (-(1-z.im)*h)) = Real.exp h*(h*Real.exp (-(1-z.im)*h)) := by ring
      _ ≤ Real.exp h*(1/δ) := mul_le_mul_of_nonneg_left hx' (Real.exp_pos h).le
      _ ≤ (1/δ)*(1+Real.exp h) := by nlinarith
  · have hx := spectralPhase_derivative_bound z (-h) δ (by linarith) hd hz0
    exact hx.trans (by nlinarith [Real.exp_pos h])

end F1Fecho.StripPhase
#print axioms F1Fecho.StripPhase.phase_bound
#print axioms F1Fecho.StripPhase.derivative_bound
