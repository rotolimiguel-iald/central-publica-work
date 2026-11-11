import TGLExt.V350PositiveFormCone
import TGLExt.V350DualFixedFormAffiliation
import TGLExt.V350DualFormNormality
import TGLExt.V350DualFormFaithfulness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open scoped ENNReal NNReal
noncomputable section

/-- Positive bounded inputs in the same regular algebra. -/
abbrev PositiveCoreInput (P : TGLExt.SiteProfile) :=
  {A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
    RegularHilbert (TGLExt.TowerHilbert P) // A ∈ regularCoreAlgebra P ∧ 0 ≤ A}

def PositiveCoreInput.zero (P : TGLExt.SiteProfile) : PositiveCoreInput P :=
  ⟨0, (regularCoreAlgebra P).zero_mem, le_rfl⟩

def PositiveCoreInput.add {P : TGLExt.SiteProfile}
    (A B : PositiveCoreInput P) : PositiveCoreInput P :=
  ⟨A.val+B.val, (regularCoreAlgebra P).add_mem A.property.1 B.property.1,
    add_nonneg A.property.2 B.property.2⟩

def PositiveCoreInput.scale {P : TGLExt.SiteProfile}
    (r : ℝ≥0) (A : PositiveCoreInput P) : PositiveCoreInput P :=
  ⟨(r : ℝ) • A.val, by
      change ((r : ℝ) : ℂ) • A.val ∈ regularCoreAlgebra P
      exact (regularCoreAlgebra P).toStarSubalgebra.smul_mem A.property.1 _,
    by
      change 0 ≤ ((r : ℝ) : ℂ) • A.val
      apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
      exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp A.property.2).smul_of_nonneg
        (by exact_mod_cast r.property)⟩

def PositiveCoreInput.conjugate {P : TGLExt.SiteProfile}
    (A : PositiveCoreInput P)
    (B : (dualFixedCore P).toStarSubalgebra) : PositiveCoreInput P :=
  ⟨star B.val * A.val * B.val, by
      have hB := ((dualFixedCore_mem_iff P B.val).mp B.property).1
      exact (regularCoreAlgebra P).mul_mem
        ((regularCoreAlgebra P).mul_mem
          ((regularCoreAlgebra P).toStarSubalgebra.star_mem' hB) A.property.1) hB,
    star_left_conjugate_nonneg A.property.2 B.val⟩

/-- The output is the actual dual integral, now in the cone affiliated with
the fixed algebra F. No identification F=base or semifiniteness is assumed. -/
def dualFixedWeight (P : TGLExt.SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (dualFixedCore P) :=
  dualFixedAffiliatedPositiveForm P A.val A.property.1 A.property.2

theorem dualFixedWeight_value (P : TGLExt.SiteProfile) (A : PositiveCoreInput P)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    (dualFixedWeight P A).value v = dualQuadraticIntegral A.val v := rfl

theorem dualFixedWeight_zero (P : TGLExt.SiteProfile) :
    dualFixedWeight P (PositiveCoreInput.zero P) =
      AffiliatedPositiveForm.zeroForm (dualFixedCore P) := by
  apply AffiliatedPositiveForm.ext
  exact dualQuadraticIntegral_zero

theorem dualFixedWeight_add (P : TGLExt.SiteProfile) (A B : PositiveCoreInput P) :
    dualFixedWeight P (A.add B) = (dualFixedWeight P A).addForm (dualFixedWeight P B) := by
  apply AffiliatedPositiveForm.ext
  exact dualQuadraticIntegral_add A.val B.val A.property.2 B.property.2

theorem dualFixedWeight_scale (P : TGLExt.SiteProfile)
    (r : ℝ≥0) (A : PositiveCoreInput P) :
    dualFixedWeight P (A.scale r) = (dualFixedWeight P A).scaleForm r := by
  apply AffiliatedPositiveForm.ext
  intro v
  change dualQuadraticIntegral ((r : ℝ) • A.val) v =
    (r : ℝ≥0∞) * dualQuadraticIntegral A.val v
  simpa using dualQuadraticIntegral_smul_operator (r : ℝ) r.property A.val v

theorem dualQuadraticIntegral_fixed_bimodule (P : TGLExt.SiteProfile)
    (A : PositiveCoreInput P) (B : (dualFixedCore P).toStarSubalgebra)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral (star B.val * A.val * B.val) v =
      dualQuadraticIntegral A.val (B.val v) := by
  have hfixed := ((dualFixedCore_mem_iff P B.val).mp B.property).2
  have hpoint : ∀ s : ℝ,
      dualQuadraticIntegrand (star B.val * A.val * B.val) v s =
        dualQuadraticIntegrand A.val (B.val v) s := by
    intro s
    unfold dualQuadraticIntegrand
    rw [map_mul, map_mul, map_star, hfixed, operatorQuadratic_conjugate]
  simp only [dualQuadraticIntegral, hpoint]

/-- The bimodule identity holds for every B in F, not only fibre operators. -/
theorem dualFixedWeight_bimodule (P : TGLExt.SiteProfile)
    (A : PositiveCoreInput P) (B : (dualFixedCore P).toStarSubalgebra) :
    dualFixedWeight P (A.conjugate B) =
      (dualFixedWeight P A).conjugate B.val B.property := by
  apply AffiliatedPositiveForm.ext
  exact dualQuadraticIntegral_fixed_bimodule P A B

theorem dualFixedWeight_mono (P : TGLExt.SiteProfile)
    (A B : PositiveCoreInput P) (hAB : A ≤ B) :
    dualFixedWeight P A ≤ dualFixedWeight P B :=
  fun v => dualQuadraticIntegral_mono A.val B.val hAB v

theorem dualFixedWeight_faithful (P : TGLExt.SiteProfile) (A : PositiveCoreInput P) :
    dualFixedWeight P A = AffiliatedPositiveForm.zeroForm (dualFixedCore P) ↔
      A = PositiveCoreInput.zero P := by
  constructor
  · intro h
    apply Subtype.ext
    exact (dualQuadraticIntegral_faithful A.val A.property.2).mp
      (fun v => congrArg (fun Q => Q.value v) h)
  · rintro rfl
    exact dualFixedWeight_zero P

variable {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]

theorem positive_internal_isLUB_nonneg (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hS : IsLUB (Set.range A) S) : 0 ≤ S :=
  (hpos (Classical.arbitrary ι)).trans (hS.1 (Set.mem_range_self _))

/-- Order normality as an actual least-upper-bound statement in the target
cone. The input supremum is internal to N; its positivity is derived. -/
theorem dualFixedWeight_preserves_internal_isLUB (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    IsLUB (Set.range (fun i => dualFixedWeight P ⟨(A i).val, (A i).property, hpos i⟩))
      (dualFixedWeight P ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩) := by
  have he := regularDualForm_preserves_internal_isLUB P A S hpos hmono hS
  constructor
  · rintro Q ⟨i,rfl⟩ v
    change dualQuadraticIntegral (A i).val v ≤ dualQuadraticIntegral S.val v
    rw [he]
    exact le_iSup (fun j => dualQuadraticIntegral (A j).val v) i
  · intro Q hQ v
    change dualQuadraticIntegral S.val v ≤ Q.value v
    rw [he]
    exact iSup_le (fun i => hQ (Set.mem_range_self i) v)

#print axioms PositiveCoreInput.zero
#print axioms PositiveCoreInput.add
#print axioms PositiveCoreInput.scale
#print axioms PositiveCoreInput.conjugate
#print axioms dualFixedWeight
#print axioms dualFixedWeight_value
#print axioms dualFixedWeight_zero
#print axioms dualFixedWeight_add
#print axioms dualFixedWeight_scale
#print axioms dualQuadraticIntegral_fixed_bimodule
#print axioms dualFixedWeight_bimodule
#print axioms dualFixedWeight_mono
#print axioms dualFixedWeight_faithful
#print axioms positive_internal_isLUB_nonneg
#print axioms dualFixedWeight_preserves_internal_isLUB
end
end TGLV350.Regular
