import TGLExt.V351BaseFunctionalWeightLaws

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV351
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal ComplexOrder
noncomputable section

theorem positive_base_functional_real_mono (P : SiteProfile)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ)
    (hψ : ∀ D, 0 ≤ D → 0 ≤ ψ D) :
    Monotone (fun D => ENNReal.ofReal (ψ D).re) := by
  intro A B hAB
  have hp := (Complex.nonneg_iff.mp (hψ (B-A) (sub_nonneg.mpr hAB))).1
  rw [map_sub, Complex.sub_re] at hp
  exact ENNReal.ofReal_le_ofReal (sub_nonneg.mp hp)

/-- A represented functional is positive in the complex order, not only in
the real part. HasSum forbids assigning zero to a divergent series. -/
theorem baseSeriesFunctional_positive (P : SiteProfile)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) :
    ∀ D, 0 ≤ D → 0 ≤ ψ D := by
  intro D hD
  rw [← (hrep D).tsum_eq]
  exact tsum_nonneg (fun k => baseVectorFunctional_positive P (v k) D hD)

/-- The normality of a vector evaluation follows from the existing strong
limit theorem on the same base, for every nonempty directed index type. -/
theorem baseVectorFunctional_normal (P : SiteProfile) (v : TowerHilbert P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (theFactorObject P).toStarSubalgebra)
    (S : (theFactorObject P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    ENNReal.ofReal (inner ℂ v (S.val v)).re =
      ⨆ i, ENNReal.ofReal (inner ℂ v ((A i).val v)).re := by
  have hbound : ∀ i, ‖(A i).val‖ ≤ ‖S.val‖ := fun i =>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hS.1 (Set.mem_range_self i))
  obtain ⟨D, _, _, hstrong, _, hD⟩ := vonNeumann_exists_positive_isLUB
    (theFactorObject P) A hpos hmono ‖S.val‖ (norm_nonneg _) hbound
  have hDS : D = S := hD.unique hS
  subst D
  have ht : Tendsto (fun i => ENNReal.ofReal (inner ℂ v ((A i).val v)).re) atTop
      (𝓝 (ENNReal.ofReal (inner ℂ v (S.val v)).re)) :=
    ENNReal.continuous_ofReal.continuousAt.tendsto.comp
      (Complex.continuous_re.continuousAt.tendsto.comp
        (tendsto_const_nhds.inner (hstrong v)))
  apply le_antisymm
  · apply le_of_tendsto ht
    exact Eventually.of_forall (fun i =>
      le_iSup (fun j => ENNReal.ofReal (inner ℂ v ((A j).val v)).re) i)
  · apply iSup_le
    intro i
    exact positive_base_functional_real_mono P (baseVectorFunctional P v)
      (baseVectorFunctional_positive P v) (hS.1 (Set.mem_range_self i))

/-- Normality in the base argument of the functional itself. This is distinct
from normality of A -> m_A(psi) in the regular core. No converse coverage theorem
or separability of the Hilbert space is assumed. -/
theorem baseSeriesFunctional_normal (P : SiteProfile)
    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)
    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,
      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D))
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (theFactorObject P).toStarSubalgebra)
    (S : (theFactorObject P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    ENNReal.ofReal (ψ S).re = ⨆ i, ENNReal.ofReal (ψ (A i)).re := by
  have hSpos : 0 ≤ S :=
    (hpos (Classical.arbitrary ι)).trans (hS.1 (Set.mem_range_self _))
  rw [baseFunctional_hasSum_positive_evaluation P ψ v hrep S hSpos]
  simp_rw [baseFunctional_hasSum_positive_evaluation P ψ v hrep _ (hpos _)]
  simp_rw [baseVectorFunctional_normal P _ A S hpos hmono hS]
  exact ennreal_tsum_iSup_directed _ (fun k =>
    (positive_base_functional_real_mono P (baseVectorFunctional P (v k))
      (baseVectorFunctional_positive P (v k))).comp hmono)

#print axioms positive_base_functional_real_mono
#print axioms baseSeriesFunctional_positive
#print axioms baseVectorFunctional_normal
#print axioms baseSeriesFunctional_normal
end
end TGLV351
