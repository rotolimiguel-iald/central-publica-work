import TGLExt.SectorRouteComparison

set_option autoImplicit false
set_option maxHeartbeats 2400000

/-!
# The angular reading of the existing metric equations (Order 012, B5)

These are rewrites only. No angle is inserted in a cosmological runtime.
The null balance, horizon prescriptions, H_sector_nonexchange / H_singlefluid_continuity and integration constant retain
their types and status. The angle reads the same beta of B1.
-/

namespace ChatgptAudit.FLRW
open TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff
noncomputable section

theorem coupling_eq_sin_sq (c : TGLCoupling) :
    c.beta = Real.sin (thetaMiguel c.beta)^2 :=
  c.reflection_weight.symm.trans (normSq_reflection _)

theorem the_angle_reaches_the_metric (c : TGLCoupling) (w : ℝ) :
    entropyFactor c w = 1+Real.sin (thetaMiguel c.beta)^2*|1+w| := by
  unfold entropyFactor
  conv_lhs => rw [coupling_eq_sin_sq c]

theorem the_passage (H : ℝ → ℝ) (t G w enthalpy : ℝ) (c : TGLCoupling)
    (D : HubbleHorizonInput H t G (entropyFactor c w) enthalpy) :
    deriv H t = -4*Real.pi*G*(1+Real.sin (thetaMiguel c.beta)^2*|1+w|)*enthalpy := by
  rw [← the_angle_reaches_the_metric c w]
  exact tgl_second_friedmann_from_clausius H t G _ enthalpy D

theorem the_angle_reads_sector_first {ι : Type*} [Fintype ι]
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (I : Set ℝ) (a : ℝ → ℝ) (F : SectorFluid ι I (flrwHubble a))
    (c : TGLCoupling) (G : ℝ) (hG : 0 < G)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0))
    (hI : ∀ x∈U, x 0∈I) (hr : ∀ x∈U, 0 < F.totalRho (x 0))
    (he : ∀ x∈U, 0 ≤ F.enthalpy (x 0))
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/(1/(4*G))) •
          flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) v = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*F.totalRho (x 0)*
        (1+Real.sin (thetaMiguel c.beta)^2*|1+F.wEff (x 0)|)-cosmological/3 := by
  obtain ⟨cosmological,hF⟩ := tgl_friedmann_from_sector_closure
    U hU hconn I a F c G hG ha hpos hI hr he H_null
  refine ⟨cosmological, fun x hx => ?_⟩
  have h := (hF x hx).1
  conv_rhs at h => rw [coupling_eq_sin_sq c]
  exact h

end
end ChatgptAudit.FLRW
