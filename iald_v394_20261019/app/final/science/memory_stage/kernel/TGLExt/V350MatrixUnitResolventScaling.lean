import TGLExt.V350MatrixUnitRightSquare
import TGLExt.V350ScaledPositiveResolvent
import TGLExt.V350ScalarTomitaResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Matrix
noncomputable section

/-- The full-domain relation for A=S†S gives T R D=R T,
where T=(I+A)⁻¹ and D=rI+(1-r)T. -/
theorem matrixUnit_resolvent_denominator_identity (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) :
    scalarTomitaResolvent P * homogeneousRightGNS (matrixUnitRightData P N i j) *
      scaledResolventDenominator (scalarTomitaResolvent P) (localEigenvalue P N i j) =
    homogeneousRightGNS (matrixUnitRightData P N i j) * scalarTomitaResolvent P := by
  apply ContinuousLinearMap.ext
  intro z
  obtain ⟨x,hx,he⟩ := scalarTomitaResolvent_equation P z
  have hc : homogeneousRightGNS (matrixUnitRightData P N i j)
      (scaledResolventDenominator (scalarTomitaResolvent P) (localEigenvalue P N i j) z) =
      (matrixUnitRightSquareInput P N i j x : ScalarGNSHilbert P) +
        scalarTomitaSquare P (matrixUnitRightSquareInput P N i j x) := by
    rw [matrixUnit_TomitaSquare_right_scaling]
    change homogeneousRightGNS (matrixUnitRightData P N i j)
      ((localEigenvalue P N i j : ℂ) • z +
        ((1-localEigenvalue P N i j : ℝ) : ℂ) • scalarTomitaResolvent P z) =
      homogeneousRightGNS (matrixUnitRightData P N i j) (x : ScalarGNSHilbert P) + _
    rw [← hx,← he]
    simp only [Complex.ofReal_sub,Complex.ofReal_one,smul_add,sub_smul,one_smul,map_add,map_sub,map_smul]
    abel
  change scalarTomitaResolvent P
    (homogeneousRightGNS (matrixUnitRightData P N i j)
      (scaledResolventDenominator (scalarTomitaResolvent P) (localEigenvalue P N i j) z)) = _
  rw [hc,scalarTomitaResolvent_inverse]
  exact congrArg (homogeneousRightGNS (matrixUnitRightData P N i j)) hx

theorem matrixUnit_resolvent_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) :
    scalarTomitaResolvent P * homogeneousRightGNS (matrixUnitRightData P N i j) =
      homogeneousRightGNS (matrixUnitRightData P N i j) *
        scaledPositiveResolvent (scalarTomitaResolvent P) (localEigenvalue P N i j) := by
  have hd := scaledResolventDenominator_positive (scalarTomitaResolvent P)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (localEigenvalue P N i j) (localEigenvalue_pos (P := P) N i j)
  have h := (Ring.eq_mul_inverse_iff_mul_eq
    (scalarTomitaResolvent P * homogeneousRightGNS (matrixUnitRightData P N i j))
    (homogeneousRightGNS (matrixUnitRightData P N i j) * scalarTomitaResolvent P)
    (scaledResolventDenominator (scalarTomitaResolvent P) (localEigenvalue P N i j)) hd.isUnit).mpr
      (matrixUnit_resolvent_denominator_identity P N i j)
  simpa only [scaledPositiveResolvent,mul_assoc] using h

#print axioms matrixUnit_resolvent_denominator_identity
#print axioms matrixUnit_resolvent_right_scaling
end
end TGLV350.Regular
