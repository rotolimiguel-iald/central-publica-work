import TGLExt.F1Fecho394.ClosedTomitaFlowR1
import TGLExt.F1Fecho394.CanonicalFockWeightModularOperatorR3
/-! Actual CFC imaginary powers of the scalar-weight Tomita square. The input
closed involution is constructed, not supplied by a modular-flow field.
The equality with regular conjugation and the trace law remain separate. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.CanonicalFockWeightModularFlow
open TGLExt TGLV350.Regular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightModularOperator
abbrev scalarTomitaImaginaryPower :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower actualClosedInput

theorem scalarTomitaImaginaryPower_damping (t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower t (resolventDampingOperator (H := GNSHilbert) scalarTomitaResolvent x)=
      resolventPhaseOperator (H := GNSHilbert) scalarTomitaResolvent t x :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_damping actualClosedInput t x

theorem scalarTomitaImaginaryPower_unique (t : ℝ) (U : GNSHilbert →L[ℂ] GNSHilbert)
    (hU : ∀ x, U (resolventDampingOperator (H := GNSHilbert) scalarTomitaResolvent x)=
      resolventPhaseOperator (H := GNSHilbert) scalarTomitaResolvent t x) (x : GNSHilbert) :
    U x=scalarTomitaImaginaryPower t x :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_unique actualClosedInput t U hU x

theorem scalarTomitaImaginaryPower_zero (x : GNSHilbert) :
    scalarTomitaImaginaryPower 0 x=x :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_zero actualClosedInput x

theorem scalarTomitaImaginaryPower_add (s t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower s (scalarTomitaImaginaryPower t x)=
      scalarTomitaImaginaryPower (s+t) x :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_add actualClosedInput s t x

theorem scalarTomitaImaginaryPower_strongly_continuous (x : GNSHilbert) :
    Continuous (fun t : ℝ => scalarTomitaImaginaryPower t x) :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_strongly_continuous actualClosedInput x

theorem scalarTomitaImaginaryPower_inverse (t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower (-t) (scalarTomitaImaginaryPower t x)=x :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaImaginaryPower_inverse actualClosedInput t x
end F1Fecho.CanonicalFockWeightModularFlow
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_damping
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_unique
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_zero
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_add
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_strongly_continuous
#print axioms F1Fecho.CanonicalFockWeightModularFlow.scalarTomitaImaginaryPower_inverse
