import TGLExt.V350ScalarDualWeight
import TGLExt.V350CoreContractCounterexample

set_option autoImplicit false
set_option maxHeartbeats 1000000

universe u

namespace TGLV351
open TGLExt TGLV350.Regular
open scoped ENNReal NNReal
noncomputable section

/-- The existing positive cone, acted on by the existing regular dual action. -/
def positiveDual (P : SiteProfile) (s : ℝ) (A : PositiveCoreInput P) :
    PositiveCoreInput P :=
  ⟨(regularDualAction P s ⟨A.val, A.property.1⟩).val,
    (regularDualAction P s ⟨A.val, A.property.1⟩).property,
    dualAmbient_nonneg s A.val A.property.2⟩

def positiveSquare (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) : PositiveCoreInput P :=
  ⟨star a.val * a.val, (regularCoreAlgebra P).mul_mem
    ((regularCoreAlgebra P).toStarSubalgebra.star_mem' a.property) a.property,
    star_mul_self_nonneg a.val⟩

def positiveUnit (P : SiteProfile) : PositiveCoreInput P :=
  ⟨1, (regularCoreAlgebra P).one_mem, zero_le_one⟩

theorem positiveUnit_ne_zero (P : SiteProfile) :
    positiveUnit P ≠ PositiveCoreInput.zero P := by
  intro h
  have hv := congrArg (fun A : PositiveCoreInput P => A.val (regularVacuum P)) h
  have hz : regularVacuum P = 0 := by simpa [positiveUnit, PositiveCoreInput.zero] using hv
  have hn := regularVacuum_norm P
  rw [hz, norm_zero] at hn
  norm_num at hn

/-- A strengthened target on the actual regular core. Semifiniteness is expressed
by finite positive minorants, not by a name or an arbitrary dense subspace.
This does not assert an inhabitant, a canonical normalization, or a legacy bridge.
The remaining construction must select the perturbation of scalarDualWeight. -/
structure RegularCoreTraceData (P : SiteProfile) where
  value : PositiveCoreInput P → ℝ≥0∞
  zero : value (PositiveCoreInput.zero P) = 0
  additive : ∀ A B, value (A.add B) = value A + value B
  homogeneous : ∀ (r : ℝ≥0) A, value (A.scale r) = (r : ℝ≥0∞) * value A
  monotone : ∀ A B, A ≤ B → value A ≤ value B
  faithful : ∀ A, value A = 0 ↔ A = PositiveCoreInput.zero P
  normal : ∀ {ι : Type u} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (_hmono : Monotone A) (hS : IsLUB (Set.range A) S),
    value ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, value ⟨(A i).val, (A i).property, hpos i⟩
  semifinite : ∀ A, value A =
    ⨆ (B : PositiveCoreInput P) (_ : B ≤ A) (_ : value B < ⊤), value B
  tracial : ∀ a, value (positiveSquare P a) = value (positiveSquare P (star a))
  dual_scaling : ∀ s A, value (positiveDual P s A) =
    ENNReal.ofReal (Real.exp (-s)) * value A

theorem RegularCoreTraceData.not_zero (P : SiteProfile)
    (T : RegularCoreTraceData.{u} P) : T.value ≠ fun _ => 0 := by
  intro h
  have hz : T.value (positiveUnit P) = 0 := congrFun h _
  exact positiveUnit_ne_zero P ((T.faithful _).mp hz)

/-- Any proposed transport of the legacy zero trace still fails. No identification
of the legacy algebra with the concrete core is presumed. -/
theorem legacy_zero_trace_cannot_supply (P : SiteProfile)
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (D : TGL.ModularRealization.WedgeModularData W)
    (f : PositiveCoreInput P → (TGLV350.ContractAudit.zeroTraceLegacyCore W D).Core) :
    ¬ ∃ T : RegularCoreTraceData.{u} P,
      T.value = (TGLV350.ContractAudit.zeroTraceLegacyCore W D).canonicalTrace ∘ f := by
  rintro ⟨T, h⟩
  exact T.not_zero P h

/-- Reuse the dual-weight theorem, applied on the same positive cone. -/
theorem scalarDualWeight_dual_invariant (P : SiteProfile) (s : ℝ)
    (A : PositiveCoreInput P) :
    scalarDualWeight P (positiveDual P s A) = scalarDualWeight P A :=
  dualQuadraticIntegral_dual_invariant s A.val (regularVacuum P)

def positiveAverageSquare (P : SiteProfile) : PositiveCoreInput P :=
  positiveSquare P ⟨regularAverage P 1, regularAverage_mem P 1⟩

/-- An exact finite witness, using the already proved Plancherel calculation. -/
theorem scalarDualWeight_averageSquare (P : SiteProfile) :
    scalarDualWeight P (positiveAverageSquare P) = 1 := by
  change dualQuadraticIntegral (star (regularAverage P 1) * regularAverage P 1)
    (regularVacuum P) = 1
  rw [regularAverage_dualQuadraticIntegral P 1 (by norm_num), regularVacuum_norm]
  norm_num

/-- The current dual weight cannot be the trace required in A1. This is a wall
against renaming an existing provider, not against existence of the canonical trace. -/
theorem scalarDualWeight_not_trace_provider (P : SiteProfile) :
    ¬ ∃ T : RegularCoreTraceData.{u} P, T.value = scalarDualWeight P := by
  rintro ⟨T, h⟩
  have hs := T.dual_scaling 1 (positiveAverageSquare P)
  rw [h, scalarDualWeight_dual_invariant, scalarDualWeight_averageSquare, mul_one] at hs
  have he : ENNReal.ofReal (Real.exp (-1)) < (1 : ℝ≥0∞) := by
    rw [ENNReal.ofReal_lt_one]
    have h : Real.exp (-1) < Real.exp 0 := Real.exp_lt_exp.mpr (by norm_num)
    simp only [Real.exp_zero] at h
    exact h
  exact (ne_of_lt he) hs.symm

#print axioms positiveDual
#print axioms positiveSquare
#print axioms positiveUnit
#print axioms positiveUnit_ne_zero
#print axioms RegularCoreTraceData
#print axioms RegularCoreTraceData.not_zero
#print axioms legacy_zero_trace_cannot_supply
#print axioms scalarDualWeight_dual_invariant
#print axioms positiveAverageSquare
#print axioms scalarDualWeight_averageSquare
#print axioms scalarDualWeight_not_trace_provider
end
end TGLV351
