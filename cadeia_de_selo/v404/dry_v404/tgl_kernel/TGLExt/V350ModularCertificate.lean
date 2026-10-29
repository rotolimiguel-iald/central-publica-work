import TGLExt.V350TowerDuality

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLExt
open TGLV350
noncomputable section

/-- An inhabitant of the precise converse contract, with no commutation premise. -/
def qgConverse_JMJ_contains_commutant (P : SiteProfile) : ConverseClauseContract P where
  inclusion := right_commutant_subset_left_bicommutant P

/-- The original tower conjugation now satisfies both directions of duality. -/
def qgFrontier_modularRealization : ModularRealizationCertificate := by
  have hc := (contract_iff_the_eighth_clause mixProfile).mp
    ⟨qgConverse_JMJ_contains_commutant mixProfile⟩
  have h := certificate_modulo_commutation hc
  refine {
    J := towerJ mixProfile
    add := h.1
    conj_smul := h.2.1
    isometric := h.2.2.1
    involutive := h.2.2.2.1
    fixes_vacuum := h.2.2.2.2.1
    maps_factor_to_commutant := ?_
    onto_commutant := ?_
  }
  · intro T hT
    refine ⟨conjByJ mixProfile T, h.2.2.2.2.2.1 ⟨T, hT, rfl⟩, ?_⟩
    intro v
    rfl
  · intro S hS
    obtain ⟨T, hT, he⟩ := h.2.2.2.2.2.2 hS
    refine ⟨T, hT, ?_⟩
    intro v
    change conjByJ mixProfile T v = S v
    rw [he]

/-- The Act III debt consumes the same closed certificate; no second model is introduced. -/
def qgPrice_towerActIII_inhabitantConstructed : ModularRealizationCertificate :=
  qgFrontier_modularRealization

/-- Type-checking bridge consumed by the extended gate. -/
def checkedV350ModularRealization : ModularRealizationCertificate :=
  qgFrontier_modularRealization

#print axioms qgConverse_JMJ_contains_commutant
#print axioms qgFrontier_modularRealization
#print axioms qgPrice_towerActIII_inhabitantConstructed
#print axioms checkedV350ModularRealization

end
end TGLExt
