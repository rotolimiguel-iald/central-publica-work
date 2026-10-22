import LocalCentralizerExpectation
import ExpectationContractGap
import SiteModularInvariance

set_option autoImplicit false
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem global_expectation_restricts_to_pinching (F : ExpectationInput P) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    F.E (towerPi P a) = towerPi P (specExpect (towerW P N) a) := by
  let L : LocalCentralizerInput P N := {
    E := fun a => F.E (towerPi P a)
    into := fun a => F.into _ (towerPi_mem_factor a)
    fixes := fun a ha => F.fixes _ ha
    ortho := fun a b hb => F.ortho _ (towerPi_mem_factor a) b hb }
  exact local_input_unique N L a

theorem global_expectation_differs_from_floor (F : ExpectationInput P)
    (hp : P.w 0 ≠ 1/2) (N : ℕ) :
    ¬ (∀ x ∈ theFactorObject P, F.E x = towerExpectation P N x) := by
  intro h
  exact expectation_not_imported_contract hp N ⟨F,h⟩

theorem shifted_range_invariant
    (theta : (TowerHilbert P →L[ℂ] TowerHilbert P) →
      (TowerHilbert P →L[ℂ] TowerHilbert P))
    (himage : theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) =
      (chainTailClosure P 1 : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) (t : ℝ) :
    modularConjugation P t ''
      (theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) =
      theta '' (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  rw [himage]
  exact tail_flow_image t 1

#print axioms global_expectation_restricts_to_pinching
#print axioms global_expectation_differs_from_floor
#print axioms shifted_range_invariant
end
end ChatgptAudit
