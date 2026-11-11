import TGLExt.F1Fecho394.RegularScalarGNSActionR2
import TGLExt.V350DualOrbitRepresentation
/-! A definitional bridge between the existing two names for the same
ambient dual representation, before specializing the large concrete Fock. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.RegularDualGNSAction
open TGLV350.Regular F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSAction
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem ambient_eq (D : Context H) (A : D.algebra.toStarSubalgebra) :
    scalarGNSAmbientAction D A=dualOrbitRepresentation A.val := rfl
theorem dual_preserves (D : Context H)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A∈D.algebra)
    (v : RegularHilbert (RegularHilbert H)) (hv : v∈GNSSubspace D) :
    dualOrbitRepresentation A v∈GNSSubspace D :=
  scalarGNSAmbientAction_preserves D ⟨A,hA⟩ v hv
end F1Fecho.RegularDualGNSAction
#print axioms F1Fecho.RegularDualGNSAction.ambient_eq
#print axioms F1Fecho.RegularDualGNSAction.dual_preserves
