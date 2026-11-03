import TGLExt.F1Fecho394.CanonicalFockCoefficientDenseR6
/-! Concrete normalized-Fourier isometry into the actual GNS. This construction
uses only the already proved inclusion and does not require surjectivity. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientGNS
open F1Rede.BosonicFock
open TGLV350.Regular F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.RegularNormalizedFourier

def coefficientEmbedding : RegularHilbert F →ₗᵢ[ℂ] GNSHilbert where
  toFun f := ⟨spectralCode f,spectralCode_mem_GNS f⟩
  map_add' f g := Subtype.ext (spectralCode.map_add f g)
  map_smul' c f := Subtype.ext (spectralCode.map_smul c f)
  norm_map' f := spectralCode.norm_map f

theorem coefficientEmbedding_coe (f:RegularHilbert F) :
    (coefficientEmbedding f).val=spectralCode f := rfl

theorem coefficientEmbedding_injective : Function.Injective coefficientEmbedding :=
  coefficientEmbedding.injective
end F1Fecho.CanonicalFockCoefficientGNS
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientEmbedding
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientEmbedding_coe
#print axioms F1Fecho.CanonicalFockCoefficientGNS.coefficientEmbedding_injective
