import TGLExt.F1Fecho394.CanonicalWedge
import TGLExt.F1Fecho394.VectorSquare
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
open MeasureTheory Filter
namespace F1Rede.CanonicalWedge
open TGLExt.ImportedSQ AuditF13v31 F1Rede.Canonical
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050

theorem WT_double_graph_iff (c : ℝ) (f g : H1) : (f,g) ∈ (WT (2*c)).graph ↔
    ∃ h : H1, (f,h) ∈ (WT c).graph ∧ (h,g) ∈ (WT c).graph := by
  rw [WT_graph,Wedge.T_double_graph_iff]
  constructor
  · rintro ⟨h,hfh,hhg⟩
    refine ⟨Phi.symm h, ?_, ?_⟩
    · apply (WT_graph c f (Phi.symm h)).mpr
      simpa only [LinearIsometryEquiv.apply_symm_apply] using hfh
    · apply (WT_graph c (Phi.symm h) g).mpr
      simpa only [LinearIsometryEquiv.apply_symm_apply] using hhg
  · rintro ⟨h,hfh,hhg⟩
    exact ⟨Phi h,(WT_graph c f h).mp hfh,(WT_graph c h g).mp hhg⟩

def DeltaCandidate : H1 →ₗ.[ℂ] H1 := WT (2*rootParameter)

theorem delta_multiplier : IsMultiplierAfter Phi canonicalSigma DeltaCandidate := by
  intro f g
  rw [DeltaCandidate,WT_graph,Wedge.T_graph]
  have he : ∀ x : ℝ, -(2*rootParameter)*x = canonicalSigma x := by
    intro x
    unfold rootParameter canonicalSigma
    ring
  simp only [he]

theorem delta_is_SdagS : IsTomitaSquare TW Jcandidate DeltaCandidate := by
  intro f g
  change (f,g) ∈ (WT (2*rootParameter)).graph ↔ _
  rw [WT_double_graph_iff]
  constructor
  · rintro ⟨m,hfm,hmg⟩
    obtain ⟨u,hu⟩ := (TW.mem_graph_iff').mp hfm
    obtain ⟨v,hv⟩ := (TW.mem_graph_iff').mp hmg
    have huf : (u:H1) = f := congrArg Prod.fst hu
    have hum : TW u = m := congrArg Prod.snd hu
    have hvm : (v:H1) = m := congrArg Prod.fst hv
    have hvg : TW v = g := congrArg Prod.snd hv
    have hf : f ∈ TW.domain := huf ▸ u.property
    have hTu : TW ⟨f,hf⟩ = m := by simpa only [← huf] using hum
    have hm : m ∈ TW.domain := hvm ▸ v.property
    have hTf : TW ⟨f,hf⟩ ∈ TW.domain := hTu.symm ▸ hm
    refine ⟨hf,(generic_composition_domain TW Jcandidate Jcandidate_involutive ⟨f,hf⟩).mpr hTf,?_⟩
    have hv' : (⟨TW ⟨f,hf⟩,hTf⟩ : TW.domain) = v := Subtype.ext (hTu.trans hvm.symm)
    exact (generic_adjoint_comp TW Jcandidate Jcandidate_involutive ⟨f,hf⟩ hTf).trans
      ((congrArg TW hv').trans hvg)
  · rintro ⟨hf,hSf,hg⟩
    have hTf := (generic_composition_domain TW Jcandidate Jcandidate_involutive ⟨f,hf⟩).mp hSf
    have hval : TW ⟨TW ⟨f,hf⟩,hTf⟩ = g :=
      (generic_adjoint_comp TW Jcandidate Jcandidate_involutive ⟨f,hf⟩ hTf).symm.trans hg
    refine ⟨TW ⟨f,hf⟩,TW.mem_graph ⟨f,hf⟩,?_⟩
    rw [← hval]
    exact TW.mem_graph ⟨TW ⟨f,hf⟩,hTf⟩

/-- Concrete inhabitant of the D1a.3 spectral contract on unchanged canonical H1.
The geometric localization and full Poincare net are separate obligations, not asserted here.
T is moreover proved POSITIVE below, rather than merely self-adjoint as the old interface requires. -/
def spectralOutput : D1a3OutputBGL where
  Fub := canonicalFub
  J := Jcandidate
  J_involutive := Jcandidate_involutive
  T := TW
  T_selfadjoint := TW_selfadjoint
  σ := canonicalSigma
  hclosed := SW_closed
  hmaps := SW_maps
  hinv := SW_involutive
  hdense := WT_dense rootParameter
  Δ := DeltaCandidate
  delta_is_SdagS := delta_is_SdagS
  delta_multiplier := delta_multiplier
  modular_is_boost := canonical_modularGroupIsBoost

theorem spectralOutput_positive (f : spectralOutput.T.domain) :
    0 ≤ (inner ℂ (f:H1) (spectralOutput.T f)).re := TW_positive f

theorem spectralOutput_nonzero : ∃ f : H1,
    f ∈ spectralOutput.KWR.toClosedSubmodule ∧ f ≠ 0 := spectralOutput.exists_nonzero

theorem spectralOutput_tomita (h k : H1)
    (hh : h ∈ spectralOutput.KWR.toClosedSubmodule) (hk : k ∈ spectralOutput.KWR.toClosedSubmodule) :
    ∃ hd : h + Complex.I • k ∈ TW.domain,
      SW TW Jcandidate ⟨h + Complex.I • k,hd⟩ = h - Complex.I • k :=
  spectralOutput.S_is_tomita_of_K h k hh hk

#print axioms WT_double_graph_iff
#print axioms delta_multiplier
#print axioms delta_is_SdagS
#print axioms spectralOutput
#print axioms spectralOutput_positive
#print axioms spectralOutput_nonzero
#print axioms spectralOutput_tomita
end F1Rede.CanonicalWedge
