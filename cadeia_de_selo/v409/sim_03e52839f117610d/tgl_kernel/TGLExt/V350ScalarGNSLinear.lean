import TGLExt.V350ScalarGNSOrbit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
open scoped ENNReal NNReal
noncomputable section

theorem dualAmbient_add_apply {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (s : ℝ)
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualAmbient s (A+B) v = dualAmbient s A v + dualAmbient s B v := by
  rw [map_add]
  rfl

theorem scalarGNSOrbit_ae (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    (scalarGNSOrbit P A : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val (regularVacuum P) := by
  let hm := scalarOrbit_memLp P A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val (regularVacuum P))),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarGNSOrbit_add (P : SiteProfile) (A B : finiteDualLeftIdeal P) :
    scalarGNSOrbit P (A+B) = scalarGNSOrbit P A + scalarGNSOrbit P B := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae P (A+B),scalarGNSOrbit_ae P A,
    scalarGNSOrbit_ae P B,Lp.coeFn_add (scalarGNSOrbit P A) (scalarGNSOrbit P B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) (regularVacuum P) = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val (regularVacuum P)) (dualAmbient s B.val.val (regularVacuum P))

theorem scalarGNSOrbit_smul (P : SiteProfile) (c : ℂ) (A : finiteDualLeftIdeal P) :
    scalarGNSOrbit P (c • A) = c • scalarGNSOrbit P A := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae P (c • A),scalarGNSOrbit_ae P A,
    Lp.coeFn_smul c (scalarGNSOrbit P A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) (regularVacuum P) = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val (regularVacuum P)) = _
  exact smul_comm _ _ _

def scalarGNSLinear (P : SiteProfile) :
    finiteDualLeftIdeal P →ₗ[ℂ] RegularHilbert (RegularHilbert (TowerHilbert P)) where
  toFun := scalarGNSOrbit P
  map_add' := scalarGNSOrbit_add P
  map_smul' := scalarGNSOrbit_smul P

theorem scalarGNSOrbit_zero_iff (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarGNSOrbit P A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) (regularVacuum P) = 0 := by
      rw [← scalarGNSOrbit_norm_sq,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := (regularCoreAlgebra P).mul_mem
      ((regularCoreAlgebra P).toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (dualQuadraticIntegral_vacuum_faithful P _ hm (star_mul_self_nonneg A.val.val)).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarGNSLinear P).map_zero

theorem scalarGNSLinear_injective (P : SiteProfile) :
    Function.Injective (scalarGNSLinear P) := by
  intro A B h
  have hz : scalarGNSLinear P (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarGNSOrbit_zero_iff P (A-B)).mp hz)

#print axioms dualAmbient_add_apply
#print axioms scalarGNSOrbit_ae
#print axioms scalarGNSOrbit_add
#print axioms scalarGNSOrbit_smul
#print axioms scalarGNSLinear
#print axioms scalarGNSOrbit_zero_iff
#print axioms scalarGNSLinear_injective
end
end TGLV350.Regular
