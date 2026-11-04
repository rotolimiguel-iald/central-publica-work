import TGLExt.F1Fecho394.RegularScalarWeightDomainR1

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarWeightOrbit
open TGLV350.Regular MeasureTheory F1Fecho.RegularScalarGNS F1Fecho.RegularScalarWeightDomain
open scoped ENNReal NNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)

theorem scalarWeightOrbit_memLp 
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteScalarSquare D A) :
    MemLp (fun s : ℝ => dualAmbient s A D.vacuum) 2 := by
  have hq := hA
  simp only [HasFiniteScalarSquare, dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
  have hn : ENNReal.ofReal dualHaarFactor ≠ 0 :=
    ne_of_gt (ENNReal.ofReal_pos.mpr dualHaarFactor_pos)
  have hi : (∫⁻ s : ℝ, ENNReal.ofReal (‖dualAmbient s A D.vacuum‖ ^ 2)) < ⊤ := by
    by_contra h
    have ht := top_unique (not_lt.mp h)
    rw [ht] at hq
    rw [ENNReal.mul_top hn] at hq
    exact (lt_irrefl _) hq
  refine ⟨(dualAmbient_strongly_continuous A D.vacuum).aestronglyMeasurable,?_⟩
  rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top (by norm_num) (by norm_num)]
  have he (s : ℝ) : ENNReal.ofReal (‖dualAmbient s A D.vacuum‖ ^ 2) =
      (‖dualAmbient s A D.vacuum‖₊ : ℝ≥0∞) ^ 2 := by
    rw [ENNReal.ofReal_pow (norm_nonneg _), ofReal_norm, enorm_eq_nnnorm]
  simp_rw [he] at hi
  simpa only [ENNReal.toReal_ofNat, ENNReal.rpow_two, enorm_eq_nnnorm, pow_two] using hi

/-- An orbit vector in a concrete Hilbert space. Completion of its range,
the left representation and the Tomita operator are separate constructions. -/
def scalarWeightOrbit  (A : scalarWeightLeftIdeal D ) :
    RegularHilbert (RegularHilbert H) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarWeightOrbit_memLp D A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val D.vacuum)

theorem scalarWeightOrbit_norm_sq  (A : scalarWeightLeftIdeal D ) :
    ENNReal.ofReal (‖scalarWeightOrbit D A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) D.vacuum := by
  have hm := scalarWeightOrbit_memLp D A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarWeightOrbit D A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val D.vacuum‖ ^ 2 := by
    unfold scalarWeightOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← TGLV350.Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

theorem scalarWeightOrbit_ae  (A : scalarWeightLeftIdeal D ) :
    (scalarWeightOrbit D A : ℝ → RegularHilbert H) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val D.vacuum := by
  let hm := scalarWeightOrbit_memLp D A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val D.vacuum)),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarWeightOrbit_add  (A B : scalarWeightLeftIdeal D ) :
    scalarWeightOrbit D (A+B) = scalarWeightOrbit D A + scalarWeightOrbit D B := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae D (A+B),scalarWeightOrbit_ae D A,
    scalarWeightOrbit_ae D B,Lp.coeFn_add (scalarWeightOrbit D A) (scalarWeightOrbit D B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) D.vacuum = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val D.vacuum) (dualAmbient s B.val.val D.vacuum)

theorem scalarWeightOrbit_smul  (c : ℂ) (A : scalarWeightLeftIdeal D ) :
    scalarWeightOrbit D (c • A) = c • scalarWeightOrbit D A := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae D (c • A),scalarWeightOrbit_ae D A,
    Lp.coeFn_smul c (scalarWeightOrbit D A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) D.vacuum = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val D.vacuum) = _
  exact smul_comm _ _ _

def scalarWeightLinear  :
    scalarWeightLeftIdeal D →ₗ[ℂ] RegularHilbert (RegularHilbert H) where
  toFun := scalarWeightOrbit D 
  map_add' := scalarWeightOrbit_add D 
  map_smul' := scalarWeightOrbit_smul D 

theorem scalarWeightOrbit_zero_iff  (A : scalarWeightLeftIdeal D ) :
    scalarWeightOrbit D A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) D.vacuum = 0 := by
      rw [← scalarWeightOrbit_norm_sq D,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := D.algebra.mul_mem
      (D.algebra.toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (D.faithful _ hm (star_mul_self_nonneg A.val.val)).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarWeightLinear D ).map_zero

theorem scalarWeightLinear_injective  :
    Function.Injective (scalarWeightLinear D ) := by
  intro A B h
  have hz : scalarWeightLinear D (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarWeightOrbit_zero_iff D (A-B)).mp hz)


theorem scalarWeightOrbit_uniform  (A : finiteIdeal D) :
    scalarWeightOrbit D (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight D ) A) =
      scalarGNSOrbit D A := rfl

theorem scalarWeightOrbit_norm_sq_real  (A : scalarWeightLeftIdeal D ) :
    ‖scalarWeightOrbit D A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val D.vacuum‖ ^ 2 := by
  unfold scalarWeightOrbit
  rw [norm_smul,mul_pow,Real.norm_eq_abs,sq_abs,Real.sq_sqrt dualHaarFactor_pos.le,
    ← TGLV350.Fourier.integral_norm_sq_eq_L2 _ (scalarWeightOrbit_memLp D A.val.val A.property)]

end
end F1Fecho.RegularScalarWeightOrbit
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_memLp
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_norm_sq_real
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_norm_sq
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_ae
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_add
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_smul
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_zero_iff
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightLinear_injective
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit_uniform
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightOrbit
#print axioms F1Fecho.RegularScalarWeightOrbit.scalarWeightLinear
