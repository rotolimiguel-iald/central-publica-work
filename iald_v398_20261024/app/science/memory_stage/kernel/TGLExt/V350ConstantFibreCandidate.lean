import TGLExt.V350UnitIntervalShiftProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 600000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The fibre candidate is extracted by the isometric unit-interval embedding.
This definition alone does not identify B with its constant amplification. -/
def fibreCandidate (B : RegularHilbert H →L[ℂ] RegularHilbert H) : H →L[ℂ] H :=
  testEmbeddingCLM.adjoint.comp (B.comp testEmbeddingCLM)

theorem unitIntervalProjection_testVector (v : H) :
    unitIntervalProjection (testVector v) = testVector v := by
  have he := congrArg (fun T : H →L[ℂ] H => T v) (testEmbedding_adjoint_embedding (H := H))
  change testEmbeddingCLM.adjoint (testVector v) = v at he
  change testVector (testEmbeddingCLM.adjoint (testVector v)) = _
  rw [he]

theorem testEmbedding_adjoint_projection (f : RegularHilbert H) :
    testEmbeddingCLM.adjoint (unitIntervalProjection f) = testEmbeddingCLM.adjoint f := by
  have he := congrArg (fun T : H →L[ℂ] H => T (testEmbeddingCLM.adjoint f))
    (testEmbedding_adjoint_embedding (H := H))
  exact he

theorem commutation_testVector_action
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : unitIntervalProjection * B = B * unitIntervalProjection) (v : H) :
    B (testVector v) = testVector (fibreCandidate B v) := by
  have he := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T (testVector v)) hB
  change unitIntervalProjection (B (testVector v)) = B (unitIntervalProjection (testVector v)) at he
  rw [unitIntervalProjection_testVector] at he
  exact he.symm

theorem commutation_fibreCandidate_read
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : unitIntervalProjection * B = B * unitIntervalProjection)
    (f : RegularHilbert H) :
    testEmbeddingCLM.adjoint (B f) = fibreCandidate B (testEmbeddingCLM.adjoint f) := by
  have he := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T f) hB
  change unitIntervalProjection (B f) = B (unitIntervalProjection f) at he
  have hr := congrArg (testEmbeddingCLM.adjoint : RegularHilbert H →L[ℂ] H) he
  rw [testEmbedding_adjoint_projection] at hr
  exact hr

theorem dualFixedCore_testVector_action (P : TGLExt.SiteProfile)
    (B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hB : B ∈ dualFixedCore P) (v : TGLExt.TowerHilbert P) :
    B (testVector v) = testVector (fibreCandidate B v) :=
  commutation_testVector_action B (dualFixedCore_commutes_unitIntervalProjection P B hB) v

#print axioms unitIntervalProjection_testVector
#print axioms testEmbedding_adjoint_projection
#print axioms commutation_testVector_action
#print axioms commutation_fibreCandidate_read
#print axioms dualFixedCore_testVector_action
end
end TGLV350.Regular
