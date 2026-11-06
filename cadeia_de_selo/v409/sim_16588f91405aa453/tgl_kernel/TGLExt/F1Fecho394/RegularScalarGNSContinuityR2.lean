import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range

/-! Norm continuity on the original scalar GNS, proved before specializing
its Hilbert carrier. Norm closedness of the concrete double commutant is a
separate general lemma. No completeness of an algebra subtype is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.RegularScalarGNSContinuity
open TGLV350.Regular F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSAction
open F1Fecho.RegularScalarGNSRepresentation
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem representation_norm_le (D : Context H) (B : D.algebra.toStarSubalgebra) :
    ‖scalarGNSRepresentation D B‖ ≤ ‖B‖ := by
  change ‖scalarGNSAction D B‖ ≤ ‖B.val‖
  exact scalarGNSAction_norm_le D B

theorem representation_continuous (D : Context H) : Continuous (scalarGNSRepresentation D) := by
  have hb (B : D.algebra.toStarSubalgebra) : ‖scalarGNSRepresentation D B‖ ≤ 1*‖B‖ := by
    simpa only [one_mul] using representation_norm_le D B
  have hl : LipschitzWith 1 (scalarGNSRepresentation D) := by
    apply LipschitzWith.of_dist_le_mul
    intro b c
    simpa only [dist_eq_norm, ← map_sub, NNReal.coe_one] using hb (b-c)
  exact hl.continuous

theorem dual_representation_continuous : Continuous (dualOrbitRepresentation (H := H)) := by
  have hb (B : RegularHilbert H →L[ℂ] RegularHilbert H) : ‖dualOrbitRepresentation B‖ ≤ 1*‖B‖ := by
    simp only [one_mul]
    change ‖operatorFieldLift (dualIntegralFamily B)‖ ≤ (dualIntegralFamily B).bound
    exact operatorFieldLift_norm_le (dualIntegralFamily B)
  exact ((dualOrbitRepresentation (H := H)).toLinearMap.mkContinuous 1 hb).continuous

theorem algebra_norm_closed (M : VonNeumannAlgebra H) : IsClosed (M : Set (H →L[ℂ] H)) := by
  rw [← VonNeumannAlgebra.centralizer_centralizer M]
  exact Set.isClosed_centralizer _

end F1Fecho.RegularScalarGNSContinuity
#print axioms F1Fecho.RegularScalarGNSContinuity.representation_norm_le
#print axioms F1Fecho.RegularScalarGNSContinuity.representation_continuous
#print axioms F1Fecho.RegularScalarGNSContinuity.dual_representation_continuous
#print axioms F1Fecho.RegularScalarGNSContinuity.algebra_norm_closed
