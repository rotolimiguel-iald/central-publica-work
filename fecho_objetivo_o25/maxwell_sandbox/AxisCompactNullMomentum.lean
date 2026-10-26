import CompactFockNullPlaneChargeR1

set_option autoImplicit false
set_option maxHeartbeats 2200000

/-! Unweighted null momentum integrability on the existing AxisCompact Fock core.
The proof reuses only the Schwartz structure already present in the Maxwell
construction. No positivity, rest frame or mass shell is assumed. -/
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Set MeasureTheory SchwartzMap
open TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore F1Fecho.CoherentKernel
open F1Fecho.WeightedPlancherel F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open ChatgptAudit.WignerRapidityMeasure016
open scoped FourierTransform

/-- Unweighted product of two scalar Fourier-Schwartz profiles. -/
theorem nullFourier_product_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => (𝓕 f x) * (𝓕 g x)) := by
  let fg : 𝓢(NullFourierSpace, ℂ) :=
    SchwartzMap.pairing (ContinuousLinearMap.mul ℂ ℂ) (𝓕 f) (𝓕 g)
  change Integrable fg
  exact fg.integrable

/-- Unweighted mixed term of two scalar Fourier-Schwartz profiles. -/
theorem nullFourier_mixed_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => inner ℂ (𝓕 f x) (𝓕 g x)) := by
  let cf : 𝓢(NullFourierSpace, ℂ) :=
    (𝓕 f).postcompCLM Complex.conjCLE.toContinuousLinearMap
  let fg : 𝓢(NullFourierSpace, ℂ) :=
    SchwartzMap.pairing (ContinuousLinearMap.mul ℂ ℂ) cf (𝓕 g)
  apply fg.integrable.congr
  filter_upwards [] with x
  simp [fg, cf]
  ring

/-- The unweighted product after the angular rescaling. -/
theorem nullAngular_product_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => angularForward f x * angularForward g x) := by
  have hc : (2 * Real.pi : ℝ) ≠ 0 := by positivity
  have hi := (nullFourier_product_integrable f g).comp_smul (inv_ne_zero hc)
  apply hi.congr
  filter_upwards [] with x
  simp only [angularForward]

/-- The unweighted mixed term after the angular rescaling. -/
theorem nullAngular_mixed_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace => inner ℂ (angularForward f x) (angularForward g x)) := by
  have hc : (2 * Real.pi : ℝ) ≠ 0 := by positivity
  have hi := (nullFourier_mixed_integrable f g).comp_smul (inv_ne_zero hc)
  apply hi.congr
  filter_upwards [] with x
  simp only [angularForward]

private theorem coherent_square_unweighted_expand (a b : ℂ) :
    ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) a + b))^2 =
      (1 / 2 : ℂ) * (starRingEnd ℂ) (a * a) + inner ℂ a b +
        (1 / 2 : ℂ) * (b * b) := by
  have hs : (Real.sqrt 2 : ℂ)^2 = 2 := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hi : ((Real.sqrt 2 : ℂ)⁻¹)^2 = (1 / 2 : ℂ) := by
    rw [inv_pow, hs]
    norm_num
  rw [mul_pow, hi]
  simp only [map_mul, RCLike.inner_apply']
  ring

/-- The diagonal coherent null stress is integrable without the Killing weight. -/
theorem nullAngular_coherent_square_unweighted_integrable (f g : 𝓢(NullFourierSpace, ℂ)) :
    Integrable (fun x : NullFourierSpace =>
      ((Real.sqrt 2 : ℂ)⁻¹ * ((starRingEnd ℂ) (angularForward f x) +
        angularForward g x))^2) := by
  have hc : Integrable (fun x : NullFourierSpace => (starRingEnd ℂ)
      (angularForward f x * angularForward f x)) :=
    Complex.conjCLE.toContinuousLinearMap.integrable_comp
      (nullAngular_product_integrable f f)
  have hi := ((hc.const_mul (1 / 2 : ℂ)).add
    (nullAngular_mixed_integrable f g)).add
      ((nullAngular_product_integrable g g).const_mul (1 / 2 : ℂ))
  apply hi.congr
  filter_upwards [] with x
  exact (coherent_square_unweighted_expand (angularForward f x) (angularForward g x)).symm

/-- Unweighted coherent null stress integrability. -/
theorem axisCompact_coherentNullStress_integrable (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    Integrable (unitaryFourierCoherentNullStress h k) := by
  have hi := ((nullAngular_coherent_square_unweighted_integrable
    (axisCompactNullData h hh 0).profile (axisCompactNullData k hk 0).profile).add
      (nullAngular_coherent_square_unweighted_integrable
        (axisCompactNullData h hh 1).profile (axisCompactNullData k hk 1).profile)).const_mul
          ((unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h k))
  apply hi.congr
  filter_upwards [] with x
  rw [axisCompact_coherentNullStress h k hh hk x]
  simp only [Pi.add_apply]

/-- Unweighted finite-Fock null stress integrability. -/
theorem axisCompact_fockNullStress_integrable (ψ χ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hχ : AxisCompactFock χ) :
    Integrable (unitaryFourierFockNullStress ψ χ) := by
  have hi := finiteKernel_integrable_on_support
    (fun h k : RegularLabel => unitaryFourierCoherentNullStress h.val k.val)
    (regularCoefficients ψ) (regularCoefficients χ)
    (fun h hh k hk => axisCompact_coherentNullStress_integrable h.val k.val
      (hψ h hh) (hχ k hk))
  apply hi.congr
  filter_upwards [] with x
  exact (unitaryFourierFockNullStress_eq_finiteKernel ψ χ x).symm

/-- The real diagonal null density is integrable in three dimensions. -/
theorem axisCompact_fockNullStress_real_integrable (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    Integrable (fun x : NullFourierSpace => (unitaryFourierFockNullStress ψ ψ x).re) := by
  exact (axisCompact_fockNullStress_integrable ψ ψ hψ hψ).re

/-- The contract's unweighted null-momentum integrand is integrable on AxisCompact. -/
theorem axisCompact_calibrated_nullMomentum_integrable {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (hψ : AxisCompactFock ψ) :
    Integrable (fun z : ℝ × (Fin 2 → ℝ) =>
      nullEnergy (toStress (regularMaxwellCalibratedForm A)).toStressTensorData ψ.val
        (z.1 • nullDir + screenEmbed z.2)) := by
  have hi := nullContractCoordinateEquiv_measurePreserving.integrable_comp_of_integrable
    (axisCompact_fockNullStress_real_integrable ψ hψ)
  apply hi.congr
  filter_upwards [] with z
  exact (calibrated_nullEnergy_contract_coordinates A ψ z).symm

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.MaxwellGlobal.nullFourier_product_integrable
#print axioms F1Fecho.MaxwellGlobal.nullFourier_mixed_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_product_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_mixed_integrable
#print axioms F1Fecho.MaxwellGlobal.nullAngular_coherent_square_unweighted_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentNullStress_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_real_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_calibrated_nullMomentum_integrable
