import TGLExt.SectorFriedmann

set_option autoImplicit false

/-!
# Additive sector Friedmann equation with the integration constant retained

The existing metric and conservation providers are consumed. There is no
assumption that total density is strictly positive or enthalpy nonnegative.
Sector non-exchange remains part of SectorFluid; the null balance and Newton
calibration remain inputs. This does not select the thermodynamic route.
-/

namespace ChatgptAudit.FLRW
open TGLExt ChatgptAudit.GeneralMetric
open scoped ContDiff BigOperators
noncomputable section
variable {ι : Type*} [Fintype ι]

/-- The additive equation from the same null-balance provider as B3, with
    a single existential integration constant over the connected chart. -/
theorem tgl_friedmann_from_sector_closure_additive
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (I : Set ℝ) (a : ℝ → ℝ) (F : SectorFluid ι I (flrwHubble a))
    (c : TGLCoupling) (G : ℝ) (hG : 0 < G)
    (ha : ∀ x∈U, ContDiffAt ℝ ∞ a (x 0)) (hpos : ∀ x∈U, 0 < a (x 0))
    (hI : ∀ x∈U, x 0∈I)
    (H_null : ∀ x∈U, ∀ v, tensorQuad (flrwMetric a x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x-
        (2*Real.pi/(1/(4*G))) •
          flrwStress a (F.correctedTotalRho c) (F.correctedTotalPressure c) x) v = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      (flrwHubble a (x 0))^2 = (8*Real.pi*G/3)*
        (∑ i, F.correctedRho c i (x 0))-cosmological/3 := by
  obtain ⟨cosmological, hF⟩ := flrw_friedmann_from_general_metric U hU hconn a
    (F.correctedTotalRho c) (F.correctedTotalPressure c) (1/(4*G)) ha hpos
    (fun x hx => (F.corrected_rho_deriv c (x 0) (hI x hx)).differentiableAt)
    (fun x hx => F.corrected_pressure_differentiable c (x 0) (hI x hx))
    H_null (fun x hx j => congrFun (sector_covariant_conservation I a F c x
      (hI x hx) (hpos x hx).ne' ((ha x hx).differentiableAt (by simp))) j)
  refine ⟨cosmological, fun x hx => ?_⟩
  simpa only [flrw_newton_coefficient G hG, SectorFluid.correctedTotalRho] using (hF x hx).1

end
end ChatgptAudit.FLRW
