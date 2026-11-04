import TGLExt.F1Fecho394.VectorWedgeImaginaryPowersR4
import TGLExt.F1Fecho394.SpectralUnitaryTransportR1
import TGLExt.F1Fecho394.CanonicalOutput
import TGLExt.O16.SelfadjointSquareResolvent

/-! Existing canonical one-particle Tomita square: its actual CFC powers equal B0(-2*pi*t).
This theorem is on H1. No second-quantization interchange is assumed or asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.OneParticleBW
open TGLExt.ImportedSQ AuditF13v31 F1Rede.Canonical F1Rede.CanonicalWedge TGLV350.Regular
open ChatgptAudit.UnboundedTransform016

def R : H1→L[ℂ]H1 := pull (VectorWedgePowers.R rootParameter)
lemma R_eq : R=WA rootParameter*WA rootParameter := by
  change pull (VectorWedgePowers.R rootParameter)=_
  rw [VectorWedgePowers.R_eq,map_mul]
  rfl
lemma complement_eq : 1-R=WB rootParameter*WB rootParameter := by
  rw [R_eq]
  exact sub_eq_iff_eq_add.mpr (by simpa only [add_comm] using (WAB_square_sum rootParameter).symm)
lemma R_nonneg : 0≤R := map_nonneg pull (VectorWedgePowers.R_nonneg rootParameter)
lemma R_le_one : R≤1 := SpectralTransport.le_one Phi.symm _ (VectorWedgePowers.R_le_one rootParameter)
lemma R_injective : Function.Injective R :=
  SpectralTransport.injective Phi.symm _ (VectorWedgePowers.R_injective rootParameter)
lemma R_complement_injective : Function.Injective (1-R : H1→L[ℂ]H1) :=
  SpectralTransport.complement_injective Phi.symm _ (VectorWedgePowers.complement_injective rootParameter)

theorem square_eq : partialOperatorSquare TW=resolventGraphOperator R R_injective :=
  boundedGraph_square_eq_resolvent (WA rootParameter) (WB rootParameter) R
    (WA_injective rootParameter) R_injective (WAB_commute rootParameter) R_eq.symm complement_eq.symm

theorem R_is_actual : R=selfadjointSquareResolvent TW TW_selfadjoint := by
  ext1 x
  obtain ⟨u,hu,he⟩ := selfadjoint_square_resolvent_equation TW TW_selfadjoint x
  have hg := (partialOperatorSquare TW).mem_graph u
  have hg' : ((u:H1),partialOperatorSquare TW u) ∈ (resolventGraphOperator R R_injective).graph := by
    rw [← square_eq]
    exact hg
  have hq := (resolvent_graph_equation R R_injective _ _).mp hg'
  change (u:H1)-R u=R (partialOperatorSquare TW u) at hq
  calc
    R x=R ((u:H1)+partialOperatorSquare TW u) := congrArg R he.symm
    _= (u:H1) := by rw [map_add,← hq]; abel
    _= _ := hu

def modularFlow : ℝ→H1≃ₗᵢ[ℂ]H1 :=
  resolventImaginaryPower R R_nonneg R_le_one R_injective R_complement_injective

theorem modularFlow_eq_boost (t : ℝ) (f : H1) : modularFlow t f=B0 (-(2*Real.pi*t)) f := by
  have h := SpectralTransport.imaginaryPower Phi.symm
    (VectorWedgePowers.R (H:=TransverseFiber) rootParameter)
    (VectorWedgePowers.R_nonneg rootParameter) (VectorWedgePowers.R_le_one rootParameter)
    (VectorWedgePowers.R_injective rootParameter) (VectorWedgePowers.complement_injective rootParameter)
    t (Phi f)
  rw [VectorWedgePowers.imaginaryPower_eq_character] at h
  change Phi.symm (characterMultiplier (2*rootParameter*t) (Phi f))=
    modularFlow t (Phi.symm (Phi f)) at h
  rw [LinearIsometryEquiv.symm_apply_apply] at h
  rw [← h]
  apply Phi.injective
  rw [LinearIsometryEquiv.apply_symm_apply,canonicalPartialFourier_boost]
  congr 1
  unfold rootParameter
  ring

end F1Fecho.OneParticleBW
#print axioms F1Fecho.OneParticleBW.square_eq
#print axioms F1Fecho.OneParticleBW.R_is_actual
#print axioms F1Fecho.OneParticleBW.modularFlow_eq_boost
