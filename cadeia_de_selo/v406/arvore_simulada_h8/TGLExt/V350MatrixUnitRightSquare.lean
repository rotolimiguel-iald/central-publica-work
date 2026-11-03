import TGLExt.V350HomogeneousRightSquareDomain

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Matrix
noncomputable section

theorem localEigenvalue_reverse_log (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    -Real.log (localEigenvalue P N j i) = Real.log (localEigenvalue P N i j) := by
  unfold localEigenvalue
  rw [Real.log_div (ne_of_gt (towerW_pos P N j)) (ne_of_gt (towerW_pos P N i)),
    Real.log_div (ne_of_gt (towerW_pos P N i)) (ne_of_gt (towerW_pos P N j))]
  ring

theorem modTwist_matrixUnit_reverse (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    modTwist P (Matrix.single j i 1) =
      (localEigenvalue P N i j : ℂ) • Matrix.single i j 1 := by
  change towerDeltaLevel P N (Matrix.single j i (1 : ℂ))ᴴ = _
  rw [Matrix.conjTranspose_single,star_one,deltaLevel_single]

theorem homogeneousRightGNS_smul_data {P : SiteProfile}
    (d e : HomogeneousRightData P) (c : ℂ)
    (hR : e.right = c • d.right) (hc : e.frequency = d.frequency) :
    homogeneousRightGNS e = c • homogeneousRightGNS d := by
  have ha : homogeneousRightAmbient e = c • homogeneousRightAmbient d := by
    unfold homogeneousRightAmbient
    rw [hR,hc,fibre_smul,fibre_smul,smul_mul_assoc]
  ext1 v
  apply Subtype.ext
  exact congrArg (fun T : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ] _ =>
    T v.val) ha

theorem matrixUnitTwistedRightGNS_reverse (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    homogeneousRightGNS (matrixUnitTwistedRightData P N j i) =
      (localEigenvalue P N i j : ℂ) • homogeneousRightGNS (matrixUnitRightData P N i j) := by
  apply homogeneousRightGNS_smul_data
  · change star (rTowerPi P (Matrix.single j i 1)) =
      (localEigenvalue P N i j : ℂ) • rTowerPi P (Matrix.single i j 1)
    rw [ContinuousLinearMap.star_eq_adjoint,← rTowerPi_star,
      modTwist_matrixUnit_reverse,rTowerPi_parameter_smul]
  · exact localEigenvalue_reverse_log P N i j

theorem matrixUnitRightGNS_star_reverse (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    star (homogeneousRightGNS (matrixUnitRightData P N j i)) =
      (localEigenvalue P N i j : ℂ) • homogeneousRightGNS (matrixUnitRightData P N i j) := by
  rw [matrixUnitRightGNS_adjoint,matrixUnitTwistedRightGNS_reverse]

theorem matrixUnit_rightCore_star (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    homogeneousRightCoreElement (matrixUnitRightData P N j i) =
      star (homogeneousRightCoreElement (matrixUnitRightData P N i j)) := by
  apply Subtype.ext
  change fibre (towerPi P (Matrix.single j i 1)) = star (fibre (towerPi P (Matrix.single i j 1)))
  rw [← fibre_star,ContinuousLinearMap.star_eq_adjoint,← towerPi_star,
    Matrix.conjTranspose_single,star_one]

theorem matrixUnitRight_mem_squareDomain (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (x : scalarTomitaSquareDomain P) :
    homogeneousRightGNS (matrixUnitRightData P N i j) (x : ScalarGNSHilbert P) ∈
      scalarTomitaSquareDomain P :=
  scalarRight_mem_squareDomain _ _ (matrixUnit_rightCore_star P N i j) x

def matrixUnitRightSquareInput (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (x : scalarTomitaSquareDomain P) : scalarTomitaSquareDomain P :=
  scalarRightSquareInput _ _ (matrixUnit_rightCore_star P N i j) x

/-- A R_y = (w_i/w_j) R_y A for the actual A=S†S, on every vector in D(A).
This is a local right-multiplier relation, not yet an identification of A^it. -/
theorem matrixUnit_TomitaSquare_right_scaling (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (x : scalarTomitaSquareDomain P) :
    scalarTomitaSquare P (matrixUnitRightSquareInput P N i j x) =
      (localEigenvalue P N i j : ℂ) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaSquare P x) := by
  unfold matrixUnitRightSquareInput
  rw [scalarTomitaSquare_right_intertwines,matrixUnitRightGNS_star_reverse]
  rfl

#print axioms localEigenvalue_reverse_log
#print axioms modTwist_matrixUnit_reverse
#print axioms homogeneousRightGNS_smul_data
#print axioms matrixUnitTwistedRightGNS_reverse
#print axioms matrixUnitRightGNS_star_reverse
#print axioms matrixUnit_rightCore_star
#print axioms matrixUnitRight_mem_squareDomain
#print axioms matrixUnitRightSquareInput
#print axioms matrixUnit_TomitaSquare_right_scaling
end
end TGLV350.Regular
