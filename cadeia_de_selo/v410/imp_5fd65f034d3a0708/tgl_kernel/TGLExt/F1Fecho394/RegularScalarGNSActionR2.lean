import TGLExt.F1Fecho394.RegularScalarGNSR3
import TGLExt.V350StrongOperatorField
/-! Concrete left GNS action of the SAME Fock core. The ambient multiplier
is the actual dual orbit. Its restriction is proved to preserve the completion
of the orbit range, and intertwines actual left multiplication. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.RegularScalarGNSAction
open TGLV350.Regular MeasureTheory F1Fecho.RegularScalarGNS
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)

def scalarGNSLeftProduct 
    (B : D.algebra.toStarSubalgebra) (A : finiteIdeal D) :
    finiteIdeal D :=
  ⟨B * A.val,HasFiniteDualSquare.left_mul B.val A.val.val A.property⟩

/-- The ambient left action uses the same dual orbit at every coordinate.
Restriction to the completed GNS range is a separate step. -/
def scalarGNSAmbientAction 
    (B : D.algebra.toStarSubalgebra) :
    RegularHilbert (RegularHilbert H) →L[ℂ]
      RegularHilbert (RegularHilbert H) :=
  operatorFieldLift (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_norm_le 
    (B : D.algebra.toStarSubalgebra) :
    ‖scalarGNSAmbientAction D B‖ ≤ ‖B.val‖ :=
  operatorFieldLift_norm_le (dualIntegralFamily B.val)

theorem scalarGNSAmbientAction_intertwines 
    (B : D.algebra.toStarSubalgebra) (A : finiteIdeal D) :
    scalarGNSAmbientAction D B (scalarGNSOrbit D A) =
      scalarGNSOrbit D (scalarGNSLeftProduct D B A) := by
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B.val) (scalarGNSOrbit D A),
    scalarGNSOrbit_ae D A,scalarGNSOrbit_ae D (scalarGNSLeftProduct D B A)]
    with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily B.val) (scalarGNSOrbit D A) s = _
  rw [h1,h3]
  change dualAmbient s B.val (scalarGNSOrbit D A s) = _
  rw [h2]
  change dualAmbient s B.val ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient s A.val.val D.vacuum) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s (B.val*A.val.val) D.vacuum
  rw [map_smul,map_mul]
  rfl

theorem scalarGNSAmbientAction_preserves 
    (B : D.algebra.toStarSubalgebra) :
    ∀ v ∈ GNSSubspace D, scalarGNSAmbientAction D B v ∈ GNSSubspace D := by
  have h : Set.MapsTo (scalarGNSAmbientAction D B)
      ((scalarGNSLinear D).range : Set _) ((scalarGNSLinear D).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarGNSLeftProduct D B A, (scalarGNSAmbientAction_intertwines D B A).symm⟩
  exact h.closure (scalarGNSAmbientAction D B).continuous

def scalarGNSAction  (B : D.algebra.toStarSubalgebra) :
    GNSHilbert D →L[ℂ] GNSHilbert D :=
  (scalarGNSAmbientAction D B).restrict (scalarGNSAmbientAction_preserves D B)

theorem scalarGNSAction_apply 
    (B : D.algebra.toStarSubalgebra) (v : GNSHilbert D) :
    (scalarGNSAction D B v).val = scalarGNSAmbientAction D B v.val := rfl

theorem scalarGNSAction_norm_le 
    (B : D.algebra.toStarSubalgebra) : ‖scalarGNSAction D B‖ ≤ ‖B.val‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro v
  exact (scalarGNSAmbientAction D B).le_of_opNorm_le
    (scalarGNSAmbientAction_norm_le D B) v.val

theorem scalarGNSAction_intertwines 
    (B : D.algebra.toStarSubalgebra) (A : finiteIdeal D) :
    scalarGNSAction D B (GNSEmbedding D A) =
      GNSEmbedding D (scalarGNSLeftProduct D B A) := by
  apply Subtype.ext
  exact scalarGNSAmbientAction_intertwines D B A


end F1Fecho.RegularScalarGNSAction
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSLeftProduct
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction_norm_le
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction_intertwines
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction_preserves
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAction_apply
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAction_norm_le
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAction_intertwines
#print axioms F1Fecho.RegularScalarGNSAction.scalarGNSAction
