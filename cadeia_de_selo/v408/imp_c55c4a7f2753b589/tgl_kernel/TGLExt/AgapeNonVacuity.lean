import TGLExt.V351DualScalingBridge
import TGLExt.Fundacao

/-!
F1.2 completion against the current Nos kernel.
The finite-trace bridge is reproduced byte-for-byte in this sandbox.
The matrix-crossed-product construction is not asserted here.
-/

set_option autoImplicit false

universe u

namespace F12Completion
open TGLExt TGLV351 TGLV350.Regular
open scoped ENNReal
noncomputable section

/-- Semifiniteness and faithfulness make the finite-trace positive cone
non-vacuous in the strong sense needed by the foundation clause. -/
theorem finiteTracePositive_has_positive (P : SiteProfile) :
    ∃ A : FiniteTracePositive.{u} P,
      0 < (regularCoreDualScalingData.{u} P).tau A := by
  have hu : (scalarInverseLimitTraceData.{u} P).value (positiveUnit P) ≠ 0 := fun h =>
    positiveUnit_ne_zero P (((scalarInverseLimitTraceData.{u} P).faithful _).mp h)
  by_contra hcon
  simp only [not_exists, not_lt] at hcon
  apply hu
  rw [(scalarInverseLimitTraceData.{u} P).semifinite (positiveUnit P)]
  refine le_antisymm ?_ zero_le
  refine iSup_le fun B => iSup_le fun _ => iSup_le fun hfin => ?_
  have h1 := hcon ⟨B, hfin⟩
  change ((scalarInverseLimitTraceData.{u} P).value B).toReal ≤ 0 at h1
  have h2 : ((scalarInverseLimitTraceData.{u} P).value B).toReal = 0 :=
    le_antisymm h1 ENNReal.toReal_nonneg
  rcases (ENNReal.toReal_eq_zero_iff _).mp h2 with h3 | h3
  · exact le_of_eq h3
  · exact absurd h3 (ne_of_lt hfin)

/-- Apply the foundation's Agape clause to the actual v351 scaling term,
using a witness with strictly positive finite trace. -/
theorem agape_on_v351_core (P : SiteProfile) :
    ∃ A : FiniteTracePositive.{u} P,
      0 < (regularCoreDualScalingData.{u} P).tau A ∧
      ((∀ s : ℝ, s ≠ 0 → ∀ m' : FiniteTracePositive.{u} P,
          (regularCoreDualScalingData.{u} P).theta s m' = m' →
            (regularCoreDualScalingData.{u} P).tau m' = 0) ∧
       (∀ s : ℝ, (regularCoreDualScalingData.{u} P).tau
            ((regularCoreDualScalingData.{u} P).theta s A) <
          (regularCoreDualScalingData.{u} P).tau
            ((regularCoreDualScalingData.{u} P).theta (s - 1) A)) ∧
       (∀ B : ℝ, ∃ s : ℝ, B < (regularCoreDualScalingData.{u} P).tau
            ((regularCoreDualScalingData.{u} P).theta s A)) ∧
       (∀ s : ℝ, 0 < (regularCoreDualScalingData.{u} P).tau
            ((regularCoreDualScalingData.{u} P).theta s A)) ∧
       (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, (regularCoreDualScalingData.{u} P).tau
            ((regularCoreDualScalingData.{u} P).theta s A) < ε) ∧
       (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0)) := by
  obtain ⟨A, hA⟩ := finiteTracePositive_has_positive.{u} P
  exact ⟨A, hA, TGLExt.Fundacao.agape (regularCoreDualScalingData.{u} P) hA⟩

#print axioms finiteTracePositive_has_positive
#print axioms agape_on_v351_core

end
end F12Completion
