import TGLExt.FLRWFieldEquations
set_option autoImplicit false
open Matrix TGLExt ChatgptAudit ChatgptAudit.GeneralMetric ChatgptAudit.FLRW
open scoped ContDiff
noncomputable section
-- Deliberate corruption: the existential constant changes sign.
example (U : Set Coordinate4) (hU : IsOpen U) (a rho pressure : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0<a(y 0))
    (x : Coordinate4) (hx : x∈U) (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x+
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    (flrwHubble a (x 0))^2 = coupling/3*rho(x 0)+cosmological/3 := by
  exact flrw_friedmann_first U hU a rho pressure ha hpos x hx coupling cosmological hE
end
