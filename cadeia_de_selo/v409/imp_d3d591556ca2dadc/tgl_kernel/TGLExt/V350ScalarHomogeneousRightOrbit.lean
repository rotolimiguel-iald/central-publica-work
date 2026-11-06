import TGLExt.V350LocalRightModularTransport
import TGLExt.V350HomogeneousCommutantTransport
import TGLExt.V350ScalarWeightOrbit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
open scoped ENNReal NNReal
noncomputable section

theorem hasFiniteScalarSquare_iff_memLp (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    HasFiniteScalarSquare P A ↔ MemLp (fun s : ℝ => dualAmbient s A (regularVacuum P)) 2 := by
  constructor
  · exact scalarWeightOrbit_memLp P A
  · intro hm
    have hi := hm.2
    rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top (by norm_num) (by norm_num)] at hi
    have he (s : ℝ) : ENNReal.ofReal (‖dualAmbient s A (regularVacuum P)‖ ^ 2) =
        (‖dualAmbient s A (regularVacuum P)‖₊ : ℝ≥0∞) ^ 2 := by
      rw [ENNReal.ofReal_pow (norm_nonneg _),ofReal_norm,enorm_eq_nnnorm]
    simp only [HasFiniteScalarSquare,dualQuadraticIntegral,dualQuadraticIntegrand_star_mul,he]
    apply ENNReal.mul_lt_top ENNReal.ofReal_lt_top
    simpa only [ENNReal.toReal_ofNat,ENNReal.rpow_two,enorm_eq_nnnorm,pow_two] using hi

/-- The right multiplier is a shift on the dual variable together with a
base commutant operator. This is not a constant right action on coefficients. -/
theorem scalarOrbit_right_homogeneous (P : SiteProfile)
    (D Y : TowerHilbert P →L[ℂ] TowerHilbert P) (c : ℝ)
    (hD : D ∈ (theFactorObject P).commutant)
    (he : ∀ t : ℝ, modularConjugation P t D = modularPhase t c • D)
    (hv : Y (hOmega P) = D (hOmega P))
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    dualAmbient s (A.val * fibre Y) (regularVacuum P) =
      fibre D (dualAmbient (s-c) A.val (regularVacuum P)) := by
  have hΩ : fibre Y (regularVacuum P) = fibre D (regularVacuum P) := by
    change fibre Y (testVector (hOmega P)) = fibre D (testVector (hOmega P))
    rw [fibre_testVector,fibre_testVector,hv]
  rw [map_mul,dualAmbient_fibre]
  change dualAmbient s A.val (fibre Y (regularVacuum P)) = _
  rw [hΩ]
  exact congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ] _ => T (regularVacuum P))
    (homogeneous_commutant_dual_intertwines P D c hD he A s)

theorem scalarWeight_right_homogeneous_finite (P : SiteProfile)
    (D Y : TowerHilbert P →L[ℂ] TowerHilbert P) (c : ℝ)
    (hD : D ∈ (theFactorObject P).commutant)
    (he : ∀ t : ℝ, modularConjugation P t D = modularPhase t c • D)
    (hv : Y (hOmega P) = D (hOmega P)) (A : scalarWeightLeftIdeal P) :
    HasFiniteScalarSquare P (A.val.val * fibre Y) := by
  apply (hasFiniteScalarSquare_iff_memLp P _).mpr
  have hm := (scalarWeightOrbit_memLp P A.val.val A.property).comp_measurePreserving
    (measurePreserving_sub_right volume c)
  have ht := (fibre D).lipschitz.comp_memLp (map_zero (fibre D)) hm
  convert ht using 1
  funext s
  exact scalarOrbit_right_homogeneous P D Y c hD he hv A.val s

theorem scalarOrbit_right_matrixUnit (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (s : ℝ) :
    dualAmbient s (A.val * fibre (towerPi P (Matrix.single i j 1))) (regularVacuum P) =
      fibre (rTowerPi P (Matrix.single i j 1))
        (dualAmbient (s-Real.log (localEigenvalue P N i j)) A.val (regularVacuum P)) := by
  apply scalarOrbit_right_homogeneous P _ _ _ (rTowerPi_mem_baseCommutant _)
    (fun t => rTowerPi_matrixUnit_homogeneous t N i j)
  rw [towerPi_omega,rTowerPi_omega]

#print axioms hasFiniteScalarSquare_iff_memLp
#print axioms scalarOrbit_right_homogeneous
#print axioms scalarWeight_right_homogeneous_finite
#print axioms scalarOrbit_right_matrixUnit
end
end TGLV350.Regular
