import TGLExt.V351ImaginaryPowerScaling
import TGLExt.V351ScalarTomitaImaginaryPowers
import TGLExt.V350MatrixUnitResolventScaling
import TGLExt.V350ScalarRegularRightPolar

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- The modular frequency is transported to the actual imaginary powers of S†S. -/
theorem matrixUnit_imaginaryPower_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x) :=
  resolventImaginaryPower_scaled_intertwining (scalarTomitaResolvent P)
    (homogeneousRightGNS (matrixUnitRightData P N i j))
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
    (localEigenvalue P N i j) (localEigenvalue_pos (P := P) N i j)
    (matrixUnit_resolvent_right_scaling P N i j) t x

/-- The right regular group commutes with these same imaginary powers. -/
theorem scalarTomitaImaginaryPower_regular_right_commutes (P : SiteProfile) (s t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (regularRightGNS P s x)=
      regularRightGNS P s (scalarTomitaImaginaryPower P t x) :=
  resolventImaginaryPower_intertwines (scalarTomitaResolvent P) (scalarTomitaResolvent P)
    (regularRightGNS P s)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_complement_injective P)
    (scalarTomitaResolvent_regular_right_commutes P s).eq t x

#print axioms matrixUnit_imaginaryPower_right_scaling
#print axioms scalarTomitaImaginaryPower_regular_right_commutes
end
end TGLV350.Regular
