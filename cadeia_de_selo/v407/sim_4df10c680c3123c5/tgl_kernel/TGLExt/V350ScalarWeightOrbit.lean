import TGLExt.V350ScalarWeightDomain
import TGLExt.V350ScalarGNSLinear

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
open scoped ENNReal NNReal
noncomputable section

theorem scalarWeightOrbit_memLp (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hA : HasFiniteScalarSquare P A) :
    MemLp (fun s : ℝ => dualAmbient s A (regularVacuum P)) 2 := by
  have hq := hA
  simp only [HasFiniteScalarSquare, dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
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
def scalarWeightOrbit (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarWeightOrbit_memLp P A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val (regularVacuum P))

theorem scalarWeightOrbit_norm_sq (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ENNReal.ofReal (‖scalarWeightOrbit P A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) (regularVacuum P) := by
  have hm := scalarWeightOrbit_memLp P A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarWeightOrbit P A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val (regularVacuum P)‖ ^ 2 := by
    unfold scalarWeightOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

theorem scalarWeightOrbit_ae (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    (scalarWeightOrbit P A : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val (regularVacuum P) := by
  let hm := scalarWeightOrbit_memLp P A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val (regularVacuum P))),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarWeightOrbit_add (P : SiteProfile) (A B : scalarWeightLeftIdeal P) :
    scalarWeightOrbit P (A+B) = scalarWeightOrbit P A + scalarWeightOrbit P B := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae P (A+B),scalarWeightOrbit_ae P A,
    scalarWeightOrbit_ae P B,Lp.coeFn_add (scalarWeightOrbit P A) (scalarWeightOrbit P B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) (regularVacuum P) = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val (regularVacuum P)) (dualAmbient s B.val.val (regularVacuum P))

theorem scalarWeightOrbit_smul (P : SiteProfile) (c : ℂ) (A : scalarWeightLeftIdeal P) :
    scalarWeightOrbit P (c • A) = c • scalarWeightOrbit P A := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae P (c • A),scalarWeightOrbit_ae P A,
    Lp.coeFn_smul c (scalarWeightOrbit P A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) (regularVacuum P) = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val (regularVacuum P)) = _
  exact smul_comm _ _ _

def scalarWeightLinear (P : SiteProfile) :
    scalarWeightLeftIdeal P →ₗ[ℂ] RegularHilbert (RegularHilbert (TowerHilbert P)) where
  toFun := scalarWeightOrbit P
  map_add' := scalarWeightOrbit_add P
  map_smul' := scalarWeightOrbit_smul P

theorem scalarWeightOrbit_zero_iff (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    scalarWeightOrbit P A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) (regularVacuum P) = 0 := by
      rw [← scalarWeightOrbit_norm_sq,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := (regularCoreAlgebra P).mul_mem
      ((regularCoreAlgebra P).toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (dualQuadraticIntegral_vacuum_faithful P _ hm (star_mul_self_nonneg A.val.val)).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarWeightLinear P).map_zero

theorem scalarWeightLinear_injective (P : SiteProfile) :
    Function.Injective (scalarWeightLinear P) := by
  intro A B h
  have hz : scalarWeightLinear P (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarWeightOrbit_zero_iff P (A-B)).mp hz)


theorem scalarWeightOrbit_uniform (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarWeightOrbit P (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A) =
      scalarGNSOrbit P A := rfl

theorem scalarWeightOrbit_norm_sq_real (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ‖scalarWeightOrbit P A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val (regularVacuum P)‖ ^ 2 := by
  unfold scalarWeightOrbit
  rw [norm_smul,mul_pow,Real.norm_eq_abs,sq_abs,Real.sq_sqrt dualHaarFactor_pos.le,
    ← Fourier.integral_norm_sq_eq_L2 _ (scalarWeightOrbit_memLp P A.val.val A.property)]

#print axioms scalarWeightOrbit_memLp
#print axioms scalarWeightOrbit
#print axioms scalarWeightOrbit_norm_sq
#print axioms scalarWeightOrbit_ae
#print axioms scalarWeightOrbit_add
#print axioms scalarWeightOrbit_smul
#print axioms scalarWeightLinear
#print axioms scalarWeightOrbit_zero_iff
#print axioms scalarWeightLinear_injective
#print axioms scalarWeightOrbit_uniform
#print axioms scalarWeightOrbit_norm_sq_real
end
end TGLV350.Regular
