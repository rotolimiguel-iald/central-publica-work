import TGLExt.F1Fecho394.CanonicalFockGNSRepresentationR6
import TGLExt.F1Fecho394.CanonicalFockWeightCompletionR5
import TGLExt.V350ScalarGNSCutMaps
import TGLExt.V350ScalarCutVacuum

/-! Actual cut maps for the existing concrete Fock GNS completion.
Reuses the v393 cut proofs. No new GNS space, state or modular identity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSCuts
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
/-- A contraction from the actual scalar GNS completion into its ambient L² space.
Its identification with the bounded cut functional is a separate norm theorem. -/
def scalarGNSCutMap (R : ℝ) :
    GNSHilbert →L[ℂ] RegularHilbert (RegularHilbert F) :=
  (measurableCut (Set.Ioc (-R) R) measurableSet_Ioc).comp (GNSSubspace).subtypeL

theorem scalarGNSCutMap_norm_le (R : ℝ) (v : GNSHilbert) :
    ‖scalarGNSCutMap  R v‖ ≤ ‖v‖ :=
  measurableCutLp_norm_le (Set.Ioc (-R) R) measurableSet_Ioc v.val

theorem scalarGNSCutMap_intertwines (R : ℝ)
    (B : core.toStarSubalgebra) (v : GNSHilbert) :
    scalarGNSCutMap  R (scalarGNSRepresentation  B v) =
      dualOrbitRepresentation B.val (scalarGNSCutMap  R v) :=
  measurableCut_operatorFieldLift (Set.Ioc (-R) R) measurableSet_Ioc
    (dualIntegralFamily B.val) v.val

theorem scalarGNSCutMap_joint_zero (v : GNSHilbert)
    (h : ∀ n : ℕ, scalarGNSCutMap  (n : ℝ) v = 0) : v = 0 := by
  apply Subtype.ext
  exact measurableCut_nat_joint_zero v.val h


/-- A finite-interval vector in the existing ambient L² space. It is not normalized
to a state and no separating property is included in its definition. -/
def scalarCutVacuum (R : ℝ) :
    RegularHilbert (RegularHilbert F) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    indicatorConstLp 2 (measurableSet_Ioc (a := -R) (b := R)) (by simp) (regularFockVacuum)

theorem scalarCutVacuum_ae (R : ℝ) :
    (scalarCutVacuum  R : ℝ → RegularHilbert F) =ᵐ[volume]
      (Set.Ioc (-R) R).indicator (fun _ => (Real.sqrt dualHaarFactor : ℝ) • regularFockVacuum) := by
  let f : RegularHilbert (RegularHilbert F) :=
    indicatorConstLp 2 (measurableSet_Ioc (a := -R) (b := R)) (by simp) (regularFockVacuum)
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ) f,
    indicatorConstLp_coeFn (p := (2 : ENNReal))
      (hs := measurableSet_Ioc (a := -R) (b := R)) (hμs := by simp) (c := regularFockVacuum)]
    with x h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • f) x = _
  simp only [Pi.smul_apply] at h1
  rw [h1,show f x = _ from h2]
  by_cases hx : x ∈ Set.Ioc (-R) R <;> simp [hx]


end F1Fecho.CanonicalFockGNSCuts
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarGNSCutMap
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarGNSCutMap_norm_le
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarGNSCutMap_intertwines
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarGNSCutMap_joint_zero
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarCutVacuum
#print axioms F1Fecho.CanonicalFockGNSCuts.scalarCutVacuum_ae
