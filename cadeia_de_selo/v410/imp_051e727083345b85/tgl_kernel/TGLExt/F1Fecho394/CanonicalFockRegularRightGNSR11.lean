import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.F1Fecho394.RegularRightOrbitPointwiseR1
import TGLExt.F1Fecho394.ClosedSubmoduleRestrictionR2

set_option autoImplicit false
set_option maxErrors 2
set_option synthInstance.maxHeartbeats 1000000
set_option linter.unusedSectionVars false
set_option maxHeartbeats 600000

namespace F1Fecho.CanonicalFockRegularRightGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockRightAverage F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockWeightInvariance
noncomputable section
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) := F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace

def regularRightCoreElement (t : ℝ) :
    (core).toStarSubalgebra :=
  ⟨regularUnitary t,regular_mem t⟩

theorem regularRightCoreElement_star (t : ℝ) :
    star (regularRightCoreElement t) = regularRightCoreElement (-t) :=
  Subtype.ext (F1Fecho.RegularCovariantCore.regular_star fockFlow t)

theorem scalarWeight_right_regular_eq
    (A : (core).toStarSubalgebra) (t : ℝ) :
    TGLV350.Regular.dualQuadraticIntegral (star (A.val * regularUnitary t) *
      (A.val * regularUnitary t)) (regularFockVacuum) =
    TGLV350.Regular.dualQuadraticIntegral (star A.val * A.val) (regularFockVacuum) :=
  F1Fecho.RegularRightAction.weight_right_regular fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A t

def scalarRegularRightProduct
    (t : ℝ) (A : scalarWeightLeftIdeal) : scalarWeightLeftIdeal :=
  ⟨A.val * regularRightCoreElement t,by
    change TGLV350.Regular.dualQuadraticIntegral (star (A.val.val * regularUnitary t) *
      (A.val.val * regularUnitary t)) (regularFockVacuum) < ⊤
    rw [scalarWeight_right_regular_eq]
    exact A.property⟩

/-- The character acts on the outer coordinate and TGLV350.Regular.shift on the inner coordinate. -/

def regularRightAmbient (t : ℝ) :
    TGLV350.Regular.RegularHilbert (TGLV350.Regular.RegularHilbert (F)) →L[ℂ]
      TGLV350.Regular.RegularHilbert (TGLV350.Regular.RegularHilbert (F)) :=
  F1Fecho.RegularRightAction.ambient (H:=F) t

theorem characterPhase_comm (s t : ℝ) : TGLV350.Regular.characterPhase s t = TGLV350.Regular.characterPhase t s := by
  unfold TGLV350.Regular.characterPhase
  congr 1
  ring

theorem regularRightAmbient_zero : regularRightAmbient 0 = 1 := F1Fecho.RegularRightAction.ambient_zero

theorem regularRightAmbient_mul (s t : ℝ) :
    regularRightAmbient s * regularRightAmbient t = regularRightAmbient (s+t) :=
  F1Fecho.RegularRightAction.ambient_mul s t

theorem regularRightAmbient_star (t : ℝ) :
    star (regularRightAmbient t) = regularRightAmbient (-t) :=
  F1Fecho.RegularRightAction.ambient_star t

theorem scalarRegularRightOrbit_intertwines
    (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularRightAmbient t (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A) =
      F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarRegularRightProduct t A) := by
  apply Lp.ext
  filter_upwards [F1Fecho.RegularRightAction.ambient_ae t
      (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A),
    F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae A,
    F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_ae (scalarRegularRightProduct t A)]
    with s h1 h2 h3
  apply h1.trans
  calc
    TGLV350.Regular.characterPhase t s • TGLV350.Regular.shift t
        (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit A s) =
      TGLV350.Regular.characterPhase t s • TGLV350.Regular.shift t
        ((Real.sqrt TGLV350.Regular.dualHaarFactor : ℝ) •
          TGLV350.Regular.dualAmbient s A.val.val regularFockVacuum) :=
      congrArg (fun v => TGLV350.Regular.characterPhase t s • TGLV350.Regular.shift t v) h2
    _ = (Real.sqrt TGLV350.Regular.dualHaarFactor : ℝ) •
        TGLV350.Regular.dualAmbient s (A.val.val * regularUnitary t) regularFockVacuum :=
      F1Fecho.RegularRightAction.ambient_orbit_pointwise t s _ _ _
        (F1Fecho.CanonicalFockRightAverage.scalarOrbit_right_regular A.val s t)
    _ = F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit (scalarRegularRightProduct t A) s := h3.symm

theorem regularRightAmbient_preserves_GNS (t : ℝ) :
    ∀ v ∈ GNSSubspace, regularRightAmbient t v ∈ GNSSubspace := by
  apply F1Fecho.ClosedSubmoduleRestriction.closure_range_preserved scalarGNSLinear (regularRightAmbient t)
  intro A
  let B := Submodule.inclusion finiteDualLeftIdeal_le_scalarWeight A
  have hi := scalarRegularRightOrbit_intertwines t B
  have he := congrArg (regularRightAmbient t)
    (F1Fecho.CanonicalFockWeightOrbit.scalarWeightOrbit_uniform A)
  have ht := he.symm.trans hi
  change regularRightAmbient t (scalarGNSOrbit A) ∈ GNSSubspace
  exact Eq.mpr (congrArg (fun v => v∈GNSSubspace) ht)
    (scalarWeightOrbit_mem_original_GNS (scalarRegularRightProduct t B))



def regularRightGNS (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  (regularRightAmbient t).restrict (regularRightAmbient_preserves_GNS t)

theorem regularRightGNS_intertwines (t : ℝ) (A : scalarWeightLeftIdeal) :
    regularRightGNS t (scalarWeightGNSEmbedding A) =
      scalarWeightGNSEmbedding (scalarRegularRightProduct t A) :=
  Subtype.ext (scalarRegularRightOrbit_intertwines t A)

theorem regularRightGNS_zero : regularRightGNS 0 = 1 := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_zero)

theorem regularRightGNS_mul (s t : ℝ) :
    regularRightGNS s * regularRightGNS t = regularRightGNS (s+t) := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_mul s t)

theorem regularRightGNS_star (t : ℝ) :
    star (regularRightGNS t) = regularRightGNS (-t) := by
  exact F1Fecho.ClosedSubmoduleRestriction.adjoint_restrict GNSSubspace
    (regularRightAmbient t) (regularRightAmbient (-t))
    (regularRightAmbient_preserves_GNS t) (regularRightAmbient_preserves_GNS (-t))
    (regularRightAmbient_star t)

theorem regularRightGNS_unitary (t : ℝ) :
    star (regularRightGNS t) * regularRightGNS t = 1 ∧
      regularRightGNS t * star (regularRightGNS t) = 1 := by
  simp [regularRightGNS_star,regularRightGNS_mul,regularRightGNS_zero]

#print axioms regularRightCoreElement
#print axioms regularRightCoreElement_star
#print axioms scalarWeight_right_regular_eq
#print axioms scalarRegularRightProduct
#print axioms regularRightAmbient
#print axioms characterPhase_comm
#print axioms regularRightAmbient_zero
#print axioms regularRightAmbient_mul
#print axioms regularRightAmbient_star
#print axioms scalarRegularRightOrbit_intertwines
#print axioms regularRightAmbient_preserves_GNS
#print axioms regularRightGNS
#print axioms regularRightGNS_intertwines
#print axioms regularRightGNS_zero
#print axioms regularRightGNS_mul
#print axioms regularRightGNS_star
#print axioms regularRightGNS_unitary
end
end F1Fecho.CanonicalFockRegularRightGNS
