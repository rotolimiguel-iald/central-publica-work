import TGLExt.F1Fecho394.RegularScalarGNSNormalityR2
import TGLExt.F1Fecho394.CanonicalFockGNSRepresentationR6
/-! The faithful actual regular-Fock GNS representation preserves directed
positive suprema. This is normality on this algebra, not a new modular or
scaled trace assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxSize 1024
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockGNSNormality
open TGLExt TGLV350.Regular
open scoped ComplexOrder
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation

local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)

theorem preserves_positive_isLUB
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → core.toStarSubalgebra) (B : core.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T) (hB : IsLUB (Set.range T) B) :
    IsLUB (Set.range (fun i => scalarGNSRepresentation (T i))) (scalarGNSRepresentation B) :=
  F1Fecho.RegularScalarGNSNormality.scalarGNSRepresentation_preserves_positive_isLUB
    (H := F1Rede.BosonicFock.F) weightContext T B hpos hmono hB

theorem preserves_positive_directed_isLUB
    (S : Set core.toStarSubalgebra) (B : core.toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B) :
    IsLUB (scalarGNSRepresentation '' S) (scalarGNSRepresentation B) :=
  F1Fecho.RegularScalarGNSNormality.scalarGNSRepresentation_preserves_positive_directed_isLUB
    (H := F1Rede.BosonicFock.F) weightContext S B hne hdir hpos hB

end F1Fecho.CanonicalFockGNSNormality
#print axioms F1Fecho.CanonicalFockGNSNormality.preserves_positive_isLUB
#print axioms F1Fecho.CanonicalFockGNSNormality.preserves_positive_directed_isLUB
