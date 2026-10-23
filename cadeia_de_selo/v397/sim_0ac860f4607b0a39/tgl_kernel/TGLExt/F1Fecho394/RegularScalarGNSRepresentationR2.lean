import TGLExt.F1Fecho394.RegularScalarGNSActionR2
import TGLExt.V350DualOrbitRepresentation
import TGLExt.V350ReducingStarRepresentation
/-! The genuine reducing star representation on the scalar-weight completion.
Vanishing of the represented operator annihilates the original finite ideal;
strong density of that ideal will provide faithfulness in the concrete model. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarGNSRepresentation
open TGLV350.Regular MeasureTheory Filter F1Fecho.RegularScalarGNS F1Fecho.RegularScalarGNSAction
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)

def scalarGNSRepresentation : D.algebra.toStarSubalgebra →⋆ₐ[ℂ]
    (GNSHilbert D →L[ℂ] GNSHilbert D) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp D.algebra.toStarSubalgebra.subtype)
    (GNSSubspace D) (scalarGNSAmbientAction_preserves D)

theorem GNSEmbedding_denseRange : DenseRange (GNSEmbedding D) := by
  let f := scalarGNSLinear D
  have h : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  exact h.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

theorem zero_annihilates_finite (B : D.algebra.toStarSubalgebra)
    (hB : scalarGNSRepresentation D B = 0) (A : finiteIdeal D) : B.val*A.val.val=0 := by
  have he : GNSEmbedding D (scalarGNSLeftProduct D B A) = GNSEmbedding D 0 :=
    calc
      _ = scalarGNSRepresentation D B (GNSEmbedding D A) :=
        (scalarGNSAction_intertwines D B A).symm
      _ = 0 := congrArg (fun T : GNSHilbert D →L[ℂ] GNSHilbert D => T (GNSEmbedding D A)) hB
      _ = _ := (GNSEmbedding D).map_zero.symm
  have hz := GNSEmbedding_injective D he
  exact congrArg (fun A : finiteIdeal D => A.val.val) hz

end F1Fecho.RegularScalarGNSRepresentation
#print axioms F1Fecho.RegularScalarGNSRepresentation.scalarGNSRepresentation
#print axioms F1Fecho.RegularScalarGNSRepresentation.GNSEmbedding_denseRange
#print axioms F1Fecho.RegularScalarGNSRepresentation.zero_annihilates_finite
