import TGLExt.V350ScalarGNSLinear
/-! Generic construction of the scalar dual-weight GNS orbit and completion.
Its algebra/vector context requires faithfulness of the original weight.
The concrete Fock instance supplies that property by its already proved lemma;
no GNS equality, injectivity, or completion result is assumed. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarGNS
open TGLV350.Regular MeasureTheory
open scoped ENNReal NNReal Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
/-- Algebra/vector inputs. Faithfulness is an already proved property in the
concrete Fock instance, not a conclusion about GNS inserted as a field. -/
structure Context (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  algebra : VonNeumannAlgebra (RegularHilbert H)
  vacuum : RegularHilbert H
  faithful : ∀ (A : RegularHilbert H →L[ℂ] RegularHilbert H), A ∈ algebra → 0 ≤ A →
    (dualQuadraticIntegral A vacuum = 0 ↔ A = 0)
variable (D : Context H)
def finiteIdeal : Submodule ℂ D.algebra.toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val}
  zero_mem' := HasFiniteDualSquare.zero
  add_mem' := fun hA hB => HasFiniteDualSquare.add _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteDualSquare.smul c _ hA

theorem scalar_finite (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteDualSquare A) : dualQuadraticIntegral (star A*A) D.vacuum < ⊤ := by
  obtain ⟨C,hC⟩ := hA
  exact (hC D.vacuum).trans_lt
    (ENNReal.mul_lt_top ENNReal.coe_lt_top ENNReal.ofReal_lt_top)

/-- Square integrability of the actual dual orbit follows from the finite
weight, with the fixed positive Haar factor removed explicitly. -/
theorem scalarOrbit_memLp 
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : HasFiniteDualSquare A) :
    MemLp (fun s : ℝ => dualAmbient s A D.vacuum) 2 := by
  have hq := scalar_finite D A hA
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
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
def scalarGNSOrbit  (A : finiteIdeal D) :
    RegularHilbert (RegularHilbert H) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarOrbit_memLp D A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val D.vacuum)

theorem scalarGNSOrbit_norm_sq  (A : finiteIdeal D) :
    ENNReal.ofReal (‖scalarGNSOrbit D A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) D.vacuum := by
  have hm := scalarOrbit_memLp D A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarGNSOrbit D A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val D.vacuum‖ ^ 2 := by
    unfold scalarGNSOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← TGLV350.Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

theorem scalarGNSOrbit_ae  (A : finiteIdeal D) :
    (scalarGNSOrbit D A : ℝ → RegularHilbert H) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val D.vacuum := by
  let hm := scalarOrbit_memLp D A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val D.vacuum)),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarGNSOrbit_add  (A B : finiteIdeal D) :
    scalarGNSOrbit D (A+B) = scalarGNSOrbit D A + scalarGNSOrbit D B := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae D (A+B),scalarGNSOrbit_ae D A,
    scalarGNSOrbit_ae D B,Lp.coeFn_add (scalarGNSOrbit D A) (scalarGNSOrbit D B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) D.vacuum = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val D.vacuum) (dualAmbient s B.val.val D.vacuum)

theorem scalarGNSOrbit_smul  (c : ℂ) (A : finiteIdeal D) :
    scalarGNSOrbit D (c • A) = c • scalarGNSOrbit D A := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae D (c • A),scalarGNSOrbit_ae D A,
    Lp.coeFn_smul c (scalarGNSOrbit D A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) D.vacuum = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val D.vacuum) = _
  exact smul_comm _ _ _

def scalarGNSLinear  :
    (finiteIdeal D) →ₗ[ℂ] RegularHilbert (RegularHilbert H) where
  toFun := scalarGNSOrbit D
  map_add' := scalarGNSOrbit_add D
  map_smul' := scalarGNSOrbit_smul D

theorem scalarGNSOrbit_zero_iff  (A : finiteIdeal D) :
    scalarGNSOrbit D A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) D.vacuum = 0 := by
      rw [← scalarGNSOrbit_norm_sq D,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := D.algebra.mul_mem
      (D.algebra.toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (D.faithful _ hm (star_mul_self_nonneg A.val.val)).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarGNSLinear D).map_zero

theorem scalarGNSLinear_injective  :
    Function.Injective (scalarGNSLinear D) := by
  intro A B h
  have hz : scalarGNSLinear D (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarGNSOrbit_zero_iff D (A-B)).mp hz)


def GNSSubspace : Submodule ℂ (RegularHilbert (RegularHilbert H)) :=
  (scalarGNSLinear D).range.topologicalClosure
abbrev GNSHilbert := GNSSubspace D
instance gnsCompleteSpace : CompleteSpace (GNSHilbert D) :=
  Submodule.topologicalClosure.completeSpace (scalarGNSLinear D).range

def GNSEmbedding : (finiteIdeal D) →ₗ[ℂ] GNSHilbert D :=
  (scalarGNSLinear D).codRestrict (GNSSubspace D)
    (fun A => (scalarGNSLinear D).range.le_topologicalClosure ⟨A,rfl⟩)

theorem GNSEmbedding_injective : Function.Injective (GNSEmbedding D) := by
  intro A B h
  exact scalarGNSLinear_injective D (congrArg Subtype.val h)


end F1Fecho.RegularScalarGNS
#print axioms F1Fecho.RegularScalarGNS.finiteIdeal
#print axioms F1Fecho.RegularScalarGNS.scalar_finite
#print axioms F1Fecho.RegularScalarGNS.scalarOrbit_memLp
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit_norm_sq
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit_ae
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit_add
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit_smul
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit_zero_iff
#print axioms F1Fecho.RegularScalarGNS.scalarGNSLinear_injective
#print axioms F1Fecho.RegularScalarGNS.scalarGNSOrbit
#print axioms F1Fecho.RegularScalarGNS.scalarGNSLinear
#print axioms F1Fecho.RegularScalarGNS.GNSSubspace
#print axioms F1Fecho.RegularScalarGNS.GNSHilbert
#print axioms F1Fecho.RegularScalarGNS.GNSEmbedding_injective
#print axioms F1Fecho.RegularScalarGNS.GNSEmbedding
