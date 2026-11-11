import TGLExt.F1Fecho394.RegularOrbitMultiplicationR1
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.F1Fecho394.CanonicalFockGNSRepresentationR6
import TGLExt.F1Fecho394.RegularScalarGNSJointContinuityR1
import TGLExt.F1Fecho394.CanonicalFockFiniteStarCoreR1
import TGLExt.V350StrongBoundedApplication
/-! Actual full-weight GNS action and simultaneous sandwich approximation,
reusing V350's proof on the same regular Fock algebra and scalar weight. -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightSandwich
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockRightAverage
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockGNSRepresentation
open scoped Topology ENNReal
def scalarWeightLeftProduct 
    (B : core.toStarSubalgebra) (A : scalarWeightLeftIdeal) :
    scalarWeightLeftIdeal :=
  ⟨B * A.val,scalarWeightLeftIdeal_left_mul B A.val A.property⟩

theorem scalarWeightOrbit_left_intertwines 
    (B : core.toStarSubalgebra) (A : scalarWeightLeftIdeal) :
    dualOrbitRepresentation B.val (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A) =
      F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightLeftProduct B A) := by
  exact F1Fecho.RegularOrbitMultiplication.apply_orbit (H := F) A.val.val B.val
    regularFockVacuum (Real.sqrt dualHaarFactor)
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A)
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarWeightLeftProduct B A))
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae A)
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae (scalarWeightLeftProduct B A))

theorem scalarWeightGNSAction_intertwines 
    (B : core.toStarSubalgebra) (A : scalarWeightLeftIdeal) :
    scalarGNSRepresentation B (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarWeightLeftProduct B A) :=
  Subtype.ext (scalarWeightOrbit_left_intertwines B A)

theorem scalarWeightGNSEmbedding_norm_sq  (A : scalarWeightLeftIdeal) :
    ENNReal.ofReal (‖scalarWeightGNSEmbedding A‖^2) =
      dualQuadraticIntegral (star A.val.val*A.val.val) (regularFockVacuum) :=
  F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_norm_sq A

theorem scalarWeightGNSEmbedding_injective  :
    Function.Injective (scalarWeightGNSEmbedding) := by
  intro A B h
  exact F1Fecho.CanonicalFockWeightOrbit.scalarWeightLinear_injective (congrArg Subtype.val h)

theorem scalarWeightGNSEmbedding_denseRange  :
    DenseRange (scalarWeightGNSEmbedding) := by
  apply (F1Fecho.CanonicalFockGNSRepresentation.scalarGNSEmbedding_denseRange).mono
  rintro _ ⟨A,rfl⟩
  exact ⟨Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight) A,
    scalarWeightGNSEmbedding_uniform A⟩

#print axioms scalarWeightLeftProduct
#print axioms scalarWeightOrbit_left_intertwines
#print axioms scalarWeightGNSAction_intertwines
#print axioms scalarWeightGNSEmbedding_norm_sq
#print axioms scalarWeightGNSEmbedding_injective
#print axioms scalarWeightGNSEmbedding_denseRange
def scalarWeightSandwich  (A : scalarWeightLeftIdeal) (h : ℝ) :
    scalarWeightLeftIdeal :=
  scalarWeightLeftProduct
    ⟨star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h),
      core.toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩
    (scalarWeightRightRegularization A h)

theorem scalarWeightSandwich_val  (A : scalarWeightLeftIdeal) (h : ℝ) :
    (scalarWeightSandwich A h).val = F1Fecho.RegularFiniteStarCore.regularSandwich fockFlow M A.val h := by
  apply Subtype.ext
  exact (mul_assoc _ _ _).symm

/-- The sandwich converges in the actual scalar GNS norm. The adjoint limit
uses the established contraction lemma, not continuity of star in SOT. -/
theorem scalarWeightGNSEmbedding_sandwich_tendsto 
    (A : scalarWeightLeftIdeal) :
    Tendsto (fun h : ℝ => scalarWeightGNSEmbedding (scalarWeightSandwich A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightGNSEmbedding A)) := by
  let T : ℝ → core.toStarSubalgebra := fun h =>
    ⟨star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h),
      core.toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩
  have hb (h : ℝ) : ‖(T h).val‖ ≤ (1 : ℝ) := by
    simpa only [T,_root_.norm_star] using F1Fecho.RegularCoreAverage.regularAverage_norm_le_one fockFlow h
  have hv : Tendsto (fun h : ℝ =>
      scalarWeightGNSEmbedding (scalarWeightRightRegularization A h))
      (𝓝[≠] 0) (𝓝 (scalarWeightGNSEmbedding A)) :=
    tendsto_subtype_rng.mpr (scalarWeightOrbit_rightRegularization_tendsto A)
  have ht := F1Fecho.RegularScalarGNSJointContinuity.representation_joint_tendsto
    (H := F) weightContext T 1 hb
    (F1Fecho.RegularFiniteStarCore.regularAverage_star_tendsto_identity fockFlow)
    (fun h => scalarWeightGNSEmbedding (scalarWeightRightRegularization A h))
    (scalarWeightGNSEmbedding A) hv
  apply ht.congr'
  exact Filter.Eventually.of_forall (fun h => scalarWeightGNSAction_intertwines (T h)
    (scalarWeightRightRegularization A h))

#print axioms scalarWeightSandwich
#print axioms scalarWeightSandwich_val
#print axioms scalarWeightGNSEmbedding_sandwich_tendsto
end F1Fecho.CanonicalFockWeightSandwich
