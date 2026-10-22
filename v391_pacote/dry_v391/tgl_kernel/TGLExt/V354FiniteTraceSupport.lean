import TGLExt.V351RegularCoreTraceConstruction
import TGLExt.InvariantProjection
import Mathlib.Analysis.VonNeumannAlgebra.Basic
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.PosPart.Basic

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351
open scoped ENNReal
noncomputable section

/-- The finite minorant is produced from the existing trace, not assumed. -/
theorem regularTrace_finite_positive_below (P : SiteProfile)
    (T : RegularCoreTraceData P) (X : PositiveCoreInput P)
    (hX : X ≠ PositiveCoreInput.zero P) :
    ∃ Y : PositiveCoreInput P, Y ≤ X ∧ 0 < T.value Y ∧ T.value Y < ⊤ := by
  by_contra h
  have hz : T.value X = 0 := by
    rw [T.semifinite X]
    apply le_antisymm
    · apply iSup_le
      intro Y
      apply iSup_le
      intro hYX
      apply iSup_le
      intro hfin
      apply le_of_eq
      by_contra hne
      exact h ⟨Y,hYX,lt_of_le_of_ne zero_le (Ne.symm hne),hfin⟩
    · exact zero_le
  exact hX ((T.faithful X).mp hz)

/-- Kernel projections stay in the same von Neumann algebra. This uses the
range-invariance criterion, without assuming a polynomial approximation. -/
theorem kernel_projection_mem_vonNeumann {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (M : VonNeumannAlgebra H) (A : H →L[ℂ] H) (hA : A ∈ M) :
    A.ker.starProjection ∈ M := by
  apply (VonNeumannAlgebra.IsStarProjection.mem_iff
    isStarProjection_starProjection M).mpr
  intro B hB
  rw [Submodule.range_starProjection]
  intro x hx
  change A (B x) = 0
  have hc := (VonNeumannAlgebra.mem_commutant_iff.mp hB) A hA
  have he := congrArg (fun T : H →L[ℂ] H => T x) hc
  change A (B x) = B (A x) at he
  rw [he, show A x = 0 from hx, map_zero]

#print axioms regularTrace_finite_positive_below
#print axioms kernel_projection_mem_vonNeumann
end
end TGLV350.Regular
