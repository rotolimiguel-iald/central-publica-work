import ConstructedNullSchwartzConsumerR1
import NullSchwartzSameSignR2

/-! The first null-plane moment of the existing REAL classical Maxwell stress,
on the constructed axis-compact core of the actual H1. The sqrt(2) Segal
projection cancels the half from the real-wave Fourier identity. The screen
reflection and longitudinal coordinate are those of nullContractedWave.

This constructs an integral identity and its integrability, without assuming
a charge identity. It does not identify the result with the strong boost
generator or extend it to finite coherent Fock sums. MaxwellCertificate,
nonzero modular energy and the complete R8 criterion remain open. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Set SchwartzMap
open TGLExt.ImportedSQ F1Fecho.WeightedPlancherel
open scoped LineDeriv

def realNullStress (h : H1) (x : NullFourierSpace) : ℝ :=
  (realProfileStress h 0 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
   realProfileStress h 0 1 (nullPlanePoint (x 0) (nullFourierScreen x)) +
   realProfileStress h 1 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
   realProfileStress h 1 1 (nullPlanePoint (x 0) (nullFourierScreen x))).re

theorem axisCompact_realNullWave (h : H1) (hh : AxisCompactProfile h)
    (a : Fin 2) (x : NullFourierSpace) :
    realProfileWave h 0 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) +
      realProfileWave h 1 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) =
    Complex.ofReal (Real.sqrt 2 * (angularForward (axisCompactNullData h hh a).profile x).re) := by
  rw [realProfileWave_null_angular h (axisCompactProfile_strongRegular h hh).1,
    nullAngularWave_eq_angularForward h a (axisCompactNullData h hh a),
    realWaveProjection_apply]

theorem axisCompact_realNullStress (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) :
    realNullStress h x = 2 *
      ((angularForward (axisCompactNullData h hh 0).profile x).re ^ 2 +
       (angularForward (axisCompactNullData h hh 1).profile x).re ^ 2) := by
  let X := nullPlanePoint (x 0) (nullFourierScreen x)
  have h0 := axisCompact_realNullWave h hh 0 x
  have h1 := axisCompact_realNullWave h hh 1 x
  change realProfileWave h 0 2 X + realProfileWave h 1 2 X = _ at h0
  change realProfileWave h 0 3 X + realProfileWave h 1 3 X = _ at h1
  unfold realNullStress realProfileStress
  rw [stress_null_contraction _ (fun μ ν => realProfileWave_antisymmetric h μ ν X)]
  change ((realProfileWave h 0 2 X + realProfileWave h 1 2 X)^2 +
    (realProfileWave h 0 3 X + realProfileWave h 1 3 X)^2).re = _
  rw [h0,h1]
  simp only [← Complex.ofReal_pow, ← Complex.ofReal_add, Complex.ofReal_re,
    mul_pow, Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)]
  ring

theorem axisCompact_realNullStress_nonneg (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) : 0 ≤ realNullStress h x := by
  rw [axisCompact_realNullStress h hh x]
  positivity

theorem axisCompact_realNullStress_moment_integrable (h : H1)
    (hh : AxisCompactProfile h) :
    Integrable (fun x : NullFourierSpace => x 0 * realNullStress h x) := by
  let f := (axisCompactNullData h hh 0).profile
  let g := (axisCompactNullData h hh 1).profile
  have hi := ((nullAngular_real_product_integrable f f).add
    (nullAngular_real_product_integrable g g)).const_mul 2
  apply hi.congr
  filter_upwards [] with x
  rw [axisCompact_realNullStress h hh x]
  dsimp [f,g]
  ring

theorem axisCompact_realNullStress_moment (h : H1) (hh : AxisCompactProfile h) :
    (∫ x : NullFourierSpace, x 0 * realNullStress h x) =
    ((-Complex.I * (2 * Real.pi : ℝ)^3) *
      ∫ p, inner ℂ ((axisCompactNullData h hh 0).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData h hh 0).profile) p)).re +
    ((-Complex.I * (2 * Real.pi : ℝ)^3) *
      ∫ p, inner ℂ ((axisCompactNullData h hh 1).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData h hh 1).profile) p)).re := by
  let f := (axisCompactNullData h hh 0).profile
  let g := (axisCompactNullData h hh 1).profile
  have hf := (axisCompactNullData h hh 0).zero_nonpositive
  have hg := (axisCompactNullData h hh 1).zero_nonpositive
  have hi0 := (nullAngular_real_product_integrable f f).const_mul 2
  have hi1 := (nullAngular_real_product_integrable g g).const_mul 2
  calc
    _ = 2 * (∫ x : NullFourierSpace,
          x 0 * (angularForward f x).re * (angularForward f x).re) +
        2 * (∫ x : NullFourierSpace,
          x 0 * (angularForward g x).re * (angularForward g x).re) := by
      rw [← integral_const_mul, ← integral_const_mul, ← integral_add hi0 hi1]
      apply integral_congr_ae
      filter_upwards [] with x
      rw [axisCompact_realNullStress h hh x]
      dsimp [f,g]
      ring
    _ = _ := by
      rw [nullAngular_real_product_weighted_parseval f f hf hf,
        nullAngular_real_product_weighted_parseval g g hg hg]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullWave
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullStress
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullStress_nonneg
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullStress_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realNullStress_moment
