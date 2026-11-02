import TGLExt.V350LocalRightModularTransport
import TGLExt.V350HomogeneousCommutantTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- Explicit data for one homogeneous right multiplier. The local instances
below discharge these fields from the existing tower; KMS is not a field. -/
structure HomogeneousRightData (P : SiteProfile) where
  right : TowerHilbert P →L[ℂ] TowerHilbert P
  left : TowerHilbert P →L[ℂ] TowerHilbert P
  frequency : ℝ
  right_mem : right ∈ (theFactorObject P).commutant
  left_mem : left ∈ theFactorObject P
  homogeneous : ∀ t : ℝ, modularConjugation P t right = modularPhase t frequency • right
  vacuum : left (hOmega P) = right (hOmega P)

theorem modularPhase_star_frequency (t c : ℝ) :
    star (modularPhase t c) = modularPhase t (-c) := by
  unfold modularPhase
  change (starRingEnd ℂ) (Complex.exp _) = _
  rw [← Complex.exp_conj]
  congr 1
  simp only [map_mul,Complex.conj_ofReal,Complex.conj_I,mul_neg,Complex.ofReal_neg,neg_mul]

theorem homogeneous_base_adjoint (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (c : ℝ)
    (he : ∀ t : ℝ, modularConjugation P t D = modularPhase t c • D) (t : ℝ) :
    modularConjugation P t (star D) = modularPhase t (-c) • star D := by
  rw [map_star,he,star_smul,modularPhase_star_frequency]

def homogeneousRightAmbient {P : SiteProfile} (d : HomogeneousRightData P) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  fibre (fibre d.right) * shift d.frequency

theorem homogeneousRightAmbient_adjoint {P : SiteProfile}
    (d e : HomogeneousRightData P) (hR : e.right = star d.right)
    (hc : e.frequency = -d.frequency) :
    star (homogeneousRightAmbient d) = homogeneousRightAmbient e := by
  unfold homogeneousRightAmbient
  rw [star_mul,shift_star,← fibre_star,← fibre_star,shift_commutes_fibre,hR,hc]

def matrixUnitRightData (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    HomogeneousRightData P where
  right := rTowerPi P (Matrix.single i j 1)
  left := towerPi P (Matrix.single i j 1)
  frequency := Real.log (localEigenvalue P N i j)
  right_mem := rTowerPi_mem_baseCommutant _
  left_mem := towerPi_mem_factor _
  homogeneous := fun t => rTowerPi_matrixUnit_homogeneous t N i j
  vacuum := by rw [towerPi_omega,rTowerPi_omega]

def matrixUnitTwistedRightData (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    HomogeneousRightData P where
  right := star (rTowerPi P (Matrix.single i j 1))
  left := towerPi P (modTwist P (Matrix.single i j 1))
  frequency := -Real.log (localEigenvalue P N i j)
  right_mem := (theFactorObject P).commutant.toStarSubalgebra.star_mem'
    (rTowerPi_mem_baseCommutant _)
  left_mem := towerPi_mem_factor _
  homogeneous := homogeneous_base_adjoint P _ _ (fun t => rTowerPi_matrixUnit_homogeneous t N i j)
  vacuum := by
    rw [ContinuousLinearMap.star_eq_adjoint,← rTowerPi_star,towerPi_omega,rTowerPi_omega]

theorem matrixUnitRightAmbient_adjoint (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    star (homogeneousRightAmbient (matrixUnitRightData P N i j)) =
      homogeneousRightAmbient (matrixUnitTwistedRightData P N i j) :=
  homogeneousRightAmbient_adjoint _ _ rfl rfl

#print axioms modularPhase_star_frequency
#print axioms homogeneous_base_adjoint
#print axioms homogeneousRightAmbient
#print axioms homogeneousRightAmbient_adjoint
#print axioms matrixUnitRightData
#print axioms matrixUnitTwistedRightData
#print axioms matrixUnitRightAmbient_adjoint
end
end TGLV350.Regular
