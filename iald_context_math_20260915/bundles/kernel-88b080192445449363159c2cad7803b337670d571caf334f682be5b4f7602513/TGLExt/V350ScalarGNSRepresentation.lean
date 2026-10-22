import TGLExt.V350ScalarGNSCompletion
import TGLExt.V350DualOrbitRepresentation
import TGLExt.V350ReducingStarRepresentation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

def scalarGNSRepresentation (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →⋆ₐ[ℂ]
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (regularCoreAlgebra P).toStarSubalgebra.subtype)
    (scalarGNSSubspace P) (scalarGNSAmbientAction_preserves P)

theorem scalarGNSEmbedding_denseRange (P : SiteProfile) :
    DenseRange (scalarGNSEmbedding P) := by
  let f := scalarGNSLinear P
  have h : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  exact h.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

theorem scalarGNSRepresentation_zero_iff (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    scalarGNSRepresentation P B = 0 ↔ B = 0 := by
  constructor
  · intro hB
    have hann : ∀ A : finiteDualLeftIdeal P, B.val * A.val.val = 0 := by
      intro A
      have he : scalarGNSEmbedding P (scalarGNSLeftProduct P B A) = scalarGNSEmbedding P 0 :=
        calc
          _ = scalarGNSRepresentation P B (scalarGNSEmbedding P A) :=
            (scalarGNSAction_intertwines P B A).symm
          _ = 0 := congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
            T (scalarGNSEmbedding P A)) hB
          _ = _ := (scalarGNSEmbedding P).map_zero.symm
      have hz := scalarGNSEmbedding_injective P he
      exact congrArg (fun A : finiteDualLeftIdeal P => A.val.val) hz
    apply Subtype.ext
    ext1 v
    change B.val v = 0
    have hlim := (finiteDualLeftIdeal_strong_approximation P B).2.2 v
    have he : (fun h : ℝ => (B.val * regularAverage P h) v) =ᶠ[𝓝[>] 0] (fun _ => 0) := by
      filter_upwards [self_mem_nhdsWithin] with h hh
      have hz := hann ⟨⟨regularAverage P h,regularAverage_mem P h⟩,
        regularAverage_hasFiniteDualSquare P h hh⟩
      exact congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ] _ => T v) hz
    have hzlim : Tendsto (fun h : ℝ => (B.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 0) :=
      tendsto_const_nhds.congr' he.symm
    exact _root_.tendsto_nhds_unique (f := fun h : ℝ => (B.val * regularAverage P h) v)
      (l := 𝓝[>] (0 : ℝ)) hlim hzlim
  · rintro rfl
    exact map_zero (scalarGNSRepresentation P)

theorem scalarGNSRepresentation_injective (P : SiteProfile) :
    Function.Injective (scalarGNSRepresentation P) := by
  intro B C h
  apply sub_eq_zero.mp
  apply (scalarGNSRepresentation_zero_iff P (B-C)).mp
  rw [map_sub,h,sub_self]

#print axioms scalarGNSRepresentation
#print axioms scalarGNSEmbedding_denseRange
#print axioms scalarGNSRepresentation_zero_iff
#print axioms scalarGNSRepresentation_injective
end
end TGLV350.Regular
