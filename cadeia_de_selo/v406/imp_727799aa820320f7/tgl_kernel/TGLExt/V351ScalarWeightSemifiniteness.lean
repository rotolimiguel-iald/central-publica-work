import TGLExt.V351ExtendedBaseDualWeight
import TGLExt.V350ScalarWeightDomain

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

namespace TGLV351
open TGLExt TGLV350.Regular Filter
open scoped ENNReal Topology
noncomputable section

/-- The square-finite domain of the actual scalar weight is WOT dense in
the same regular core. This is the usual semifiniteness criterion for a
normal weight; it is not a claim about finite positive minorants of each input. -/
theorem scalarWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P} := by
  apply Set.Subset.antisymm
  · exact closure_minimal (fun A hA => hA.1) (regularCore_wot_closed P)
  · intro A hA
    obtain ⟨hf, hm, ht⟩ := scalarDualWeight_square_finite_strong_density P ⟨A.toCLM, hA⟩
    have hw := strong_tendsto_wot
      (fun h : ℝ => A.toCLM * regularAverage P h) A.toCLM ht
    apply mem_closure_of_tendsto hw
    filter_upwards [self_mem_nhdsWithin] with h hh
    exact ⟨hm h, hf h hh⟩

/-- Semifiniteness does not mean that the unit itself has finite weight. -/
theorem scalarWeight_unit_not_square_finite (P : SiteProfile) :
    ¬ HasFiniteScalarSquare P
      (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) := by
  intro h
  have hi := baseDualWeight_unit_infinite P (hOmega P) (by
    intro hz
    have hn := regularVacuum_norm P
    change ‖testVector (hOmega P)‖ = 1 at hn
    rw [testVector_norm, hz, norm_zero] at hn
    norm_num at hn)
  change dualQuadraticIntegral 1 (regularVacuum P) = ⊤ at hi
  have hf : dualQuadraticIntegral 1 (regularVacuum P) < ⊤ := by
    simpa only [HasFiniteScalarSquare, star_one, one_mul] using h
  rw [hi] at hf
  exact (lt_irrefl _) hf

#print axioms scalarWeight_square_finite_wot_closure
#print axioms scalarWeight_unit_not_square_finite
end
end TGLV351
