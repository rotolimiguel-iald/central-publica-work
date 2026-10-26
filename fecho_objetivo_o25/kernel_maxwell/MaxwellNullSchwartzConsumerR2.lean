import MaxwellNullPlaneWaveR2
import AngularWeightedPlancherelR3
import MaxwellMomentTransportR3

/-! Candidate consumer of the actual null Maxwell wave.

The extra domain data are a Schwartz representative of the null screen amplitude
of the SAME H1 profile, zero at nonpositive null frequency. The two a.e.
representative relations explicitly use the existing orbital and null measures;
they are regularity data, not an integral, charge, or generator identity.

The conclusions are (i) the existing contracted complex wave is its angular
Fourier transform, (ii) its mixed first moment is the exact weighted Parseval
form, and (iii) the existing B0 action has the same representative dilated by
u -> exp(s)u, whose pointwise derivative is +u partial_u.

OPEN: construct these data on a nonzero smooth core and prove density; derive
the equivalence of the two a.e. representations; prove a strong L2 derivative
and the Fock energy identity; handle same-sign real-wave terms and all finite
coherent sums; extend to Regular and construct a nonzero modular-energy
witness. No MaxwellCertificate, charge_link, trace/PF, or gate is asserted.
R2 repairs product-volume conversion, the integrable norm majorant and Fin.cons
coordinate elimination. The R1 terminal errors remain in custody; premises unchanged.
-/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Set SchwartzMap Module
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.NullFrequency F1Fecho.WeightedPlancherel
open scoped FourierTransform LineDeriv

abbrev NullFourierSpace := EuclideanSpace ℝ (Fin 3)

def nullFourierCoordinates (q : Transverse) (u : ℝ) : NullFourierSpace :=
  WithLp.toLp 2 (Fin.cons u q)

def nullFourierScreen (x : NullFourierSpace) : Transverse := fun a => -x a.succ

def nullFrequencyDirection : NullFourierSpace := nullFourierCoordinates 0 1

def nullFourierProfilePoint (y : MomentumCoordinates) : NullFourierSpace :=
  nullFourierCoordinates y.1 (shellNullFrequency y)

def nullCoordinateEquiv : (ℝ × Transverse) ≃ᵐ NullFourierSpace :=
  (MeasurableEquiv.piFinSuccAbove (fun _ : Fin 3 => ℝ) 0).symm.trans
    (MeasurableEquiv.toLp 2 (Fin 3 → ℝ))

@[simp] theorem nullCoordinateEquiv_apply (z : ℝ × Transverse) :
    nullCoordinateEquiv z = nullFourierCoordinates z.2 z.1 := by
  simp [nullCoordinateEquiv, nullFourierCoordinates,
    MeasurableEquiv.piFinSuccAbove_symm_apply, Fin.insertNthEquiv, Fin.insertNth_zero]

 theorem nullCoordinateEquiv_measurePreserving : MeasurePreserving nullCoordinateEquiv := by
  exact (PiLp.volume_preserving_toLp (Fin 3)).comp
    (volume_preserving_piFinSuccAbove (fun _ : Fin 3 => ℝ) 0).symm

 theorem integral_nullFourierCoordinates (F : NullFourierSpace → ℂ) (hF : Integrable F) :
    (∫ p, F p) = ∫ q : Transverse, ∫ u : ℝ, F (nullFourierCoordinates q u) := by
  have hi := nullCoordinateEquiv_measurePreserving.integrable_comp_of_integrable hF
  calc
    _ = ∫ z : ℝ × Transverse, F (nullCoordinateEquiv z) :=
      (nullCoordinateEquiv_measurePreserving.integral_comp' F).symm
    _ = _ := by
      simpa only [nullCoordinateEquiv_apply, MeasureTheory.Measure.volume_eq_prod] using
        (integral_prod_symm (fun z : ℝ × Transverse => F (nullCoordinateEquiv z)) hi)

 theorem nullFourierCoordinates_inner (q : Transverse) (u : ℝ) (x : NullFourierSpace) :
    inner ℝ (nullFourierCoordinates q u) x = u*x 0 + q 0*x 1 + q 1*x 2 := by
  simp [PiLp.inner_apply, nullFourierCoordinates, Fin.sum_univ_succ, Fin.sum_univ_two,
    real_inner_comm]
  <;> ring

@[simp] theorem nullFrequencyDirection_inner (x : NullFourierSpace) :
    inner ℝ x nullFrequencyDirection = x 0 := by
  rw [real_inner_comm, nullFrequencyDirection, nullFourierCoordinates_inner]
  simp

/-- A concrete smooth-representative domain, not a charge-link hypothesis.
No existence or density of this domain is claimed in this component. -/
structure NullSchwartzData (h : H1) (a : Fin 2) where
  profile : 𝓢(NullFourierSpace, ℂ)
  zero_nonpositive : ∀ p, p 0 ≤ 0 → profile p = 0
  null_ae : ∀ᵐ q : Transverse, ∀ᵐ u ∂volume.restrict (Ioi 0),
    nullProfileAmplitude h a (nullMomentumCoordinates q u) =
      profile (nullFourierCoordinates q u)
  orbital_ae : (fun y => nullProfileAmplitude h a y) =ᵐ[orbitalMeasure 0]
    fun y => profile (nullFourierProfilePoint y)

 theorem nullAngular_integrand_integrable (f : 𝓢(NullFourierSpace, ℂ))
    (x : NullFourierSpace) :
    Integrable (fun p => Complex.exp (-Complex.I * (inner ℝ p x : ℂ)) * f p) := by
  apply f.integrable.norm.mono'
  · have hc : Continuous (fun p : NullFourierSpace =>
        Complex.exp (-Complex.I * (inner ℝ p x : ℂ)) * f p) := by fun_prop
    exact hc.aestronglyMeasurable
  · filter_upwards [] with p
    simp [norm_mul, Complex.norm_exp, Complex.mul_re]

 theorem angularForward_integral_null (f : 𝓢(NullFourierSpace, ℂ))
    (x : NullFourierSpace) :
    angularForward f x =
      ∫ p, Complex.exp (-Complex.I * (inner ℝ p x : ℂ)) * f p := by
  unfold angularForward
  rw [SchwartzMap.fourier_coe, Real.fourier_eq']
  have he (p : NullFourierSpace) :
      ((-2 * Real.pi * inner ℝ p ((2 * Real.pi)⁻¹ • x) : ℝ) : ℂ) * Complex.I =
        -Complex.I * (inner ℝ p x : ℂ) := by
    rw [real_inner_smul_right]
    push_cast
    field_simp [Real.pi_ne_zero]
    <;> ring
  simp_rw [he, smul_eq_mul]

 theorem nullAngularWave_eq_angularForward (h : H1) (a : Fin 2)
    (D : NullSchwartzData h a) (x : NullFourierSpace) :
    nullAngularWave h a (x 0) (nullFourierScreen x) = angularForward D.profile x := by
  rw [angularForward_integral_null,
    integral_nullFourierCoordinates _ (nullAngular_integrand_integrable D.profile x)]
  unfold nullAngularWave
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

/-- The actual Maxwell component, with a coordinate reflection of the screen.
The reflection is explicit and preserves the longitudinal coordinate x 0. -/
def nullContractedWave (h : H1) (a : Fin 2) (x : NullFourierSpace) : ℂ :=
  lowerProfileWave h 0 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x)) +
    lowerProfileWave h 1 (nullScreenIndex a) (nullPlanePoint (x 0) (nullFourierScreen x))

 theorem nullContractedWave_eq_angularForward (h : H1) (hh : RegularProfile h)
    (a : Fin 2) (D : NullSchwartzData h a) (x : NullFourierSpace) :
    nullContractedWave h a x = angularForward D.profile x := by
  unfold nullContractedWave
  rw [lowerProfileWave_null_angular h hh,
    nullAngularWave_eq_angularForward h a D]

/-- The mixed physical-wave first moment; the raw angular factor is exact.
This is sesquilinear and is not yet the real stress charge. -/
 theorem nullContractedWave_weighted_parseval (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (a b : Fin 2)
    (D : NullSchwartzData h a) (E : NullSchwartzData k b) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) *
      inner ℂ (nullContractedWave h a x) (nullContractedWave k b x)) =
        (-Complex.I * (2 * Real.pi : ℝ)^3) *
          ∫ p, inner ℂ (D.profile p) ((∂_{nullFrequencyDirection} E.profile) p) := by
  simp_rw [nullContractedWave_eq_angularForward h hh a D,
    nullContractedWave_eq_angularForward k hk b E]
  simpa only [nullFrequencyDirection_inner, finrank_euclideanSpace_fin] using
    (angular_weighted_parseval D.profile E.profile nullFrequencyDirection)

/-- A smooth coordinate orbit; equality to the existing B0 action is proved
below in the orbital a.e. sense, rather than used as an input. -/
def nullFrequencyDilation (s : ℝ) (p : NullFourierSpace) : NullFourierSpace :=
  p + ((Real.exp s - 1) * p 0) • nullFrequencyDirection

 theorem nullFrequencyDilation_coordinates (s u : ℝ) (q : Transverse) :
    nullFrequencyDilation s (nullFourierCoordinates q u) =
      nullFourierCoordinates q (Real.exp s * u) := by
  apply PiLp.ext
  intro i
  refine Fin.cases ?_ (fun j => ?_) i
  · change u + ((Real.exp s - 1) * u) * 1 = Real.exp s * u
    ring
  · change q j + ((Real.exp s - 1) * u) * 0 = q j
    ring

 theorem shellNullFrequency_B0_ae (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,
      shellNullFrequency (coordinateBoost 0 (-s) y) = Real.exp s * shellNullFrequency y := by
  filter_upwards [shellEnergy_boost_ae (-s)] with y hy
  change shellEnergy (coordinateBoost 0 (-s) y) -
    (Real.cosh (-s) * y.2 + Real.sinh (-s) * shellEnergy y) = _
  rw [hy, Real.cosh_neg, Real.sinh_neg, ← Real.cosh_add_sinh]
  unfold shellNullFrequency
  ring

 theorem nullFourierProfilePoint_B0_ae (s : ℝ) :
    ∀ᵐ y ∂orbitalMeasure 0,
      nullFourierProfilePoint (coordinateBoost 0 (-s) y) =
        nullFrequencyDilation s (nullFourierProfilePoint y) := by
  filter_upwards [shellNullFrequency_B0_ae s] with y hy
  unfold nullFourierProfilePoint
  rw [nullFrequencyDilation_coordinates, hy]
  rfl

 theorem nullProfileAmplitude_B0_ae (s : ℝ) (h : H1) (a : Fin 2) :
    (fun y => nullProfileAmplitude (B0 s h) a y) =ᵐ[orbitalMeasure 0]
      fun y => nullProfileAmplitude h a (coordinateBoost 0 (-s) y) := by
  filter_upwards [B0_profile_ae s h] with y hy
  unfold nullProfileAmplitude
  rw [hy]
  rfl

 theorem nullSchwartz_B0_ae (s : ℝ) (h : H1) (a : Fin 2) (D : NullSchwartzData h a) :
    (fun y => nullProfileAmplitude (B0 s h) a y) =ᵐ[orbitalMeasure 0]
      fun y => D.profile (nullFrequencyDilation s (nullFourierProfilePoint y)) := by
  have hr := (coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae D.orbital_ae
  filter_upwards [nullProfileAmplitude_B0_ae s h a, hr,
    nullFourierProfilePoint_B0_ae s] with y hy hr' hp
  rw [hy, hr', hp]

/-- Pointwise generator on the SAME Schwartz profile as in weighted Parseval.
This theorem is not a strong derivative in H1 and not HasBoostEnergy. -/
 theorem nullSchwartz_dilation_hasDerivAt (f : 𝓢(NullFourierSpace, ℂ))
    (p : NullFourierSpace) :
    HasDerivAt (fun s => f (nullFrequencyDilation s p))
      (p 0 • ((∂_{nullFrequencyDirection} f) p)) 0 := by
  have hd : HasDerivAt (fun s => nullFrequencyDilation s p)
      (p 0 • nullFrequencyDirection) 0 := by
    simpa [nullFrequencyDilation] using
      ((((Real.hasDerivAt_exp 0).sub_const 1).mul_const (p 0)).smul_const
        nullFrequencyDirection).const_add p
  have hf : HasFDerivAt (f : NullFourierSpace → ℂ) (fderiv ℝ f p) p :=
    f.differentiableAt.hasFDerivAt
  have hz : p = nullFrequencyDilation 0 p := by simp [nullFrequencyDilation]
  simpa only [Function.comp_def, map_smul,
    SchwartzMap.lineDerivOp_apply_eq_fderiv] using hf.comp_hasDerivAt_of_eq 0 hd hz

 theorem nullSchwartz_profile_generator (h : H1) (a : Fin 2)
    (D : NullSchwartzData h a) (y : MomentumCoordinates) :
    HasDerivAt (fun s => D.profile
      (nullFrequencyDilation s (nullFourierProfilePoint y)))
      (shellNullFrequency y • ((∂_{nullFrequencyDirection} D.profile)
        (nullFourierProfilePoint y))) 0 := by
  exact nullSchwartz_dilation_hasDerivAt D.profile (nullFourierProfilePoint y)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.nullCoordinateEquiv_measurePreserving
#print axioms F1Fecho.MaxwellGlobal.integral_nullFourierCoordinates
#print axioms F1Fecho.MaxwellGlobal.nullAngular_integrand_integrable
#print axioms F1Fecho.MaxwellGlobal.angularForward_integral_null
#print axioms F1Fecho.MaxwellGlobal.nullAngularWave_eq_angularForward
#print axioms F1Fecho.MaxwellGlobal.nullContractedWave_eq_angularForward
#print axioms F1Fecho.MaxwellGlobal.nullContractedWave_weighted_parseval
#print axioms F1Fecho.MaxwellGlobal.shellNullFrequency_B0_ae
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_B0_ae
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_dilation_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.nullSchwartz_profile_generator
