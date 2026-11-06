import TGLExt.V350DualClosedForm

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem operatorQuadratic_conjugate (A B : H →L[ℂ] H) (v : H) :
    (inner ℂ v ((star B * A * B) v)).re = (inner ℂ (B v) (A (B v))).re := by
  change (inner ℂ v (B.adjoint (A (B v)))).re = _
  rw [ContinuousLinearMap.adjoint_inner_right]

theorem dualAmbient_conjugate_fibre (s : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (B : H →L[ℂ] H) :
    dualAmbient s (star (fibre B) * A * fibre B) =
      star (fibre B) * dualAmbient s A * fibre B := by
  simp only [map_mul, map_star, dualAmbient_fibre]

/-- Bimodule identity as equality of extended quadratic evaluations.
It does not assume that the value has already been represented in the base cone. -/
theorem dualQuadraticIntegrand_bimodule
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (B : H →L[ℂ] H)
    (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (star (fibre B) * A * fibre B) v s =
      dualQuadraticIntegrand A (fibre B v) s := by
  unfold dualQuadraticIntegrand
  rw [dualAmbient_conjugate_fibre, operatorQuadratic_conjugate]

theorem dualQuadraticIntegral_bimodule
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (B : H →L[ℂ] H)
    (v : RegularHilbert H) :
    dualQuadraticIntegral (star (fibre B) * A * fibre B) v =
      dualQuadraticIntegral A (fibre B v) := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_bimodule]

theorem base_conjugate_mem (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)) (hA : A ∈ regularCoreAlgebra P)
    (B : (TGLExt.theFactorObject P).toStarSubalgebra) :
    star (fibre B.val) * A * fibre B.val ∈ regularCoreAlgebra P := by
  have hB := amplified_factor_mem P B.val B.property
  exact (regularCoreAlgebra P).mul_mem
    ((regularCoreAlgebra P).mul_mem ((regularCoreAlgebra P).toStarSubalgebra.star_mem' hB) hA) hB

/-- The conjugated input is positive in the same algebra. -/
def dualBaseConjugatedForm (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A)
    (B : (TGLExt.theFactorObject P).toStarSubalgebra) :
    AffiliatedPositiveForm (regularCoreAlgebra P) :=
  dualAffiliatedPositiveForm P (star (fibre B.val) * A * fibre B.val)
    (base_conjugate_mem P A hA B) (star_left_conjugate_nonneg hpos _)

theorem dualBaseConjugatedForm_value (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A)
    (B : (TGLExt.theFactorObject P).toStarSubalgebra)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    (dualBaseConjugatedForm P A hA hpos B).value v =
      (dualAffiliatedPositiveForm P A hA hpos).value (fibre B.val v) :=
  dualQuadraticIntegral_bimodule A B.val v

theorem dualAmbient_commute (s r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s (dualAmbient r A) = dualAmbient r (dualAmbient s A) := by
  calc
    _ = dualAmbient (r+s) A := (congrArg (fun e => e A) (dualAmbient_add r s)).symm
    _ = dualAmbient (s+r) A := by rw [add_comm]
    _ = _ := congrArg (fun e => e A) (dualAmbient_add s r)

theorem dualQuadraticIntegrand_transport (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (v : RegularHilbert H) (s : ℝ) :
    dualQuadraticIntegrand (dualAmbient r A) v s =
      dualQuadraticIntegrand A (characterMultiplier (-r) v) s := by
  unfold dualQuadraticIntegrand
  rw [dualAmbient_commute, dualAmbient_apply]
  have hq := operatorQuadratic_conjugate (dualAmbient s A)
    (star (characterMultiplier (H := H) r)) v
  simp only [characterMultiplier_star, neg_neg] at hq
  rw [characterMultiplier_star, hq]

theorem dualQuadraticIntegral_transport (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (dualAmbient r A) v =
      dualQuadraticIntegral A (characterMultiplier (-r) v) := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_transport]

/-- The output form is fixed by the implemented dual transport, including infinity. -/
theorem dualQuadraticIntegral_vector_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral A (characterMultiplier r v) = dualQuadraticIntegral A v := by
  have h := dualQuadraticIntegral_transport (-r) A v
  rw [neg_neg, dualQuadraticIntegral_dual_invariant] at h
  exact h.symm

theorem dualFiniteDomain_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (v : RegularHilbert H) :
    characterMultiplier r v ∈ (dualClosedPositiveForm A hA).finiteDomain ↔
      v ∈ (dualClosedPositiveForm A hA).finiteDomain := by
  change dualQuadraticIntegral A (characterMultiplier r v) < ⊤ ↔
    dualQuadraticIntegral A v < ⊤
  rw [dualQuadraticIntegral_vector_dual_invariant]

#print axioms operatorQuadratic_conjugate
#print axioms dualQuadraticIntegral_bimodule
#print axioms base_conjugate_mem
#print axioms dualBaseConjugatedForm
#print axioms dualBaseConjugatedForm_value
#print axioms dualAmbient_commute
#print axioms dualQuadraticIntegral_transport
#print axioms dualQuadraticIntegral_vector_dual_invariant
#print axioms dualFiniteDomain_dual_invariant
end
end TGLV350.Regular
