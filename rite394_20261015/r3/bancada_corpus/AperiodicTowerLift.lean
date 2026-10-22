import AperiodicCentralizerExpectation
import TGLExt.TheLiftFiresOnThePeriodicTower
import TGLExt.TheModularFlowIsAHorizon

set_option autoImplicit false

namespace ChatgptAudit.Aperiodic046

open TGLExt

noncomputable section

/-- The lift now has a constructed expectation for every admissible profile. -/
theorem the_lift_fires_on_the_aperiodic_tower (P : SiteProfile) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h ((aperiodicExpectationInput P).E A) =
        (aperiodicExpectationInput P).E (adT h A) :=
  the_lift_on_the_tower (aperiodicExpectationInput P) h

/-- Every other inhabitant agrees on the factor and has the same covariance. -/
theorem every_expectation_on_the_general_tower_is_covariant (P : SiteProfile)
    (I : ExpectationInput P) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      I.E A = (aperiodicExpectationInput P).E A ∧
        adT h (I.E A) = I.E (adT h A) :=
  fun A hA => ⟨the_expectation_is_unique I (aperiodicExpectationInput P) A hA,
    the_lift_on_the_tower I h A hA⟩

theorem aperiodic_expectation_agrees_periodic (P : SiteProfile)
    (T : ℝ) (hT : 0 < T) (hp : LocalPhasePeriod P T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E A = (periodicExpectationInput P T hT hp).E A :=
  the_expectation_is_unique (aperiodicExpectationInput P)
    (periodicExpectationInput P T hT hp) A hA

theorem aperiodic_expectation_agrees_tracial (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E A = (tracialExpectationInput P hp).E A :=
  the_expectation_is_unique (aperiodicExpectationInput P) (tracialExpectationInput P hp) A hA

theorem aperiodic_expectation_commutes_with_modular_flow (P : SiteProfile) (t : ℝ) :
    ∀ A ∈ theFactorObject P,
      modularConjugation P t ((aperiodicExpectationInput P).E A) =
        (aperiodicExpectationInput P).E (modularConjugation P t A) :=
  every_expectation_commutes_with_modular_flow (aperiodicExpectationInput P) t

/-- The response composition remains conditional on a factor-preserving covariant source. -/
theorem response_covariant_on_the_general_tower (P : SiteProfile) (h : TowerHorizon P)
    (K : (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hKmem : ∀ A ∈ theFactorObject P, K A ∈ theFactorObject P)
    (hKcov : ∀ A ∈ theFactorObject P, adT h (K A) = K (adT h A)) :
    ∀ A ∈ theFactorObject P,
      adT h ((aperiodicExpectationInput P).E (K A)) =
        (aperiodicExpectationInput P).E (K (adT h A)) := by
  intro A hA
  rw [the_lift_on_the_tower (aperiodicExpectationInput P) h (K A) (hKmem A hA),
    hKcov A hA]

#print axioms the_lift_fires_on_the_aperiodic_tower
#print axioms every_expectation_on_the_general_tower_is_covariant
#print axioms aperiodic_expectation_agrees_periodic
#print axioms aperiodic_expectation_agrees_tracial
#print axioms aperiodic_expectation_commutes_with_modular_flow
#print axioms response_covariant_on_the_general_tower

end

end ChatgptAudit.Aperiodic046
