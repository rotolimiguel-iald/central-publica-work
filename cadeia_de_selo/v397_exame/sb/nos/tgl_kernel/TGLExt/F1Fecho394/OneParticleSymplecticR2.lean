import TGLExt.F1Fecho394.CanonicalOutput
/-! The existing canonical modular conjugation maps its fixed standard space
into the symplectic complement. Derived from the self-adjoint half-modular
operator, with its actual domain; not from a named locality assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.OneParticleSymplectic
open TGLExt.ImportedSQ F1Rede.CanonicalWedge ChatgptAudit.Continuous050

theorem TW_on_KWR (f : H1) (hf : f ∈ KWR.toClosedSubmodule) :
    ∃ hd : f ∈ TW.domain, TW ⟨f,hd⟩ = Jcandidate f := by
  obtain ⟨hd,hs⟩ := (KWR_mem f).mp hf
  refine ⟨hd,?_⟩
  change Jcandidate (TW ⟨f,hd⟩) = f at hs
  have h := congrArg Jcandidate hs
  simpa only [Jcandidate_involutive (TW ⟨f,hd⟩)] using h

theorem Jcandidate_into_symplectic (g : H1) (hg : g ∈ KWR.toClosedSubmodule) :
    Jcandidate g ∈ KWR.symplComp.toClosedSubmodule := by
  apply ClosedSubmodule.mem_symplComp_iff.mpr
  intro f hf
  obtain ⟨df,tf⟩ := TW_on_KWR f hf
  obtain ⟨dg,tg⟩ := TW_on_KWR g hg
  have hsym : TW.IsFormalAdjoint TW := by
    have h := LinearPMap.adjoint_isFormalAdjoint (T := TW) (WT_dense rootParameter)
    simpa only [LinearPMap.isSelfAdjoint_def.mp TW_selfadjoint] using h
  have hinner : inner ℂ (Jcandidate f) g = inner ℂ f (Jcandidate g) := by
    simpa only [tf,tg] using hsym ⟨f,df⟩ ⟨g,dg⟩
  have hanti : inner ℂ (Jcandidate f) g = star (inner ℂ f (Jcandidate g)) := by
    simpa only [Jcandidate_involutive g] using
      antiunitary_inner_conj Jcandidate f (Jcandidate g)
  have h := congrArg Complex.im (hinner.symm.trans hanti)
  simp only [Complex.star_def,Complex.conj_im] at h
  linarith

end F1Fecho.OneParticleSymplectic
#print axioms F1Fecho.OneParticleSymplectic.TW_on_KWR
#print axioms F1Fecho.OneParticleSymplectic.Jcandidate_into_symplectic
