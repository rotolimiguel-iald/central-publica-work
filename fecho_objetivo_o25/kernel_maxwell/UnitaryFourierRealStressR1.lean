import ConstructedRealNullStressMomentR1

/-! Additive Fourier-normalization adapter for the existing real Maxwell stress.
The raw angular Fourier convention contributes (2*pi)^3 to its first moment.
The unitary convention therefore multiplies the quadratic stress by its
reciprocal. No profile, H1 norm, boost, existing stress, or pinned file is changed.
The result identifies a frequency integral, not yet HasBoostEnergy or the full
Fock charge. The strong derivative, Fock-domain extension and nonzero modular
energy remain separate obligations. This file is a sandbox candidate. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory SchwartzMap
open TGLExt.ImportedSQ F1Fecho.WeightedPlancherel
open scoped LineDeriv

def unitaryFourierStressScale : ℝ := ((2 * Real.pi)^3)⁻¹

theorem unitaryFourierStressScale_pos : 0 < unitaryFourierStressScale := by
  unfold unitaryFourierStressScale
  positivity

def unitaryFourierRealNullStress (h : H1) (x : NullFourierSpace) : ℝ :=
  unitaryFourierStressScale * realNullStress h x

theorem axisCompact_unitaryFourierRealNullStress_nonneg
    (h : H1) (hh : AxisCompactProfile h) (x : NullFourierSpace) :
    0 ≤ unitaryFourierRealNullStress h x :=
  mul_nonneg (le_of_lt unitaryFourierStressScale_pos)
    (axisCompact_realNullStress_nonneg h hh x)

theorem axisCompact_unitaryFourierRealNullStress_moment_integrable
    (h : H1) (hh : AxisCompactProfile h) :
    Integrable (fun x : NullFourierSpace => x 0 * unitaryFourierRealNullStress h x) := by
  apply ((axisCompact_realNullStress_moment_integrable h hh).const_mul
    unitaryFourierStressScale).congr
  filter_upwards [] with x
  unfold unitaryFourierRealNullStress
  ring

private theorem cancel_angular_volume (z : ℂ) :
    unitaryFourierStressScale * ((-Complex.I * (2 * Real.pi : ℝ)^3) * z).re =
      (-Complex.I * z).re := by
  have hp : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  simp only [unitaryFourierStressScale, Complex.mul_re, Complex.mul_im,
    Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
    Complex.ofReal_pow, Complex.ofReal_re, Complex.ofReal_im]
  field_simp
  <;> ring

theorem axisCompact_unitaryFourierRealNullStress_moment
    (h : H1) (hh : AxisCompactProfile h) :
    (∫ x : NullFourierSpace, x 0 * unitaryFourierRealNullStress h x) =
      (-Complex.I * ∫ p, inner ℂ ((axisCompactNullData h hh 0).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData h hh 0).profile) p)).re +
      (-Complex.I * ∫ p, inner ℂ ((axisCompactNullData h hh 1).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData h hh 1).profile) p)).re := by
  calc
    _ = unitaryFourierStressScale *
        (∫ x : NullFourierSpace, x 0 * realNullStress h x) := by
      rw [← integral_const_mul]
      apply integral_congr_ae
      filter_upwards [] with x
      unfold unitaryFourierRealNullStress
      ring
    _ = _ := by
      rw [axisCompact_realNullStress_moment h hh, mul_add,
        cancel_angular_volume, cancel_angular_volume]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierStressScale_pos
#print axioms F1Fecho.MaxwellGlobal.axisCompact_unitaryFourierRealNullStress_nonneg
#print axioms F1Fecho.MaxwellGlobal.axisCompact_unitaryFourierRealNullStress_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_unitaryFourierRealNullStress_moment
