import TGLExt.F1Fecho394.CanonicalFockWeightPolarR9
import TGLExt.F1Fecho394.ClosedTomitaPolarFlipR2
/-! The actual polar antiunitary exchanges the independently constructed GNS
resolvent with its complement. All inputs below have concrete constructors;
no modular flip, trace, or polar factorization is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightPolar
open TGLV350.Regular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightModularOperator
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace

theorem scalarTomitaPolar_resolvent (z : GNSHilbert) :
    scalarTomitaPolarFactor (CanonicalFockWeightModularOperator.scalarTomitaResolvent z)=
      scalarTomitaPolarFactor z-CanonicalFockWeightModularOperator.scalarTomitaResolvent (scalarTomitaPolarFactor z) :=
  ClosedTomitaOperator.polar_resolvent (H := GNSHilbert) actualClosedInput scalarTomitaPolarFactor
    scalarTomitaRootDomain_le_closed scalarTomitaPolarFactor_root
    scalarTomitaPositiveRoot_denseRange z

theorem scalarTomitaPolar_conjugate_resolvent :
    antiunitaryConjugate (H := GNSHilbert) scalarTomitaPolarFactor CanonicalFockWeightModularOperator.scalarTomitaResolvent=
      1-CanonicalFockWeightModularOperator.scalarTomitaResolvent :=
  ClosedTomitaOperator.polar_conjugate_resolvent (H := GNSHilbert) actualClosedInput scalarTomitaPolarFactor
    scalarTomitaRootDomain_le_closed scalarTomitaPolarFactor_root
    scalarTomitaPositiveRoot_denseRange
end F1Fecho.CanonicalFockWeightPolar
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_resolvent
#print axioms F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_conjugate_resolvent
