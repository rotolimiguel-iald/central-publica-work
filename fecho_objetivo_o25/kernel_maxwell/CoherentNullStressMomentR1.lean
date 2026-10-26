import CompactFockBoostDerivativeR2
import UnitaryFourierStressTensorR2
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! The complex mixed coherent null moment of the existing normalized tensor.
Its two same-sign terms vanish by positive-frequency support; its remaining
mixed term is evaluated by the existing weighted angular Parseval identity.
The sqrt(2) and (2*pi)^3 factors are kept explicitly until cancellation.
This is a mixed theorem, not polarization of a diagonal charge assertion. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.MaxwellGlobal
open MeasureTheory SchwartzMap Module
open TGLExt.ImportedSQ F1Fecho.WeightedPlancherel F1Fecho.MaxwellStress
open scoped LineDeriv

private theorem coherent_square_expand (w : ℝ) (a b : ℂ) :
    (w : ℂ) * ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) a + b))^2 =
      (1 / 2 : ℂ) * (starRingEnd ℂ) ((w : ℂ) * a * a) +
        (w : ℂ) * inner ℂ a b + (1 / 2 : ℂ) * ((w : ℂ) * b * b) := by
  have hs : (Real.sqrt 2 : ℂ)^2 = 2 := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hi : ((Real.sqrt 2 : ℂ)⁻¹)^2 = (1 / 2 : ℂ) := by
    rw [inv_pow, hs]
    norm_num
  rw [mul_pow, hi]
  simp only [map_mul, Complex.conj_ofReal, RCLike.inner_apply']
  ring

theorem nullAngular_coherent_square_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => (x 0 : ℂ) *
      ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) (angularForward f x) +
        angularForward g x))^2) := by
  have hc : Integrable (fun x : NullFourierSpace => (starRingEnd ℂ)
      ((x 0 : ℂ) * angularForward f x * angularForward f x)) :=
    Complex.conjCLE.toContinuousLinearMap.integrable_comp
      (nullAngular_weighted_product_integrable f f)
  have hi := ((hc.const_mul (1 / 2 : ℂ)).add
    (nullAngular_weighted_mixed_integrable f g)).add
      ((nullAngular_weighted_product_integrable g g).const_mul (1 / 2 : ℂ))
  apply hi.congr
  filter_upwards [] with x
  exact (coherent_square_expand (x 0) (angularForward f x) (angularForward g x)).symm

theorem nullAngular_coherent_square_moment (f g : 𝓢(NullFourierSpace, ℂ))
    (hf : ∀ p, p 0 ≤ 0 → f p = 0) (hg : ∀ p, p 0 ≤ 0 → g p = 0) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) *
      ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) (angularForward f x) +
        angularForward g x))^2) =
      (-Complex.I * (2 * Real.pi : ℝ)^3) *
        ∫ p, inner ℂ (f p) ((∂_{nullFrequencyDirection} g) p) := by
  have hc : Integrable (fun x : NullFourierSpace => (starRingEnd ℂ)
      ((x 0 : ℂ) * angularForward f x * angularForward f x)) :=
    Complex.conjCLE.toContinuousLinearMap.integrable_comp
      (nullAngular_weighted_product_integrable f f)
  have hm := nullAngular_weighted_mixed_integrable f g
  have hb := nullAngular_weighted_product_integrable g g
  simp_rw [coherent_square_expand]
  rw [integral_add ((hc.const_mul (1 / 2 : ℂ)).add hm) (hb.const_mul (1 / 2 : ℂ)),
    integral_add (hc.const_mul (1 / 2 : ℂ)) hm, integral_const_mul, integral_const_mul,
    integral_conj, nullAngular_weighted_same_sign_zero f f hf hf,
    nullAngular_weighted_same_sign_zero g g hg hg]
  simp only [map_zero, mul_zero, zero_add, add_zero]
  simpa only [nullFrequencyDirection_inner, finrank_euclideanSpace_fin] using
    angular_weighted_parseval f g nullFrequencyDirection

def unitaryFourierCoherentNullStress (h k : H1) (x : NullFourierSpace) : ℂ :=
  unitaryFourierCoherentStress h k 0 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierCoherentStress h k 0 1 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierCoherentStress h k 1 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierCoherentStress h k 1 1 (nullPlanePoint (x 0) (nullFourierScreen x))

theorem axisCompact_coherentNullWave (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k)
    (a : Fin 2) (x : NullFourierSpace) :
    coherentProfileWave h k 0 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) +
      coherentProfileWave h k 1 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) =
      (Real.sqrt 2 : ℂ)⁻¹ *
        ((starRingEnd ℂ) (angularForward (axisCompactNullData h hh a).profile x) +
          angularForward (axisCompactNullData k hk a).profile x) := by
  calc
    _ = (Real.sqrt 2 : ℂ)⁻¹ *
        ((starRingEnd ℂ) (nullContractedWave h a x) + nullContractedWave k a x) := by
      simp only [coherentProfileWave, nullContractedWave, map_add]
      ring
    _ = _ := by rw [axisCompact_nullContractedWave h hh a x,
      axisCompact_nullContractedWave k hk a x]

theorem axisCompact_coherentNullStress (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) (x : NullFourierSpace) :
    unitaryFourierCoherentNullStress h k x =
      (unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k) *
        (((Real.sqrt 2 : ℂ)⁻¹ *
          ((starRingEnd ℂ) (angularForward (axisCompactNullData h hh 0).profile x) +
            angularForward (axisCompactNullData k hk 0).profile x))^2 +
         ((Real.sqrt 2 : ℂ)⁻¹ *
          ((starRingEnd ℂ) (angularForward (axisCompactNullData h hh 1).profile x) +
            angularForward (axisCompactNullData k hk 1).profile x))^2) := by
  let X := nullPlanePoint (x 0) (nullFourierScreen x)
  have h0 := axisCompact_coherentNullWave h k hh hk 0 x
  have h1 := axisCompact_coherentNullWave h k hh hk 1 x
  change coherentProfileWave h k 0 2 X + coherentProfileWave h k 1 2 X = _ at h0
  change coherentProfileWave h k 0 3 X + coherentProfileWave h k 1 3 X = _ at h1
  calc
    _ = (unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k) *
        (stress metricSignC (fun μ ν => coherentProfileWave h k μ ν X) 0 0 +
         stress metricSignC (fun μ ν => coherentProfileWave h k μ ν X) 0 1 +
         stress metricSignC (fun μ ν => coherentProfileWave h k μ ν X) 1 0 +
         stress metricSignC (fun μ ν => coherentProfileWave h k μ ν X) 1 1) := by
      unfold unitaryFourierCoherentNullStress unitaryFourierCoherentStress coherentProfileStress
      dsimp [X]
      ring
    _ = _ := by
      rw [stress_null_contraction _ (fun μ ν => coherentProfileWave_antisymmetric h k μ ν X),
        h0, h1]

theorem axisCompact_coherentNullStress_moment_integrable (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    Integrable (fun x : NullFourierSpace => (x 0 : ℂ) * unitaryFourierCoherentNullStress h k x) := by
  have hi := ((nullAngular_coherent_square_integrable
    (axisCompactNullData h hh 0).profile (axisCompactNullData k hk 0).profile).add
      (nullAngular_coherent_square_integrable
        (axisCompactNullData h hh 1).profile (axisCompactNullData k hk 1).profile)).const_mul
          ((unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k))
  apply hi.congr
  filter_upwards [] with x
  rw [axisCompact_coherentNullStress h k hh hk x]
  ring

private theorem cancel_coherent_angular_volume (a b z : ℂ) :
    (unitaryFourierStressScale : ℂ) * z *
      (((-Complex.I * (2 * Real.pi : ℝ)^3) * a) +
       ((-Complex.I * (2 * Real.pi : ℝ)^3) * b)) = -Complex.I * (z * (a + b)) := by
  unfold unitaryFourierStressScale
  push_cast
  have hp : (Real.pi : ℂ) ≠ 0 := by exact_mod_cast Real.pi_ne_zero
  field_simp [hp, Real.pi_ne_zero]
  <;> ring

theorem axisCompact_coherentNullStress_moment (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) * unitaryFourierCoherentNullStress h k x) =
      -Complex.I * coherentBoostPair h k := by
  let f0 := (axisCompactNullData h hh 0).profile
  let f1 := (axisCompactNullData h hh 1).profile
  let g0 := (axisCompactNullData k hk 0).profile
  let g1 := (axisCompactNullData k hk 1).profile
  calc
    _ = (unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k) *
        ((∫ x : NullFourierSpace, (x 0 : ℂ) *
          ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) (angularForward f0 x) + angularForward g0 x))^2) +
         (∫ x : NullFourierSpace, (x 0 : ℂ) *
          ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) (angularForward f1 x) + angularForward g1 x))^2)) := by
      rw [← integral_add (nullAngular_coherent_square_integrable f0 g0)
        (nullAngular_coherent_square_integrable f1 g1), ← integral_const_mul]
      apply integral_congr_ae
      filter_upwards [] with x
      rw [axisCompact_coherentNullStress h k hh hk x]
      dsimp [f0, f1, g0, g1]
      ring
    _ = _ := by
      rw [nullAngular_coherent_square_moment f0 g0
        (axisCompactNullData h hh 0).zero_nonpositive (axisCompactNullData k hk 0).zero_nonpositive,
        nullAngular_coherent_square_moment f1 g1
        (axisCompactNullData h hh 1).zero_nonpositive (axisCompactNullData k hk 1).zero_nonpositive,
        cancel_coherent_angular_volume, coherentBoostPair,
        axisCompact_oneParticleBoostPair_null_integrals h k hh hk]

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullAngular_coherent_square_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_coherent_square_moment
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullWave
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress_moment
