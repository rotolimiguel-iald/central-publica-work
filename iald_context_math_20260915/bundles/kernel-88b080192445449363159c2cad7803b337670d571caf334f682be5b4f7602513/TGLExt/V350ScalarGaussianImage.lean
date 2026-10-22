import TGLExt.V350ScalarGaussianGNSMap
import TGLExt.V350DualOrbitStrongLimits

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- The actual closed image of the bounded Gaussian map; no claim that
Gaussian multiplication preserves the original H_I is used. -/
def scalarGaussianImage (P : SiteProfile) :
    Submodule ℂ (RegularHilbert (RegularHilbert (TowerHilbert P))) :=
  (scalarGaussianGNSMap P).range.topologicalClosure

instance scalarGaussianImage_complete (P : SiteProfile) : CompleteSpace (scalarGaussianImage P) :=
  Submodule.topologicalClosure.completeSpace (scalarGaussianGNSMap P).range

theorem scalarGaussianImage_invariant (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    ∀ v ∈ scalarGaussianImage P, dualOrbitRepresentation A.val v ∈ scalarGaussianImage P := by
  have h : Set.MapsTo (dualOrbitRepresentation A.val)
      ((scalarGaussianGNSMap P).range : Set _)
      ((scalarGaussianGNSMap P).range : Set _) := by
    rintro _ ⟨v,rfl⟩
    exact ⟨scalarGNSRepresentation P A v,scalarGaussianGNSMap_intertwines P A v⟩
  exact h.closure (dualOrbitRepresentation A.val).continuous

/-- Finite-square regular averages place the Gaussian vacuum in the image
closure. The value at h=0 is never used as an approximation to the identity. -/
theorem scalarGaussianVacuum_mem_image (P : SiteProfile) :
    scalarGaussianVacuum P ∈ scalarGaussianImage P := by
  have ht := dualOrbit_tendsto_of_uniformly_bounded (regularAverage P) 1 1
    (regularAverage_norm_le_one P) (regularAverage_tendsto_identity P)
    (scalarGaussianVacuum P)
  have ht' : Tendsto (fun h : ℝ =>
      dualOrbitRepresentation (regularAverage P h) (scalarGaussianVacuum P))
      (𝓝[>] (0 : ℝ)) (𝓝 (scalarGaussianVacuum P)) := by
    simpa only [map_one,one_apply_eq_self] using
      ht.mono_left (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply (scalarGaussianGNSMap P).range.isClosed_topologicalClosure.mem_of_tendsto ht'
  filter_upwards [self_mem_nhdsWithin] with h hh
  let a : finiteDualLeftIdeal P := ⟨⟨regularAverage P h,regularAverage_mem P h⟩,
    regularAverage_hasFiniteDualSquare P h hh⟩
  apply (scalarGaussianGNSMap P).range.le_topologicalClosure
  exact ⟨scalarGNSEmbedding P a,scalarGaussianGNSMap_embedding P a⟩

def scalarGaussianOrbitLinear (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →ₗ[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) where
  toFun A := dualOrbitRepresentation A.val (scalarGaussianVacuum P)
  map_add' A B := by simp
  map_smul' c A := by simp

theorem scalarGaussianImage_eq_orbit (P : SiteProfile) :
    scalarGaussianImage P = (scalarGaussianOrbitLinear P).range.topologicalClosure := by
  apply le_antisymm
  · apply Submodule.topologicalClosure_minimal
    · rintro _ ⟨v,rfl⟩
      refine (scalarGNSEmbedding_denseRange P).induction ?_
        ((scalarGaussianOrbitLinear P).range.isClosed_topologicalClosure.preimage
          (scalarGaussianGNSMap P).continuous) v
      rintro _ ⟨a,rfl⟩
      change scalarGaussianGNSMap P (scalarGNSEmbedding P a) ∈ _
      rw [scalarGaussianGNSMap_embedding]
      exact (scalarGaussianOrbitLinear P).range.le_topologicalClosure ⟨a.val,rfl⟩
    · exact (scalarGaussianOrbitLinear P).range.isClosed_topologicalClosure
  · apply Submodule.topologicalClosure_minimal
    · rintro _ ⟨A,rfl⟩
      exact scalarGaussianImage_invariant P A _ (scalarGaussianVacuum_mem_image P)
    · exact (scalarGaussianGNSMap P).range.isClosed_topologicalClosure

def scalarGaussianImageMap (P : SiteProfile) :
    ScalarGNSHilbert P →L[ℂ] scalarGaussianImage P :=
  (scalarGaussianGNSMap P).codRestrict (scalarGaussianImage P)
    (fun v => (scalarGaussianGNSMap P).range.le_topologicalClosure ⟨v,rfl⟩)

theorem scalarGaussianImageMap_injective (P : SiteProfile) :
    Function.Injective (scalarGaussianImageMap P) := by
  intro x y h
  exact scalarGaussianGNSMap_injective P (congrArg Subtype.val h)

theorem scalarGaussianImageMap_denseRange (P : SiteProfile) :
    DenseRange (scalarGaussianImageMap P) := by
  let f := scalarGaussianGNSMap P
  have h : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  exact h.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

#print axioms scalarGaussianImage
#print axioms scalarGaussianImage_complete
#print axioms scalarGaussianImage_invariant
#print axioms scalarGaussianVacuum_mem_image
#print axioms scalarGaussianOrbitLinear
#print axioms scalarGaussianImage_eq_orbit
#print axioms scalarGaussianImageMap
#print axioms scalarGaussianImageMap_injective
#print axioms scalarGaussianImageMap_denseRange
end
end TGLV350.Regular
