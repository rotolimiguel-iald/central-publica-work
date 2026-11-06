import TGLExt.V350FixedCoreBaseIdentification
import TGLExt.V350BoundedFiniteSquares

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology ENNReal
noncomputable section

/-- Bounded dual-integral values are actual positive elements of the original
base, represented in the same regular core by fibre amplification. -/
theorem exists_boundedDualValue_in_base (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) (c : ℝ) (hc : 0 ≤ c)
    (hbound : ∀ v, dualQuadraticIntegral A v ≤ ENNReal.ofReal (c * ‖v‖ ^ 2)) :
    ∃ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D ∧
      ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (fibre D.val v)).re := by
  obtain ⟨B,hmB,hB,_,hrep⟩ := exists_boundedDualValue_in_fixedCore P A hm hA c hc hbound
  obtain ⟨D,hmD,he⟩ := (dualFixedCore_eq_amplified_base P B).mp hmB
  subst B
  exact ⟨⟨D,hmD⟩,(fibre_nonneg_iff D).mp hB,hrep⟩

theorem HasFiniteDualSquare.exists_base_value (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hf : HasFiniteDualSquare A) :
    ∃ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D ∧
      ∀ v, dualQuadraticIntegral (star A * A) v =
        ENNReal.ofReal (inner ℂ v (fibre D.val v)).re := by
  obtain ⟨B,hmB,hB,hrep⟩ := HasFiniteDualSquare.exists_bounded_value P A hm hf
  obtain ⟨D,hmD,he⟩ := (dualFixedCore_eq_amplified_base P B).mp hmB
  subst B
  exact ⟨⟨D,hmD⟩,(fibre_nonneg_iff D).mp hB,hrep⟩

theorem boundedBaseDualValue_unique (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (D E : (theFactorObject P).toStarSubalgebra) (hD : 0 ≤ D) (hE : 0 ≤ E)
    (hd : ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (fibre D.val v)).re)
    (he : ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (fibre E.val v)).re) : D = E := by
  apply Subtype.ext
  apply fibre_injective
  exact boundedDualValue_unique A _ _ (fibre_nonneg hD) (fibre_nonneg hE) hd he

/-- Strong density of square-finite inputs with bounded positive values in M.
The general extended-positive/predual weight interface remains separate. -/
theorem finiteBaseValues_strong_approximation (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → ∃ D : (theFactorObject P).toStarSubalgebra, 0 ≤ D ∧
      ∀ v, dualQuadraticIntegral
          (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) v =
        ENNReal.ofReal (inner ℂ v (fibre D.val v)).re) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
  obtain ⟨hf,hm,ht⟩ := finiteDualLeftIdeal_strong_approximation P A
  exact ⟨fun h hh => HasFiniteDualSquare.exists_base_value P _ (hm h) (hf h hh),hm,ht⟩

#print axioms exists_boundedDualValue_in_base
#print axioms HasFiniteDualSquare.exists_base_value
#print axioms boundedBaseDualValue_unique
#print axioms finiteBaseValues_strong_approximation
end
end TGLV350.Regular
