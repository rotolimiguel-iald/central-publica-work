import OppositeNullData
import NullSchwartzSameSignR2

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Unweighted opposite-null stress integrability on the AxisCompact core. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open TGLExt.NullMomentumInvariant
open F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016 F1Fecho.NullFrequency
open F1Fecho.WeightedPlancherel F1Fecho.OrbitalScreen
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions

/-- Real opposite-null density as a function of the three null Fourier coordinates. -/
def realOppositeStress3D (h : H1) (x : NullFourierSpace) : ℝ :=
  realOppositeNullStress h (oppositeNullPlanePoint (x 0) (nullFourierScreen x))

/-- The real opposite Maxwell wave is the real part of the constructed Fourier wave. -/
theorem axisCompact_realOppositeWave (h : H1) (hh : AxisCompactProfile h)
    (a : Fin 2) (x : NullFourierSpace) :
    realProfileWave h 0 (nullScreenIndex a)
        (oppositeNullPlanePoint (x 0) (nullFourierScreen x)) -
      realProfileWave h 1 (nullScreenIndex a)
        (oppositeNullPlanePoint (x 0) (nullFourierScreen x)) =
    Complex.ofReal (Real.sqrt 2 *
      (angularForward (axisCompactOppositeData h hh a).profile x).re) := by
  unfold realProfileWave
  rw [← map_sub, lowerProfileWave_opposite_angular h (axisCompactProfile_strongRegular h hh).1,
    oppositeNullAngularWave_eq_angularForward h a (axisCompactOppositeData h hh a),
    realWaveProjection_apply]

/-- Exact sum of real Fourier squares for the opposite-null density. -/
theorem axisCompact_realOppositeStress3D (h : H1) (hh : AxisCompactProfile h)
    (x : NullFourierSpace) :
    realOppositeStress3D h x = 2 *
      ((angularForward (axisCompactOppositeData h hh 0).profile x).re ^ 2 +
       (angularForward (axisCompactOppositeData h hh 1).profile x).re ^ 2) := by
  let X := oppositeNullPlanePoint (x 0) (nullFourierScreen x)
  have h0 := axisCompact_realOppositeWave h hh 0 x
  have h1 := axisCompact_realOppositeWave h hh 1 x
  change realProfileWave h 0 2 X - realProfileWave h 1 2 X = _ at h0
  change realProfileWave h 0 3 X - realProfileWave h 1 3 X = _ at h1
  unfold realOppositeStress3D
  rw [realOppositeNullStress_eq_squares]
  change ((realProfileWave h 0 2 X - realProfileWave h 1 2 X)^2 +
    (realProfileWave h 0 3 X - realProfileWave h 1 3 X)^2).re = _
  rw [h0, h1]
  simp only [← Complex.ofReal_pow, ← Complex.ofReal_add, Complex.ofReal_re,
    mul_pow, Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]
  ring

private theorem coherent_square_unweighted_eq_real (a : ℂ) :
    ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) a + a))^2 = (2 * a.re ^ 2 : ℂ) := by
  have ha : (starRingEnd ℂ) a + a = (2 * a.re : ℂ) := by
    apply Complex.ext <;> simp [Complex.add_re, Complex.add_im] <;> ring
  have hs : (Real.sqrt 2 : ℂ)^2 = 2 := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hi : ((Real.sqrt 2 : ℂ)⁻¹)^2 = (1 / 2 : ℂ) := by
    rw [inv_pow, hs]
    norm_num
  rw [ha, mul_pow, hi]
  push_cast
  ring

private theorem nullAngular_real_square_unweighted_integrable
    (f : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => 2 * (angularForward f x).re ^ 2) := by
  have hi := (nullAngular_coherent_square_unweighted_integrable f f).re
  apply hi.congr
  filter_upwards [] with x
  rw [coherent_square_unweighted_eq_real]
  norm_cast

/-- The unweighted real opposite density is integrable in three dimensions. -/
theorem axisCompact_realOppositeStress3D_integrable (h : H1) (hh : AxisCompactProfile h) :
    Integrable (realOppositeStress3D h) := by
  let f := (axisCompactOppositeData h hh 0).profile
  let g := (axisCompactOppositeData h hh 1).profile
  have hi := (nullAngular_real_square_unweighted_integrable f).add
    (nullAngular_real_square_unweighted_integrable g)
  apply hi.congr
  filter_upwards [] with x
  rw [axisCompact_realOppositeStress3D h hh x]
  dsimp [f, g]
  ring

/-- The calibrated coherent opposite density is integrable in null Fourier coordinates. -/
theorem axisCompact_unitaryRealOppositeStress3D_integrable
    (h : H1) (hh : AxisCompactProfile h) :
    Integrable (fun x : NullFourierSpace =>
      unitaryFourierRealOppositeStress h
        (oppositeNullPlanePoint (x 0) (nullFourierScreen x))) := by
  have hi := (axisCompact_realOppositeStress3D_integrable h hh).const_mul
    (unitaryFourierStressScale * Real.exp (‖h‖ ^ 2))
  apply hi.congr
  filter_upwards [] with x
  rfl

/-- The opposite physical null plane in the existing volume-preserving chart. -/
theorem nullContractCoordinateEquiv_oppositePlane (z : ℝ × Transverse) :
    oppositeNullPlanePoint ((nullContractCoordinateEquiv z) 0)
      (nullFourierScreen (nullContractCoordinateEquiv z)) =
      WithLp.toLp 2 (z.1 • oppositeNullDir + screenEmbed z.2) := by
  rw [nullContractCoordinateEquiv_zero, nullContractCoordinateEquiv_screen]
  ext μ
  fin_cases μ <;> simp [oppositeNullPlanePoint, oppositeNullDir, screenEmbed]

/-- Objective opposite-momentum integrability for every coherent AxisCompact label. -/
theorem axisCompact_calibrated_oppositeMomentum_integrable {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    Integrable (fun z : ℝ × (Fin 2 → ℝ) =>
      oppositeNullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData
        (regularExponential h).val (z.1 • oppositeNullDir + screenEmbed z.2)) := by
  have hi := nullContractCoordinateEquiv_measurePreserving.integrable_comp_of_integrable
    (axisCompact_unitaryRealOppositeStress3D_integrable h.val hh)
  apply hi.congr
  filter_upwards [] with z
  simp only [Function.comp_apply, nullContractCoordinateEquiv_oppositePlane]
  exact (calibrated_oppositeNullEnergy_exponential A h _).symm

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.axisCompact_realOppositeWave
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realOppositeStress3D
#print axioms F1Fecho.MaxwellGlobal.axisCompact_realOppositeStress3D_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_unitaryRealOppositeStress3D_integrable
#print axioms F1Fecho.MaxwellGlobal.nullContractCoordinateEquiv_oppositePlane
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_oppositeMomentum_integrable
