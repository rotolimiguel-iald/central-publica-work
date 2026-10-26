import TGLExt.GlobalLiftLadder
import TGLExt.CornerFamily
import TGLExt.V351RegularCoreTraceConstruction

set_option autoImplicit false

universe u

namespace TGLV351
open TGLExt TGLV350.Regular
noncomputable section

/-- The finite-trace part of the positive regular core. The full trace is
ENNReal-valued, so a real-valued `DualScalingData.tau` must use this domain. -/
def FiniteTracePositive (P : SiteProfile) : Type :=
  {A : PositiveCoreInput P // (scalarInverseLimitTraceData.{u} P).value A < ⊤}

def finiteTraceDual (P : SiteProfile) (s : ℝ)
    (A : FiniteTracePositive.{u} P) : FiniteTracePositive.{u} P := by
  refine ⟨positiveDual P s A.val, ?_⟩
  rw [(scalarInverseLimitTraceData.{u} P).dual_scaling]
  exact ENNReal.mul_lt_top (by simp) A.property

/-- The existing v351 trace and dual action supply the legacy real-valued
scaling interface on the finite-trace positive cone. -/
def regularCoreDualScalingData (P : SiteProfile) :
    DualScalingData (FiniteTracePositive.{u} P) where
  tau A := ((scalarInverseLimitTraceData.{u} P).value A.val).toReal
  theta s A := finiteTraceDual.{u} P s A
  scaling s A := by
    change ((scalarInverseLimitTraceData.{u} P).value
      (positiveDual P s A.val)).toReal =
        Real.exp (-s) * ((scalarInverseLimitTraceData.{u} P).value A.val).toReal
    rw [(scalarInverseLimitTraceData.{u} P).dual_scaling]
    exact ENNReal.toReal_ofReal_mul _ _ (le_of_lt (Real.exp_pos _))

/-- Existing obstruction now applies to the actual finite-trace positive core. -/
theorem finiteTracePositive_not_fixed (P : SiteProfile) (s : ℝ) (hs : 0 < s)
    (A : FiniteTracePositive.{u} P)
    (hA : A.val ≠ PositiveCoreInput.zero P) :
    finiteTraceDual.{u} P s A ≠ A := by
  apply (regularCoreDualScalingData.{u} P).finite_trace_not_fixed hs
  change ((scalarInverseLimitTraceData.{u} P).value A.val).toReal ≠ 0
  have hweight : (scalarInverseLimitTraceData.{u} P).value A.val ≠ 0 := by
    intro hz
    exact hA (((scalarInverseLimitTraceData.{u} P).faithful A.val).mp hz)
  exact ne_of_gt (ENNReal.toReal_pos hweight (ne_of_lt A.property))

#print axioms regularCoreDualScalingData
#print axioms finiteTracePositive_not_fixed

end
end TGLV351
