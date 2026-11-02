import TGLExt.V350ScalarGaussianImage
import TGLExt.V350BoundedInjectivePolar

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section

def scalarGaussianImageRepresentation (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →⋆ₐ[ℂ]
      (scalarGaussianImage P →L[ℂ] scalarGaussianImage P) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (regularCoreAlgebra P).toStarSubalgebra.subtype)
    (scalarGaussianImage P) (scalarGaussianImage_invariant P)

theorem scalarGaussianImageMap_intertwines (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (scalarGaussianImageMap P).comp (scalarGNSRepresentation P A) =
      (scalarGaussianImageRepresentation P A).comp (scalarGaussianImageMap P) := by
  ext1 v
  apply Subtype.ext
  exact scalarGaussianGNSMap_intertwines P A v

/-- A linear unitary between H_I and the actual Gaussian image closure.
This is not scalarTomitaPolarFactor and does not identify two Tomita operators. -/
def scalarGaussianUnitary (P : SiteProfile) :
    ScalarGNSHilbert P ≃ₗᵢ[ℂ] scalarGaussianImage P :=
  boundedInjectivePolar (scalarGaussianImageMap P)
    (scalarGaussianImageMap_injective P) (scalarGaussianImageMap_denseRange P)

theorem scalarGaussianUnitary_intertwines (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    scalarGaussianUnitary P (scalarGNSRepresentation P A v) =
      scalarGaussianImageRepresentation P A (scalarGaussianUnitary P v) := by
  apply boundedInjectivePolar_intertwines
  · exact scalarGaussianImageMap_intertwines P A
  · simpa only [← map_star] using scalarGaussianImageMap_intertwines P (star A)

/-- The auxiliary vector lies in the original scalar-weight GNS space.
Its own modular objects are not identified with those of the original weight. -/
def scalarGNSCyclicVector (P : SiteProfile) : ScalarGNSHilbert P :=
  (scalarGaussianUnitary P).symm ⟨scalarGaussianVacuum P,scalarGaussianVacuum_mem_image P⟩

theorem scalarGNSCyclicVector_image (P : SiteProfile) :
    scalarGaussianUnitary P (scalarGNSCyclicVector P) =
      ⟨scalarGaussianVacuum P,scalarGaussianVacuum_mem_image P⟩ :=
  (scalarGaussianUnitary P).apply_symm_apply _

theorem scalarGNSCyclicVector_separating (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra)
    (h : scalarGNSRepresentation P A (scalarGNSCyclicVector P) = 0) : A = 0 := by
  have he := congrArg (scalarGaussianUnitary P) h
  rw [scalarGaussianUnitary_intertwines,scalarGNSCyclicVector_image,map_zero] at he
  apply Subtype.ext
  exact scalarGaussianVacuum_separating P A.val A.property (congrArg Subtype.val he)

def scalarGaussianOrbitEmbedding (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →ₗ[ℂ] scalarGaussianImage P :=
  (scalarGaussianOrbitLinear P).codRestrict (scalarGaussianImage P) (fun A =>
    scalarGaussianImage_invariant P A _ (scalarGaussianVacuum_mem_image P))

theorem scalarGaussianOrbitEmbedding_denseRange (P : SiteProfile) :
    DenseRange (scalarGaussianOrbitEmbedding P) := by
  let f := scalarGaussianOrbitLinear P
  have hd : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  have hc : DenseRange (fun A =>
      (⟨f A,subset_closure (Set.mem_range_self A)⟩ :
        ↥((f.range.topologicalClosure : Submodule ℂ _)))) :=
    hd.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)
  have htransport : ∀ (S : Submodule ℂ _) (he : S = f.range.topologicalClosure)
      (hm : ∀ A, f A ∈ S), DenseRange (f.codRestrict S hm) := by
    intro S he hm
    subst S
    exact hc
  exact htransport (scalarGaussianImage P) (scalarGaussianImage_eq_orbit P) _

theorem scalarGNSCyclicVector_cyclic (P : SiteProfile) :
    DenseRange (fun A : (regularCoreAlgebra P).toStarSubalgebra =>
      scalarGNSRepresentation P A (scalarGNSCyclicVector P)) := by
  have hd := (scalarGaussianUnitary P).symm.surjective.denseRange.comp
    (scalarGaussianOrbitEmbedding_denseRange P) (scalarGaussianUnitary P).symm.continuous
  have he : (fun A : (regularCoreAlgebra P).toStarSubalgebra =>
      (scalarGaussianUnitary P).symm (scalarGaussianOrbitEmbedding P A)) =
      (fun A => scalarGNSRepresentation P A (scalarGNSCyclicVector P)) := by
    funext A
    apply (scalarGaussianUnitary P).injective
    rw [(scalarGaussianUnitary P).apply_symm_apply,scalarGaussianUnitary_intertwines,
      scalarGNSCyclicVector_image]
    rfl
  exact he ▸ hd

#print axioms scalarGaussianImageRepresentation
#print axioms scalarGaussianImageMap_intertwines
#print axioms scalarGaussianUnitary
#print axioms scalarGaussianUnitary_intertwines
#print axioms scalarGNSCyclicVector
#print axioms scalarGNSCyclicVector_image
#print axioms scalarGNSCyclicVector_separating
#print axioms scalarGaussianOrbitEmbedding
#print axioms scalarGaussianOrbitEmbedding_denseRange
#print axioms scalarGNSCyclicVector_cyclic
end
end TGLV350.Regular
