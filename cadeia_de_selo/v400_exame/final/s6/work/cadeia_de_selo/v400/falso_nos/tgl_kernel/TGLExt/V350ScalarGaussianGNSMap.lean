import TGLExt.V350ScalarGaussianVacuum
import TGLExt.V350L2PositiveMultiplier

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

/-- An injective contraction from the original H_I to its existing L² ambient
space. It does not assert that Gaussian multiplication preserves H_I. -/
def scalarGaussianGNSMap (P : SiteProfile) : ScalarGNSHilbert P →L[ℂ]
    RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  (realScalarMultiplier gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one).comp
      (scalarGNSSubspace P).subtypeL

theorem scalarGaussianGNSMap_norm_le (P : SiteProfile) (v : ScalarGNSHilbert P) :
    ‖scalarGaussianGNSMap P v‖ ≤ ‖v‖ :=
  realScalarMultiplier_norm_le gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one v.val

theorem scalarGaussianGNSMap_injective (P : SiteProfile) :
    Function.Injective (scalarGaussianGNSMap P) := by
  intro v w h
  apply Subtype.ext
  exact realScalarMultiplier_injective gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one gaussianProfile_pos h

theorem scalarGaussianGNSMap_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    scalarGaussianGNSMap P (scalarGNSRepresentation P B v) =
      dualOrbitRepresentation B.val (scalarGaussianGNSMap P v) := by
  exact congrArg (fun T => T v.val)
    (realScalarMultiplier_commutes_field gaussianProfile gaussianProfile_continuous
      (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (dualIntegralFamily B.val))

/-- The transport sends the original finite-ideal GNS vectors to the orbit of
the auxiliary separating vector, with exactly the same Haar coefficient. -/
theorem scalarGaussianGNSMap_embedding (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarGaussianGNSMap P (scalarGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarGaussianVacuum P) := by
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarGNSOrbit P A),
    scalarGNSOrbit_ae P A,scalarGaussianVacuum_ae P,
    operatorFieldLift_ae (dualIntegralFamily A.val.val) (scalarGaussianVacuum P)]
    with s h1 h2 h3 h4
  change realScalarMultiplier gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarGNSOrbit P A) s =
    operatorFieldLift (dualIntegralFamily A.val.val) (scalarGaussianVacuum P) s
  rw [h1,h2,h4,h3]
  change (gaussianProfile s : ℂ) •
    ((Real.sqrt dualHaarFactor : ℂ) • dualAmbient s A.val.val (regularVacuum P)) =
    dualAmbient s A.val.val ((gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • regularVacuum P))
  rw [map_smul,map_smul]

#print axioms scalarGaussianGNSMap
#print axioms scalarGaussianGNSMap_norm_le
#print axioms scalarGaussianGNSMap_injective
#print axioms scalarGaussianGNSMap_intertwines
#print axioms scalarGaussianGNSMap_embedding
end
end TGLV350.Regular
