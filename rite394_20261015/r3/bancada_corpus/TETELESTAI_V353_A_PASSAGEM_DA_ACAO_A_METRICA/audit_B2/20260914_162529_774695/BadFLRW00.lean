import TGLExt.FLRWFieldEquations
set_option autoImplicit false
open Matrix TGLExt ChatgptAudit ChatgptAudit.GeneralMetric ChatgptAudit.FLRW
open scoped ContDiff
noncomputable section
-- Deliberate corruption: the 00 Einstein coefficient is changed.
example (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x 0 0 =
      4*(flrwHubble a (x 0))^2 := by
  exact flrw_einstein_00 U hU a ha hpos x hx
end
