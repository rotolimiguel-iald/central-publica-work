import TGLExt.V350MatrixUnitRootScaling
import TGLExt.V350ScalarTomitaPolarInvolution

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous049 ChatgptAudit
noncomputable section

theorem antiunitary_ofReal_smul {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (U : H ≃ₛₗᵢ[starRingEnd ℂ] H) (r : ℝ) (x : H) :
    U ((r : ℂ) • x) = (r : ℂ) • U x := by
  rw [map_smulₛₗ]
  simp

/-- The actual J of S exchanges a homogeneous right matrix unit with its
weighted left adjoint. Equality is extended from the dense image of B. -/
theorem matrixUnit_polar_right_weighted (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (z : ScalarGNSHilbert P) :
    (Real.sqrt (localEigenvalue P N i j) : ℂ) •
      scalarTomitaPolarFactor P (homogeneousRightGNS (matrixUnitRightData P N i j) z) =
    scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
      (scalarTomitaPolarFactor P z) := by
  refine (scalarTomitaPositiveRoot_denseRange P).induction ?_
    (isClosed_eq (((scalarTomitaPolarFactor P).continuous.comp
      (homogeneousRightGNS (matrixUnitRightData P N i j)).continuous).const_smul
        (Real.sqrt (localEigenvalue P N i j) : ℂ))
      ((scalarGNSRepresentation P
        (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))).continuous.comp
          (scalarTomitaPolarFactor P).continuous)) z
  rintro _ ⟨x,rfl⟩
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
      (matrixUnitRightRootInput P N i j x) =
    scalarRightClosedTomitaInput (matrixUnitRightData P N i j)
      (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x) := Subtype.ext rfl
  calc
    _ = scalarTomitaPolarFactor P
        ((Real.sqrt (localEigenvalue P N i j) : ℂ) •
          homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPositiveRoot P x)) :=
      (antiunitary_ofReal_smul (scalarTomitaPolarFactor P) _ _).symm
    _ = scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P (matrixUnitRightRootInput P N i j x)) :=
      congrArg (scalarTomitaPolarFactor P) (matrixUnit_positiveRoot_right_scaling P N i j x).symm
    _ = scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
        (matrixUnitRightRootInput P N i j x)) := scalarTomitaPolarFactor_root P _
    _ = scalarClosedTomita P (scalarRightClosedTomitaInput (matrixUnitRightData P N i j)
        (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)) := congrArg (scalarClosedTomita P) he
    _ = scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
        (scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) x)) :=
      scalarClosedTomita_right_intertwines _ _
    _ = _ := congrArg (scalarGNSRepresentation P
      (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))))
        (scalarTomitaPolarFactor_root P x).symm

theorem matrixUnit_polar_left_weighted (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))) z) =
    (Real.sqrt (localEigenvalue P N i j) : ℂ) •
      homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPolarFactor P z) := by
  have hh := congrArg (scalarTomitaPolarFactor P)
    (matrixUnit_polar_right_weighted P N i j (scalarTomitaPolarFactor P z))
  simpa only [antiunitary_ofReal_smul,
    scalarTomitaPolarFactor_involutive P z,
    scalarTomitaPolarFactor_involutive P
      (homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPolarFactor P z))] using hh.symm

theorem matrixUnit_polar_conjugate_left (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))) =
    (Real.sqrt (localEigenvalue P N i j) : ℂ) • homogeneousRightGNS (matrixUnitRightData P N i j) := by
  apply ContinuousLinearMap.ext
  intro z
  have hh := matrixUnit_polar_left_weighted P N i j ((scalarTomitaPolarFactor P).symm z)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply,
    smul_apply] using hh

#print axioms antiunitary_ofReal_smul
#print axioms matrixUnit_polar_right_weighted
#print axioms matrixUnit_polar_left_weighted
#print axioms matrixUnit_polar_conjugate_left
end
end TGLV350.Regular
