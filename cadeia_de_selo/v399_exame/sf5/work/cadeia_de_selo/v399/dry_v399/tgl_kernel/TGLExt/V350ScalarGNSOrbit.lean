import TGLExt.V350ScalarDualWeight
import TGLExt.V350FourierL1L2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
open scoped ENNReal NNReal
noncomputable section

/-- Square integrability of the actual dual orbit follows from the finite
weight, with the fixed positive Haar factor removed explicitly. -/
theorem scalarOrbit_memLp (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteDualSquare A) :
    MemLp (fun s : ℝ => dualAmbient s A (regularVacuum P)) 2 := by
  have hq := HasFiniteDualSquare.scalar_finite P A hA
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
  have hn : ENNReal.ofReal dualHaarFactor ≠ 0 :=
    ne_of_gt (ENNReal.ofReal_pos.mpr dualHaarFactor_pos)
  have hi : (∫⁻ s : ℝ, ENNReal.ofReal (‖dualAmbient s A (regularVacuum P)‖ ^ 2)) < ⊤ := by
    by_contra h
    have ht := top_unique (not_lt.mp h)
    rw [ht] at hq
    rw [ENNReal.mul_top hn] at hq
    exact (lt_irrefl _) hq
  refine ⟨(dualAmbient_strongly_continuous A (regularVacuum P)).aestronglyMeasurable,?_⟩
  rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top (by norm_num) (by norm_num)]
  have he (s : ℝ) : ENNReal.ofReal (‖dualAmbient s A (regularVacuum P)‖ ^ 2) =
      (‖dualAmbient s A (regularVacuum P)‖₊ : ℝ≥0∞) ^ 2 := by
    rw [ENNReal.ofReal_pow (norm_nonneg _), ofReal_norm, enorm_eq_nnnorm]
  simp_rw [he] at hi
  simpa only [ENNReal.toReal_ofNat, ENNReal.rpow_two, enorm_eq_nnnorm, pow_two] using hi

/-- An orbit vector in a concrete Hilbert space. Completion of its range,
the left representation and the Tomita operator are separate constructions. -/
def scalarGNSOrbit (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarOrbit_memLp P A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val (regularVacuum P))

theorem scalarGNSOrbit_norm_sq (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    ENNReal.ofReal (‖scalarGNSOrbit P A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) (regularVacuum P) := by
  have hm := scalarOrbit_memLp P A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarGNSOrbit P A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val (regularVacuum P)‖ ^ 2 := by
    unfold scalarGNSOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

#print axioms scalarOrbit_memLp
#print axioms scalarGNSOrbit
#print axioms scalarGNSOrbit_norm_sq
end
end TGLV350.Regular
