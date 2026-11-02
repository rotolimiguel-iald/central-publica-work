import TGLExt.AperiodicCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace TowerDephasingStationary
open TGLExt ChatgptAudit ChatgptAudit.Aperiodic046 Filter
noncomputable section

/-- Pointwise stationarity of the existing full centralizer expectation, proved
on the actual infinite tower by its finite prefixes and their GNS limit. This
is stronger than preservation of the range as a set. -/
theorem existing_tower_dephasing_is_stationary (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) (t : ℝ) :
    modularConjugation P t (aperiodicExpectation P A) = aperiodicExpectation P A := by
  have hB := (aperiodic_expectation_spec P A hA).1
  have he (N : ℕ) :
      towerExpectation P N (modularConjugation P t (aperiodicExpectation P A)) =
      towerExpectation P N (aperiodicExpectation P A) := by
    rw [← expectation_flow_commutes, aperiodic_expectation_prefix P N A hA,
        modularConjugation_local]
    congr 1
    ext i j
    by_cases h : towerW P N i = towerW P N j
    · simp [flowLevel, modularPhase, h]
    · simp [flowLevel, h]
  apply factor_eq_of_omega ((modularConjugation_preserves_factor P t _).mp hB) hB
  have ht := expectation_omega_limit
    (modularConjugation P t (aperiodicExpectation P A))
  simp only [he] at ht
  exact tendsto_nhds_unique ht (expectation_omega_limit (aperiodicExpectation P A))

/-- The requested equality on the full dephased range forces the comparison
flow to fix it pointwise. No physical geometric action is assumed. -/
theorem existing_tower_flow_bridge_iff_stationary (P : SiteProfile)
    (alpha : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P) →
      (TowerHilbert P →L[ℂ] TowerHilbert P)) :
    (∀ A ∈ theFactorObject P, ∀ t,
      modularConjugation P t (aperiodicExpectation P A) =
        alpha t (aperiodicExpectation P A)) ↔
    (∀ A ∈ theFactorObject P, ∀ t,
      alpha t (aperiodicExpectation P A) = aperiodicExpectation P A) := by
  constructor
  · intro h A hA t
    rw [← h A hA t, existing_tower_dephasing_is_stationary P A hA t]
  · intro h A hA t
    rw [existing_tower_dephasing_is_stationary P A hA t, h A hA t]

#print axioms existing_tower_dephasing_is_stationary
#print axioms existing_tower_flow_bridge_iff_stationary
end
end TowerDephasingStationary
