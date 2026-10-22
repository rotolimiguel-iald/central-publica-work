import TGLExt.F1Fecho394.RegularScalarGaussianR1
import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
import TGLExt.V350L2PositiveMultiplier
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarGaussianGNS
open TGLV350.Regular MeasureTheory F1Fecho.RegularScalarGNS
open F1Fecho.RegularScalarGNSRepresentation F1Fecho.RegularScalarGaussian
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
noncomputable section

/-- An injective contraction from the original H_I to its existing L² ambient
space. It does not assert that Gaussian multiplication preserves H_I. -/
def scalarGaussianGNSMap (D : Context H) : GNSHilbert D →L[ℂ]
    RegularHilbert (RegularHilbert H) :=
  (realScalarMultiplier gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one).comp
      (GNSSubspace D).subtypeL

theorem scalarGaussianGNSMap_norm_le (D : Context H) (v : GNSHilbert D) :
    ‖scalarGaussianGNSMap D v‖ ≤ ‖v‖ :=
  realScalarMultiplier_norm_le gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one v.val

theorem scalarGaussianGNSMap_injective (D : Context H) :
    Function.Injective (scalarGaussianGNSMap D) := by
  intro v w h
  apply Subtype.ext
  exact realScalarMultiplier_injective gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one gaussianProfile_pos h

theorem scalarGaussianGNSMap_intertwines (D : Context H)
    (B : D.algebra.toStarSubalgebra) (v : GNSHilbert D) :
    scalarGaussianGNSMap D (scalarGNSRepresentation D B v) =
      dualOrbitRepresentation B.val (scalarGaussianGNSMap D v) := by
  exact congrArg (fun T => T v.val)
    (realScalarMultiplier_commutes_field gaussianProfile gaussianProfile_continuous
      (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (dualIntegralFamily B.val))

/-- The transport sends the original finite-ideal GNS vectors to the orbit of
the auxiliary separating vector, with exactly the same Haar coefficient. -/
theorem scalarGaussianGNSMap_embedding (D : Context H) (A : finiteIdeal D) :
    scalarGaussianGNSMap D (GNSEmbedding D A) =
      dualOrbitRepresentation A.val.val (scalarGaussianVacuum D) := by
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarGNSOrbit D A),
    scalarGNSOrbit_ae D A,scalarGaussianVacuum_ae D,
    operatorFieldLift_ae (dualIntegralFamily A.val.val) (scalarGaussianVacuum D)]
    with s h1 h2 h3 h4
  change realScalarMultiplier gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarGNSOrbit D A) s =
    operatorFieldLift (dualIntegralFamily A.val.val) (scalarGaussianVacuum D) s
  rw [h1,h2,h4,h3]
  change (gaussianProfile s : ℂ) •
    ((Real.sqrt dualHaarFactor : ℂ) • dualAmbient s A.val.val D.vacuum) =
    dualAmbient s A.val.val ((gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • D.vacuum))
  rw [map_smul,map_smul]

#print axioms scalarGaussianGNSMap
#print axioms scalarGaussianGNSMap_norm_le
#print axioms scalarGaussianGNSMap_injective
#print axioms scalarGaussianGNSMap_intertwines
#print axioms scalarGaussianGNSMap_embedding
end
end F1Fecho.RegularScalarGaussianGNS
