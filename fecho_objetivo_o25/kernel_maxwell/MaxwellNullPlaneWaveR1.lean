import NullFrequencyBochnerR2
import MaxwellNullPlaneAlgebraR2
import ProfileTensorWaveR1
import RealProfileMaxwellStressR4
import RegularMaxwellEnergyR2

/-! Candidate: the actual regular Maxwell wave on the null plane becomes
an angular Fourier integral in positive null frequency. Integrability is
proved from the existing RegularProfile, hence also StrongRegularProfile;
no integral identity, charge link or generator-domain property is an input.

The orbital measure and the actual H1 profile are unchanged. The preceding
Bochner transport cancels u against du/u. The real classical wave is obtained
by the existing sqrt(2) real-linear projection. This file does not establish
weighted Parseval for this profile, the charge/generator identity, the full
MaxwellCertificate, or nonzero modular energy. No build run by the author. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Set
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency

/-- Index of a transverse screen component in the actual four-vector. -/
def nullScreenIndex (a : Fin 2) : Fin 4 := ⟨a.val + 2, by omega⟩

def nullPlanePoint (λ : ℝ) (z : Fin 2 → ℝ) : Spacetime :=
  WithLp.toLp 2 (![λ, λ, z 0, z 1] : Fin 4 → ℝ)

def nullProfileAmplitude (h : H1) (a : Fin 2) (y : MomentumCoordinates) : ℂ :=
  ∑ j : Fin 2, (nullPolarization y a j : ℂ) * h y j

/-- Raw angular Fourier convention: there is no (2*pi) normalization here. -/
def nullAngularWave (h : H1) (a : Fin 2) (λ : ℝ) (z : Fin 2 → ℝ) : ℂ :=
  ∫ q : Transverse, ∫ u in Ioi 0,
    Complex.exp (Complex.I * ((-u * λ + q 0 * z 0 + q 1 * z 1 : ℝ) : ℂ)) *
      nullProfileAmplitude h a (nullMomentumCoordinates q u)

/-- Polarization is independent of null frequency at fixed transverse q. -/
theorem nullPolarization_nullMomentum (q : Transverse) (u v : ℝ) :
    nullPolarization (nullMomentumCoordinates q u) =
      nullPolarization (nullMomentumCoordinates q v) := rfl

theorem lowerProfileDensity_null_factor (h : H1) (a : Fin 2) (y : MomentumCoordinates) :
    lowerProfileDensity h 0 (nullScreenIndex a) y +
      lowerProfileDensity h 1 (nullScreenIndex a) y =
        (shellNullFrequency y : ℂ) * nullProfileAmplitude h a y := by
  have h0 : metricSignC (0 : Fin 4) = 1 := rfl
  have h1 : metricSignC (1 : Fin 4) = -1 := rfl
  have ha : metricSignC (nullScreenIndex a) = -1 := by
    fin_cases a <;> norm_num [nullScreenIndex, metricSignC]
  have hs (j : Fin 2) :
      -cartesianStrength y j 0 (nullScreenIndex a) +
        cartesianStrength y j 1 (nullScreenIndex a) =
          shellNullFrequency y * nullPolarization y a j :=
    null_strength_factor y a j
  calc
    _ = ∑ j : Fin 2,
        ((-cartesianStrength y j 0 (nullScreenIndex a) +
          cartesianStrength y j 1 (nullScreenIndex a) : ℝ) : ℂ) * h y j := by
      simp only [lowerProfileDensity, profileDensity, h0, h1, ha, Fin.sum_univ_two]
      push_cast
      ring
    _ = _ := by
      simp only [hs, Complex.ofReal_mul, nullProfileAmplitude, Finset.mul_sum, mul_assoc]

theorem lowerProfileWaveIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (μ ν : Fin 4) (x : Spacetime) :
    Integrable (fun y => wavePhase x y * lowerProfileDensity h μ ν y) (orbitalMeasure 0) := by
  have he : (fun y => wavePhase x y * lowerProfileDensity h μ ν y) =
      fun y => (metricSignC μ * metricSignC ν) *
        (wavePhase x y * profileDensity h μ ν y) := by
    funext y
    unfold lowerProfileDensity
    ring
  rw [he]
  exact (profileWaveIntegrand_integrable h hh μ ν x).const_mul _

theorem nullProfileWaveIntegrand_eq (h : H1) (a : Fin 2)
    (x : Spacetime) (y : MomentumCoordinates) :
    wavePhase x y * lowerProfileDensity h 0 (nullScreenIndex a) y +
      wavePhase x y * lowerProfileDensity h 1 (nullScreenIndex a) y =
        shellNullFrequency y • (wavePhase x y * nullProfileAmplitude h a y) := by
  rw [← mul_add, lowerProfileDensity_null_factor, Complex.real_smul]
  ring

/-- Integrability is discharged from the two existing Maxwell components. -/
theorem nullProfileWaveIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (x : Spacetime) :
    Integrable (fun y => shellNullFrequency y •
      (wavePhase x y * nullProfileAmplitude h a y)) (orbitalMeasure 0) := by
  have hi := (lowerProfileWaveIntegrand_integrable h hh 0 (nullScreenIndex a) x).add
    (lowerProfileWaveIntegrand_integrable h hh 1 (nullScreenIndex a) x)
  exact hi.congr (ae_of_all _ (fun y => nullProfileWaveIntegrand_eq h a x y))

/-- The actual contracted wave, after cancelling the invariant null measure. -/
theorem lowerProfileWave_null_transport (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (x : Spacetime) :
    lowerProfileWave h 0 (nullScreenIndex a) x +
      lowerProfileWave h 1 (nullScreenIndex a) x =
        ∫ q : Transverse, ∫ u in Ioi 0,
          wavePhase x (nullMomentumCoordinates q u) *
            nullProfileAmplitude h a (nullMomentumCoordinates q u) := by
  rw [lowerProfileWave_integral, lowerProfileWave_integral,
    ← integral_add (lowerProfileWaveIntegrand_integrable h hh 0 (nullScreenIndex a) x)
      (lowerProfileWaveIntegrand_integrable h hh 1 (nullScreenIndex a) x)]
  calc
    _ = ∫ y, shellNullFrequency y •
        (wavePhase x y * nullProfileAmplitude h a y) ∂orbitalMeasure 0 :=
      integral_congr_ae (ae_of_all _ (fun y => nullProfileWaveIntegrand_eq h a x y))
    _ = _ := orbital_nullFrequency_bochner_cancel
      (fun y => wavePhase x y * nullProfileAmplitude h a y)
      (nullProfileWaveIntegrand_integrable h hh a x)

theorem wavePhase_nullPlanePoint (λ : ℝ) (z : Fin 2 → ℝ) (y : MomentumCoordinates) :
    wavePhase (nullPlanePoint λ z) y =
      Complex.exp (Complex.I *
        ((-shellNullFrequency y * λ + y.1 0 * z 0 + y.1 1 * z 1 : ℝ) : ℂ)) := by
  have hp : -(inner ℝ (metricFlip (shellEmbedding y)) (nullPlanePoint λ z)) =
      -shellNullFrequency y * λ + y.1 0 * z 0 + y.1 1 * z 1 := by
    rw [metricFlip_inner]
    simp [shellEmbedding, nullPlanePoint, shellMomentum, shellNullFrequency, shellEnergy]
    <;> ring
  unfold wavePhase
  rw [hp]

theorem wavePhase_nullMomentum (λ : ℝ) (z : Fin 2 → ℝ) (q : Transverse)
    (u : ℝ) (hu : 0 < u) :
    wavePhase (nullPlanePoint λ z) (nullMomentumCoordinates q u) =
      Complex.exp (Complex.I * ((-u * λ + q 0 * z 0 + q 1 * z 1 : ℝ) : ℂ)) := by
  have hn : shellNullFrequency (nullMomentumCoordinates q u) = u :=
    null_inverseLongitudinal (transverseMass 0 q) u hu
  rw [wavePhase_nullPlanePoint, hn]
  rfl

theorem lowerProfileWave_null_angular (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (λ : ℝ) (z : Fin 2 → ℝ) :
    lowerProfileWave h 0 (nullScreenIndex a) (nullPlanePoint λ z) +
      lowerProfileWave h 1 (nullScreenIndex a) (nullPlanePoint λ z) =
        nullAngularWave h a λ z := by
  rw [lowerProfileWave_null_transport h hh a (nullPlanePoint λ z)]
  unfold nullAngularWave
  apply integral_congr_ae
  filter_upwards [] with q
  apply integral_congr_ae
  filter_upwards [ae_restrict_mem measurableSet_Ioi] with u hu
  rw [wavePhase_nullMomentum λ z q u hu]

/-- The existing REAL Maxwell wave, with its existing sqrt(2) projection. -/
theorem realProfileWave_null_angular (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (λ : ℝ) (z : Fin 2 → ℝ) :
    realProfileWave h 0 (nullScreenIndex a) (nullPlanePoint λ z) +
      realProfileWave h 1 (nullScreenIndex a) (nullPlanePoint λ z) =
        realWaveProjection (nullAngularWave h a λ z) := by
  unfold realProfileWave
  rw [← map_add, lowerProfileWave_null_angular h hh a λ z]

/-- The same result on the existing labels of the regular coherent Fock domain. -/
theorem realProfileWave_null_angular_strong (h : H1) (hh : StrongRegularProfile h)
    (a : Fin 2) (λ : ℝ) (z : Fin 2 → ℝ) :
    realProfileWave h 0 (nullScreenIndex a) (nullPlanePoint λ z) +
      realProfileWave h 1 (nullScreenIndex a) (nullPlanePoint λ z) =
        realWaveProjection (nullAngularWave h a λ z) :=
  realProfileWave_null_angular h hh.1 a λ z

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.nullPolarization_nullMomentum
#print axioms F1Fecho.MaxwellGlobal.lowerProfileDensity_null_factor
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWaveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.nullProfileWaveIntegrand_eq
#print axioms F1Fecho.MaxwellGlobal.nullProfileWaveIntegrand_integrable
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_null_transport
#print axioms F1Fecho.MaxwellGlobal.wavePhase_nullPlanePoint
#print axioms F1Fecho.MaxwellGlobal.wavePhase_nullMomentum
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_null_angular
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_null_angular
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_null_angular_strong
