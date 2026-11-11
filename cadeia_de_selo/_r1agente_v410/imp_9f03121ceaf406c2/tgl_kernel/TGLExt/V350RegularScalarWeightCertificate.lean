import TGLExt.V350ScalarModularInvariance
import TGLExt.V350FixedBaseEquivalence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

universe u

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology ENNReal NNReal
noncomputable section

/-- A certificate about the particular regular core, dual action, base and
scalar weight built from one SiteProfile. Every field refers to those actual
objects. It contains no canonical trace, KMS assertion or geometric witness. -/
structure RegularScalarWeightCertificate (P : SiteProfile) : Prop where
  fixed_base : ∀ B, B ∈ dualFixedCore P ↔
    ∃ C ∈ theFactorObject P, B = fibre C
  base_equivalence_is_amplification : ∀ A : (theFactorObject P).toStarSubalgebra,
    (fixedBaseEquiv P A).val = fibre A.val
  zero : scalarDualWeight P (PositiveCoreInput.zero P) = 0
  additive : ∀ A B : PositiveCoreInput P,
    scalarDualWeight P (A.add B) = scalarDualWeight P A + scalarDualWeight P B
  homogeneous : ∀ (r : ℝ≥0) (A : PositiveCoreInput P),
    scalarDualWeight P (A.scale r) = (r : ℝ≥0∞) * scalarDualWeight P A
  monotone : ∀ A B : PositiveCoreInput P, A ≤ B →
    scalarDualWeight P A ≤ scalarDualWeight P B
  faithful : ∀ A : PositiveCoreInput P,
    scalarDualWeight P A = 0 ↔ A = PositiveCoreInput.zero P
  normal : ∀ {ι : Type u} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S),
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩
  ideal_left_closed : ∀ B A : (regularCoreAlgebra P).toStarSubalgebra,
    A ∈ finiteDualLeftIdeal P → B * A ∈ finiteDualLeftIdeal P
  ideal_square_finite : ∀ A : (regularCoreAlgebra P).toStarSubalgebra,
    A ∈ finiteDualLeftIdeal P →
    dualQuadraticIntegral (star A.val * A.val) (regularVacuum P) < ⊤
  ideal_strong_approximation : ∀ A : (regularCoreAlgebra P).toStarSubalgebra,
    (∀ h : ℝ, 0 < h → HasFiniteDualSquare (A.val * regularAverage P h)) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v)
      (𝓝[>] 0) (𝓝 (A.val v)))
  candidate_flow_invariant : ∀ (A : PositiveCoreInput P) (t : ℝ),
    scalarDualWeight P (A.regularConjugate t) = scalarDualWeight P A
  bounded_value_is_original_state : ∀ (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra),
    (∀ v, dualQuadraticIntegral A.val v =
      ENNReal.ofReal (inner ℂ v (fibre D.val v)).re) →
    scalarDualWeight P A = ENNReal.ofReal (inner ℂ (hOmega P) (D.val (hOmega P))).re

/-- The fields are discharged for the actual construction, not accepted
as hypotheses from a caller or replaced by Boolean flags. -/
theorem regularScalarWeightCertificate (P : SiteProfile) :
    RegularScalarWeightCertificate.{u} P where
  fixed_base := dualFixedCore_eq_amplified_base P
  base_equivalence_is_amplification := fixedBaseEquiv_apply P
  zero := scalarDualWeight_zero P
  additive := scalarDualWeight_add P
  homogeneous := scalarDualWeight_scale P
  monotone := scalarDualWeight_mono P
  faithful := scalarDualWeight_faithful P
  normal := scalarDualWeight_normal P
  ideal_left_closed := finiteDualLeftIdeal_left_mul P
  ideal_square_finite := fun A hA => HasFiniteDualSquare.scalar_finite P A.val hA
  ideal_strong_approximation := finiteDualLeftIdeal_strong_approximation P
  candidate_flow_invariant := scalarDualWeight_regular_invariant P
  bounded_value_is_original_state := scalarDualWeight_bounded_base_value P

#print axioms regularScalarWeightCertificate
end
end TGLV350.Regular
