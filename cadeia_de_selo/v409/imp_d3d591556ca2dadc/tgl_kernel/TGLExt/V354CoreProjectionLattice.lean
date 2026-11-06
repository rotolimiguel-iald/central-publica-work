import TGLExt.V354RegularSupport
import TGLExt.SusyRelativeGap
import Mathlib.Order.Sublattice
import Mathlib.Analysis.CStarAlgebra.Projection

set_option autoImplicit false

namespace TGLV354
open TGLExt TGLV350.Regular TGLV351
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- All closed subspaces whose orthogonal projections belong to N. -/
def coreProjectionSpaces (N : VonNeumannAlgebra H) : Sublattice (ClosedSubmodule ℂ H) where
  carrier := {S | ∀ B ∈ N.commutant, S ≤ S.comap B}
  supClosed' := by
    intro S hS T hT B hB
    apply sup_le
    · intro x hx
      exact (le_sup_left : S ≤ S ⊔ T) (hS B hB hx)
    · intro x hx
      exact (le_sup_right : T ≤ S ⊔ T) (hT B hB hx)
  infClosed' := by
    intro S hS T hT B hB x hx
    exact ⟨hS B hB hx.1, hT B hB hx.2⟩

abbrev CoreProjection (N : VonNeumannAlgebra H) : Type := coreProjectionSpaces N

instance (N : VonNeumannAlgebra H) : BoundedOrder (CoreProjection N) where
  top := ⟨⊤, by intro B hB; exact le_top⟩
  bot := ⟨⊥, by intro B hB; exact bot_le⟩
  le_top _ := le_top (α := ClosedSubmodule ℂ H)
  bot_le _ := bot_le (α := ClosedSubmodule ℂ H)

/-- The concrete orthogonal projection, not a numeric stand-in. -/
def CoreProjection.operator {N : VonNeumannAlgebra H} (p : CoreProjection N) : H →L[ℂ] H :=
  p.val.toSubmodule.starProjection

theorem CoreProjection.operator_mem {N : VonNeumannAlgebra H} (p : CoreProjection N) :
    p.operator ∈ N := by
  apply (VonNeumannAlgebra.IsStarProjection.mem_iff isStarProjection_starProjection N).mpr
  intro B hB
  rw [Submodule.range_starProjection]
  exact p.property B hB

theorem CoreProjection.operator_le_iff {N : VonNeumannAlgebra H} (p q : CoreProjection N) :
    p.operator ≤ q.operator ↔ p ≤ q := by
  rw [(show IsStarProjection p.operator from isStarProjection_starProjection).le_iff_mul_eq_right
    (show IsStarProjection q.operator from isStarProjection_starProjection)]
  constructor
  · intro h x hx
    apply Submodule.starProjection_eq_self_iff.mp
    have hp : p.operator x = x := Submodule.starProjection_eq_self_iff.mpr hx
    change q.operator x=x
    simpa only [ContinuousLinearMap.mul_apply, hp] using congrArg (fun A : H →L[ℂ] H => A x) h
  · intro h
    ext x
    exact Submodule.starProjection_eq_self_iff.mpr
      (h (Submodule.starProjection_apply_mem _ x))

/-- Every actual projection in N is represented, so the lattice is the full projection lattice. -/
def CoreProjection.ofOperator (N : VonNeumannAlgebra H) (e : H →L[ℂ] H)
    (he : IsStarProjection e) (hm : e ∈ N) : CoreProjection N :=
  ⟨⟨e.range,ContinuousLinearMap.IsIdempotentElem.isClosed_range he.isIdempotentElem⟩,
    (VonNeumannAlgebra.IsStarProjection.mem_iff he N).mp hm⟩

theorem CoreProjection.operator_ofOperator (N : VonNeumannAlgebra H) (e : H →L[ℂ] H)
    (he : IsStarProjection e) (hm : e ∈ N) :
    (CoreProjection.ofOperator N e he hm).operator = e := by
  obtain ⟨hp,hh⟩ := isStarProjection_iff_eq_starProjection_range.mp he
  exact hh.symm

@[simp] theorem CoreProjection.operator_bot (N : VonNeumannAlgebra H) :
    (⊥ : CoreProjection N).operator=0 := Submodule.starProjection_bot

theorem CoreProjection.sup_apply_eq_zero {N : VonNeumannAlgebra H}
    (p q : CoreProjection N) (x : H) (hp : p.operator x=0) (hq : q.operator x=0) :
    (p ⊔ q).operator x=0 := by
  apply (Submodule.starProjection_apply_eq_zero_iff _).mpr
  change x ∈ (p.val.toSubmodule ⊔ q.val.toSubmodule).topologicalClosureᗮ
  rw [Submodule.orthogonal_closure,← Submodule.inf_orthogonal]
  exact ⟨(Submodule.starProjection_apply_eq_zero_iff _).mp hp,
    (Submodule.starProjection_apply_eq_zero_iff _).mp hq⟩

def CoreProjection.positive (P : SiteProfile) (p : CoreProjection (regularCoreAlgebra P)) :
    PositiveCoreInput P := ⟨p.operator,p.operator_mem,
      (show IsStarProjection p.operator from isStarProjection_starProjection).nonneg⟩

/-- A1 restricted to every actual projection of the same regular core. -/
def coreProjectionTrace (P : SiteProfile) :
    SemifiniteTraceData (CoreProjection (regularCoreAlgebra P)) where
  tau p := scalarInverseLimitWeight P (p.positive P)
  mono := fun {p q} h => scalarInverseLimitWeight_mono P _ _
    ((CoreProjection.operator_le_iff p q).mpr h)
  faithful := by
    intro p hp
    have hz := congrArg Subtype.val ((scalarInverseLimitWeight_faithful P _).mp hp)
    change p.operator = 0 at hz
    apply bot_unique
    intro x hx
    have hh : p.operator x = x := Submodule.starProjection_eq_self_iff.mpr hx
    rw [hz, ContinuousLinearMap.zero_apply] at hh
    exact hh.symm

#print axioms coreProjectionSpaces
#print axioms CoreProjection.operator_mem
#print axioms CoreProjection.operator_le_iff
#print axioms CoreProjection.operator_ofOperator
#print axioms coreProjectionTrace
end
end TGLV354
