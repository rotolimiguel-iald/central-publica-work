import TGLExt.SectorFluidClosure

set_option autoImplicit false
set_option maxHeartbeats 2400000

/-!
# The conserved sector closure reaches the existing FLRW metric (Order 012, B3)

The null balance is an input. Conservation is obtained from H_sector_nonexchange, and the
Einstein/Friedmann provider of B2 is actually invoked. Its integration constant
is retained. The zero-constant specialization has H_zero_cosmological on its face.
-/

namespace ChatgptAudit.FLRW

open TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff
noncomputable section

variable {ι : Type*} [Fintype ι]

theorem sector_covariant_conservation (I : Set ℝ) (a : ℝ → ℝ)
    (F : SectorFluid ι I (flrwHubble a)) (c : TGLCoupling)
    (x : Coordinate4) (ht : x 0∈I) (hz : a (x 0) ≠ 0)
    (ha : DifferentiableAt ℝ a (x 0)) :
    tensorFieldDivergence (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a)))
      (flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c)) x = 0 := by
  rw [flrw_stress_divergence a _ _ x hz ha
    (F.corrected_rho_deriv c (x 0) ht).differentiableAt
    (F.corrected_pressure_differentiable c (x 0) ht),
    F.corrected_continuity c (x 0) ht]
  ext j
  fin_cases j <;> rfl

/-- G is an area calibration; beta is the single datum of B1. -/
theorem tgl_friedmann_from_sector_closure
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (I : Set ℝ) (a : ℝ → ℝ) (F : SectorFluid ι I (flrwHubble a))
    (c : TGLCoupling) (G : ℝ) (hG : 0 < G)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0))
    (hI : ∀ x∈U, x 0∈I)
    (hr : ∀ x∈U, 0 < F.totalRho (x 0))
    (he : ∀ x∈U, 0 ≤ F.enthalpy (x 0))
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/(1/(4*G))) •
          flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) v = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
        F.totalRho (x 0)*(1+c.beta*|1+F.wEff (x 0)|)-cosmological/3 ∧
      deriv (flrwHubble a) (x 0) = -4*Real.pi*G*
        (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) ∧
      deriv (F.correctedTotalRho c) (x 0)+3*flrwHubble a (x 0)*
        (F.correctedTotalRho c (x 0)+F.correctedTotalPressure c (x 0)) = 0 := by
  have hc := flrw_newton_coefficient G hG
  obtain ⟨cosmological, hF⟩ := flrw_friedmann_from_general_metric U hU hconn a
    (F.correctedTotalRho c) (F.correctedTotalPressure c) (1/(4*G)) ha hpos
    (fun x hx => (F.corrected_rho_deriv c (x 0) (hI x hx)).differentiableAt)
    (fun x hx => F.corrected_pressure_differentiable c (x 0) (hI x hx))
    H_null (fun x hx j => congrFun (sector_covariant_conservation I a F c x
      (hI x hx) (hpos x hx).ne' ((ha x hx).differentiableAt (by simp))) j)
  refine ⟨cosmological, fun x hx => ⟨?_,?_,(hF x hx).2.2⟩⟩
  · rw [(hF x hx).1, hc, F.multiplicative_closure c (x 0) (hr x hx) (he x hx)]
    ring
  · rw [(hF x hx).2.1]
    have hk : -(2*Real.pi/(1/(4*G)))/2 = -4*Real.pi*G := by linarith
    rw [hk]

/-- Specialization at an explicitly zero integration constant, using the full
    metric equation rather than assuming the desired scalar Friedmann law. -/
theorem tgl_friedmann_zero_cosmological
    (U : Set Coordinate4) (hU : IsOpen U) (I : Set ℝ) (a : ℝ → ℝ)
    (F : SectorFluid ι I (flrwHubble a)) (c : TGLCoupling) (G cosmological : ℝ)
    (hG : 0 < G) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (hr : 0 < F.totalRho (x 0)) (he : 0 ≤ F.enthalpy (x 0))
    (H_zero_cosmological : cosmological = 0)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x+
      cosmological • flrwMetric a x = (2*Real.pi/(1/(4*G))) •
        flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) :
    (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
      F.totalRho (x 0)*(1+c.beta*|1+F.wEff (x 0)|) := by
  rw [flrw_friedmann_first U hU a _ _ ha hpos x hx _ _ hE,
    H_zero_cosmological, flrw_newton_coefficient G hG,
    F.multiplicative_closure c (x 0) hr he]
  ring

end
end ChatgptAudit.FLRW
