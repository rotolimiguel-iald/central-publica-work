import TGLExt.F1Fecho394.CanonicalFockGNSR5
import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
/-! The actual regular Fock core acts faithfully on its scalar dual-weight
GNS space. The representation is constructed from its dual orbit; faithfulness
uses the actual strongly convergent finite-square averages. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockGNSRepresentation
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS
open scoped Topology

abbrev scalarGNSRepresentation :=
  F1Fecho.RegularScalarGNSRepresentation.scalarGNSRepresentation weightContext

theorem scalarGNSEmbedding_denseRange : DenseRange GNSEmbedding :=
  F1Fecho.RegularScalarGNSRepresentation.GNSEmbedding_denseRange weightContext

theorem scalarGNSRepresentation_zero_iff (B : core.toStarSubalgebra) :
    scalarGNSRepresentation B = 0 ↔ B = 0 := by
  constructor
  · intro hB
    have hann : ∀ A : finiteLeftIdeal, B.val * A.val.val = 0 :=
      F1Fecho.RegularScalarGNSRepresentation.zero_annihilates_finite weightContext B hB
    apply Subtype.ext
    ext1 v
    change B.val v = 0
    have hlim := (finite_square_strong_density B).2.2 v
    have he : (fun h : ℝ => (B.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v)
        =ᶠ[𝓝[>] 0] (fun _ => 0) := by
      filter_upwards [self_mem_nhdsWithin] with h hh
      have hz := hann ⟨⟨F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
        F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h⟩,
        F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh⟩
      exact congrArg (fun T : RegularHilbert F →L[ℂ] _ => T v) hz
    have hzlim : Tendsto (fun h : ℝ => (B.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v)
        (𝓝[>] 0) (𝓝 0) := tendsto_const_nhds.congr' he.symm
    exact _root_.tendsto_nhds_unique hlim hzlim
  · rintro rfl
    exact map_zero scalarGNSRepresentation

theorem scalarGNSRepresentation_injective : Function.Injective scalarGNSRepresentation :=
  (injective_iff_map_eq_zero' scalarGNSRepresentation).2 scalarGNSRepresentation_zero_iff

end F1Fecho.CanonicalFockGNSRepresentation
#print axioms F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
#print axioms F1Fecho.CanonicalFockGNSRepresentation.scalarGNSEmbedding_denseRange
#print axioms F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation_zero_iff
#print axioms F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation_injective
