import TGLExt.V350ScalarDualWeightFaithfulness
import TGLExt.V350BoundedBaseDualValues

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology ENNReal NNReal
noncomputable section

/-- Scalar evaluation of the actual dual form at the same tower vacuum,
embedded in the unit interval. This is a weight, not a trace. -/
def scalarDualWeight (P : SiteProfile) (A : PositiveCoreInput P) : ℝ≥0∞ :=
  dualQuadraticIntegral A.val (regularVacuum P)

theorem scalarDualWeight_zero (P : SiteProfile) :
    scalarDualWeight P (PositiveCoreInput.zero P) = 0 :=
  dualQuadraticIntegral_zero _

theorem scalarDualWeight_add (P : SiteProfile) (A B : PositiveCoreInput P) :
    scalarDualWeight P (A.add B) = scalarDualWeight P A + scalarDualWeight P B :=
  dualQuadraticIntegral_add A.val B.val A.property.2 B.property.2 _

theorem scalarDualWeight_scale (P : SiteProfile) (r : ℝ≥0) (A : PositiveCoreInput P) :
    scalarDualWeight P (A.scale r) = (r : ℝ≥0∞) * scalarDualWeight P A := by
  change dualQuadraticIntegral ((r : ℝ) • A.val) (regularVacuum P) =
    (r : ℝ≥0∞) * dualQuadraticIntegral A.val (regularVacuum P)
  simpa using dualQuadraticIntegral_smul_operator (r : ℝ) r.property A.val (regularVacuum P)

theorem scalarDualWeight_mono (P : SiteProfile) (A B : PositiveCoreInput P) (hAB : A ≤ B) :
    scalarDualWeight P A ≤ scalarDualWeight P B :=
  dualQuadraticIntegral_mono A.val B.val hAB _

theorem scalarDualWeight_faithful (P : SiteProfile) (A : PositiveCoreInput P) :
    scalarDualWeight P A = 0 ↔ A = PositiveCoreInput.zero P := by
  constructor
  · intro hz
    exact Subtype.ext ((dualQuadraticIntegral_vacuum_faithful P A.val A.property.1 A.property.2).mp hz)
  · rintro rfl
    exact scalarDualWeight_zero P

/-- Normality uses an internal directed supremum in N, not a separately
assumed ambient strong limit. -/
theorem scalarDualWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩ :=
  regularDualForm_preserves_internal_isLUB P A S hpos hmono hS (regularVacuum P)

theorem HasFiniteDualSquare.scalar_finite (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hf : HasFiniteDualSquare A) :
    dualQuadraticIntegral (star A * A) (regularVacuum P) < ⊤ := by
  obtain ⟨C,hC⟩ := hf
  have he := hC (regularVacuum P)
  rw [regularVacuum_norm, one_pow, ENNReal.ofReal_one, mul_one] at he
  exact he.trans_lt ENNReal.coe_lt_top

/-- The already constructed complex left ideal is strongly dense in N,
and all of its squares have finite scalar weight. -/
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
  obtain ⟨hf,hm,ht⟩ := finiteDualLeftIdeal_strong_approximation P A
  exact ⟨fun h hh => HasFiniteDualSquare.scalar_finite P _ (hf h hh),hm,ht⟩

/-- On a bounded base-valued output, scalar evaluation agrees with the
original vector state on that very base element. -/
theorem scalarDualWeight_bounded_base_value (P : SiteProfile) (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra)
    (hrep : ∀ v, dualQuadraticIntegral A.val v =
      ENNReal.ofReal (inner ℂ v (fibre D.val v)).re) :
    scalarDualWeight P A = ENNReal.ofReal (inner ℂ (hOmega P) (D.val (hOmega P))).re := by
  change dualQuadraticIntegral A.val (testVector (hOmega P)) = _
  rw [hrep, fibre_testVector, testVector_inner]

#print axioms scalarDualWeight
#print axioms scalarDualWeight_zero
#print axioms scalarDualWeight_add
#print axioms scalarDualWeight_scale
#print axioms scalarDualWeight_mono
#print axioms scalarDualWeight_faithful
#print axioms scalarDualWeight_normal
#print axioms HasFiniteDualSquare.scalar_finite
#print axioms scalarDualWeight_square_finite_strong_density
#print axioms scalarDualWeight_bounded_base_value
end
end TGLV350.Regular
