import TGLExt.F1Fecho394.CanonicalFockRightRootR10
import TGLExt.F1Fecho394.CanonicalFockWeightPolarR9
import TGLExt.F1Fecho394.CanonicalFockPolarRightAlgebraR6

/-! The actual polar conjugation exchanges regular left and right multiplication. Uses the dense range of the proved positive root, not an input right-action identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockRightPolar
local instance : CompleteSpace F1Fecho.CanonicalFockGNS.GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (F1Fecho.CanonicalFockGNS.GNSHilbert →L[ℂ] F1Fecho.CanonicalFockGNS.GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugate_apply)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open scoped Topology
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightClosedTomita
open F1Fecho.CanonicalFockRightTomita F1Fecho.CanonicalFockWeightPolar
open F1Fecho.CanonicalFockPolarRight
open F1Fecho.CanonicalFockRightRoot (scalarRegularRightRootInput scalarTomitaPositiveRoot_regular_right_commutes)
/-- The actual polar antiunitary exchanges this right action with left
multiplication. The extension uses the dense image of the SAME positive root. -/
theorem scalarTomitaPolarFactor_regular_right  (t : ℝ)
    (z : GNSHilbert) :
    scalarTomitaPolarFactor (regularRightGNS t z) =
      scalarGNSRepresentation (star (regularRightCoreElement t))
        (scalarTomitaPolarFactor z) := by
  refine (scalarTomitaPositiveRoot_denseRange).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) z
  rintro _ ⟨x,rfl⟩
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed)
      (scalarRegularRightRootInput t x) =
    scalarRegularRightClosedTomitaInput t
      (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x) := Subtype.ext rfl
  calc
    _ = scalarTomitaPolarFactor
        (scalarTomitaPositiveRoot (scalarRegularRightRootInput t x)) :=
      congrArg (scalarTomitaPolarFactor) (scalarTomitaPositiveRoot_regular_right_commutes t x).symm
    _ = closedTomita (Submodule.inclusion (scalarTomitaRootDomain_le_closed)
        (scalarRegularRightRootInput t x)) := scalarTomitaPolarFactor_root _
    _ = closedTomita (scalarRegularRightClosedTomitaInput t
        (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x)) :=
      congrArg (closedTomita) he
    _ = scalarGNSRepresentation (star (regularRightCoreElement t))
        (closedTomita (Submodule.inclusion (scalarTomitaRootDomain_le_closed) x)) :=
      scalarClosedTomita_regular_right_intertwines t _
    _ = _ := congrArg (scalarGNSRepresentation (star (regularRightCoreElement t)))
      (scalarTomitaPolarFactor_root x).symm

theorem scalarTomitaPolar_conjugate_regular_right  (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) (scalarTomitaPolarFactor) (regularRightGNS t) =
      scalarGNSRepresentation (star (regularRightCoreElement t)) := by
  apply ContinuousLinearMap.ext
  intro x
  have h := scalarTomitaPolarFactor_regular_right t ((scalarTomitaPolarFactor).symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply] using h

theorem scalarTomitaPolarFactor_regular_left  (t : ℝ)
    (z : GNSHilbert) :
    scalarTomitaPolarFactor
      (scalarGNSRepresentation (star (regularRightCoreElement t)) z) =
        regularRightGNS t (scalarTomitaPolarFactor z) := by
  have h := congrArg (scalarTomitaPolarFactor)
    (scalarTomitaPolarFactor_regular_right t (scalarTomitaPolarFactor z))
  simpa only [scalarTomitaPolarFactor_involutive z,
    scalarTomitaPolarFactor_involutive (regularRightGNS t (scalarTomitaPolarFactor z))] using h.symm

/-- The previously constructed right translation is the original polar right
action on every vector in the full scalar-weight ideal. -/
theorem scalarRightAction_regular  (t : ℝ)
    (A : scalarWeightLeftIdeal) :
    scalarWeightGNSEmbedding (scalarRegularRightProduct t A) =
      antiunitaryConjugate (H := GNSHilbert) (scalarTomitaPolarFactor)
        (scalarGNSRepresentation (star (regularRightCoreElement t)))
          (scalarWeightGNSEmbedding A) := by
  have h := scalarTomitaPolarFactor_regular_left t
    (scalarTomitaPolarFactor.symm (scalarWeightGNSEmbedding A))
  have hi := congrArg (regularRightGNS t)
    (scalarTomitaPolarFactor.apply_symm_apply (scalarWeightGNSEmbedding A))
  calc
    _ = regularRightGNS t (scalarWeightGNSEmbedding A) :=
      (regularRightGNS_intertwines t A).symm
    _ = scalarTomitaPolarFactor (scalarGNSRepresentation (star (regularRightCoreElement t))
        (scalarTomitaPolarFactor.symm (scalarWeightGNSEmbedding A))) := (h.trans hi).symm
    _ = _ := rfl

theorem scalarPolarRightAlgebra_regular_mem (t : ℝ) :
    regularRightCoreElement t ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor := by
  have h (s : ℝ) : ScalarPolarRight scalarTomitaPolarFactor (regularRightCoreElement s) := by
    intro A
    exact ⟨(scalarRegularRightProduct s A).property,scalarRightAction_regular s A⟩
  apply (scalarPolarRightAlgebra_mem_iff scalarTomitaPolarFactor (regularRightCoreElement t)).mpr
  refine ⟨h t,?_⟩
  simpa only [regularRightCoreElement_star] using h (-t)
end F1Fecho.CanonicalFockRightPolar
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_right
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right
#print axioms F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_left
#print axioms F1Fecho.CanonicalFockRightPolar.scalarRightAction_regular
#print axioms F1Fecho.CanonicalFockRightPolar.scalarPolarRightAlgebra_regular_mem
