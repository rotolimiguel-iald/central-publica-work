import AperiodicVectorAverage
import AperiodicAveragePrefix
import TracialCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Filter
open scoped Topology

noncomputable section

/-- Choose the constructed strong limit on the factor; the contract ignores values outside it. -/
def aperiodicExpectation (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P := by
  classical
  exact if hA : A ∈ theFactorObject P then
    Classical.choose (aperiodic_average_operator P A hA)
  else 0

/-- Membership, norm bound, and strong convergence are proved by the operator construction. -/
theorem aperiodic_expectation_spec (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    aperiodicExpectation P A ∈ theFactorObject P ∧
      ‖aperiodicExpectation P A‖ ≤ ‖A‖ ∧
      ∀ v, Tendsto
        (fun n : ℕ => periodAverage P ((n : ℝ) + 1) (by positivity) A v)
        atTop (𝓝 (aperiodicExpectation P A v)) := by
  simpa only [aperiodicExpectation, dif_pos hA] using
    Classical.choose_spec (aperiodic_average_operator P A hA)

/-- The selected limit has the local pinching as every finite prefix. -/
theorem aperiodic_expectation_prefix (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    towerExpectation P N (aperiodicExpectation P A) =
      towerPi P (specExpect (towerW P N) (expectationMatrix P N A)) :=
  aperiodic_average_prefix_of_limit P N A (aperiodicExpectation P A)
    ((aperiodic_expectation_spec P A hA).2.2 (hOmega P))

/-- The limit lies in the global centralizer, without a common local phase period. -/
theorem aperiodic_expectation_into (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    aperiodicExpectation P A ∈ omegaCentralizer P := by
  apply centralizer_from_expectations _ (aperiodic_expectation_spec P A hA).1
  intro N
  rw [aperiodic_expectation_prefix P N A hA]
  exact pinching_into_global_centralizer _ _

/-- Every element of the centralizer is fixed by the constructed map. -/
theorem aperiodic_expectation_fixes (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ omegaCentralizer P) :
    aperiodicExpectation P A = A := by
  have he (N : ℕ) :
      towerExpectation P N (aperiodicExpectation P A) = towerExpectation P N A := by
    rw [aperiodic_expectation_prefix P N A hA.1,
      pinching_fixes_global_local N _
        (expectation_of_centralizer_is_centralizer N A hA)]
    rfl
  apply factor_eq_of_omega (aperiodic_expectation_spec P A hA.1).1 hA.1
  have ht := expectation_omega_limit (aperiodicExpectation P A)
  simp only [he] at ht
  exact tendsto_nhds_unique ht (expectation_omega_limit A)

/-- The finite pinching orthogonalities pass to the GNS limit. -/
theorem aperiodic_expectation_ortho (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ omegaCentralizer P) :
    omegaState P (star B * (A - aperiodicExpectation P A)) = 0 := by
  have hn (N : ℕ) : inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P)) = 0 := by
    have h := pinching_global_ortho N (expectationMatrix P N A)
      (towerExpectation P N B) (expectation_of_centralizer_is_centralizer N B hB)
    rw [omega_product_inner, star_star] at h
    rw [aperiodic_expectation_prefix P N A hA]
    exact h
  have ht : Tendsto (fun N => inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P)))
      atTop (𝓝 (inner ℂ (B (hOmega P))
        (A (hOmega P) - aperiodicExpectation P A (hOmega P)))) :=
    (expectation_omega_limit B).inner
      ((expectation_omega_limit A).sub
        (expectation_omega_limit (aperiodicExpectation P A)))
  have he : (fun N => inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P))) =
      (fun _ : ℕ => (0 : ℂ)) := funext hn
  rw [he] at ht
  have hz := tendsto_nhds_unique ht tendsto_const_nhds
  rw [omega_product_inner, star_star]
  exact hz

/-- A constructed inhabitant for every admissible profile, including aperiodic ones. -/
def aperiodicExpectationInput (P : SiteProfile) : ExpectationInput P where
  E := aperiodicExpectation P
  into := aperiodic_expectation_into P
  fixes := aperiodic_expectation_fixes P
  ortho := fun A hA B hB => aperiodic_expectation_ortho P A B hA hB

theorem aperiodic_contract_inhabited (P : SiteProfile) : Nonempty (ExpectationInput P) :=
  ⟨aperiodicExpectationInput P⟩

theorem aperiodic_expectation_contractive (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖(aperiodicExpectationInput P).E A‖ ≤ ‖A‖ :=
  (aperiodic_expectation_spec P A hA).2.1

theorem aperiodic_expectation_idempotent (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E ((aperiodicExpectationInput P).E A) =
      (aperiodicExpectationInput P).E A :=
  (aperiodicExpectationInput P).fixes _ ((aperiodicExpectationInput P).into A hA)

#print axioms aperiodicExpectation
#print axioms aperiodic_expectation_spec
#print axioms aperiodic_expectation_prefix
#print axioms aperiodic_expectation_into
#print axioms aperiodic_expectation_fixes
#print axioms aperiodic_expectation_ortho
#print axioms aperiodicExpectationInput
#print axioms aperiodic_contract_inhabited
#print axioms aperiodic_expectation_contractive
#print axioms aperiodic_expectation_idempotent

end

end ChatgptAudit.Aperiodic046
