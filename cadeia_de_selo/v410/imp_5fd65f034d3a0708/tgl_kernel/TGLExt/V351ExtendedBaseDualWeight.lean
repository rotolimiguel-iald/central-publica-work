import TGLExt.V351RegularCoreTraceContract
import TGLExt.V350FixedBaseEquivalence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1200000

namespace TGLV351
open TGLExt TGLV350.Regular Filter
open scoped ENNReal NNReal Topology
noncomputable section

/-- Restrict the actual fixed-algebra form along the existing isometric copy
of the base Hilbert space. Affiliation is proved using the amplified commutant.
This definition does not assert a representation-independent cone isomorphism. -/
def fixedFormOnBase (P : SiteProfile) (Q : AffiliatedPositiveForm (dualFixedCore P)) :
    AffiliatedPositiveForm (theFactorObject P) where
  value := fun v => Q.value (testVectorIsometry v)
  map_zero := by rw [map_zero, Q.map_zero]
  map_smul := by intro c v; rw [map_smul, Q.map_smul]
  parallelogram := by intro v w; rw [map_add, map_sub, Q.parallelogram]
  lowerSemicontinuous := Q.lowerSemicontinuous.comp testVectorIsometry.continuous
  unitary_commutant_invariant := by
    intro U hU v
    let V : unitary (RegularHilbert (TowerHilbert P) →L[ℂ]
        RegularHilbert (TowerHilbert P)) :=
      ⟨fibre U.val, Unitary.map_mem fibreRepresentation U.property⟩
    have hV : ∀ B ∈ dualFixedCore P, V.val * B = B * V.val := by
      intro B hB
      obtain ⟨D, hD, rfl⟩ := (dualFixedCore_eq_amplified_base P B).mp hB
      change fibre U.val * fibre D = fibre D * fibre U.val
      rw [← fibre_mul, ← fibre_mul, hU D hD]
    change Q.value (testVector (U.val v)) = Q.value (testVector v)
    rw [← fibre_testVector]
    exact Q.unitary_commutant_invariant V hV (testVector v)

/-- The same dual integral now has a typed extended positive value in the
original base representation, with no bounded-value hypothesis. -/
def baseDualWeight (P : SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (theFactorObject P) :=
  fixedFormOnBase P (dualFixedWeight P A)

theorem baseDualWeight_value (P : SiteProfile) (A : PositiveCoreInput P)
    (v : TowerHilbert P) :
    (baseDualWeight P A).value v = dualQuadraticIntegral A.val (testVector v) := rfl

/-- The equality is in ENNReal, so infinite outputs are retained. -/
theorem scalarDualWeight_eq_base_evaluation (P : SiteProfile) (A : PositiveCoreInput P) :
    scalarDualWeight P A = (baseDualWeight P A).value (hOmega P) := rfl

theorem baseDualWeight_zero (P : SiteProfile) :
    baseDualWeight P (PositiveCoreInput.zero P) =
      AffiliatedPositiveForm.zeroForm (theFactorObject P) := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact dualQuadraticIntegral_zero (testVector v)

theorem baseDualWeight_add (P : SiteProfile) (A B : PositiveCoreInput P) :
    baseDualWeight P (A.add B) = (baseDualWeight P A).addForm (baseDualWeight P B) := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact congrArg (fun Q => (fixedFormOnBase P Q).value v) (dualFixedWeight_add P A B)

theorem baseDualWeight_scale (P : SiteProfile) (r : ℝ≥0) (A : PositiveCoreInput P) :
    baseDualWeight P (A.scale r) = (baseDualWeight P A).scaleForm r := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact congrArg (fun Q => (fixedFormOnBase P Q).value v) (dualFixedWeight_scale P r A)

/-- The input is conjugated by the actual image under fixedBaseEquiv;
the output is conjugated by the original base operator. -/
theorem baseDualWeight_bimodule (P : SiteProfile) (A : PositiveCoreInput P)
    (B : (theFactorObject P).toStarSubalgebra) :
    baseDualWeight P (A.conjugate (fixedBaseEquiv P B)) =
      (baseDualWeight P A).conjugate B.val B.property := by
  apply AffiliatedPositiveForm.ext
  intro v
  change dualQuadraticIntegral
      (star (fixedBaseEquiv P B).val * A.val * (fixedBaseEquiv P B).val) (testVector v) =
    dualQuadraticIntegral A.val (testVector (B.val v))
  rw [dualQuadraticIntegral_fixed_bimodule, fixedBaseEquiv_apply, fibre_testVector]

theorem baseDualWeight_mono (P : SiteProfile) (A B : PositiveCoreInput P) (hAB : A ≤ B) :
    baseDualWeight P A ≤ baseDualWeight P B :=
  fun v => dualFixedWeight_mono P A B hAB (testVector v)

theorem baseDualWeight_faithful (P : SiteProfile) (A : PositiveCoreInput P) :
    baseDualWeight P A = AffiliatedPositiveForm.zeroForm (theFactorObject P) ↔
      A = PositiveCoreInput.zero P := by
  constructor
  · intro hz
    apply (scalarDualWeight_faithful P A).mp
    rw [scalarDualWeight_eq_base_evaluation, hz]
    rfl
  · rintro rfl
    exact baseDualWeight_zero P

theorem baseDualWeight_preserves_internal_isLUB (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    IsLUB (Set.range (fun i => baseDualWeight P ⟨(A i).val, (A i).property, hpos i⟩))
      (baseDualWeight P ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩) := by
  have he := regularDualForm_preserves_internal_isLUB P A S hpos hmono hS
  constructor
  · rintro Q ⟨i, rfl⟩ v
    change dualQuadraticIntegral (A i).val (testVector v) ≤
      dualQuadraticIntegral S.val (testVector v)
    rw [he]
    exact le_iSup (fun j => dualQuadraticIntegral (A j).val (testVector v)) i
  · intro Q hQ v
    change dualQuadraticIntegral S.val (testVector v) ≤ Q.value v
    rw [he]
    exact iSup_le (fun i => hQ (Set.mem_range_self i) v)

theorem baseDualWeight_bounded_value (P : SiteProfile) (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra)
    (hrep : ∀ w, dualQuadraticIntegral A.val w =
      ENNReal.ofReal (inner ℂ w (fibre D.val w)).re) (v : TowerHilbert P) :
    (baseDualWeight P A).value v = ENNReal.ofReal (inner ℂ v (D.val v)).re := by
  rw [baseDualWeight_value, hrep, fibre_testVector, testVector_inner]

/-- An infinite output is an actual case of the base construction, not a
finite-domain approximation silently converted with toReal. -/
theorem baseDualWeight_unit_infinite (P : SiteProfile) (v : TowerHilbert P) (hv : v ≠ 0) :
    (baseDualWeight P (positiveUnit P)).value v = ⊤ := by
  rw [baseDualWeight_value]
  apply dualQuadraticIntegral_one
  intro hz
  apply hv
  apply norm_eq_zero.mp
  rw [← testVector_norm, hz, norm_zero]

/-- The finite control remains the same normalized averaged square. -/
theorem baseDualWeight_averageSquare (P : SiteProfile) :
    (baseDualWeight P (positiveAverageSquare P)).value (hOmega P) = 1 :=
  scalarDualWeight_averageSquare P

#print axioms fixedFormOnBase
#print axioms baseDualWeight
#print axioms baseDualWeight_value
#print axioms scalarDualWeight_eq_base_evaluation
#print axioms baseDualWeight_zero
#print axioms baseDualWeight_add
#print axioms baseDualWeight_scale
#print axioms baseDualWeight_bimodule
#print axioms baseDualWeight_mono
#print axioms baseDualWeight_faithful
#print axioms baseDualWeight_preserves_internal_isLUB
#print axioms baseDualWeight_bounded_value
#print axioms baseDualWeight_unit_infinite
#print axioms baseDualWeight_averageSquare
end
end TGLV351
