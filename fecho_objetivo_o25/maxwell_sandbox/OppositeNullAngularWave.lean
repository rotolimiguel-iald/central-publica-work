import OppositeNullCoordinates

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Opposite-null angular wave and its exact Fourier-Schwartz representation. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel

/-- Raw opposite-null angular wave, with the opposite polarization amplitude. -/
def oppositeNullAngularWave (h : H1) (a : Fin 2) (ell : ℝ) (z : Fin 2 → ℝ) : ℂ :=
  ∫ q : Transverse, ∫ u in Ioi 0,
    Complex.exp (Complex.I * ((-u * ell + q 0 * z 0 + q 1 * z 1 : ℝ) : ℂ)) *
      oppositeNullProfileAmplitude h a (oppositeMomentumCoordinates q u)

/-- Exact opposite-null factorization of the two Maxwell wave components. -/
theorem oppositeProfileWaveIntegrand_eq (h : H1) (a : Fin 2)
    (x : Spacetime) (y : MomentumCoordinates) :
    wavePhase x y * lowerProfileDensity h 0 (nullScreenIndex a) y -
      wavePhase x y * lowerProfileDensity h 1 (nullScreenIndex a) y =
        shellOppositeFrequency y • (wavePhase x y * oppositeNullProfileAmplitude h a y) := by
  rw [← mul_sub, lowerProfileDensity_opposite_factor, Complex.real_smul]
  ring

/-- Opposite-null integrability follows from the two existing regular components. -/
theorem oppositeProfileWaveIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (x : Spacetime) :
    Integrable (fun y => shellOppositeFrequency y •
      (wavePhase x y * oppositeNullProfileAmplitude h a y)) (orbitalMeasure 0) := by
  have hi := (lowerProfileWaveIntegrand_integrable h hh 0 (nullScreenIndex a) x).sub
    (lowerProfileWaveIntegrand_integrable h hh 1 (nullScreenIndex a) x)
  exact hi.congr (ae_of_all _ (fun y => oppositeProfileWaveIntegrand_eq h a x y))

/-- The opposite contracted wave after cancelling the invariant orbital measure. -/
theorem lowerProfileWave_opposite_transport (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (x : Spacetime) :
    lowerProfileWave h 0 (nullScreenIndex a) x -
      lowerProfileWave h 1 (nullScreenIndex a) x =
        ∫ q : Transverse, ∫ u in Ioi 0,
          wavePhase x (oppositeMomentumCoordinates q u) *
            oppositeNullProfileAmplitude h a (oppositeMomentumCoordinates q u) := by
  rw [lowerProfileWave_integral, lowerProfileWave_integral,
    ← integral_sub (lowerProfileWaveIntegrand_integrable h hh 0 (nullScreenIndex a) x)
      (lowerProfileWaveIntegrand_integrable h hh 1 (nullScreenIndex a) x)]
  calc
    _ = ∫ y, shellOppositeFrequency y •
        (wavePhase x y * oppositeNullProfileAmplitude h a y) ∂orbitalMeasure 0 :=
      integral_congr_ae (ae_of_all _ (fun y => oppositeProfileWaveIntegrand_eq h a x y))
    _ = _ := orbital_oppositeFrequency_bochner_cancel
      (fun y => wavePhase x y * oppositeNullProfileAmplitude h a y)
      (oppositeProfileWaveIntegrand_integrable h hh a x)

/-- The phase at an opposite-shell momentum on the opposite null plane. -/
theorem wavePhase_oppositeMomentum (ell : ℝ) (z : Fin 2 → ℝ) (q : Transverse)
    (u : ℝ) (hu : 0 < u) :
    wavePhase (oppositeNullPlanePoint ell z) (oppositeMomentumCoordinates q u) =
      Complex.exp (Complex.I * ((-u * ell + q 0 * z 0 + q 1 * z 1 : ℝ) : ℂ)) := by
  rw [wavePhase_oppositeNullPlanePoint,
    shellOppositeFrequency_oppositeMomentumCoordinates q hu]
  rfl

/-- The physical opposite contraction is the raw opposite angular wave. -/
theorem lowerProfileWave_opposite_angular (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (ell : ℝ) (z : Fin 2 → ℝ) :
    lowerProfileWave h 0 (nullScreenIndex a) (oppositeNullPlanePoint ell z) -
      lowerProfileWave h 1 (nullScreenIndex a) (oppositeNullPlanePoint ell z) =
        oppositeNullAngularWave h a ell z := by
  rw [lowerProfileWave_opposite_transport h hh a (oppositeNullPlanePoint ell z)]
  unfold oppositeNullAngularWave
  apply integral_congr_ae
  filter_upwards [] with q
  apply integral_congr_ae
  filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
  rw [wavePhase_oppositeMomentum ell z q u hu]

/-- Opposite-shell representative in the same three-dimensional Fourier coordinates. -/
def oppositeFourierProfilePoint (y : MomentumCoordinates) : NullFourierSpace :=
  nullFourierCoordinates y.1 (shellOppositeFrequency y)

/-- Smooth representative data for the opposite amplitude; existence is proved separately. -/
structure OppositeNullSchwartzData (h : H1) (a : Fin 2) where
  profile : 𝓢(NullFourierSpace, ℂ)
  zero_nonpositive : ∀ p, p 0 ≤ 0 → profile p = 0
  null_ae : ∀ᵐ q : Transverse, ∀ᵐ u ∂volume.restrict (Ioi 0),
    oppositeNullProfileAmplitude h a (oppositeMomentumCoordinates q u) =
      profile (nullFourierCoordinates q u)
  orbital_ae : (fun y => oppositeNullProfileAmplitude h a y) =ᵐ[orbitalMeasure 0]
    fun y => profile (oppositeFourierProfilePoint y)

/-- The opposite angular wave is the angular Fourier transform of its representative. -/
theorem oppositeNullAngularWave_eq_angularForward (h : H1) (a : Fin 2)
    (D : OppositeNullSchwartzData h a) (x : NullFourierSpace) :
    oppositeNullAngularWave h a (x 0) (nullFourierScreen x) = angularForward D.profile x := by
  rw [angularForward_integral_null,
    integral_nullFourierCoordinates _ (nullAngular_integrand_integrable D.profile x)]
  unfold oppositeNullAngularWave
  apply integral_congr_ae
  filter_upwards [D.null_ae] with q hq
  have hzero : (Ioi (0 : ℝ)).indicator
      (fun u => Complex.exp (-Complex.I *
        (inner ℝ (nullFourierCoordinates q u) x : ℂ)) *
          D.profile (nullFourierCoordinates q u)) =
      fun u => Complex.exp (-Complex.I *
        (inner ℝ (nullFourierCoordinates q u) x : ℂ)) *
          D.profile (nullFourierCoordinates q u) := by
    funext u
    by_cases hu : 0 < u
    · simp [hu]
    · have hz := D.zero_nonpositive (nullFourierCoordinates q u) (le_of_not_gt hu)
      simp only [mem_Ioi, hu, not_false_eq_true, indicator_of_notMem]
      rw [hz, mul_zero]
  rw [← hzero, integral_indicator measurableSet_Ioi]
  apply integral_congr_ae
  filter_upwards [hq] with u hu
  rw [hu, nullFourierCoordinates_inner]
  congr 2
  simp only [nullFourierScreen]
  push_cast
  ring

/-- The actual opposite Maxwell component in null Fourier coordinates. -/
def oppositeContractedWave (h : H1) (a : Fin 2) (x : NullFourierSpace) : ℂ :=
  lowerProfileWave h 0 (nullScreenIndex a)
      (oppositeNullPlanePoint (x 0) (nullFourierScreen x)) -
    lowerProfileWave h 1 (nullScreenIndex a)
      (oppositeNullPlanePoint (x 0) (nullFourierScreen x))

/-- Objective Fourier representation of the physical opposite component. -/
theorem oppositeContractedWave_eq_angularForward (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (D : OppositeNullSchwartzData h a) (x : NullFourierSpace) :
    oppositeContractedWave h a x = angularForward D.profile x := by
  unfold oppositeContractedWave
  rw [lowerProfileWave_opposite_angular h hh,
    oppositeNullAngularWave_eq_angularForward h a D]

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.oppositeProfileWaveIntegrand_eq
#print axioms F1Fecho.MaxwellGlobal.oppositeProfileWaveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_opposite_transport
#print axioms F1Fecho.MaxwellGlobal.wavePhase_oppositeMomentum
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_opposite_angular
#print axioms F1Fecho.MaxwellGlobal.oppositeNullAngularWave_eq_angularForward
#print axioms F1Fecho.MaxwellGlobal.oppositeContractedWave_eq_angularForward
