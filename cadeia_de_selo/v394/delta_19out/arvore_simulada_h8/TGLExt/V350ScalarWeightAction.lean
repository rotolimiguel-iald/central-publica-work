import TGLExt.V350ScalarWeightCompletion
import TGLExt.V350ScalarGNSRepresentation
import TGLExt.V350DualOrbitStrongLimits
import TGLExt.V350StrongBoundedApplication

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

def scalarWeightLeftProduct (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : scalarWeightLeftIdeal P) :
    scalarWeightLeftIdeal P :=
  ⟨B * A.val,scalarWeightLeftIdeal_left_mul P B A.val A.property⟩

theorem scalarWeightOrbit_left_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : scalarWeightLeftIdeal P) :
    dualOrbitRepresentation B.val (scalarWeightOrbit P A) =
      scalarWeightOrbit P (scalarWeightLeftProduct P B A) := by
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily B.val) (scalarWeightOrbit P A),
    scalarWeightOrbit_ae P A,scalarWeightOrbit_ae P (scalarWeightLeftProduct P B A)]
    with s h1 h2 h3
  change operatorFieldLift (dualIntegralFamily B.val) (scalarWeightOrbit P A) s = _
  rw [h1,h3]
  change dualAmbient s B.val (scalarWeightOrbit P A s) = _
  rw [h2]
  change dualAmbient s B.val ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient s A.val.val (regularVacuum P)) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s (B.val*A.val.val) (regularVacuum P)
  rw [map_smul,map_mul]
  rfl

theorem scalarWeightGNSAction_intertwines (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (A : scalarWeightLeftIdeal P) :
    scalarGNSRepresentation P B (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B A) :=
  Subtype.ext (scalarWeightOrbit_left_intertwines P B A)

theorem scalarWeightGNSEmbedding_norm_sq (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ENNReal.ofReal (‖scalarWeightGNSEmbedding P A‖^2) =
      dualQuadraticIntegral (star A.val.val*A.val.val) (regularVacuum P) :=
  scalarWeightOrbit_norm_sq P A

theorem scalarWeightGNSEmbedding_injective (P : SiteProfile) :
    Function.Injective (scalarWeightGNSEmbedding P) := by
  intro A B h
  exact scalarWeightLinear_injective P (congrArg Subtype.val h)

theorem scalarWeightGNSEmbedding_denseRange (P : SiteProfile) :
    DenseRange (scalarWeightGNSEmbedding P) := by
  apply (scalarGNSEmbedding_denseRange P).mono
  rintro _ ⟨A,rfl⟩
  exact ⟨Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A,
    scalarWeightGNSEmbedding_uniform P A⟩

#print axioms scalarWeightLeftProduct
#print axioms scalarWeightOrbit_left_intertwines
#print axioms scalarWeightGNSAction_intertwines
#print axioms scalarWeightGNSEmbedding_norm_sq
#print axioms scalarWeightGNSEmbedding_injective
#print axioms scalarWeightGNSEmbedding_denseRange
end
end TGLV350.Regular
