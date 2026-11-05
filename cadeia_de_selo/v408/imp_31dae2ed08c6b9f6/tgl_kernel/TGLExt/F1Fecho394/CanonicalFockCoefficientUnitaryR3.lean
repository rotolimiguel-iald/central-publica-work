import TGLExt.F1Fecho394.CanonicalFockSpectralGNSR6
import TGLExt.F1Fecho394.CanonicalFockCoefficientEmbeddingR2
/-! The same normalized Fourier coefficient isometry onto the actual GNS.
Both image inclusions are imported from their proved consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientGNS
open F1Rede.BosonicFock
open TGLV350.Regular F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.RegularNormalizedFourier F1Fecho.CanonicalFockSpectralGNS
theorem GNS_eq_spectralCode_range :
    (GNSSubspace : Set (RegularHilbert (RegularHilbert F)))=Set.range (spectralCode (H:=F)) := by
  apply Set.Subset.antisymm GNS_subset_spectralCode
  rintro _ ⟨f,rfl⟩
  exact spectralCode_mem_GNS f

theorem coefficientEmbedding_surjective : Function.Surjective coefficientEmbedding := by
  intro x
  have hmem : x.val ∈ Set.range (spectralCode (H:=F)) :=
    GNS_subset_spectralCode x.property
  change ∃ f : RegularHilbert F, spectralCode f = x.val at hmem
  exact ⟨Classical.choose hmem, Subtype.ext (Classical.choose_spec hmem)⟩

def coefficientUnitary : RegularHilbert F ≃ₗᵢ[ℂ] GNSHilbert :=
  LinearIsometryEquiv.ofSurjective coefficientEmbedding coefficientEmbedding_surjective

theorem coefficientUnitary_coe (f : RegularHilbert F) :
    (coefficientUnitary f).val=spectralCode f := rfl

end F1Fecho.CanonicalFockCoefficientGNS
#print axioms F1Fecho.CanonicalFockCoefficientGNS.GNS_eq_spectralCode_range
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientEmbedding_surjective
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientUnitary_coe
