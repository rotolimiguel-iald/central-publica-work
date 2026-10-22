import TGLExt.SectorFriedmannAdditive
set_option autoImplicit false
open TGLExt ChatgptAudit.GeneralMetric ChatgptAudit.FLRW
open scoped ContDiff BigOperators
noncomputable section
variable {ι : Type*} [Fintype ι]
example
    (U : Set Coordinate4) (hU : IsOpen U) (I : Set ℝ) (a : ℝ → ℝ)
    (F : SectorFluid ι I (flrwHubble a)) (c : TGLCoupling) (G cosmological : ℝ)
    (hG : 0 < G) (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0))
    (hpos : ∀ y∈U, 0 < a (y 0)) (x : Coordinate4) (hx : x∈U)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x+
      cosmological • flrwMetric a x = (2*Real.pi/(1/(4*G))) •
        flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) :
    (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
      (∑ i, F.correctedRho c i (x 0))  := by
  exact tgl_friedmann_sector_additive_of_metric U hU I a F c G cosmological hG ha hpos x hx hE
end
