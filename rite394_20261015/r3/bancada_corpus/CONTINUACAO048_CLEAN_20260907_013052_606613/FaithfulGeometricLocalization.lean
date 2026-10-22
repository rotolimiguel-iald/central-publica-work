import StationaryModularPeriod
import ThermalLimitControls
import ApproximateBoostFlow

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Geometry048

open TGLExt ChatgptAudit ChatgptAudit.Thermal025
  ChatgptAudit.Optical036 ChatgptAudit.Optical043 ChatgptAudit.Boost044
noncomputable section

/-- Faithfulness transfers an algebraic period to the labels of a covariant family. -/
theorem faithful_covariance_period_return {R X : Type*}
    (localize : R → X) (hfaith : Function.Injective localize)
    (Phi : ℝ → R → R) (sigma : ℝ → X → X) (T : ℝ)
    (hperiod : ∀ x, sigma T x = x)
    (hcov : ∀ s r, localize (Phi s r) = sigma s (localize r)) :
    ∀ r, Phi T r = r := by
  intro r
  apply hfaith
  exact (hcov T r).trans (hperiod (localize r))

/-- A period of the modular unitary is a period on all bounded operators. -/
theorem modular_period_conjugation_eq (P : SiteProfile) (T : ℝ)
    (hperiod : modularFlow P T = id)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P T A = A := by
  have hU (v : TowerHilbert P) : modularFlow P T v = v := congrFun hperiod v
  have hm (v : TowerHilbert P) : modularFlow P (-T) v = v := by
    have h := modularFlow_inverse (P := P) T v
    rwa [hU] at h
  ext v
  change modularFlow P T (A (modularFlow P (-T) v)) = A v
  rw [hU, hm]

/-- At a modular period, the image of every set of operators is unchanged. -/
theorem modular_period_image_eq (P : SiteProfile) (T : ℝ)
    (hperiod : modularFlow P T = id)
    (C : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
    (modularConjugation P T) '' C = C := by
  ext A
  constructor
  · rintro ⟨B, hB, rfl⟩
    simpa only [modular_period_conjugation_eq P T hperiod] using hB
  · intro hA
    exact ⟨A, hA, modular_period_conjugation_eq P T hperiod A⟩

/-- This conclusion needs faithfulness of the region family, not merely isotony. -/
theorem modular_period_geometric_return {R : Type*} (P : SiteProfile)
    (localize : R → Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hfaith : Function.Injective localize) (Phi : ℝ → R → R)
    (T : ℝ) (hperiod : modularFlow P T = id)
    (hcov : ∀ s r, (modularConjugation P s) '' localize r = localize (Phi s r)) :
    ∀ r, Phi T r = r :=
  faithful_covariance_period_return localize hfaith Phi
    (fun s C => (modularConjugation P s) '' C) T
    (modular_period_image_eq P T hperiod) (fun s r => (hcov s r).symm)

/-- A global dilation-covariant family must identify these two labels at a period. -/
theorem modular_period_dilation_return (P : SiteProfile) (T : ℝ)
    (hperiod : modularFlow P T = id)
    (A : ℝ → Set (TowerHilbert P →L[ℂ] TowerHilbert P)) (rate : ℝ)
    (hcov : ∀ s r, (modularConjugation P s) '' A r =
      A (Real.exp (-rate * s) * r)) (r : ℝ) :
    A (Real.exp (-rate * T) * r) = A r := by
  calc
    A (Real.exp (-rate * T) * r) = (modularConjugation P T) '' A r :=
      (hcov T r).symm
    _ = A r := modular_period_image_eq P T hperiod (A r)

/-- Separation of just one pair of labels suffices; no injective net is postulated. -/
theorem modular_period_dilation_obstruction (P : SiteProfile) (T : ℝ)
    (hperiod : modularFlow P T = id)
    (A : ℝ → Set (TowerHilbert P →L[ℂ] TowerHilbert P)) (rate : ℝ)
    (hseparates : A (Real.exp (-rate * T)) ≠ A 1) :
    ¬ (∀ s r, (modularConjugation P s) '' A r =
      A (Real.exp (-rate * s) * r)) := by
  intro hcov
  apply hseparates
  simpa only [mul_one] using modular_period_dilation_return P T hperiod A rate hcov 1

theorem dilation_factor_ne_one (rate T : ℝ) (hrate : rate ≠ 0) (hT : T ≠ 0) :
    Real.exp (-rate * T) ≠ 1 := by
  intro h
  have hz : -rate * T = 0 := Real.exp_eq_one_iff.mp h
  exact (mul_ne_zero (neg_ne_zero.mpr hrate) hT) hz

/-- A periodic modular flow cannot globally dilate a faithful family nontrivially. -/
theorem faithful_modular_dilation_localization_impossible (P : SiteProfile)
    (T : ℝ) (hT : 0 < T) (hperiod : modularFlow P T = id)
    (A : ℝ → Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hfaith : Function.Injective A) (rate : ℝ) (hrate : rate ≠ 0) :
    ¬ (∀ s r, (modularConjugation P s) '' A r =
      A (Real.exp (-rate * s) * r)) := by
  apply modular_period_dilation_obstruction P T hperiod A rate
  intro h
  exact dilation_factor_ne_one rate T hrate (ne_of_gt hT) (hfaith h)

/-- The actual central null curve has an inverse coordinate on its image. -/
theorem central_null_curve_injective : Function.Injective centralNullCurve := by
  intro r t h
  have hp := congrArg opticalPhaseCoordinate h
  simpa only [optical_phase_coordinate_central] using hp

/-- The geometric flow044 really fails to return at a nonzero central point. -/
theorem central_boost_no_return (rate T r : ℝ)
    (hrate : rate ≠ 0) (hT : T ≠ 0) (hr : r ≠ 0) :
    boostFlow rate T (centralNullCurve r) ≠ centralNullCurve r := by
  intro h
  rw [boost_flow_central] at h
  have hs := central_null_curve_injective h
  apply dilation_factor_ne_one rate T hrate hT
  apply mul_right_cancel₀ hr
  simpa only [one_mul] using hs

/-- Restricting the actual boost-covariant family to the ray gives the exact dilation. -/
theorem central_boost_covariance_to_dilation (P : SiteProfile)
    (localize : Coordinate4 → Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (rate : ℝ)
    (hcov : ∀ s x, (modularConjugation P s) '' localize x =
      localize (boostFlow rate s x)) :
    ∀ s r, (modularConjugation P s) '' localize (centralNullCurve r) =
      localize (centralNullCurve (Real.exp (-rate * s) * r)) := by
  intro s r
  simpa only [boost_flow_central] using hcov s (centralNullCurve r)

/-- Only faithfulness along the central ray is required, rather than across the chart. -/
theorem faithful_central_boost_localization_impossible (P : SiteProfile)
    (T : ℝ) (hT : 0 < T) (hperiod : modularFlow P T = id)
    (localize : Coordinate4 → Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hfaith : Function.Injective (fun r : ℝ => localize (centralNullCurve r)))
    (rate : ℝ) (hrate : rate ≠ 0) :
    ¬ (∀ s x, (modularConjugation P s) '' localize x =
      localize (boostFlow rate s x)) := by
  intro hcov
  exact faithful_modular_dilation_localization_impossible P T hT hperiod
    (fun r => localize (centralNullCurve r)) hfaith rate hrate
    (central_boost_covariance_to_dilation P localize rate hcov)

/-- The previously constructed period of the nontracial reference profile. -/
def thirdModularPeriod : ℝ :=
  2 * Real.pi / |Real.log (1 / 3 : ℝ) - Real.log (1 - (1 / 3 : ℝ))|

theorem third_modular_period_positive : 0 < thirdModularPeriod := by
  apply div_pos (mul_pos (by norm_num : (0 : ℝ) < 2) Real.pi_pos)
  apply abs_pos.mpr
  exact stationary_log_gap_ne_zero (P := thirdThermalReference)
    (p := (1 / 3 : ℝ)) (fun _ => rfl) (by norm_num)

theorem third_modular_flow_period :
    modularFlow thirdThermalReference thirdModularPeriod = id := by
  exact lattice_modular_period
    (stationary_log_gap_ne_zero (P := thirdThermalReference)
      (p := (1 / 3 : ℝ)) (fun _ => rfl) (by norm_num))
    (stationary_site_log_lattice (P := thirdThermalReference)
      (p := (1 / 3 : ℝ)) (fun _ => rfl))

theorem third_faithful_dilation_localization_impossible
    (A : ℝ → Set (TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference))
    (hfaith : Function.Injective A) (rate : ℝ) (hrate : rate ≠ 0) :
    ¬ (∀ s r, (modularConjugation thirdThermalReference s) '' A r =
      A (Real.exp (-rate * s) * r)) :=
  faithful_modular_dilation_localization_impossible thirdThermalReference
    thirdModularPeriod third_modular_period_positive third_modular_flow_period
    A hfaith rate hrate

theorem third_faithful_central_boost_localization_impossible
    (localize : Coordinate4 → Set (TowerHilbert thirdThermalReference →L[ℂ]
      TowerHilbert thirdThermalReference))
    (hfaith : Function.Injective (fun r : ℝ => localize (centralNullCurve r)))
    (rate : ℝ) (hrate : rate ≠ 0) :
    ¬ (∀ s x, (modularConjugation thirdThermalReference s) '' localize x =
      localize (boostFlow rate s x)) :=
  faithful_central_boost_localization_impossible thirdThermalReference
    thirdModularPeriod third_modular_period_positive third_modular_flow_period
    localize hfaith rate hrate

/-- A constant family equal to the actual factor is covariant: faithfulness matters. -/
theorem constant_factor_localization_covariant (P : SiteProfile) (s : ℝ) :
    (modularConjugation P s) '' (theFactorObject P :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P)) = theFactorObject P := by
  ext A
  constructor
  · rintro ⟨B, hB, rfl⟩
    exact (modularConjugation_preserves_factor P s B).mp hB
  · intro hA
    refine ⟨(modularConjugation P s).symm A, ?_,
      (modularConjugation P s).apply_symm_apply A⟩
    apply (modularConjugation_preserves_factor P s _).mpr
    simpa only [StarAlgEquiv.apply_symm_apply] using hA

theorem constant_factor_localization_not_injective (P : SiteProfile) :
    ¬ Function.Injective (fun _ : ℝ => (theFactorObject P :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P))) := by
  intro h
  have he : (0 : ℝ) = 1 := h rfl
  norm_num at he

#print axioms faithful_covariance_period_return
#print axioms modular_period_conjugation_eq
#print axioms modular_period_image_eq
#print axioms modular_period_geometric_return
#print axioms modular_period_dilation_return
#print axioms modular_period_dilation_obstruction
#print axioms dilation_factor_ne_one
#print axioms faithful_modular_dilation_localization_impossible
#print axioms central_null_curve_injective
#print axioms central_boost_no_return
#print axioms central_boost_covariance_to_dilation
#print axioms faithful_central_boost_localization_impossible
#print axioms thirdModularPeriod
#print axioms third_modular_period_positive
#print axioms third_modular_flow_period
#print axioms third_faithful_dilation_localization_impossible
#print axioms third_faithful_central_boost_localization_impossible
#print axioms constant_factor_localization_covariant
#print axioms constant_factor_localization_not_injective

end
end ChatgptAudit.Geometry048
