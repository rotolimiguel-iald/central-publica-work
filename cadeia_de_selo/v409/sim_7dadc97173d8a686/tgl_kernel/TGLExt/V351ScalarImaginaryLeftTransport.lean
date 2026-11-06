import TGLExt.V351ScalarImaginaryRightTransport
import TGLExt.V351ScalarTomitaImaginaryConjugation
import TGLExt.V350MatrixUnitPolarTransport

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- The same polar antiunitary transports right scaling to the left adjoint
generator. Its antilinearity conjugates the scalar phase. -/
theorem matrixUnit_imaginaryPower_left_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))) x) =
      star (modularPhase t (Real.log (localEigenvalue P N i j))) •
        scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
          (scalarTomitaImaginaryPower P t x) := by
  apply (scalarTomitaPolarFactor P).injective
  rw [scalarTomitaImaginaryPower_polar_commutes,
    matrixUnit_polar_left_weighted, map_smul,
    matrixUnit_imaginaryPower_right_scaling, map_smulₛₗ]
  simp only [starRingEnd_apply, star_star, matrixUnit_polar_left_weighted,
    scalarTomitaImaginaryPower_polar_commutes]
  exact smul_comm _ _ _

/-- The left regular generator commutes with the original imaginary powers,
using the already constructed right transport and the same J. -/
theorem scalarTomitaImaginaryPower_regular_left_commutes (P : SiteProfile)
    (s t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P (star (regularRightCoreElement P s)) x) =
      scalarGNSRepresentation P (star (regularRightCoreElement P s))
        (scalarTomitaImaginaryPower P t x) := by
  apply (scalarTomitaPolarFactor P).injective
  rw [scalarTomitaImaginaryPower_polar_commutes,
    scalarTomitaPolarFactor_regular_left,
    scalarTomitaImaginaryPower_regular_right_commutes,
    scalarTomitaPolarFactor_regular_left,
    scalarTomitaImaginaryPower_polar_commutes]

#print axioms matrixUnit_imaginaryPower_left_scaling
#print axioms scalarTomitaImaginaryPower_regular_left_commutes
end
end TGLV350.Regular
